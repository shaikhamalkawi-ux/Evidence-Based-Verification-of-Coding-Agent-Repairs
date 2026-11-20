#!/usr/bin/env python3
"""P23 frozen visible IAM condition operator grammar tests on original cfn-lint schema.

This executes the unchanged historical IAM policy.json through Draft7Validator.
Neither hidden SWE-bench task tests nor reference fixes are accessed. The test
cases and this executable are frozen before creating the first source patch.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

TASK="aws-cloudformation__cfn-lint-3779"
BASE_SHA="de28d1e43777e3782a06b74d9091c3471636eb70"
SCHEMA_PATH="src/cfnlint/data/schemas/other/iam/policy.json"
SCHEMA_BLOB="99f30247c838aea3910f891a54c9bbad1d67c88a"
CASES=Path(__file__).with_name("P23_FROZEN_VISIBLE_IAM_CASES_20261120.json")

def git(root,*args):
    return subprocess.check_output(["git","-C",str(root),*args],text=True).strip()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--source",type=Path,required=True)
    parser.add_argument("--stage",choices=("historical_base","first_candidate"),required=True)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()

    from jsonschema import Draft7Validator

    source=args.source.resolve()
    head=git(source,"rev-parse","HEAD")
    blob=git(source,"hash-object",SCHEMA_PATH)
    if args.stage=="historical_base" and (head!=BASE_SHA or blob!=SCHEMA_BLOB):
        raise ValueError("P23 historical original schema base blob mismatch")
    if args.stage=="first_candidate" and head==BASE_SHA:
        raise ValueError("P23 expected a committed candidate not historical base")

    cases=json.loads(CASES.read_text(encoding="utf8"))
    assert cases["case_count"]==64
    assert cases["valid_count"]==45 and cases["invalid_count"]==19
    assert cases["original_policy_schema_blob"]==SCHEMA_BLOB
    assert cases["original_base_sha"]==BASE_SHA
    assert len({x["case_id"] for x in cases["cases"]})==64
    assert any(x["operator"]=="ForAnyValue:StringEquals" for x in cases["cases"])
    assert any(x["operator"]=="StringEqualsIfExists" for x in cases["cases"])

    schema=json.loads((source/SCHEMA_PATH).read_text(encoding="utf8"))
    assert "Condition" in schema["definitions"]
    assert schema["definitions"]["Condition"]["additionalProperties"] is False
    # Deliberately no AWS IAM action authorization claims here; only operator
    # grammar and original schema value shape, with unchanged local test data.
    rule={"$ref":"#/definitions/Condition","definitions":schema["definitions"]}
    Draft7Validator.check_schema(rule)
    validator=Draft7Validator(rule)

    observations=[]
    for case in cases["cases"]:
        value=cases["fixed_test_values"][case["value_kind"]]
        condition={case["operator"]:value}
        errors=list(validator.iter_errors(condition))
        actual=len(errors)==0
        observations.append({
            "case_id":case["case_id"],
            "operator":case["operator"],
            "expected_valid":case["expected_valid"],
            "schema_accepted":actual,
            "correct_classification":case["expected_valid"]==actual,
            "validation_error_count":len(errors),
        })

    record={
      "schema":"99llm_P23_FROZEN_VISIBLE_SOURCE_SCHEMA_GRAMMAR_v1",
      "task":TASK,
      "stage":args.stage,
      "original_base_sha":BASE_SHA,
      "source_head_sha":head,
      "actual_source_schema_blob":blob,
      "original_source_schema_blob":SCHEMA_BLOB,
      "source_schema_path":SCHEMA_PATH,
      "frozen_case_sha256":hashlib.sha256(CASES.read_bytes()).hexdigest(),
      "case_count":len(observations),
      "admitted_cases":sum(x["schema_accepted"] for x in observations),
      "classification_passed":sum(x["correct_classification"] for x in observations),
      "classification_failed":sum(not x["correct_classification"] for x in observations),
      "misclassified_case_ids":[x["case_id"] for x in observations if not x["correct_classification"]],
      "cases":observations,
      "python_version":sys.version.split()[0],
      "jsonschema_version":__import__("importlib.metadata",fromlist=["version"]).version("jsonschema"),
      "hidden_original_task_oracle_accessed":False,
      "original_agent_attested":False,
      "source_benchmark_gold_patch_used":False,
      "task_resolved_claim":False,
      "scientific_scope":"Schema grammar acceptance only, not original task oracle or complete IAM service authorization"
    }
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(record,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("P23_FROZEN_IAM_SCHEMA_RECEIPT "+json.dumps({k:v for k,v in record.items() if k!="cases"},sort_keys=True))
    if len(observations)!=64:
        raise ValueError("P23 frozen count mismatch")

if __name__=="__main__":
    main()
