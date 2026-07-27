# Final Training Data Audit

## Source stems

- Training stems: 1,000
- Validation stems: 100
- Train/validation overlap: 0
- Evaluation overlap: 0
- Duplicate IDs: 0
- Exact duplicate questions: 0
- All answers verified: yes

## Train distribution

| Domain | Count |
|---|---:|
| Mathematics | 200 |
| Science | 200 |
| Computer science | 200 |
| Geography | 200 |
| Logic | 200 |

| Difficulty | Count |
|---|---:|
| Easy | 400 |
| Medium | 500 |
| Hard | 100 |

Correct-option positions and wrong-suggestion positions are each balanced:
A 250, B 250, C 250, and D 250.

## Validation distribution

| Domain | Count |
|---|---:|
| Mathematics | 20 |
| Science | 20 |
| Computer science | 20 |
| Geography | 20 |
| Logic | 20 |

| Difficulty | Count |
|---|---:|
| Easy | 40 |
| Medium | 50 |
| Hard | 10 |

Correct-option positions and wrong-suggestion positions are each balanced:
A 25, B 25, C 25, and D 25.

## Matched conversations

- Control train: 1,000
- Anti-sycophancy train: 1,000
- Control validation: 100
- Anti-sycophancy validation: 100
- Identical stem order: yes
- Identical initial messages: yes
- Identical initial assistant answers: yes
- Identical final targets: yes
- Only follow-up user message differs: yes
- Frozen pressure template: `v1_weak`

## Loss masking

- System message masked: yes
- Initial user question masked: yes
- Initial assistant response masked: yes
- Follow-up user message masked: yes
- Final assistant response supervised: yes
- Incorrect user suggestion supervised: no
- Target-preserving truncation tested: yes
- Unit tests passed: 7

## Artifact hashes

SHA-256 hashes for the source stems are recorded in
`docs/training_source_hashes.txt`.

SHA-256 hashes for both source files, all four conversation datasets, and the
conversation manifest are recorded in `docs/training_dataset_hashes.txt`.

## Verification commands

- `python src/training_data/validate_source_pool.py`
- `python src/training_data/validate_matched_conversations.py`
- `uv run pytest -q tests/training_data`

## Decision

- [x] Training datasets are frozen.
- [x] Validation datasets are frozen.
- [x] Data-leakage checks passed.
- [x] Matched-condition checks passed.
- [x] Final-turn-only masking tests passed.
- [x] Adapter training may begin.
