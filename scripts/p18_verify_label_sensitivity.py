#!/usr/bin/env python3
"""P18 post-reveal result/claim-boundary consistency checks over archived data.

No original test source is imported. This verifies saved, source-linked task
receipts and exact P17 P9 seal; it does NOT execute Docker or independently
validate a coding agent's model identity.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ORIGINAL=ROOT/"data/audits/P17_TORCHTUNE_ORIGINAL_ORACLE_20261120.json"
P18=ROOT/"data/audits/P18_TORCHTUNE_POSTREVEAL_ORACLE_LITERAL_RETEST_20261120.json"
SEAL=ROOT/"pilot/torchtune/sealed/P9_DECISIONS_SEALED.jsonl"
DIAGNOSTIC=ROOT/"data/audits/P18_TORCHTUNE_POSTREVEAL_ERROR_TAXONOMY_20261120.json"
PROTO=ROOT/"protocol/P18_POSTREVEAL_LITERAL_SENSITIVITY_REGISTER_20261120.json"
FROZEN=ROOT/"pilot/frozen_task_frame_20261117.json"

def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def validate(ledger=None):
    d=read(P18) if ledger is None else ledger
    old=read(ORIGINAL)
    p=read(PROTO)
    diag=read(DIAGNOSTIC)
    frame=read(FROZEN)
    assert len(frame["selected"])==10
    assert frame["selected"][4]["instance_id"]=="pytorch__torchtune-2139"
    assert d["task_id"]=="pytorch__torchtune-2139"
    assert d["original_cohort_task_index_one_based"]==5
    assert d["scientific_status"]=="EXECUTED_ORIGINAL_TASK_ORACLE_BUT_POSTREVEAL_ONLY_NOT_BLINDED_AGENT_OR_POLICY_TRIAL"
    assert p["status"]=="PREREGISTERED_POSTREVEAL_NOT_BLINDED"
    assert d["first_initial_candidate"]["candidate_sha"]==old["original_harness_task_result"]["head_sha"]=="57f45fdd5552908d4b5d42cccd7359ccb4de2560"
    assert d["first_initial_candidate"]["original_blinded_oracle_run_id"]==44613016409
    assert d["first_initial_candidate"]["f2p_passed"]==old["original_harness_task_result"]["f2p_passed"]==0
    assert d["first_initial_candidate"]["f2p_total"]==old["original_harness_task_result"]["f2p_total"]==1
    assert d["first_initial_candidate"]["p2p_failed"]==old["original_harness_task_result"]["p2p_failed"]==0
    assert d["first_initial_candidate"]["tests_executed"]==old["original_harness_task_result"]["tests_executed"]==651
    assert d["first_initial_candidate"]["original_resolved"] is False
    assert d["first_initial_candidate"]["original_test_output_sha256"]==old["original_harness_task_result"]["original_test_output_sha256"]
    assert d["first_initial_candidate"]["preoracle_decisions_sha256"]==hashlib.sha256(SEAL.read_bytes()).hexdigest()
    result=d["exposed_single_literal_variant"]
    assert result["stage"]=="POSTREVEAL_NOT_BLIND"
    assert result["status"]=="COMPLETE_POSTREVEAL"
    assert result["candidate_sha"]=="6c029466df2fdca0b28273b58eaab46ef6460075"
    assert result["candidate_sha"]==p["new_P18_postreveal_candidate_sha"]
    assert result["original_p17_heldout_task_run"]==44613016409
    assert result["f2p_passed"]==result["f2p_total"]==1
    assert result["p2p_failed"]==0
    assert result["tests_executed"]==651
    assert result["original_resolved"] is True
    assert result["matched_reports"]==1
    assert result["original_harness_sha"]==d["original_harness_sha"]==p["original_harness_sha"]
    assert result["dataset_rev"]==d["original_dataset_sha"]==p["original_dataset_revision"]
    assert result["original_test_output_sha256"]=="3d0c13446d3e5548c8dd718a3c0c3a722b6b803a974f13401deee0f24b25044e"
    assert result["source_git_blob_sha"]=="0c0aeef1bb24336dff8904dd61d6ad33d4233dee"
    assert result["agent_policy_decision_rescored"] is False
    assert result["original_task_population_increased"] is False
    assert result["human_feedback_or_authentic_agent_attestation"] is False
    assert result["full_two_GPU_DORA_training_reproduced"] is False
    assert result["incremental_scope_confirmed_by_execution"] is True
    assert d["score_label_interpretation"]["change_in_task_count_for_original_frozen_cohort"]==0
    assert d["score_label_interpretation"]["original_SWEbench_blinded_case_count_still"]==6
    assert d["score_label_interpretation"]["original_blinded_successful_tasks_still"]==2
    assert d["score_label_interpretation"]["original_blinded_failed_tasks_still"]==4
    assert d["institutional_boundaries"]["original_P9_frozen"] is True
    assert d["institutional_boundaries"]["original_two_gpu_training_executed"] is False
    assert diag["original_test_output_sha256"]==d["first_initial_candidate"]["original_test_output_sha256"]
    assert diag["failed_f2p_test_ids"]==[
        "tests/torchtune/modules/peft/test_dora.py::TestDoRALinear::test_dora_meta_device_init_error"]
    assert d["failure_provenance"]["original_expected_regex"]==p["observed_expected_regex"]
    assert d["failure_provenance"]["p17_observed_exception_text"]==p["observed_P17_runtime_error"]
    return {
      "status":"PASS_ARCHIVED_EXECUTION_CONSISTENCY_ONLY",
      "task":"pytorch__torchtune-2139",
      "original_task_count_added_by_P18":0,
      "original_P17_F2P":"0/1",
      "exposed_P18_F2P":"1/1",
      "original_evaluator_tests_executed_each":651,
      "P2P_failures_both":0,
      "source_changed_only_error_literal":True,
      "full_two_GPU_DoRA_training_verified":False,
      "original_P17_P9_decisions_changed":False,
      "original_blinded_six_task_panel_changed":False,
      "new_blinded_coding_agent_efficacy_estimate":False
    }


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    result=validate()
    print(json.dumps(result,sort_keys=True))
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
