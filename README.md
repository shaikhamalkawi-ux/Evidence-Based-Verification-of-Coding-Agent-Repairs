# Evidence-Based Verification of Coding-Agent Repairs

**Public research-code prototype.** This repository studies what evidence is sufficient to accept or hold a coding agent's claimed repair after developer feedback. It is **not** a claim that the agent repaired a real-world issue, and **no held-out task oracle has been run by this repository** as of this release.

## Research question

Can a decision rule that links tests to the **correct patch, actor, task scope, and decision time** distinguish defensible repair evidence from self-reported success, mismatched tests, and subsequent human-authored fixes?

The prototype specifies three policies evaluated on **the same decision-time record**:

| Policy | Acceptance signal |
| --- | --- |
| Self-report | Patch applies and agent claims the repair is complete |
| Local-test | Patch applies and a visible, nonempty local test reports success |
| Source-linked | Patch applies; a predecision, nonempty passing test has the exact patch SHA and prespecified scope; the actor matches; no unrelated intervening edit |

The third rule is an **experimental candidate**, not a validated new algorithm. Each decision is recorded and SHA-256 sealed before the separate oracle is opened. The later oracle must be independently controlled, unchanged by the agent, and tied to the same patch SHA. Missing or compromised labels remain **HOLD/unknown**, never assumed failures.

## Reproduce the current software checks

Python 3.11+ is sufficient; the prototype uses only the standard library.

```bash
python3 -m unittest discover -s tests -v

python3 scripts/p9_decide.py \
  --input examples/SYNTHETIC_decision_only.jsonl \
  --out /tmp/coding-repair-decision-seal

python3 scripts/p9_reveal.py \
  --sealed-dir /tmp/coding-repair-decision-seal \
  --oracle examples/SYNTHETIC_oracle_AFTER_SEAL.jsonl \
  --out /tmp/coding-repair-synthetic-score.json
```

The example input and oracle files are **SYNTHETIC fixtures only**. The CI workflow validates the 21 unit/negative-control checks and the synthetic seal–reveal cycle. Passing CI proves only that this software behaves as tested; it does **not** validate real coding-agent repairs.

## Research protocol and evidence acquisition

See [Evidence acquisition and frozen-decision protocol](protocol/research_design.md) and [Arabic method summary](protocol/method_ar.md). A real comparison requires all of the following:

1. Freeze an untouched task frame, repository states, intended correction intervention, and test manifests before examining the outcomes.
2. Run or observe the agent's repair and capture the visible record; save the policy decisions and a public, immutable timestamped hash **before** the independent oracle is run.
3. Execute fixed, held-out tests on the exact submitted patch in an independently controlled Docker-capable environment. Save command logs, test counts, repository SHA, test-manifest hashes, and runner identity.
4. Assess false acceptance, unnecessary hold, and unadmitted outcomes with the **same evaluated denominator** across policies. Report selection bias and uncertainty; do not infer causal efficacy without an intervention design.

**Important limitations:** The post-seal reporter validates the supplied evidence fields and hashes; it is **not** itself a cryptographic attestation of a GitHub Actions run or a complete repository correctness oracle. Test-run provenance must be independently corroborated. The historical GitHub examples used to develop this protocol were observed before the prototype was tested and are not an untouched evaluation set.

## Publication and provenance

This is preliminary, non-peer-reviewed code and a research protocol. There is no assigned article DOI, validated effect estimate, or verified cross-model improvement. Previous manuscript materials are kept separate and are **not redistributed in this repository**. External datasets, benchmark patches, and contributor records retain their original authorship and license conditions. See [source provenance](provenance/SOURCE_NOTES.md) before adding third-party data.

Do not commit tokens, credentials, unpublished traces, or held-out oracle files. Keep independent oracle outputs outside the predecision workspace.
