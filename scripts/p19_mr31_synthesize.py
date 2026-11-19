#!/usr/bin/env python3
"""P19 reproducible MR31 editorial evidence matrix from immutable X1 records.

Reads previously published original six-task mixed-stage task truth and one
POST-REVEAL literal-only ablation. This is a publication-facing DESCRIPTIVE
SYNTHESIS, not a fresh benchmark run, independent model experiment, causal
policy evaluation, or admission of an exposed task as an additional success.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/audits/P17_SIX_TASK_MIXED_STAGE_NONVACUITY_20261120.json"
ABLATED=ROOT/"data/audits/P18_TORCHTUNE_POSTREVEAL_ORACLE_LITERAL_RETEST_20261120.json"
FRAME=ROOT/"pilot/frozen_task_frame_20261117.json"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def classify(row):
    """Two orthogonal original benchmark dimensions, not an inferred cause."""
    f2p=row["f2p_passed"]
    total=row["f2p_total"]
    p2p=row["p2p_failed"]
    if any(type(x) is not int for x in (f2p,total,p2p)) or total<=0 or not (0<=f2p<=total) or p2p<0:
        raise ValueError("Invalid original F2P/P2P count")
    expected=f2p==total and p2p==0
    if type(row["truth"]) is not bool or row["truth"]!=expected:
        raise ValueError("Unexpected original task outcome")
    if expected:return "ORIGINAL_HARNESS_RESOLVED"
    if f2p==total and p2p>0:return "F2P_PASSED_P2P_REGRESSION"
    if f2p<total and p2p>0:return "F2P_FAILED_P2P_REGRESSION"
    return "F2P_FAILED_NO_RECORDED_P2P_REGRESSION"


def synthesize():
    data=read(SOURCE)
    post=read(ABLATED)
    original=read(FRAME)
    assert len(original["selected"])==original["n_selected"]==10
    rows=data["rows"]
    if len(rows)!=6 or len({r["task"] for r in rows})!=6:
        raise ValueError("Must use exactly six original distinct evaluated task IDs")
    if data["independently_scored_distinct_tasks"]!=6 or data["passed_tasks"]!=2 or data["failed_tasks"]!=4:
        raise ValueError("Six-task original result changed")
    selected={r["instance_id"]:i+1 for i,r in enumerate(original["selected"])}
    output_rows=[]
    counts={}
    for r in rows:
        task=r["task"]
        if task not in selected:raise ValueError("Original task selection changed: "+task)
        cls=classify(r)
        counts[cls]=counts.get(cls,0)+1
        record={
            "task_index_in_original_frame_one_based":selected[task],
            "task_id":task,
            "stage_kind":r["stage"],
            "original_harness_task_resolved":r["truth"],
            "original_f2p_passed":r["f2p_passed"],
            "original_f2p_total":r["f2p_total"],
            "original_p2p_failed":r["p2p_failed"],
            "original_tests_executed":r["tests"],
            "original_oracle_run_id":r["run_id"],
            "original_oracle_url":r["original_harness_source_url"],
            "original_patch_sha":r["head"],
            "independent_task_level_unit_count":1,
            "original_outcome_class":cls,
            "frozen_policy_decisions":r["policy"],
        }
        if task=="pytorch__torchtune-2139":
            variant=post["exposed_single_literal_variant"]
            if r["head"]!=post["first_initial_candidate"]["candidate_sha"] or r["truth"] is not False:
                raise ValueError("Torchtune original result was incorrectly replaced")
            if variant["f2p_passed"]!=1 or variant["f2p_total"]!=1 or variant["p2p_failed"]!=0:
                raise ValueError("Unexpected postreveal literal test outcome")
            if variant["stage"]!="POSTREVEAL_NOT_BLIND" or variant["original_task_population_increased"] is not False:
                raise ValueError("P18 cannot be admitted as original blind task")
            record["postreveal_sensitivity_overlay"]={
                "excluded_from_original_task_result":True,
                "new_original_task_count":0,
                "original_f2p":"0/1",
                "postreveal_f2p":"1/1",
                "modified_source_component":"RuntimeError message literal only",
                "same_original_harness_tests_executed":r["tests"]==variant["tests_executed"]==651,
                "postreveal_original_oracle_url":variant["source_url"],
                "hidden_assertion_was_known_before_variant":True,
                "does_not_certify_two_gpu_training":True,
            }
        output_rows.append(record)
    output_rows.sort(key=lambda x:x["task_index_in_original_frame_one_based"])
    if sorted(x["task_index_in_original_frame_one_based"] for x in output_rows)!=[1,2,3,4,5,8]:
        raise ValueError("Original six task identities or frozen index altered")

    expected_counts={
        "ORIGINAL_HARNESS_RESOLVED":2,
        "F2P_PASSED_P2P_REGRESSION":1,
        "F2P_FAILED_P2P_REGRESSION":1,
        "F2P_FAILED_NO_RECORDED_P2P_REGRESSION":2,
    }
    if counts!=expected_counts:raise ValueError("Original task failure-mode decomposition changed")
    policy={}
    for name in ("self_report","local_pass","source_linked"):
        accepted=[x for x in output_rows if x["frozen_policy_decisions"][name]=="ACCEPT"]
        held=[x for x in output_rows if x["frozen_policy_decisions"][name]=="HOLD"]
        if len(accepted)+len(held)!=6:raise ValueError("Nonbinary policy label")
        policy[name]={
            "accepted_task_count":len(accepted),
            "held_task_count":len(held),
            "false_accept_count":sum(not x["original_harness_task_resolved"] for x in accepted),
            "correct_accept_count":sum(x["original_harness_task_resolved"] for x in accepted),
            "unnecessary_hold_count":sum(x["original_harness_task_resolved"] for x in held),
            "risk_among_accepted_defined":bool(accepted),
            "false_accept_risk_among_accepted":(
                sum(not x["original_harness_task_resolved"] for x in accepted)/len(accepted)
                if accepted else None),
        }
        published=data["policies"][name]
        if any([
            policy[name]["accepted_task_count"]!=published["n_accepted"],
            policy[name]["false_accept_count"]!=published["n_false_accepted"],
            policy[name]["correct_accept_count"]!=published["n_correct_accepted"],
            policy[name]["unnecessary_hold_count"]!=published["n_unnecessary_hold"],
            policy[name]["risk_among_accepted_defined"]!=published["false_accept_rate_defined"]
        ]):raise ValueError("Policy regression or denominator rewrite")
    if policy["source_linked"]["false_accept_risk_among_accepted"] is not None:
        raise ValueError("Never impute a zero-accept rate as zero")
    return {
        "schema":"99llm_X1_P19_MR31_provisional_evidence_matrix_v1",
        "status":"EDITORIAL_SYNTHESIS_ONLY_NO_NEW_ORIGINAL_TASK_RESULTS",
        "scientific_unit":"distinct fixed original SWE-bench-Live task; Matplotlib synthetic feedback stage counted once",
        "original_fixed_task_frame":10,
        "original_distinct_tasks_with_valid_independent_oracle":6,
        "original_distinct_tasks_not_yet_evaluated":4,
        "original_resolved_task_count":2,
        "original_unresolved_task_count":4,
        "original_task_evidence_sources":{
            "six_task_source":str(SOURCE.relative_to(ROOT)),
            "six_task_SHA256":hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            "p18_postreveal_source":str(ABLATED.relative_to(ROOT)),
            "p18_postreveal_SHA256":hashlib.sha256(ABLATED.read_bytes()).hexdigest(),
            "frozen_frame":str(FRAME.relative_to(ROOT)),
            "frozen_frame_SHA256":hashlib.sha256(FRAME.read_bytes()).hexdigest(),
        },
        "failure_mode_count_table":expected_counts,
        "original_task_rows":output_rows,
        "frozen_decision_risk_coverage_descriptive":policy,
        "p18_postreveal_literal_flip_present_as_overlay_not_extra_task":True,
        "P18_new_original_blinded_task_count":0,
        "human_second_coder_present":False,
        "actor_authentication_verified_for_benchmark_rows":False,
        "vacuous_zero_accept_policy_risk":None,
        "comparability_limit":"Mixed-stage feasibility panel: four prior initial tasks plus P17 DoRA initial and final post-synthetic-feedback Matplotlib. No causal effect, no homogeneous prospective efficacy estimate.",
        "paper_status":"Proposed MR31 addendum; MR30 and frozen P9/P10-P18 scientific results unchanged",
        "claim_boundary":"Do not claim benchmark defect prevalence, model-wide bug fixing ability, real human developer feedback, operational GPU DoRA training correctness, or superiority of source-linked policy from this small data."
    }


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",required=True,type=Path)
    args=ap.parse_args()
    result=synthesize()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("P19_EVIDENCE_MATRIX "+json.dumps({
      "n_task":result["original_distinct_tasks_with_valid_independent_oracle"],
      "original_success":result["original_resolved_task_count"],
      "failure_modes":result["failure_mode_count_table"],
      "policy":result["frozen_decision_risk_coverage_descriptive"],
      "P18_new_task_count":result["P18_new_original_blinded_task_count"]},sort_keys=True))
