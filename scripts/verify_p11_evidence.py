#!/usr/bin/env python3
"""P11 read-only audit of two DISJOINT previously executed evidence frames.

Recomputes archived source counts, exact event/actor chronology, and consistency
of historical *post-seal* official benchmark receipts. This DOES NOT execute
GitHub remote CI, independently rerun SWE-bench, or estimate policy efficacy.
"""
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/audits/P11_SOURCE_AND_ORACLE_BOUNDARIES_20261118.json"
FRAME = ROOT / "data/cohorts/copilot_2026_sep_oct_first10_frozen.json"
FREEZE = "0dfca364481605b12c2699296a9f948cb790b095"
POLICIES = ("self_report", "local_pass", "source_linked")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    assert parsed.tzinfo is not None
    return parsed.astimezone(timezone.utc)


def check_recorded_anchor(ledger: dict, source: dict) -> None:
    anchors = {a["name"]: a for a in ledger["prespecified_narrow_event_anchors"]}
    assert len(anchors) == 4
    by_source = {x["source"]: x for x in source["raw_documents"]}
    def comment(doc, url, author, at):
        matches = [x for x in doc["records"]["comments"]
                   if x["url"] == url and x["user"] == author
                   and x["created_at"] == at]
        assert len(matches) == 1, f"Missing exact archived event: {url}"
        return matches[0]
    def commit(doc, sha, author):
        matches = [x for x in doc["records"]["commits"]
                   if x["sha"] == sha and x.get("author") == author]
        assert len(matches) == 1, f"Missing exact archived commit: {sha}"
        return matches[0]

    # Positive chronology, not verified complete repair or prepatch failed CI.
    a = anchors["HUMAN_DIRECTIVE_COPILOT_UPDATE"]
    d = by_source[a["source"]]
    human = comment(d, a["human_comment_url"], a["human_comment_author"],
                    a["human_comment_at"])
    assert "@copilot" in human["body"].lower()
    assert "Do not make changes beyond" in human["body"]
    prior = commit(d, a["prior_copilot_commit"], "Copilot")
    follow = commit(d, a["subsequent_copilot_commit"], "Copilot")
    assert prior["at"] < a["human_comment_at"] < follow["at"]
    assert follow["at"] == a["subsequent_copilot_at"]
    assert a["same_name_failed_prepatch_check_recovered"] is False
    # Postpatch check receipt was checked against a separate GitHub endpoint.
    # It is documented by URL, not cryptographically reverified here.
    assert a["postpatch_verify_conclusion"] == "success"
    assert a["postpatch_verify_check_name"] == "verify"
    assert utc(a["postpatch_verify_completed_at"]) > utc(follow["at"])

    # Negative control: later success belongs to non-Copilot-labeled author.
    a = anchors["HUMAN_AUTHOR_NEGATIVE_CONTROL"]
    d = by_source[a["source"]]
    c = comment(d, a["human_review_url"], a["human_review_author"], a["human_review_at"])
    assert "NEEDS CHANGES" in c["body"]
    t = comment(d, a["subsequent_instruction_url"], a["human_review_author"],
                a["subsequent_instruction_at"])
    assert a["subsequent_instruction_target"].lower() in t["body"].lower()
    final = commit(d, a["final_commit"], a["final_commit_author"])
    assert final["at"] == a["final_commit_at"]
    assert utc(final["at"]) > utc(a["human_review_at"])
    assert not [x for x in d["records"]["commits"]
                if x.get("author") == "Copilot" and utc(x["at"]) > utc(a["human_review_at"])]
    assert len(a["final_sha_successful_check_names"]) == 9

    # Mixed ownership cannot be reduced to original PR authorship.
    a = anchors["MIXED_AUTHORSHIP_CONTROL"]
    d = by_source[a["source"]]
    commits = d["records"]["commits"]
    bot = [x for x in commits if x.get("author") == "Copilot"]
    later = [x for x in commits if x.get("author") == a["later_non_copilot_account"]]
    assert len(bot) == a["initial_copilot_labeled_commit_count"] == 2
    assert len(later) == a["later_non_copilot_labeled_commit_count"] == 8
    assert all(utc(x["at"]) > max(utc(b["at"]) for b in bot) for x in later)
    assert commits[-1]["sha"] == a["final_commit"]

    a = anchors["MERGE_WITHOUT_HEAD_CHECK_CONTROL"]
    d = by_source[a["source"]]
    assert d["records"]["pr"]["merged_at"] is not None
    assert d["records"]["commits"][-1]["sha"] == a["final_commit"]
    assert a["final_commit_checkrun_count_seen"] == 0


def audit(ledger_path: Path = LEDGER) -> dict:
    ledger = load(Path(ledger_path))
    frame = load(FRAME)
    src = ledger["source_frame"]
    rows = src["rows"]
    frozen = frame["cases"]
    assert ledger["schema"] == "EVCAR-99LLM-X1-P11-20261118-v1"
    assert ledger["frozen_frame_commit"] == FREEZE
    assert len(frozen) == len(rows) == 10
    assert [x["ordinal"] for x in rows] == list(range(1, 11))
    assert [x["ordinal"] for x in frozen] == list(range(1, 11))

    raw_documents = []
    state_counts = Counter()
    clusters = Counter()
    archived_commits = archived_discussion = 0
    all_utc = []
    for f, row in zip(frozen, rows):
        assert row["source"] == f'{f["repository"]}#{f["pr_number"]}'
        assert row["pr_url"] == f["pr_url"]
        assert row["opened_at"] == f["created_at"]
        assert row["source_archive_path"].startswith("data/source/p10/")
        assert Path(row["source_archive_path"]).name == row["source_archive_path"].split("/")[-1]
        document = load(ROOT / row["source_archive_path"])
        assert document["source"] == row["source"] and not document["errors"]
        assert document["freeze_commit"] == FREEZE
        pr = document["records"]["pr"]
        cs = document["records"]["commits"]
        ds = document["records"]["comments"]
        assert pr["author"] == f["actor"] == "Copilot"
        assert pr["created_at"] == f["created_at"]
        assert pr["commits"] == len(cs) == row["commit_count"]
        assert len(ds) == row["archived_discussion_events"]
        assert row["state"] == pr["state"]
        assert row["merged"] == (pr["merged_at"] is not None)
        assert sum(c.get("author") == "Copilot" for c in cs) == row["copilot_labeled_commits"]
        assert sum(c.get("author") not in (None, "Copilot") for c in cs) == row["other_named_commits"]
        assert sum(c.get("author") is None for c in cs) == row["unresolved_commit_authors"]
        assert len({c["sha"] for c in cs}) == len(cs)
        assert all(c.get("at") for c in cs) and all(d.get("created_at") and d.get("url") for d in ds)
        all_utc.append(utc(pr["created_at"]))
        state_counts["merged" if row["merged"] else
                     "closed_unmerged" if row["state"] == "closed" else "open"] += 1
        clusters[f["repository"]] += 1
        archived_commits += len(cs)
        archived_discussion += len(ds)
        raw_documents.append(document)

    assert all_utc == sorted(all_utc)
    assert len(clusters) == src["distinct_repositories"] == 5
    assert archived_commits == src["archived_pr_commits"] == 42
    assert archived_discussion == src["archived_comments_and_reviews"] == 129
    assert src["query_results"] == 60
    assert src["copilot_authored_query_results"] == 33
    assert src["uniform_independent_task_oracles"] == 0
    assert src["evaluated_repair_effectiveness"] == "NOT_ESTIMABLE"
    assert all(state_counts[k] == src[k] == 3 for k in ("merged", "closed_unmerged"))
    assert state_counts["open"] == src["open"] == 4
    check_recorded_anchor(ledger, {"raw_documents": raw_documents})

    bench = ledger["benchmark_initial_only"]
    assert bench["independent_source_frame"] and bench["not_copilot_2026_pr_frame"]
    assert bench["original_harness_commit"] == "ad79b850f15e33992e96f03f6e97f05ddf9aa0be"
    assert bench["dataset_revision"] == "babb27e45e072219195db7a744bbf0d3c1a36e56"
    assert len(bench["cases"]) == 3
    assert not (set(clusters) & {x["repo"] for x in bench["cases"]})
    result = {policy: dict(accept=0, hold=0, false_accept_count=0,
                           unnecessary_hold_count=0) for policy in POLICIES}
    total_tests = oracle_pass = oracle_fail = 0
    for case in bench["cases"]:
        seal_path = ROOT / "pilot" / case["short"] / "locked/P9_DECISIONS_SEALED.jsonl"
        seal = load(seal_path)
        prereg = load(ROOT / "pilot" / case["short"] / "oracle_evaluation_preregister.json")
        assert seal["episode_id"] == case["instance_id"] + "__INITIAL_ATTEMPT_ONLY"
        assert seal["head_sha"] == case["head_sha"]
        assert seal["repo"] == case["repo"]
        assert seal["decisions"] == case["preoracle_policy_decisions"]
        assert utc(seal["t_decision"]) < utc(case["oracle_started_at"])
        assert prereg["dataset_revision_sha"] == bench["dataset_revision"]
        assert prereg["harness_ref"] == bench["original_harness_commit"]
        assert case["f2p_total"] > 0 and 0 <= case["f2p_passed"] <= case["f2p_total"]
        assert case["p2p_failed"] >= 0 and case["executed_tests"] >= case["f2p_total"]
        resolved = case["f2p_passed"] == case["f2p_total"] and case["p2p_failed"] == 0
        assert resolved == case["official_resolved"]
        total_tests += case["executed_tests"]
        oracle_pass += int(resolved)
        oracle_fail += int(not resolved)
        for p in POLICIES:
            d = seal["decisions"][p]
            assert d in ("ACCEPT", "HOLD")
            result[p]["accept" if d == "ACCEPT" else "hold"] += 1
            result[p]["false_accept_count"] += int(d == "ACCEPT" and not resolved)
            result[p]["unnecessary_hold_count"] += int(d == "HOLD" and resolved)

    bsum = bench["observed_only_summary"]
    assert total_tests == bsum["executed_tests_total"] == 10915
    assert (oracle_pass, oracle_fail) == (bsum["oracle_true_pass"],
                                          bsum["oracle_true_fail"]) == (2, 1)
    assert bsum["admitted_oracles"] == len(bench["cases"])
    assert all(result[p][k] == bsum[p][k] for p in POLICIES for k in result[p])
    assert bsum["source_linked"]["accepted_denominator"] == 0
    assert bsum["source_linked"]["false_accept_rate_among_accepted"] is None
    return {
        "source_frame": {"n": len(rows), "repositories": len(clusters),
                         "commits": archived_commits, "discussion_events": archived_discussion,
                         "state": dict(state_counts),
                         "independent_uniform_oracles": 0},
        "benchmark_initial_only": {
            "n": len(bench["cases"]), "oracle_pass": oracle_pass,
            "oracle_fail": oracle_fail, "executed_tests": total_tests,
            "policies": result,
            "source_linked_accept_denominator": 0},
        "recomputation_status": "PASS_LOCAL_ARCHIVES_ONLY",
        "external_ci_observation_replayed": False,
        "benchmark_oracle_reexecuted": False,
        "causal_policy_efficacy_estimated": False,
    }


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2, sort_keys=True))
