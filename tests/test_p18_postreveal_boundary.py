"""P18 source-level post-reveal-only guards; no new prospective task labels."""
import json
import hashlib
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

def read(p):
    return json.loads((ROOT/p).read_text(encoding="utf-8"))


class TestP18LiteralOnlyPostReveal(unittest.TestCase):
    def test_p17_original_task_outcome_is_immutable(self):
        p17=read("data/audits/P17_TORCHTUNE_ORIGINAL_ORACLE_20261120.json")
        r=p17["original_harness_task_result"]
        self.assertEqual((r["f2p_passed"],r["f2p_total"],r["p2p_failed"]),(0,1,0))
        self.assertFalse(r["official_resolved"])
        self.assertEqual(r["tests_executed"],651)
        self.assertEqual(r["head_sha"],"57f45fdd5552908d4b5d42cccd7359ccb4de2560")

    def test_source_ablation_is_post_reveal_only(self):
        p=read("protocol/P18_POSTREVEAL_LITERAL_SENSITIVITY_REGISTER_20261120.json")
        self.assertEqual(p["status"],"PREREGISTERED_POSTREVEAL_NOT_BLINDED")
        self.assertTrue(p["source_patch_untouched_at_registration"])
        self.assertEqual(p["original_P17_candidate_sha"],"57f45fdd5552908d4b5d42cccd7359ccb4de2560")
        self.assertEqual(p["observed_P17_runtime_error"],"DoRA magnitude norm is still on meta device")
        self.assertEqual(p["observed_expected_regex"],"Cannot initialize DoRA magnitude")
        self.assertEqual(p["old_literal"].replace("DoRA magnitude norm is still on meta device",
                                                  "Cannot initialize DoRA magnitude: computed norm is still on meta device"),
                         p["new_literal"])
        self.assertIn("no new algorithmic", str(p).lower())

    def test_original_f2p_failure_is_well_bounded_after_reveal(self):
        d=read("data/audits/P18_TORCHTUNE_POSTREVEAL_ERROR_TAXONOMY_20261120.json")
        self.assertEqual(d["study"],"POSTREVEAL_PUBLIC_SOURCE_DIAGNOSIS_NOT_BLIND")
        self.assertEqual(d["f2p_passed"],0)
        self.assertEqual(d["f2p_total"],1)
        self.assertEqual(d["p2p_failed"],0)
        self.assertEqual(d["failed_f2p_test_ids"],[
            "tests/torchtune/modules/peft/test_dora.py::TestDoRALinear::test_dora_meta_device_init_error"])
        self.assertFalse(d["original_resolved"])
        self.assertEqual(d["original_test_output_sha256"],
                         "864bb5edf03e1810a348ead57862d7a057c852df95bf56f33a4b9403f5ca1282")

    def test_original_P9_seal_unmodified_and_no_new_task(self):
        s=read("pilot/torchtune/sealed/P9_DECISION_SEAL.json")
        b=(ROOT/"pilot/torchtune/sealed/P9_DECISIONS_SEALED.jsonl").read_bytes()
        self.assertEqual(hashlib.sha256(b).hexdigest(),s["decisions_sha256"])
        self.assertEqual(s["decisions_sha256"],
                         "c62f5bffce085577ad1f5b0e4da05ec0a3a76b133e0eebd1f626bb4b2261ed35")
        r=read("pilot/torchtune/P18_POSTREVEAL_ORIGINAL_TASK_RETEST_REGISTER.json")
        self.assertTrue(r["no_new_P9_decisions"])
        self.assertTrue(r["original_six_task_population_denominator_unchanged"])
        self.assertTrue(r["text_diff_only"])
        self.assertTrue(r["original_GPU_training_unverified"])

    def test_no_human_or_qualifying_agent_claim_from_postreveal(self):
        r=read("pilot/torchtune/P18_POSTREVEAL_ORIGINAL_TASK_RETEST_REGISTER.json")
        self.assertEqual(r["status"],"PREREGISTERED_POSTREVEAL_ORACLE_RETEST_NOT_BLIND")
        self.assertTrue(r["no_new_candidate_agent_authentication"])
        self.assertEqual(r["new_P18_postreveal_candidate_sha"],
                         "6c029466df2fdca0b28273b58eaab46ef6460075")


if __name__ == "__main__":
    unittest.main()
