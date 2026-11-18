# 99llm-X1 P13 — Post-Reveal Mechanistic Correction: Regression Safety Without Issue Resolution

**Date:** 18 November 2026 (UTC)
**Status:** completed executable **POST-REVEAL DIAGNOSTIC**, NOT a new untouched trial, not a coding-agent post-feedback recovery and not an efficacy estimate. The parent P12 initial candidate's immutable pre-oracle decisions, source SHA and result remain unchanged; MR30 remains frozen.

## Research finding: two independent obligations

P12 exposed a deceptively successful coding patch: it passed all three preregistered visible group-provenance tests but failed the independent original SWE-bench-Live issue oracle (**F2P 0/3**, **P2P failures 2**). After the P12 oracle was revealed, P13 made a **separate, source-grounded mechanistic change** to preserve the original in-memory PDM Requirement objects while adding the missing group ancestry.

A controlled **post-reveal** public-test comparison shows P13 restores both groups of previously observed behavior:

| Outcome on the historical PDM task | Original upstream | P12 first patch (pre-oracle sealed) | P13 correction (post-reveal) |
| --- | ---: | ---: | ---: |
| Preregistered group-inclusion tests passed | 0/3 | 3/3 | **3/3** |
| Existing public update tests passed | 22/22 | 20/22 | **22/22** |
| Original benchmark FAIL_TO_PASS successes | Not executed on original base in this study | 0/3 | **0/3** |
| Original benchmark PASS_TO_PASS failures | Not executed on original base in this study | 2 | **0** |
| Original task resolved? | Not evaluated | No | **No** |
| Independent prospective evidence? | — | Yes, P12 first attempt only | **No; benchmark results were already revealed** |

**Main result:** P13 eliminated observed regressions and preserved all 25 applicable public checks, **but did not solve the original benchmark issue**. This cleanly distinguishes **non-regression/compatibility** from **issue-resolution correctness**; success on one axis must not be used as a proxy for the other.

## Mechanistic contrast and exact intervention

The original PDM update command builds its lock resolver input from existing parsed requirements held in **all_dependencies**. It also mutates selected Requirement objects **before** this call when requested options change the prerelease policy or version constraints.

The P12 first attempt replaced the source expression with fresh **project.get_dependencies(group)** results, recovering nested dependency-group provenance. However, this re-parsed new Requirement objects and could discard earlier in-memory edits to **prerelease** and **specifier**.

P13 changed only **src/pdm/cli/commands/update.py** on original upstream SHA **564d09acbf2c8ef6500a3864f1fa1d38b3c5cdd5**. Its [reproducible candidate recipe](../pilot/pdm/p13_candidate_postreveal.py) expands the included groups, matches each directly declared dependency to its existing object by **identify()**, preserves that original object's state and unions the resolved group memberships; for included dependencies without a direct original counterpart it uses the expanded Requirement. This is a **source-level engineering fix**, not a novel general algorithm.

Two previously failing original public tests recovered:
- **test_update_ignore_constraints** (in source [tests/cli/test_update.py](https://github.com/pdm-project/pdm/blob/564d09acbf2c8ef6500a3864f1fa1d38b3c5cdd5/tests/cli/test_update.py)).
- **test_update_existing_package_with_prerelease** (same original source).

The recovery of 2/2 public regressions under the single revised source statement is **consistent with** the object-identity mechanism. It does **not** prove this is the only underlying defect, nor that the patch addresses the original benchmark's unseen semantic requirements. Original hidden F2P stayed **0/3** in the post-reveal retest.

## Execution and source provenance

| Stage | Executed result | Public record |
| --- | --- | --- |
| P12 original base visible suite | 0 passed / 3 failed | [GitHub Actions run 44236766300](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44236766300) |
| P12 original first candidate visible suite | 3/3 passed | [Run 44236769972](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44236769972) |
| P12 existing public PDM suite, post-seal | Original 22/22, candidate 20/22 | [Run 44237704069](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44237704069) |
| P12 first candidate **original, independent, post-seal** SWE-bench-Live | 939 parsed tests; F2P 0/3, P2P failures 2; unresolved | [Run 44237374542](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44237374542) |
| P13 new correction public suites | Visible 3/3 and existing PDM update 22/22 | [Run 44238675293](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44238675293) |
| P13 **post-reveal** reuse of original task oracle | 939 parsed tests; F2P 0/3, P2P failures 0; unresolved | [Run 44238901257](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44238901257) |

**P12 exact candidate:** commit 5c5ea31661c70a7bd7ec7b661f32f380b45c1d40, patch SHA-256 53c79ba925902cfd39739be353686dd7970dc683e5716afa79b8638e974552e9. P12 policy decisions were fixed at UTC 2026-11-18T04:24:00Z and SHA-256 **bc51ef445bc321854288d882677b42c416d7d6584b55a51854d79c40a36b3503**, before the original task oracle began at 04:27:41Z. The original three policy decisions remain self-report=ACCEPT, local-test=ACCEPT, source-linked=HOLD.

**P13 diagnostic candidate:** exact reproducible Git commit 75473b04603db84fa67dc814f4d67e459a183bb0; source-base SHA and harness/dataset revision **identical to P12**. The P13 original task retest was intentionally run **after** the original P12 evaluator outcomes had been inspected. The original harness and benchmark labels were not used to generate the P13 code, but **prior exposure to task outcomes invalidates any description of P13 as an untouched benchmark rollout**. The Git name used in candidate replay is artificial and does not establish independently verified agent authorship.

The same official harness revision was used for P12 and P13: **ad79b850f15e33992e96f03f6e97f05ddf9aa0be**, dataset revision **babb27e45e072219195db7a744bbf0d3c1a36e56**. Both original evaluations produced exactly one parseable task report with 939 tests and zero setup errors. The P13 original test output SHA-256 is **a4a7d78aba6777d65aebcf9f691db1b1bbdf33e09e69839b7432d2305d72dad9**. Source-level recipe, public-workflow manifests and [machine-readable research ledger](../data/audits/P13_PDM_POSTREVEAL_RETEST_20261118.json) are committed; raw original harness reports are retained in GitHub Actions artifacts with finite retention.

## Prior-work and originality audit

Using regression tests to protect previous behavior is **not** novel. Chen et al., *When Old Meets New: Evaluating the Impact of Regression Tests on SWE Issue Resolution* (2025), develop regression-test reuse in TestPrune ([arXiv:2510.18270](https://arxiv.org/abs/2510.18270)). Li et al., *Are Benchmark Tests Strong Enough? Mutation-Guided Diagnosis and Augmentation of Regression Suites* (2026), develop STING and document benchmark test insufficiency ([arXiv:2604.01518](https://arxiv.org/abs/2604.01518)). The [official SWE-bench-Live protocol](https://huggingface.co/datasets/SWE-bench-Live/SWE-bench-Live) requires a rollout restricted to problem statement and task image, not original gold and test fields. P13 must not be marketed as a compliant blind benchmark agent result.

The **specific supported contribution** of our 99llm-X1 sequence is not new regression-test methodology: it is an auditable policy-decision/patch-SHA/test-timeline contrast, plus a demonstrably **separable** compatibility-versus-issue-resolution outcome on pinned real source. Any stronger claim of policy efficacy requires agents with independently verifiable author identity and nonzero source-linked acceptance, prespecified feedback, and a larger uniformly executable set.

## Independent editorial decision

**KEEP:** P12 as the first-attempt *negative* independent benchmark case; P13 as a separately versioned **post-reveal mechanistic diagnostic** showing recovery of both visible functionality and P2P preservation but continued F2P failure. The machine-readable ledgers make cases and tests easy to reproduce.

**HOLD:** any assertion that P13 solved the real issue, that source-linked acceptance is empirically superior, or that the original developer supplied corrective feedback. Neither iteration supports an autonomously verified agent deployment or population rates. Only 4 of the frozen 10 benchmark tasks have original pre-oracle results; six remain unexecuted.

**Next strong research step:** Do not keep optimizing this exposed PDM instance against the same original hidden oracle. Return to the next **untouched** task in the frozen frame, register the full two-stage feedback protocol and actor-provenance capture, freeze decisions, and use the independent oracle only once per submitted candidate. Build a homogeneous denominator before publishing efficacy rates. P10 historical Copilot PRs, P12 initial benchmark evidence, P13 post-reveal diagnosis and locked MR30 must remain separated.

**Artifact links:** [P12 initial negative-result report](../reports/P12_PDM_FIRST_ATTEMPT_SCIENTIFIC_FINDINGS_20261118.md); [P13 research ledger](../data/audits/P13_PDM_POSTREVEAL_RETEST_20261118.json); [P13 diagnostic plan](../pilot/pdm/P13_POSTREVEAL_DIAGNOSTIC_PLAN_20261118.json); [P13 source recipe](../pilot/pdm/p13_candidate_postreveal.py).
