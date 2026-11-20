#!/usr/bin/env python3
"""P19 freeze-before-candidate original ChatAdapter AST CPU test receipt runner.

Only executes source-visible tests authored before candidate. This is not a
Databricks LM optimization or an original SWE-bench-Live held-out verifier.
"""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
TEST=ROOT/"pilot/dspy/p19_visible_original_adapter_ast.py"
TARGET="dspy/adapters/chat_adapter.py"


def git(root,*args):
    return subprocess.check_output(["git","-C",str(root),*args],text=True).strip()


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--repo",type=Path,required=True)
    p.add_argument("--stage",choices=["historical_base","candidate"],required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    src=a.repo.resolve()
    os.environ["P19_DSPY_SOURCE_ROOT"]=str(src)
    import pydantic
    spec=importlib.util.spec_from_file_location("p19_visible_historical_chat_adapter",TEST)
    if spec is None or spec.loader is None:raise RuntimeError("Test file not importable")
    module=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=module
    spec.loader.exec_module(module)
    suite=unittest.TestLoader().loadTestsFromModule(module)
    registered=suite.countTestCases()
    if registered!=9:raise RuntimeError(f"Frozen P19 visible suite must contain 9 tests, found {registered}")
    log=io.StringIO()
    result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
    record={
      "schema":"99llm_X1_P19_historical_ChatAdapter_AST_visible_receipt_v1",
      "task":"stanfordnlp__dspy-1609",
      "stage":a.stage,
      "source_upstream_base_sha":"16ceaba5f7126ca86e5b50b669975c926b9f8f55",
      "head_sha":git(src,"rev-parse","HEAD"),
      "target_source_file":TARGET,
      "target_source_blob_sha":git(src,"hash-object",TARGET),
      "visible_tests_sha256":hashlib.sha256(TEST.read_bytes()).hexdigest(),
      "tests_run":result.testsRun,
      "passed":result.testsRun-len(result.errors)-len(result.failures)-len(result.skipped),
      "failed":len(result.failures),
      "errors":len(result.errors),
      "skipped":len(result.skipped),
      "status":"success" if result.wasSuccessful() else "failure",
      "source_ast_original_functions":True,
      "production_dspy_package_imported":False,
      "live_external_llm_called":False,
      "benchmark_gold_accessed":False,
      "true_task_oracle":False,
      "pydantic_version":pydantic.__version__,
      "completed_at_utc":datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z"),
    }
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(record,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    a.out.with_suffix(".unittest.log").write_text(log.getvalue(),encoding="utf-8")
    print("P19_VISIBLE_SOURCE_RECEIPT "+json.dumps(record,sort_keys=True))
    print(log.getvalue()[-16000:])
    if result.testsRun!=registered:raise SystemExit("Test collection incomplete")


if __name__=="__main__":
    main()
