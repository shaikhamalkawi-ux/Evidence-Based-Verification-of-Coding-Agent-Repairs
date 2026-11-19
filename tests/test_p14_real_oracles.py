"""P14 observed original hidden-oracle *receipt* conformance tests.

These tests consume the two historical, already-executed original-harness
receipts. They DO NOT rerun SWE-bench-Live or imply n=2 independent tasks.
"""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"data/audits/P14_MATPLOTLIB_TWO_STAGE_ORIGINAL_ORACLE_20261119.jsonl"
spec=importlib.util.spec_from_file_location("p14_two_stage_reconcile",ROOT/"scripts/p14_two_stage_reconcile.py")
p14=importlib.util.module_from_spec(spec)
spec.loader.exec_module(p14)


class P14ExecutedOriginalOracles(unittest.TestCase):
    def _score(self):
        with tempfile.TemporaryDirectory() as td:
            s=p14.run(PATH,Path(td)/"p14_summary.json")
            return s

    def test_both_exact_stage_oracles_admitted_but_one_task(self):
        result=self._score()
        self.assertEqual(result["task_count_in_this_experiment"],1)
        self.assertEqual(result["candidate_stage_count"],2)
        self.assertFalse(result["stages_statistically_independent"])
        self.assertEqual(result["hidden_original_oracle_admitted_stage_count"],2)
        self.assertEqual(result["hidden_original_oracle_unadmitted_stage_count"],0)
        self.assertEqual(result["transition"],"NEITHER_CANDIDATE_RESOLVES_TASK")
        self.assertEqual([r["stage"] for r in result["stages"]],["stage1","stage2"])
        self.assertEqual([r["original_task_pass"] for r in result["stages"]],[False,False])

    def test_original_matplotlib_f2p_stays_zero_despite_visible_gain(self):
        result=self._score()
        for row in result["stages"]:
            self.assertEqual(row["f2p_total"],1)
            self.assertEqual(row["f2p_passed"],0)
            self.assertEqual(row["p2p_failed"],0)
            self.assertEqual(row["tests_executed"],8228)
            self.assertTrue(row["oracle_admitted"])
        source=p14.read_jsonl(PATH)
        self.assertEqual([x["matched_reports"] for x in source],[1,1])
        self.assertEqual([x["official_resolved"] for x in source],[False,False])
        self.assertEqual(len({x["original_test_output_sha256"] for x in source}),2)

    def test_frozen_stage2_accept_is_an_observed_false_accept(self):
        result=self._score()
        pol=result["original_p9_score"]["policies"]
        self.assertEqual((pol["self_report"]["all_accept"],pol["self_report"]["false_accept"]),(1,1))
        self.assertEqual((pol["local_pass"]["all_accept"],pol["local_pass"]["false_accept"]),(1,1))
        self.assertEqual((pol["source_linked"]["all_accept"],pol["source_linked"]["false_accept"]),(0,0))
        self.assertIsNone(pol["source_linked"]["false_accept_among_accepted"])
        self.assertEqual(result["original_p9_score"]["oracle_fail"],2)
        self.assertEqual(result["original_p9_score"]["oracle_pass"],0)

    def test_never_relabel_synthetic_feedback_as_human(self):
        result=self._score()
        self.assertFalse(result["human_developer_feedback"])
        self.assertFalse(result["agent_authorship_independently_attested"])
        self.assertIn("AI-generated",result["feedback_type"])
        self.assertEqual(result["decision_sha256"],
                         "9ad19413cc0a447464759bafc5786f6b63b179393c429d61dc69b5290ea7496a")

    def test_tampered_stage2_sha_must_fail(self):
        from copy import deepcopy
        rows=p14.read_jsonl(PATH)
        rows[1]["head_sha"]="f"*40
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"tampered.jsonl"
            path.write_text("".join(json.dumps(row)+"\n" for row in rows),encoding="utf-8")
            with self.assertRaises(ValueError):
                p14.run(path,Path(td)/"summary.json")

    def test_tampered_original_task_resolution_must_fail(self):
        rows=p14.read_jsonl(PATH)
        rows[1]["official_resolved"]=True
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"tampered.jsonl"
            path.write_text("".join(json.dumps(row)+"\n" for row in rows),encoding="utf-8")
            with self.assertRaises(ValueError):
                p14.run(path,Path(td)/"summary.json")

    def test_empty_oracle_never_imputed_as_failed_task(self):
        rows=p14.read_jsonl(PATH)
        rows[1]["status"]="error"
        rows[1]["f2p_total"]=0
        rows[1]["f2p_passed"]=0
        rows[1]["p2p_failed"]=0
        rows[1]["tests_executed"]=0
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"unavailable.jsonl"
            path.write_text("".join(json.dumps(row)+"\n" for row in rows),encoding="utf-8")
            result=p14.run(path,Path(td)/"summary.json")
            self.assertEqual(result["hidden_original_oracle_unadmitted_stage_count"],1)
            self.assertEqual(result["transition"],"UNKNOWN_INCOMPLETE_ORACLE")
            self.assertIsNone(result["stages"][1]["original_task_pass"])

if __name__=="__main__":
    unittest.main()
