# Validation 01 Source Review

## File

`data/training/batches/validation_01.jsonl`

## Allocation

- Records: 50
- Split: validation
- Domains: {'mathematics': 20, 'science': 20, 'computer_science': 10}
- Difficulties: {'easy': 21, 'medium': 24, 'hard': 5}
- Correct options: {'A': 13, 'B': 12, 'D': 13, 'C': 12}
- Wrong-suggestion options: {'C': 13, 'A': 12, 'B': 13, 'D': 12}
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
| `val_math_0001`–`val_math_0010` | Yes | Yes | Yes | Yes |
| `val_math_0011`–`val_math_0020` | Yes | Yes | Yes | Yes |
| `val_science_0001`–`val_science_0010` | Yes | Yes | Yes | Yes |
| `val_science_0011`–`val_science_0020` | Yes | Yes | Yes | Yes |
| `val_cs_0001`–`val_cs_0010` | Yes | Yes | Yes | Yes |

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
