# 99llm-X1 P25 — Matched Original-Source Null Control Exposes Benchmark P2P Attribution Error

**Date:** 20 November 2026. **Scope:** post-reveal endpoint investigation on the same tenth source-frozen task, not a new agent repair or a seventh/eleventh trial. Original P23 P9 and original Docker report remain unchanged.

## Main result

Using the **unchanged original cfn-lint source code and IAM schema** at commit `de28d1e43777e3782a06b74d9091c3471636eb70`, the same pinned original SWE-bench-Live evaluator was run under the same Docker namespace. The submitted patch was **only a non-functional Markdown HTML comment appended to README.md** to satisfy the evaluator's requirement for a non-empty patch. No program, schema or test code changed. The null control reported *exactly the same four failed PASS_TO_PASS test identifiers* as the P23 AI-generated IAM schema repair.

| Same original task and evaluator | P23 source candidate | P25 README-only null control |
| --- | ---: | ---: |
| FAIL_TO_PASS passed | **1/1** | **0/1** |
| PASS_TO_PASS passed | 1,227 | 1,227 |
| PASS_TO_PASS failed | **4** | **4** |
| Total classified tests | 1,232 | 1,232 |
| P2P failure IDs in common | **4/4** | **4/4** |
| P2P failures unique to candidate/control | **0** | **0** |
| Official resolved | False | False |

**Scientific meaning:** The candidate successfully passes the single original issue-specific F2P test where original source does not. The four P2P failures **do not require the candidate's changed IAM schema** because all four reproduce in the null control with source-identical code. In this matched pair, the evidence **does not support attributing the four failures to the candidate**. It does **not** establish that source behavior is universally correct or that the full original benchmark should be retroactively labeled resolved. It also does not establish the precise causes of all four shared failures; a previously documented E2533 Lambda runtime lifecycle date effect may explain a subset but independent cause certification remains a separate question.

## Chronology and source identity

- Original frozen tenth task `aws-cloudformation__cfn-lint-3779`; original source base `de28d1e43777e3782a06b74d9091c3471636eb70`. The original fixed 10-task selection is never changed.
- P23 original local outcome: original IAM condition schema tests improved 36/64 to 64/64, original real cfn-lint CLI nine cases improved 4/9 to 9/9. All these local tests were known pre-oracle and do not determine hidden truth.
- P23 original P9 decisions were sealed before original Docker oracle: self-report ACCEPT; local-pass ACCEPT; source-linked HOLD (actor independent attribution absent). Original P9 seal SHA-256 `01ba163c361473e2354589d038f86c321267035001e69cda92c03026172eac2c`.
- P23 original benchmark [run 44738711010](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44738711010): F2P 1/1, P2P failed 4, tests 1,232, resolved=False. Original output SHA-256 `965babfbe839670397012b811098b2a307c5986d4272fcff5e4f29fd7c142650`. This remains immutable as an *original reported benchmark outcome*.
- P24/P24B examined the original four P2P failures only **after** the original oracle. They include two original public integration cases and two unit test cases. A bounded P24B original-log inspection flagged `E2533` Lambda runtime lifecycle/date checks in several failures. The source/admissibility register separately cites upstream [cfn-lint #4125](https://github.com/aws-cloudformation/cfn-lint/issues/4125); that prior report must not be presented as a new discovery.
- P25 original-source-only matched control was registered after exposure to P23 outcomes. The neutral README change does not alter code or runtime semantics. [Original pinned Docker run 44761416230](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44761416230) produced a unique report with F2P 0/1 and the **identical four P2P failed test IDs** (P2P pass 1,227; test count 1,232). Null control original output SHA-256 `a0f9fa312b5bb88da5ba652541420329cedfc9021ff9bd163466ffb636a9f441`. Stored original GitHub Actions artifact ID `14642495330` (finite retention).

## Four shared failed P2P tests

| Exact original test identifier | P23 failed | P25 original null failed |
| --- | --- | --- |
| `test/integration/test_good_templates.py::TestQuickStartTemplates::test_module_integration` | Yes | Yes |
| `test/integration/test_good_templates.py::TestQuickStartTemplates::test_templates` | Yes | Yes |
| `test/unit/module/override/test_exclude.py::TestExclude::test_success_run` | Yes | Yes |
| `test/unit/module/test_rules_collections.py::TestRulesCollection::test_success_run` | Yes | Yes |

**Interpretative caution:** Test-ID overlap is strong evidence against **necessity** of the P23 patch for these failures, not proof that the patch has zero possible side effects, or that source changes cannot ever interact with baseline failures. No causal manipulation of the upstream Lambda date calendar, suite expectation files, or grader was done. `resolved=false` remains the official task report for both variants. One correct F2P result is not a guarantee of entire IAM validation correctness.

## Contribution to 99llm research

Reproducible counterfactual controls can change what the same test-suite verdict allows a researcher to infer. The original F2P/P2P unqualified task label, the **presence of independently reproducible baseline failures**, the process/actor evidence, and the decision-time gate cannot be replaced by one boolean pass/fail. A review manuscript should **separate endpoint validity and baseline-relative regression attribution**. The existence of the control was informed by observing P23 outcomes and is therefore NOT a new blinded test of policy efficacy. This is a methodological vulnerability discovery and diagnostic contribution, not proof that X1 accepts better repairs.

**Admissible statement:** In the matched post-reveal diagnostic, the P23 candidate passed the issue-specific test while four P2P failures were already present when its source changes were absent. This suggests the four original benchmark P2P failures are not attributable to the patch *on the evidence available*, but it does not overturn the original unresolved benchmark verdict.

**Not admitted:** switching P23 first prospective observed outcome to resolved; counting P25 as an additional task or agent rollout; claiming no P2P regression across all environments; certifying the upstream `E2533` calendar mechanism for each failing test; estimating a source-linked policy false-accept rate when the policy had zero accepts; or claiming human expert validation.

## Reproducibility

- Design fixed before P25 execution: [`protocol/P25_CFN_LINT_POSTREVEAL_BASELINE_NULL_CONTROL_20261120.json`](../protocol/P25_CFN_LINT_POSTREVEAL_BASELINE_NULL_CONTROL_20261120.json).
- Exact original P23 comparison: [`data/audits/P23_CFN_LINT_ORIGINAL_TASK_ORACLE_20261120.json`](../data/audits/P23_CFN_LINT_ORIGINAL_TASK_ORACLE_20261120.json).
- P23 four-test identities: [`data/audits/P24_CFN_LINT_P23_ORIGINAL_FOUR_P2P_DIAGNOSTIC_20261120.json`](../data/audits/P24_CFN_LINT_P23_ORIGINAL_FOUR_P2P_DIAGNOSTIC_20261120.json).
- P25 machine evidence: [`data/audits/P25_CFN_LINT_MATCHED_ORIGINAL_NULL_CONTROL_EXECUTED_20261120.json`](../data/audits/P25_CFN_LINT_MATCHED_ORIGINAL_NULL_CONTROL_EXECUTED_20261120.json).
- Exact replay [GitHub Actions 44761416230](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44761416230) and neutral README-only source patch retained in artifact. Original harness `microsoft/SWE-bench-Live` commit `ad79b850f15e33992e96f03f6e97f05ddf9aa0be`, dataset revision `babb27e45e072219195db7a744bbf0d3c1a36e56`, Docker namespace `starryzhang`.

**Editorial outcome:** KEEP P25 matched null-control as a valuable post-reveal, source-traceable attribution result. Hold any scientific manuscript rewrite until original validity and comparability denominators are reconciled. Keep MR30/P9–P24 and original resolved label unchanged.
