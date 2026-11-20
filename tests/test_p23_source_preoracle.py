"""P23 frozen source/CLI/preoracle original P9 provenance conformance.

These are software/source-record checks only, NOT an independent cfn-lint
benchmark oracle and NOT independent agent-authorship attestation.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"pilot/cfnlint"
AUD=ROOT/"data/audits"


def read(p):
    return json.loads(Path(p).read_text(encoding="utf8"))


class TestP23SourceAndSeal(unittest.TestCase):
    def test_original_tenth_task_exact_unsubstituted(self):
        frame=read(ROOT/"pilot/frozen_task_frame_20261117.json")
        r=read(ROOT/"protocol/P23_CFN_LINT_ORIGINAL_TENTH_TASK_REGISTER_20261120.json")
        self.assertEqual(len(frame["selected"]),10)
        self.assertEqual(frame["selected"][9]["instance_id"],r["task"])
        self.assertEqual(frame["selected"][9]["repo"],"aws-cloudformation/cfn-lint")
        self.assertEqual(r["historical_source_sha"],"de28d1e43777e3782a06b74d9091c3471636eb70")
        self.assertTrue(r["no_test_patch_or_gold_access"])

    def test_frozen_schema_cases_and_no_weakening_of_invalid_controls(self):
        cases=read(P/"P23_FROZEN_VISIBLE_IAM_CASES_20261120.json")
        self.assertEqual(cases["case_count"],64)
        self.assertEqual(cases["valid_count"],45)
        self.assertEqual(cases["invalid_count"],19)
        self.assertEqual(len({c["case_id"] for c in cases["cases"]}),64)
        self.assertEqual(sum(c["expected_valid"] for c in cases["cases"]),45)
        self.assertEqual(cases["original_policy_schema_blob"],"99f30247c838aea3910f891a54c9bbad1d67c88a")
        self.assertTrue(cases["prepatch_frozen"])

    def test_first_candidate_36_to_61_and_same_source_cases(self):
        d=read(AUD/"P23_ORIGINAL_AND_FIRST_IAM_SOURCE_VISIBLE_20261120.json")
        self.assertEqual(d["base"]["classification_passed"],36)
        self.assertEqual(d["base"]["classification_failed"],28)
        self.assertEqual(d["first_candidate"]["classification_passed"],61)
        self.assertEqual(d["first_candidate"]["classification_failed"],3)
        self.assertEqual(d["base"]["frozen_case_sha256"],d["first_candidate"]["frozen_case_sha256"])
        self.assertEqual(d["first_candidate_git_sha"],"7ce6016f638058b44f471fee575a3b298c84b369")
        self.assertTrue(d["original_hidden_oracle_not_accessed"])

    def test_second_source_64_and_all_invalid_rejected(self):
        d=read(AUD/"P23_SECOND_SOURCE_FIXED_64_CASES_20261120.json")
        self.assertEqual(d["second_candidate"]["classification_passed"],64)
        self.assertEqual(d["second_candidate"]["classification_failed"],0)
        self.assertEqual(d["second_candidate_sha"],"a1bd25e330d96cf450a44809fecd060d795e24ab")
        self.assertEqual(d["second_candidate_schema_blob"],"bbf877cd6815856f8714537465123ed5551b8e79")
        self.assertTrue(d["negative_controls_19_of_19_rejected"])
        self.assertTrue(d["second_patch_only_three_date_patterns"]["all_other_original_fields_equal"])

    def test_extra_cli_cases_after_patch_before_hidden_are_not_independent(self):
        d=read(AUD/"P23_ORIGINAL_AND_FIXED_CFN_LINT_CLI_E3510_20261120.json")
        self.assertEqual(d["original_cli"]["matching_expectation"],4)
        self.assertEqual(d["final_cli"]["matching_expectation"],9)
        self.assertEqual(d["final_cli"]["n_cases"],9)
        self.assertEqual(d["final_cli"]["valid_expected_e3510_absent"],6)
        self.assertEqual(d["final_cli"]["invalid_expected_e3510_present"],3)
        self.assertEqual(d["original_cli"]["cli_case_sha256"],d["final_cli"]["cli_case_sha256"])
        self.assertTrue(d["original_hidden_task_oracle_unseen"])
        self.assertFalse(d["signed_actor_proof_absent"] is False)

    def test_original_P9_byte_hashes_and_temporal_order(self):
        i=(P/"sealed/P23_DECISION_INPUT.jsonl").read_bytes()
        d=(P/"sealed/P9_DECISIONS_SEALED.jsonl").read_bytes()
        seal=read(P/"sealed/P9_DECISION_SEAL.json")
        reg=read(P/"P23_PREORACLE_ORIGINAL_TASK_EVALUATION_REGISTER_20261120.json")
        self.assertEqual(hashlib.sha256(i).hexdigest(),seal["input_sha256"])
        self.assertEqual(hashlib.sha256(d).hexdigest(),seal["decisions_sha256"])
        self.assertEqual(hashlib.sha256((ROOT/"scripts/p9_decide.py").read_bytes()).hexdigest(),seal["script_sha256"])
        self.assertEqual(seal["decisions_sha256"],reg["original_P9_decision_sha256"])
        self.assertEqual(seal["input_sha256"],reg["original_P9_input_sha256"])
        self.assertEqual(seal["script_sha256"],reg["original_P9_script_sha256"])
        dec=json.loads(d)
        inp=json.loads(i)
        self.assertEqual(dec["t_decision"],"2026-11-20T12:43:48Z")
        self.assertEqual(dec["t_decision"],inp["t_decision"])
        self.assertTrue(all(x["completed_at"]<dec["t_decision"] for x in inp["receipts"]))
        self.assertEqual(dec["head_sha"],reg["candidate_source_sha"])

    def test_original_P9_does_not_assert_authenticated_agent(self):
        dec=read(P/"sealed/P9_DECISIONS_SEALED.jsonl")
        inp=read(P/"sealed/P23_DECISION_INPUT.jsonl")
        self.assertEqual(dec["decisions"],{"self_report":"ACCEPT","local_pass":"ACCEPT","source_linked":"HOLD"})
        self.assertTrue(inp["agent_claimed_fixed"])
        self.assertFalse(inp["target_agent_is_commit_author"])
        self.assertTrue(inp["source_notes"]["full_600_line_user_example_not_executed"])
        self.assertTrue(inp["source_notes"]["additional_cli_tests_designed_after_second_candidate_before_execution"])

    def test_original_heldout_test_unseen_when_source_decision_frozen(self):
        inp=read(P/"sealed/P23_DECISION_INPUT.jsonl")
        self.assertEqual(inp["source_notes"]["cumulative_patch_sha256"],"f2aa236b6f72a006f920046be80b0a8cce272ef8a3dd9b118d091e2541a9a286")
        self.assertTrue(inp["source_notes"]["no_original_hidden_test_access"])
        reg=read(P/"P23_PREORACLE_ORIGINAL_TASK_EVALUATION_REGISTER_20261120.json")
        self.assertFalse(reg["official_harness_test_patch_prior_access"])
        self.assertTrue(reg["official_harness_original_result_pending"])
        self.assertTrue(reg["previous_results_and_MR30_unchanged"])


if __name__=="__main__":
    unittest.main()
