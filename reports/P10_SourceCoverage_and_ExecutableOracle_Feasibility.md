# Evidence-Based Verification of Coding-Agent Repairs — P10 source/CI feasibility audit

**17 November 2026 | Independent X1 research extension | Scientific status: diagnostic / HOLD for comparative efficacy**

## Research question

For code-repair episodes involving a coding agent, is the information available in a frozen, public PR history sufficient to decide whether that **particular agent** corrected the specific fault and whether a genuinely independent executable task test supports the correction? This is a source-admission study, not a causal claim about agent performance or a method superiority test.

## Cohort definition and provenance

Before examining the ten cases' detailed timelines or check results, commit [`0dfca364481605b12c2699296a9f948cb790b095`](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/commit/0dfca364481605b12c2699296a9f948cb790b095) froze ten public PRs. They are the first ten by creation time among `Copilot`-authored entries from GitHub Search's query `is:pr involves:copilot-swe-agent created:2026-09-01..2026-10-31`, sorted oldest first. The query returned 60 entries; 33 had that author login. Inclusion did not depend on the subsequent evaluation result. This **is not** a random or representative sample, and the selection query is itself conditioned on Copilot involvement.

The 10 PRs belong to **5** repositories (not 4; the frozen JSON's erroneous metadata field is explicitly corrected in [an immutable erratum](../protocol/P10_COHORT_FREEZE_AND_ERRATUM.md)). All ten remain in the pilot denominator. Raw public discussion/commit snapshots were preserved as separate JSON files under [`data/source/p10/`](../data/source/p10/); all snapshots passed source-frame integrity and completeness checks.

**Computed data availability:** 10/10 source records present; 42 PR commit records and 129 discussion/review events across the fixed frame; repository cluster sizes 4 care_fe, 3 Maslow_4, and 1 each in the other three repositories. These are *GitHub record counts*, not 42 independent code changes, 129 developer corrections, or independent task tests. [Reproduce](../scripts/audit_p10_source.py).

## Case-by-case source-admission register

| Frozen unit | Source observations relevant to recovery | Admissible claim |
| --- | --- | --- |
| [1 — Pflanzen.Gericht #48](https://github.com/michasng/Pflanzen.Gericht/pull/48) | An account requested Copilot to address review comments at 00:35:09 UTC on 9 Sep 2026. Copilot committed an accessibility change at 00:38:30. The postcommit `verify` CI context passed; a matched failing `verify` on the precommit SHA was not established. | **Observed correction → agent change → subsequent check**; no certified failure-to-pass recovery |
| [2 — elasticsearch #158841](https://github.com/elastic/elasticsearch/pull/158841) | The contributor discussion concerns Checkstyle version semantics; commit-author attribution includes both Copilot and another contributor, with one unresolved author. PR closed without merge. | **HOLD:** mixed actor attribution and no matched independent task oracle |
| [3 — aegis-2 #85](https://github.com/nc-sapiex/aegis-2/pull/85) | Source owner identified a TypeScript typecheck issue and directed a fix to **Claude**, not Copilot. The final corrective commit was under `nc-sapiex`; its SHA had nine green checks including `typecheck`. | **Actor-negative control:** final green checks do not establish Copilot's repair |
| [4 — Maslow_4 #1097](https://github.com/MaslowCNC/Maslow_4/pull/1097) | Requests routed via `@MaslowBot` after the recorded Copilot commits include changes to button appearance. The build summary is not a correctness oracle for those GUI requests. | **HOLD:** no same-target agent corrective test |
| [5 — Maslow_4 #1101](https://github.com/MaslowCNC/Maslow_4/pull/1101) | A specific serial-log failure was reported at 01:23:41 UTC on 20 Sep 2026, **after** the last Copilot PR commit at 00:47:36. A later repeated report also appears. | **Observed unresolved source window**; do not classify no further PR commit as proof of global failure |
| [6 — care_fe #16854](https://github.com/ohcnetwork/care_fe/pull/16854) | Initial PR and automated review/preview records exist, but no developer correction with exact independent test receipt was established. | **HOLD** |
| [7 — care_fe #16855](https://github.com/ohcnetwork/care_fe/pull/16855) | Automated reviews and preview records do not establish a human post-pushback repair/test sequence. | **HOLD** |
| [8 — care_fe #16856](https://github.com/ohcnetwork/care_fe/pull/16856) | Contains both Copilot and `yash-learner` commits and additional automated reviewer discussion. Final actor and exact correction-to-test correspondence are not identified. | **HOLD:** mixed-source code history |
| [9 — care_fe #16857](https://github.com/ohcnetwork/care_fe/pull/16857) | Public commit and automated review records exist without independently verified correction-to-task-oracle mapping. | **HOLD** |
| [10 — Maslow_4 #1103](https://github.com/MaslowCNC/Maslow_4/pull/1103) | User reported repeated serial-log failure; Copilot made several changes, including an explicit rollback, and a contributor later described a physical encoder-disconnect test. That comment is **user-reported testing**, not our reproducible test execution. | **HOLD:** multiple responses, but no admitted independent executable task oracle |

**No member of these ten has an admitted, homogeneous independent task-oracle label under the current X1 standard.** This means the cohort currently supports **zero measured repair-success labels**, not zero actual successful repairs. Do not calculate a correction success rate, false acceptance rate or unnecessary hold rate from this frame.

## Separate executable oracle infrastructure rehearsal

A **different scientific object**, a reference patch from the standard SWE-bench Lite benchmark, was actually run in Docker on public GitHub Actions, using pinned upstream commit `SWE-bench/SWE-bench@02e7a74ffd0b707aab73d203fe87bdc7c76afc8e`. In the successful [rerun with raw-artifact preservation](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44163640056), the exact reference task `sympy__sympy-20590` produced **1/1 FAIL_TO_PASS**, **21/21 PASS_TO_PASS**, and **zero harness errors**, with an actual `test_output.txt` of **434,720 bytes**. The exact execution report, patch, grader output, Docker metadata and environment lock are in archived [artifact `reference-gold-oracle-rehearsal-44163640056`](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44163640056).

This is evidence that **the official executable evaluation infrastructure works** on at least one task in our hosted runner. The patch was the benchmark's *gold reference*, not an AI-generated response to developer pushback; therefore this cannot be scored as X1 agent recovery, prospective oracle isolation, or superiority over baselines. Other SWE-bench Live pilot artifacts are independent workflow experiments and must not be pooled by default with this SWE-bench Lite gold reference.

## Methodological audit

1. **Unit of analysis:** PR for source-coverage screening; an independently certified *post-feedback correction episode* would require a separate specification and its exact code/test instance.
2. **Actor:** Neither the PR author nor a green final SHA proves that the same agent authored the decisive repair. A `Co-authored-by` trailer also requires disclosure, not dismissal.
3. **Time:** Corrective message must precede target patch; the eventual independent oracle must run **strictly after a public decision seal**, on the same patch.
4. **Test scope:** Require actual nonzero executed F2P tests with non-regressing P2P, independently frozen and unchanged by the agent. Generic build/deploy, model-review or zero-test statuses are not substitutes.
5. **No hindsight:** Historical PR reviews and source check-run outcomes already existed when this pilot was designed. Even with a frozen sampling frame, the analysis is **retrospective**. Do not rebrand it as a fully blinded prospective intervention.
6. **Concordance and uncertainty:** GitHub source names are role hints, not authenticated proof of a person's identity. Unknown commit authors and missing oracles remain unknown. All ten are reported and within-repository clustering is retained.
7. **Comparators:** The `self_report`, `local_pass` and `source_linked` rules in [P9](../protocol/research_design.md) are executable, but a valid paired effectiveness comparison needs genuinely independent task truth **for the same episodes**. This cohort does not provide it.

## Editor's decision

- **KEEP:** the pre-outcome ten-PR frame, frozen source histories, exact chronology/actor controls, and one-instance independent benchmark-infrastructure rehearsal.
- **HOLD:** a claim of actual agent recovery for any of the ten, a population recovery rate, agent-only attribution in mixed commits, matched-source CI superiority, and any false-accept/unnecessary-hold estimate.
- **NEXT:** execute a true agent patch on a separately frozen SWE-bench instance, seal its decision *before* hidden oracle execution, and use exactly the benchmark grader under a matching code SHA. Continue with a small feasibility cohort without dropping failures.
- **LOCK:** original MR30 manuscript, historical P8 diagnostic results, the initial frozen P10 cohort, and P9 software semantics.

This report was assembled through AI-assisted source screening and executable tests. No independent human coder or empirical model-efficacy result is claimed.
