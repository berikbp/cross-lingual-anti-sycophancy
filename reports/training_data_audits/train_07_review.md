# Train 07 Source Review

## File

`data/training/batches/train_07.jsonl`

## Allocation

- Records: 50
- Split: train
- Domains: {'science': 50}
- Difficulties: {'medium': 25, 'hard': 7, 'easy': 18}
- Correct options: {'A': 11, 'B': 16, 'D': 13, 'C': 10}
- Wrong-suggestion options: {'C': 16, 'D': 12, 'B': 10, 'A': 12}
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
| `train_science_0101`–`train_science_0110` | Yes | Yes | Yes | Yes |
| `train_science_0111`–`train_science_0120` | Yes | Yes | Yes | Yes |
| `train_science_0121`–`train_science_0130` | Yes | Yes | Yes | Yes |
| `train_science_0131`–`train_science_0140` | Yes | Yes | Yes | Yes |
| `train_science_0141`–`train_science_0150` | Yes | Yes | Yes | Yes |

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
