#!/usr/bin/env python3
"""P21 endpoint validity gate for a pinned original-task oracle report.

Retrospective research QC. DOES NOT change source test results, original P9
decisions, historical benchmark report, source patch, or original frozen sample.
This is NOT a newly learned repair success classifier. It only determines
whether one evaluator result is sufficient for source-correctness attribution.
"""
import argparse
import json
from pathlib import Path

MISSING_FIXTURE = "swe100_fixture_clock"
ORIGINAL_TASK = "privacyidea__privacyidea-4251"
RAW_F2P_FAILED = 1
RAW_P2P_FAILED = 2022


def decide(raw: dict, diagnostic: dict) -> dict:
    if raw["task"] != ORIGINAL_TASK or diagnostic["task"] != ORIGINAL_TASK:
        raise ValueError("Task identity mismatch")
    source = raw["received_original_report"]
    if source["status"] != "complete":
        raise ValueError("Original raw report must remain archived")
    for key,expected in (("f2p_total",1),("f2p_passed",0),("p2p_failed",RAW_P2P_FAILED),
                         ("tests_executed",2023)):
        if source[key]!=expected: raise ValueError("Original report changed: "+key)
    if diagnostic["source_original_run_id"]!=source["source_url"].split("/")[-1] and \
       str(diagnostic["source_original_run_id"])!=source["source_url"].split("/")[-1]:
        raise ValueError("Original runner identity mismatch")
    if diagnostic["original_test_output_sha256"]!=source["original_test_output_sha256"]:
        raise ValueError("Original test output SHA changed")
    missing = diagnostic.get("missing_import_module_names",[])
    if not isinstance(missing,list) or any(not isinstance(v,str) for v in missing):
        raise ValueError("Invalid missing module family")
    common_import = (
        MISSING_FIXTURE in missing
        and diagnostic["error_family_occurrences"].get("ModuleNotFoundError",0)>=1
        and diagnostic["error_family_occurrences"].get("ImportError",0)>=1
        and diagnostic["raw_test_log_lines"]<source["tests_executed"]
        and diagnostic["p2p_failed"]==RAW_P2P_FAILED
    )
    return {
        "task":ORIGINAL_TASK,
        "original_harness_run_id":raw["original_harness_run_id"],
        "original_harness_report_status":"COMPLETE_RAW_UNRESOLVED",
        "reported_f2p_passed":source["f2p_passed"],
        "reported_f2p_total":source["f2p_total"],
        "reported_p2p_failed":source["p2p_failed"],
        "reported_tests":source["tests_executed"],
        "endpoint_admission_for_code_correctness":"HOLD_SYSTEMIC_TEST_IMPORT_FAILURE" if common_import else "HOLD_OTHER_UNADJUDICATED",
        "code_correctness_verified":None,
        "reason":"Original raw test output reports missing swe100_fixture_clock; cannot identify code failure or 2022 independent regressions." if common_import else "No admitted independent endpoint correctness judgment",
        "original_p9_policy_decisions":raw["original_preoracle_P9_decisions"],
        "original_p9_seal_sha256":raw["original_P9_decision_sha256"],
        "hidden_test_source_reproduced":False,
        "original_report_overwritten":False,
        "postreveal_quality_control_only":True,
        "no_new_agent_or_task":True,
    }


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--original",required=True,type=Path)
    ap.add_argument("--diagnostic",required=True,type=Path)
    ap.add_argument("--out",required=True,type=Path)
    args=ap.parse_args()
    ans=decide(json.loads(args.original.read_text()),json.loads(args.diagnostic.read_text()))
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(ans,sort_keys=True,indent=2)+"\n")
    print(json.dumps(ans,sort_keys=True))
