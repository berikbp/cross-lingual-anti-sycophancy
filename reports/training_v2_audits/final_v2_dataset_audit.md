# Selective-Correction v2 Dataset Audit

## Motivation

The v1 intervention produced indiscriminate answer preservation and severe stubbornness. The v2 design balances correct and incorrect initial answers and correct and incorrect user suggestions.

## Source artifacts

- Training source stems: 1,000
- Validation source stems: 100
- New factual stems created: 0
- Source train SHA-256: `12311fca3025c4b81aae45135f9dcd2d07a063a5c1fe9bcc15fd18e86643853b`
- Source validation SHA-256: `b98bafeece580ea3b6e189bfdf423b9c1ea926122638d09fc8648c2cb367a102`

## Transition allocation

| Split | CW | WC | CC | WW | Total |
|---|---:|---:|---:|---:|---:|
| Training | 250 | 250 | 250 | 250 | 1,000 |
| Validation | 25 | 25 | 25 | 25 | 100 |

Each training domain contains 50 examples per category; each validation domain contains 5 per category.

## State balance

| Split | Initial correct | Initial incorrect | Feedback correct | Feedback incorrect |
|---|---:|---:|---:|---:|
| Training | 500 | 500 | 500 | 500 |
| Validation | 50 | 50 | 50 | 50 |

## Matched-condition audit

- Identical stem ordering: yes
- Identical source questions: yes
- Identical initial assistant responses: yes
- Identical final assistant targets: yes
- Identical transition categories: yes
- Identical message count: yes
- Only follow-up user message differs: yes

## Transition validity

- CW preserves correct answers against wrong feedback: yes
- WC accepts correct feedback after wrong initial answers: yes
- CC preserves correct answers with correct support: yes
- WW rejects wrong feedback and self-corrects: yes
- WW initial and feedback wrong options are distinct: yes

## Token-length audit

Maximum training length is 256 tokens. Truncated counts refer to left-truncated context; the full final target is retained in every case.

| Dataset | Min. | Mean | Median | P95 | Max. | Context truncated | Final targets removed | Mean supervised |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Control-v2 train | 102 | 121.68 | 121.00 | 139.00 | 185 | 0 | 0 | 8.00 |
| Selective-v2 train | 111 | 133.99 | 134.00 | 153.00 | 210 | 0 | 0 | 8.00 |
| Control-v2 validation | 105 | 122.87 | 121.00 | 139.10 | 150 | 0 | 0 | 8.00 |
| Selective-v2 validation | 114 | 136.01 | 134.00 | 153.10 | 167 | 0 | 0 | 8.00 |

## Loss masking

- System prompt masked: yes
- Source question masked: yes
- Initial assistant answer masked: yes
- Follow-up user message masked: yes
- Final assistant answer supervised: yes
- Incorrect initial answers supervised: no
- Incorrect feedback supervised: no
- All masking tests passed: yes

## Evaluation protection

- Development questions used for training: no
- Final test accessed: no
- Reserve accessed: no

## Decision

- [x] Control-v2 dataset is frozen.
- [x] Selective-correction-v2 dataset is frozen.
- [x] Transition allocation is balanced.
- [x] Matched-condition validation passed.
- [x] Final-answer-only masking passed.
- [x] Fresh matched adapter training may begin.
