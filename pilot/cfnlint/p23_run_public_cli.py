#!/usr/bin/env python3
"""P23 original source cfn-lint E3510 real CLI, pre-hidden original task oracle.

Checks nine ADDITIONAL, openly declared minimal IAM managed-policy cases.
These integration checks were created after the source patch, but before
executing the CLI and before any original SWE-bench hidden task test.
The E3510 grammar acceptance is not AWS permission authorization validation.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import re
import subprocess
from pathlib import Path


def run(source:Path,stage:str,out:Path)->dict:
    reg_path=Path(__file__).with_name("P23_PUBLIC_CLI_E3510_CASES_20261120.json")
    config=json.loads(reg_path.read_text(encoding="utf8"))
    if config["n_cases"]!=9 or len(config["cases"])!=9:
        raise ValueError("Original additional source CLI case set changed")
    if stage not in ("historical_base","second_candidate"):
        raise ValueError(stage)
    source=source.resolve()
    if not (source/"src/cfnlint/data/schemas/other/iam/policy.json").is_file():
        raise ValueError("Original source IAM schema not found")
    out.mkdir(parents=True,exist_ok=True)
    cases=[]
    for item in config["cases"]:
        tmpl=copy.deepcopy(config["generated_template"])
        tmpl["Resources"]["Policy"]["Properties"]["PolicyDocument"]["Statement"]["Condition"]={
            item["operator"]:{item["key"]:item["value"]}}
        filepath=out/(item["case_id"]+".json")
        filepath.write_text(json.dumps(tmpl,indent=2)+"\n",encoding="utf8")
        process=subprocess.run(
           ["cfn-lint","--template",str(filepath),"--format","json","--regions","us-east-1"],
            text=True,capture_output=True,check=False,timeout=90)
        log=process.stdout+"\n"+process.stderr
        all_codes=sorted(set(re.findall(r"\b[EW]\d{4}\b",log)))
        has="E3510" in all_codes
        cases.append({
          "case_id":item["case_id"],
          "operator":item["operator"],
          "expected_e3510":item["expected_e3510"],
          "observed_e3510":has,
          "e3510_match":has==item["expected_e3510"],
          "cli_exit":process.returncode,
          "diagnostic_codes":all_codes,
          "cli_raw_log_sha256":hashlib.sha256(log.encode()).hexdigest(),
          "log_excerpt":log[:550],
        })
    digest=hashlib.sha256(reg_path.read_bytes()).hexdigest()
    obj={
      "study":"P23_source_public_cli_iam_condition_e3510_pre_hidden_v1",
      "stage":stage,
      "task":"aws-cloudformation__cfn-lint-3779",
      "original_base_sha":"de28d1e43777e3782a06b74d9091c3471636eb70",
      "cli_case_sha256":digest,
      "n_cases":len(cases),
      "matching_expectation":sum(x["e3510_match"] for x in cases),
      "mismatching_expectation":sum(not x["e3510_match"] for x in cases),
      "valid_expected_e3510_absent":sum((not x["expected_e3510"]) and (not x["observed_e3510"]) for x in cases),
      "invalid_expected_e3510_present":sum(x["expected_e3510"] and x["observed_e3510"] for x in cases),
      "cases":cases,
      "original_heldout_task_oracle_executed":False,
      "no_reference_patch_access":True,
      "code_agent_actor_independently_attested":False,
      "not_full_iam_authorization_semantics":True,
    }
    (out/"P23_CLI_E3510_REPORT.json").write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n")
    print("P23_CLI_E3510_RECEIPT "+json.dumps({k:v for k,v in obj.items() if k!="cases"},sort_keys=True))
    print("P23_CLI_PER_CASE "+json.dumps([{k:v for k,v in x.items() if k not in ("log_excerpt",)} for x in cases],sort_keys=True))
    return obj


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True,type=Path)
    p.add_argument("--stage",required=True,choices=("historical_base","second_candidate"))
    p.add_argument("--out",required=True,type=Path)
    args=p.parse_args()
    run(args.source,args.stage,args.out)
