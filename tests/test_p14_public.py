"""P14 postseal public suite safeguards. This is NOT a held-out oracle."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT/"data/audits/P14_MATPLOTLIB_POSTSEAL_PUBLIC_LINES_20261119.json"
RESULTS = ROOT/"data/audits/P14_MATPLOTLIB_TWO_STAGE_RECONCILED_20261119.json"
REGISTER = ROOT/"pilot/matplotlib/P14_PREORACLE_EVALUATION_REGISTER.json"

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


class TestP14PublicRegressions(unittest.TestCase):
    def test_original_public_source_unchanged_for_three_states(self):
        x=read(AUDIT)
        r=read(REGISTER)
        self.assertTrue(x["not_original_hidden_oracle"])
        self.assertTrue(x["excluded_from_frozen_policy_decisions"])
        self.assertTrue(x["same_historical_test_source_for_all_three"])
        self.assertFalse(x["stage2_is_independent_task"])
        self.assertEqual(x["historical_source_base_sha"],r["upstream_base_sha"])
        self.assertEqual(x["candidate_shas"]["stage1"],r["stage1"]["candidate_sha"])
        self.assertEqual(x["candidate_shas"]["stage2"],r["stage2"]["candidate_sha"])

    def test_observed_original_public_passes_and_skips_not_imputed(self):
        x=read(AUDIT)
        for stage in ("base","stage1","stage2"):
            result=x[stage]
            self.assertEqual(result["tests"],42)
            self.assertEqual(result["passed"],30)
            self.assertEqual(result["skipped"],12)
            self.assertEqual(result["failed"],0)
            self.assertEqual(result["errors"],0)
            self.assertEqual(result["exit_code"],0)
            self.assertEqual(result["passed"]+result["skipped"],result["tests"])

    def test_public_tests_do_not_override_failed_hidden_task(self):
        x=read(AUDIT)
        s=read(RESULTS)
        self.assertEqual(x["candidate_shas"]["stage2"],s["stages"][1]["candidate_sha"])
        self.assertEqual(s["stages"][1]["f2p_passed"],0)
        self.assertEqual(s["stages"][1]["f2p_total"],1)
        self.assertFalse(s["stages"][1]["original_task_pass"])
        self.assertEqual(s["transition"],"NEITHER_CANDIDATE_RESOLVES_TASK")
        self.assertEqual(s["task_count_in_this_experiment"],1)

if __name__=="__main__":
    unittest.main()
