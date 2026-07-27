# Training Source Batch 02 Review

## File

`data/training/batches/train_02.jsonl`

## Allocation

- Split: train
- Domain: mathematics
- Records: 50
- Expected IDs: `train_math_0051` through `train_math_0100`
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
| Difficulty | easy 21, medium 25, hard 4 |
| Correct option | A 16, B 11, C 15, D 8 |
| Wrong-suggestion option | A 10, B 15, C 13, D 12 |

Batch-level option counts follow the frozen randomized allocation.
Balance is enforced across all 200 mathematics stems.

## Manual review

| Stem range | Answers checked | Distractors checked | Semantic overlap checked | Approved |
|---|---:|---:|---:|---:|
| 0051–0060 | Yes | Yes | Yes | Yes |
| 0061–0070 | Yes | Yes | Yes | Yes |
| 0071–0080 | Yes | Yes | Yes | Yes |
| 0081–0090 | Yes | Yes | Yes | Yes |
| 0091–0100 | Yes | Yes | Yes | Yes |

## Semantic review

The batch was compared against the complete exclusion corpus and the
other mathematics training batches. Items that were too close to an
evaluation template were replaced before approval. In particular:

- a simple linear-equation template became an arithmetic-sequence
  common-difference inference;
- a semicircle-area template became a square-diagonal area problem.

Remaining similarity flags involved broad shared vocabulary rather than
the same underlying problem.

## Quality checks

- [x] Exactly one correct answer per stem
- [x] Assigned wrong suggestions are plausible
- [x] Difficulty labels are reasonable
- [x] Evaluation templates are not reproduced by changing numbers
- [x] Arithmetic, algebra, geometry, probability, statistics, ratios,
      and sequences are represented
- [x] No model was used to select or filter stems

## Decision

- [x] Batch approved
- [ ] Batch requires revision

## Notes

This file contains source stems only. No matched conversations were
generated.
