"""P18 one-literal post-reveal original task outcome and non-vacuity guards.

These are tests of archived original-harness receipts; they do not rerun the
original benchmark and do not make P18 an independent coding-agent trial.
"""
from __future__ import annotations
from copy import deepcopy
import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts/p18_verify_label_sensitivity.py"
spec=importlib.util.spec_from_file_location("p18_verify_label_sensitivity",SCRIPT)
checker=importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class P18OriginalOracleSensitivityTests(unittest.TestCase):
    def setUp(self):
        self.original=checker.read(checker.P18)

    def test_real_original_harness_flip_with_same_task(self):
        r=checker.validate()
        self.assertEqual(r["original_P17_F2P"],"0/1")
        self.assertEqual(r["exposed_P18_F2P"],"1/1")
        self.assertEqual(r["P2P_failures_both"],0)
        self.assertEqual(r["original_evaluator_tests_executed_each"],651)

    def test_not_a_seventh_original_blinded_task(self):
        r=checker.validate()
        self.assertEqual(r["original_task_count_added_by_P18"],0)
        self.assertFalse(r["original_blinded_six_task_panel_changed"])
        self.assertFalse(r["new_blinded_coding_agent_efficacy_estimate"])
        self.assertFalse(r["full_two_GPU_DoRA_training_verified"])
        self.assertFalse(r["original_P17_P9_decisions_changed"])

    def test_changing_p17_original_failure_is_detected(self):
        x=deepcopy(self.original)
        x["first_initial_candidate"]["f2p_passed"]=1
        with self.assertRaises(AssertionError):
            checker.validate(x)

    def test_ignoring_hidden_label_revelation_is_detected(self):
        x=deepcopy(self.original)
        x["exposed_single_literal_variant"]["stage"]="PREREGISTERED_BLIND"
        with self.assertRaises(AssertionError):
            checker.validate(x)

    def test_claiming_actual_two_gpu_training_detected(self):
        x=deepcopy(self.original)
        x["exposed_single_literal_variant"]["full_two_GPU_DORA_training_reproduced"]=True
        with self.assertRaises(AssertionError):
            checker.validate(x)

    def test_wrong_sha_or_different_dataset_detected(self):
        x=deepcopy(self.original)
        x["exposed_single_literal_variant"]["candidate_sha"]="a"*40
        with self.assertRaises(AssertionError):
            checker.validate(x)
        y=deepcopy(self.original)
        y["exposed_single_literal_variant"]["dataset_rev"]="wrongrev"
        with self.assertRaises(AssertionError):
            checker.validate(y)

    def test_inflated_population_denominator_detected(self):
        x=deepcopy(self.original)
        x["score_label_interpretation"]["change_in_task_count_for_original_frozen_cohort"]=1
        with self.assertRaises(AssertionError):
            checker.validate(x)

    def test_actor_attribution_or_P9_redecision_rejected(self):
        x=deepcopy(self.original)
        x["exposed_single_literal_variant"]["human_feedback_or_authentic_agent_attestation"]=True
        with self.assertRaises(AssertionError):
            checker.validate(x)
        y=deepcopy(self.original)
        y["exposed_single_literal_variant"]["agent_policy_decision_rescored"]=True
        with self.assertRaises(AssertionError):
            checker.validate(y)


if __name__=="__main__":
    unittest.main()
