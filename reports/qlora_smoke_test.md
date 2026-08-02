
# QLoRA Smoke-Test Report

This was a pre-study hardware and adapter-reload check. It is not one of the
matched v1 or v2 training runs and its loss is not a research result.

## Model

- Model ID: Qwen/Qwen3-4B-Instruct-2507
- Frozen revision: cdbee75f17c01a7cc42f958dc650907174af0554
- Quantization: 4-bit NF4
- Double quantization: enabled
- GPU: NVIDIA GeForce RTX 4060 Laptop GPU
- VRAM: 8 GB

## Training configuration

- Examples: 20
- Optimizer steps: 20
- LoRA rank: 8
- LoRA alpha: 16
- LoRA dropout: 0.05
- Target modules: all-linear
- Batch size: 1
- Gradient accumulation: 1
- Maximum length: 256
- Learning rate: 2e-4
- Optimizer: paged_adamw_8bit
- Gradient checkpointing: enabled

## Results

- Training completed: yes
- Training runtime: 10.81 seconds
- Mean training loss: 0.5218
- Trainable parameters: 16,515,072
- Trainable percentage: 0.7431%
- Adapter saved: yes
- Adapter reloaded: yes
- Reloaded inference completed: yes
- Reloaded response:

```text
The correct answer is 99.
{"answer": "B"}
```
