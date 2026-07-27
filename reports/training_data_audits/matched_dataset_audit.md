# Matched Dataset Audit

## Counts

| Dataset | Examples |
|---|---:|
| Control train | 1,000 |
| Anti-sycophancy train | 1,000 |
| Control validation | 100 |
| Anti-sycophancy validation | 100 |

## Exact matching checks

- [x] Stem order is identical between conditions.
- [x] Metadata and allocation fields are identical.
- [x] System prompts are identical.
- [x] Initial question messages are identical.
- [x] Initial assistant responses are identical and correct.
- [x] Final assistant targets are identical and correct.
- [x] Only the second user message differs.
- [x] Control follow-ups contain the frozen neutral reconsideration prompt.
- [x] Anti-sycophancy follow-ups contain the assigned wrong-answer text.
- [x] Anti-sycophancy uses protocol `1.0` and pressure template `v1_weak`.
- [x] Conversation-manifest hashes match the physical files.

## Qwen tokenizer length audit

| Dataset | Mean | Median | Minimum | Maximum |
|---|---:|---:|---:|---:|
| Control train | 121.678 | 121 | 102 | 185 |
| Anti-sycophancy train | 133.525 | 134 | 111 | 208 |
| Control validation | 122.870 | 121 | 105 | 150 |
| Anti-sycophancy validation | 135.160 | 134 | 114 | 166 |

The anti-sycophancy training conversations average 11.847 more tokens because
the frozen incorrect-suggestion follow-up is longer. The maximum paired
difference is 23 tokens. Both conditions remain well within the planned
sequence length.

Machine-readable statistics are recorded in
`reports/training_data_audits/conversation_length_stats.json`.

## Decision

- [x] Matched-condition validation passed.
- [x] Length differences are documented.
- [x] The datasets are ready for final-turn-only tokenization.
