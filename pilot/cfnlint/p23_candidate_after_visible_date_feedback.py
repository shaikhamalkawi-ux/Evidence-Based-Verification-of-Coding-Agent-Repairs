#!/usr/bin/env python3
"""P23 second, PRE-HIDDEN-ORACLE source patch: date comparison IAM operator regex.

This is an adaptive local iteration: 3 valid date-operator source cases remained
rejected after P23 first patch. Extend only the historical IAM Condition grammar
with the AWS-documented DateLessThan/DateGreaterThan family. No hidden benchmark
oracle outcome or reference solution was accessed at this stage.
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import subprocess
from pathlib import Path

FIRST_SHA="7ce6016f638058b44f471fee575a3b298c84b369"
FIRST_BLOB="50b226c27628fdaab4c27226702f9b5674b10a52"
TARGET="src/cfnlint/data/schemas/other/iam/policy.json"

def git(root,*args):
    return subprocess.check_output(["git","-C",str(root),*args],text=True).strip()

def main(root:Path,out:Path):
    root=root.resolve()
    if git(root,"rev-parse","HEAD")!=FIRST_SHA:
        raise ValueError("P23 second patch must begin exactly from first candidate")
    if git(root,"hash-object",TARGET)!=FIRST_BLOB:
        raise ValueError("First candidate schema blob did not match locked public receipt")
    fp=root/TARGET
    original=json.loads(fp.read_text(encoding="utf8"))
    candidate=copy.deepcopy(original)
    condition=candidate["definitions"]["Condition"]
    if condition["additionalProperties"] is not False:
        raise ValueError("Source schema no longer fails closed")
    patterns=condition["patternProperties"]
    if len(patterns)!=24:
        raise ValueError("Unexpected P23 first candidate pattern count")

    new={
      "^Date(Less|Greater)Than(Equals)?(IfExists)?$":{"$ref":"#/definitions/ConditionValue"},
      "^ForAllValues:Date(Less|Greater)Than(Equals)?(IfExists)?$":{"$ref":"#/definitions/ConditionSetValue"},
      "^ForAnyValue:Date(Less|Greater)Than(Equals)?(IfExists)?$":{"$ref":"#/definitions/ConditionSetValue"},
    }
    if any(k in patterns for k in new):
        raise ValueError("P23 second candidate expected absent Date comparison keys")
    for k,schema in new.items():
        re.compile(k)
        patterns[k]=schema
    assert len(patterns)==27
    for k in original["definitions"]["Condition"]["patternProperties"]:
        assert candidate["definitions"]["Condition"]["patternProperties"][k]==original["definitions"]["Condition"]["patternProperties"][k]
    undo=copy.deepcopy(candidate)
    for k in new:del undo["definitions"]["Condition"]["patternProperties"][k]
    if undo!=original:
        raise ValueError("P23 second candidate changed something besides 3 date patterns")
    fp.write_text(json.dumps(candidate,indent=1,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf8")
    subprocess.run(["git","-C",str(root),"diff","--check"],check=True)
    if git(root,"diff","--name-only").splitlines()!=[TARGET]:
        raise ValueError("P23 second candidate changed non-target paths")
    receipt={"first_head_sha":FIRST_SHA,"first_schema_blob":FIRST_BLOB,
             "new_pattern_count":3,"new_patterns":new,
             "all_other_original_fields_equal":True,
             "second_schema_blob":git(root,"hash-object",TARGET),
             "no_gold_access":True,"post_visible_adaptive_pre_hidden":True}
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
    print("P23_SECOND_DATE_PATTERN_PATCH "+json.dumps(receipt,sort_keys=True))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True,type=Path)
    p.add_argument("--out",required=True,type=Path)
    args=p.parse_args()
    main(args.source,args.out)
