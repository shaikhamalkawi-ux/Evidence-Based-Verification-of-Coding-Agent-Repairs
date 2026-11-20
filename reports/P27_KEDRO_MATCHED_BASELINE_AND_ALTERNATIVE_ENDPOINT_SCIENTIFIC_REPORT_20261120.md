# 99llm-X1 P27 — Recovered Kedro Null Control and Baseline-Relative Endpoint Sensitivity

**Date:** 20 November 2026. **Status:** Existing-artifact source audit plus post-reveal endpoint sensitivity, NOT a new agent execution, new original task, blind experiment or retrospective policy edit. MR30, original P9 and all original task reports remain unchanged.

## 1. The unexpectedly recovered evidence

P26 classified Kedro's 25 P2P failures as an **unattributed baseline risk** because its source ledger did not include a valid original-source control. A complete cross-check of the GitHub Actions archive found that such a control had **already been preregistered and executed on 17 November 2026**:

- Original GPT-6-scripted Kedro first candidate: [original evaluator run 44159300952](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44159300952), original source base \`a565d6607d1d16933dbb1ea42cfb9de39ef80980\`, candidate source SHA \`355ae83abe163ab9bbe2aaf7a59cc055f220d13e\`.
- Historical diagnostic no-op control: [GitHub Actions 44162955737](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44162955737), **same source base** and only a Python comment added at the end of \`kedro/__init__.py\`, not executable code.
- Original no-op diagnostic was registered after disclosure of the first candidate outcome in \`pilot/kedro/null_semantic_patch_control_prereg.json\`. This experiment was post-reveal from inception.
- P27 did **not** run either original benchmark again. It read both already executed GitHub Actions report artifacts, checked the original source/revision/date contracts and extracted test identity sets by the same task ID. [Reconciliation run 44771086488](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44771086488).

The matched original-source comparison is:

| Original Kedro task evidence | AI-generated first candidate | Unmodified-source comment-only control |
| --- | ---: | ---: |
| Original issue-specific F2P passed | **1/1** | **0/1** |
| Original P2P passed | 1,566 | 1,566 |
| Original P2P failed | **25** | **25** |
| Exact failed P2P test IDs in common | **25/25** | **25/25** |
| Candidate-only / control-only failed P2P IDs | **0 / 0** | **0 / 0** |
| Original tests executed | 1,592 | 1,592 |
| Original official resolved | False | False |

The exact result appears at \`data/audits/P27_KEDRO_PREEXISTING_MATCHED_NULL_20261120.json\`. Original raw reports have separate SHA-256 hashes, and original artifacts remain accessible in the past GitHub Actions runs (retention is finite). Original P9 decisions \`self_report=ACCEPT,\ local_pass=ACCEPT,\ source_linked=HOLD\` were NOT recomputed.

**Admissible finding:** All 25 P2P failures in the original candidate evaluation also existed with source-original Kedro code and a comment-only neutral patch. Thus the candidate's edit was **not necessary for any of the 25 named failed P2P tests** in the paired historical evaluations. This is stronger than simply seeing the same number of failures.

**Not established:** that Kedro was fully solved in production, that all defects are harmless, that all failures have the same underlying causes, or that the original official benchmark's \`resolved=false\` verdict should be rewritten.

## 2. The same phenomenon now appears in two distinct repositories

The separately executed and previously documented P25 cfn-lint null control also reproduced all **four** P2P failures with original source and only a README comment. Both Kedro and cfn-lint candidates pass their issue-specific F2P tests, whereas their matched original-source controls fail F2P. Yet the sets of failed P2P tests are identical between candidate and original-source control in each task.

| Original issue | F2P AI candidate | F2P original-source control | Failed P2P set overlap | Candidate-only failed P2P |
| --- | --- | --- | --- | --- |
| Kedro #4406 | 1/1 | 0/1 | **25/25** | **0** |
| cfn-lint #3779 | 1/1 | 0/1 | **4/4** | **0** |

This **two-case replication of a failure-attribution problem** is decision-relevant. It shows why treating every P2P failure in a time-dependent original benchmark as a newly introduced source-code regression can produce a false explanation of the agent's patch. It is not an estimate of the frequency of the problem in benchmarks.

## 3. Two explicitly DIFFERENT endpoints — never substitute one for the other

**Original official SWE-bench-Live endpoint**: a task is resolved only if all F2P and all P2P pass. Under this unchanged official rule, both Kedro and cfn-lint remain **UNRESOLVED**.

**Posthoc baseline-relative test-adequacy endpoint**: a candidate passes the narrowly defined task-test check if (i) all F2P pass and (ii) there are either zero failed P2P, or *no candidate-only failed P2P test ID* compared with a matched original-source neutral control on the same original task/test snapshot. The comparison is by exact failed test ID sets, not by counts alone.

This alternative test criterion is **NOT an official benchmark score**, a new coding-agent performance metric, or a guarantee of universal regression safety. Both null controls and this re-interpretation occurred after original test outcomes were available; candidate and null were not executed simultaneously, even though the same original harness revision, Docker namespace and source task were used. Only **task-specific test evidence** is considered, not real deployment behavior.

For the original 9 candidates with original P9 decisions, the posthoc baseline-relative task-test partition is:

- **4 direct F2P FAIL**: PDM, Matplotlib, torchtune, DSPy;
- **2 original official task PASS**: Babel, Faker;
- **2 baseline-relative-only PASS**: Kedro, cfn-lint;
- **1 UNKNOWN / invalid endpoint**: privacyIDEA, because of the original missing fixture \`swe100_fixture_clock\`.
- Reflex remains the tenth original selected task but has **no patch or original task oracle**, and is excluded only from the nine-decision denominator.

## 4. Conditional P27 bounds versus original P26 bounds

| Policy | ACCEPT/9 | Original P26 admitted-failure bounds | **P27 alternative baseline-relative test-adequacy failure bounds** |
| --- | ---: | ---: | ---: |
| Self-report | 5/9 | 2/5–4/5 (40–80%) | **2/5–2/5 (40%)** |
| Local test success | 8/9 | 4/8–7/8 (50–87.5%) | **4/8–5/8 (50–62.5%)** |
| Original P9 source-linked actor gate | 0/9 | Undefined | **Undefined** |

**CRITICAL:** The P27 intervals do **not** mathematically tighten the P26 interval for the *same estimand*. They answer a **different, explicitly posthoc question** that admits no-*incremental*-P2P evidence from matched original-source controls. They must never be shown in a paper as if P25/P27 had revised the original SWE-bench-Live labels to PASS. The old P26 original endpoint uncertainty analysis remains valid and unchanged.

Within P27's alternative definition, the local-pass policy accepted eight cases: four definite original issue-specific F2P failures, three test-adequacy passes (Faker, Kedro, cfn-lint), and one indeterminate import-invalid task. Hence this *conditional* local accepted-failure fraction is logically between **4/8 and 5/8**, not a confidence interval. Self-report accepted five cases: two direct issue-test failures, and three test-adequacy passes, giving **2/5** for this explicitly different endpoint.

The source-linked policy accepted zero patches, and its accepted-risk remains undefined regardless of endpoint. The lack of independent actor attestation is not a demonstrated hidden-bug detector.

## 5. Interpretation for a separate research manuscript

This is a compelling methodological case of **evidence-claim separation**: a source-time-locked repair can meet its issue-specific checks while the original benchmark fails due to regressions already observed when the patch is absent. A valid assurance chain should disclose not just green/local test counts but at least five distinct elements: (1) original issue-specific F2P result, (2) complete original P2P report, (3) matched original-source baseline for P2P attribution where available, (4) endpoint execution validity, and (5) source/actor provenance.

There is no need to invent a new universal verifier, causal estimator, MCDM ranking, weighted scalar score, or additional acceptance threshold. Selective risk and coverage (Geifman and El-Yaniv, NeurIPS 2017) and partial-identification bounds (Manski, 2005) are established prior work; this research contribution lies in **source-traced evidence admission and matched baseline counterexamples**.

The original MR30 16,118-episode source-annotation reanalysis remains a different locked review/reanalysis paper and must NOT be rewritten, cited as an independent agentic validator, or mixed into the original ten-task data denominator. No real human coder or second human reliability study was performed.

## 6. Reproduction and audit

- P27 prior original source comparator register: \`protocol/P27_KEDRO_PRIOR_ORIGINAL_NULL_ARTIFACT_RECOVERY_20261120.json\`.
- The ORIGINAL 17 November control preregistration: \`pilot/kedro/null_semantic_patch_control_prereg.json\`; original null run [44162955737](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44162955737).
- P27 old artifacts compared by exact test IDs, no new Docker tests: \`data/audits/P27_KEDRO_PREEXISTING_MATCHED_NULL_20261120.json\`; comparison [run 44771086488](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44771086488).
- Posthoc endpoint assumptions: \`protocol/P27_POSTREVEAL_BASELINE_RELATIVE_ENDPOINT_SENSITIVITY_20261120.json\`.
- Deterministic source replay: \`scripts/p27_relative_endpoint_sensitivity.py\`; full Python/negative controls [run 44771948313](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44771948313), **157/157 PASS**, SHA-256 of output JSON \`d526c426b2ed17af895b1b211ec57514d0963f4ad4395c9667ff8155fdde8d76\`.
- Independent JavaScript source recomputation: \`data/audits/P27_INDEPENDENT_JS_BASELINE_RELATIVE_BOUNDS_20261120.json\`.
- P25 separate cfn-lint null control and report: \`data/audits/P25_CFN_LINT_MATCHED_ORIGINAL_NULL_CONTROL_EXECUTED_20261120.json\` and \`reports/P25_CFN_LINT_MATCHED_SOURCE_NULL_CONTROL_ATTRIBUTION_20261120.md\`.

**Editorial disposition:** KEEP the two original-source matched controls as the strongest new P25–P27 evidence on benchmark outcome attribution. KEEP the P26 and P27 calculations in clearly distinguished sections. HOLD original policy superiority, P9 actor verification, and any rewrite of official first-attempt task outcomes. Prepare a separate companion-paper Results and Discussion around this precise contribution, only after author approval of journal scope and originality.
