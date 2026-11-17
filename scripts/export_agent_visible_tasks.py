#!/usr/bin/env python3
"""Create an agent-visible task handoff, excluding all oracle, solution and hint fields."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

SHA40 = re.compile(r"^[0-9a-f]{40}$")
VISIBLE = frozenset(("instance_id", "repo", "base_commit", "problem_statement"))

def extract_visible(frame: dict, source_rows: list[dict]) -> list[dict]:
    chosen = frame.get("selected")
    if not isinstance(chosen, list) or len(chosen) != 10:
        raise ValueError("Precommitted frame must contain exactly ten selected instances")
    expected = {r["instance_id"]: r["repo"] for r in chosen}
    if len(expected) != len(chosen):
        raise ValueError("Duplicate frame instance ID")
    seen: dict[str, dict] = {}
    for row in source_rows:
        if not isinstance(row, dict):
            raise ValueError("Unexpected dataset record")
        iid = row.get("instance_id")
        if iid not in expected:
            continue
        if iid in seen:
            raise ValueError("Duplicate dataset instance")
        info = {key: row.get(key) for key in VISIBLE}
        if info["repo"] != expected[iid]:
            raise ValueError("Repository mismatch with frozen frame")
        if not isinstance(info["base_commit"], str) or not SHA40.fullmatch(info["base_commit"]):
            raise ValueError("Invalid source base commit")
        if not isinstance(info["problem_statement"], str) or not info["problem_statement"].strip():
            raise ValueError("Missing public task problem statement")
        # Build a new object from the explicit allow-list.
        info["problem_sha256"] = hashlib.sha256(info["problem_statement"].encode("utf-8")).hexdigest()
        seen[iid] = info
    if set(seen) != set(expected):
        raise ValueError("Missing instances: no replacement or selective deletion permitted")
    return [seen[r["instance_id"]] for r in chosen]

def save_visible(frame: dict, source_rows: list[dict], path: Path) -> list[dict]:
    result = extract_visible(frame, source_rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise ValueError("Refuse to overwrite a visible-task export")
    path.write_text("".join(json.dumps(x, ensure_ascii=False, sort_keys=True)+"\n" for x in result), encoding="utf-8")
    return result

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--frame", type=Path, required=True)
    p.add_argument("--rows", type=Path, required=True, help="Original dataset JSONL; do not print/release")
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    frame=json.loads(a.frame.read_text(encoding="utf-8"))
    raw=[json.loads(x) for x in a.rows.read_text(encoding="utf-8").splitlines() if x.strip()]
    out=save_visible(frame,raw,a.out)
    print(json.dumps({"selected":len(out),"allowed_keys":sorted(VISIBLE|{"problem_sha256"}),"hidden_labels_exported":False},indent=2))
