"""Regression checks for P11 evidence boundaries; not external task validation."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("verify_p11_evidence",ROOT/"scripts/verify_p11_evidence.py")
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class P11EvidenceTests(unittest.TestCase):
    def test_source_and_benchmark_denominators_remain_disjoint(self):
        s=m.audit()
        self.assertEqual(s["source_frame"]["n"],10)
        self.assertEqual(s["source_frame"]["repositories"],5)
        self.assertEqual(s["source_frame"]["commits"],42)
        self.assertEqual(s["source_frame"]["discussion_events"],129)
        self.assertEqual(s["source_frame"]["independent_uniform_oracles"],0)
        self.assertEqual(s["benchmark_initial_only"]["n"],3)
        self.assertEqual(s["benchmark_initial_only"]["executed_tests"],10915)
        self.assertEqual((s["benchmark_initial_only"]["oracle_pass"],
                          s["benchmark_initial_only"]["oracle_fail"]),(2,1))
        self.assertFalse(s["causal_policy_efficacy_estimated"])

    def test_conservative_policy_has_empty_accepted_denominator(self):
        s=m.audit()["benchmark_initial_only"]
        x=s["policies"]["source_linked"]
        self.assertEqual((x["accept"], x["hold"]), (0,3))
        self.assertEqual(x["unnecessary_hold_count"],2)
        self.assertEqual(s["source_linked_accept_denominator"],0)

    def test_empty_accepted_rate_is_null_not_zero(self):
        j=m.load(m.LEDGER)
        self.assertIsNone(j["benchmark_initial_only"]["observed_only_summary"]["source_linked"]["false_accept_rate_among_accepted"])

    def test_tampering_source_commit_count_fails(self):
        data=m.load(m.LEDGER)
        data["source_frame"]["rows"][0]["commit_count"] += 1
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"corrupt.json"
            p.write_text(json.dumps(data),encoding="utf-8")
            with self.assertRaises(AssertionError):
                m.audit(p)

    def test_tampering_oracle_truth_fails(self):
        data=m.load(m.LEDGER)
        data["benchmark_initial_only"]["cases"][0]["official_resolved"]=True
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"corrupt.json"
            p.write_text(json.dumps(data),encoding="utf-8")
            with self.assertRaises(AssertionError):
                m.audit(p)

    def test_actor_negative_control_fails_if_reassigned(self):
        data=m.load(m.LEDGER)
        anchors=data["prespecified_narrow_event_anchors"]
        a=next(x for x in anchors if x["name"]=="HUMAN_AUTHOR_NEGATIVE_CONTROL")
        a["final_commit_author"]="Copilot"
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"corrupt.json"
            p.write_text(json.dumps(data),encoding="utf-8")
            with self.assertRaises(AssertionError):
                m.audit(p)


if __name__=="__main__":
    unittest.main()
