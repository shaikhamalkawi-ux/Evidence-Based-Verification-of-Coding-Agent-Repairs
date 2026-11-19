"""P14 original-oracle reconciliation unit tests (SYNTHETIC, NOT real results)."""
from __future__ import annotations

from copy import deepcopy
import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"scripts"))
from p9_reveal import oracle_label

spec=importlib.util.spec_from_file_location(
    "p14_two_stage_reconcile",ROOT/"scripts/p14_two_stage_reconcile.py")
p14=importlib.util.module_from_spec(spec)
spec.loader.exec_module(p14)

FROZEN=p14.load(p14.REGISTER)
DECISIONS=p14.read_jsonl(p14.SEAL/"P9_DECISIONS_SEALED.jsonl")

def synthetic(stage, result):
    """Artificial test payload for software checks only. Never treated as observed."""
    unit=FROZEN[stage]
    good=bool(result)
    return {
      "episode_id":unit["episode_id"],
      "stage":stage,
      "head_sha":unit["candidate_sha"],
      "oracle_type":"heldout_harness",
      "oracle_code_sha256":"a"*64,
      "source_url":"https://example.invalid/SYNTHETIC_ONLY",
      "started_at":"2026-11-19T19:01:30Z",
      "oracle_test_manifest_frozen_before_decision":True,
      "oracle_independent_of_visible_receipts":True,
      "oracle_unmodified_by_agent":True,
      "status":"complete",
      "f2p_total":3,
      "f2p_passed":3 if good else 0,
      "p2p_failed":0 if good else 2,
      "tests_executed":939,
      "official_resolved":good,
      "original_test_output_sha256":"b"*64,
      "scientific_scope":"TWO_CORRELATED_STAGE_CANDIDATES_FROM_ONE_SYNTHETIC_FEEDBACK_TASK",
      "original_harness_commit":FROZEN["harness_sha"],
      "dataset_revision":FROZEN["dataset_revision_sha"],
      "matched_reports":1,
      "human_developer_feedback":False,
      "agent_authorship_independently_attested":False,
    }


class P14ReconcileTests(unittest.TestCase):
    def setUp(self):
        self.frozen=deepcopy(FROZEN)
        self.dec=deepcopy(DECISIONS)
        self.recs=[synthetic("stage1",False),synthetic("stage2",True)]

    def test_synthetic_two_stage_pair_admitted_separately(self):
        rows=p14.admissions(self.recs,self.frozen,self.dec,oracle_label)
        self.assertEqual(len(rows),2)
        self.assertEqual([r["stage"] for r in rows],["stage1","stage2"])
        self.assertEqual([r["original_task_pass"] for r in rows],[False,True])
        self.assertEqual(sum(r["oracle_admitted"] for r in rows),2)

    def test_synthetic_changing_sha_rejected(self):
        x=deepcopy(self.recs)
        x[1]["head_sha"]="c"*40
        with self.assertRaises(ValueError):
            p14.admissions(x,self.frozen,self.dec,oracle_label)

    def test_synthetic_lost_stage_not_replaced(self):
        with self.assertRaises(ValueError):
            p14.admissions(self.recs[:1],self.frozen,self.dec,oracle_label)

    def test_synthetic_falsely_attributed_human_feedback_rejected(self):
        x=deepcopy(self.recs)
        x[1]["human_developer_feedback"]=True
        with self.assertRaises(ValueError):
            p14.admissions(x,self.frozen,self.dec,oracle_label)

    def test_synthetic_falsely_attested_agent_rejected(self):
        x=deepcopy(self.recs)
        x[1]["agent_authorship_independently_attested"]=True
        with self.assertRaises(ValueError):
            p14.admissions(x,self.frozen,self.dec,oracle_label)

    def test_synthetic_ambiguous_reports_rejected(self):
        x=deepcopy(self.recs)
        x[0]["matched_reports"]=2
        with self.assertRaises(ValueError):
            p14.admissions(x,self.frozen,self.dec,oracle_label)

    def test_synthetic_zero_tests_remain_unknown(self):
        x=deepcopy(self.recs)
        x[0]["f2p_total"]=0
        x[0]["f2p_passed"]=0
        x[0]["tests_executed"]=0
        x[0]["official_resolved"]=False
        result=p14.admissions(x,self.frozen,self.dec,oracle_label)
        self.assertIsNone(result[0]["original_task_pass"])
        self.assertFalse(result[0]["oracle_admitted"])
        self.assertEqual(result[0]["nonadmission_reason"],"invalid_oracle_counts")

    def test_synthetic_false_official_resolved_rejected(self):
        x=deepcopy(self.recs)
        x[1]["official_resolved"]=False
        with self.assertRaises(ValueError):
            p14.admissions(x,self.frozen,self.dec,oracle_label)


if __name__=="__main__":
    unittest.main()
