"""P22 source eligibility and env dependency diagnostic conformance, no oracle."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/"data/audits"

def load(name):
    return json.loads((AUDIT/name).read_text(encoding="utf-8"))


class P22OriginalEligibility(unittest.TestCase):
    def test_same_original_frozen_ninth_task(self):
        frame=json.loads((ROOT/"pilot/frozen_task_frame_20261117.json").read_text())
        self.assertEqual(len(frame["selected"]),10)
        self.assertEqual(frame["selected"][8]["instance_id"],"reflex-dev__reflex-4510")
        self.assertEqual(frame["selected"][8]["repo"],"reflex-dev/reflex")
        reg=json.loads((ROOT/"protocol/P22_REFLEX_ORIGINAL_FIELD_FOREACH_PREPATCH_20261120.json").read_text())
        self.assertEqual(reg["base_sha"],"2520c51aaf4c0a4af965026ae3a3fd5b03930288")
        self.assertTrue(reg["no_reference_solution_or_test_patch_access"])

    def test_unpinned_three_python_original_import_error_is_not_reported_bug(self):
        a=load("P22_REFLEX_THREE_PYTHON_VISIBLE_SOURCE_COMPARISON_20261120.json")
        self.assertEqual(len(a["observations"]),3)
        self.assertEqual({x["python"].split(".")[1] for x in a["observations"]},{"11","12","13"})
        self.assertTrue(all(x["install_exit"]==0 for x in a["observations"]))
        self.assertTrue(all(x["exception_type"]=="RuntimeError" for x in a["observations"]))
        self.assertTrue(all(x["exception_message"]=="generator didn't stop after throw()" for x in a["observations"]))
        self.assertFalse(a["original_reported_typing_any_error_reproduced"])
        self.assertEqual(a["task_truth_eligibility"],"VISIBLE_REPRO_MISMATCH_HOLD")

    def test_nested_exception_is_import_compatibility_problem(self):
        a=load("P22B_REFLEX_ORIGINAL_EXCEPTION_CHAIN_20261120.json")
        self.assertEqual([x["type"] for x in a["exception_chain"]],["RuntimeError","ImportError"])
        self.assertIn("Discriminator",a["exception_chain"][1]["message"])
        self.assertIn("pydantic.v1",a["exception_chain"][1]["message"])
        self.assertFalse(a["benchmark_oracle_used"])
        self.assertFalse(a["source_modified"])

    def test_vintage_sqlmodel_pins_not_a_new_repair(self):
        a=load("P22C_REFLEX_VINTAGE_DEPENDENCY_COMPARISON_20261120.json")
        self.assertEqual({x["pin"] for x in a["controlled_vintage_dependency_experiments"]},
                         {"sqlmodel==0.0.14","sqlmodel==0.0.22"})
        self.assertTrue(all(x["source_install_success"] and x["pin_install_success"]
                            for x in a["controlled_vintage_dependency_experiments"]))
        self.assertTrue(all(not x["user_supplied_reproducer_exception"]
                            for x in a["controlled_vintage_dependency_experiments"]))
        self.assertFalse(a["model_candidate_submitted"])
        self.assertFalse(a["benchmark_oracle_accessed"])
        self.assertEqual(a["determination"],"P22_PREPATCH_SOURCE_OUTCOME_DEPENDENCY_CONTINGENT_HOLD")

    def test_claim_limits_do_not_create_task_outcome(self):
        a=load("P22C_REFLEX_VINTAGE_DEPENDENCY_COMPARISON_20261120.json")
        self.assertFalse(a["source_substitution"])
        self.assertFalse(a["model_candidate_submitted"])
        self.assertFalse(a["benchmark_oracle_accessed"])
        self.assertIn("Neither",a["claim_boundary"])

if __name__=="__main__":
    unittest.main()
