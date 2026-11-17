# Pilot cohort freeze — scope and correction

On 17 November 2026, before fetching detailed PR reviews, commit lists or CI outcomes, the 10-PR selection was publicly committed at [`0dfca364481605b12c2699296a9f948cb790b095`](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/commit/0dfca364481605b12c2699296a9f948cb790b095).

**Metadata erratum (no changes to membership):** the frozen JSON incorrectly states `distinct_repositories: 4`. The enumerated ten URLs unambiguously belong to **5** distinct repositories. This is corrected here without overwriting the frozen cohort or substituting a member. All downstream scripts must compute `len(set(case.repository))` from records and assert it equals 5.

The source query is conditioned on Copilot being *involved*, not on approval or failure. The sample consists of the lexicographically first ten **creation-time ordered** records authored by `Copilot`, after a public query for 1 September–31 October 2026. Search results included `closed_at` and `merged_at` metadata already, but no detailed per-commit CI outcomes had been consulted for these ten when the cohort was frozen.

**Pilot aim:** assess source coverage, chronology, and the feasibility of an oracle-blind, matched-information replay; NOT estimate population repair prevalence or a statistically powered improvement. All ten remain in the denominator, including duplicates from the same originating repository, unavailable paths, open PRs, and check-run failures.

Historical CI existing before analysis is retrospective observation, not a prospectively hidden new oracle. Claims of independent task correctness require an executable, held-out task verifier on the exact patch SHA after decision sealing.
