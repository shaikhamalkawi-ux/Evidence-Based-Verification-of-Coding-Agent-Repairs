#!/usr/bin/env python3
"""Deterministic ID-only selection. Never read problem text, gold patches, tests or outcomes."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

SALT = "EVCAR-FEASIBILITY-TEN-2026-11-17"
EXCLUDED_IDS = {"amoffat__sh-744"}
HEX40 = re.compile(r"^[0-9a-f]{40}$")

def select(rows: list[dict], dataset_sha: str, n: int = 10) -> dict:
    if not HEX40.fullmatch(dataset_sha):
        raise ValueError("Dataset source must be pinned by 40-character SHA")
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("Invalid sample size")
    seen = set()
    valid = []
    for row in rows:
        # Strict data minimisation: any hidden-oracle or unregistered field is rejected.
        if not isinstance(row, dict) or set(row) != {"instance_id", "repo"}:
            raise ValueError("Non-metadata field found: refuse to inspect future labels")
        iid, repo = row["instance_id"], row["repo"]
        if not isinstance(iid, str) or not iid or not isinstance(repo, str) or not repo:
            raise ValueError("Invalid instance metadata")
        if iid in seen:
            raise ValueError("Duplicate task ID")
        seen.add(iid)
        if iid in EXCLUDED_IDS:
            continue
        rank_key = hashlib.sha256((SALT + "|" + iid).encode("utf-8")).hexdigest()
        valid.append((rank_key, iid, repo))
    valid.sort()
    selected = []
    chosen_repos = set()
    for key, iid, repo in valid:
        if repo in chosen_repos:
            continue
        selected.append({"instance_id": iid, "repo": repo, "selection_sha256": key})
        chosen_repos.add(repo)
        if len(selected) == n:
            break
    if len(selected) != n:
        raise ValueError("Insufficient distinct repositories; do not replace or cherry-pick")
    return {
        "frame_type": "INFRASTRUCTURE_FEASIBILITY_ONLY_NOT_EFFICACY",
        "dataset_id": "SWE-bench-Live/SWE-bench-Live",
        "split": "lite",
        "dataset_revision_sha": dataset_sha,
        "selection_salt": SALT,
        "selection_rule": "sort SHA256(salt|instance_id), pick first 10 with distinct repo; exclude published calibration ID",
        "eligible_metadata_records": len(valid),
        "n_requested": n,
        "n_selected": len(selected),
        "future_oracle_seen_by_selector": False,
        "selected": selected,
        "claim_boundary": "Selection only; patch generation, predecision seal and hidden oracle still NOT EXECUTED",
    }

def run(metadata: Path, dataset_sha: str, out: Path, n: int = 10) -> dict:
    raw = metadata.read_text(encoding="utf-8")
    rows = [json.loads(line) for line in raw.splitlines() if line.strip()]
    if not rows:
        raise ValueError("Empty metadata file")
    result = select(rows, dataset_sha, n)
    result["source_metadata_sha256"] = hashlib.sha256(metadata.read_bytes()).hexdigest()
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        raise ValueError("Refuse to overwrite existing frame")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--metadata", type=Path, required=True)
    p.add_argument("--dataset-sha", required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--n", type=int, default=10)
    a = p.parse_args()
    print(json.dumps(run(a.metadata, a.dataset_sha, a.out, a.n), indent=2))
