"""P29 immutable-source original stdout / node-ID parser and tampering tests."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
from unittest.mock import patch

SCRIPT=Path(__file__).resolve().parents[1]/"scripts/p29_full_pytest_id_audit.py"
spec=importlib.util.spec_from_file_location("p29_raw",SCRIPT)
p29=importlib.util.module_from_spec(spec)
spec.loader.exec_module(p29)

class P29RawNameControls(unittest.TestCase):
    def test_spaces_preserved_in_parameterized_names(self):
        a,b=p29.parse_full_pytest_summary(b"PASSED tests/x.py::a[No-1, 2, 3]\nFAILED tests/x.py::a[Yes-1, 2, 3]\n")
        self.assertEqual(a,{"tests/x.py::a[No-1, 2, 3]"})
        self.assertEqual(b,{"tests/x.py::a[Yes-1, 2, 3]"})
    def test_unbalanced_id_rejected(self):
        with self.assertRaises(AssertionError):
            p29.parse_full_pytest_summary(b"PASSED test/x.py::a\nFAILED test/x.py::b[No-1,\n")
    def test_false_application_error_not_test_failure(self):
        a,b=p29.parse_full_pytest_summary(b"ERROR    root:file.py:1 fail\nSKIPPED [1] x.py\nPASSED test/x.py::a\nFAILED test/x.py::b\n")
        self.assertEqual(len(a),1);self.assertEqual(len(b),1)
    def test_duplicate_test_rejected(self):
        with self.assertRaises(AssertionError):
            p29.parse_full_pytest_summary(b"PASSED test/x.py::a\nPASSED test/x.py::a\nFAILED test/x.py::b\n")
    def test_conflicting_status_rejected(self):
        with self.assertRaises(AssertionError):
            p29.parse_full_pytest_summary(b"PASSED test/x.py::a\nFAILED test/x.py::a\n")
    def test_empty_failed_rejected(self):
        with self.assertRaises(AssertionError):
            p29.parse_full_pytest_summary(b"PASSED test/x.py::a\n")
    def test_parser_truncation_counter(self):
        self.assertEqual(p29.count_parser_truncation(["t[A","t[B]","t[C"]),2)
    def test_set_digest_sorted_invariant(self):
        self.assertEqual(p29.set_digest(["a","b"]),p29.set_digest(["b","a"]))
    def test_original_status_duplicate_rejected(self):
        data={"task":{"resolved":False,"tests_status":{"FAIL_TO_PASS":{"success":["a"],"failure":[]},"PASS_TO_PASS":{"success":[],"failure":["b","b"]}}}}
        with self.assertRaises(AssertionError):
            p29.parse_official(json.dumps(data).encode(),"task")
    def test_other_original_task_rejected(self):
        with self.assertRaises(AssertionError):
            p29.parse_official(b'{"other":{}}',"task")
    def test_zip_member_in_scope(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"arch.zip"
            with zipfile.ZipFile(p,"w") as z:z.writestr("file","hello")
            self.assertEqual(p29.load_bytes(p,"file"),b"hello")
    def test_original_run_ids_unmodified(self):
        self.assertEqual(p29.CASES["kedro"]["candidate_run"],44159300952)
        self.assertEqual(p29.CASES["cfn_lint"]["control_run"],44761416230)
    def test_corrupted_original_log_fails(self):
        with patch.object(p29,"load_bytes",return_value=b"INTENTIONAL-REPLACEMENT"):
            with self.assertRaises(AssertionError):p29.audit_pair("kedro","none","none")

if __name__=="__main__":unittest.main()
