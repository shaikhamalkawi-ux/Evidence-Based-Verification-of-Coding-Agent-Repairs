#!/usr/bin/env python3
"""P23 first single-file source patch: canonicalize historical IAM Condition regexes.

Only jsonschema definitions.Condition.patternProperties regex keys are changed,
no "allow everything" bypass. Existing ConditionValue vs ConditionSetValue refs,
all other JSON fields, invalid operator rejection and additionalProperties=false
are unchanged. This is an AI-assisted source patch, NOT agent-authorship proof.
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import subprocess
from pathlib import Path

BASE_SHA="de28d1e43777e3782a06b74d9091c3471636eb70"
SOURCE_BLOB="99f30247c838aea3910f891a54c9bbad1d67c88a"
TARGET="src/cfnlint/data/schemas/other/iam/policy.json"


def git(root,*args):
    return subprocess.check_output(["git","-C",str(root),*args],text=True).strip()


def rewrite_one(key: str)->str:
    # Original grammar has 8 ForAllValues, 8 ForAnyValues and 8 scalar entries.
    qualifier=None
    if key.startswith("ForAllValues:"):
        qualifier="ForAllValues"
    elif key.startswith("ForAnyValues:"):
        qualifier="ForAnyValue"    # AWS singular, not ForAnyValues
    if qualifier is not None:
        atom=key.split(":",1)[1]
        if not (atom.startswith("^") and atom.endswith("$")):
            raise ValueError("Unexpected original set operator regex "+key)
        atom=atom[1:-1]
        atom=atom.replace("Like?","Like") # fix accidental optional 'e'
        atom=atom.replace("Number","Numeric")
        if "(Exists)?" in atom or "(IfExists)?" in atom:
            raise ValueError("Unexpected qualified operator modifier "+key)
        new=f"^{qualifier}:{atom}(IfExists)?$"
    else:
        if not (key.startswith("^") and key.endswith("$") and "(Exists)?" in key):
            raise ValueError("Unexpected original ordinary operator regex "+key)
        atom=key[1:-1].replace("Number","Numeric").replace("(Exists)?","(IfExists)?")
        new=f"^{atom}$"
    re.compile(new)
    return new


def patch(source:Path)->dict:
    source=source.resolve()
    if git(source,"rev-parse","HEAD")!=BASE_SHA:
        raise ValueError("P23 historical source commit not exact")
    if git(source,"hash-object",TARGET)!=SOURCE_BLOB:
        raise ValueError("P23 historical schema blob not exact")
    fp=source/TARGET
    original=json.loads(fp.read_text(encoding="utf8"))
    before=copy.deepcopy(original)
    condition=original["definitions"]["Condition"]
    if condition.get("additionalProperties") is not False:
        raise ValueError("IAM schema must fail closed on unknown operator names")
    entries=condition["patternProperties"]
    if len(entries)!=24:
        raise ValueError("Unexpected historical regex count, avoid accidental rewrite")
    normalized={}
    mappings=[]
    for key,spec in entries.items():
        rewritten=rewrite_one(key)
        if rewritten in normalized:
            raise ValueError("Regex key collision: "+rewritten)
        normalized[rewritten]=spec
        mappings.append({"before":key,"after":rewritten})
    condition["patternProperties"]=normalized
    assert condition["properties"]==before["definitions"]["Condition"]["properties"]
    restored=copy.deepcopy(original)
    restored["definitions"]["Condition"]["patternProperties"]=before["definitions"]["Condition"]["patternProperties"]
    if restored!=before:
        raise AssertionError("P23 candidate attempted to modify non-Condition-patternProperties content")
    fp.write_text(json.dumps(original,ensure_ascii=False,sort_keys=True,indent=1)+"\n",encoding="utf8")
    subprocess.run(["git","-C",str(source),"diff","--check"],check=True)
    changed=git(source,"diff","--name-only").splitlines()
    if changed!=[TARGET]:
        raise ValueError("Unexpected modified paths: "+repr(changed))
    return {"rewritten_patterns":len(mappings),"mappings":mappings,"source_blob":git(source,"hash-object",TARGET)}


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True,type=Path)
    p.add_argument("--out",required=True,type=Path)
    args=p.parse_args()
    result=patch(args.source)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf8")
    print("P23_FIRST_CANDIDATE_FIXED_PATTERN_COUNT="+str(result["rewritten_patterns"]))
    print("P23_FIRST_CANDIDATE_SCHEMA_BLOB="+result["source_blob"])
    print("P23_SOURCE_SCOPE=CONDITION_PATTERN_PROPERTIES_ONLY")
    print("P23_ORIGINAL_BENCHMARK_GOLD_NOT_ACCESSED")
