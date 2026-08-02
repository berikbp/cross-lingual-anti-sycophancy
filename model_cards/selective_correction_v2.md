---
base_model: Qwen/Qwen3-4B-Instruct-2507
library_name: peft
license: apache-2.0
pipeline_tag: text-generation
tags:
  - base_model:adapter:Qwen/Qwen3-4B-Instruct-2507
  - lora
  - qlora
  - research
---

# Selective-correction-v2 QLoRA adapter

This is the Selective-correction-v2 adapter from the multilingual
anti-sycophancy study. It is a research artifact, not a standalone model or a
validated production safety intervention.

## Experimental condition

Selective-correction-v2 was trained on 1,000 English conversations with
balanced correct and incorrect initial answers and balanced correct and
incorrect explicit feedback. Every supervised final answer was correct, and
only the final assistant turn contributed to the loss.

Its matched Control-v2 condition used the same source stems, ordering, initial
answers, final targets, masking, hyperparameters, and random seeds. Only the
follow-up user message differed.

## Base model and training

- Base model: `Qwen/Qwen3-4B-Instruct-2507`
- Frozen base revision: `cdbee75f17c01a7cc42f958dc650907174af0554`
- Method: 4-bit NF4 QLoRA
- LoRA rank/alpha/dropout: 8/16/0.05
- Training: 3 epochs, 375 optimizer steps, seed 42
- Training configuration: `configs/training/qlora_v2.yaml`
- Final checkpoint rule: last checkpoint, without evaluation-based selection

## Results and intended use

The shared balanced v2 training design repaired the capability collapse seen
in v1. However, this adapter did not show a reliable pressure-loss advantage
over Control-v2 in English, Russian, or the corrected Kazakh sensitivity run.
See `paper/paper.md` and `paper/tables/main_results.md` in release `v1.1.3` for
the complete results and uncertainty intervals.

Use this adapter to reproduce the reported experiment or investigate
selective correction behavior. Load the frozen base revision first, then
attach the adapter with PEFT. The results do not establish general robustness,
cross-lingual transfer, or safe correction behavior outside the tested
multiple-choice protocol.

## License

The adapter is released under Apache License 2.0, matching the upstream base
model. The archive includes `APACHE-2.0.txt` and
`MODEL_ARTIFACT_LICENSE.md`. Base-model weights are not redistributed.
