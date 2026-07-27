# Train 10 Source Review

## File

`data/training/batches/train_10.jsonl`

## Allocation

- Records: 50
- Split: train
- Domains: {'computer_science': 50}
- Difficulties: {'medium': 30, 'hard': 7, 'easy': 13}
- Correct options: {'A': 15, 'C': 6, 'B': 10, 'D': 19}
- Wrong-suggestion options: {'B': 15, 'C': 20, 'A': 11, 'D': 4}
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
| `train_cs_0051`–`train_cs_0060` | Yes | Yes | Yes | Yes |
| `train_cs_0061`–`train_cs_0070` | Yes | Yes | Yes | Yes |
| `train_cs_0071`–`train_cs_0080` | Yes | Yes | Yes | Yes |
| `train_cs_0081`–`train_cs_0090` | Yes | Yes | Yes | Yes |
| `train_cs_0091`–`train_cs_0100` | Yes | Yes | Yes | Yes |

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
