# 99llm-X1 P12 — An Exact-Patch Visible-Test Pass That Failed an Independent Task Oracle

**Scientific status:** single-task, source- and execution-backed initial-attempt demonstration; not a recovered repair after developer feedback, a causal evaluation, or a validated superior acceptance policy.

**Date:** 18 November 2026 (UTC). **Project boundaries:** MR30 is unchanged. The P10 naturalistic Copilot pull-request cohort remains separate. No human second coder or real human developer feedback was employed.

## Executive finding

A GPT-6 research-generated patch to the historical PDM dependency-manager source passed all **three preregistered, developer-visible tests**, while its untouched, independently executed original SWE-bench-Live task oracle **failed all 3 FAIL_TO_PASS tests and regressed 2 PASS_TO_PASS tests**. The original harness parsed **939 tests** on the exact candidate SHA. An additional **post-seal** run of PDM's existing public update suite found **22/22 passing** on the unchanged upstream base versus **20/22 passing** on the first patch, identifying two real regressions absent from the three narrow gate tests.

**This is a negative result for the first repair, not a negative result for the entire coding-agent research question.** It exhibits why narrow self-selected tests and patches cannot substitute for independent held-out task evidence.

## Frozen selection, source and outcome order

The already frozen SWE-bench-Live lite task frame contains ten distinct-repository instances chosen by deterministic ID hashing. The first case, Kedro, was already evaluated in P11. P12 used **the next previously unevaluated case in frozen order**, the second record, **pdm-project__pdm-3419**. The P12 protocol and three visible tests were committed before writing the proposed code change, and none of the task's original hidden test patches or reference gold patch was read during candidate generation.

| Controlled item | Frozen value / source |
| --- | --- |
| Task | pdm-project__pdm-3419 |
| Historical upstream | pdm-project/pdm at 564d09acbf2c8ef6500a3864f1fa1d38b3c5cdd5 |
| Dataset | SWE-bench-Live lite, revision babb27e45e072219195db7a744bbf0d3c1a36e56 |
| Original official harness | microsoft/SWE-bench-Live at ad79b850f15e33992e96f03f6e97f05ddf9aa0be |
| First candidate commit | 5c5ea31661c70a7bd7ec7b661f32f380b45c1d40 |
| First patch SHA-256 | 53c79ba925902cfd39739be353686dd7970dc683e5716afa79b8638e974552e9 |
| Decision timestamp (UTC) | 2026-11-18T04:24:00Z |
| Pre-oracle decision SHA-256 | bc51ef445bc321854288d882677b42c416d7d6584b55a51854d79c40a36b3503 |
| Original oracle started (UTC) | 2026-11-18T04:27:41Z |
| Original oracle artifact | [pdm-gpt6-initial-heldout-oracle](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44237374542/artifacts/14397996854) |

The source edit was limited to **src/pdm/cli/commands/update.py**. It replaced the original collection of already-parsed requirements from each dependency group with calls to **project.get_dependencies(group)**, expanding the included group's provenance. The modified candidate Git commit was built reproducibly in GitHub Actions with an **artificial name and timestamp** to lock its SHA; this **does not independently attest autonomous software-agent authorship**.

The original protocol said to issue a single developer-style **synthetic** corrective request only if the initial visible suite exhibited a real failure. As the first candidate passed 3/3 visible tests, **no developer feedback, no synthetic corrective intervention and no second candidate were manufactured**. The task's scientific scope is **INITIAL ATTEMPT ONLY**.

## Executed evidence by evidence tier

| Evidence tier | Unmodified historical base | First proposed patch | Time relative to lock | Interpretation |
| --- | --- | --- | --- | --- |
| Three preregistered visible group-provenance tests | 0 passed, 3 failed | **3 passed, 0 failed** | Before seal | Narrow regression addressed; this is not the task oracle. |
| Twenty-two existing public PDM update tests | **22 passed, 0 failed** | 20 passed, **2 failed** | After seal | Candidate caused additional public regressions; these results cannot retroactively change the sealed acceptance decisions. |
| Original SWE-bench-Live hidden task verifier | Not executed on the base in this P12 comparison | **0/3 F2P passed; 2 P2P failed; 939 tests executed** | After seal | Valid failed independent task verdict for the exact first candidate under the pinned harness and dataset. |

The two additional **public** regressions were:
- [test_update_ignore_constraints](https://github.com/pdm-project/pdm/blob/564d09acbf2c8ef6500a3864f1fa1d38b3c5cdd5/tests/cli/test_update.py), concerning an unconstrained update.
- [test_update_existing_package_with_prerelease](https://github.com/pdm-project/pdm/blob/564d09acbf2c8ef6500a3864f1fa1d38b3c5cdd5/tests/cli/test_update.py), concerning pre-release selection.

A plausible, **not yet experimentally isolated**, mechanism comes from upstream source: before collecting the requirements passed to the lock resolver, the update command adjusts the previous parsed Requirement objects' **prerelease** and **specifier** fields for selected packages. The initial patch creates **new Requirement objects** with project.get_dependencies(group), potentially discarding these transient mutations while recovering group-membership annotations. This explanation must remain **hypothesis**, not proven cause of all three original hidden F2P failures.

Execution receipts:
- [Original base visible tests: 3 failed](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44236766300)
- [Initial candidate visible tests: 3 passed](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44236769972)
- [Timestamped pre-oracle seal and decisions](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44237029383)
- [Public update regression suite, post-seal](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44237704069)
- [Original independent SWE-bench-Live evaluation, post-seal](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44237374542)

## Three policies, locked before independent outcomes

The unchanged P9 decision script read the same pre-oracle record for all three policies. It produced:

| Frozen acceptance rule | Pre-oracle decision | Original task truth | In this *one task* |
| --- | --- | --- | --- |
| Self-report | ACCEPT | FAIL | False accept (count 1) |
| Visible local test | ACCEPT | FAIL | False accept (count 1) |
| SHA/scope/actor-linked | HOLD | FAIL | Correct hold (count 1) |

The stronger gate's HOLD is due to **missing independent agent-author attestation**, *not* because its algorithm had been shown to identify the hidden PDM bug. Never call a zero-false-accept count from a zero-accept rule empirical superiority. As the stronger gate accepted **zero** tasks, its false-accept rate among accepted tasks is **undefined**, not 0%.

A current **four-task descriptive** snapshot (Kedro, Babel, Faker and now PDM), all **INITIAL ATTEMPT ONLY**, gives:

| Policy | Accepted of 4 | False accepts (count) | True-passing tasks held |
| --- | ---: | ---: | ---: |
| Self-report | 3 | 2 | 1 |
| Local-test | 3 | 2 | 1 |
| Source-linked | 0 | 0 | 2 |

Across the four original hidden task oracles, **two candidates passed and two failed**. The original prespecified ten-task benchmark contains **six members not independently executed**. Four cases are neither a powered sample nor a causal superiority experiment; these case counts are diagnostic and must not be combined with the separate ten-Copilot-PR P10 source-only dataset.

## Editor-style independent assessment

**Supported contribution:** A well-controlled counterexample showing that passing a narrowly relevant local suite is insufficient to establish task repair, strengthened by an external pinned task oracle and a separate public regression suite which detected regressions after decisions were frozen. Exact candidate, task, decision and independent evaluation times are on GitHub. The contrast between recovery of group provenance and unintended loss of version-constraint behavior generates a falsifiable mechanistic hypothesis.

**Not supported:** A successful two-stage coding-agent correction; an independent Copilot rollout; a human-coded audit; a causal advantage of SHA-linked acceptance; a confidence interval for policy superiority; model-wide false-accept prevalence; or proof that the proposed replacement statement is the only cause of the task's hidden failures.

**Editorial rating:** KEEP this P12 negative-result case as detailed mechanistic and evidence-sufficiency support. HOLD any efficacy or autonomous-agent claims. Do not change the locked MR30 manuscript merely to inflate this extension. A stronger stand-alone article requires independently authored and verified agent commits that give the strict gate some eligible ACCEPTs, an actual standardized corrective-feedback stage, and sufficient cases with independent tasks and common denominators.

## Reproducibility and research ledger

Machine-readable provenance and truth boundaries: [P12_PDM_INITIAL_ORACLE_20261118.json](../data/audits/P12_PDM_INITIAL_ORACLE_20261118.json). The preserved GitHub Actions artifacts contain candidate patches, pinned dependency environment and original independent test output. Software guard tests verify frozen source selection, original pre-oracle decision bytes, timing and exclusion of post-feedback claims, but do not in themselves reproduce Docker's original test execution.

If the PDM patch is repaired now using the failed public or hidden results, that is **post-reveal development** on an already exposed task and must be archived as such, without being counted as a new blind or prospective success. For a genuine post-feedback trial, choose an untouched next member of the original ten-task frame and preregister the full two-stage and actor-evidence process before any hidden oracle access.
