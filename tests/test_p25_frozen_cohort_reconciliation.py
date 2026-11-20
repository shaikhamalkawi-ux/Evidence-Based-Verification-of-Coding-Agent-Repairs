"""P25 ten frozen task evidence admission and non-vacuous decision denominator guards."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
def read(p):
    return json.loads((ROOT/p).read_text(encoding="utf-8"))


class TestP25FrozenFrameReconciliation(unittest.TestCase):
    def setUp(self):
        self.frame=read("pilot/frozen_task_frame_20261117.json")
        self.panel=read("data/audits/P25_TEN_FROZEN_TASKS_ENDPOINT_ADMISSION_RECONCILIATION_20261120.json")
        self.records=self.panel["rows"]

    def test_original_ten_all_present_exact_order_no_substitution(self):
        self.assertEqual(len(self.records),len(self.frame["selected"]))
        self.assertEqual(self.panel["sample_n_frozen"],10)
        self.assertEqual([r["task"] for r in self.records],[s["instance_id"] for s in self.frame["selected"]])
        self.assertEqual([r["original_selection_sha256"] for r in self.records],
                         [s["selection_sha256"] for s in self.frame["selected"]])

    def test_original_raw_task_outcome_counts_and_denominators(self):
        has_oracle=[r for r in self.records if r["raw_original_harness_run_id"] is not None]
        self.assertEqual(len(has_oracle),self.panel["raw_original_harness_executed_count"])
        self.assertEqual(len(has_oracle),9)
        self.assertEqual(sum(r["raw_original_resolved"] is True for r in has_oracle),2)
        self.assertEqual(sum(r["raw_original_resolved"] is False for r in has_oracle),7)
        self.assertEqual(self.panel["not_executed_original_harness_count"],1)
        self.assertEqual(self.panel["seven_task_descriptive_raw_harness_subset_count"],7)

    def test_privacyidea_import_failure_not_a_verified_false_accept(self):
        x=self.records[6]
        self.assertEqual(x["task"],"privacyidea__privacyidea-4251")
        self.assertEqual(x["underlying_code_correctness_admission"],"HOLD_SYSTEMIC_TEST_IMPORT_FAILURE")
        self.assertFalse(x["enter_seven_task_mixed_stage_raw_harness_descriptive_panel"])
        self.assertFalse(x["is_a_definitively_source_attributed_false_accept"])
        self.assertEqual(x["p9_original_preoracle"]["local_pass"],"ACCEPT")
        self.assertIs(x["raw_original_resolved"],False)

    def test_reflex_prepatch_and_no_independent_oracle(self):
        x=self.records[8]
        self.assertEqual(x["task"],"reflex-dev__reflex-4510")
        self.assertIsNone(x["raw_original_harness_run_id"])
        self.assertIsNone(x["raw_original_resolved"])
        self.assertEqual(x["underlying_code_correctness_admission"],"HOLD_SOURCE_DEPENDENCY_AND_REPRODUCTION")
        self.assertIsNone(x["p9_original_preoracle"]["local_pass"])

    def test_cfnlint_raw_unresolved_vs_baseline_shared_p2p(self):
        x=self.records[9]
        self.assertEqual(x["task"],"aws-cloudformation__cfn-lint-3779")
        self.assertEqual(x["issue_f2p"],"1/1")
        self.assertEqual(x["p2p_exact_matched_failure_overlap"],"4/4")
        self.assertEqual(x["reference_null_control_run_id"],44761416230)
        self.assertFalse(x["enter_seven_task_mixed_stage_raw_harness_descriptive_panel"])
        self.assertFalse(x["is_a_definitively_source_attributed_false_accept"])
        self.assertIs(x["raw_original_resolved"],False)
        self.assertEqual(x["p9_original_preoracle"]["local_pass"],"ACCEPT")

    def test_seven_task_panel_policy_values_are_explicitly_descriptive(self):
        subset=[r for r in self.records if r["enter_seven_task_mixed_stage_raw_harness_descriptive_panel"]]
        self.assertEqual(len(subset),7)
        policies=self.panel["seven_task_nonhomogeneous_policy_snapshot"]
        self.assertEqual(policies["self_report"]["accepted"],4)
        self.assertEqual(policies["self_report"]["accepted_raw_unresolved"],3)
        self.assertEqual(policies["local_pass"]["accepted"],6)
        self.assertEqual(policies["local_pass"]["accepted_raw_unresolved"],5)
        self.assertEqual(policies["source_linked"]["accepted"],0)
        self.assertIsNone(policies["source_linked"]["risk_among_accepted"])
        self.assertEqual(policies["source_linked"]["held_raw_resolved"],2)
        self.assertIn("not confirmed",self.panel["panel_label"])

    def test_postreveal_experiments_are_not_added_as_new_tasks(self):
        self.assertFalse(any("P25" in r["task"] for r in self.records))
        self.assertEqual(len({r["task"] for r in self.records}),10)
        self.assertTrue(any("not an eleventh" in s for s in self.panel["methodological_limits"]))
        self.assertTrue(any("no human coder" in s.lower() for s in self.panel["methodological_limits"]))


if __name__=="__main__":
    unittest.main()
