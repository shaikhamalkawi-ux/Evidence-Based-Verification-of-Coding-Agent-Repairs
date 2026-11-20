# 99llm-X1 P19 — Typed DSPy Demonstration Serialization: Source Recovery Without Original Task Resolution

**Date:** 20 November 2026 UTC. **Scientific status:** original frozen sixth task executed, original benchmark **UNRESOLVED**. This is a negative source-to-task adequacy case. Original P9, P10–P18 and MR30 remain untouched.

## Main finding

The first GPT-6-generated DSPy source candidate changed how typed List[str] output demonstrations are serialized in historical ChatAdapter. Nine PRE-FROZEN source-AST tests improved from historical baseline **3/9** passing to **9/9** on the first patch. A later, wholly separate, postseal execution of the original public functional regression tests passed **51/51 for both source states**, with zero errors/skips/failures. Nevertheless the original pinned SWE-bench-Live task oracle executed **261 tests**, passed **0/4 FAIL_TO_PASS** checks, had **0 PASS_TO_PASS regressions**, and marked the original DSPy issue **UNRESOLVED**.

| Evidence tier | Historical base | First P19 candidate | Boundary |
| --- | ---: | ---: | --- |
| Nine preregistered, original-source ChatAdapter AST tests | 3/9 | **9/9** | Narrow typed demo contract only |
| Postseal original public functional tests (two unchanged files) | 51/51 | **51/51** | No observed regressions on these 51; NOT hidden task oracle |
| Original independent task FAIL_TO_PASS | Not re-executed in this original task comparison | **0/4** | Original issue NOT resolved |
| Original task PASS_TO_PASS failures | Not re-executed on base | **0** | No observed P2P regressions |
| Original task total parsed tests | Not re-executed on base | **261** | 261 tests are NOT 261 independent coding tasks |
| Remote Databricks LM + CoNLL end-to-end optimization | NOT RUN | **NOT RUN** | No external provider/model credentials or data used |

## Frozen source, sample and visible mechanism

The task was the ORIGINAL sixth of ten source-frozen SWE-bench-Live lite tasks: stanfordnlp__dspy-1609. Historic DSPy base commit 16ceaba5f7126ca86e5b50b669975c926b9f8f55, file dspy/adapters/chat_adapter.py Git blob 5a20dcff321e3aded9c32039d9c060aa79a5e1ea. Frozen visible problem statement SHA-256 5915cc3207d8269cdc125cb1d6dcf6e74fbf90464dd216f95d0878b4d4e2f210. Original problem reports TypedPredictor List[str] predictions working but BootstrapFewShot optimization failing with a Trailing data JSON decoder error on a remote hosted LLM.

Source-only mechanism hypothesis, registered BEFORE candidate: typed list-valued demonstrations in ChatAdapter use a human-readable list representation, while TypedPredictor's output parser expects a JSON array. The first patch conditionally serializes LIST/TUPLE assistant demo values to JSON when the output field actually has a TypedPredictor parser; untyped output demos, user inputs, and scalar outputs retain prior formatting. This hypothesis is plausible but DOES NOT establish the remote optimization exception's complete cause.

Frozen visible test source: pilot/dspy/p19_visible_original_adapter_ast.py, SHA-256 c8c47bf6ae3c641c47683d2becb181ee208f397309e81055bc09a3cc43f51104. The test harness compiles the actual historical ChatAdapter functions and class source AST, using import-only stand-ins for unrelated package bootstrapping, and real Pydantic 2.9.2. Typed List[str], list[str], nested Pydantic models, unicode/quotes, empty lists, untyped lists, list inputs, scalar output, and a complete adapter demo parse are tested. Nine tests were frozen before code generation. The base had 3 pass, 1 assertion failure and 5 errors; the first candidate 9 pass, 0 fail/errors. Baseline [run 44666172721](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44666172721); candidate [run 44666349696](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44666349696). The new original-context first patch Git SHA is 2a2938cbd2b616c684768902bdcc0bfc09e7b9a4; exact patch SHA-256 e9771581fa04391b72b86f0da93495c0749e6f10f84452a83c4e8d2968a98a08. Synthetic Git metadata are NOT independent agent-authorship verification.

## Two separate preoracle policy decisions

Before the original held-out task test was downloaded, GitHub Actions [seal run 44666717097](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44666717097) applied the UNMODIFIED original P9 policy and a DISTINCT prospective artifact-only process rule (P19-v1). Both were frozen at **2026-11-20T03:17:43Z** and publicly committed by seal commit 241dbe9f626b6ea880926e25d40888d5159884a9. Original P9 decisions SHA-256 caaf84674bbe01354a6710803c383554ee48d44ac9b60c2a30a576437d0d6d6b; separate process decision SHA-256 c0dab6c34c148c878d2b2befe33e8fe67100849f8f80deb7938f3acec61d0515.

| Frozen policy | Before held-out test | Original task outcome | Interpretation |
| --- | --- | --- | --- |
| P9 self-report completion | HOLD | FAIL | No original full-task completion claim was made |
| P9 local test success | **ACCEPT** | FAIL | Original-task false accept; nine checks too narrow |
| P9 actor-source-linked | HOLD | FAIL | Actor attestation missing, NOT a demonstrated bug detector |
| NEW artifact-linked/no-actor P19-v1 | **ACCEPT** | FAIL | Prospective first-case false accept; not original P9 |

The process gate requires exact source, candidate and receipt SHA, nine pre-frozen visible passes, no skips/errors and source-only controls, but does not require independently authenticated model-agent authorship. P19 reveals that even a strong source-artifact chain cannot compensate for missing end-to-end task behavior coverage. The correct research choice is to report both acceptance and risk; no one-task superiority claim. Zero task-level accepted under original actor-source-linked policy still means the false-accept RATE among accepted is **UNDEFINED**, not 0%. No human coder or independent human developer was invented.

## Original independent benchmark

Only AFTER both seals and exact Git code SHA validation, the original benchmark task was fetched in the official evaluator. Original pinned dataset SWE-bench-Live/SWE-bench-Live lite revision babb27e45e072219195db7a744bbf0d3c1a36e56, original pinned harness commit ad79b850f15e33992e96f03f6e97f05ddf9aa0be. Executed run [44666993268](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44666993268), original harness code SHA-256 9a9361d7c53f64d573ef546325b6f13d5b593fa78b4ddcbaa380efa0cd0aac04, original raw test output SHA-256 f80810c03c46a09b5b79499a4aa0f7ca8c8d97d8a56cad675eb3d32c5cc26a48, original output artifact ID 14598665908. The original report is unique and valid: F2P 0/4, P2P failed 0, 261 tests parsed, official resolved false, no evaluator-level setup errors. Machine ledger: [P19_DSPY_INITIAL_ORIGINAL_TASK_ORACLE_20261120.json](../data/audits/P19_DSPY_INITIAL_ORIGINAL_TASK_ORACLE_20261120.json).

## Original public regression source QA — POSTSEAL ONLY

Original historical tests/functional/test_functional.py and tests/functional/test_signature_typed.py were independently executed on the original base and exact first patch. The first infrastructure attempt [44667385576](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44667385576) was unable to collect because modern LiteLLM no longer supports old disk cache settings; a second infrastructure attempt [44667619747](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44667619747) used a nonexistent legacy version and also executed zero tests. Neither is counted as a code-regression finding. A pinned historic-compatible LiteLLM v1.53.1, with disk cache type still defined, allowed unchanged tests to run. Final [run 44667789516](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44667789516): 51 passed, zero skipped/failed/error on BOTH code states. This test run occurred after decisions were sealed and cannot enter those original policy decisions. Machine evidence: [P19_POSTSEAL_ORIGINAL_PUBLIC_REGRESSION_20261120.json](../data/audits/P19_POSTSEAL_ORIGINAL_PUBLIC_REGRESSION_20261120.json).

## Seven-task bounded synthesis and next contribution

There are now **SEVEN distinct frozen original benchmark tasks** with admitted original verifier results: 2 successfully resolved and 5 unresolved, leaving 3 originally frozen tasks without results. In a clearly labeled EXPLORATORY mixed-stage comparison (one Matplotlib post-synthetic-feedback final patch and six initial patches), original P9 self-report accepts 4/7 with 3 false accepts; local-pass accepts 6/7 with **5 false accepts**, while original actor-linked policy accepts 0/7, abstaining even on both actual successes. The novel P19-v1 process-only gate is observed on ONE newly preregistered case and accepted that incorrectly resolved case. None of this proves a population causal effect, calibration or superiority. Machine ledger: [P19_SEVEN_TASK_MIXED_STAGE_NONVACUITY_20261120.json](../data/audits/P19_SEVEN_TASK_MIXED_STAGE_NONVACUITY_20261120.json). P10 naturalistic Copilot PRs and P18 exposed-oracle error-text ablations have separate denominators; they are not secretly added to this panel.

**Editorial direction:** Source lineage integrity, source/actor authentication and task verification scope must be separately represented. A nonvacuous admission gate requires a credible task-to-test coverage argument, not only a green prespecified local test set. This is a research hypothesis for a NEW, forward-registered protocol, not a retroactive rewrite of P9 results or a demonstration of an original new optimizer. The 7-task sample is still small and heterogeneous. Original MR30 and all P9–P18 scientific baselines are not modified.

## Reproducibility and claim status

Keep: exact frozen ten-case task ID, source hashes, original baseline and patch, nine AST tests, preoracle dual-policy seal, independently executed held-out task verifier, original public 51/51 regression contrast, and versioned machine-readable ledgers. Hold: proof of complete Databricks/CoNLL optimization, original issue full resolution, authenticated autonomous model actor, human coding, superiority of X1, confident generalization, and permanent raw evidence archive. GitHub Actions raw artifacts currently have a 60-day retention policy and need a license-compatible permanent deposit for journal reproducibility.

**Final P19 status: source-level behavior recovered, original hidden task still UNRESOLVED. Source-identity-only checks were insufficient to guarantee task correctness.**
