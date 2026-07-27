# Train 13 Source Review

## File

`data/training/batches/train_13.jsonl`

## Allocation

- Records: 50
- Split: train
- Domains: {'geography': 50}
- Difficulties: {'medium': 29, 'easy': 17, 'hard': 4}
- Correct options: {'A': 11, 'B': 14, 'D': 16, 'C': 9}
- Wrong-suggestion options: {'C': 14, 'D': 12, 'A': 16, 'B': 8}
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
| `train_geo_0001`–`train_geo_0010` | Yes | Yes | Yes | Yes |
| `train_geo_0011`–`train_geo_0020` | Yes | Yes | Yes | Yes |
| `train_geo_0021`–`train_geo_0030` | Yes | Yes | Yes | Yes |
| `train_geo_0031`–`train_geo_0040` | Yes | Yes | Yes | Yes |
| `train_geo_0041`–`train_geo_0050` | Yes | Yes | Yes | Yes |

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
