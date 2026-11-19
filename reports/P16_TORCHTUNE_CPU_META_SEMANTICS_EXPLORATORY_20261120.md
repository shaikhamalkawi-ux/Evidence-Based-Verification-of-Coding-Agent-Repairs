# 99llm-X1 P16 — CPU-only PyTorch meta Parameter operation probe

**Status:** Executed CPU-only exploratory diagnostic, NOT a torchtune task fix. No candidate patch submitted. No hidden benchmark tests retrieved. Original P9 policy, prior five-task task results, P15 resource HOLD, and MR30 unchanged.

## Observed source-anchored mechanism

The originally frozen task is pytorch__torchtune-2139, historical source commit f2bd4bc25b24587aef40f486087412b9da8f1d94 in the same GitHub repository now named meta-pytorch/torchtune. The original historical DoRALinear source file torchtune/modules/peft/dora.py (Git blob 6f097da6d039738c320e8775ad61950c56fe0108) calls **self.magnitude.copy_(weight_norm)** inside initialize_dora_magnitude. The distributed recipe (historical Git blob e95fbb40c60c0d7f18e694aeb8dabac5a70e664b) constructs a model on meta, then initializes adapters, loads base weights, initializes DoRA magnitude and checks no parameters remain on meta.

The one **isolated toy CPU experiment** instantiated an nn.Parameter on meta, used precisely that copy_ operation with CPU tensor values [2.0, 3.0, 4.0], then compared a separate explicit to_empty(device='cpu') materialization step. Actual GitHub Actions run 44607950785 with torch 2.10.0+cpu observed:

| Isolated toy observation | Observed result |
| --- | --- |
| Initially a meta Parameter | True |
| Copy CPU tensor into meta Parameter raises? | No |
| Does Parameter still report device=meta after copy_? | **Yes** |
| After explicit Module.to_empty(device='cpu') | Parameter is **not** meta |
| Then copy the same three CPU values | Exact [2.0, 3.0, 4.0] |

The two declared CPU semantics conditions **both passed** in the actual runner. This supports an underlying PyTorch property worth checking in the actual torchtune DoRA initialization path. It is **not** an isolated proof of the original DoRA training failure's root cause: the toy module has no DoRALinear class, torchao quantization, FSDP shards, DTensor, two worker ranks, checkpoints or real 8B model. In particular, calling to_empty on a real FSDP-managed sharded module might be incorrect. **Do not recommend to_empty as a production patch based solely on this microexperiment.**

This experiment's pre-registration status is explicitly **exploratory after an initial local sanity check**. It cannot be presented as blind or prospective code-repair evidence.

## Original benchmark and resource status

P15 independently executed a resource check in GitHub Actions run 44603543854. That standard runner had no accessible NVIDIA devices or nvidia-smi and no imported PyTorch at the time. Its classification RESOURCE_HOLD_FULL_TWO_GPU_REPRO applies only to the **original visible two-GPU distributed training reproducer on that runner**. A separate eligible two-GPU environment and original data/checkpoint authorization would be needed for the complete reproduction. The original SWE-bench-Live Docker oracle is a separate verification route and has **not** been executed for this torchtune candidate.

Original task index 5 remains unchanged in the frozen ten-task frame. No torchtune task candidate was generated or accepted/rejected. The original five distinct tasks with previously executed original benchmarks remain five; P16 does not add a sixth.

## Reproducibility

- Exact historical torch/DoRA source: https://github.com/meta-pytorch/torchtune/blob/f2bd4bc25b24587aef40f486087412b9da8f1d94/torchtune/modules/peft/dora.py
- Original distributed recipe: https://github.com/meta-pytorch/torchtune/blob/f2bd4bc25b24587aef40f486087412b9da8f1d94/recipes/lora_finetune_distributed.py
- Executable self-contained toy script: ../scripts/p16_meta_magnitude_cpu_probe.py
- Claim boundaries/limitations: ../protocol/P16_CPU_META_SEMANTICS_BOUNDARIES_20261120.json
- Machine-readable CPU execution receipt: ../data/audits/P16_CPU_META_MAGNITUDE_OBSERVED_20261120.json
- Original executed GitHub Actions run: https://github.com/shaikhamalkawi-ux/Evidence-Based-Verification-of-Coding-Agent-Repairs/actions/runs/44607950785
- Original GitHub Actions artifact ID: 14570827656 (finite 60-day retention)

This mechanistic diagnostic does not resolve the non-vacuity blocker established in P15. Future source-linked policy experiments still require independently authenticated agent attribution, or a distinctly named process-only gate tested prospectively. No human second coder is requested.

**Conclusion: KEEP as supporting source-grounded exploratory mechanism, HOLD all claims of actual distributed DoRA repair, GPU training success and original independent benchmark efficacy.**
