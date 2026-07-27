# Train 17 Source Review

## File

`data/training/batches/train_17.jsonl`

## Allocation

- Records: 50
- Split: train
- Domains: {'logic': 50}
- Difficulties: {'easy': 19, 'medium': 25, 'hard': 6}
- Correct options: {'C': 10, 'A': 14, 'B': 10, 'D': 16}
- Wrong-suggestion options: {'B': 12, 'A': 11, 'C': 15, 'D': 12}
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
| `train_logic_0001`–`train_logic_0010` | Yes | Yes | Yes | Yes |
| `train_logic_0011`–`train_logic_0020` | Yes | Yes | Yes | Yes |
| `train_logic_0021`–`train_logic_0030` | Yes | Yes | Yes | Yes |
| `train_logic_0031`–`train_logic_0040` | Yes | Yes | Yes | Yes |
| `train_logic_0041`–`train_logic_0050` | Yes | Yes | Yes | Yes |

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
