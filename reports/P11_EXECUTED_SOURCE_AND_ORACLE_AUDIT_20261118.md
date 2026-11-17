# 99llm-X1 P11 — Executed Source-Attribution and Oracle-Boundary Audit

**Date:** 18 November 2026 (UTC). **State:** completed *retrospective* audit of two distinct prior datasets, not a new prospective post-feedback efficacy experiment. **MR30 remains frozen.** There was no independent second human coder and none is claimed.

## 1. The scientific distinction

An agent-associated pull request may merge, receive a favorable check, or be revised by a different contributor. None of those three observations alone proves that the agent corrected the developer's identified defect. The required unit of analysis is a pinned sequence: **specific feedback; specific agent actor; exact subsequent commit SHA; exact test or verifiable property; and correct time ordering**. When a genuinely independent, pre-frozen oracle is unavailable, report chronology and scope rather than task-resolution truth.

The naturalistic GitHub cohort and the executable SWE-bench-Live feasibility cohort below must NOT be pooled.

## 2. P10 naturalistic GitHub cohort — full, pre-frozen ten

The original search on 17 November 2026 was the creation-ascending September–October 2026 GitHub pull-request query involving copilot-swe-agent. It returned **60** PRs, of which **33** were authored by the Copilot account. The first **10** author-matching PRs were immutably frozen at [commit 0dfca364](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/commit/0dfca364481605b12c2699296a9f948cb790b095), before their detailed commits/reviews/check-runs were consulted. No case was excluded or substituted due to its outcome.

The source archive spans **5** repositories, **42** PR commits and **129** comment/review events; its latest archived states are **3 merged, 3 closed without merge and 4 open**. The frozen JSON mistakenly states four repositories; its existing erratum fixes this to five **without modifying the frozen original**. The selection is nonrandom and source-clustered.

### Event-level audit: positive and negative attribution cases

| Case | Evidence | Narrowly supported finding |
| --- | --- | --- |
| [Pflanzen.Gericht #48](https://github.com/michasng/Pflanzen.Gericht/pull/48) | Human [explicitly requested Copilot review fixes at 00:35:09Z](https://github.com/michasng/Pflanzen.Gericht/pull/48#issuecomment-5593934426); a Copilot-labeled commit [64e4f8f](https://github.com/michasng/Pflanzen.Gericht/commit/64e4f8f584f6ac069e7722c5b4d323ae0df2d4c7) followed at 00:38:30Z; a named [postpatch verify job](https://github.com/michasng/Pflanzen.Gericht/actions/runs/34295900313/job/102292731484) succeeded at 00:41:26Z. | A documented feedback-to-agent-edit sequence and postpatch check, **not** a same-check failure-to-success recovery. The prior SHA had no comparable failed verify job in the retrieved runs. Review suggestions are not prior failed CI, and complete task truth remains untested independently. |
| [aegis-2 #85](https://github.com/nc-sapiex/aegis-2/pull/85) | Human [NEEDS CHANGES](https://github.com/nc-sapiex/aegis-2/pull/85#issuecomment-5652215802); explicit later correction instruction was to Claude, not Copilot; final [783aaa6 commit](https://github.com/nc-sapiex/aegis-2/commit/783aaa61cd12682e662135c6760914208d3dc289) was labeled as authored by nc-sapiex; nine CI checks succeeded on that SHA. | **Actor-negative control**: the later green checks cannot be assigned to a subsequent Copilot fix. |
| [care_fe #16856](https://github.com/ohcnetwork/care_fe/pull/16856) | Two initial Copilot-labeled commits were followed by eight commits labeled with a different contributor, ending at [667edfe](https://github.com/ohcnetwork/care_fe/commit/667edfecdc7a41524a28107f28242e2660b29a82). | Subsequent edits and status checks reflect mixed ownership; do not infer sole agent completion. |
| [Maslow_4 #1103](https://github.com/MaslowCNC/Maslow_4/pull/1103) | The PR merged, but the inspected [GitHub check-runs API for its final head SHA](https://api.github.com/repos/MaslowCNC/Maslow_4/commits/fd41fd4303fda1f61fb281b526475f878b428e95/check-runs?per_page=100) returned zero checks. | Merge is observed; the queried final commit has no independent CI-verification receipt. |

All **ten**, including the other six without a narrowly certified post-feedback repair event, are retained with their individual statuses in the [machine-readable P11 evidence register](../data/audits/P11_SOURCE_AND_ORACLE_BOUNDARIES_20261118.json). **No uniform independent complete-task oracle exists for this source frame**. That does not mean zero successful real repairs; it means repair-effectiveness prevalence and comparison cannot be estimated from these observations.

## 3. Separate SWE-bench-Live feasibility frame: three completed initial-attempt oracles

In an unrelated, separately registered ten-task feasibility frame, **three initial GPT-6 research-generated candidate patches** were sealed before the withheld oracle and subsequently executed in the original Docker-backed SWE-bench-Live harness on 17 November 2026. The remaining seven prespecified members have **not** been silently imputed or replaced. No candidate underwent scripted corrective feedback or a second corrective agent patch; these results are **INITIAL-ATTEMPT ONLY**.

Official dataset revision: babb27e45e072219195db7a744bbf0d3c1a36e56. Original harness SHA: ad79b850f15e33992e96f03f6e97f05ddf9aa0be.

| Case (link to actual GitHub Actions oracle) | Sealed self-report | Sealed local-test | Sealed source-linked | FAIL_TO_PASS | PASS_TO_PASS failures | Total evaluated tests | Original oracle |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [Kedro](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44159300952) | ACCEPT | ACCEPT | HOLD | 1/1 | **25** | 1,592 | **UNRESOLVED** |
| [Babel](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44161755692) | HOLD | HOLD | HOLD | 8/8 | **0** | 7,272 | **RESOLVED** |
| [Faker](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44166705455) | ACCEPT | ACCEPT | HOLD | 1/1 | **0** | 2,051 | **RESOLVED** |

For **these three initial patches only**, each original evaluator reported a unique parsed nonempty outcome, with exact candidate patch SHA and timestamped prior sealed decision checked in the original CI workflows. The 10,915 total test observations are **test executions**, not 10,915 independent agent tasks. Job-level success alone was **not** used as the oracle label; parsed original FAIL_TO_PASS / PASS_TO_PASS outcomes were.

### Paired decision counts, with no unsupported rates

| Policy | ACCEPT count | HOLD count | False accepts, count | True passes incorrectly held, count |
| --- | ---: | ---: | ---: | ---: |
| Self-report | 2 | 1 | 1 (Kedro) | 1 (Babel) |
| Local-test | 2 | 1 | 1 (Kedro) | 1 (Babel) |
| Source-linked | **0** | **3** | **0** | **2** (Babel, Faker) |

The source-linked policy held **all three** cases, partly because agent ownership was not independently certified for the research-generated commits. Its zero false-accept count is **vacuous**. The false-accept *rate among source-linked accepted tasks is undefined because that denominator is zero*. There is no evidence here that source-linked acceptance is statistically or causally superior. The two unnecessary holds expose its observable conservatism and coverage cost.

## 4. Reproducible evidence and audit scope

The new [Python verifier](../scripts/verify_p11_evidence.py) recomputes all 10 frozen records against archived source JSON, actor/timestamp matching on the documented events, the 42/129 counts, the separate pilot's three pre-oracle decision seals, decision-vs-oracle chronology, and the descriptive decision confusion counts. The [negative-control tests](../tests/test_p11.py) reject altered source counts, altered adjudicated oracle truth, and reassigned human authorship.

This is a **local archive consistency recheck**, not a live reread of GitHub CI during the test, an independently replayed Docker oracle, or cryptographic proof that a GitHub contributor was solely autonomous. The external job receipt URLs remain independently inspectable, and each scientific assertion is scoped to the identified SHA.

## 5. Editorial decision

**KEEP:** source-anchored instruction-to-edit, actor-negative, mixed-author and no-CI counterexamples. **KEEP (separate):** three genuinely executed initial-attempt official benchmark oracles and the predecision policy vector. **HOLD:** inference about population repair prevalence, post-developer-feedback recovery, false-accept rate for a zero-accept policy, and comparative superiority. **REMOVE:** any claim that merge, bot-authored PR login or successful downstream check proves complete agent repair.

A real efficacy study still requires a pre-registered **two-stage post-feedback** experiment on untouched selected tasks, with verifiable agent authorship, the correction request, exact submitted second patch SHA, and the external oracle isolated until after decision sealing. Do not rebrand these three first attempts as repaired-after-feedback tasks. MR30 and the P10 frozen cohort are unchanged.

*P11 record is a scientific continuation within the separate coding-agent verification research repository, not a new journal submission.*
