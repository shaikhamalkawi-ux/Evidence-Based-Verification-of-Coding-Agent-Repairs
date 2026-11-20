"""P25 original task matched null-control attribution; never rescore P23 P9."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/"data/audits"

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

class P25OriginalNull(unittest.TestCase):
    def setUp(self):
        self.r=read(A/"P25_CFN_LINT_MATCHED_ORIGINAL_NULL_CONTROL_EXECUTED_20261120.json")
        self.p=read(A/"P23_CFN_LINT_ORIGINAL_TASK_ORACLE_20261120.json")
        self.design=read(ROOT/"protocol/P25_CFN_LINT_POSTREVEAL_BASELINE_NULL_CONTROL_20261120.json")
        self.prior=read(A/"P24_CFN_LINT_P23_ORIGINAL_FOUR_P2P_DIAGNOSTIC_20261120.json")

    def test_frozen_original_source_and_same_task(self):
        self.assertEqual(self.r["task"],self.design["original_frozen_case"])
        self.assertEqual(self.r["source_base_sha"],self.design["original_base_commit"])
        self.assertEqual(self.r["original_harness_run"],self.design["original_P23_ORACLE_run_id"])
        self.assertEqual(self.design["original_frozen_rank"],10)
        self.assertTrue(self.r["no_source_code_or_schema_change"])

    def test_first_original_p23_oracle_remains_unresolved(self):
        original=self.p["original_harness_task_observation"]
        self.assertIs(original["official_resolved"],False)
        self.assertEqual((original["f2p_passed"],original["f2p_total"],original["p2p_failed"]),(1,1,4))
        self.assertTrue(self.r["original_official_task_label_rewritten"] is False)
        self.assertTrue(self.r["original_P9_not_resealed"])

    def test_original_base_null_has_same_four_p2p_failures(self):
        r=self.r
        self.assertEqual(r["status"],"COMPLETE_POSTREVEAL_CONTROL")
        self.assertEqual(r["matched_reports"],1)
        self.assertEqual((r["f2p_passed"],r["f2p_total"]),(0,1))
        self.assertEqual((r["p2p_passed"],r["p2p_failed"]),(1227,4))
        self.assertEqual(r["tests_executed"],1232)
        self.assertIs(r["resolved"],False)
        ids=set(self.design["original_four_failing_P2P_tests"])
        self.assertEqual(set(r["matched_failure_overlap_ids"]),ids)
        self.assertEqual(set(self.prior["failing_p2p_test_ids"]),ids)
        self.assertEqual(r["control_only_failure_ids"],[])
        self.assertEqual(r["original_only_failure_ids"],[])
        self.assertTrue(r["p2p_failure_id_sets_identical"])

    def test_null_is_not_an_agent_repair_or_new_task(self):
        self.assertEqual(self.r["baseline_control_patch_type"],"README_MARKDOWN_COMMENT_ONLY")
        self.assertTrue(self.r["postreveal_only"])
        self.assertTrue(self.r["no_new_agent_or_original_blind_task"])
        self.assertFalse(self.r["code_task_full_success_claim"])
        self.assertTrue(self.r["source_patch_not_agent_attested"])
        self.assertTrue(self.design["no_change_to_P23_original_result"])

    def test_original_sample_frame_stays_ten(self):
        frozen=read(ROOT/"pilot/frozen_task_frame_20261117.json")
        self.assertEqual(frozen["n_selected"],10)
        self.assertEqual(frozen["selected"][9]["instance_id"],self.r["task"])
        self.assertEqual(frozen["dataset_revision_sha"],"babb27e45e072219195db7a744bbf0d3c1a36e56")

    def test_explicit_predeclared_limit_prevents_overclaim(self):
        limits=" ".join(self.design["claim_limits"]).lower()
        self.assertIn("not a new blind",limits)
        self.assertIn("official benchmark",limits)
        self.assertIn("not retroactively",limits)
        self.assertIn("no hidden grader",limits)


if __name__=="__main__":
    unittest.main()
