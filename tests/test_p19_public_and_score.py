"""P19 original public regression and exact mixed-stage score QA only.

Production source tests were executed on the historical DSPy checkout after
original policy seals; this cannot retroactively become preoracle gate evidence.
"""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/"data/audits"

def r(name):
    return json.loads((A/name).read_text(encoding="utf-8"))

class TestP19PublicAndTaskCounts(unittest.TestCase):
    def test_exact_original_public_runtime_has_no_observed_regressions(self):
        d=r("P19_POSTSEAL_ORIGINAL_PUBLIC_REGRESSION_20261120.json")
        self.assertEqual(d["task"],"stanfordnlp__dspy-1609")
        self.assertEqual(d["source_base"],"16ceaba5f7126ca86e5b50b669975c926b9f8f55")
        self.assertEqual(d["candidate_head"],"2a2938cbd2b616c684768902bdcc0bfc09e7b9a4")
        self.assertTrue(d["never_included_in_preoracle_P9_or_process_v1_decisions"])
        self.assertFalse(d["original_independent_task_oracle"])
        for stage in ("base","candidate"):
            v=d[stage]
            self.assertEqual(v["tests"],51)
            self.assertEqual(v["passed"],51)
            self.assertEqual(v["failed"],0)
            self.assertEqual(v["errors"],0)
            self.assertEqual(v["skipped"],0)
            self.assertEqual(v["exit_code"],0)

    def test_full_task_failure_cannot_be_reclassified_by_public_tests(self):
        d=r("P19_DSPY_INITIAL_ORIGINAL_TASK_ORACLE_20261120.json")
        o=d["original_benchmark_result"]
        self.assertEqual((o["f2p_passed"],o["f2p_total"],o["p2p_failed"]),(0,4,0))
        self.assertFalse(o["official_resolved"])
        self.assertEqual(o["tests_executed"],261)
        self.assertEqual(d["original_visible"]["candidate_passed"],9)
        self.assertFalse(d["model_based_Databricks_optimization_reproducer_executed"])

    def test_recompute_seven_task_original_P9_policy_counts(self):
        d=r("P19_SEVEN_TASK_MIXED_STAGE_NONVACUITY_20261120.json")
        rows=d["unique_task_rows"]
        self.assertEqual(len(rows),7)
        self.assertEqual(len(set(x["task"] for x in rows)),7)
        self.assertEqual(sum(bool(x["truth"]) for x in rows),2)
        for k in ("self_report","local_pass","source_linked"):
            a=[x for x in rows if x["policy"][k]=="ACCEPT"]
            hold=[x for x in rows if x["policy"][k]=="HOLD"]
            self.assertEqual(len(a),d["original_P9_descriptive_policies"][k]["n_accepted"])
            self.assertEqual(len(hold),d["original_P9_descriptive_policies"][k]["n_hold"])
            self.assertEqual(sum(not x["truth"] for x in a),
                             d["original_P9_descriptive_policies"][k]["n_false_accepted"])
            self.assertEqual(sum(bool(x["truth"]) for x in hold),
                             d["original_P9_descriptive_policies"][k]["n_unnecessary_hold"])
        self.assertIsNone(d["original_P9_descriptive_policies"]["source_linked"]["false_accept_fraction_among_accepted"])

    def test_process_v1_is_one_task_only_and_a_false_accept_not_new_truth(self):
        d=r("P19_SEVEN_TASK_MIXED_STAGE_NONVACUITY_20261120.json")
        p=d["forward_process_v1_P19_ONLY"]
        self.assertEqual(p["sample_size"],1)
        self.assertEqual(p["preoracle_accept"],"ACCEPT")
        self.assertFalse(p["original_independent_oracle_success"])
        self.assertTrue(p["original_task_false_accept"])
        self.assertTrue(d["no_P18_postreveal_in_original_sample"])


if __name__=="__main__":
    unittest.main()
