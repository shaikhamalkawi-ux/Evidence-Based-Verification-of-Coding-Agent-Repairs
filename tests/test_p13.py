"""P13 archived-result invariants: rigorously keep exploratory retest OUT of blind denominator."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("verify_p13_mechanism",ROOT/"scripts/verify_p13_mechanism.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class TestP13PostReveal(unittest.TestCase):
    def test_original_hidden_not_solving_task(self):
        x=m.audit()
        self.assertEqual(x["P12_F2P_passed"],0)
        self.assertEqual(x["P13_F2P_passed"],0)
        self.assertFalse(x["P13_original_task_resolved"])

    def test_regressions_fixed_without_issue_success(self):
        x=m.audit()
        self.assertEqual(x["P12_original_update_public_regressions"],2)
        self.assertEqual(x["P13_original_update_public_regressions"],0)
        self.assertEqual((x["P12_P2P_failed"],x["P13_P2P_failed"]),(2,0))
        self.assertEqual((x["P12_visible_pass"],x["P13_visible_pass"]),(3,3))

    def test_postreveal_candidate_never_a_fifth_prospective_trial(self):
        x=m.audit()
        self.assertEqual(x["exposed_task_count"],1)
        self.assertEqual(x["prospective_policy_trial_count_added_by_P13"],0)
        self.assertFalse(x["P13_hidden_retest_blinded"])

    def test_tampering_retest_f2p_is_rejected(self):
        doc=m.read(m.P13)
        doc["variants"][2]["f2p_passed"]=3
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"bad.json";p.write_text(json.dumps(doc),encoding="utf-8")
            with self.assertRaises(AssertionError):
                m.audit(p)

    def test_tampering_retest_blind_flag_is_rejected(self):
        doc=m.read(m.P13)
        doc["variants"][2]["not_blinded_by_this_test"]=False
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"bad.json";p.write_text(json.dumps(doc),encoding="utf-8")
            with self.assertRaises(AssertionError):
                m.audit(p)

    def test_tampering_original_frozen_p2p_is_rejected(self):
        doc=m.read(m.P13)
        doc["variants"][1]["p2p_failed"]=0
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"bad.json";p.write_text(json.dumps(doc),encoding="utf-8")
            with self.assertRaises(AssertionError):
                m.audit(p)


if __name__=="__main__":
    unittest.main()
