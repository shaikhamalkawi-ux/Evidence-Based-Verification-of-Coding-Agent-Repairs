"""P20 original-source proof and preoracle P9 integrity negative controls.

No original benchmark gold; no full Flask app. Original task correctness must
come ONLY from the original pinned SWE-bench-Live evaluator after this seal.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"pilot/privacyidea"
A=ROOT/"data/audits"

def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


class TestP20SourcePreoracle(unittest.TestCase):
    def setUp(self):
        self.r=read(A/"P20_PRIVACYIDEA_ORIGINAL_VISIBLE_SOURCE_20261120.json")
        self.reg=read(P/"P20_PREORACLE_ORIGINAL_EVALUATION_REGISTER.json")

    def test_same_original_frozen_ten_task_frame(self):
        frame=read(ROOT/"pilot/frozen_task_frame_20261117.json")
        self.assertEqual(len(frame["selected"]),10)
        self.assertEqual(frame["selected"][6]["instance_id"],"privacyidea__privacyidea-4251")
        self.assertEqual(self.reg["original_case_index_one_based"],7)
        self.assertEqual(self.reg["original_case_base_sha"],"a44f38b40a61c5b91e6de68d20d27ed01d3ccb56")

    def test_source_exact_original_to_candidate_and_unchanged_test_hash(self):
        self.assertEqual(len(self.r["source_case_results"]),2)
        original,candidate=self.r["source_case_results"]
        self.assertEqual(original["head_sha"],self.reg["original_case_base_sha"])
        self.assertEqual(candidate["head_sha"],self.reg["initial_candidate_sha"])
        self.assertEqual(original["source_blob_sha"],self.reg["original_case_source_blob"])
        self.assertEqual(candidate["source_blob_sha"],"f1e0d1d1847baa5814c04f54807dce9df7524b8c")
        self.assertEqual(original["frozen_tests_sha256"],candidate["frozen_tests_sha256"])
        self.assertEqual(candidate["frozen_tests_sha256"],self.reg["original_visible_tests_sha256"])
        self.assertEqual(hashlib.sha256((P/"p20_visible_original_script_handler_ast.py").read_bytes()).hexdigest(),
                         self.reg["original_visible_tests_sha256"])

    def test_original_source_baseline_fails_and_candidate_visible_succeeds(self):
        a,b=self.r["source_case_results"]
        self.assertEqual((a["passed"],a["errors"],a["failed"],a["tests"]),(5,5,0,10))
        self.assertEqual((b["passed"],b["errors"],b["failed"],b["tests"]),(10,0,0,10))
        self.assertFalse(b["Flask_HTTP_status_tested"])
        self.assertFalse(b["full_privacyidea_app_loaded"])
        self.assertFalse(b["original_benchmark_oracle_accessed"])
        self.assertFalse(b["external_scripts_executed"])

    def test_original_P9_decision_and_input_hashes_exact(self):
        seal=read(P/"sealed/P9_DECISION_SEAL.json")
        decision=read(P/"sealed/P9_DECISIONS_SEALED.jsonl")
        raw_input=(P/"sealed/P20_DECISION_INPUT.jsonl").read_bytes()
        raw_decision=(P/"sealed/P9_DECISIONS_SEALED.jsonl").read_bytes()
        self.assertEqual(hashlib.sha256(raw_input).hexdigest(),seal["input_sha256"],self.reg["original_P9_input_sha256"])
        self.assertEqual(hashlib.sha256(raw_decision).hexdigest(),seal["decisions_sha256"],self.reg["original_P9_decisions_sha256"])
        self.assertEqual(hashlib.sha256((ROOT/"scripts/p9_decide.py").read_bytes()).hexdigest(),
                         seal["script_sha256"],self.reg["original_P9_script_sha256"])
        self.assertEqual(decision["t_decision"],"2026-11-20T03:40:19Z")
        self.assertEqual(decision["head_sha"],self.reg["initial_candidate_sha"])
        self.assertEqual(decision["decisions"],{"self_report":"HOLD","local_pass":"ACCEPT","source_linked":"HOLD"})

    def test_limited_source_coverage_cannot_be_a_task_oracle(self):
        self.assertTrue(self.r["source_AST_with_import_only_stubs"])
        self.assertTrue(self.r["original_benchmark_was_not_read_when_generating_these"])
        self.assertFalse(self.r["benchmark_gold_accessed_during_tests"])
        self.assertFalse(self.r["no_production_Flask_HTTP_task_test_execution"] is False)
        self.assertTrue(self.reg["no_original_hidden_data_seen_yet"])
        self.assertFalse(self.reg["initial_claim_of_full_HTTP_task_resolution"])
        self.assertFalse(self.reg["actor_independently_authenticated"])

    def test_source_inputs_cannot_contain_future_oracle_label(self):
        data=read(P/"sealed/P20_DECISION_INPUT.jsonl")
        forbidden={"oracle","oracle_status","oracle_result","future_ci","future_test","heldout_result",
                   "label","resolved","task_outcome","test_patch","FAIL_TO_PASS","PASS_TO_PASS"}
        self.assertFalse(forbidden.intersection(data))
        self.assertFalse(data["agent_claimed_fixed"])
        self.assertFalse(data["target_agent_is_commit_author"])
        self.assertTrue(data["source_verification"]["full_original_HTTP_task_completion_claim"] is False)


if __name__=="__main__":
    unittest.main()
