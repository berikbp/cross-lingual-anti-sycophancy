# Train 19 Source Review

## File

`data/training/batches/train_19.jsonl`

## Allocation

- Records: 50
- Split: train
- Domains: {'logic': 50}
- Difficulties: {'medium': 23, 'easy': 25, 'hard': 2}
- Correct options: {'A': 11, 'B': 13, 'C': 18, 'D': 8}
- Wrong-suggestion options: {'C': 14, 'A': 11, 'B': 9, 'D': 16}
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
| `train_logic_0101`–`train_logic_0110` | Yes | Yes | Yes | Yes |
| `train_logic_0111`–`train_logic_0120` | Yes | Yes | Yes | Yes |
| `train_logic_0121`–`train_logic_0130` | Yes | Yes | Yes | Yes |
| `train_logic_0131`–`train_logic_0140` | Yes | Yes | Yes | Yes |
| `train_logic_0141`–`train_logic_0150` | Yes | Yes | Yes | Yes |

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
