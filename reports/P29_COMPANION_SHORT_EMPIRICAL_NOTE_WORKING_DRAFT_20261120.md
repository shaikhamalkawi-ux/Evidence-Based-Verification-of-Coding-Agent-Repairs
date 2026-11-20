# From Benchmark Verdicts to Evidence-Admissible Repair Claims: A Source-Locked SWE-bench-Live Case Series
**P29 UPDATED WORKING SHORT-NOTE DRAFT — NOT A FULL JOURNAL MANUSCRIPT; NOT SUBMITTED; NO AUTHOR APPROVAL CLAIMED**

## Abstract
Test-graded coding-agent evaluations frequently treat a binary benchmark verdict as evidence about whether a proposed patch fixed an issue. The inference is not automatic when the evaluation environment cannot execute a valid oracle or when regression-test failures occur without the candidate's edit. We present a retrospective, source-locked case series of ten originally SHA-selected SWE-bench-Live lite tasks. Nine tasks yielded source candidates with original pre-oracle acceptance decisions; the tenth had no candidate and is not imputed as a failure. Among nine original benchmark reports, two were marked resolved and seven unresolved. We distinguish two original issue-specific test passes, four executed issue-specific test failures, and three unadmitted or attribution-uncertain endpoints. For two unresolved cases, Kedro #4406 and cfn-lint #3779, previously executed, post-reveal matched original-source no-behavior-change controls failed exactly the same 25 and four named PASS_TO_PASS tests, respectively, as their issue-specific-test-passing candidates, with no candidate-exclusive P2P failure names. A new replay of four original text logs, preserving spaces in full pytest node names, finds 87 candidate FAILED names within 88 control FAILED names for Kedro, and seven within eight for cfn-lint, with zero candidate-only raw FAILED names in each pair; the one control-only name is the issue-specific F2P. Three of Kedro's 25 scored P2P keys are parser-truncated, so the raw-name audit is needed to substantiate complete-name concordance. These observations show that the source patches were not necessary for the named failures in the paired executions, but do not establish overall program correctness or reverse original strict benchmark scores. Under the original endpoint-admission question, sharp finite-case accepted-failure bounds are 40–80% for self-report (5/9 accepted) and 50–87.5% for local-test success (8/9 accepted). A separate, explicitly posthoc baseline-relative test-adequacy endpoint produces 40% and 50–62.5%, respectively; these are different estimands, not tightened confidence intervals. A source-linked actor gate accepted zero candidates and has undefined accepted risk. The contribution is a small, reproducible evidence-interpretation example—not a new risk–coverage algorithm, correctness oracle, representative agent benchmark, or causal policy evaluation. Strong prior work and dated October–November 2026 SWE-bench-Live technical diagnostics, including Kedro #4406 itself, already identify related test-oracle defects, sharply limiting novelty claims.

**Keywords:** Coding agents; SWE-bench-Live; negative control; test adequacy; failure attribution; partial identification; source provenance; measurement validity.

## 1. Introduction and research questions
Software-repair benchmarks commonly require an issue-specific FAIL_TO_PASS (F2P) test suite and unchanged PASS_TO_PASS (P2P) regression tests. A candidate can pass the issue-specific F2P tests yet fail a strict full-benchmark status, for reasons that include newly introduced regressions, failures already present with the old source under the executed environment, or incomplete test execution. These cases are not interchangeable as evidence about a candidate's source changes.

Prior research has established software-repair patch overfitting, incomplete acceptance tests, SWE-bench validation weaknesses, and harness defects [1–8]. An October 2026 public SWE-bench-Live diagnostic also reported related environment failures, including privacyidea-4251, the same task as one studied here [9]. We therefore do **not** claim priority for discovering such defects.

Three descriptive questions guide this case series:
- **RQ1** Which original task outcomes support a bounded issue-test claim, and which require an endpoint or source-attribution HOLD?
- **RQ2** In the available source-original no-behavior-change comparisons, do candidate P2P failure identifiers also occur without the candidate patch?
- **RQ3** What finite-case conditional accepted-failure bounds are logically consistent with the original locked acceptance decisions under two **different** task-test endpoint contracts?

## 2. Methods and evidence admission
The pre-existing study frame contains ten SHA-selected SWE-bench-Live lite tasks. Nine source candidate/decision records have a P9 policy decision sealed before their original independent task benchmark test, using a fixed original dataset revision `babb27e45e072219195db7a744bbf0d3c1a36e56` and original harness commit `ad79b850f15e33992e96f03f6e97f05ddf9aa0be`. Reflex #4510 had no patch or original task oracle. The unit of analysis is the unique task, not the number of test nodes, script executions or revised candidate stages. One Matplotlib candidate was examined after scripted AI-style corrective feedback, and cfn-lint used a second visible source candidate; this is a **heterogeneous retrospective case series**, not a homogeneous first-attempt efficacy experiment.

The original strict benchmark endpoint remains unchanged: all expected F2P and P2P tests must pass for RESOLVED. The **P26 source-admission partition**, devised after seeing outcomes, marks an original task-test PASS only if the original independent oracle executed all F2P successfully with zero failed P2P; it identifies a direct issue-test FAIL if a valid F2P did not pass; and otherwise marks UNKNOWN if P2P attribution is unsupported or an original missing fixture invalidates code-level interpretation. This intentionally does not equate every raw unresolved label with source-code failure.

For the two originally unresolved cases in RQ2, source-original neutral controls were run only after the candidate results were visible. Kedro's historical neutral run on 17 November 2026 was later recovered from GitHub Actions artifacts. The controls preserve the original executable source and alter only an inert Python comment (Kedro) or Markdown comment (cfn-lint). We compare exact named P2P failure identifiers under the paired candidate and control executions. Same failure names show the patch is not *necessary* for those observed test failures; they do not identify their unique causes, guarantee absence of side effects, or prove robustness across times/environments.

For any original acceptance policy `p`, let `A_p` be its accepted candidate tasks, `F_p` those with admitted direct F2P failure, and `U_p` those with unknown original full-task status or attribution. For nonempty `A_p`, the **P26 question** has finite-frame logical bounds
`|F_p|/|A_p| <= Risk_p <= (|F_p|+|U_p|)/|A_p|`,
conditional on the explicit classification and free completion of the unknown states. These are descriptive sharp bounds, *not* confidence intervals or general-population guarantees. The accepted risk is undefined if `|A_p|=0`.

The **P27 posthoc alternative endpoint** asks only whether all original F2P pass and no candidate-exclusive failed P2P names remain relative to a matched original-source control; it is a narrower test-adequacy condition, NOT the original benchmark's RESOLVED outcome. The same fraction formula is applied to this **different** endpoint, with privacyIDEA still unknown. P26 results are left intact.

## 3. Results
### 3.1 The original ten selected cases
| Frozen task | Raw original outcome | P26 admitted status | P27 *different* relative test status |
|---|---|---|---|
| kedro-org__kedro-4406 | UNRESOLVED | UNKNOWN, P2P attribution | PASS relative only |
| pdm-project__pdm-3419 | UNRESOLVED | FAIL original F2P | FAIL original F2P |
| matplotlib__matplotlib-28933 | UNRESOLVED | FAIL original F2P | FAIL original F2P |
| python-babel__babel-1163 | RESOLVED | PASS original oracle | PASS original oracle |
| pytorch__torchtune-2139 | UNRESOLVED | FAIL original F2P | FAIL original F2P |
| stanfordnlp__dspy-1609 | UNRESOLVED | FAIL original F2P | FAIL original F2P |
| privacyidea__privacyidea-4251 | UNRESOLVED | UNKNOWN, missing test import | UNKNOWN, missing import |
| joke2k__faker-2155 | RESOLVED | PASS original oracle | PASS original oracle |
| reflex-dev__reflex-4510 | NO CANDIDATE | OUTSIDE 9-task decision denominator | OUTSIDE |
| aws-cloudformation__cfn-lint-3779 | UNRESOLVED | UNKNOWN, P2P baseline attribution | PASS relative only |

### 3.2 Original-source controls
| Task | Candidate F2P | Neutral source F2P | Failed P2P names shared | Candidate-only failed P2P names |
|---|---:|---:|---:|---:|
| Kedro #4406 | 1/1 | 0/1 | 25/25 | 0 |
| cfn-lint #3779 | 1/1 | 0/1 | 4/4 | 0 |

Both original candidate scores remain UNRESOLVED by the stipulated strict benchmark rule. We make no assertion that the 29 shared failures have independent causes; there are only two paired task comparisons.

### 3.3 P29 raw full pytest-ID cross-check (read-only retrospective source recovery)
The original GitHub Actions artifacts from **Kedro #4406** (candidate run 44159300952; original-source neutral run 44162955737) and **cfn-lint #3779** (candidate run 44738711010; neutral run 44761416230) were downloaded and verified by SHA-256. An independent standard-library parser extracted only complete `FAILED` and `PASSED` pytest result names from the archived original text summaries. It did not infer a test status from Kedro application error-logging messages.

| Historical task | Raw FAILED full names, candidate | Raw FAILED full names, neutral | Shared full FAILED names | Candidate-only FAILED full names | Control-only FAILED full names |
|---|---:|---:|---:|---:|---:|
| Kedro #4406 | 87 | 88 | 87 | **0** | **1 (issue F2P)** |
| cfn-lint #3779 | 7 | 8 | 7 | **0** | **1 (issue F2P)** |

The original benchmark P2P outcome stays **25/25** matched parsed failed keys for Kedro and **4/4** for cfn-lint, with each original candidate officially **UNRESOLVED**. Three of Kedro's 25 official parsed P2P failure keys truncate parametrized pytest IDs at spaces. Full raw test identifiers establish the narrower claim that *none of the raw FAILED names in the candidate trace is absent from its original-source neutral trace*. These raw 87 and seven failed tests are **not** a newly sampled 94-task experiment, not independent replicate units, and not the official scored P2P denominators.

Our interpretation must also acknowledge the dated upstream prior evidence: SWE-bench-Live [issue #113](https://github.com/microsoft/SWE-bench-Live/issues/113), filed **11 November 2026**, reports the **same Kedro #4406** and 25 P2P failures when executing the *gold patch* under the stated 2026 environment. It explicitly says the 3 November dataset revision fixed some sibling tasks but not this one. This is not our original-source control or the same harness SHA, and its full claimed causal explanation is not independently reproduced here. SWE-bench-Live [issue #102](https://github.com/microsoft/SWE-bench-Live/issues/102) had already diagnosed whitespace truncation of parametrized pytest IDs on 23 October. The broader five-dimensional patch correctness evidence framework of Wu et al. (arXiv:2611.10837, 7 November 2026) is additional close methodological prior work.

### 3.4 Conditional accepted-failure bounds
| Policy | P9 ACCEPT / 9 | P26 original admitted failure bound | P27 different posthoc relative test bound |
|---|---:|---:|---:|
| Self-report | 5/9 | 40–80% | 40% |
| Visible local-test pass | 8/9 | 50–87.5% | 50–62.5% |
| Source-linked actor evidence | 0/9 | undefined | undefined |

An original task success was held by both self-report and local-test success; the strict gate held both successes, so conclusions must include lost acceptance coverage as well as false-accept uncertainty. The strict gate cannot be called superior because it accepted no task.

## 4. Discussion
**The main evidence distinction:** a test outcome, the ability to attribute a failed test to a source patch, and the identity of the agent that authored the patch are separate claims. In two reported task pairs, the exact failed P2P names occur with the original executable source. This rebuts a claim that those particular P2P failures require the candidate edit, not a claim that the official strict benchmark scoring code is false or invalid per its stated rules.

**Novelty boundary:** In addition to an exact-instance upstream technical report predating our Kedro audit, a 7 November 2026 five-dimensional evidence profile [13] covers substantially overlapping general methodology. Earlier program-repair studies already demonstrate overfitting [1–3]; code-agent studies audit benchmark and patch-test validity [4–8]; a dated upstream SWE-bench-Live issue [9] discusses near-identical environment problem classes, including the same privacyIDEA task. Manski's partial-identification logic [10] and Geifman–El-Yaniv selective risk–coverage framing [11] are prior art. The contribution here is no more than a narrowly reproducible source-to-claim ledger and two matched task-specific negative-control counterexamples combined with finite-case endpoint sensitivity.

**Threats to validity:** Historical Kedro and cfn-lint full pytest names are sensitive to original log formatting, though raw SHA-256/uniqueness checks and corrupted-ID controls were passed. Very small selected sample; mixed candidate stages and scripted assistance rather than independently authenticated agent rollouts; post-reveal selection of controls; time gap between Kedro candidate and control; possible grader/test changes not eliminated by exact test-name matching; unobserved full-program behavior; and privacyIDEA invalid import. There is no randomization, independent human reference coding, calibrated model evaluation, model comparison, population estimate, or causal effect.

## 5. Conclusion and next empirical gate
A frozen strict benchmark verdict does not uniquely tell us whether an agent's source edit introduced a regression, and post-reveal matched original-source runs can demonstrate counterexamples to that attribution. In nine decisions with mixed evidence completeness, finite-case accepted-failure bounds describe uncertainty more accurately than assigning all unresolved outcomes as failed repairs. This case series is useful as a transparent reproducibility note; it is **not yet sufficient for a full-length generalizable methods paper**. The next defensible step, if a stronger paper is desired, is a genuinely prospective, pre-specified and actor-attested replication using a fresh frame, independent exact source/patch provenance, and prespecified original-source negative controls.

## Selected verified references (short-note working list; NOT final submission bibliography)
1. Smith et al. (2015), *Is the Cure Worse Than the Disease?* FSE. https://doi.org/10.1145/2786805.2786825
2. Zemín et al. (2025), *An Empirical Study on the Suitability of Test-based Patch Acceptance Criteria*. TOSEM. https://doi.org/10.1145/3702971
3. Wang, Pradel, Liu (2026), *Are “Solved Issues” in SWE-bench Really Solved Correctly?* ICSE. https://doi.org/10.1145/3744916.3764576
4. Aleithan et al. (2024), *SWE-Bench+*. https://arxiv.org/abs/2410.06992
5. Zhang et al. (2025), *SWE-bench Goes Live!*. https://arxiv.org/abs/2505.23419
6. OpenAI (2026-02-23), *Why SWE-bench Verified No Longer Measures Frontier Coding Capabilities*. https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/
7. OpenAI (2026-07-08), *Separating Signal from Noise in Coding Evaluations*. https://openai.com/index/separating-signal-from-noise-coding-evaluations/
8. Chen (2026), *When Agent Evaluation Becomes Unreliable*. https://arxiv.org/abs/2610.16067
9. mz24cn (2026-10-23), *Gold-patch validity gate*, microsoft/SWE-bench-Live issue #100 (public unreviewed technical report). https://github.com/microsoft/SWE-bench-Live/issues/100
10. Manski (2005), *Partial identification with missing data: concepts and findings*. https://doi.org/10.1016/j.ijar.2004.10.006
11. Geifman and El-Yaniv (2017), *Selective Classification for Deep Neural Networks*. https://papers.neurips.cc/paper_files/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html
12. Ding (2026), *What the Specification Did Not Say*. https://arxiv.org/abs/2610.30635

13. Wu et al. (7 Nov 2026), *Patch Correctness in Automated Program Repair: A Five-Dimensional Evidence Framework.* https://arxiv.org/abs/2611.10837
14. mz24cn (11 Nov 2026), *Remaining Evaluation-Environment Issues Where the Gold Patch Fails*, SWE-bench-Live issue #113 (unreviewed upstream technical report). https://github.com/microsoft/SWE-bench-Live/issues/113
15. mz24cn (23 Oct 2026), *Whitespace Truncation of Parametrized Pytest IDs*, SWE-bench-Live issue #102 (unreviewed). https://github.com/microsoft/SWE-bench-Live/issues/102

**Draft QA status:** citations are a verified starter list, **not an exhaustive systematic review nor the 26+ cited journal submission reference audit**. No claim of publication readiness.
