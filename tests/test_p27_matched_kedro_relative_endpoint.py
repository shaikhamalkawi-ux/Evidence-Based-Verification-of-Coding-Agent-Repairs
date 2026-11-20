"""P27 postreveal matched-source negative-control and alternative endpoint tests."""
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
spec=importlib.util.spec_from_file_location("p27",ROOT/"scripts/p27_relative_endpoint_sensitivity.py")
p27=importlib.util.module_from_spec(spec)
spec.loader.exec_module(p27)

class TestP27KedroExistingNull(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out=p27.compute()
        cls.kedro=json.loads((ROOT/p27.KEDRO).read_text(encoding="utf-8"))

    def test_original_old_matched_control_recovered_exact(self):
        r=self.kedro
        self.assertEqual(r["original_p9_candidate_run_id"],44159300952)
        self.assertEqual(r["prior_postreveal_null_run_id"],44162955737)
        self.assertEqual(r["status"],"COMPLETE_SAME_FAILURE_SET")
        self.assertEqual(len(r["matched_p2p_failed_test_ids"]),25)
        self.assertEqual(r["candidate_only_failed_p2p_test_ids"],[])
        self.assertEqual(r["control_only_failed_p2p_test_ids"],[])
        self.assertTrue(r["original_null_is_original_source_with_comment_only"])

    def test_original_kedro_P9_and_raw_resolved_unchanged(self):
        original=json.loads((ROOT/"pilot/kedro/locked/P9_DECISIONS_SEALED.jsonl").read_text())
        self.assertEqual(original["decisions"],{"self_report":"ACCEPT","local_pass":"ACCEPT","source_linked":"HOLD"})
        self.assertEqual(original["head_sha"],"355ae83abe163ab9bbe2aaf7a59cc055f220d13e")
        r=self.kedro
        self.assertIs(r["original_candidate"]["resolved"],False)
        self.assertIs(r["original_source_comment_only_null"]["resolved"],False)
        self.assertEqual((r["original_candidate"]["f2p_passed"],r["original_source_comment_only_null"]["f2p_passed"]),(1,0))
        self.assertEqual((r["original_candidate"]["p2p_failed"],r["original_source_comment_only_null"]["p2p_failed"]),(25,25))
        self.assertEqual((r["original_candidate"]["tests_executed"],r["original_source_comment_only_null"]["tests_executed"]),(1592,1592))

    def test_different_postreveal_estimand_not_original_truth(self):
        d=self.out
        self.assertEqual(d["study_status"],"POSTREVEAL_SENSITIVITY_DIFFERENT_ESTIMAND_NOT_A_RECLASSIFICATION")
        self.assertTrue(d["original_reported_task_verdicts_unchanged"])
        self.assertTrue(d["P26_original_endpoint_risk_intervals_unchanged"])
        self.assertFalse(d["no_original_model_actor_attestation"] is False)
        self.assertTrue(d["no_task_oracle_reexecution"])
        self.assertTrue(d["no_new_P9_decisions"])
        rows={r["task"]:r for r in d["source_task_rows"]}
        for task in ["kedro-org__kedro-4406","aws-cloudformation__cfn-lint-3779"]:
            self.assertEqual(rows[task]["postrevealed_relative_endpoint"],"PASS_BASELINE_RELATIVE_ONLY")
            self.assertIs(rows[task]["original_official_raw_resolved"],False)

    def test_postreveal_relative_risk_bounds_shrink_without_changing_P26(self):
        p=self.out["policies"]
        self.assertEqual((p["self_report"]["accepted"],p["self_report"]["direct_issue_F2P_fail_accepted"]),(5,2))
        self.assertEqual(p["self_report"]["accepted_relative_failure_fraction_bounds"],["2/5","2/5"])
        self.assertEqual(p["local_pass"]["accepted"],8)
        self.assertEqual(p["local_pass"]["accepted_relative_failure_fraction_bounds"],["1/2","5/8"])
        self.assertEqual((p["local_pass"]["matched_baseline_nonincremental_P2P_accepted"],
                          p["local_pass"]["invalid_endpoint_unknown_accepted"]),(2,1))
        self.assertIsNone(p["source_linked"]["accepted_relative_failure_fraction_bounds"])
        self.assertEqual(self.out["P26_original_endpoint_policy_bounds"]["local_pass"],["1/2","7/8"])
        self.assertEqual(self.out["P26_original_endpoint_policy_bounds"]["self_report"],["2/5","4/5"])

    def test_all_original_ten_selected_unchanged(self):
        frame=json.loads((ROOT/"pilot/frozen_task_frame_20261117.json").read_text())
        self.assertEqual(len(self.out["source_task_rows"]),10)
        self.assertEqual([r["task"] for r in self.out["source_task_rows"]],
                         [r["instance_id"] for r in frame["selected"]])
        self.assertEqual(self.out["candidates_with_original_p9_decisions"],9)

    def test_unmatched_null_cannot_cause_admission(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)
            inputs=[p27.REG,p27.KEDRO,p27.CFN,p27.parent.FRAME,p27.parent.P19,p27.parent.P25,
                    p27.parent.P20,p27.parent.P21,p27.parent.P23,p27.parent.P25NULL,p27.parent.PROTOCOL]
            for rel in inputs:
                target=out/rel
                target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(ROOT/rel,target)
            file=out/p27.KEDRO
            obj=json.loads(file.read_text())
            obj["matched_p2p_failed_test_ids"]=obj["matched_p2p_failed_test_ids"][:-1]
            file.write_text(json.dumps(obj)+"\n")
            with self.assertRaises(AssertionError):
                p27.compute(out)


if __name__=="__main__":
    unittest.main()
