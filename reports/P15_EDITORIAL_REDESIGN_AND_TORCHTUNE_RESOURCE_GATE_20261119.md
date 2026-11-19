# 99llm-X1 — P15 External Editorial Redesign and Prospective Resource Gate

Date: 19 November 2026. Status: protocol + real GitHub resource preflight; NOT new repair results. MR30 and original P9/P10–P14 frozen.

## Primary methodological blocker

Original P9 source-linked policy accepted ZERO evaluated benchmark tasks because deterministic Git replay labels do not independently authenticate the model/agent author. The zero false-accept COUNT is therefore vacuous. False-accept RATE among accepted cases is UNDEFINED; no claim of superiority is defensible. The original five task-level oracle evaluations comprise two passes and three failures; Matplotlib has two correlated stages but one task. P13 is post-reveal diagnosis, not another blind task.

Do NOT relax original P9 retrospectively. If the paper claims X1 is empirically superior, that claim must be held. The existing defensible claim is an evidence-sufficiency audit: visible/local tests can pass while the independent issue oracle fails.

## Separate evidence axes

Actor/source integrity: (P1) exact source base, patch hash and resulting Git SHA; (P2) verifiable GitHub runner, workflow code and receipt; (P3) independently authenticated actor identity and model-call/tool-execution trace bound to output patch bytes. P1 or P2 NEVER imply P3; a fabricated Git author name is not agent attestation.

Task verification: (V1) nonzero predeclared visible local tests on exact patch SHA; (V2) public original regression tests on exact patch, with skips separate from passes; (V3) independently executed original pinned task benchmark F2P and P2P. V3 is outcome truth obtained only AFTER decisions sealed, not an admission-policy input.

Forward comparators: (A) frozen P9 self report and local pass; (B) prospectively preregistered PROCESS-linked exact-patch+V1+V2 gate that makes no actor-authentication claim; (C) independent actor-attested gate only if genuine P3 evidence exists. Name B differently from original P9 source-linked policy. Run all on the SAME preregistered information budget, freeze BEFORE original hidden task oracle; report coverage, false accepts, unnecessary holds. If accepted count = 0, selective failure risk among accepted is UNDEFINED, never 0%.

Statistical unit = unique original benchmark task. Candidate revisions within one feedback session form a paired transition only, not independent samples. A five-task feasibility case series is not proof of population rates or causal efficacy.

## Preserve the next frozen task, torchtune

Original frame index 5: pytorch__torchtune-2139, commit f2bd4bc25b24587aef40f486087412b9da8f1d94, frozen statement SHA 31a8dfd18349fa14a79aa3958c6f166a475dd8f8cd4a48a098bf38a16e3b1cdf. GitHub repository was renamed from pytorch/torchtune to meta-pytorch/torchtune (stable repository ID 707869465); task and source remain unchanged.

Original visible reproducer: tune run --nnodes 1 --nproc_per_node 2 lora_finetune_distributed --config llama3/8B_dora. Reported error: Unexpected param or buffer ... on meta device. The historic distributed recipe creates on meta, shards, loads state and initializes DoRA magnitude. The historic recipe integration test uses @gpu_test(gpu_count=2) and may download remote assets; unit tests are lighter but are not the same reproduction.

First execute the read-only actual GitHub-hosted GPU preflight. If two accessible GPUs are unavailable, record RESOURCE_HOLD for full original distributed reproduction, not code failure. Small CPU/micro model probes may investigate code but cannot claim equivalent full training success. The original SWE-bench-Live pinned Docker oracle may have its own requirements; evaluate its feasibility separately and never invent results. DO NOT skip torchtune or replace the fifth task with an easier one.

## Prospective execution steps

1. Lock task source / visible test scope / external data admission, resource profile and original sample frame, before a candidate.
2. Run the actual AI coding agent under a controlled transcript with source authenticity; record model-call IDs, tool calls, exact output patch bytes, actor identity evidence and timestamps. A self-created log only establishes local traceability, not provider-signed independent identity.
3. Generate initial code and issue exactly one scripted, AI-labeled corrective message only if triggered by a real visible test failure; retain both stage patches and exact source SHAs.
4. Freeze both pre-oracle decisions using original P9 policy and a separately labeled prospective process gate if justified. Use source/actor eligibility codes, not arbitrary exclusion.
5. Only then execute original independent task oracle on each exact patch. Missing/zero tests, infeasible hardware and changed Docker test manifests are UNKNOWN or RESOURCE_HOLD, not FAIL.
6. Archive runnable code, receipts and raw test logs, with permanent repository/DOI when possible. Report all frozen tasks and unadmitted cases transparently.

## Editorial decision

Keep P12–P14 negative results in a transparent technical evidence paper. HOLD superiority of X1, validated agent authenticity, genuine human developer interaction, population risk estimates and proof that an improved visible suite resolves the original issue. No human coder or intercoder experiment required. Do not overwrite frozen MR30.

Relevant public references: https://swe-bench-live.github.io/ (August 2026 trajectory requirement and anti-leakage); https://github.com/meta-pytorch/torchtune/blob/f2bd4bc25b24587aef40f486087412b9da8f1d94/CONTRIBUTING.md (resource/test tiers); https://arxiv.org/abs/2609.08149 (task verifier/reward hacking concerns). These are conceptual precedents, not X1 validation.

## Executed P15 resource-admission outcome (19 November 2026)

Real GitHub Actions execution: https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44603543854

The standard ubuntu-24.04 runner exposed NO NVIDIA GPU device nodes, did not contain nvidia-smi, and did not have torch installed. The original published reproducer requests TWO local worker ranks. Under the preregistered resource rule, this is RESOURCE_HOLD_FULL_TWO_GPU_REPRO FOR THIS RUNNER ONLY. It is not proof that other cloud computers lack GPUs and NOT a judgement on the repair or the independently scored original benchmark task. No candidate patch was submitted and no gold/test_patch was read.

Exact machine-readable receipt: data/audits/P15_TORCHTUNE_ORIGINAL_RESOURCE_PREFLIGHT_20261119.json. Runner result original GitHub Actions artifact ID: 14568278992. Source software/negative controls passed 52/52 in https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44604485698 .

Cloud next step: use a same-node 2-GPU runner with adequate VRAM and model/checkpoint permissions if a full original distributed DoRA reproduction is required. GitHub's published larger GPU runner reference lists ONE Tesla T4 (16GB) per GPU runner, which is not equivalent to a same-node two-GPU machine: https://docs.github.com/en/actions/reference/runners/larger-runners . A self-hosted two-GPU runner or a separately approved cloud VM can satisfy the hardware requirement. Verify actual hardware/driver/device counts before any repair experiment, without claiming that two available GPUs alone prove the 8B workload has enough memory or downloaded assets.

Crucial benchmark boundary: The SWE-bench-Live website's August 2026 update requires original agent rollout trajectories for leaderboard submission integrity: https://swe-bench-live.github.io/ . Prior P12/P14 executed the pinned original harness and obtained F2P/P2P outcomes, but do NOT describe those as independently authenticated leaderboard submissions. Deterministic research-generated patch scripts do not constitute provider-signed agent rollout evidence. This is another reason for a prospective workflow-trace/actor-proof protocol.

Author recommendation after resource preflight: Keep task index 5 frozen, record the full-reproduction resource hold, and prioritize a genuinely verifiable model/tool-to-patch execution chain plus non-vacuous acceptance coverage in the next study. MR30 and original P9 scientific results remain unchanged.
