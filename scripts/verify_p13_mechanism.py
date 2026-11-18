#!/usr/bin/env python3
"""Verify P13 public/post-reveal ledger consistency against locked P12 records.

This is local archived-evidence consistency only, NOT an independent CI rerun,
not a fresh held-out experiment, and NOT source-linked policy acceptance.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P12 = ROOT / "data/audits/P12_PDM_INITIAL_ORACLE_20261118.json"
P13 = ROOT / "data/audits/P13_PDM_POSTREVEAL_RETEST_20261118.json"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def audit(p13_path=P13):
    p12 = read(P12)
    p13 = read(p13_path)
    assert p13["schema"] == "99llm_X1_P13_PDM_PostRevealMechanisticRecheck_20261118_v1"
    assert p13["status"] == "EXECUTED_POSTREVEAL_DIAGNOSTIC_NOT_BLIND"
    assert p13["task"]["instance_id"] == p12["task"]["instance_id"]
    assert p13["task"]["upstream_base_sha"] == p12["task"]["source_base_sha"]
    assert p13["task"]["dataset_revision"] == p12["task"]["revision"]
    assert p13["task"]["harness_sha"] == p12["evidence"][-1]["original_harness_commit"]
    variants = p13["variants"]
    assert [x["name"] for x in variants] == [
        "original_upstream_base",
        "P12_initial_preoracle_sealed",
        "P13_postreveal_mechanistic_revision",
    ]
    base, initial, retest = variants
    assert base["visible_pass"] == 0 and base["visible_total"] == 3
    assert base["public_pass"] == 22 and base["public_total"] == 22
    assert base["f2p_passed"] is None and base["p2p_failed"] is None
    assert initial["candidate_sha"] == p12["task"]["first_candidate_sha"]
    assert initial["patch_sha256"] == p12["task"]["first_patch_sha256"]
    assert initial["not_blinded_by_this_test"] is False
    assert initial["official_run_id"] == 44237374542
    assert initial["f2p_total"] == p12["evidence"][-1]["f2p_total"] == 3
    assert initial["f2p_passed"] == p12["evidence"][-1]["f2p_passed"] == 0
    assert initial["p2p_failed"] == p12["evidence"][-1]["p2p_failed"] == 2
    assert initial["original_tests_executed"] == 939
    assert retest["candidate_sha"] == "75473b04603db84fa67dc814f4d67e459a183bb0"
    assert retest["visible_pass"] == 3 and retest["visible_total"] == 3
    assert retest["public_pass"] == 22 and retest["public_total"] == 22
    assert retest["f2p_total"] == 3 and retest["f2p_passed"] == 0
    assert retest["p2p_failed"] == 0 and retest["original_tests_executed"] == 939
    assert retest["official_run_id"] == 44238901257
    assert retest["not_blinded_by_this_test"] is True
    assert retest["official_hidden_status"] == "COMPLETE_UNRESOLVED_POSTREVEAL"
    assert retest["original_test_output_sha256"] == "a4a7d78aba6777d65aebcf9f691db1b1bbdf33e09e69839b7432d2305d72dad9"
    assert p13["frozen_policy_unchanged"]["P13_has_new_preoracle_decision"] is False
    assert p13["frozen_policy_unchanged"]["P13_is_new_policy_evaluation"] is False
    assert p13["frozen_policy_unchanged"]["original_P12_decisions_sha256"] == (
        hashlib.sha256((ROOT/"pilot/pdm/locked/P9_DECISIONS_SEALED.jsonl").read_bytes()).hexdigest()
    )
    assert p13["three_axes"]["group_provenance_narrow"].startswith("P12 and P13 visible 3/3")
    assert len({x["candidate_sha"] for x in variants}) == 3
    return {
        "archive_consistency":"PASS",
        "exposed_task_count":1,
        "prospective_policy_trial_count_added_by_P13":0,
        "P12_visible_pass":3,
        "P13_visible_pass":3,
        "P12_original_update_public_regressions":2,
        "P13_original_update_public_regressions":0,
        "P12_F2P_passed":0,
        "P13_F2P_passed":0,
        "P12_P2P_failed":2,
        "P13_P2P_failed":0,
        "P13_hidden_retest_blinded":False,
        "P13_original_task_resolved":False
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
