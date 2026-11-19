"""P15 preflight negative controls. Synthetic hardware cases, no GPU repair claims."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("p15_preflight",ROOT/"scripts/p15_preflight.py")
p15=importlib.util.module_from_spec(spec)
spec.loader.exec_module(p15)


class P15ResourceGateTests(unittest.TestCase):
    def test_missing_gpu_tools_classified_resource_hold_not_repair_failure(self):
        self.assertEqual(p15.determine_status(None,None,[],False),
                         "RESOURCE_HOLD_FULL_TWO_GPU_REPRO")

    def test_one_gpu_insufficient_for_original_two_ranks(self):
        self.assertEqual(p15.determine_status(1,1,["/dev/nvidia0"],True),
                         "RESOURCE_HOLD_FULL_TWO_GPU_REPRO")
        self.assertEqual(p15.determine_status(1,0,[],True),
                         "RESOURCE_HOLD_FULL_TWO_GPU_REPRO")

    def test_observed_two_gpus_only_a_hardware_flag_not_task_success(self):
        self.assertEqual(p15.determine_status(2,2,["/dev/nvidia0","/dev/nvidia1"],True),
                         "TWO_GPU_HARDWARE_OBSERVED_NOT_FULL_TASK_ADMISSION")

    def test_ambiguous_device_evidence_preserves_original_task(self):
        self.assertEqual(p15.determine_status(None,None,["/dev/nvidia0"],False),
                         "UNKNOWN_GPU_ACCESS_PRESERVE_TASK")

    def test_unexpected_device_node_rejected(self):
        with self.assertRaises(ValueError):
            p15.determine_status(None,None,["/tmp/fake_gpu"],False)

    def test_exact_original_frozen_case(self):
        reg=json.loads(p15.PATH.read_text(encoding="utf-8"))
        frame=json.loads(p15.FRAME.read_text(encoding="utf-8"))
        case=reg["next_frozen_case"]
        self.assertEqual(frame["selected"][case["index_one_based"]-1]["instance_id"],
                         "pytorch__torchtune-2139")
        self.assertEqual(case["original_base_sha"],"f2bd4bc25b24587aef40f486087412b9da8f1d94")
        self.assertEqual(case["original_repo_identifier"],"pytorch/torchtune")
        self.assertEqual(case["canonical_repo_current"],"meta-pytorch/torchtune")
        self.assertEqual(case["github_stable_repository_id"],"707869465")
        self.assertFalse(reg["experimental_gates"]["gate_C_coding_attempt"]["no_candidate_written_in_P15"] is False)

    def test_original_p9_and_oracle_are_untouched(self):
        reg=json.loads(p15.PATH.read_text(encoding="utf-8"))
        self.assertEqual(reg["policy_lock"]["P9_version"],"X1-P9-alpha-1-20261116")
        self.assertEqual(reg["experimental_gates"]["gate_D_independent_original_oracle"]["result"],"pending")
        self.assertTrue(reg["experimental_gates"]["gate_C_coding_attempt"]["no_candidate_written_in_P15"])
        self.assertIn("UNKNOWN / HOLD", reg["experimental_gates"]["gate_D_independent_original_oracle"]["zero_tests_or_infra_error"])


if __name__=="__main__":
    unittest.main()
