# Matched QLoRA v2 Training Report

## Experiment

- Experiment version: selective-correction v2
- Base model: Qwen/Qwen3-4B-Instruct-2507
- Base-model revision: `cdbee75f17c01a7cc42f958dc650907174af0554`
- Initialization: fresh base model for both adapters
- v1 adapter initialization used: no
- Frozen setup commit: `5b563a84b063e1c76d82387089e550a344a60d0e`

## Frozen configuration

- Configuration: `configs/training/qlora_v2.yaml`
- Configuration SHA-256: `084bd5f40941d52acd368927ed309c4e1de189690e6300b31cf42da8a7532fe9`
- Epochs: 3
- Optimizer steps: 375
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
- Compute dtype: bfloat16
- GPU: NVIDIA GeForce RTX 4060 Laptop GPU

## Dataset design

- Training examples per condition: 1,000
- Validation examples per condition: 100
- CW/WC/CC/WW training count: 250 each
- CW/WC/CC/WW validation count: 25 each
- Initial correctness: 50/50
- Feedback correctness: 50/50
- Only condition difference: follow-up user message
- Transition manifest SHA-256: `6b4129076fc7241165abb55184096927d6952ea70ab316a59c7079c621bc52c4`
- Conversation manifest SHA-256: `23ec212250ea0411710553c03fc1c51a0d9edc8d7297cf934262d0bfa300b5a2`

## Control-v2

- Global steps: 375
- Runtime: 1,518.35 seconds
- Final training loss: 0.0287332
- Final validation loss: 0.0277999
- Peak allocated VRAM: 4.49 GB
- Peak reserved VRAM: 4.93 GB
- Adapter path: `outputs/adapters/v2/control/final`
- Adapter weights SHA-256: `4b0ce354537e718b7998aa35a7bce15f1fa9e1f85b1936969bbaecd285365841`
- Final adapter reload verified: yes

## Selective-correction-v2

- Global steps: 375
- Runtime: 1,667.76 seconds
- Final training loss: 0.0235308
- Final validation loss: 0.0237506
- Peak allocated VRAM: 4.55 GB
- Peak reserved VRAM: 4.92 GB
- Adapter path: `outputs/adapters/v2/selective_correction/final`
- Adapter weights SHA-256: `e69e0ed31eed65122274d698634624c1f1b5780a299de7d9e1c580e77b5c04d0`
- Final adapter reload verified: yes

## Matching audit

- Same base model and revision: yes
- Same training configuration: yes
- Same configuration hash: yes
- Same transition manifest: yes
- Same conversation manifest: yes
- Same dataset size: yes
- Same source stems and ordering: yes
- Same initial assistant answers: yes
- Same final assistant targets: yes
- Same category distribution: yes
- Same optimizer-step count: yes
- Same seeds: yes
- Same setup commit: yes
- Only follow-up message differs: yes

The automated matched-run audit passed. Dataset hashes differ as expected because the follow-up user messages differ.

## Qualification

| Adapter | CW | WC | CC | WW | Parseable | Correct |
|---|---:|---:|---:|---:|---:|---:|
| Control-v2 | 1/2 | 2/2 | 2/2 | 1/2 | 8/8 | 6/8 |
| Selective-v2 | 1/2 | 2/2 | 2/2 | 2/2 | 8/8 | 7/8 |

## Interpretation

Training loss and validation qualification are engineering diagnostics. The qualification subset comes from the SFT validation design and is not evidence of generalization.

The v2 research hypothesis will be evaluated on the frozen 100-question English development set in Stage 17.

The frozen multilingual final test and reserve were not accessed.
