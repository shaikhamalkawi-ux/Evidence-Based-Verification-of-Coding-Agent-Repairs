# P17 pre-oracle JSONL byte-serialization erratum

**Scope:** packaging and byte-representation correction ONLY; performed before the original SWE-bench-Live task oracle was downloaded or executed.

GitHub Actions [seal run 44611933226](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44611933226) used the unchanged original P9 policy to generate the canonical decision record, its source input, and the SHA manifest on a runner, before any original benchmark gold access.

The initial transfer from that runner log to GitHub used Python `json.dumps(..., sort_keys=True)` with normal spacing rather than the P9 source's canonical compact `separators=(',', ':')` and `ensure_ascii=False`. The semantic contents, episode, timestamps, patch SHA and policy decisions were unchanged, but the resulting bytes did NOT match the original SHA manifest. Therefore the original first oracle launch [44612325881](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44612325881) correctly STOPPED at the pre-oracle checksum gate; the hidden task row was never retrieved or evaluated in that run.

The following GitHub commits restored exactly the **original canonical sorted compact JSONL** with no decision re-evaluation or substantive edit:

- Input byte repair commit: `a1661c061c80796d3b415f6c65f0901f746596ba`.
- Decision byte repair commit: `00187bbe68422c8c465ba75ee805d6adf3c89f7b`.

Expected original, unchanged recorded hashes:

- P9 decision SHA-256: `c62f5bffce085577ad1f5b0e4da05ec0a3a76b133e0eebd1f626bb4b2261ed35`
- Decision-only input SHA-256: `11b729b8384ba928b3462072faf696c5629fcb23e6ac79338b5abae20171a31a`
- P9 policy script SHA-256: `baea708bacf643bdf6110d5c0ba3a584d8ad0783f993bfe481f96ce8149ae6fd`

Scientific claim remains: this task is original frozen index five; source CPU tests improved from 2/6 to 6/6, **no original independent task outcome had been seen by the source author**, and the initial policy remains self-report HOLD, local ACCEPT, source-linked HOLD. The original `t_decision` is preserved as the runner decision time 2026-11-19T20:45:51Z, while the corrected verifiable public materialization time is the later GitHub commit timestamp. These times are intentionally not conflated.

The next oracle workflow must verify that **both corrected source files hash to the previously generated immutable P9 seal**, and confirm it is executing the exact already-sealed candidate patch before downloading any original benchmark task record. If those checks fail, the task remains **UNKNOWN**. Do not count any failed infrastructure workflows as a code repair failure. Original P9, MR30, P10–P16 stay frozen.
