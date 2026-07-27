# Training Source Batch 03 Review

## File

`data/training/batches/train_03.jsonl`

## Allocation

- Split: train
- Domain: mathematics
- Records: 50
- Expected IDs: `train_math_0101` through `train_math_0150`
- Model evaluation performed: no

## Automated checks

- [x] Valid JSONL
- [x] Exactly 50 records
- [x] IDs form the expected contiguous manifest block
- [x] Frozen allocation fields preserved
- [x] Four distinct, non-empty options
- [x] Correct and wrong options differ
- [x] Wrong-suggestion text matches its assigned option
- [x] All records marked verified
- [x] All verification notes present
- [x] No exact overlap with the exclusion corpus
- [x] No exact duplicate across completed training batches

## Allocation summary

| Field | Distribution |
|---|---|
| Difficulty | easy 21, medium 28, hard 1 |
| Correct option | A 14, B 11, C 10, D 15 |
| Wrong-suggestion option | A 13, B 13, C 12, D 12 |

## Manual review

| Stem range | Answers checked | Distractors checked | Semantic overlap checked | Approved |
|---|---:|---:|---:|---:|
| 0101–0110 | Yes | Yes | Yes | Yes |
| 0111–0120 | Yes | Yes | Yes | Yes |
| 0121–0130 | Yes | Yes | Yes | Yes |
| 0131–0140 | Yes | Yes | Yes | Yes |
| 0141–0150 | Yes | Yes | Yes | Yes |

## Semantic review

Domain-level review replaced structurally repetitive items, including:

- a repeated speed-unit conversion with a stated-formula temperature
  conversion;
- a regular-polygon perimeter template with a three-sided fencing
  equation;
- pentagon counting with minute-hand rotation;
- decimal conversion with a fraction-of-a-turn problem;
- a mirrored acute/obtuse classification with square-root estimation;
- a consecutive-integer mean template with a finite geometric sum;
- a quadrilateral angle-sum template with verbal algebra translation;
- inverse variation with an unknown-value mean problem.

The revised batch contains no number-swapped copy of an excluded item.

## Quality checks

- [x] Exactly one correct answer per stem
- [x] Assigned wrong suggestions are plausible
- [x] Difficulty labels are reasonable
- [x] Units and conditions are explicit
- [x] Topic structures differ from completed batches
- [x] No model was used to select or filter stems

## Decision

- [x] Batch approved
- [ ] Batch requires revision

## Notes

This file contains source stems only. No matched conversations were
generated.
