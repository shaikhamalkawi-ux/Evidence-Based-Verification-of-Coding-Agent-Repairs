# 99llm-X1 P18 — A Post-Reveal One-Literal Reversal of an Original SWE-bench-Live Task Label

**Scientific status:** Executed **POST-REVEAL** original-task sensitivity diagnostic, not a second independent/untouched agent solution. Historical P17 remains officially UNRESOLVED. Date: 19 November 2026 UTC (20 November 2026 in Dubai).

## Executive result

A single change to the wording of one `RuntimeError` — **without changing a conditional expression, tensor operation, DoRA calculation, or distributed-training code** — changed the SAME pinned original SWE-bench-Live task's benchmark verdict from **UNRESOLVED** to **RESOLVED**. This result documents evaluation **sensitivity to an error-message contract**. It does not show the underlying complete distributed DoRA 8B training now works or that an agent autonomously repaired the issue after feedback.

| Independent original-harness outcome | P17 first code patch (before hidden outcome) | P18 one-literal edit (AFTER hidden outcome) |
| --- | ---: | ---: |
| FAIL_TO_PASS checks passed | **0/1** | **1/1** |
| PASS_TO_PASS regressions | **0** | **0** |
| Original harness executed tests | **651** | **651** |
| Unique parsed reports | 1 | 1 |
| Official original resolved label | false | **true** |
| Full two-GPU Llama3 8B DoRA reproduction | NOT EXECUTED | **NOT EXECUTED** |
| New independent blinded agent result | P17 first attempt only | **NO — already exposed** |

### Reproducible sources

- **P17 first original task execution:** [GitHub Actions 44613016409](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44613016409); exact candidate `57f45fdd5552908d4b5d42cccd7359ccb4de2560`; original output SHA-256 `864bb5edf03e1810a348ead57862d7a057c852df95bf56f33a4b9403f5ca1282`.
- **P18 bounded post-reveal diagnosis:** [GitHub Actions 44614541023](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44614541023), [bounded failure taxonomy](../data/audits/P18_TORCHTUNE_POSTREVEAL_ERROR_TAXONOMY_20261120.json); zero raw hidden test code placed in the public source repository.
- **P18 CPU literal-only control:** [GitHub Actions 44615105523](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44615105523), [machine-readable CPU comparison](../data/audits/P18_POSTREVEAL_LITERAL_ONLY_CPU_20261120.json); P17 fails newly created post-reveal message test, P18 passes it, original six source CPU tests stay **6/6**.
- **P18 exact post-reveal original task re-execution:** [GitHub Actions 44615715646](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44615715646), [task-level original-harness comparison ledger](../data/audits/P18_TORCHTUNE_POSTREVEAL_ORACLE_LITERAL_RETEST_20261120.json); original output SHA-256 `3d0c13446d3e5548c8dd718a3c0c3a722b6b803a974f13401deee0f24b25044e`.

## 1. Original frozen task and failure detail

The original fixed task is `pytorch__torchtune-2139` at index 5 of the prespecified ten-task SWE-bench-Live lite frame. Historical torchtune source commit: `f2bd4bc25b24587aef40f486087412b9da8f1d94`, historical DoRA file `torchtune/modules/peft/dora.py`. Dataset frozen revision `babb27e45e072219195db7a744bbf0d3c1a36e56`; official unchanged harness commit `ad79b850f15e33992e96f03f6e97f05ddf9aa0be`.

P17 was a hypothesis-informed (from P16) first candidate that conditionally materialized a stale meta DoRA magnitude Parameter, but did not claim the original full two-GPU distributed task fixed. Original source CPU checks recovered from 2/6 to 6/6. Frozen BEFORE task oracle was the P9 policy decision **self_report HOLD / local_pass ACCEPT / source_linked HOLD**, recorded at 2026-11-19T20:45:51Z, decision SHA-256 `c62f5bffce085577ad1f5b0e4da05ec0a3a76b133e0eebd1f626bb4b2261ed35`. Source-linked HOLD was an authorship-evidence hold, not demonstrated detection of a hidden software bug.

After P17 was independently run and the task marked unresolved, P18 inspected its original task failure output. The one failing F2P check was `tests/torchtune/modules/peft/test_dora.py::TestDoRALinear::test_dora_meta_device_init_error`. Its expected exception regex was `Cannot initialize DoRA magnitude`, while P17 raised `RuntimeError('DoRA magnitude norm is still on meta device')`. The executed log reports a regex mismatch. This does **not** establish that all DoRA behavior was correct; it identifies what failed this particular original task F2P test.

## 2. EXACTLY one-literal code ablation, AFTER revelation

Source-revision relation is preserved: P18 began from the original exact P17 candidate Git SHA `57f45fdd5552908d4b5d42cccd7359ccb4de2560`, and the updated candidate SHA is `6c029466df2fdca0b28273b58eaab46ef6460075` (new historical DoRA source blob `0c0aeef1bb24336dff8904dd61d6ad33d4233dee`). The CI verified that the Git incremental patch contains exactly **one removed line and one added line**, with no expression change besides a string literal:

```python
# Original P17 diagnostic:
raise RuntimeError('DoRA magnitude norm is still on meta device')

# P18 post-reveal diagnostic:
raise RuntimeError('Cannot initialize DoRA magnitude: computed norm is still on meta device')
```

No other source behavior was modified. The original six CPU tests continued to pass 6/6, and a NEW post-reveal regex test (NOT part of the original preoracle input) changed from failure to success. Then the original benchmark ran the exact source-modified P18 patch, produced **1/1 F2P, 0 P2P failures and 651 executed tests**, and marked the task resolved.

**Causal interpretation of the mechanical contrast is narrow:** because the source diff contains only the literal, and original task/dataset/harness and test counts match, it is sound to say the **observed benchmark verdict** changed with the literal in this controlled retest. This is not evidence of generalizable model success, of correctness beyond the executed tests, or of a new independent task.

### Important boundary on benchmark validity

An error message may be a **legitimate API contract** for software users and tests. Therefore the example should NOT be described as an obviously invalid or meaningless test. What this case establishes is that label interpretation must distinguish **contract-conformance** from **end-to-end operational success**. The original benchmark's passing label, on this one already exposed task, does not test the user's original two-GPU Llama3/8B DoRA finetuning workflow; it does test a reported exception behavior. Neither P17 nor P18 executed full original GPU training on that hosted runner.

## 3. Scientific accounting and no-feedback leakage

The P17 first candidate's ORIGINAL unseen-task outcome remains **FAIL: 0/1 F2P**; P17 and its original P9 frozen decision are byte-identical to the previous baseline. P18 was produced **after inspecting the original F2P test's expected wording**, so its re-execution is an intentionally **unblinded endpoint-sensitivity ablation**. Consequently P18 **does not add a seventh task**, does not change the six-task original benchmark panel's success/failure totals (**2 originally resolved, 4 originally unresolved**), does not show a successful autonomous repair after genuine developer pushback, and does not cure the zero-accept non-vacuity problem of strict P9 source-linked policy.

Two P18 workflow execution limitations were logged and fixed at infrastructure level: the first original retest (run 44615536169) stopped before evaluator execution due to diff comparison of `-` and `+` marker prefixes; subsequent run 44615715646 verified the diff correctly, executed the original task and yielded the reported result. Original source patch/hidden test code was not changed to fix runner verification.

## 4. Editorial novelty check

**What P18 adds:** a source-locked **within-the-same-task executable counterexample** to equating a boolean task-resolved label with complete operational remediation, accompanied by original source code SHA, one-literal controlled contrast, original unchanged evaluator and explicit **post-reveal** status. This can strengthen a larger study of *verification contract sensitivity and evidence sufficiency*.

**What P18 does not add:** a novel error-message testing algorithm, a measured causal advantage of P9/X1, a fully distributed DoRA training repair, general benchmark unreliability, an independently attributable coding-agent response, a new independent validation task or an out-of-sample result.

**Editor decision:** KEEP as post-reveal mechanistic **endpoint-sensitivity demonstration** or supplementary negative-result explanation. HOLD claims of benchmark-wide validity problems or superiority of a proposed new gate. Any future systematic error-contract study should preregister a taxonomy (behavioral resolution, interface signature, error-message contract, regression preservation, resource feasibility), collect samples independently of observing failure content, quantify categories with task-level denominators and use new untouched instances; do not infer rates from one post-reveal experiment.

## 5. Reproducibility inventory

- [Original P17 scientific paper](../reports/P17_HISTORICAL_DORA_SOURCE_AND_ORIGINAL_ORACLE_20261120.md) and [original task ledger](../data/audits/P17_TORCHTUNE_ORIGINAL_ORACLE_20261120.json) — unchanged.
- [P18 protocol bounding post-reveal evidence](../protocol/P18_POSTREVEAL_TORCHTUNE_BOUNDARIES_20261120.json), [literal ablation registration](../protocol/P18_POSTREVEAL_LITERAL_SENSITIVITY_REGISTER_20261120.json) and [pre-retest registration](../pilot/torchtune/P18_POSTREVEAL_ORIGINAL_TASK_RETEST_REGISTER.json).
- [Exact one-literal code recipe](../pilot/torchtune/p18_postreveal_message_ablation.py) and [new, explicitly post-reveal CPU error message check](../pilot/torchtune/p18_postreveal_error_contract.py).
- [Bounded post-reveal original failure lines, not original test source](../data/audits/P18_TORCHTUNE_POSTREVEAL_ERROR_TAXONOMY_20261120.json).
- [CPU original-source unchanged 6/6 tests and textual contrast](../data/audits/P18_POSTREVEAL_LITERAL_ONLY_CPU_20261120.json).
- [P18 actual original task parsed results, SHA and score boundary](../data/audits/P18_TORCHTUNE_POSTREVEAL_ORACLE_LITERAL_RETEST_20261120.json).

The GitHub Actions original task output artifacts are retained with **finite 60-day retention**. Their URLs, exact source outputs and SHA-256 are in the ledgers. A license-compliant permanent raw-reproduction archive remains a future stage; do not paste private/hidden third-party test source into the manuscript or public repository.

**Conclusion:** One literal-only post-reveal modification flipped the pinned benchmark task's reported label. This is evidence of label sensitivity and a reason for multi-axis claim boundaries, not an independently validated new repair or model improvement.
