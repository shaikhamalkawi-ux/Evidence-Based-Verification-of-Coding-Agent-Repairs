"""P19 original task and original decision claim-boundary conformance.

These are tests of saved, executed source receipts and the ORIGINAL preoracle
seal, NOT an original-task rerun and NOT a substitute for held-out tests.
"""
import json
import hashlib
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"pilot/dspy"
A=ROOT/"data/audits"

def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


class TestP19ExecutedOracle(unittest.TestCase):
    def setUp(self):
        self.r=read(A/"P19_DSPY_INITIAL_ORIGINAL_TASK_ORACLE_20261120.json")
        self.o=self.r["original_benchmark_result"]
        self.panel=read(A/"P19_SEVEN_TASK_MIXED_STAGE_NONVACUITY_20261120.json")

    def test_original_task_was_a_real_executed_failure_not_infrastructure(self):
        self.assertEqual(self.o["episode_id"],"stanfordnlp__dspy-1609__INITIAL_ATTEMPT_SOURCE_ONLY")
        self.assertEqual(self.o["head_sha"],"2a2938cbd2b616c684768902bdcc0bfc09e7b9a4")
        self.assertEqual(self.o["status"],"complete")
        self.assertEqual(self.o["matched_reports"],1)
        self.assertEqual(self.o["f2p_total"],4)
        self.assertEqual(self.o["f2p_passed"],0)
        self.assertEqual(self.o["p2p_failed"],0)
        self.assertEqual(self.o["tests_executed"],261)
        self.assertIs(self.o["official_resolved"],False)

    def test_p19_is_original_frozen_sixth_task(self):
        frame=read(ROOT/"pilot/frozen_task_frame_20261117.json")
        self.assertEqual(frame["selected"][5]["instance_id"],"stanfordnlp__dspy-1609")
        self.assertEqual(frame["selected"][5]["repo"],"stanfordnlp/dspy")
        self.assertEqual(self.r["original_frozen_index_one_based"],6)
        self.assertEqual(self.r["original_source_base_sha"],"16ceaba5f7126ca86e5b50b669975c926b9f8f55")

    def test_local_visible_pass_does_not_override_original_F2P(self):
        self.assertEqual(self.r["original_visible"]["base_passed"],3)
        self.assertEqual(self.r["original_visible"]["candidate_passed"],9)
        self.assertEqual(self.r["original_visible"]["candidate_total"],9)
        self.assertEqual(self.o["f2p_passed"],0)
        self.assertIs(self.r["model_based_Databricks_optimization_reproducer_executed"],False)
        self.assertEqual(self.r["original_P9_decisions"]["local_pass"],"ACCEPT")
        self.assertEqual(self.r["separately_registered_process_gate"]["preoracle_decision"],"ACCEPT")

    def test_original_P9_seal_unchanged_and_alternative_separate(self):
        seal=read(P/"sealed/P19_TWO_POLICY_SEAL_MANIFEST.json")
        p9=read(P/"sealed/P9_DECISION_SEAL.json")
        b=(P/"sealed/P9_DECISIONS_SEALED.jsonl").read_bytes()
        c=(P/"sealed/P19_PROCESS_LINKED_V1_SEALED.jsonl").read_bytes()
        self.assertEqual(hashlib.sha256(b).hexdigest(),seal["P9_original_decisions_sha256"],p9["decisions_sha256"])
        self.assertEqual(hashlib.sha256(c).hexdigest(),seal["new_process_decision_sha256"])
        self.assertEqual(self.r["original_P9_seal_sha256"],seal["P9_original_decisions_sha256"])
        self.assertEqual(self.r["separately_registered_process_gate"]["preoracle_sha256"],seal["new_process_decision_sha256"])
        self.assertEqual(self.r["original_decisions_frozen_at"],"2026-11-20T03:17:43Z")

    def test_seven_distinct_original_tasks_not_261_independent_trials(self):
        p=self.panel
        self.assertEqual(p["original_task_count"],10)
        self.assertEqual(p["now_evaluated_distinct_task_count"],7)
        self.assertEqual(p["not_yet_evaluated_task_count"],3)
        self.assertEqual(p["original_oracle_task_pass_count"],2)
        self.assertEqual(p["original_oracle_task_fail_count"],5)
        self.assertEqual(len(p["unique_task_rows"]),7)
        self.assertEqual(len({x["task"] for x in p["unique_task_rows"]}),7)
        self.assertEqual(sum(x["truth"] for x in p["unique_task_rows"]),2)

    def test_seven_task_original_P9_acceptance_counts(self):
        policies=self.panel["original_P9_descriptive_policies"]
        self.assertEqual((policies["local_pass"]["n_accepted"],policies["local_pass"]["n_false_accepted"]),(6,5))
        self.assertEqual((policies["self_report"]["n_accepted"],policies["self_report"]["n_false_accepted"]),(4,3))
        self.assertEqual((policies["source_linked"]["n_accepted"],policies["source_linked"]["n_false_accepted"]),(0,0))
        self.assertIsNone(policies["source_linked"]["false_accept_fraction_among_accepted"])
        self.assertEqual(policies["source_linked"]["n_unnecessary_hold"],2)

    def test_new_process_gate_only_one_task_no_fake_superiority(self):
        v=self.panel["forward_process_v1_P19_ONLY"]
        self.assertEqual(v["case"],"stanfordnlp__dspy-1609")
        self.assertEqual(v["preoracle_accept"],"ACCEPT")
        self.assertTrue(v["original_task_false_accept"])
        self.assertEqual(v["sample_size"],1)
        self.assertTrue(v["not_population_approval_or_efficiency_evidence"])
        self.assertTrue(self.panel["no_P18_postreveal_in_original_sample"])

    def test_original_runner_and_hash_evidence_trace(self):
        self.assertEqual(self.o["source_url"],"https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44666993268")
        self.assertEqual(self.r["original_harness_artifact_id"],14598665908)
        self.assertEqual(self.o["dataset_revision"],"babb27e45e072219195db7a744bbf0d3c1a36e56")
        self.assertEqual(self.o["original_harness_sha"],"ad79b850f15e33992e96f03f6e97f05ddf9aa0be")
        self.assertEqual(self.o["oracle_code_sha256"],"9a9361d7c53f64d573ef546325b6f13d5b593fa78b4ddcbaa380efa0cd0aac04")
        self.assertEqual(len(self.o["original_test_output_sha256"]),64)


if __name__=="__main__":
    unittest.main()
