# 99llm-X1 P25 — Frozen Ten-Task Endpoint-Admissibility Synthesis

**Date:** 20 November 2026. **Status:** editor-level, evidence-first reconciliation. This is neither a new blind agent trial nor a modification to MR30, original P9, or prior task-level outcomes.

## What is actually known about the ten selected tasks?

All ten tasks and the original SHA selection have been preserved; original benchmark Docker reports were executed on **nine** distinct tasks. The raw official statuses are **two resolved and seven unresolved**, with one task not executed. These raw counts are not nine independent verified causal coding-repair outcomes. At least two cases have separate endpoint or baseline-attribution concerns.

| Frozen # | Task | Original benchmark status | Endpoint-science interpretation |
| ---: | --- | --- | --- |
| 1 | kedro-org__kedro-4406 | Unresolved | 1/1 F2P but 25 P2P failed; baseline-relative causation not separately certified |
| 2 | pdm-project__pdm-3419 | Unresolved | 0/3 F2P; original initial candidate, later P13 work explicitly post-reveal |
| 3 | matplotlib__matplotlib-28933 | Unresolved | 0/1 F2P after scripted correction; paired stages are one task |
| 4 | python-babel__babel-1163 | Resolved | Original harness F2P 8/8, zero P2P failures; accepted raw verifier result |
| 5 | pytorch__torchtune-2139 | Unresolved | 0/1 F2P on original blind first candidate; P18 regex-only improvement was post-reveal |
| 6 | stanfordnlp__dspy-1609 | Unresolved | 0/4 F2P; 9/9 source-local tests did not cover remote end-to-end issue |
| 7 | privacyidea__privacyidea-4251 | Raw unresolved | **QC HOLD:** original test output has missing `swe100_fixture_clock` import; raw 2,022 P2P failures do not prove 2,022 code regressions |
| 8 | joke2k__faker-2155 | Resolved | Original harness F2P 1/1, zero P2P failures; accepted raw verifier result |
| 9 | reflex-dev__reflex-4510 | **Not executed** | **Visibility HOLD:** original `typing.Any` symptom not reproduced; present-day imports fail, vintage SQLModel pins produce no exception |
| 10 | aws-cloudformation__cfn-lint-3779 | Raw unresolved | **Baseline-attribution HOLD:** P23 F2P 1/1, but exact same four P2P failures also occur in P25 original-source null control |

These distinctions are machine-recorded at [`P25_TEN_FROZEN_TASKS_ENDPOINT_ADMISSION_RECONCILIATION_20261120.json`](../data/audits/P25_TEN_FROZEN_TASKS_ENDPOINT_ADMISSION_RECONCILIATION_20261120.json). The P20 reported unresolved status and P23 reported unresolved status are **not** rewritten. P25 control is not a tenth+1 task.

## Why a policy superiority statement still cannot be published

In the earlier **seven-task mixed-stage descriptive panel only** (P19, prior to adding endpoint-unadmitted P20 and baseline-confounded P23), original P9 self-report accepted four cases, three raw unresolved; local-pass accepted six, five raw unresolved; and the actor-source-linked policy accepted zero. Among source-linked accepted cases the false acceptance rate is undefined; among the two raw resolved cases it held both. The P19 panel mixes initial attempts and a corrected Matplotlib stage and **is not** a homogeneous prospective population estimand. Do not generalize the 5/6 figure as a market or real coding-agent deployment false acceptance rate.

After the additional tasks, presenting **one naive nine-case** false-accept rate would be methodologically wrong because `privacyIDEA`'s task truth has an admitted import/collection defect and `cfn-lint`'s four P2P failures are baseline-reproduced. These are different failure mechanisms and require distinct evidence states rather than assigning both source repair failure. There is no independent agent-author attribution for the strict P9 gate in this pilot.

## What P25 adds that prior P23 could not

P23's source-only IAM regex changes improved a local original-source test family and passed its single original F2P. Its original Docker task still returned `resolved=false` because four P2P tests failed. P25 ran **exact original source without the candidate changes**, with only an inert README comment, using the same task/harness/image. The four P2P failures reproduced by exact name **4/4** and there were **zero candidate-only P2P failures** in this matched pair. This directly rejects the simplistic inference 'the P23 patch introduced those four failures' on the current evidence. It does not prove universal absence of patch regressions, exact date causation or retrospective full benchmark success.

Both source and control were post-reveal for attribution analysis (the original P23 result was blind to the held-out test at decision time). **Keep the time and information budget boundaries explicit**.

## Editorial recommendation

**Acceptable paper claim:** Verification of coding-agent repairs requires distinguishing what a local test checks, whether the original task benchmark actually executed and collected its tests, whether baseline failures explain P2P outcomes, and whether the alleged model actor is independently attributable to the patch. A source-linked rule that abstains on all cases is not empirically demonstrated to identify good patches.

**Not acceptable:** Claiming that all raw unresolved tasks are coding defects, that the original benchmark's 2,022 P2P failures each indicate a privacyIDEA regression, that P25 retrospectively turns P23 into a benchmark pass, that post-reveal DoRA wording optimization demonstrates blind repair, or that P9 source-linked policy has proved superior precision.

**Highest-value next evidence:** For any future genuine selective policy study, use a provenance-eligible real agent execution with attested or externally recorded model/tool trace linked to patch SHA; preregister source, patch, local tests and process-only gate and execute the original task oracle after public timestamped lock. If that is infeasible, **publish the evidence-sufficiency and endpoint-attribution methodological case series**, not a predictive policy effectiveness paper.

## Reproducibility and scope

- P23 original task [GitHub Actions run 44738711010](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44738711010).
- P25 original-source matched null control [run 44761416230](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44761416230).
- P21 original privacyIDEA endpoint QC [run 44672006805](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44672006805).
- P22 original Reflex visibility diagnostics [run 44673175694](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44673175694).
- Original original-harness task frame: `pilot/frozen_task_frame_20261117.json`, dataset revision `babb27e45e072219195db7a744bbf0d3c1a36e56`, original evaluator SHA `ad79b850f15e33992e96f03f6e97f05ddf9aa0be`.

Original main paper MR30, frozen decisions, test manifests, task frames and candidate patch bytes remain untouched. This report is editorial scientific synthesis and an evidence lineage extension only.
