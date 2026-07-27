# Train 15 Source Review

## File

`data/training/batches/train_15.jsonl`

## Allocation

- Records: 50
- Split: train
- Domains: {'geography': 50}
- Difficulties: {'medium': 26, 'easy': 18, 'hard': 6}
- Correct options: {'C': 14, 'D': 11, 'B': 10, 'A': 15}
- Wrong-suggestion options: {'A': 13, 'B': 17, 'D': 12, 'C': 8}
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
| `train_geo_0101`–`train_geo_0110` | Yes | Yes | Yes | Yes |
| `train_geo_0111`–`train_geo_0120` | Yes | Yes | Yes | Yes |
| `train_geo_0121`–`train_geo_0130` | Yes | Yes | Yes | Yes |
| `train_geo_0131`–`train_geo_0140` | Yes | Yes | Yes | Yes |
| `train_geo_0141`–`train_geo_0150` | Yes | Yes | Yes | Yes |

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
