"""P14 evidence-boundary checks. These are software-only, NOT task oracle tests.

Both candidate SHAs and decisions were sealed and publicly timestamped BEFORE
the original benchmark task oracle. Two stages = ONE benchmark task.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "pilot" / "matplotlib"

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def load_jsonl(path):
    return [json.loads(s) for s in Path(path).read_text(encoding="utf-8").splitlines() if s.strip()]

class TestP14MatplotlibPreoracle(unittest.TestCase):
    def test_frozen_task_index_and_unmodified_matplotlib_source(self):
        frame = load(ROOT/"pilot/frozen_task_frame_20261117.json")
        reg = load(P/"P14_PREREGISTRATION_20261119.json")
        self.assertEqual(len(frame["selected"]), 10)
        self.assertEqual(reg["task"]["index_one_based"], 3)
        self.assertEqual(frame["selected"][2]["instance_id"], "matplotlib__matplotlib-28933")
        self.assertEqual(frame["selected"][2]["repo"], "matplotlib/matplotlib")
        self.assertEqual(reg["task"]["base_commit"], "cf84d9a6410dec07f57916905c9f54bf00d22b2e")
        self.assertEqual(reg["task"]["source_blob_sha"], "9629a821368cc66ddf98f31371ef7c0672642ead")
        self.assertEqual(reg["benchmark"]["dataset_sha"], frame["dataset_revision_sha"])

    def test_visible_test_file_was_frozen_before_first_patch(self):
        fb = load(P/"P14_SCRIPTED_FEEDBACK_AFTER_FIRST.json")
        sha = hashlib.sha256((P/"visible_tests.py").read_bytes()).hexdigest()
        self.assertEqual(sha, fb["observed_before_feedback"]["frozen_visible_test_file_sha256"])
        self.assertEqual(sha, "d3767954e5018d2c7fde871fcce2d6850e48e0529224713666e08c918a14ded0")
        self.assertEqual(fb["observed_before_feedback"]["first_patch"]["failed"], 1)
        self.assertEqual(fb["observed_before_feedback"]["first_patch"]["passed"], 5)
        self.assertEqual(fb["observed_before_feedback"]["failing_test"],
                         "pilot/matplotlib/visible_tests.py::test_xy_keyword_signature_for_each_setter")
        self.assertFalse(fb["observed_before_feedback"].get("hidden_oracle_seen", False))
        self.assertTrue(fb["synthetic_not_human"])
        self.assertTrue(fb["before_hidden_oracle"])

    def test_preoracle_seal_persists_original_p9_policy(self):
        seal = load(P/"sealed/P9_DECISION_SEAL.json")
        locked = (P/"sealed/P9_DECISIONS_SEALED.jsonl").read_bytes()
        inp = (P/"sealed/P14_DECISION_INPUT.jsonl").read_bytes()
        reg = load(P/"P14_PREORACLE_EVALUATION_REGISTER.json")
        self.assertEqual(hashlib.sha256(locked).hexdigest(), seal["decisions_sha256"])
        self.assertEqual(hashlib.sha256(inp).hexdigest(), seal["input_sha256"])
        self.assertEqual(hashlib.sha256((ROOT/"scripts/p9_decide.py").read_bytes()).hexdigest(), seal["script_sha256"])
        self.assertEqual(reg["preoracle_decisions_sha256"], seal["decisions_sha256"])
        self.assertEqual(reg["preoracle_input_sha256"], seal["input_sha256"])
        self.assertEqual(seal["episode_count"], 2)
        self.assertEqual(reg["preoracle_git_seal_commit"], "3aced6a089fa27e7802e8220404afb2ab9f21e28")
        self.assertEqual(reg["preoracle_timestamp_utc"], "2026-11-19T19:00:29Z")

    def test_stage_specific_decisions_same_task_and_timing(self):
        reg = load(P/"P14_PREORACLE_EVALUATION_REGISTER.json")
        ds = load_jsonl(P/"sealed/P9_DECISIONS_SEALED.jsonl")
        inp = load_jsonl(P/"sealed/P14_DECISION_INPUT.jsonl")
        self.assertEqual(len(ds), len(inp))
        by_id = {x["episode_id"]: x for x in ds}
        self.assertEqual(len(by_id), 2)
        self.assertEqual(reg["original_sample_size"], 10)
        self.assertFalse(reg["stage1_stage2_statistical_independence"])
        self.assertFalse(reg["feedback_real_human"])
        self.assertFalse(reg["agent_authorship_independently_attested"])
        for stage, expected in (
            ("stage1", {"self_report": "HOLD", "local_pass": "HOLD", "source_linked": "HOLD"}),
            ("stage2", {"self_report": "ACCEPT", "local_pass": "ACCEPT", "source_linked": "HOLD"}),
        ):
            unit = reg[stage]
            d = by_id[unit["episode_id"]]
            self.assertEqual(d["head_sha"], unit["candidate_sha"])
            self.assertEqual(d["decisions"], expected)
            self.assertEqual(d["t_decision"], reg["preoracle_timestamp_utc"])
        self.assertEqual({x["repo"] for x in inp}, {"matplotlib/matplotlib"})
        self.assertTrue(all(x["t_decision"] > x["receipts"][0]["completed_at"] for x in inp))
        self.assertTrue(all(x["target_agent_is_commit_author"] is False for x in inp))
        self.assertTrue(all(x["unrelated_intervening_edit"] is False for x in inp))
        self.assertEqual(inp[0]["receipts"][0]["status"], "failure")
        self.assertEqual(inp[1]["receipts"][0]["status"], "success")
        self.assertEqual(inp[0]["head_sha"], reg["stage1"]["candidate_sha"])
        self.assertEqual(inp[1]["head_sha"], reg["stage2"]["candidate_sha"])

    def test_oracle_fields_absent_from_locked_decision_inputs(self):
        inputs = load_jsonl(P/"sealed/P14_DECISION_INPUT.jsonl")
        forbidden = {"oracle", "oracle_status", "oracle_result", "future_ci", "future_test",
                     "heldout_result", "label", "resolved", "task_outcome",
                     "test_patch", "FAIL_TO_PASS", "PASS_TO_PASS"}
        self.assertEqual(len(inputs), 2)
        for row in inputs:
            self.assertFalse(forbidden.intersection(row))
            self.assertNotIn("oracle_result", row.get("source_verification", {}))

    def test_no_fake_human_review_or_qualifying_agent_attestation(self):
        fb = load(P/"P14_SCRIPTED_FEEDBACK_AFTER_FIRST.json")
        reg = load(P/"P14_PREORACLE_EVALUATION_REGISTER.json")
        self.assertFalse(reg["feedback_real_human"])
        self.assertTrue(reg["feedback_synthetic_ai"])
        self.assertFalse(reg["agent_authorship_independently_attested"])
        self.assertTrue(fb["synthetic_not_human"])
        self.assertEqual(fb["requested_corrective_attempts"], 1)

if __name__ == "__main__":
    unittest.main()
