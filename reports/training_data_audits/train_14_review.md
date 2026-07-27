# Train 14 Source Review

## File

`data/training/batches/train_14.jsonl`

## Allocation

- Records: 50
- Split: train
- Domains: {'geography': 50}
- Difficulties: {'easy': 21, 'medium': 24, 'hard': 5}
- Correct options: {'B': 14, 'C': 13, 'A': 14, 'D': 9}
- Wrong-suggestion options: {'D': 13, 'A': 11, 'C': 15, 'B': 11}
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
| `train_geo_0051`–`train_geo_0060` | Yes | Yes | Yes | Yes |
| `train_geo_0061`–`train_geo_0070` | Yes | Yes | Yes | Yes |
| `train_geo_0071`–`train_geo_0080` | Yes | Yes | Yes | Yes |
| `train_geo_0081`–`train_geo_0090` | Yes | Yes | Yes | Yes |
| `train_geo_0091`–`train_geo_0100` | Yes | Yes | Yes | Yes |

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
