#!/usr/bin/env python3
"""P14 two-stage task-level reconciliation of postseal original-oracle receipts.

The original P9 oracle-label logic and policy decisions remain unchanged.
The two measured candidate revisions are correlated observations of ONE task.
This script does not run a task oracle, change any candidate patch, or consult
benchmark gold patches. It admits unknown/error outcomes as nonadmitted.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
P14 = ROOT / "pilot/matplotlib"
SEAL = P14 / "sealed"
REGISTER = P14 / "P14_PREORACLE_EVALUATION_REGISTER.json"
STAGES = ("stage1", "stage2")
HEX40 = re.compile(r"^[0-9a-f]{40}$")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(s) for s in path.read_text(encoding="utf-8").splitlines() if s.strip()]


def admissions(records: list[dict], frozen: dict, decisions: list[dict],
               oracle_label) -> list[dict]:
    """Exactly two registered stage rows, without episode substitution."""
    if len(records) != 2 or len(decisions) != 2:
        raise ValueError("Must retain both original stage records.")
    ids = [r.get("episode_id") for r in records]
    if len(set(ids)) != 2:
        raise ValueError("Duplicate or replaced P14 stage.")
    by_id = {d["episode_id"]: d for d in decisions}
    outcomes = []
    for stage in STAGES:
        info = frozen[stage]
        episode_id = info["episode_id"]
        matching = [r for r in records if r["episode_id"] == episode_id]
        if len(matching) != 1:
            raise ValueError("Missing or substituted exact stage: " + stage)
        r = matching[0]
        dec = by_id[episode_id]
        if r.get("stage") != stage or r.get("head_sha") != info["candidate_sha"]:
            raise ValueError("Stage/source SHA mismatch")
        if r.get("original_harness_commit") != frozen["harness_sha"]:
            raise ValueError("Changed original evaluator")
        if r.get("dataset_revision") != frozen["dataset_revision_sha"]:
            raise ValueError("Changed source dataset")
        if r.get("scientific_scope") != "TWO_CORRELATED_STAGE_CANDIDATES_FROM_ONE_SYNTHETIC_FEEDBACK_TASK":
            raise ValueError("Invalid scientific boundary")
        if r.get("human_developer_feedback") is not False:
            raise ValueError("Synthetic human attribution")
        if r.get("agent_authorship_independently_attested") is not False:
            raise ValueError("Unjustified agent attestation")
        if r.get("matched_reports") is not None and (
            type(r["matched_reports"]) is not int or r["matched_reports"] < 0):
            raise ValueError("Invalid number of original reports")
        if r.get("status") == "complete" and r.get("matched_reports") != 1:
            raise ValueError("Ambiguous original reports cannot be admitted")
        result, reason = oracle_label(dec, r)
        if result is not None:
            if r.get("official_resolved") is not None:
                if type(r["official_resolved"]) is not bool or r["official_resolved"] != bool(result):
                    raise ValueError("Disagreement between original benchmark and test counts")
            output_hash = r.get("original_test_output_sha256")
            if not isinstance(output_hash, str) or len(output_hash) != 64:
                raise ValueError("Missing executed original test evidence hash")
        outcomes.append({
            "stage":stage,
            "episode_id":episode_id,
            "candidate_sha":info["candidate_sha"],
            "predecision_policies":dec["decisions"],
            "oracle_admitted":result is not None,
            "nonadmission_reason":None if result is not None else reason,
            "original_task_pass":None if result is None else bool(result),
            "f2p_total":r.get("f2p_total") if result is not None else None,
            "f2p_passed":r.get("f2p_passed") if result is not None else None,
            "p2p_failed":r.get("p2p_failed") if result is not None else None,
            "tests_executed":r.get("tests_executed") if result is not None else None,
            "source_url":r.get("source_url"),
        })
    return outcomes


def run(oracle_jsonl: Path, output_path: Path) -> dict:
    from sys import path as sys_path
    sys_path.insert(0, str(ROOT / "scripts"))
    from p9_reveal import oracle_label, run as score_p9

    frame = load(ROOT/"pilot/frozen_task_frame_20261117.json")
    frozen = load(REGISTER)
    if len(frame["selected"]) != 10 or frame["selected"][2]["instance_id"] != frozen["task"]:
        raise ValueError("Lost original preselected task denominator")
    if frozen["stage1_stage2_statistical_independence"] is not False:
        raise ValueError("Do not treat two revisions as two independent tasks")
    if frozen["feedback_real_human"] is not False or frozen["agent_authorship_independently_attested"] is not False:
        raise ValueError("Incorrect human/agent provenance")

    seal = load(SEAL/"P9_DECISION_SEAL.json")
    raw_dec = (SEAL/"P9_DECISIONS_SEALED.jsonl").read_bytes()
    raw_input = (SEAL/"P14_DECISION_INPUT.jsonl").read_bytes()
    for observed, expected in (
        (hashlib.sha256(raw_dec).hexdigest(),seal["decisions_sha256"]),
        (hashlib.sha256(raw_input).hexdigest(),seal["input_sha256"]),
        (hashlib.sha256((ROOT/"scripts/p9_decide.py").read_bytes()).hexdigest(),seal["script_sha256"]),
        (seal["decisions_sha256"],frozen["preoracle_decisions_sha256"]),
        (seal["input_sha256"],frozen["preoracle_input_sha256"]),
    ):
        if observed != expected:
            raise ValueError("Original P14 decision seal integrity failure")
    decisions = read_jsonl(SEAL/"P9_DECISIONS_SEALED.jsonl")
    records = read_jsonl(oracle_jsonl)
    outcomes = admissions(records,frozen,decisions,oracle_label)

    p9_output = output_path.with_suffix(".p9_comparison.json")
    p9_score = score_p9(SEAL, oracle_jsonl, p9_output)
    if p9_score["total_decisions"] != 2:
        raise ValueError("P9 denominator must be two correlated decisions")
    if p9_score["oracle_admitted"] != sum(x["oracle_admitted"] for x in outcomes):
        raise ValueError("P9 admission mismatch")
    if len({x["candidate_sha"] for x in outcomes}) != 2:
        raise ValueError("Both original patch SHAs must remain identifiable")

    if all(x["oracle_admitted"] for x in outcomes):
        a,b = (x["original_task_pass"] for x in outcomes)
        if not a and b:
            transition = "UNRESOLVED_TO_RESOLVED_AFTER_SYNTHETIC_FEEDBACK"
        elif a and not b:
            transition = "RESOLVED_TO_UNRESOLVED_AFTER_SYNTHETIC_FEEDBACK"
        elif a and b:
            transition = "BOTH_CANDIDATES_PASS"
        else:
            transition = "NEITHER_CANDIDATE_RESOLVES_TASK"
    else:
        transition = "UNKNOWN_INCOMPLETE_ORACLE"

    summary = {
        "project":"99llm-X1-P14",
        "task":"matplotlib__matplotlib-28933",
        "task_count_in_this_experiment":1,
        "candidate_stage_count":2,
        "stages_statistically_independent":False,
        "feedback_type":"AI-generated scripted correction based on genuine visible failure",
        "human_developer_feedback":False,
        "agent_authorship_independently_attested":False,
        "decision_sha256":seal["decisions_sha256"],
        "policy_version":seal["policy_version"],
        "hidden_original_oracle_admitted_stage_count":p9_score["oracle_admitted"],
        "hidden_original_oracle_unadmitted_stage_count":p9_score["oracle_unadmitted"],
        "transition":transition,
        "stages":outcomes,
        "original_p9_score":p9_score,
        "scientific_limit":"One correlated task, not independent n=2 and not a causal or generalizable policy superiority evaluation",
    }
    output_path.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return summary


if __name__ == "__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--oracle-jsonl",required=True,type=Path)
    ap.add_argument("--out",required=True,type=Path)
    args=ap.parse_args()
    print(json.dumps(run(args.oracle_jsonl,args.out),indent=2,sort_keys=True))
