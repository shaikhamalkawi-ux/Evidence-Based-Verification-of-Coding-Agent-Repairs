# 99llm-X1 P17 — Historical DoRA Source Repair: CPU Mechanism Recovery Without Independent Issue Resolution

Date: 20 November 2026 (Asia/Dubai; original tool receipt UTC 19 November). Status: **EXECUTED NEGATIVE ORIGINAL BENCHMARK TASK**, original P9 policy and original code fixed before gold access. Historical task pytorch__torchtune-2139, original preselected index 5 of ten; no task substitution.

## 1. Main result

The historically pinned DoRALinear class AST, executed under CPU PyTorch 2.10.0 with import-only stubs for unrelated torchao/torchtune modules, went from **2/6** original-source diagnostic passes (3 failures, 1 error) to **6/6** after a source-limited conditional-materialization patch. The original SWE-bench-Live task oracle, however, marked the candidate **UNRESOLVED**, FAIL_TO_PASS **0/1**, PASS_TO_PASS failures **0**, and **651 parsed tests**. Both are observed results. The CPU test does NOT prove distributed DoRA training success; the original harness is a different, task-specific outcome.

| Original evaluation tier | Historical base | P17 first candidate | Meaning |
| --- | ---: | ---: | --- |
| Six frozen tests on original DoRALinear class AST (CPU, nonquantized) | 2/6 | **6/6** | Narrow mechanism supported, not production training |
| Original pinned SWE-bench-Live task FAIL_TO_PASS | Not run on base in P17 oracle comparison | **0/1** | Task remains unresolved |
| Original original-task PASS_TO_PASS failures | Not run on base | **0** | No original regression among parsed P2P |
| Original pinned harness tests parsed | Not run on base | **651** | 651 test executions, not 651 independent tasks |
| Original 2-GPU Llama3/8B DoRA visible reproduction | RESOURCE_HOLD on the standard runner | **Not run** | No CUDA/GPU or model checkpoint validation |

## 2. Exact historical source and candidate

Original source identifier: pytorch/torchtune, now meta-pytorch/torchtune, same GitHub repository. Original source commit f2bd4bc25b24587aef40f486087412b9da8f1d94. Original DoRA module torchtune/modules/peft/dora.py Git blob 6f097da6d039738c320e8775ad61950c56fe0108. Source recipe original line: `self.magnitude.copy_(weight_norm)`.

P17 modifies only that source file: when the target magnitude is still on meta, check that the calculated norm is materialized and register a new trainable Parameter from its detached computed value. When the target magnitude is already materialized, retain original in-place copy_, preserving identity. This was a hypothesis informed by the **previously observed, explicitly exploratory P16 toy mechanism** and must not be called a blind discovery of meta semantics. The replacement of a Parameter after FSDP sharding may have untested consequences for DTensor/shards/optimizer references.

Original first candidate Git SHA: 57f45fdd5552908d4b5d42cccd7359ccb4de2560. Patch SHA-256: c29fe9f9e1c2c97d6921bcb04f6a93f60a63858215fc5b4597f03446a1239801. Source test SHA-256: 4a91adf73f993650fcecfcd571b4610290e3bf6a2098f8ecae9e55fe0a8010b5. Source evidence [GitHub Actions run 44611483239](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44611483239); raw event and environment [machine receipt](../data/audits/P17_HISTORICAL_DORA_CPU_SOURCE_VISIBLE_20261120.json).

The CPU tests are built by compiling **unchanged original DoRALinear class AST nodes** and original helper functions from a Git blob-checked historical source file while supplying import-only substitutes for unrelated optional packages. The quantized torchao branch, production torchtune package import, actual FSDP/DTensor state and any two-rank GPU training were **not** exercised. Preserve this exact distinction.

## 3. Preoracle rule and chronology

The original P9 rule X1-P9-alpha-1-20261116 was run before original hidden test data access on candidate SHA 57f45... . Recorded P9 decision time 2026-11-19T20:45:51Z. **Frozen P9 decisions: self-report HOLD, local-pass ACCEPT, source-linked HOLD**. Self-report was HOLD because the AI had NOT claimed the complete original distributed task fixed; local-pass ACCEPT reflects six successful CPU tests despite incomplete task scope, and source-linked HOLD reflects missing independent agent author attestation. No human coder or genuine human developer interaction was involved.

Decision SHA-256 c62f5bffce085577ad1f5b0e4da05ec0a3a76b133e0eebd1f626bb4b2261ed35; original decision input SHA-256 11b729b8384ba928b3462072faf696c5629fcb23e6ac79338b5abae20171a31a. The original seal is retained at [GitHub Actions 44611933226](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44611933226).

**Transparent packaging erratum:** two initial, result-free original-oracle workflows 44612325881 and 44612710001 stopped at cryptographic input/decision byte verification. GitHub transferred the log-printed decision with ordinary JSON spacing, while original P9 had canonical compact decisions but hashes raw, original spaced input. The GitHub commits corrected the precise bytes **without a new policy decision**. Detailed provenance in [P17_PREORACLE_CANONICAL_BYTE_ERRATUM.md](../pilot/torchtune/P17_PREORACLE_CANONICAL_BYTE_ERRATUM.md). The first successful exact-byte gate completed before the original task was read. The deterministic synthetic Git author date in the patch commit is not evidence of actual wall-clock authorship.

Independent original evaluator run: [GitHub Actions 44613016409](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44613016409), started at 2026-11-19T20:52:56Z after the frozen decision and canonical byte validation. Exact original official harness commit ad79b850f15e33992e96f03f6e97f05ddf9aa0be, exact original dataset revision babb27e45e072219195db7a744bbf0d3c1a36e56. Unique parseable report 1. F2P passed 0/1, P2P failed 0, tests executed 651, original resolved false. Original test log SHA-256 864bb5edf03e1810a348ead57862d7a057c852df95bf56f33a4b9403f5ca1282. Archived artifact ID 14574041643. [Original oracle machine receipt](../data/audits/P17_TORCHTUNE_ORIGINAL_ORACLE_20261120.json).

## 4. Implication for acceptance versus correctness

On P17, source-specific CPU repair checks recovered, but the original independent task truth was FAIL. P9 local-pass's preoracle ACCEPT is therefore a **false acceptance for the complete original task**. This result does **not** prove that the local CPU tests themselves were wrong; they were narrow. The P9 self-report HOLD is correct for this task, and source-linked HOLD cannot be counted as a demonstrated bug detection because independent agent authorship is missing.

Across all **six distinct original-frozen tasks** now evaluated (Kedro, Babel, Faker, PDM, Matplotlib and torchtune), original oracle true task outcomes are **2 resolved / 4 unresolved**. In a deliberately labeled exploratory, mixed-stage task-level synthesis, self-report accepts 4/6 and falsely accepts 3, local-pass accepts 5/6 and falsely accepts 4, and strict actor-linked accepts 0/6 (false accept fraction among accepted **undefined**, two true-passing tasks unnecessarily held). Matplotlib contributes one post-synthetic-feedback final patch; other cases are initial candidates. This cannot support population generalization, a confidence interval, causal effect or superior source-linked accuracy. [Six-task machine ledger](../data/audits/P17_SIX_TASK_MIXED_STAGE_NONVACUITY_20261120.json).

## 5. Independent editor decision and what comes next

**KEEP:** source-anchored CPU mechanism improvement, independent unchanged hidden original task failure, dual chronology/patch SHA audit, and source-clocks/actor verification limitations. The negative result is scientifically informative because six narrow successes were not enough to establish completion.

**HOLD:** any assertion that DoRA distributed GPU training now works, a production-ready patch, FSDP stability, two GPU task reproducibility, real human developer feedback, authenticated autonomous agent identity or X1 superiority. The no-GPU resource status refers to the original two-rank visible reproducer on the standard runner; original Docker oracle was separately executed and successfully parsed its own 651 tests.

To improve the actual code, analyze the publicly visible post-reveal original task failures in a **new, explicitly POSTREVEAL** version rather than rewrite P17, and conduct source-specific distributed CPU/Gloo and eventual two-GPU tests if feasible. Any original benchmark rerun on changed code is then post-reveal engineering evidence, not a fresh blind agent-policy success. Prefer keeping P17 original task first-attempt result frozen.

Reproducibility code: [P17 candidate source recipe](../pilot/torchtune/p17_candidate_initial.py), [six CPU-source checks](../pilot/torchtune/p17_visible_original_dora_cpu.py), [runner receipts](../scripts/p17_run_visible_cpu.py), [original P9 seal](../pilot/torchtune/sealed/P9_DECISION_SEAL.json). Original GitHub Actions artifacts have finite 60-day retention. Do not publicly release raw hidden test patches or third-party binaries without licence checks. MR30 and P9–P16 remain unchanged.
