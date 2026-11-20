"""P21 source-bound endpoint QC negative controls (no original task patch)."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("p21_qc",ROOT/"scripts/p21_original_endpoint_qc.py")
p21=importlib.util.module_from_spec(spec)
spec.loader.exec_module(p21)
ORIGINAL=ROOT/"data/audits/P20_PRIVACYIDEA_ORIGINAL_HARNESS_RAW_WITH_QC_HOLD_20261120.json"
DIAGNOSTIC=ROOT/"data/audits/P21_PRIVACYIDEA_ORIGINAL_ORACLE_ENDPOINT_QC_CAUSE_20261120.json"


class TestP21EndpointIntegrity(unittest.TestCase):
    def setUp(self):
        self.original=json.loads(ORIGINAL.read_text())
        self.diagnostic=json.loads(DIAGNOSTIC.read_text())

    def test_import_failure_excludes_original_source_truth_without_deleting_raw_label(self):
        d=p21.decide(self.original,self.diagnostic)
        self.assertEqual(d["endpoint_admission_for_code_correctness"],
                         "HOLD_SYSTEMIC_TEST_IMPORT_FAILURE")
        self.assertIsNone(d["code_correctness_verified"])
        self.assertEqual((d["reported_f2p_passed"],d["reported_f2p_total"]),(0,1))
        self.assertEqual(d["reported_p2p_failed"],2022)
        self.assertEqual(d["reported_tests"],2023)
        self.assertEqual(d["original_harness_report_status"],"COMPLETE_RAW_UNRESOLVED")

    def test_original_p9_decisions_remain_immutable(self):
        d=p21.decide(self.original,self.diagnostic)
        self.assertEqual(d["original_p9_policy_decisions"],
                         {"self_report":"HOLD","local_pass":"ACCEPT","source_linked":"HOLD"})
        self.assertEqual(d["original_p9_seal_sha256"],
                         "33edbd2833c0730d6fa280a42f2cd05fe6deb754dce8c29764be5d40786f3f3d")
        self.assertFalse(d["original_report_overwritten"])
        self.assertTrue(d["postreveal_quality_control_only"])
        self.assertTrue(d["no_new_agent_or_task"])

    def test_missing_import_trace_is_present(self):
        self.assertIn("swe100_fixture_clock",self.diagnostic["missing_import_module_names"])
        self.assertEqual(self.diagnostic["original_test_output_sha256"],
                         "8fe0b9bfaccd2cc607abdc8cfbb7cf81d85d60aabb5664389e86c5c7e686efcb")
        self.assertEqual(self.diagnostic["raw_test_log_lines"],56)

    def test_mismatched_test_log_hash_rejected(self):
        changed=copy.deepcopy(self.diagnostic)
        changed["original_test_output_sha256"]="0"*64
        with self.assertRaises(ValueError):p21.decide(self.original,changed)

    def test_source_task_substitution_rejected(self):
        changed=copy.deepcopy(self.original)
        changed["task"]="some-other-task"
        with self.assertRaises(ValueError):p21.decide(changed,self.diagnostic)

    def test_fake_unique_behavioural_regression_count_rejected(self):
        changed=copy.deepcopy(self.original)
        changed["received_original_report"]["p2p_failed"]=2000
        with self.assertRaises(ValueError):p21.decide(changed,self.diagnostic)

    def test_missing_fixture_nonexistence_never_becomes_proven_success(self):
        changed=copy.deepcopy(self.diagnostic)
        changed["missing_import_module_names"]=[]
        d=p21.decide(self.original,changed)
        self.assertIsNone(d["code_correctness_verified"])
        self.assertEqual(d["endpoint_admission_for_code_correctness"],"HOLD_OTHER_UNADJUDICATED")


if __name__=="__main__":
    unittest.main()
