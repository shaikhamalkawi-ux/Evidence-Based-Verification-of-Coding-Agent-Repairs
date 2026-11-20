"""P26 sharp finite-frame partial-identification and tamper controls."""
from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("p26",ROOT/"scripts/p26_identified_acceptance_bounds.py")
p26=importlib.util.module_from_spec(spec)
spec.loader.exec_module(p26)


class TestP26EndpointIdentifiedBounds(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=p26.compute()

    def test_exact_original_task_frame_and_order(self):
        d=self.result
        frame=p26.load(ROOT,p26.FRAME)
        self.assertEqual(d["selected_original_task_count"],10)
        self.assertEqual([r["task"] for r in d["task_records"]],
                         [r["instance_id"] for r in frame["selected"]])
        self.assertEqual(d["attempted_original_task_candidate_count"],9)
        self.assertEqual(d["no_candidate_original_task_count"],1)
        self.assertEqual((d["raw_original_resolved_count"],d["raw_original_unresolved_count"]),(2,7))

    def test_issue_f2p_truth_and_endpoint_unknown_partition(self):
        d=self.result
        self.assertEqual(d["endpoint_admitted_issue_specific_F2P_fail_count"],4)
        self.assertEqual(d["endpoint_admitted_original_task_pass_count"],2)
        self.assertEqual(d["endpoint_unknown_with_candidate_count"],3)
        self.assertEqual(set(r["task"] for r in d["task_records"] if r["endpoint_class"]==p26.FAIL),
                         {"pdm-project__pdm-3419","matplotlib__matplotlib-28933",
                          "pytorch__torchtune-2139","stanfordnlp__dspy-1609"})

    def test_local_pass_exact_sharp_risk_range(self):
        x=self.result["policies"]["local_pass"]
        self.assertEqual(x["accept_count"],8)
        self.assertEqual(x["attempted_decision_denominator"],9)
        self.assertEqual((x["accepted_direct_F2P_fail"],x["accepted_original_task_pass"],
                          x["accepted_endpoint_or_attribution_unknown"]),(4,1,3))
        self.assertEqual(x["false_accept_count_identified_interval"],[4,7])
        self.assertEqual(x["false_accept_risk_sharp_exact_bounds"],["1/2","7/8"])
        self.assertEqual(x["false_accept_risk_sharp_decimal_bounds"],[0.5,0.875])

    def test_self_report_exact_sharp_risk_range(self):
        x=self.result["policies"]["self_report"]
        self.assertEqual(x["accept_count"],5)
        self.assertEqual((x["accepted_direct_F2P_fail"],x["accepted_original_task_pass"],
                          x["accepted_endpoint_or_attribution_unknown"]),(2,1,2))
        self.assertEqual(x["false_accept_count_identified_interval"],[2,4])
        self.assertEqual(x["false_accept_risk_sharp_exact_bounds"],["2/5","4/5"])

    def test_source_linked_zero_accept_is_not_perfect_precision(self):
        x=self.result["policies"]["source_linked"]
        self.assertEqual(x["accept_count"],0)
        self.assertIsNone(x["false_accept_risk_sharp_exact_bounds"])
        self.assertIsNone(x["false_accept_risk_sharp_decimal_bounds"])
        self.assertFalse(x["risk_defined"])
        self.assertEqual(x["guaranteed_passing_tasks_held"],2)
        self.assertTrue(self.result["source_linked_zero_accept_risk_is_undefined"])

    def test_unknown_codes_preserve_missingness_mechanism(self):
        rows={r["task"]:r for r in self.result["task_records"]}
        self.assertEqual(rows["kedro-org__kedro-4406"]["endpoint_class"],"UNKNOWN_UNATTRIBUTED_P2P")
        self.assertEqual(rows["privacyidea__privacyidea-4251"]["endpoint_class"],"UNKNOWN_INVALID_IMPORT_ENDPOINT")
        self.assertEqual(rows["aws-cloudformation__cfn-lint-3779"]["endpoint_class"],"UNKNOWN_BASELINE_MATCHED_P2P")
        self.assertEqual(rows["reflex-dev__reflex-4510"]["endpoint_class"],p26.NO_CANDIDATE)
        self.assertEqual(rows["reflex-dev__reflex-4510"]["p9_decisions"],
                         {q:None for q in p26.POLICIES})

    def test_original_policy_is_not_retrained_or_gated_on_hidden_status(self):
        d=self.result
        self.assertTrue(d["original_policy_unchanged"])
        self.assertTrue(d["original_task_outcomes_unchanged"])
        self.assertFalse(d["policies"]["local_pass"]["confidence_interval_applicable"])
        self.assertTrue(any("mixed" in x.lower() or "matplotlib" in x.lower()
                            for x in d["denominator_and_homogeneity_limits"]))
        self.assertTrue(any("MR30" in x for x in d["denominator_and_homogeneity_limits"]))

    def test_bad_matched_null_control_cannot_shrink_unknown_set(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for f in [p26.FRAME,p26.P19,p26.P25,p26.P20,p26.P21,p26.P23,p26.P25NULL,p26.PROTOCOL]:
                dst=root/f
                dst.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(ROOT/f,dst)
            null_file=root/p26.P25NULL
            d=json.loads(null_file.read_text())
            d["matched_failure_overlap_ids"]=d["matched_failure_overlap_ids"][:3]
            null_file.write_text(json.dumps(d)+"\n")
            with self.assertRaises(AssertionError):
                p26.compute(root)

    def test_task_substitution_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for f in [p26.FRAME,p26.P19,p26.P25,p26.P20,p26.P21,p26.P23,p26.P25NULL,p26.PROTOCOL]:
                dst=root/f
                dst.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(ROOT/f,dst)
            path=root/p26.FRAME
            d=json.loads(path.read_text())
            d["selected"][9]["instance_id"]="test-source-substitution"
            path.write_text(json.dumps(d)+"\n")
            with self.assertRaises(AssertionError):
                p26.compute(root)


if __name__=="__main__":
    unittest.main()
