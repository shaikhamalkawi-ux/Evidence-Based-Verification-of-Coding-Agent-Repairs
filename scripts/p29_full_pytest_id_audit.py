#!/usr/bin/env python3
"""P29 source-locked raw FULL pytest summary ID comparison. Historical artifacts ONLY."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile

CASES = {
    "kedro": {
        "task":"kedro-org__kedro-4406",
        "report_candidate":"original_eval_report.json","report_control":"official_report.json",
        "candidate_run":44159300952,"control_run":44162955737,
        "candidate_log_sha256":"b3c2a0e6c924bbeac7fcc69e10bccb48d09da7628fe0ba6d8a77b651f3703994",
        "control_log_sha256":"4141f2b471ea4d0f53a1c3f7b51a41b03f7fc9641108dc34ed78d2ea9466b147",
        "candidate_failed":87,"control_failed":88,"candidate_passed":1630,"control_passed":1629,
        "scored_p2p_failed":25,"scored_p2p_passed":1566,"truncated_p2p":3,
        "f2p_name":"tests/ipython/test_ipython.py::TestLoadIPythonExtension::test_ipython_kedro_extension_alias"
    },
    "cfn_lint": {
        "task":"aws-cloudformation__cfn-lint-3779",
        "report_candidate":"original_report.json","report_control":"original_report.json",
        "candidate_run":44738711010,"control_run":44761416230,
        "candidate_log_sha256":"965babfbe839670397012b811098b2a307c5986d4272fcff5e4f29fd7c142650",
        "control_log_sha256":"a0f9fa312b5bb88da5ba652541420329cedfc9021ff9bd163466ffb636a9f441",
        "candidate_failed":7,"control_failed":8,"candidate_passed":1676,"control_passed":1675,
        "scored_p2p_failed":4,"scored_p2p_passed":1227,"truncated_p2p":0,
        "f2p_name":"test/unit/rules/resources/iam/test_identity_policy.py::TestIdentityPolicies::test_string_statements_with_condition"
    }
}
SUMMARY = re.compile(r"^(PASSED|FAILED) ((?:tests?|lib)/[^\r\n]+)$")


def load_bytes(source, name):
    p = Path(source)
    if p.is_dir():
        return (p/name).read_bytes()
    if p.suffix != ".zip":
        raise ValueError("Expected original artifact ZIP or extracted directory")
    with zipfile.ZipFile(p) as z:
        if z.testzip() is not None:
            raise ValueError("Invalid original ZIP")
        return z.read(name)


def parse_full_pytest_summary(raw):
    passed, failed = set(), set()
    cp = cf = 0
    for line in raw.decode("utf-8").splitlines():
        m = SUMMARY.fullmatch(line)
        if not m:
            continue
        kind, node = m.groups()
        if "::" not in node or node.count("[") != node.count("]"):
            raise AssertionError("Malformed full pytest node ID")
        if kind == "PASSED":
            cp += 1
            passed.add(node)
        else:
            cf += 1
            failed.add(node)
    if cp != len(passed) or cf != len(failed) or (passed & failed):
        raise AssertionError("Duplicate or conflicting full node status")
    if cp == 0 or cf == 0:
        raise AssertionError("Missing full summary statuses")
    return passed, failed


def set_digest(items):
    return hashlib.sha256(("\n".join(sorted(items))+"\n").encode()).hexdigest()


def count_parser_truncation(values):
    return sum("[" in x and "]" not in x for x in values)


def parse_official(raw, task):
    obj = json.loads(raw)
    if set(obj) != {task}:
        raise AssertionError("Original task ID mismatch")
    report = obj[task]
    st = report["tests_status"]
    f, p = st["FAIL_TO_PASS"], st["PASS_TO_PASS"]
    for g in (f,p):
        for key in ("success","failure"):
            if not isinstance(g[key], list) or len(g[key]) != len(set(g[key])):
                raise AssertionError("Invalid/duplicate official test identifier")
    return report,f,p


def audit_pair(case, candidate, control):
    cfg = CASES[case]
    a = load_bytes(candidate,"original_test_output.txt")
    b = load_bytes(control,"original_test_output.txt")
    if hashlib.sha256(a).hexdigest() != cfg["candidate_log_sha256"]:
        raise AssertionError("Original candidate text hash mismatch")
    if hashlib.sha256(b).hexdigest() != cfg["control_log_sha256"]:
        raise AssertionError("Original control text hash mismatch")
    cp, cf = parse_full_pytest_summary(a)
    np, nf = parse_full_pytest_summary(b)
    cr,ff,pp = parse_official(load_bytes(candidate,cfg["report_candidate"]),cfg["task"])
    nr,fn,pn = parse_official(load_bytes(control,cfg["report_control"]),cfg["task"])
    if cr["resolved"] is not False or nr["resolved"] is not False:
        raise AssertionError("Original strict benchmark scores not preserved")
    if not (len(ff["success"])==len(fn["failure"])==1 and not ff["failure"] and not fn["success"]
            and ff["success"][0]==fn["failure"][0]==cfg["f2p_name"]):
        raise AssertionError("Issue-specific F2P contrast lost")
    if not (len(pp["failure"])==len(pn["failure"])==cfg["scored_p2p_failed"] and
            len(pp["success"])==len(pn["success"])==cfg["scored_p2p_passed"] and
            set(pp["failure"])==set(pn["failure"])):
        raise AssertionError("Original P2P matched report no longer agrees")
    if count_parser_truncation(pp["failure"]) != cfg["truncated_p2p"]:
        raise AssertionError("Parser-truncated original P2P identifiers changed")
    if [len(cf),len(nf),len(cp),len(np)] != [
            cfg["candidate_failed"],cfg["control_failed"],cfg["candidate_passed"],cfg["control_passed"]]:
        raise AssertionError("Full raw pytest outcome totals differ")
    if cf-nf or nf-cf != {cfg["f2p_name"]}:
        raise AssertionError("Unmatched raw complete FAILED test ID")
    if cp-np != {cfg["f2p_name"]} or np-cp:
        raise AssertionError("Raw complete PASSED test ID differs")
    return {
        "task":cfg["task"],"candidate_run":cfg["candidate_run"],"neutral_run":cfg["control_run"],
        "raw_candidate_failed_full_ids":len(cf),"raw_neutral_failed_full_ids":len(nf),
        "raw_candidate_passed_full_ids":len(cp),"raw_neutral_passed_full_ids":len(np),
        "raw_shared_failed_full_ids":len(cf & nf),"raw_candidate_only_failed_full_ids":len(cf-nf),
        "raw_control_only_failed_full_ids":len(nf-cf),
        "candidate_failed_full_ids_sha256":set_digest(cf),
        "neutral_failed_full_ids_sha256":set_digest(nf),
        "original_scored_p2p_failed_each":cfg["scored_p2p_failed"],
        "official_report_truncated_p2p_ids":cfg["truncated_p2p"],
        "postreveal_control":True,"new_task_or_agent_run":False,
        "original_strict_resolved":False,
        "warning":"Raw full pytest names are not official F2P/P2P counts or independent tasks."
    }


def compute(paths):
    return {
        "schema":"99llm_X1_P29_full_pytest_names_from_original_artifacts_v1",
        "scope":"HISTORICAL_ARTIFACT_REPLAY_NO_NEW_BENCHMARK",
        "cases":{name:audit_pair(name,*paths[name]) for name in CASES},
        "all_previous_P9_P26_P27_and_MR30_locked":True,
        "upstream_issue113_gold_reproduction_rerun_by_this_code":False,
        "new_actor_provenance":False
    }


def main():
    parser = argparse.ArgumentParser()
    for s in ("kedro_candidate","kedro_control","cfn_candidate","cfn_control"):
        parser.add_argument("--"+s.replace("_","-"),required=True)
    parser.add_argument("--out",required=True)
    a=parser.parse_args()
    data=compute({"kedro":(a.kedro_candidate,a.kedro_control),
                  "cfn_lint":(a.cfn_candidate,a.cfn_control)})
    dest=Path(a.out); dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("P29_COMPLETE_SOURCE_RAW_PYTEST_NAME_AUDIT "+json.dumps(data["cases"],sort_keys=True))
    print("P29_ORIGINAL_POLICY_AND_BENCHMARK_UNCHANGED")


if __name__=="__main__":
    main()
