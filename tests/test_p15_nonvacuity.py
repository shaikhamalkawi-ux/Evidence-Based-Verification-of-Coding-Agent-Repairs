"""P15 five-task nonvacuity ledger checks, NOT independent benchmark reruns.

All five original Docker outcomes and P9 decisions are sourced from prior
independently executed GitHub Actions runs. This posthoc aggregation mixes four
initial and one final after synthetic feedback; no population efficacy claimed.
"""
from __future__ import annotations
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
FILE=ROOT/"data/audits/P15_FIVE_TASK_NONVACUITY_MIXED_STAGE_LEDGER_20261119.json"


def load():
    return json.loads(FILE.read_text(encoding="utf-8"))


def recompute(d):
    rows=d["task_records"]
    if len(rows)!=5 or len({r["task"] for r in rows})!=5:
        raise ValueError("Five distinct original tasks required; no duplicated stages")
    if sum(r["stage"]=="INITIAL" for r in rows)!=4:
        raise ValueError("Mixed-stage limitation must remain declared")
    if sum(r["stage"]=="POST_SYNTHETIC_FEEDBACK_FINAL" for r in rows)!=1:
        raise ValueError("Matplotlib final candidate remains one correlated task")
    for r in rows:
        truth=(r["f2p_total"]>0 and r["f2p_passed"]==r["f2p_total"] and r["p2p_failed"]==0)
        if r["truth"]!=truth or r["tests"]<=0:
            raise ValueError("Bad original oracle truth; test counts must be positive")
        if len(r["head"])!=40 or not r["original_harness_source_url"].startswith("https://github.com/"):
            raise ValueError("Missing source identity")
    obs={}
    for name in ("self_report","local_pass","source_linked"):
        acc=[r for r in rows if r["policy"][name]=="ACCEPT"]
        hold=[r for r in rows if r["policy"][name]=="HOLD"]
        if len(acc)+len(hold)!=len(rows):
            raise ValueError("Invalid policy decision value")
        obs[name]={
          "n_tasks":len(rows),
          "n_accepted":len(acc),
          "n_hold":len(hold),
          "n_correct_accepted":sum(r["truth"] for r in acc),
          "n_false_accepted":sum(not r["truth"] for r in acc),
          "n_unnecessary_hold":sum(r["truth"] for r in hold),
          "false_accept_fraction_among_accepted":f"{sum(not r['truth'] for r in acc)}/{len(acc)}" if acc else None,
          "false_accept_rate_defined":bool(acc),
          "coverage_fraction":f"{len(acc)}/{len(rows)}"
        }
    if obs!=d["policy_descriptive_counts"]:
        raise ValueError("Published policy counts do not match original task rows")
    if sum(r["truth"] for r in rows)!=d["count_passed_oracle"]:
        raise ValueError("True pass count changed")
    if sum(not r["truth"] for r in rows)!=d["count_failed_oracle"]:
        raise ValueError("True failure count changed")
    return obs


class P15NonvacuityTests(unittest.TestCase):
    def test_original_five_case_ledger_consistent(self):
        counts=recompute(load())
        self.assertEqual(counts["self_report"]["n_accepted"],4)
        self.assertEqual(counts["self_report"]["n_false_accepted"],3)
        self.assertEqual(counts["local_pass"]["n_false_accepted"],3)
        self.assertEqual(counts["source_linked"]["n_accepted"],0)
        self.assertEqual(counts["source_linked"]["n_unnecessary_hold"],2)

    def test_zero_accept_risk_undefined_not_zero(self):
        d=load()
        p=d["policy_descriptive_counts"]["source_linked"]
        self.assertEqual(p["coverage_fraction"],"0/5")
        self.assertIsNone(p["false_accept_fraction_among_accepted"])
        self.assertFalse(p["false_accept_rate_defined"])
        self.assertEqual(p["n_correct_accepted"],0)
        self.assertEqual(p["n_false_accepted"],0)

    def test_original_ten_frame_and_p15_not_admitted(self):
        d=load()
        self.assertEqual(d["original_task_count_prespecified"],10)
        self.assertEqual(d["unique_distinct_tasks_with_original_harness_outcome"],5)
        self.assertEqual(d["remaining_without_executed_original_harness"],5)
        self.assertEqual(d["count_passed_oracle"],2)
        self.assertEqual(d["count_failed_oracle"],3)
        self.assertNotIn("pytorch__torchtune-2139",[r["task"] for r in d["task_records"]])
        self.assertTrue(any("mixed-stage" in x.lower() for x in d["comparability_limits"]))

    def test_true_pass_rewrite_detected(self):
        d=load()
        d["task_records"][0]["truth"]=True
        with self.assertRaises(ValueError):
            recompute(d)

    def test_p9_policy_nonvacuity_bypass_detected(self):
        d=load()
        d["task_records"][0]["policy"]["source_linked"]="ACCEPT"
        with self.assertRaises(ValueError):
            recompute(d)

    def test_duplicate_matplotlib_stage_not_double_counted(self):
        d=load()
        d["task_records"].append(d["task_records"][-1].copy())
        with self.assertRaises(ValueError):
            recompute(d)

if __name__=="__main__":
    unittest.main()
