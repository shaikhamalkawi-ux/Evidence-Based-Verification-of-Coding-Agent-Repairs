"""P19 MR31 editorial matrix deterministic source and publication-claim tests.

No hidden oracle is run. Observations are fixed source P17 and P18 results,
with the exposed P18 literal-only label flip intentionally excluded from the
original independent six-task denominator.
"""
from __future__ import annotations
import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
S=ROOT/"scripts/p19_mr31_synthesize.py"
spec=importlib.util.spec_from_file_location("p19_mr31_synthesize",S)
p19=importlib.util.module_from_spec(spec)
spec.loader.exec_module(p19)


class P19EvidenceSynthesisTests(unittest.TestCase):
    def setUp(self):
        self.r=p19.synthesize()

    def test_original_six_tasks_and_four_holds_unchanged(self):
        self.assertEqual(self.r["original_fixed_task_frame"],10)
        self.assertEqual(self.r["original_distinct_tasks_with_valid_independent_oracle"],6)
        self.assertEqual(self.r["original_distinct_tasks_not_yet_evaluated"],4)
        self.assertEqual(self.r["original_resolved_task_count"],2)
        self.assertEqual(self.r["original_unresolved_task_count"],4)
        self.assertEqual(len({x["task_id"] for x in self.r["original_task_rows"]}),6)
        self.assertEqual([x["task_index_in_original_frame_one_based"] for x in self.r["original_task_rows"]],[1,2,3,4,5,8])

    def test_original_F2P_P2P_classification_exact(self):
        self.assertEqual(self.r["failure_mode_count_table"],{
            "ORIGINAL_HARNESS_RESOLVED":2,
            "F2P_PASSED_P2P_REGRESSION":1,
            "F2P_FAILED_P2P_REGRESSION":1,
            "F2P_FAILED_NO_RECORDED_P2P_REGRESSION":2,
        })
        byid={r["task_id"]:r for r in self.r["original_task_rows"]}
        self.assertEqual(byid["kedro-org__kedro-4406"]["original_outcome_class"],"F2P_PASSED_P2P_REGRESSION")
        self.assertEqual(byid["pdm-project__pdm-3419"]["original_outcome_class"],"F2P_FAILED_P2P_REGRESSION")
        self.assertEqual(byid["python-babel__babel-1163"]["original_outcome_class"],"ORIGINAL_HARNESS_RESOLVED")
        self.assertEqual(byid["joke2k__faker-2155"]["original_outcome_class"],"ORIGINAL_HARNESS_RESOLVED")

    def test_source_linked_policy_all_hold_is_not_perfect_risk(self):
        risk=self.r["frozen_decision_risk_coverage_descriptive"]
        self.assertEqual(risk["source_linked"]["accepted_task_count"],0)
        self.assertEqual(risk["source_linked"]["unnecessary_hold_count"],2)
        self.assertFalse(risk["source_linked"]["risk_among_accepted_defined"])
        self.assertIsNone(risk["source_linked"]["false_accept_risk_among_accepted"])
        self.assertIsNone(self.r["vacuous_zero_accept_policy_risk"])

    def test_self_report_and_local_acceptance_tradeoff(self):
        risk=self.r["frozen_decision_risk_coverage_descriptive"]
        self.assertEqual((risk["self_report"]["accepted_task_count"],risk["self_report"]["false_accept_count"]),(4,3))
        self.assertEqual((risk["local_pass"]["accepted_task_count"],risk["local_pass"]["false_accept_count"]),(5,4))
        self.assertEqual(risk["self_report"]["correct_accept_count"],1)
        self.assertEqual(risk["local_pass"]["correct_accept_count"],1)
        self.assertEqual(risk["local_pass"]["unnecessary_hold_count"],1)

    def test_p18_label_flip_is_overlay_not_7th_blinded_success(self):
        self.assertTrue(self.r["p18_postreveal_literal_flip_present_as_overlay_not_extra_task"])
        self.assertEqual(self.r["P18_new_original_blinded_task_count"],0)
        rows=[x for x in self.r["original_task_rows"] if x["task_id"]=="pytorch__torchtune-2139"]
        self.assertEqual(len(rows),1)
        x=rows[0]
        self.assertFalse(x["original_harness_task_resolved"])
        self.assertEqual((x["original_f2p_passed"],x["original_f2p_total"]),(0,1))
        overlay=x["postreveal_sensitivity_overlay"]
        self.assertTrue(overlay["excluded_from_original_task_result"])
        self.assertEqual(overlay["original_f2p"],"0/1")
        self.assertEqual(overlay["postreveal_f2p"],"1/1")
        self.assertTrue(overlay["hidden_assertion_was_known_before_variant"])
        self.assertTrue(overlay["same_original_harness_tests_executed"])
        self.assertTrue(overlay["does_not_certify_two_gpu_training"])

    def test_wrong_task_oracle_labels_rejected(self):
        bad={"f2p_passed":1,"f2p_total":1,"p2p_failed":0,"truth":False}
        with self.assertRaises(ValueError):
            p19.classify(bad)
        with self.assertRaises(ValueError):
            p19.classify({"f2p_passed":0,"f2p_total":0,"p2p_failed":0,"truth":False})

    def test_no_human_coder_no_agent_author_authentication_claimed(self):
        self.assertFalse(self.r["human_second_coder_present"])
        self.assertFalse(self.r["actor_authentication_verified_for_benchmark_rows"])
        self.assertIn("Mixed-stage",self.r["comparability_limit"])
        self.assertEqual(self.r["status"],"EDITORIAL_SYNTHESIS_ONLY_NO_NEW_ORIGINAL_TASK_RESULTS")


if __name__=="__main__":
    unittest.main()
