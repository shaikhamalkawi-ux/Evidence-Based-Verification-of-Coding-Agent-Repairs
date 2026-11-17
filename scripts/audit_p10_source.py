#!/usr/bin/env python3
"""Recompute a conservative source-coverage audit of the PRE-FROZEN P10 PR frame.

This does NOT identify actual agent-repair success. It deliberately does not
query GitHub, execute agent patches, access future hidden tests, or impute
missing verification. Source snapshots were acquired after cohort freeze.
"""
from __future__ import annotations
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
FRAME = ROOT / "data/cohorts/copilot_2026_sep_oct_first10_frozen.json"
SOURCE = ROOT / "data/source/p10"

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def classify_name(login):
    """A literal account-name heuristic, NOT identity verification."""
    s = str(login or "").lower()
    known_automation = {
        "copilot", "maslowbot", "elasticsearchmachine", "github-actions",
        "cloudflare-workers-and-pages", "coderabbitai",
    }
    if s in known_automation or s.endswith("[bot]") or s.endswith("-bot"):
        return "automation_label"
    return "unverified_nonbot_label" if s else "unknown"

def source_path(case):
    return SOURCE / (''.join(c if c.isalnum() else '_' for c in case["repository"]) +
                     f'_{case["pr_number"]}.json')

def audit():
    frame = load(FRAME)
    rows = frame["cases"]
    assert len(rows) == 10, "Preserve all ten frozen records"
    ids = [(x["repository"], x["pr_number"]) for x in rows]
    assert len(ids) == len(set(ids)), "Duplicate PR in frozen frame"
    assert [x["ordinal"] for x in rows] == list(range(1, 11))
    n_repos = len({x["repository"] for x in rows})
    assert n_repos == 5, "The erratum documents five distinct repositories"
    t = [datetime.fromisoformat(x["created_at"].replace("Z","+00:00")) for x in rows]
    assert t == sorted(t), "Frozen creation-order violation"

    items = []
    n_commits = 0
    n_comments = 0
    count_by_repo = Counter()
    for x in rows:
        path = source_path(x)
        assert path.is_file(), f"Missing source: {path}"
        raw = path.read_bytes()
        doc = json.loads(raw)
        assert doc["source"] == f'{x["repository"]}#{x["pr_number"]}'
        assert doc["freeze_commit"] == "0dfca364481605b12c2699296a9f948cb790b095"
        assert not doc.get("errors"), f"Source retrieval errors for {doc['source']}"
        p = doc["records"]["pr"]
        assert p["author"] == "Copilot", f"Author mismatch for {doc['source']}"
        assert p["created_at"] == x["created_at"]
        commits = doc["records"]["commits"]
        comments = doc["records"]["comments"]
        assert len(commits) == p["commits"], f"Partial PR commit list for {doc['source']}"
        assert len(commits) < 100, f"Pagination audit needed for {doc['source']}"
        assert len(comments) < 100, f"Pagination audit needed for {doc['source']}"
        assert len(set(c["sha"] for c in commits)) == len(commits)
        assert all(c.get("at") for c in commits)
        assert all(c.get("url") and c.get("created_at") for c in comments)
        n_commits += len(commits)
        n_comments += len(comments)
        count_by_repo[x["repository"]] += 1
        nonbot = [c for c in comments if classify_name(c.get("user")) == "unverified_nonbot_label"]
        items.append({
            "ordinal": x["ordinal"], "source":doc["source"], "source_url":x["pr_url"],
            "state": p["state"], "merged": p["merged_at"] is not None,
            "pr_commits": len(commits), "archived_discussion_events":len(comments),
            "nonbot_label_events_not_human_certified":len(nonbot),
            "nonbot_label_accounts": sorted({c["user"] for c in nonbot}),
            "commits_attributed_to_other_named_accounts": sum(c.get("author") not in (None,"Copilot") for c in commits),
            "commits_with_unresolved_actor": sum(c.get("author") is None for c in commits),
            "snapshot_sha256": hashlib.sha256(raw).hexdigest(),
            "oracle_status": "NOT_ADMITTED_HOMOGENEOUS_TASK_ORACLE",
            "scientific_status": "DIAGNOSTIC_SOURCE_ONLY",
        })
    return {
      "scope": "frozen 10-PR observational source-coverage pilot, not a causal trial",
      "cohort_freeze_commit":"0dfca364481605b12c2699296a9f948cb790b095",
      "rows_in_frozen_frame":len(rows),
      "distinct_repositories":n_repos,
      "repository_cluster_sizes":dict(sorted(count_by_repo.items())),
      "archive_complete":True,
      "commit_records_read":n_commits,
      "comment_or_review_events_read":n_comments,
      "no_independent_task_oracle":True,
      "independently_admitted_task_oracles":0,
      "repair_effectiveness_estimable":False,
      "admonition":"Zero admitted task oracles is NOT zero successful repairs. P10 public CI may serve only context-specific diagnostics.",
      "units":items
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output")
    args=p.parse_args()
    result=audit()
    payload=json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+"\n"
    if args.output:
        out=Path(args.output)
        out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(payload,encoding="utf-8")
    print(payload)

if __name__ == "__main__":
    main()
