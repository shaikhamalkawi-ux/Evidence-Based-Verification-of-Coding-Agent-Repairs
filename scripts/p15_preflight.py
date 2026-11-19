#!/usr/bin/env python3
"""P15 source- and resource-locked TWO-GPU feasibility preflight (NO candidate patch).

This script never loads hidden SWE-bench task tests, never invokes a training
recipe, never accesses reference repair/gold files and never asserts that a
CPU-only surrogate verifies the original two-GPU DoRA task.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "protocol/P15_TORCHTUNE_RESOURCE_AND_ACTOR_FEASIBILITY_20261119.json"
FRAME = ROOT / "pilot/frozen_task_frame_20261117.json"


def canonical(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def time_utc():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def determine_status(nvidia_count, torch_count, nvidia_devices, smi_installed):
    """Hardware availability only; no prediction of benchmark resolution."""
    counts = [c for c in (nvidia_count, torch_count) if type(c) is int and c >= 0]
    if not isinstance(nvidia_devices, list):
        raise ValueError("NVIDIA node list must be a list")
    if any(not isinstance(node, str) or not node.startswith("/dev/nvidia") for node in nvidia_devices):
        raise ValueError("Unexpected GPU device node")
    if len(nvidia_devices) == 0 and (not counts or max(counts) < 2):
        return "RESOURCE_HOLD_FULL_TWO_GPU_REPRO"
    if counts and min(counts) >= 2:
        return "TWO_GPU_HARDWARE_OBSERVED_NOT_FULL_TASK_ADMISSION"
    return "UNKNOWN_GPU_ACCESS_PRESERVE_TASK"


def preflight():
    reg = json.loads(PATH.read_text(encoding="utf-8"))
    frame = json.loads(FRAME.read_text(encoding="utf-8"))
    task = reg["next_frozen_case"]
    idx = task["index_one_based"] - 1
    assert idx == 4 and frame["n_selected"] == len(frame["selected"]) == 10
    assert frame["selected"][idx]["instance_id"] == task["instance_id"]
    assert frame["selected"][idx]["repo"] == task["original_repo_identifier"]
    assert frame["dataset_revision_sha"] == reg["source_dataset_rev"]
    assert task["original_base_sha"] == "f2bd4bc25b24587aef40f486087412b9da8f1d94"
    assert task["frozen_visible_problem_sha256"] == "31a8dfd18349fa14a79aa3958c6f166a475dd8f8cd4a48a098bf38a16e3b1cdf"
    assert reg["experimental_gates"]["gate_C_coding_attempt"]["no_candidate_written_in_P15"] is True

    smi = shutil.which("nvidia-smi")
    if smi:
        try:
            process = subprocess.run([smi,"--query-gpu=index,name,memory.total","--format=csv,noheader,nounits"],
                                      capture_output=True,text=True,check=False,timeout=12)
            code=process.returncode
            smi_lines=[s.strip() for s in process.stdout.splitlines() if s.strip()]
            count=len(smi_lines) if code == 0 else None
            smi_error=process.stderr[:600]
        except (OSError, subprocess.TimeoutExpired) as e:
            code=None
            count=None
            smi_lines=[]
            smi_error=type(e).__name__ + ": " + str(e)[:300]
    else:
        code=None
        count=None
        smi_lines=[]
        smi_error="nvidia-smi binary absent on the workflow runner"

    gpu_nodes=sorted(str(p) for p in Path("/dev").glob("nvidia[0-9]*"))
    torch_available=importlib.util.find_spec("torch") is not None
    torch_count=None
    torch_error=None
    torch_version=None
    if torch_available:
        try:
            import torch
            torch_version=str(torch.__version__)
            torch_count=int(torch.cuda.device_count())
        except (ImportError, RuntimeError, OSError) as e:
            torch_error=type(e).__name__ + ": " + str(e)[:300]

    status=determine_status(count,torch_count,gpu_nodes,smi is not None)
    result={
      "schema":"99llm_X1_P15_torchtune_resource_preflight_v1",
      "performed_at_utc":time_utc(),
      "case":task["instance_id"],
      "case_position_one_based":task["index_one_based"],
      "original_source_repo":task["original_repo_identifier"],
      "canonical_github_repo_at_audit":task["canonical_repo_current"],
      "original_source_base_sha":task["original_base_sha"],
      "source_frame_sha256":hashlib.sha256(FRAME.read_bytes()).hexdigest(),
      "preregistration_sha256":hashlib.sha256(PATH.read_bytes()).hexdigest(),
      "runner":os.environ.get("RUNNER_NAME","unreported"),
      "runner_os":os.environ.get("RUNNER_OS","unreported"),
      "github_repository":os.environ.get("GITHUB_REPOSITORY","unreported"),
      "github_actions_run_id":os.environ.get("GITHUB_RUN_ID","unreported"),
      "nvidia_smi_installed":bool(smi),
      "nvidia_smi_exit_code":code,
      "nvidia_smi_gpu_count":count,
      "nvidia_smi_visible_devices":smi_lines,
      "nvidia_smi_error":smi_error,
      "nvidia_device_nodes":gpu_nodes,
      "torch_importable":torch_available,
      "torch_version":torch_version,
      "torch_cuda_device_count":torch_count,
      "torch_gpu_detection_error":torch_error,
      "required_parallel_gpu_ranks_in_original_visible_repro":2,
      "resource_status_for_original_visible_two_gpu_repro":status,
      "full_8b_training_reproduction_executed":False,
      "torchtune_source_patch_generated":False,
      "hidden_benchmark_test_patch_seen":False,
      "independent_task_oracle_executed":False,
      "code_correctness_label":None,
      "model_agent_actor_independently_attested":False,
      "workflow_identity_proves_model_authorship":False,
      "denominator_note":"This is a task-resource feasibility record. Resource shortage is not a failed repair or a new benchmark task."
    }
    return result


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",required=True,type=Path)
    args=ap.parse_args()
    data=preflight()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(data,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf-8")
    print("P15_RESOURCE_PREFLIGHT_RECORD "+canonical(data).strip())
    print("P15_RESOURCE_STATE "+data["resource_status_for_original_visible_two_gpu_repro"])
    print("P15_HIDDEN_ORACLE_NOT_CALLED_OR_PATCH_CREATED")


if __name__=="__main__":
    main()
