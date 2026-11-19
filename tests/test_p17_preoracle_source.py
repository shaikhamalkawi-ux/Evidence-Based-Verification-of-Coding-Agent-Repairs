"""P17 sealed source/CPU evidence conformance; NOT a hidden DoRA task oracle."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"pilot/torchtune"
V=ROOT/"data/audits/P17_HISTORICAL_DORA_CPU_SOURCE_VISIBLE_20261120.json"

def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

class TestP17CandidateAndPreOracle(unittest.TestCase):
    def test_original_frozen_index_and_base_unmodified(self):
        frame=read(ROOT/"pilot/frozen_task_frame_20261117.json")
        p=read(P/"P17_PREREGISTRATION_20261120.json")
        self.assertEqual(len(frame["selected"]),10)
        self.assertEqual(frame["selected"][4]["instance_id"],"pytorch__torchtune-2139")
        self.assertEqual(p["fixed_cohort"]["original_base_sha"],"f2bd4bc25b24587aef40f486087412b9da8f1d94")
        self.assertEqual(p["fixed_cohort"]["source_git_blob_sha"],"6f097da6d039738c320e8775ad61950c56fe0108")

    def test_original_historical_ast_test_frozen(self):
        v=read(V)
        p=read(P/"P17_PREREGISTRATION_20261120.json")
        test_sha=hashlib.sha256((P/"p17_visible_original_dora_cpu.py").read_bytes()).hexdigest()
        self.assertEqual(v["results"][0]["visible_tests_sha256"],test_sha)
        self.assertEqual(v["results"][1]["visible_tests_sha256"],test_sha)
        self.assertTrue(p["visible_test_protocol"]["locked_before_patch"])
        self.assertTrue(v["original_class_ast_executed"])
        self.assertFalse(v["full_torchtune_class_imported"])

    def test_original_source_baseline_and_candidate_results(self):
        v=read(V)
        a,b=v["results"]
        self.assertEqual(a["phase"],"base")
        self.assertEqual(b["phase"],"initial_candidate")
        self.assertEqual((a["passes"],a["failures"],a["errors"]),(2,3,1))
        self.assertEqual((b["passes"],b["failures"],b["errors"]),(6,0,0))
        self.assertEqual((a["tests_executed"],b["tests_executed"]),(6,6))
        self.assertEqual(b["head_sha"],"57f45fdd5552908d4b5d42cccd7359ccb4de2560")

    def test_original_P9_seal_has_exact_original_byte_contracts(self):
        manifest=read(P/"sealed/P9_DECISION_SEAL.json")
        d=(P/"sealed/P9_DECISIONS_SEALED.jsonl").read_bytes()
        i=(P/"sealed/P17_DECISION_INPUT.jsonl").read_bytes()
        reg=read(P/"P17_PREORACLE_EVALUATION_REGISTER.json")
        self.assertEqual(hashlib.sha256(d).hexdigest(),manifest["decisions_sha256"])
        self.assertEqual(hashlib.sha256(i).hexdigest(),manifest["input_sha256"])
        self.assertEqual(hashlib.sha256((ROOT/"scripts/p9_decide.py").read_bytes()).hexdigest(),manifest["script_sha256"])
        self.assertEqual(manifest["decisions_sha256"],reg["original_P9_policy_sha256"])
        self.assertEqual(manifest["input_sha256"],reg["original_P9_input_sha256"])
        self.assertEqual(manifest["episode_count"],1)
        # P9 decisions use compact canonical JSONL, but it hashes the raw input byte stream
        # without imposing the same canonical representation on the input.
        self.assertIn(b'", "',i)
        self.assertNotIn(b'", "',d)

    def test_locked_policies_do_not_infer_full_task_success(self):
        d=read(P/"sealed/P9_DECISIONS_SEALED.jsonl")
        inp=read(P/"sealed/P17_DECISION_INPUT.jsonl")
        self.assertEqual(d["decisions"],{"self_report":"HOLD","local_pass":"ACCEPT","source_linked":"HOLD"})
        self.assertFalse(inp["agent_claimed_fixed"])
        self.assertFalse(inp["target_agent_is_commit_author"])
        self.assertTrue(inp["source_verification"]["full_two_gpu_dora_recipe_success_not_observed"])
        self.assertTrue(inp["source_verification"]["original_torchtune_gpu_integration_test_not_executed"])
        self.assertEqual(d["t_decision"],"2026-11-19T20:45:51Z")
        self.assertGreater(d["t_decision"],inp["receipts"][0]["completed_at"])

    def test_original_oracle_not_used_for_original_preoracle_inputs(self):
        inp=read(P/"sealed/P17_DECISION_INPUT.jsonl")
        forbidden={"oracle","oracle_status","oracle_result","future_ci","future_test","heldout_result",
                   "label","resolved","task_outcome","test_patch","FAIL_TO_PASS","PASS_TO_PASS"}
        self.assertFalse(forbidden.intersection(inp))
        self.assertTrue(inp["source_verification"]["original_hidden_benchmark_not_yet_accessed"])
        self.assertFalse(read(P/"P17_PREREGISTRATION_20261120.json")["policy_boundary"]["original_P9_unchanged"] is False)

    def test_invalid_first_two_workflows_stopped_without_hidden_exposure(self):
        e=(P/"P17_PREORACLE_CANONICAL_BYTE_ERRATUM.md").read_text(encoding="utf-8")
        self.assertIn("44612325881",e)
        self.assertIn("44612710001",e)
        self.assertIn("before",e.lower())
        self.assertIn("raw",e.lower())

if __name__=="__main__":
    unittest.main()
