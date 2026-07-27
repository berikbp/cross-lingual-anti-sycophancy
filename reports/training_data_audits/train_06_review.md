# Train 06 Source Review

## File

`data/training/batches/train_06.jsonl`

## Allocation

- Records: 50
- Split: train
- Domains: {'science': 50}
- Difficulties: {'medium': 24, 'easy': 23, 'hard': 3}
- Correct options: {'C': 13, 'A': 15, 'B': 9, 'D': 13}
- Wrong-suggestion options: {'D': 11, 'B': 13, 'C': 10, 'A': 16}
- Model evaluation performed: no

## Automated checks

- [x] Valid JSONL
- [x] Exactly 50 records
- [x] Frozen manifest order and fields preserved
- [x] Four distinct, non-empty options
- [x] Correct and wrong options differ
- [x] Wrong-suggestion text matches
- [x] Every record is verified
- [x] Verification notes are complete
- [x] No exact exclusion overlap
- [x] No exact duplicate in the source pool

## Manual review

| Stem range | Answers checked | Distractors checked | Semantic overlap checked | Approved |
|---|---:|---:|---:|---:|
| `train_science_0051`–`train_science_0060` | Yes | Yes | Yes | Yes |
| `train_science_0061`–`train_science_0070` | Yes | Yes | Yes | Yes |
| `train_science_0071`–`train_science_0080` | Yes | Yes | Yes | Yes |
| `train_science_0081`–`train_science_0090` | Yes | Yes | Yes | Yes |
| `train_science_0091`–`train_science_0100` | Yes | Yes | Yes | Yes |

## Quality checks

- [x] Exactly one correct answer per stem
- [x] Assigned wrong suggestion is plausible
- [x] Difficulty is consistent with the frozen label
- [x] Questions use stable, tool-free knowledge
- [x] Evaluation questions are not reused
- [x] No model output was used to select stems

## Decision

- [x] Batch approved
- [ ] Batch requires revision

## Notes

Source stems only; no question was selected or filtered using model performance.
