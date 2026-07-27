# Train 20 Source Review

## File

`data/training/batches/train_20.jsonl`

## Allocation

- Records: 50
- Split: train
- Domains: {'logic': 50}
- Difficulties: {'medium': 24, 'easy': 19, 'hard': 7}
- Correct options: {'A': 12, 'D': 14, 'C': 12, 'B': 12}
- Wrong-suggestion options: {'D': 11, 'B': 12, 'C': 12, 'A': 15}
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
| `train_logic_0151`–`train_logic_0160` | Yes | Yes | Yes | Yes |
| `train_logic_0161`–`train_logic_0170` | Yes | Yes | Yes | Yes |
| `train_logic_0171`–`train_logic_0180` | Yes | Yes | Yes | Yes |
| `train_logic_0181`–`train_logic_0190` | Yes | Yes | Yes | Yes |
| `train_logic_0191`–`train_logic_0200` | Yes | Yes | Yes | Yes |

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
