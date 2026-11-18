"""P12 integrity checks for the pre-registered PDM INITIAL ONLY pilot.

No hidden oracle outcome imported or simulated. This test covers source/visible
metadata and the GitHub-public timestamped P9 decision seal, not PDM correctness.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
PDM=ROOT/"pilot/pdm"

def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


class PDMPreoracleTests(unittest.TestCase):
    def test_selection_remains_original_frozen_index(self):
        f=read(ROOT/"pilot/frozen_task_frame_20261117.json")
        p=read(PDM/"P12_PREREGISTRATION_20261118.json")
        self.assertEqual(f["selected"][1]["instance_id"],"pdm-project__pdm-3419")
        self.assertEqual(p["task"]["base_commit"],"564d09acbf2c8ef6500a3864f1fa1d38b3c5cdd5")
        self.assertEqual(f["n_selected"],10)
        self.assertEqual(p["source"]["dataset_revision"],f["dataset_revision_sha"])
        self.assertEqual(p["task"]["frozen_index_one_based"],2)

    def test_real_p9_seal_matches_original_policy_script(self):
        seal=read(PDM/"locked/P9_DECISION_SEAL.json")
        decisions=(PDM/"locked/P9_DECISIONS_SEALED.jsonl").read_bytes()
        source=(PDM/"decision_input.jsonl").read_bytes()
        p9=(ROOT/"scripts/p9_decide.py").read_bytes()
        self.assertEqual(hashlib.sha256(decisions).hexdigest(),seal["decisions_sha256"])
        self.assertEqual(hashlib.sha256(source).hexdigest(),seal["input_sha256"])
        self.assertEqual(hashlib.sha256(p9).hexdigest(),seal["script_sha256"])
        self.assertEqual(seal["episode_count"],1)
        self.assertEqual(seal["policy_version"],"X1-P9-alpha-1-20261116")

    def test_initial_decision_precedes_oracle_and_does_not_claim_agent_attribution(self):
        d=read(PDM/"locked/P9_DECISIONS_SEALED.jsonl")
        inp=read(PDM/"decision_input.jsonl")
        prereg=read(PDM/"oracle_evaluation_preregister.json")
        self.assertEqual(d["decisions"],{"self_report":"ACCEPT","local_pass":"ACCEPT","source_linked":"HOLD"})
        self.assertEqual(d["head_sha"],inp["head_sha"])
        self.assertEqual(inp["head_sha"],prereg["target_candidate_head_sha"])
        self.assertEqual(prereg["preoracle_decisions_sha256"],
                         hashlib.sha256((PDM/"locked/P9_DECISIONS_SEALED.jsonl").read_bytes()).hexdigest())
        self.assertEqual(d["t_decision"],prereg["preoracle_decision_time_utc"])
        self.assertGreater(d["t_decision"],inp["receipts"][0]["completed_at"])
        self.assertFalse(inp["target_agent_is_commit_author"])
        self.assertFalse(inp["source_verification"]["post_feedback_patch_exists"])
        self.assertFalse(inp["source_verification"]["scripted_developer_feedback_received"])
        self.assertFalse(prereg["agent_authorship_independently_attested"])
        self.assertEqual(prereg["task_stage"],"INITIAL_ATTEMPT_ONLY_PER_FROZEN_STOP_RULE")

    def test_visible_base_failure_is_not_a_hidden_oracle(self):
        inp=read(PDM/"decision_input.jsonl")
        v=inp["source_verification"]
        self.assertEqual((v["baseline_visible_tests"]["passed"],v["baseline_visible_tests"]["failed"]),(0,3))
        self.assertEqual((v["initial_visible_tests"]["passed"],v["initial_visible_tests"]["failed"]),(3,0))
        self.assertEqual(inp["receipts"][0]["status"],"success")
        self.assertEqual(inp["receipts"][0]["test_count"],3)
        self.assertEqual(v["scope"],"INITIAL_ONLY_BY_PRE_REGISTERED_STOP_RULE; NOT TWO_STAGE_OR_POST_FEEDBACK")
        self.assertTrue(inp["receipts"][0]["test_scope_prespecified"])
        self.assertIn("44236769972",inp["receipts"][0]["source_url"])

    def test_forbidden_hidden_fields_not_in_predecision_record(self):
        inp=read(PDM/"decision_input.jsonl")
        forbidden={"oracle","oracle_status","oracle_result","future_ci","future_test",
                   "heldout_result","label","resolved","task_outcome","test_patch",
                   "FAIL_TO_PASS","PASS_TO_PASS"}
        self.assertFalse(forbidden.intersection(inp))


if __name__=="__main__":
    unittest.main()
