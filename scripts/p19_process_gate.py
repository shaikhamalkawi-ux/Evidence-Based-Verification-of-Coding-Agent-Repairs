#!/usr/bin/env python3
"""P19 V1 process-linked admission, strictly separate from frozen P9.

No agent-authentication claim. No original benchmark oracle/gold/heldout labels.
This is a prospective one-case process-gate diagnostic, NOT an efficacy proof.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
VERSION="X1-P19-artifact-linked-no-actor-v1"
EXPECTED={
  "task":"stanfordnlp__dspy-1609",
  "base":"16ceaba5f7126ca86e5b50b669975c926b9f8f55",
  "source_file":"dspy/adapters/chat_adapter.py",
  "test_sha256":"c8c47bf6ae3c641c47683d2becb181ee208f397309e81055bc09a3cc43f51104",
  "candidate_sha":"2a2938cbd2b616c684768902bdcc0bfc09e7b9a4",
  "candidate_blob":"5aece153412ca5a1e6f4c7e95815b17ec561ec32",
  "patch_sha256":"e9771581fa04391b72b86f0da93495c0749e6f10f84452a83c4e8d2968a98a08",
  "tests":9,
}
FORBIDDEN={"oracle","oracle_status","oracle_result","future_ci","future_test",
           "heldout_result","label","resolved","task_outcome","test_patch",
           "FAIL_TO_PASS","PASS_TO_PASS"}


def _utc(s):
    if not isinstance(s,str) or not s.endswith("Z"):
        raise ValueError("Timestamp must be UTC Z")
    return datetime.fromisoformat(s.replace("Z","+00:00"))


def run(inp:Path,out:Path):
    text=inp.read_text(encoding="utf-8").splitlines()
    if len(text)!=1:raise ValueError("Exactly one P19 decision unit")
    record=json.loads(text[0])
    if FORBIDDEN.intersection(record):
        raise ValueError("Original oracle leakage into prospective decision features")
    p=ROOT/"pilot/dspy/P19_PREREGISTRATION_20261120.json"
    reg=json.loads(p.read_text(encoding="utf-8"))
    frame=json.loads((ROOT/"pilot/frozen_task_frame_20261117.json").read_text(encoding="utf-8"))
    if frame["selected"][5]["instance_id"]!=EXPECTED["task"] or reg["task"]["instance_id"]!=EXPECTED["task"]:
        raise ValueError("Original frozen selection frame mismatch")
    if reg["prospective_process_only_v1"]["name"]!="artifact_linked_no_actor_v1_P19_PROSPECTIVE":
        raise ValueError("Changed registered process gate name")
    src=record.get("source_verification",{})
    features={
      "patch_applied":record.get("patch_applied") is True,
      "fixed_task":src.get("task")==EXPECTED["task"],
      "original_base_exact":src.get("base_sha")==EXPECTED["base"],
      "source_file_exact":src.get("source_file")==EXPECTED["source_file"],
      "candidate_sha_exact":record.get("head_sha")==EXPECTED["candidate_sha"],
      "candidate_source_blob_exact":src.get("candidate_source_blob")==EXPECTED["candidate_blob"],
      "patch_sha256_exact":src.get("patch_sha256")==EXPECTED["patch_sha256"],
      "frozen_test_sha256_exact":src.get("frozen_visible_tests_sha256")==EXPECTED["test_sha256"],
      "visible_suite_fixed_before_candidate":src.get("visible_suite_preregistered") is True,
      "visible_suite_all_nine_pass":src.get("visible_passed")==EXPECTED["tests"] and src.get("visible_total")==EXPECTED["tests"],
      "visible_no_errors_skips":src.get("visible_failed")==0 and src.get("visible_errors")==0 and src.get("visible_skipped")==0,
      "legacy_controls_preserved":src.get("legacy_untyped_input_and_scalar_controls_pass") is True,
      "source_patch_only":src.get("only_historical_chat_adapter_modified") is True,
      "no_unrelated_edit":record.get("unrelated_intervening_edit") is False,
      "no_actor_authentication_claim":record.get("target_agent_is_commit_author") is False,
    }
    receipts=record.get("receipts",[])
    if len(receipts)!=1:raise ValueError("One prespecified visible receipt required")
    q=receipts[0]
    features.update({
      "receipt_kind_local":q.get("kind")=="local_test",
      "receipt_sha_exact":q.get("head_sha")==record.get("head_sha"),
      "receipt_scope_prespecified":q.get("test_scope_prespecified") is True,
      "receipt_nonempty_all_pass":q.get("status")=="success" and q.get("test_count")==EXPECTED["tests"],
      "receipt_source_url":q.get("source_url")=="https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44666349696",
      "receipt_completed_before_seal":_utc(q.get("completed_at")) <= _utc(record.get("t_decision")),
    })
    result={
      "policy_version":VERSION,
      "task":EXPECTED["task"],
      "episode_id":record["episode_id"],
      "head_sha":record["head_sha"],
      "t_decision":record["t_decision"],
      "decision":"ACCEPT" if all(features.values()) else "HOLD",
      "features":features,
      "actor_model_identity_independently_attested":False,
      "this_is_original_P9_source_linked_policy":False,
      "reference_oracle_used":False,
      "scientific_scope":"One newly preregistered, artifact-only prospective gate; not causal or multi-task policy superiority",
      "input_sha256":hashlib.sha256(inp.read_bytes()).hexdigest(),
      "policy_script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      "prespecified_protocol_sha256":hashlib.sha256(p.read_bytes()).hexdigest()
    }
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,sort_keys=True,separators=(",",":"),ensure_ascii=False)+"\n",encoding="utf-8")
    print("P19_PROCESS_V1_SOURCE_ONLY_DECISION "+json.dumps(result,sort_keys=True))
    print("P19_PROCESS_V1_NOT_ACTOR_ATTESTED_AND_NOT_ORIGINAL_P9")
    return result


if __name__=="__main__":
    a=argparse.ArgumentParser()
    a.add_argument("--input",required=True,type=Path)
    a.add_argument("--out",required=True,type=Path)
    t=a.parse_args()
    run(t.input,t.out)
