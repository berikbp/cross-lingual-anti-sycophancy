# Matched QLoRA Training Report

## Base model

- Model: Qwen/Qwen3-4B-Instruct-2507
- Revision: `cdbee75f17c01a7cc42f958dc650907174af0554`
- Quantization: 4-bit NF4
- Double quantization: enabled
- Compute dtype: bfloat16
- GPU: NVIDIA GeForce RTX 4060 Laptop GPU
- VRAM: 8 GB nominal; 7.61 GiB CUDA capacity

## Frozen configuration

- Configuration: `configs/training/qlora_v1.yaml`
- Configuration SHA-256: `521580f3739be5f4ba69d46aa54602470c69c4a1bd62a87c002bfcf0e43d99de`
- Frozen Git commit: `1474a9f7dc8d72fe04394d223fe4e3835c4b4d43`
- Epochs: 3
- Effective batch size: 8
- Learning rate: 1e-4
- Scheduler: cosine
- Warmup ratio: 0.05
- Optimizer: paged AdamW 8-bit
- LoRA rank: 8
- LoRA alpha: 16
- LoRA dropout: 0.05
- Target modules: all-linear
- Maximum length: 256
- Seed: 42
- Data seed: 42
- Checkpoint rule: final checkpoint

## Dry tests

- Control: 2/2 optimizer steps; adapter save and reload passed
- Anti-sycophancy: 2/2 optimizer steps; adapter save and reload passed
- Control peak reserved memory: 4.92 GB
- Anti-sycophancy peak reserved memory: 4.92 GB
- Temporary dry-run adapters: removed

## Control adapter

- Training records: 1,000
- Validation records: 100
- Epochs completed: 3
- Global steps: 375
- Runtime: 1,558.31 seconds (25 minutes 58 seconds)
- Final training loss: 0.01202199
- Final validation loss: 0.000000651165
- Peak allocated GPU memory: 4.49 GB
- Peak reserved GPU memory: 4.93 GB
- Final adapter path: `outputs/adapters/control/final`
- Adapter weights SHA-256: `cfcfa3c3c00874859a6aecdb395c8b6cb311d370fbb61a8decbbea5abebd0e0c`

## Anti-sycophancy adapter

- Training records: 1,000
- Validation records: 100
- Epochs completed: 3
- Global steps: 375
- Runtime: 1,610.43 seconds (26 minutes 50 seconds)
- Final training loss: 0.01145262
- Final validation loss: 0.000000123829
- Peak allocated GPU memory: 4.54 GB
- Peak reserved GPU memory: 4.90 GB
- Final adapter path: `outputs/adapters/anti_sycophancy/final`
- Adapter weights SHA-256: `4fb7b0aa1102cc1bae26854513e915c4e62a903a899d948b91fdec8500799ccc`

## Matching audit

- Same base model and revision: yes
- Same configuration hash: yes
- Same optimizer and scheduler: yes
- Same epoch count: yes
- Same optimizer-step count: yes
- Same seeds: yes
- Same software and CUDA versions: yes
- Same GPU: yes
- Same source stem ordering: yes
- Same final-answer targets: yes
- Only follow-up user message differs: yes
- Matched-run audit: passed

The training and validation file hashes differ as expected because the frozen
follow-up user messages differ between conditions.

## Adapter qualification

The fixed subset consists of the first 10 frozen SFT-validation records. It
was not selected using adapter performance.

| Condition | Parseable | Correct |
|---|---:|---:|
| Control | 10/10 | 6/10 |
| Anti-sycophancy | 10/10 | 7/10 |

Both final adapters loaded from disk and produced deterministic, parseable
JSON responses.

## Interpretation

Training and validation losses are engineering diagnostics. Qualification
accuracy is also an engineering sanity check because the questions belong to
the SFT validation set. None of these values is evidence that the
anti-sycophancy intervention succeeded.

Intervention success will be determined later using the frozen evaluation
protocol. No master-pool or final-test question was evaluated during Stage 12.
