"""P19 prospective seal identity and process-policy negative controls.

Executed AFTER decisions were publicly committed, WITHOUT benchmark gold or
task labels. Never evaluates the original benchmark task.
"""
from __future__ import annotations
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
F=ROOT/"pilot/dspy"
S=F/"sealed"

def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


SPEC=importlib.util.spec_from_file_location("p19_process_gate",ROOT/"scripts/p19_process_gate.py")
GATE=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)


class TestP19Preoracle(unittest.TestCase):
    def test_original_task_position_sha_and_unmodified_cohort(self):
        frame=read(ROOT/"pilot/frozen_task_frame_20261117.json")
        reg=read(F/"P19_PREORACLE_ORIGINAL_EVALUATION_REGISTER.json")
        self.assertEqual(len(frame["selected"]),10)
        self.assertEqual(frame["selected"][5]["instance_id"],"stanfordnlp__dspy-1609")
        self.assertEqual(reg["original_frozen_task"],"stanfordnlp__dspy-1609")
        self.assertEqual(reg["original_source_base_sha"],"16ceaba5f7126ca86e5b50b669975c926b9f8f55")
        self.assertEqual(reg["initial_candidate_sha"],"2a2938cbd2b616c684768902bdcc0bfc09e7b9a4")

    def test_two_separate_policy_byte_hashes_locked(self):
        reg=read(F/"P19_PREORACLE_ORIGINAL_EVALUATION_REGISTER.json")
        m=read(S/"P19_TWO_POLICY_SEAL_MANIFEST.json")
        p9=read(S/"P9_DECISION_SEAL.json")
        self.assertEqual(hashlib.sha256((S/"P19_DECISION_INPUT.jsonl").read_bytes()).hexdigest(),
                         m["raw_decision_input_sha256"])
        self.assertEqual(hashlib.sha256((S/"P9_DECISIONS_SEALED.jsonl").read_bytes()).hexdigest(),
                         m["P9_original_decisions_sha256"])
        self.assertEqual(hashlib.sha256((S/"P19_PROCESS_LINKED_V1_SEALED.jsonl").read_bytes()).hexdigest(),
                         m["new_process_decision_sha256"])
        self.assertEqual(hashlib.sha256((ROOT/"scripts/p9_decide.py").read_bytes()).hexdigest(),
                         m["P9_original_script_sha256"])
        self.assertEqual(hashlib.sha256((ROOT/"scripts/p19_process_gate.py").read_bytes()).hexdigest(),
                         m["new_process_script_sha256"])
        self.assertEqual(m["P9_original_decisions_sha256"],p9["decisions_sha256"],
                         reg["original_P9_decisions_sha256"])
        self.assertEqual(m["raw_decision_input_sha256"],p9["input_sha256"],
                         reg["original_P9_input_sha256"])

    def test_original_P9_and_new_process_not_conflated(self):
        reg=read(F/"P19_PREORACLE_ORIGINAL_EVALUATION_REGISTER.json")
        d=read(S/"P9_DECISIONS_SEALED.jsonl")
        p=read(S/"P19_PROCESS_LINKED_V1_SEALED.jsonl")
        self.assertEqual(d["decisions"],{"self_report":"HOLD","local_pass":"ACCEPT","source_linked":"HOLD"})
        self.assertEqual(p["decision"],"ACCEPT")
        self.assertEqual(p["policy_version"],"X1-P19-artifact-linked-no-actor-v1")
        self.assertFalse(p["actor_model_identity_independently_attested"])
        self.assertFalse(p["this_is_original_P9_source_linked_policy"])
        self.assertFalse(p["reference_oracle_used"])
        self.assertEqual(d["head_sha"],p["head_sha"],reg["initial_candidate_sha"])
        self.assertEqual(d["t_decision"],p["t_decision"],reg["decision_sealed_timestamp_utc"])
        self.assertTrue(all(p["features"].values()))

    def test_fixed_original_cpu_suite_hash_and_only_one_candidate(self):
        r=read(F/"P19_PREORACLE_ORIGINAL_EVALUATION_REGISTER.json")
        actual=hashlib.sha256((F/"p19_visible_original_adapter_ast.py").read_bytes()).hexdigest()
        self.assertEqual(actual,r["frozen_visible_test_sha256"])
        self.assertEqual(r["historical_visible_baseline"]["passed"],3)
        self.assertEqual(r["initial_visible_candidate"]["passed"],9)
        self.assertEqual(r["initial_visible_candidate"]["total"],9)
        self.assertIn("INITIAL_ATTEMPT_ONLY",r["stage"])
        self.assertFalse(r["original_live_databricks_LM_not_called"] is False)

    def test_no_original_hidden_oracle_features_in_input(self):
        r=read(S/"P19_DECISION_INPUT.jsonl")
        self.assertFalse(GATE.FORBIDDEN.intersection(r))
        self.assertTrue(r["source_verification"]["original_independent_task_oracle_not_yet_seen"])
        self.assertFalse(r["target_agent_is_commit_author"])
        self.assertFalse(r["agent_claimed_fixed"])

    def _mutate(self,mutate):
        r=read(S/"P19_DECISION_INPUT.jsonl")
        mutate(r)
        with tempfile.TemporaryDirectory() as tmp:
            inp=Path(tmp)/"input.jsonl"
            out=Path(tmp)/"output.jsonl"
            inp.write_text(json.dumps(r)+"\n")
            return GATE.run(inp,out)

    def test_changed_candidate_sha_must_HOLD_in_new_process(self):
        x=self._mutate(lambda r:r.update(head_sha="f"*40))
        self.assertEqual(x["decision"],"HOLD")
        self.assertFalse(x["features"]["candidate_sha_exact"])

    def test_false_actor_attestation_must_NOT_upgrade_process_admission(self):
        x=self._mutate(lambda r:r.update(target_agent_is_commit_author=True))
        self.assertEqual(x["decision"],"HOLD")
        self.assertFalse(x["features"]["no_actor_authentication_claim"])

    def test_original_test_zero_count_is_not_admitted(self):
        x=self._mutate(lambda r:r["receipts"][0].update(test_count=0))
        self.assertEqual(x["decision"],"HOLD")
        self.assertFalse(x["features"]["receipt_nonempty_all_pass"])

    def test_illegal_hidden_oracle_field_must_raise(self):
        with self.assertRaises(ValueError):
            self._mutate(lambda r:r.update(resolved=True))


if __name__=="__main__":
    unittest.main()
