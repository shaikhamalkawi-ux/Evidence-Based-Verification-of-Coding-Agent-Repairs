#!/usr/bin/env python3
"""P26: retrospective sharp descriptive bounds on ORIGINAL task-acceptance risk.

Do not change original P9 decisions, historical SWE-bench-Live task reports,
original sample, or substantive claims. No hidden test access; local JSON
sources are verified below. Mixed candidate stages, 9 evaluated candidates
of 10 originally frozen tasks. No independent actor attestation.

This finite-frame calculation is an application of elementary partial
identification; it is not a new theorem, benchmark metric, population-risk
estimate, or demonstration of source-linked superiority.
"""
import argparse
from fractions import Fraction
import json
from pathlib import Path

REL = Path(__file__).resolve().parents[1]
FRAME = "pilot/frozen_task_frame_20261117.json"
P19 = "data/audits/P19_SEVEN_TASK_MIXED_STAGE_NONVACUITY_20261120.json"
P25 = "data/audits/P25_TEN_FROZEN_TASKS_ENDPOINT_ADMISSION_RECONCILIATION_20261120.json"
P20 = "data/audits/P20_PRIVACYIDEA_ORIGINAL_HARNESS_RAW_WITH_QC_HOLD_20261120.json"
P21 = "data/audits/P21_PRIVACYIDEA_ENDPOINT_ADMISSION_REPRODUCED_20261120.json"
P23 = "data/audits/P23_CFN_LINT_ORIGINAL_TASK_ORACLE_20261120.json"
P25NULL = "data/audits/P25_CFN_LINT_MATCHED_ORIGINAL_NULL_CONTROL_EXECUTED_20261120.json"
PROTOCOL = "protocol/P26_ENDPOINT_PARTIAL_IDENTIFICATION_PRECOMPUTATION_20261120.json"
POLICIES = ("self_report", "local_pass", "source_linked")
PASS = "PASS_ORIGINAL_TASK_ORACLE"
FAIL = "FAIL_DIRECT_F2P"
UNKNOWN = ("UNKNOWN_UNATTRIBUTED_P2P", "UNKNOWN_INVALID_IMPORT_ENDPOINT", "UNKNOWN_BASELINE_MATCHED_P2P")
NO_CANDIDATE = "NO_CANDIDATE_NO_ORIGINAL_ORACLE"


def load(root, relative):
    return json.loads((root / relative).read_text(encoding="utf8"))


def endpoint(row, raw7, p20, p21, p23, null):
    task = row["task"]
    if task == "reflex-dev__reflex-4510":
        assert row["raw_original_harness_run_id"] is None
        assert all(row["p9_original_preoracle"][p] is None for p in POLICIES)
        return NO_CANDIDATE, "No source candidate, no P9 decisions, and no original task oracle"
    if task == "privacyidea__privacyidea-4251":
        raw = p20["received_original_report"]
        assert p21["endpoint_admission_for_code_correctness"] == "HOLD_SYSTEMIC_TEST_IMPORT_FAILURE"
        assert p21["code_correctness_verified"] is None
        assert p21["original_task_report_p2p_failed"] == raw["p2p_failed"] == 2022
        assert p21["original_task_report_tests_classified"] == raw["tests_executed"] == 2023
        assert raw["f2p_passed"] == 0 and raw["f2p_total"] == 1
        assert p21["postreveal_observed_error"] == "ModuleNotFoundError: No module named 'swe100_fixture_clock'"
        return UNKNOWN[1], "Original task test import failure; source correctness is unadmitted"
    if task == "aws-cloudformation__cfn-lint-3779":
        original = p23["original_harness_task_observation"]
        assert original["f2p_passed"] == original["f2p_total"] == 1
        assert original["p2p_failed"] == 4
        assert original["official_resolved"] is False
        assert null["matched_reports"] == 1
        assert null["f2p_passed"] == 0 and null["f2p_total"] == 1
        assert null["p2p_failed"] == 4
        assert null["control_only_failure_ids"] == []
        assert null["original_only_failure_ids"] == []
        assert len(null["matched_failure_overlap_ids"]) == 4
        assert null["no_source_code_or_schema_change"] is True
        return UNKNOWN[2], "F2P passed but 4 failed P2P also occur with original source and README-only control"
    r = raw7[task]
    assert row["raw_original_harness_run_id"] == r["run_id"]
    assert row["raw_original_resolved"] is r["truth"]
    assert row["p9_original_preoracle"] == r["policy"]
    assert r["f2p_total"] > 0 and r["tests"] > 0
    if r["f2p_passed"] < r["f2p_total"]:
        assert r["truth"] is False
        return FAIL, "At least one original issue-specific F2P test actually failed"
    if r["p2p_failed"] == 0:
        assert r["truth"] is True
        return PASS, "All issue-specific F2P tests passed and no P2P failures"
    assert r["truth"] is False and task == "kedro-org__kedro-4406"
    assert r["f2p_passed"] == r["f2p_total"] == 1
    assert r["p2p_failed"] == 25
    return UNKNOWN[0], "F2P passed but 25 P2P failures lack an admissible original-source matched control"


def count_policy(rows, policy):
    attempted = [r for r in rows if r["endpoint_class"] != NO_CANDIDATE]
    assert len(attempted) == 9
    accepted = [r for r in attempted if r["p9_decisions"][policy] == "ACCEPT"]
    held = [r for r in attempted if r["p9_decisions"][policy] == "HOLD"]
    assert len(accepted) + len(held) == len(attempted)
    pos = sum(r["endpoint_class"] == PASS for r in accepted)
    neg = sum(r["endpoint_class"] == FAIL for r in accepted)
    unknown = sum(r["endpoint_class"] in UNKNOWN for r in accepted)
    assert len(accepted) == pos + neg + unknown
    confirmed_pos = [r for r in attempted if r["endpoint_class"] == PASS]
    held_pos = sum(r["p9_decisions"][policy] == "HOLD" for r in confirmed_pos)
    n = len(accepted)
    return {
        "policy":policy,
        "attempted_decision_denominator":len(attempted),
        "accept_count":n,
        "hold_count":len(held),
        "acceptance_coverage_exact":f"{n}/{len(attempted)}",
        "accepted_direct_F2P_fail":neg,
        "accepted_original_task_pass":pos,
        "accepted_endpoint_or_attribution_unknown":unknown,
        "false_accept_count_identified_interval":[neg,neg+unknown],
        "false_accept_risk_sharp_exact_bounds":[str(Fraction(neg,n)),str(Fraction(neg+unknown,n))] if n else None,
        "false_accept_risk_sharp_decimal_bounds":[float(Fraction(neg,n)),float(Fraction(neg+unknown,n))] if n else None,
        "risk_defined":n>0,
        "guaranteed_passing_task_count":len(confirmed_pos),
        "guaranteed_passing_tasks_held":held_pos,
        "confidence_interval_applicable":False,
        "coverage_population_inference_admitted":False
    }


def compute(root=REL):
    protocol = load(root,PROTOCOL)
    frame = load(root,FRAME)
    panel = load(root,P25)
    baseline7 = load(root,P19)
    p20,p21,p23,null = (load(root,p) for p in (P20,P21,P23,P25NULL))
    assert protocol["study_status"] == "POSTHOC_DETERMINISTIC_ID_SET_NOT_NEW_BLINDED_POLICY"
    assert protocol["original_population_size"] == frame["n_selected"] == len(frame["selected"]) == 10
    assert frame["dataset_revision_sha"] == panel["source_dataset_revision"] == "babb27e45e072219195db7a744bbf0d3c1a36e56"
    assert panel["raw_original_harness_executed_count"] == 9
    assert panel["raw_original_harness_resolved_count"] == 2
    assert panel["raw_original_harness_unresolved_count"] == 7
    assert len(panel["rows"]) == 10
    assert baseline7["now_evaluated_distinct_task_count"] == len(baseline7["unique_task_rows"]) == 7
    raw7 = {r["task"]:r for r in baseline7["unique_task_rows"]}
    assert len(raw7) == 7

    results = []
    for idx,(r,entry) in enumerate(zip(panel["rows"],frame["selected"])):
        assert r["task"] == entry["instance_id"]
        assert r["original_repo"] == entry["repo"]
        assert r["original_selection_sha256"] == entry["selection_sha256"]
        assert r["original_frozen_rank"] == idx+1
        status,reason = endpoint(r,raw7,p20,p21,p23,null)
        results.append({
            "rank":idx+1,
            "task":r["task"],
            "stage":r["record_stage"],
            "raw_original_resolved":r["raw_original_resolved"],
            "original_oracle_run":r["raw_original_harness_run_id"],
            "endpoint_class":status,
            "admission_reason":reason,
            "p9_decisions":r["p9_original_preoracle"]
        })
    expected = protocol["expected_verified_cross_check"]
    for key,cls in (
        ("direct_F2P_failed_task_ids",FAIL),
        ("direct_original_task_pass_ids",PASS),
        ("endpoint_or_attribution_underdetermined_task_ids",UNKNOWN),
        ("no_coded_attempt",NO_CANDIDATE),
    ):
        observed = [r["task"] for r in results
                    if (r["endpoint_class"] in cls if isinstance(cls,tuple)
                        else r["endpoint_class"] == cls)]
        if set(observed) != set(expected[key]):
            raise ValueError("Original evidence source changed: "+key+" expected "+str(expected[key])+" observed "+str(observed))

    policies = {p:count_policy(results,p) for p in POLICIES}
    assert policies["self_report"]["accept_count"] == 5
    assert policies["local_pass"]["accept_count"] == 8
    assert policies["source_linked"]["accept_count"] == 0
    assert policies["local_pass"]["false_accept_count_identified_interval"] == [4,7]
    assert policies["self_report"]["false_accept_count_identified_interval"] == [2,4]
    assert policies["source_linked"]["false_accept_risk_sharp_exact_bounds"] is None

    return {
        "schema":"99llm_X1_P26_original_frozen_partial_identification_v1",
        "scientific_status":"DESCRIPTIVE_FINITE_FRAME_POSTHOC_MIXED_STAGE",
        "selected_original_task_count":10,
        "attempted_original_task_candidate_count":9,
        "no_candidate_original_task_count":1,
        "original_raw_harness_executed_count":9,
        "raw_original_resolved_count":2,
        "raw_original_unresolved_count":7,
        "endpoint_admitted_issue_specific_F2P_fail_count":sum(r["endpoint_class"]==FAIL for r in results),
        "endpoint_admitted_original_task_pass_count":sum(r["endpoint_class"]==PASS for r in results),
        "endpoint_unknown_with_candidate_count":sum(r["endpoint_class"] in UNKNOWN for r in results),
        "task_records":results,
        "policies":policies,
        "original_policy_unchanged":True,
        "original_task_outcomes_unchanged":True,
        "source_linked_zero_accept_risk_is_undefined":True,
        "denominator_and_homogeneity_limits":[
            "Nine attempted tasks, not ten: Reflex had no patch and no original P9 decision.",
            "Matplotlib uses a final synthetic feedback stage while other cases are different agent-stage configurations. No homogeneous population inference.",
            "The lower/upper values apply only under explicitly declared F2P and baseline-admission rules; unknown tasks are free to be either successful or unsuccessful.",
            "The labels are issue-specific test results and source-attribution holds; not claims about deployment or comprehensive correctness.",
            "The bounds are sharp finite-case logical completions, not confidence intervals, weighted scores, new risk metric or proof of source-linked superiority.",
            "Original MR30 is distinct and remains locked."
        ]
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",type=Path,required=True)
    args=ap.parse_args()
    result=compute()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf8")
    print("P26_IDENTIFIED_POLICY_BOUNDS "+json.dumps(result["policies"],sort_keys=True))
    print("P26_TASK_ENDPOINT_COUNTS "+json.dumps({key:result[key] for key in (
        "selected_original_task_count","attempted_original_task_candidate_count",
        "endpoint_admitted_issue_specific_F2P_fail_count",
        "endpoint_admitted_original_task_pass_count",
        "endpoint_unknown_with_candidate_count")},sort_keys=True))


if __name__=="__main__":
    main()
