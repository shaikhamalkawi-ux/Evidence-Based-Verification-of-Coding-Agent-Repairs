# P29 — Historical Raw Full-Pytest-Node Audit and Independent-Prior-Evidence Closure
**20 November 2026 | 99llm-X1 companion project | Original MR30 and P9–P28 preserved**

## Executive scientific finding
Reopened **four exact original archived GitHub Actions artifacts** for the two post-reveal neutral controls, without rerunning an agent, the original test harness, or a Docker evaluation. Compared the complete names from the \`PASSED\`/\`FAILED\` lines of the original pytest summary in each \`original_test_output.txt\`, independent of the original SWE-bench-Live log parser.

| Original task (unique task unit) | Historical candidate raw FAILED full IDs | Historical unchanged-source neutral FAILED full IDs | Shared failed full IDs | Candidate-only failed full IDs | Neutral-only failed full IDs |
| --- | ---: | ---: | ---: | ---: | ---: |
| **Kedro #4406** | **87** | **88** | **87** | **0** | **1** (original F2P) |
| **cfn-lint #3779** | **7** | **8** | **7** | **0** | **1** (original F2P) |

The candidate additionally has one \`PASSED\` full-ID test absent among the control PASSED IDs; that exact ID is the neutral-only FAIL and the benchmark's original issue-specific F2P. Raw pytest \`PASSED\` counts are Kedro 1,630 vs 1,629 and cfn-lint 1,676 vs 1,675. The paired raw failure sets are exact at complete node-name level **within these two historical executions**. The 87 and seven raw fail lines are *not* 87 or seven independent tasks, and are **not** the official P2P fail counts.

## Report parser issue and resolution of the diagnostic ambiguity
The **original official benchmark reports still contain exactly 25/25 identical failed P2P *parser keys* for Kedro and 4/4 for cfn-lint**. However **3 of Kedro's 25 parser-emitted failed IDs** contain an opening parameter bracket \`[\` without a closing \`]\`: they have been truncated at a space inside parametrized pytest node names. This is consistent with the earlier publicly reported SWE-bench-Live whitespace parsing defect in upstream issue **#102** (23 October 2026), with proposed fix discussed in **#109**. Therefore P27 should not describe every returned *parser key* as a complete original pytest test name.

The P29 **independent raw-log** comparison instead reads complete \`FAILED tests/...\` and \`FAILED test/...\` summary lines preserving spaces inside brackets. It rejects unbalanced brackets, duplicate IDs, and conflicting pass/fail statuses; ignores application \`ERROR\` log messages that are not pytest test-result records. For Kedro, these full raw ID sets contain 87 and 88 failed tests and are nested exactly candidate ⊂ neutral. cfn-lint's seven named raw failures are also nested in the neutral's eight.

This **supports the bounded P27 no-candidate-only-failure observation despite the old parser's three truncated IDs**. It does not prove all tests were executed in every possible environment; the full raw summaries contain tests beyond the official benchmark's F2P/P2P scoring lists.

## Frozen original benchmark and policies — unchanged
| P9 policy | Accepted/9 | P26 original endpoint partial-ID bounds | P27 different, post-reveal baseline-relative endpoint |
| --- | ---: | ---: | ---: |
| Self-report | 5/9 | 40–80% | 40% |
| Any local-test success | 8/9 | 50–87.5% | 50–62.5% |
| Source/actor-linked | 0/9 | undefined | undefined |

Original frozen frame: **10** selected; **9** original candidates with pre-oracle decisions; **1** Reflex without candidate. Original strict official scores **2 RESOLVED, 7 UNRESOLVED, one unattempted**. P26 and P27 are **different estimands** and these intervals are not two confidence intervals or a method-improvement estimate. Both Kedro and cfn-lint original reported \`resolved=false\`. The strict source/actor gate accepted none, so accepted-failure risk is **undefined, not zero**; it also held both originally passing tasks.

## Audit evidence and immutable source provenance
- Original Kedro candidate (17 Nov): run **44159300952**, artifact **14363775392**; original source-neutral (17 Nov): run **44162955737**, artifact **14364582406**.
- Original cfn-lint candidate (20 Nov): run **44738711010**, artifact **14630435763**; original source-neutral (20 Nov): run **44761416230**, artifact **14642495330**.
- Original dataset revision \`babb27e45e072219195db7a744bbf0d3c1a36e56\`, original evaluation harness \`ad79b850f15e33992e96f03f6e97f05ddf9aa0be\`. Both no-behavior-change controls are **post-reveal diagnostics**. Kedro source and null are sequential, not simultaneous.
- All four source artifacts: ZIP integrity PASS, original test-output SHA-256 checked, original report's official scoring partitions checked. Derived full-name failure-set SHA-256 digests are saved in \`data/audits/P29_RAW_FULL_NODE_ID_MATCH_RESULT_20261120.json\`. Complete raw archived test outputs are **not reproduced in this public branch**; source GitHub Actions artifact retention is finite.
- Standalone standard-library script \`scripts/p29_full_pytest_id_audit.py\` and 13 corruption/identity/parser tests; GitHub Actions CI workflow reruns the extraction **only** against those exact already-executed artifacts (not a benchmark oracle). A separate local reference script/verification also produced the identical source-count vectors.

## New decisive prior-art evidence
**A materially more direct precedent was found than P28 recognized:** upstream [microsoft/SWE-bench-Live #113](https://github.com/microsoft/SWE-bench-Live/issues/113), **opened 11 November 2026**, named the exact Kedro \`kedro-org__kedro-4406\` instance and **25 original P2P test failures** under a **reference gold patch**. It reports a moving \`kedro-starters\` dependency as the likely reason. Its test groups **13+6+6** agree with our Kedro P27 scored group breakdown. The prior report used official evaluator commit \`62d02936\` (abbreviated by its author) and gold patch, so it is *not* an independently rerun copy of our no-code original-source diagnostic. Treat it as **prior independent technical report, not as new discovery or an independently verified causal mechanism**.

The prior upstream [issue #100](https://github.com/microsoft/SWE-bench-Live/issues/100), opened 23 October, raised benchmark environment validity in related instances; a maintainer commented on **7 November** that a dataset update fixed the reported issue. The later issue #113 explicitly says that dataset revision \`babb27e4\` dated **3 November** fixed several sibling cases but **not** Kedro #4406. Do not infer every task became valid from the blanket closure of #100. Newer versions may change; version mapping must be checked case by case.

The technical report [Wu et al., 7 Nov 2026, arXiv 2611.10837](https://arxiv.org/abs/2611.10837) already proposes a broader five-dimensional source/test-oracle/execution/label-adjudication framework, creating a major novelty collision with a generic companion method. The earlier studies by Smith et al. (FSE 2015), test-based acceptance audits (TOSEM 2025), ICSE 2026 PatchDiff, and [upstream #102](https://github.com/microsoft/SWE-bench-Live/issues/102) further restrict novelty.

## Interpretation and editorial disposition
**KEEP:** unique complete raw pytest ID concordance in two historical pairs; source/hash/time provenance; limited non-necessity of patch to produce the named failed tests; test-parser limitation and repair by re-reading full source logs; independently evidenced prior-art collision.

**HOLD:** first-ever discovery, general correction to SWE-bench-Live, proof of deployment correctness, proof that \`kedro-starters\` drift is the single cause of every failure, generalizable agent failure rate, risk–coverage innovation, causal policy superiority, new actor-attested model experiment, or journal-ready full-length methods claim.

**Next real research gate:** a separate new pre-registered task frame with actual actor-authenticated agent rollouts and paired negative controls, or a sharply bounded short reproducibility/case-series note. P29 **does not count as the prospective execution** proposed as a design-only plan in P28.

**Result-change statement:** P29 adds independent read-only verification and refines the distinction between *parser keys* and *full raw pytest names*. Original P9/MR30/P26/P27/benchmark results and all original files remain unmodified. The new 87/88 and 7/8 are *additional summary counts of old artifacts*, not revised task outcomes.
