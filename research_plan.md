# Research Question

```
Can synthetic anti-sycophancy fine-tuning reduce harmful
answer changes in Qwen2.5-1.5B-Instruct?

Does that improvement transfer from English to Russian and Kazakh?
```


# Model:

Qwen/Qwen3-4b



## Hypotheses

### 1. English mitigation

The fine-tuned model will agree with incorrect users less frequently than the original model.

### 2. Cross-lingual transfer

English anti-sycophancy training will cause at least some reduction in sycophancy in Russian and Kazakh.

### 3. Capability retention

The intervention will not substantially reduce accuracy when no misleading user opinion is present.

### 4. Stubbornness risk

The intervention might make the model reject users too often, including when the user is correct.
