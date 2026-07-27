# Train 16 Source Review

## File

`data/training/batches/train_16.jsonl`

## Allocation

- Records: 50
- Split: train
- Domains: {'geography': 50}
- Difficulties: {'medium': 21, 'easy': 24, 'hard': 5}
- Correct options: {'D': 14, 'A': 10, 'C': 14, 'B': 12}
- Wrong-suggestion options: {'C': 13, 'A': 10, 'D': 13, 'B': 14}
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
| `train_geo_0151`–`train_geo_0160` | Yes | Yes | Yes | Yes |
| `train_geo_0161`–`train_geo_0170` | Yes | Yes | Yes | Yes |
| `train_geo_0171`–`train_geo_0180` | Yes | Yes | Yes | Yes |
| `train_geo_0181`–`train_geo_0190` | Yes | Yes | Yes | Yes |
| `train_geo_0191`–`train_geo_0200` | Yes | Yes | Yes | Yes |

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
