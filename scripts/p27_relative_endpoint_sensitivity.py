#!/usr/bin/env python3
"""P27 post-reveal, explicitly ALTERNATIVE matched-baseline task test endpoint.

Uses P26 frozen source classification unchanged; adds recovered already-executed
Kedro original-source control and executed P25 cfn-lint null control to
illustrate sensitivity to using an incremental-P2P criterion.

Original SWE-bench-Live official task labels, MR30, original P9 policy
decisions, original P26 identified intervals remain UNCHANGED.
No new candidate or original task oracle is executed by this code.
"""
import argparse
from fractions import Fraction
import json
from pathlib import Path
import p26_identified_acceptance_bounds as parent

ROOT=Path(__file__).resolve().parents[1]
REG="protocol/P27_POSTREVEAL_BASELINE_RELATIVE_ENDPOINT_SENSITIVITY_20261120.json"
KEDRO="data/audits/P27_KEDRO_PREEXISTING_MATCHED_NULL_20261120.json"
CFN="data/audits/P25_CFN_LINT_MATCHED_ORIGINAL_NULL_CONTROL_EXECUTED_20261120.json"
CLASSES=("PASS_OFFICIAL","PASS_BASELINE_RELATIVE_ONLY","FAIL_F2P","UNKNOWN_IMPORT","NO_CANDIDATE")


def compute(root=ROOT):
    p=parent.compute(root)
    reg=parent.load(root,REG)
    kedro=parent.load(root,KEDRO)
    cfn=parent.load(root,CFN)
    assert reg["status"]=="POSTHOC_ALTERNATIVE_ENDPOINT_NOT_REPLACEMENT_FOR_ORIGINAL_BENCHMARK"
    assert reg["original_P9_decisions_unmodified"] is True
    assert reg["original_official_resolved_labels_unmodified"] is True
    assert reg["primary_P26_original_risk_bounds_unmodified"] is True
    assert p["selected_original_task_count"]==10
    assert p["attempted_original_task_candidate_count"]==9
    assert len(p["task_records"])==10
    assert kedro["status"]=="COMPLETE_SAME_FAILURE_SET"
    assert kedro["original_p9_candidate_run_id"]==44159300952
    assert kedro["prior_postreveal_null_run_id"]==44162955737
    assert kedro["original_candidate"]["f2p_passed"]==kedro["original_candidate"]["f2p_total"]==1
    assert kedro["original_source_comment_only_null"]["f2p_passed"]==0
    assert kedro["original_candidate"]["p2p_failed"]==kedro["original_source_comment_only_null"]["p2p_failed"]==25
    assert len(kedro["matched_p2p_failed_test_ids"])==25
    assert len(kedro["candidate_only_failed_p2p_test_ids"])==0
    assert len(kedro["control_only_failed_p2p_test_ids"])==0
    assert kedro["original_null_is_original_source_with_comment_only"] is True
    assert kedro["original_candidate"]["resolved"] is False
    assert cfn["source_base_sha"]=="de28d1e43777e3782a06b74d9091c3471636eb70"
    assert cfn["matched_reports"]==1
    assert cfn["f2p_passed"]==0 and cfn["f2p_total"]==1
    assert cfn["p2p_failed"]==4
    assert len(cfn["matched_failure_overlap_ids"])==4
    assert cfn["candidate_only_failure_ids"]==cfn["control_only_failure_ids"]==[]
    assert cfn["no_source_code_or_schema_change"] is True

    mapping={
        parent.PASS:"PASS_OFFICIAL",
        parent.FAIL:"FAIL_F2P",
        "UNKNOWN_UNATTRIBUTED_P2P":"PASS_BASELINE_RELATIVE_ONLY",
        "UNKNOWN_BASELINE_MATCHED_P2P":"PASS_BASELINE_RELATIVE_ONLY",
        "UNKNOWN_INVALID_IMPORT_ENDPOINT":"UNKNOWN_IMPORT",
        parent.NO_CANDIDATE:"NO_CANDIDATE"
    }
    results=[]
    for row in p["task_records"]:
        key=row["endpoint_class"]
        if key not in mapping:raise ValueError("Unexpected previous source class: "+key)
        new=mapping[key]
        if new=="PASS_BASELINE_RELATIVE_ONLY":
            if row["task"] not in ("kedro-org__kedro-4406","aws-cloudformation__cfn-lint-3779"):
                raise ValueError("No matched original-source P2P control for "+row["task"])
        results.append({
            "rank":row["rank"],
            "task":row["task"],
            "original_official_raw_resolved":row["raw_original_resolved"],
            "source_admitted_P26_endpoint":key,
            "postrevealed_relative_endpoint":new,
            "p9_original_decisions":row["p9_decisions"],
            "original_harness_run_id":row["original_oracle_run"],
            "original_policy_retrained":False
        })
    for cls,wanted in reg["expected_classes"].items():
        actual=[r["task"] for r in results if r["postrevealed_relative_endpoint"]==cls]
        if set(actual)!=set(wanted):
            raise ValueError("P27 alternative endpoint disagrees with source lock: "+cls)
    assert len(set(r["task"] for r in results))==10
    available=[r for r in results if r["postrevealed_relative_endpoint"]!="NO_CANDIDATE"]
    assert len(available)==9

    counts={}
    for policy in parent.POLICIES:
        accepted=[r for r in available if r["p9_original_decisions"][policy]=="ACCEPT"]
        held=[r for r in available if r["p9_original_decisions"][policy]=="HOLD"]
        assert len(accepted)+len(held)==len(available)
        f=sum(x["postrevealed_relative_endpoint"]=="FAIL_F2P" for x in accepted)
        u=sum(x["postrevealed_relative_endpoint"]=="UNKNOWN_IMPORT" for x in accepted)
        p_official=sum(x["postrevealed_relative_endpoint"]=="PASS_OFFICIAL" for x in accepted)
        p_relative=sum(x["postrevealed_relative_endpoint"]=="PASS_BASELINE_RELATIVE_ONLY" for x in accepted)
        assert f+u+p_official+p_relative==len(accepted)
        a=len(accepted)
        counts[policy]={
            "accepted":a,"held":len(held),"denominator":len(available),
            "direct_issue_F2P_fail_accepted":f,
            "original_official_pass_accepted":p_official,
            "matched_baseline_nonincremental_P2P_accepted":p_relative,
            "invalid_endpoint_unknown_accepted":u,
            "accepted_relative_failure_count_bounds":[f,f+u],
            "accepted_relative_failure_fraction_bounds":[str(Fraction(f,a)),str(Fraction(f+u,a))] if a else None,
            "accepted_relative_failure_decimal_bounds":[float(Fraction(f,a)),float(Fraction(f+u,a))] if a else None,
            "alternative_endpoint_not_original_official_verdict":True
        }
    assert counts["self_report"]["accepted"]==5
    assert counts["self_report"]["accepted_relative_failure_fraction_bounds"]==["2/5","2/5"]
    assert counts["local_pass"]["accepted"]==8
    assert counts["local_pass"]["accepted_relative_failure_fraction_bounds"]==["1/2","5/8"]
    assert counts["source_linked"]["accepted"]==0
    assert counts["source_linked"]["accepted_relative_failure_fraction_bounds"] is None

    return {
        "schema":"99llm_X1_P27_postreveal_alternative_matched_original_P2P_test_adequacy_v1",
        "study_status":"POSTREVEAL_SENSITIVITY_DIFFERENT_ESTIMAND_NOT_A_RECLASSIFICATION",
        "frozen_original_tasks":10,"candidates_with_original_p9_decisions":9,
        "original_reported_task_verdicts_unchanged":True,
        "P26_original_endpoint_risk_intervals_unchanged":True,
        "P27_existing_source_nulls":["kedro-org__kedro-4406","aws-cloudformation__cfn-lint-3779"],
        "source_task_rows":results,
        "policies":counts,
        "P26_original_endpoint_policy_bounds":{q:p["policies"][q]["false_accept_risk_sharp_exact_bounds"] for q in parent.POLICIES},
        "main_interpretive_boundary":"P27 tests an explicitly different posthoc F2P + no candidate-only P2P test-set definition. It does NOT infer official original benchmark RESOLVED, flawless code, human review or a new blinded evaluation.",
        "no_task_oracle_reexecution":True,
        "no_original_model_actor_attestation":True,
        "no_new_P9_decisions":True
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    output=compute()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(output,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("P27_BASELINE_RELATIVE_SENSITIVITY "+json.dumps(output["policies"],sort_keys=True))
    print("P27_NOT_ORIGINAL_BENCHMARK_RELABEL_OR_NEW_AGENT_TRIAL")


if __name__=="__main__":
    main()
