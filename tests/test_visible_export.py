"""Synthetic negative tests: withheld benchmark fields must never reach model-visible export."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import export_agent_visible_tasks as x

def fixture():
    chosen=[{"instance_id":f"repo{i}__case-{i}","repo":f"group/repo{i}"} for i in range(10)]
    frame={"selected":chosen}
    rows=[{"instance_id":a["instance_id"],"repo":a["repo"],"base_commit":f"{i:040x}",
           "problem_statement":f"Fix behavior for case {i}",
           "patch":"PRIVATE_GOLD_PATCH","test_patch":"PRIVATE_TEST_PATCH",
           "FAIL_TO_PASS":["PRIVATE_TEST_LABEL"],"PASS_TO_PASS":["PRIVATE_TEST_LABEL"],
           "hint":"WITHHELD_HINT"} for i,a in enumerate(chosen)]
    return frame,rows

class TestVisibleExport(unittest.TestCase):
    def test_exact_allowed_fields(self):
        f,rows=fixture()
        result=x.extract_visible(f,rows)
        self.assertEqual(len(result),10)
        self.assertEqual(set(result[0]),set(x.VISIBLE)|{"problem_sha256"})
        self.assertNotIn("PRIVATE_GOLD_PATCH",json.dumps(result))
        self.assertNotIn("PRIVATE_TEST_PATCH",json.dumps(result))
        self.assertNotIn("WITHHELD_HINT",json.dumps(result))
    def test_hash_correct(self):
        f,r=fixture();out=x.extract_visible(f,r)
        self.assertEqual(out[0]["problem_sha256"],hashlib.sha256(out[0]["problem_statement"].encode()).hexdigest())
    def test_frame_order_preserved(self):
        f,r=fixture();r.reverse()
        out=x.extract_visible(f,r)
        self.assertEqual([t["instance_id"] for t in out],[y["instance_id"] for y in f["selected"]])
    def test_bad_sha_refused(self):
        f,r=fixture();r[0]["base_commit"]="main"
        with self.assertRaises(ValueError):x.extract_visible(f,r)
    def test_repo_mismatch_refused(self):
        f,r=fixture();r[0]["repo"]="wrong/repo"
        with self.assertRaises(ValueError):x.extract_visible(f,r)
    def test_missing_task_refused(self):
        f,r=fixture();r.pop()
        with self.assertRaises(ValueError):x.extract_visible(f,r)
    def test_duplicate_task_refused(self):
        f,r=fixture();r.append(copy.deepcopy(r[0]))
        with self.assertRaises(ValueError):x.extract_visible(f,r)
    def test_missing_problem_refused(self):
        f,r=fixture();r[0]["problem_statement"]=" "
        with self.assertRaises(ValueError):x.extract_visible(f,r)
    def test_wont_overwrite_output(self):
        f,r=fixture()
        with tempfile.TemporaryDirectory() as td:
            o=Path(td)/"visible.jsonl"
            x.save_visible(f,r,o)
            with self.assertRaises(ValueError):x.save_visible(f,r,o)
    def test_no_substitution(self):
        f,r=fixture();f["selected"][0]["instance_id"]="changed"
        with self.assertRaises(ValueError):x.extract_visible(f,r)

if __name__=="__main__":
    unittest.main()
