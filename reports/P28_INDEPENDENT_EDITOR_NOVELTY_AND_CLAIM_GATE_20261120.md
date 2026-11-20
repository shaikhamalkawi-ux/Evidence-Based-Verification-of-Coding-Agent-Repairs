# 99llm-X1 — P28 Independent Editorial Novelty and Claim-Boundary Gate
Date: 20 November 2026. Status: **EDITORIAL-SCIENTIFIC GATE, NOT A SUBMITTED OR ACCEPTED MANUSCRIPT**. P28 adds no new original benchmark execution, no model run and no change to any P9/P25/P26/P27 evidence.

## Editor decision
**KEEP** the nine-candidate source-admission ledger and two source-original matched no-behavior-change P2P controls as a narrow, reproducible *case series*; **HOLD** the claim of an original, general-purpose verification technique or a journal-ready full-length methods paper. **GO, conditional** for a short empirical-methods note or software-engineering workshop discussion **only if** its limited objective and prior-art collision are disclosed. Stronger claims require a separate, pre-registered, actor-attributed prospective replication.

## 1. The empirical objects — source read back on the P27 head
- Frozen SWE-bench-Live lite frame: **10 selected tasks**. **9** source candidates with pre-oracle P9 decisions; Reflex had no source candidate or oracle and cannot be silently coded as failure.
- Original benchmark: **2 RESOLVED, 7 UNRESOLVED, 1 unattempted**. The official original verdicts are immutable.
- Original-endpoint attribution ledger P26: **2 original test PASS; 4 direct valid F2P FAIL; 3 UNKNOWN** (Kedro, cfn-lint, privacyIDEA).
- Two source-original negative controls, post-reveal: Kedro #4406: candidate F2P **1/1**, control **0/1**, exact named P2P failures **25/25 shared**, no candidate-only or control-only failed IDs; cfn-lint #3779: candidate F2P **1/1**, control **0/1**, exact named P2P failures **4/4 shared**, again no unique failed IDs. **These are two task-level observations, NOT 29 independent trials.**
- The historical Kedro control was already run on **17 November** and recovered, not rerun, in P27. It was registered before its own control run but **after the candidate result was disclosed**. The cfn-lint control was also post-reveal. The Kedro candidate/control ran at different times.
- An original unresolved label does not itself prove a new regression caused by an agent; equally, matching P2P failure IDs does not prove the full code correct, prove the same physical cause for every failure, or invalidate the stipulated strict benchmark grading rule.

## 2. Policy evidence: two different estimands, not a tightened interval
| Frozen P9 acceptance gate | Accepted / 9 | P26 original source-admission accepted-failure bounds | P27 *different*, posthoc F2P + no candidate-only P2P test-adequacy bounds |
|---|---:|---:|---:|
| Self-report | 5/9 | **2/5–4/5 = 40–80%** | **2/5 = 40%** |
| Local test success | 8/9 | **4/8–7/8 = 50–87.5%** | **4/8–5/8 = 50–62.5%** |
| Source-linked actor gate | 0/9 | **UNDEFINED** (0 accepted) | **UNDEFINED** |

No confidence intervals, population-risk estimates, superiority claims, policy training, or human coder agreement are warranted. The zero-acceptance source gate **held both original passing tasks**; it cannot be advertised as successful verification.

## 3. Novelty collisions — publication-stage red team
1. **Overfitting / weak tests is established APR literature**, not a discovery here: Smith et al., *Is the Cure Worse Than the Disease?* (FSE 2015, DOI 10.1145/2786805.2786825); Zemín et al., *Suitability of Test-based Patch Acceptance Criteria* (TOSEM 2025, DOI 10.1145/3702971); Wang, Pradel and Liu, *Are “Solved Issues” in SWE-bench Really Solved Correctly?* (ICSE 2026, DOI 10.1145/3744916.3764576).
2. **SWE-bench test / benchmark validity already under scrutiny:** Aleithan et al. SWE-Bench+ (arXiv 2410.06992); OpenAI (Feb 23 and Jul 8, 2026); Chen (arXiv 2610.16067, Oct 2026) directly audits agent evaluation oracles; Ding (arXiv 2610.30635, Oct 2026) studies specification–oracle gaps. These works have different experiments and cannot be treated as direct replications of our task IDs.
3. **Strongest near-overlap in the *same* SWE-bench-Live environment:** a third-party, non-peer-reviewed [microsoft/SWE-bench-Live issue #100](https://github.com/microsoft/SWE-bench-Live/issues/100), opened **23 Oct 2026**, reports environment-related F2P/P2P validity problems in 40 tasks, expressly lists **privacyidea-4251** (same as our task), a family of **cfn-lint** date-sensitive failures, and **different Kedro IDs** 4387/4580. It reports an original gold patch reproducing cfn-lint P2P failures on task 3767, including at least one exact test ID also among our #3779 four. These are the author's reported figures, **not independently reproduced in P28**. Issue #100 does NOT provide our #3779 original-source no-op comparison or our #4406 exact 25/25 negative-control pair. We must cite it prominently and not claim to be first to expose the general problem.
4. **Partial identification and risk–coverage are established:** Manski (2005, DOI 10.1016/j.ijar.2004.10.006) and Geifman–El-Yaniv (NeurIPS 2017). The bound formula and reject option cannot be claimed as novel.

**Residual defensible contribution, cautiously stated:** an auditable *worked application* that separates contemporaneous accept decisions, original strict task reports, independent exact-ID matched baseline diagnostic observations and endpoint-specific finite-frame risk bounds in one source-frozen, 10-selected / 9-decided case series. Not a new general verification algorithm, first discovery of flakiness or objective corrected leaderboard.

## 4. Six reviewer objections to answer before submission
1. **Prior-art overlap**: an October 2026 issue already diagnosed closely related SWE-bench-Live environment failures, including exactly privacyidea-4251.
2. **Sample**: 9 heterogeneous candidates across multiple stages, rather than independent matched agent rollouts; no frequency or model ranking inference.
3. **Outcome construct**: issue-specific F2P fail is a benchmark-task test outcome, not definitive demonstration of incorrect real-world functionality; a relative-P2P PASS is a narrow test-adequacy outcome, not a repaired program guarantee.
4. **Selection/diagnosis timing**: both controls selected after the candidate results and Kedro candidate/null not simultaneous; exact failure-ID overlap rejects a necessity explanation, but may not isolate a common cause.
5. **Provenance**: source SHA and GitHub run IDs are documented; independently authenticated *agent actor* provenance is lacking. A Git username or scripted assistant output is insufficient.
6. **Risk/coverage**: 0/9 accepted is a vacuous strict policy; accepted risk undefined. Policy thresholds and comparison are not prospectively evaluated or causally identified.

## 5. Conditional manuscript decision
**Do not submit a full journal article from this nine-case set as a claimed generalizable verification method.** Draft a bounded reproducibility-focused short empirical note as a working artifact, with exact IDs, frozen evidence, two distinct estimands, dated competing prior work and explicit noncausal boundaries. The note can be improved with another well-designed, genuinely prospective series; *do not perform retrospective policy resealing or expand the original denominators*. A prospective protocol can be designed without introducing a fictional human coder.

## 6. Source lock, checks and change report
P28 independently reaggregated the P25 selection/P9 rows against P26 and P27 JavaScript audit rows; **all three acceptance-gate count vectors and both sets of bounds matched**. It checked Kedro 25 and cfn-lint 4 exact shared-ID lengths and zero candidate-only P2P IDs. The archived P26 and P27 workflow jobs are successfully completed (151/151 and 157/157 were reported by their historical actions); P28 ran **no new evaluator**. Existing source JSON blobs and their Git object IDs are in `data/audits/P28_INDEPENDENT_SOURCE_REAGGREGATION_20261120.json`.

**RESULT-CHANGE STATEMENT: ZERO.** No scientific result, numerical value, original source record, dataset, patch, P9 decision, P26/P27 estimand, original official benchmark verdict, MR30 manuscript or previous GitHub PR was changed. P28 is additive editorial/novelty evidence only.

## Primary sources
- https://github.com/microsoft/SWE-bench-Live/issues/100 (unreviewed technical report, opened 2026-10-23)
- https://doi.org/10.1145/3744916.3764576 (ICSE 2026; independent larger study)
- https://doi.org/10.1145/3702971 (TOSEM 2025)
- https://doi.org/10.1145/2786805.2786825 (FSE 2015)
- https://arxiv.org/abs/2610.16067 (preprint, adjacent oracle-validity work)
- https://arxiv.org/abs/2610.30635 (preprint, different specification–oracle construct)
- https://arxiv.org/abs/2410.06992 (SWE-Bench+, preprint)
- https://arxiv.org/abs/2505.23419 (SWE-bench-Live benchmark description)
- https://doi.org/10.1016/j.ijar.2004.10.006 (Manski 2005)
- https://papers.neurips.cc/paper_files/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html (Geifman–El-Yaniv 2017)
