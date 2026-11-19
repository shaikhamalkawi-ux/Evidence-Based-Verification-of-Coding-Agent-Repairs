# 99llm-X1 P14 — Matplotlib Two-Stage Synthetic Feedback and Exact-Patch Task Oracle

**Dated:** 19 November 2026 (UTC). **Status:** Executed and source-reconciled **negative** benchmark task result. ONE frozen task with TWO correlated candidate revisions; no human developer/coder and no independently attested agent identity. MR30, P10, P11, P12 and P13 remain unchanged.

## Executive finding

A GPT-6-generated Matplotlib AxLine source repair improved from **5/6 to 6/6** originally frozen visible checks after one AI-written, developer-style correction responding to an observed test failure. **Neither patch solved the independent SWE-bench-Live task.** The original pinned evaluator ran **8,228 tests per stage** and found **0/1 FAIL_TO_PASS success, 0 PASS_TO_PASS failures**, and **UNRESOLVED** for each. The 8,228 tests are internal to one task, not 8,228 independent instances.

After sealing the decisions, an unmodified original Matplotlib public test suite passed **30 tests and skipped 12** on the original base, first patch and second patch alike. Thus the local/visible recovery and lack of detected public regressions **did not suffice for issue resolution**.

## Original registration, source and chronology

| Grounded field | Exact historical value |
| --- | --- |
| Task | matplotlib__matplotlib-28933, index 3 of ten originally frozen tasks |
| Source | matplotlib/matplotlib commit cf84d9a6410dec07f57916905c9f54bf00d22b2e |
| Source file / Git blob | lib/matplotlib/lines.py / 9629a821368cc66ddf98f31371ef7c0672642ead |
| Requested behavior | AxLine.set_xy1 and AxLine.set_xy2 accept xy coordinate pairs, including Artist.set(xy1=..., xy2=...) |
| Original benchmark | SWE-bench-Live lite, revision babb27e45e072219195db7a744bbf0d3c1a36e56 |
| Original harness | microsoft/SWE-bench-Live, commit ad79b850f15e33992e96f03f6e97f05ddf9aa0be |
| Original six visible tests SHA-256 | d3767954e5018d2c7fde871fcce2d6850e48e0529224713666e08c918a14ded0 |
| Stage 1 candidate | ad65fe2531ce297d5770257370b469b80731a614 |
| Stage 1 patch SHA-256 | 38d8adc4b7de66735b1318afde6e6e38b0b1bd3f6508157634f11407d7ce6050 |
| Stage 2 candidate | 1c9cb477367e56439fc71e08a4da0661cd105843 |
| Stage 2 full patch SHA-256 | f29d98f8cfe6ef1cf29a9852ce02f3af7fd03e48171ca627a411813dab2c5512 |
| Two decisions sealed at UTC | 2026-11-19T19:00:29Z |
| Decisions SHA-256 | 9ad19413cc0a447464759bafc5786f6b63b179393c429d61dc69b5290ea7496a |
| Public immutable seal commit | 3aced6a089fa27e7802e8220404afb2ab9f21e28 |
| Original hidden oracle executions began | 2026-11-19T19:05:15Z, strictly after seal |

All six visible tests were specified before the first code patch and cover single-pair positional setters, old two-scalar setters, batch Artist property setting, named xy keyword calls, slope/xy2 exclusivity and actual Agg rendering.

The initial candidate made y optional but retained the parameter name x, resulting in **5/6** passing. The one authentic remaining visible failure was the named xy keyword argument. One scripted **AI-generated** feedback message explicitly targeted that failure. The second patch changed the parameter to xy while preserving backward compatibility, passing **6/6**. The original historical base passed **1/6**.

The Git author used for deterministic candidate SHAs is synthetic: it is not independent autonomous-agent attestation. No real human developer feedback and no human coder/intercoder stage occurred. No original hidden test or gold patch was consulted to generate either candidate.

Original visible records: [stage 1 execution](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44592478321); [stage 2 execution](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44593154169). A failed build attempt [44592112859](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44592112859) was an infrastructure error (ephemeral editable-build header paths), not a code-test result. The runner was repaired by keeping NumPy/pybind11 headers in the persistent build environment, without changing source or tests.

## Original task oracle: independently executed on BOTH exact submitted patches

| Outcome | Stage 1 before feedback | Stage 2 after synthetic feedback |
| --- | ---: | ---: |
| Frozen visible tests passed | 5/6 | 6/6 |
| Original task FAIL_TO_PASS successes | **0/1** | **0/1** |
| Original task PASS_TO_PASS failures | **0** | **0** |
| Original tests parsed | **8,228** | **8,228** |
| Unique parsed original reports | 1 | 1 |
| Original resolved flag | **false** | **false** |
| Original evaluator task errors | 0 | 0 |

Both Docker runner stages, exact patch checks and source outputs: [P14 original two-stage GitHub Actions run 44594455715](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44594455715). Original test output SHA-256 stage1: 243fc0eb19b90f0549a6d15b23f69a4a6cddeb821b1a0cb52780dfb43f32a440. Stage2: e0ef2ae29371a844007704535a7adbc2534cc849aa4e57839919a12c6cdcb3e1. GitHub Actions artifacts stage1 14564494382, stage2 14566665436.

These are **two evaluations of one task**, not independent samples. Both are UNRESOLVED. Absence of P2P regressions is not evidence of task correctness.

## Three original P9 policies: no change after outcomes

| Frozen original P9 rule | Stage 1 pre-oracle | Stage 2 pre-oracle | Stage 2 task truth |
| --- | --- | --- | --- |
| Self-report | HOLD | **ACCEPT** | FAIL, false acceptance |
| Visible local pass | HOLD | **ACCEPT** | FAIL, false acceptance |
| Source-, SHA-, scope- and actor-linked | HOLD | HOLD | FAIL, conservative hold |

All decisions were committed before original hidden-data access. The P9 code remains X1-P9-alpha-1-20261116. The strict rule held because **independent agent-author attestation was unavailable**. Therefore its observed count of zero false acceptances is vacuous: **zero accepted means the false-accept rate among accepted is undefined**, not 0%. The strict policy did not demonstrate discovery of the actual hidden issue or comparative superiority.

Source-locked machine evidence: [two original task receipts](../data/audits/P14_MATPLOTLIB_TWO_STAGE_ORIGINAL_ORACLE_20261119.jsonl) and [independently reproduced original P9 score](../data/audits/P14_MATPLOTLIB_TWO_STAGE_RECONCILED_20261119.json). Exact stage-source and oracle admissions were recomputed in [reconciliation GitHub Actions 44596442022](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44596442022), including **66/66 software and tamper-control tests passing**. The [reconciler](../scripts/p14_two_stage_reconcile.py) refuses swapped patch SHAs, human/agent misattribution, zero-test admissions and contradictory original-task labels.

## Original Matplotlib public regression tests — POSTSEAL only

| Matplotlib historical test_lines.py source | Executed/passed | Skipped | Failed |
| --- | ---: | ---: | ---: |
| Original base | 30/30 | 12 | 0 |
| Stage 1 | 30/30 | 12 | 0 |
| Stage 2 | 30/30 | 12 | 0 |

[Original historical public-source tests run 44596318868](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44596318868), plus [machine-readable evidence](../data/audits/P14_MATPLOTLIB_POSTSEAL_PUBLIC_LINES_20261119.json). A preliminary run 44595858417 encountered a pyparsing deprecation warning promoted to collection error on **all three source states**. The same original source tests then executed after adding only a narrow warning filter in the runner; **not** after editing the source, visible suite or frozen decisions. The 12 skipped tests are not counted as passes.

This three-way comparison is the main evidence-sufficiency result: **6/6 visible targeted checks on the corrected patch; 30/30 executed public regression tests with 12 skips; yet 0/1 original independently held-out issue test**. It is not an original regression-testing algorithm or proof that all public behavior is preserved.

## Scientific interpretation and editorial judgment

**KEEP:** a reproducible negative task-correctness case with exact source SHAs, genuine visible failure, explicit AI-generated feedback, exact decision-before-oracle chronology, independently executed original task checks, postseal public regression contrast, and self-report/local false-accept examples.

**HOLD:** any general conclusion that synthetic developer feedback improves or degrades agents, any causal source-linked policy superiority claim, any genuine human coding/review claim, and any model-wide prevalence estimate. The two correlated stages remain **one** task; the original ten-task frozen benchmark has now **five distinct tasks with executable original oracle evidence**, leaving five still unexecuted. P10's naturalistic Copilot PR cases have a separate source-only denominator.

The mechanism responsible for the unchanged original FAIL_TO_PASS failure is **unidentified from the aggregate original test counts alone**. Do not invent its exact line or infer an additional hidden assertion. A later diagnostic on the exposed Matplotlib task would be **post-reveal** and must not retroactively alter these original results.

**Next preregistered sample-order target:** pytorch__torchtune-2139, pending a source/resource feasibility check rather than replacement by an easier task. Do not modify the frozen MR30 manuscript or earlier experimental versions based on an inflated effect claim.

## Files and reproducibility retention

- [P14 original preregistration](../pilot/matplotlib/P14_PREREGISTRATION_20261119.json)
- [Six original visible checks](../pilot/matplotlib/visible_tests.py)
- [Scripted correction provenance](../pilot/matplotlib/P14_SCRIPTED_FEEDBACK_AFTER_FIRST.json)
- [Public preoracle seal](../pilot/matplotlib/sealed/P9_DECISION_SEAL.json)
- [Both original frozen decisions](../pilot/matplotlib/sealed/P9_DECISIONS_SEALED.jsonl)
- [Original oracle machine receipts](../data/audits/P14_MATPLOTLIB_TWO_STAGE_ORIGINAL_ORACLE_20261119.jsonl)
- [Full reconciliation and original P9 descriptive score](../data/audits/P14_MATPLOTLIB_TWO_STAGE_RECONCILED_20261119.json)
- [Original public regression records](../data/audits/P14_MATPLOTLIB_POSTSEAL_PUBLIC_LINES_20261119.json)
- [Two-stage scoring source](../scripts/p14_two_stage_reconcile.py)

Raw original task logs/report/test-output artifacts were uploaded by GitHub Actions with a finite **60-day retention** policy. These machine hashes and URLs are retained, but a license-compatible long-term archive of raw artifacts is not yet deposited. Publication-grade archival completeness therefore remains a separate HOLD.

**Final state:** P14 EXECUTED, original task NOT RESOLVED by either stage, no validated policy advantage.
