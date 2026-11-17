"""P10 tests: deterministic, frozen-frame integrity and role-label safeguards.

Software QA only; passing these tests does not certify any agent repair.
"""
from pathlib import Path
import importlib.util
import json
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("audit_p10_source",ROOT/"scripts/audit_p10_source.py")
p10=importlib.util.module_from_spec(spec)
spec.loader.exec_module(p10)

class SourceFrameTests(unittest.TestCase):
    def test_fixed_denominator(self):
        r=p10.audit()
        self.assertEqual(r["rows_in_frozen_frame"],10)
        self.assertEqual(r["distinct_repositories"],5)
        self.assertTrue(r["archive_complete"])
        self.assertEqual(len(r["units"]),10)
        self.assertFalse(r["repair_effectiveness_estimable"])
        self.assertEqual(r["independently_admitted_task_oracles"],0)

    def test_actor_label_does_not_match_substring_bot(self):
        self.assertEqual(p10.classify_name("IDAbbott"),"unverified_nonbot_label")
        self.assertEqual(p10.classify_name("MaslowBot"),"automation_label")
        self.assertEqual(p10.classify_name("github-actions[bot]"),"automation_label")
        self.assertEqual(p10.classify_name("Copilot"),"automation_label")
        self.assertEqual(p10.classify_name(None),"unknown")

    def test_source_snapshots_have_sha256(self):
        r=p10.audit()
        self.assertTrue(all(len(x["snapshot_sha256"])==64 for x in r["units"]))

    def test_duplicate_pr_fails(self):
        orig=p10.FRAME
        with tempfile.TemporaryDirectory() as td:
            data=json.loads(orig.read_text())
            data["cases"][1]["pr_number"]=data["cases"][0]["pr_number"]
            data["cases"][1]["repository"]=data["cases"][0]["repository"]
            out=Path(td)/"frame.json"
            out.write_text(json.dumps(data))
            try:
                p10.FRAME=out
                with self.assertRaises(AssertionError):
                    p10.audit()
            finally:
                p10.FRAME=orig

    def test_reordered_case_fails(self):
        orig=p10.FRAME
        with tempfile.TemporaryDirectory() as td:
            data=json.loads(orig.read_text())
            data["cases"][1],data["cases"][0]=data["cases"][0],data["cases"][1]
            out=Path(td)/"frame.json"
            out.write_text(json.dumps(data))
            try:
                p10.FRAME=out
                with self.assertRaises(AssertionError):
                    p10.audit()
            finally:
                p10.FRAME=orig

if __name__=="__main__":
    unittest.main()
