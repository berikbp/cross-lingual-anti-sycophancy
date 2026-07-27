# Train 11 Source Review

## File

`data/training/batches/train_11.jsonl`

## Allocation

- Records: 50
- Split: train
- Domains: {'computer_science': 50}
- Difficulties: {'easy': 21, 'medium': 22, 'hard': 7}
- Correct options: {'D': 10, 'C': 14, 'B': 17, 'A': 9}
- Wrong-suggestion options: {'C': 10, 'B': 7, 'A': 13, 'D': 20}
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
| `train_cs_0101`–`train_cs_0110` | Yes | Yes | Yes | Yes |
| `train_cs_0111`–`train_cs_0120` | Yes | Yes | Yes | Yes |
| `train_cs_0121`–`train_cs_0130` | Yes | Yes | Yes | Yes |
| `train_cs_0131`–`train_cs_0140` | Yes | Yes | Yes | Yes |
| `train_cs_0141`–`train_cs_0150` | Yes | Yes | Yes | Yes |

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
