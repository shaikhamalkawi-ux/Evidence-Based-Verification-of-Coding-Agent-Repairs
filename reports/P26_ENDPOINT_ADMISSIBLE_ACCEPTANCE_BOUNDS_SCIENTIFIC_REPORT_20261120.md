# 99llm-X1 P26 — Endpoint-Admissible Acceptance Bounds for Source-Linked Coding-Repair Evidence

**Research status:** Posthoc evidence-admission and finite-frame partial-identification extension, **not a new prospective trial, a new selective-classification algorithm, or a revision to MR30.** Based on the original ten-task SHA-selected SWE-bench-Live lite frame and pre-oracle original P9 policy decisions. Calculation and independent code-path audit executed on 20 November 2026.

## 1. The scientific problem after P25

A boolean original benchmark verdict need not constitute a sufficient endpoint for **source-attributed repair failure**. This was demonstrated rather than assumed in two distinct ways:

- **privacyIDEA (original task #7):** an original Docker report marked the task unresolved with F2P 0/1 and 2,022 failed P2P entries, but the original output had a systemic missing module (\`swe100_fixture_clock\`), and the endpoint validation gate declared a **code-correctness HOLD**. The raw result is immutable, but not an admitted behavioral failure label.
- **cfn-lint (original task #10):** original hidden F2P passed 1/1, with four failed P2P tests, so the raw benchmark declared unresolved. A post-reveal control with **unchanged original source and only an inert README comment** reproduced all four failed P2P test IDs exactly. In the matched pair, the four failures do not require the source patch. The raw benchmark verdict is still unresolved and the existence of other faults is not ruled out.

A third case, **Kedro (original task #1)**, passes F2P 1/1 but has 25 failed P2P tests. No matched original-source control has yet been performed for those 25; the causal interpretation of that P2P outcome is therefore held open.

These are not claims that the three source repairs succeeded. They are **missing endpoint attribution** states, with different evidence reasons.

## 2. Frozen frame and evidence partition

All ten originally selected tasks are preserved. Nine had a frozen coding-repair candidate and pre-oracle P9 decisions, and nine produced an original Docker benchmark report. The tenth selected task, Reflex, never received a source patch or original task oracle. Among the nine attempted original tasks, the evidence supports the following more cautious endpoint partition:

| Source-admission class | Distinct original tasks | Why |
| --- | --- | --- |
| PASS original independent task oracle | Babel, Faker | F2P passed and zero failed P2P in original independently executed task oracle |
| FAIL original issue-specific F2P | PDM, Matplotlib, torchtune, DSPy | At least one original issue-specific F2P failed in an executed test; no known systemic import/collection invalidation in these outcomes |
| UNKNOWN due to unattributed P2P | Kedro | F2P passes; 25 P2P fail, with no matched original-source baseline |
| UNKNOWN due to invalid endpoint | privacyIDEA | Missing imported fixture in original test output makes reported failure unsuitable for source correctness |
| UNKNOWN due to matched baseline P2P | cfn-lint | F2P passes; the exact four failed P2P tests also fail with original unmodified code |
| No source attempt or P9 decision | Reflex | Frozen task preserved, but no full original reported-issue reproduction/agent candidate or oracle |

The original official raw figures remain **9/10 executed, 2/9 resolved, 7/9 unresolved**. These original figures are **not** equivalent to 7 confirmed newly caused code defects. In particular, the 4 direct F2P failures cannot be conflated with the 3 unknown source/endpoint states, and the one unattempted task must not be imputed as failed.

The original **Matplotlib** final candidate followed one scripted AI-produced corrective instruction, whereas the other cases are initial attempts or different candidate configurations. The nine-task comparison is a **mixed-stage descriptive case series**. Treat the distinct original task—not each initial/final revision or each individual unit test—as the counting unit.

## 3. Exact logic and sharp finite-frame identification

For a policy \(p\), let \(A_p\) be the set of its ACCEPT decisions among the nine attempted tasks. Partition those accepted cases into directly failed F2P \(F_p\), original task-oracle PASS \(S_p\), and unresolved/endpoint-QC-unknown \(U_p\).

For \(|A_p|>0\), under *no invented binary truth assignment* to the unknown accepted cases, the accepted-failure fraction satisfies the standard finite-case partial-identification bounds:

\[
\frac{|F_p|}{|A_p|}
\;\leq\; \mathrm{Risk}_{p,\mathrm{accepted}}
\;\leq\; \frac{|F_p|+|U_p|}{|A_p|}.
\]

The endpoint status is a declared **task-test admission contract**, not a universal judgement about all source behavior or future deployment. Each bound is *sharp given those classifications and no additional cross-task constraints*: all unknown accepted cases may consistently be completed as PASS (lower endpoint) or FAIL (upper endpoint). This is an application of established missing-outcome **partial-identification logic**, not a new mathematical theorem. See Manski (2005, DOI 10.1016/j.ijar.2004.10.006).

If \(|A_p|=0\), accepted-failure risk is **undefined (0/0)**. It is not zero. Coverage \(|A_p|/9\) is directly observed regardless of endpoint unknowns, but is only finite-case process coverage.

## 4. New results

| Original P9 policy | ACCEPT among 9 candidates | Accepted direct F2P FAIL | Accepted original PASS | Accepted unknown endpoint/attribution | Sharp accepted-failure fraction |
| --- | ---: | ---: | ---: | ---: | --- |
| Self-report | 5/9 | 2 | 1 | 2 | **2/5–4/5 (40%–80%)** |
| Any visible local test success | 8/9 | 4 | 1 | 3 | **4/8–7/8 (50%–87.5%)** |
| Source-linked with independent agent attribution | 0/9 | 0 | 0 | 0 | **UNDEFINED** |

These exact numerical bounds were recomputed by the **unchanged standard-library Python source** \`scripts/p26_identified_acceptance_bounds.py\` using only original source evidence. Run [44769991402](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44769991402) verified **151/151** software and corruption controls, with output SHA-256 \`4ce92ed6a4a835504bd250157f03744efca55cb74e449e7de1dfba7f338f6569\`.

A **separate JavaScript recomputation**, without calling the Python bound code, recovered the same accepted counts and endpoint allocations. The independent cross-check and all nine task classifications are saved at \`data/audits/P26_INDEPENDENT_CODEPATH_IDENTIFIED_INTERVALS_20261120.json\`.

The original source-linked policy held **both of the two source-admitted original task successes**, which establishes a *coverage/nonvacuity concern* for this sample, not the absence of a safety benefit. The gate has no ACCEPT cases because independently authenticated model/agent actor evidence was unavailable. It cannot be declared perfectly precise.

**Why the bound matters:** the naive 7/8 raw-unresolved fraction among local-pass ACCEPT cases treats all three uncertain accepted cases as actual failures. The source-admissible lower bound is only 4/8 because four specifically recorded task-oracle F2P failures remain after removing all uncertain endpoint assignments. Reporting both endpoints is scientifically safer than either calling all three missing cases failures or treating them as successes.

## 5. Literature positioning and genuine contribution

Selective classification's **risk–coverage trade-off** predates this project (e.g., Geifman and El-Yaniv, NeurIPS 2017; https://papers.neurips.cc/paper_files/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html). Missing-outcome sharp bounds likewise predate this work (Manski, 2005; https://doi.org/10.1016/j.ijar.2004.10.006). Neither the formula nor the vocabulary is claimed new.

The candidate **domain contribution** is narrower and more concrete: source-time-locked coding-repair decisions are mapped into **endpoint-admissible versus attribution-held source claims**, with one source-preserving negative-control experiment showing why an original unresolved Docker report may not establish repair-caused regressions. The result is an auditable **finite-case uncertainty ledger**, rather than a newly invented policy or a leaderboard claiming superior repair accuracy.

Published discussion of SWE-bench Verified has noted evaluation leakage, overly specific tests and environment dependence (OpenAI, 23 February 2026; https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/). That article concerns **SWE-bench Verified**, not the original SWE-bench-Live lite evaluation executed here, and its numbers must NOT be transferred to this project. It serves only as background motivation for endpoint diligence.

## 6. Explicit limitations and editorial decision

This is **not** a powered experiment, a population estimate, a causal policy comparison, field deployment study, or evidence that one model is better than another. The source candidates were produced in AI-assisted scripted research rather than independently attested autonomous-agent rollouts. One case includes post-feedback script intervention; other tasks have differing environments. No real human coder or second human agreement experiment occurred, and none is invented.

The three unknown tasks do not assert a 50/50 probability of success. The intervals contain logical completions, **not likelihoods, Bayesian posteriors, confidence intervals, or calibrated risk guarantees**. No weights, thresholds, or new arbitrary utility function were introduced.

The original P9 policy, all timestamped decisions, actual original task oracle reports, source patches, MR30 manuscript, and its 16,118-episode review findings are left **unchanged**. The present result belongs in a **separate companion methodological paper or a clearly flagged later-authorized extension**, not in an overwrite of MR30.

**Editorial decision:** KEEP P26 identified intervals and exact source-to-claim ledger as a substantive research contribution; HOLD any statement of policy superiority, externally validated model attribution, or universal code-repair correctness. Consider a new, explicitly post-reveal original-source matched control on Kedro to test the unattributed 25 P2P failures; do not silently reclassify it based on inference.

## 7. Executable audit sources

- \`protocol/P26_ENDPOINT_PARTIAL_IDENTIFICATION_PRECOMPUTATION_20261120.json\`: source admission and no-imputation rules.
- \`scripts/p26_identified_acceptance_bounds.py\`: source-to-endpoint calculation with standard-library exact rational bounds.
- \`tests/test_p26_identified_bounds.py\`: all original frame, tamper, and zero-accept negative controls.
- \`data/audits/P26_INDEPENDENT_CODEPATH_IDENTIFIED_INTERVALS_20261120.json\`: separately coded verification of results and all ten states.
- \`data/audits/P25_TEN_FROZEN_TASKS_ENDPOINT_ADMISSION_RECONCILIATION_20261120.json\`: parent original source evidence ledger.
- The existing original P9 and dataset identifiers: policy \`X1-P9-alpha-1-20261116\`, dataset revision \`babb27e45e072219195db7a744bbf0d3c1a36e56\` and official original harness SHA \`ad79b850f15e33992e96f03f6e97f05ddf9aa0be\`.
