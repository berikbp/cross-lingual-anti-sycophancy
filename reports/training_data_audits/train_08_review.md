# Train 08 Source Review

## File

`data/training/batches/train_08.jsonl`

## Allocation

- Records: 50
- Split: train
- Domains: {'science': 50}
- Difficulties: {'hard': 2, 'medium': 27, 'easy': 21}
- Correct options: {'D': 11, 'B': 10, 'C': 18, 'A': 11}
- Wrong-suggestion options: {'B': 12, 'D': 16, 'C': 10, 'A': 12}
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
| `train_science_0151`–`train_science_0160` | Yes | Yes | Yes | Yes |
| `train_science_0161`–`train_science_0170` | Yes | Yes | Yes | Yes |
| `train_science_0171`–`train_science_0180` | Yes | Yes | Yes | Yes |
| `train_science_0181`–`train_science_0190` | Yes | Yes | Yes | Yes |
| `train_science_0191`–`train_science_0200` | Yes | Yes | Yes | Yes |

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
