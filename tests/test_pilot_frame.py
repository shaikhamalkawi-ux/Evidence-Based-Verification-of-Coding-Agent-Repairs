"""Negative controls for prospective task-ID selection. Synthetic metadata only."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import select_pilot_frame as sp

SHA = "0" * 40

def rows(k=12):
    return [{"instance_id": "repo" + str(i) + "__case-" + str(i), "repo": "org/repo" + str(i)}
            for i in range(k)]

class TestPilotSelector(unittest.TestCase):
    def test_selection_is_deterministic(self):
        a = sp.select(rows(), SHA, n=5)
        b = sp.select(list(reversed(rows())), SHA, n=5)
        self.assertEqual(a["selected"], b["selected"])
        self.assertEqual(a["n_selected"], 5)

    def test_previously_exposed_calibration_excluded(self):
        r = rows() + [{"instance_id": "amoffat__sh-744", "repo": "amoffat/sh"}]
        s = sp.select(r, SHA)
        self.assertNotIn("amoffat__sh-744", [x["instance_id"] for x in s["selected"]])

    def test_hidden_oracle_field_refused(self):
        bad = rows()
        bad[0]["FAIL_TO_PASS"] = ["hidden"]
        with self.assertRaises(ValueError):
            sp.select(bad, SHA)

    def test_reference_patch_refused(self):
        bad = rows()
        bad[0]["patch"] = "not permitted"
        with self.assertRaises(ValueError):
            sp.select(bad, SHA)

    def test_duplicate_tasks_refused(self):
        with self.assertRaises(ValueError):
            sp.select(rows() + [rows()[0]], SHA)

    def test_dataset_revision_required(self):
        with self.assertRaises(ValueError):
            sp.select(rows(), "main")

    def test_distinct_repos_required(self):
        d = [{"instance_id": "task-" + str(i), "repo": "one/repo"} for i in range(12)]
        with self.assertRaises(ValueError):
            sp.select(d, SHA)

    def test_does_not_replace_short_frame(self):
        with self.assertRaises(ValueError):
            sp.select(rows(4), SHA, 10)

    def test_frozen_output_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as t:
            base = Path(t)
            inp, out = base / "input.jsonl", base / "frame.json"
            inp.write_text("".join(json.dumps(x) + "\n" for x in rows()), encoding="utf-8")
            result = sp.run(inp, SHA, out)
            self.assertEqual(result["n_selected"], 10)
            with self.assertRaises(ValueError):
                sp.run(inp, SHA, out)
            self.assertTrue(result["source_metadata_sha256"])

if __name__ == "__main__":
    unittest.main()
