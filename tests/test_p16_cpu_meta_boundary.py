"""P16 observed PyTorch CPU-only meta-parameter semantics and scope guards.

These tests check a saved observed GitHub Actions CPU micro-probe, not the
original torchtune distributed source, SWE-bench-Live task, or agent repair.
"""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "data/audits/P16_CPU_META_MAGNITUDE_OBSERVED_20261120.json"
BOUNDARY = ROOT / "protocol/P16_CPU_META_SEMANTICS_BOUNDARIES_20261120.json"


class TestP16CPUProbe(unittest.TestCase):
    def setUp(self):
        self.r = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        self.p = json.loads(BOUNDARY.read_text(encoding="utf-8"))

    def test_original_frozen_torchtune_source_and_copy_semantics(self):
        self.assertEqual(self.r["source_task"], "pytorch__torchtune-2139")
        self.assertEqual(self.r["source_base_sha"], self.p["source_task"]["base_sha"])
        self.assertEqual(self.r["historical_dora_blob_sha"], self.p["source_task"]["dora_git_blob_sha"])
        self.assertEqual(self.r["historical_visible_operation"], "self.magnitude.copy_(weight_norm)")
        self.assertTrue(self.r["toy_originally_meta"])
        self.assertTrue(self.r["toy_still_meta_after_copy"])
        self.assertEqual(self.r["toy_device_after_copy"], "meta")
        self.assertIsNone(self.r["toy_copy_into_meta_raised"])

    def test_explicit_cpu_materialization_toy_only(self):
        self.assertTrue(self.r["test_copy_preserves_meta_storage_without_materialization"])
        self.assertTrue(self.r["test_explicit_materialization_then_copy"])
        self.assertEqual(self.r["tests_declared"], self.r["tests_passed"])
        self.assertEqual(self.r["tests_declared"], 2)
        self.assertEqual(self.r["toy_explicitly_materialized_to_cpu"], "cpu")
        self.assertFalse(self.r["toy_is_meta_after_materialization"])
        self.assertEqual(self.r["toy_values_after_materialization_and_copy"], [2.0, 3.0, 4.0])

    def test_never_impute_toy_success_as_real_issue_resolution(self):
        for key in (
            "original_torchtune_do_r_a_class_imported",
            "original_distributed_lora_recipe_executed",
            "two_gpu_training_reproduced",
            "training_model_8b_loaded",
            "original_independent_task_oracle_executed",
            "source_candidate_patch_generated",
            "source_linked_agent_authorship_attested",
            "code_repair_success_claim",
        ):
            self.assertIs(self.r[key], False, key)
        self.assertEqual(self.r["label"], "MECHANISM_CANDIDATE_NOT_ROOT_CAUSE_PROOF")
        self.assertEqual(self.r["status"], "COMPLETE_ISOLATED_CPU_SEMANTICS_ONLY")

    def test_authenticated_run_provenance_is_not_model_actor_attestation(self):
        source = self.r["provenance"]
        self.assertEqual(source["github_actions_run_id"], 44607950785)
        self.assertEqual(source["github_actions_job_id"], 135856570141)
        self.assertTrue(source["github_actions_url"].endswith("/44607950785"))
        self.assertEqual(self.r["cuda_devices_visible_in_this_cpu_microprobe"], 0)
        self.assertTrue(self.p["no_oracle_use"])
        self.assertTrue(self.p["no_source_patch_submitted"])
        self.assertTrue(self.p["not_task_success"])


if __name__ == "__main__":
    unittest.main()
