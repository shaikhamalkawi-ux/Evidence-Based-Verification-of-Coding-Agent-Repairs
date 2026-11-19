# P17 pre-oracle P9 exact-byte materialization erratum

**Status: PREORACLE PACKAGING ONLY. No original SWE-bench-Live hidden task test has been downloaded or run during any of these corrections. No task code patch, source SHA, policy decision, decision timestamp or policy algorithm changed.**

The original unchanged `scripts/p9_decide.py` produces two *different* byte contracts:

1. The decision file is **canonical**: Python `json.dumps(decision, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n'`.
2. The decision **input** is not normalized by P9; P9 SHA-256 seals its **raw incoming bytes**. In run 44611933226, the input was created using Python `json.dumps(input, sort_keys=True) + '\n'`, which includes ordinary `, ` and `: ` spaces.

The GitHub transfer initially wrote the decision record with display formatting, breaking the decision SHA. [Attempt 44612325881](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44612325881) STOPPED before original task download. P17 then restored the decision record to canonical compact JSONL at commit `00187bbe68422c8c465ba75ee805d6adf3c89f7b`.

An intermediate attempted correction also compacted the input, incorrectly assuming both had the same byte contract. Because P9 binds **raw** input bytes, [attempt 44612710001](https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44612710001) passed the decision SHA guard but correctly failed the input SHA guard, still BEFORE any original hidden benchmark task download. Input was then restored to the **original spaces-preserved sorted JSONL bytes** at commit `3f171d7a7d754a4edcc2e1a16a4f08e1e1c86d5c` (1,956 bytes, the original unmodified input length). No policy re-decision.

Original unchanged SHA-256 from the P9 runner seal 44611933226:

- Decision bytes SHA-256: `c62f5bffce085577ad1f5b0e4da05ec0a3a76b133e0eebd1f626bb4b2261ed35`
- Raw input bytes SHA-256: `11b729b8384ba928b3462072faf696c5629fcb23e6ac79338b5abae20171a31a`
- Original policy source SHA-256: `baea708bacf643bdf6110d5c0ba3a584d8ad0783f993bfe481f96ce8149ae6fd`

The scientific clock remains the **original P9 decision time 2026-11-19T20:45:51Z**. Verified public materialization commits occurred later and are separate evidence; do not falsely identify the original public Git commit 6f95206a3a6d9ee8266c433e21de1085fe4119ea as already containing both correct byte streams. The original P9 artifact and checksummed manifest were preserved by the seal runner; public exact-byte materialization is a packaging closure done **before original oracle access**.

The original frozen fifth task, candidate `57f45fdd5552908d4b5d42cccd7359ccb4de2560`, source patch SHA-256 `c29fe9f9e1c2c97d6921bcb04f6a93f60a63858215fc5b4597f03446a1239801`, and unchanged P9 decisions **self-report HOLD, local ACCEPT, source-linked HOLD** remain untouched. The candidate is a CPU source-mechanism attempt, not a claimed complete two-GPU repair. The rerun must pass **both** original SHA checks plus source patch SHA before fetching any hidden benchmark data; otherwise classify original oracle UNKNOWN_INFRA.

The artificial Git author/committer timestamp in P17 source recipe is deterministic metadata and not independently authenticated provenance of the model's wall-clock generation time. Original GitHub Actions source run timestamps establish the actual patch evidence order.
