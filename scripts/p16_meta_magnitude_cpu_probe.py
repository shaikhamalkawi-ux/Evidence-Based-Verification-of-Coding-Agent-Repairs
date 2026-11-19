#!/usr/bin/env python3
"""99llm-X1 P16: isolated, executable PyTorch meta-device magnitude probe.

Exploratory CPU micro-test, not an original torchtune source execution, GPU
distributed training, or a hidden SWE-bench-Live repair oracle. Original DoRA
source at frozen base uses self.magnitude.copy_(weight_norm) within its
initialize_dora_magnitude method. This test isolates ONLY that PyTorch
parameter operation, without rewriting torchtune or pretending it fixes FSDP.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

SOURCE_BASE_SHA = "f2bd4bc25b24587aef40f486087412b9da8f1d94"
SOURCE_DORA_GIT_BLOB_SHA = "6f097da6d039738c320e8775ad61950c56fe0108"
SOURCE_RECIPE_GIT_BLOB_SHA = "e95fbb40c60c0d7f18e694aeb8dabac5a70e664b"


def run():
    import torch
    from torch import nn

    class MinimalMetaMagnitude(nn.Module):
        def __init__(self):
            super().__init__()
            # Isolate the specific meta-initialization used by the historical
            # distributed recipe; NOT a production DoRALinear instance.
            self.magnitude = nn.Parameter(torch.empty(3, device="meta"))

        @torch.no_grad()
        def initialize_dora_magnitude(self, weight_norm):
            # The same operation visible in the historical DoRA source.
            self.magnitude.copy_(weight_norm)

    probe = MinimalMetaMagnitude()
    initial_meta = bool(probe.magnitude.is_meta)
    cpu_norm = torch.tensor([2.0, 3.0, 4.0], dtype=torch.float32, device="cpu")
    copy_error = None
    try:
        probe.initialize_dora_magnitude(cpu_norm)
    except (RuntimeError, NotImplementedError, TypeError) as exc:
        copy_error = type(exc).__name__ + ": " + str(exc)[:300]
    meta_after_copy = bool(probe.magnitude.is_meta)
    device_after_copy = str(probe.magnitude.device)

    # Compare only a toy *explicitly materialized* 3-element parameter.
    # Production sharded parameters cannot be inferred from this simple test.
    probe.to_empty(device="cpu")
    probe.initialize_dora_magnitude(cpu_norm)
    final_meta = bool(probe.magnitude.is_meta)
    final_device = str(probe.magnitude.device)
    final_values = [float(x) for x in probe.magnitude.detach().tolist()]
    test_1 = initial_meta and meta_after_copy and copy_error is None
    test_2 = not final_meta and final_device == "cpu" and final_values == [2.0, 3.0, 4.0]

    record = {
        "schema": "99llm_X1_P16_meta_copy_cpu_microprobe_v1",
        "status": "COMPLETE_ISOLATED_CPU_SEMANTICS_ONLY" if test_1 and test_2 else "HOLD_UNEXPECTED_CPU_SEMANTICS",
        "recorded_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source_task": "pytorch__torchtune-2139",
        "source_repo": "meta-pytorch/torchtune",
        "source_base_sha": SOURCE_BASE_SHA,
        "historical_dora_blob_sha": SOURCE_DORA_GIT_BLOB_SHA,
        "historical_recipe_blob_sha": SOURCE_RECIPE_GIT_BLOB_SHA,
        "historical_visible_operation": "self.magnitude.copy_(weight_norm)",
        "torch_version": str(torch.__version__),
        "platform": platform.platform(),
        "cuda_devices_visible_in_this_cpu_microprobe": int(torch.cuda.device_count()),
        "toy_magnitude_elements": 3,
        "toy_expected_cpu_values": [2.0, 3.0, 4.0],
        "toy_originally_meta": initial_meta,
        "toy_copy_into_meta_raised": copy_error,
        "toy_still_meta_after_copy": meta_after_copy,
        "toy_device_after_copy": device_after_copy,
        "toy_explicitly_materialized_to_cpu": final_device,
        "toy_is_meta_after_materialization": final_meta,
        "toy_values_after_materialization_and_copy": final_values,
        "test_copy_preserves_meta_storage_without_materialization": test_1,
        "test_explicit_materialization_then_copy": test_2,
        "tests_passed": int(test_1) + int(test_2),
        "tests_declared": 2,
        "original_torchtune_do_r_a_class_imported": False,
        "original_distributed_lora_recipe_executed": False,
        "two_gpu_training_reproduced": False,
        "training_model_8b_loaded": False,
        "original_independent_task_oracle_executed": False,
        "source_candidate_patch_generated": False,
        "source_linked_agent_authorship_attested": False,
        "code_repair_success_claim": False,
        "label": "MECHANISM_CANDIDATE_NOT_ROOT_CAUSE_PROOF",
        "scientific_scope": "Only copy_ and to_empty behavior on an isolated toy meta Parameter; original FSDP/DTensor and full DoRA module not tested.",
    }
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    out = run()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("P16_CPU_META_MICROPROBE " + json.dumps(out, sort_keys=True))
    if out["tests_passed"] != out["tests_declared"]:
        raise SystemExit("HOLD: observed PyTorch meta semantics contradict the toy probe expectations")


if __name__ == "__main__":
    main()
