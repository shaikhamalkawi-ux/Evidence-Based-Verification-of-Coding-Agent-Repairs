#!/usr/bin/env python3
"""P20 historical exact-source 10-test ScriptEventHandler actions check.

No Flask/SQLAlchemy runtime, no script execution, no hidden task oracle.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib, importlib.util, io, json, os
from pathlib import Path
import subprocess, sys, unittest

ROOT=Path(__file__).resolve().parents[1]
TEST=ROOT/"pilot/privacyidea/p20_visible_original_script_handler_ast.py"
TARGET="privacyidea/lib/eventhandler/scripthandler.py"


def git(repo,*args):
    return subprocess.check_output(["git","-C",str(repo),*args],text=True).strip()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path,required=True)
    ap.add_argument("--stage",choices=["original_base","first_candidate"],required=True)
    ap.add_argument("--out",type=Path,required=True)
    a=ap.parse_args()
    os.environ["P20_PRIVACYIDEA_SOURCE_ROOT"]=str(a.repo.resolve())
    spec=importlib.util.spec_from_file_location("p20_source_visible",TEST)
    if spec is None or spec.loader is None:
        raise ValueError("Cannot load frozen source test script")
    mod=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=mod
    spec.loader.exec_module(mod)
    suite=unittest.TestLoader().loadTestsFromModule(mod)
    expected=suite.countTestCases()
    if expected!=10:
        raise ValueError(f"Expected original 10 frozen source tests: {expected}")
    out=io.StringIO()
    result=unittest.TextTestRunner(stream=out,verbosity=2).run(suite)
    record={
       "schema":"99llm_X1_P20_historical_script_actions_visible_receipt_v1",
       "episode":"privacyidea__privacyidea-4251",
       "stage":a.stage,
       "source_base":"a44f38b40a61c5b91e6de68d20d27ed01d3ccb56",
       "head_sha":git(a.repo,"rev-parse","HEAD"),
       "source_blob_sha":git(a.repo,"hash-object",TARGET),
       "source_path":TARGET,
       "frozen_tests_sha256":hashlib.sha256(TEST.read_bytes()).hexdigest(),
       "tests":result.testsRun,
       "passed":result.testsRun-len(result.failures)-len(result.errors)-len(result.skipped),
       "failed":len(result.failures),
       "errors":len(result.errors),
       "skipped":len(result.skipped),
       "test_status":"success" if result.wasSuccessful() else "failure",
       "historical_class_AST_executed":True,
       "full_privacyidea_app_loaded":False,
       "Flask_HTTP_status_tested":False,
       "external_scripts_executed":False,
       "original_benchmark_oracle_accessed":False,
       "agent_independent_authorship_attested":False,
       "completed_utc":datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z"),
    }
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(record,sort_keys=True,indent=2)+"\n")
    a.out.with_suffix(".unittest.log").write_text(out.getvalue())
    print("P20_SOURCE_VISIBLE_RECEIPT "+json.dumps(record,sort_keys=True))
    print(out.getvalue()[-17000:])
    if result.testsRun!=expected:raise RuntimeError("Partial original suite execution")


if __name__=="__main__":
    main()
