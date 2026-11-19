#!/usr/bin/env python3
"""Run a frozen, actual-source DoRALinear CPU unittest suite and retain receipt.

The suite uses historical source AST and import-only stubs for nonquantized
DoRA. This is NOT 2-GPU torchtune recipe integration or original task oracle.
"""
from __future__ import annotations
import argparse
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest


def git(repo,*args):
    return subprocess.check_output(["git","-C",str(repo),*args],text=True).strip()


def run(repo: Path, phase: str, out: Path):
    os.environ["P17_TORCHTUNE_SOURCE_ROOT"]=str(repo)
    import torch

    loader=unittest.TestLoader()
    suite=loader.discover(start_dir=str(Path(__file__).resolve().parents[1]/"pilot/torchtune"),
                          pattern="p17_visible_original_dora_cpu.py")
    tests=suite.countTestCases()
    if tests!=6:raise ValueError("P17 must have exactly six frozen CPU checks")
    io_capture=io.StringIO()
    with redirect_stdout(io_capture),redirect_stderr(io_capture):
        result=unittest.TextTestRunner(stream=io_capture,verbosity=2).run(suite)
    body=io_capture.getvalue()
    receipt={
      "phase":phase,"task":"pytorch__torchtune-2139",
      "repo_base":"f2bd4bc25b24587aef40f486087412b9da8f1d94",
      "head_sha":git(repo,"rev-parse","HEAD"),
      "source_git_blob":git(repo,"hash-object","torchtune/modules/peft/dora.py"),
      "tests_executed":result.testsRun,
      "passes":result.testsRun-len(result.failures)-len(result.errors)-len(result.skipped),
      "failures":len(result.failures),"errors":len(result.errors),
      "skipped":len(result.skipped),
      "status":"SUCCESS" if result.wasSuccessful() else "VISIBLE_SOURCE_DIAGNOSTIC_FAILURE",
      "tested_historical_source_ast":True,
      "import_only_stubs_not_fully_imported_torchtune":True,
      "quantized_path_not_run":True,
      "GPU_FSDP_2RANK_tested":False,
      "original_task_oracle_executed":False,
      "candidate_authorship_independently_attested":False,
      "torch_version":str(torch.__version__),
      "visible_tests_sha256":hashlib.sha256(
        (Path(__file__).resolve().parents[1]/"pilot/torchtune/p17_visible_original_dora_cpu.py").read_bytes()
      ).hexdigest(),
      "completed_utc":datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z"),
    }
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    out.with_suffix(".unittest.log").write_text(body,encoding="utf-8")
    print("P17_VISIBLE_SOURCE_RECEIPT "+json.dumps(receipt,sort_keys=True))
    print(body[-15000:])
    if result.testsRun!=tests:raise ValueError("Unexpected original-source test shortfall")
    return receipt


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--repo",type=Path,required=True)
    parser.add_argument("--phase",choices=("base","initial_candidate"),required=True)
    parser.add_argument("--out",type=Path,required=True)
    a=parser.parse_args()
    run(a.repo.resolve(),a.phase,a.out)
