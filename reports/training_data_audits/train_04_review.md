# Training Source Batch 04 Review

## File

`data/training/batches/train_04.jsonl`

## Allocation

- Split: train
- Domain: mathematics
- Records: 50
- Expected IDs: `train_math_0151` through `train_math_0200`
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
| Difficulty | easy 20, medium 19, hard 11 |
| Correct option | A 12, B 15, C 12, D 11 |
| Wrong-suggestion option | A 12, B 12, C 13, D 13 |

The larger number of hard items is required by the frozen manifest and
brings the four-batch domain total to exactly 20 hard stems.

## Manual review

| Stem range | Answers checked | Distractors checked | Semantic overlap checked | Approved |
|---|---:|---:|---:|---:|
| 0151–0160 | Yes | Yes | Yes | Yes |
| 0161–0170 | Yes | Yes | Yes | Yes |
| 0171–0180 | Yes | Yes | Yes | Yes |
| 0181–0190 | Yes | Yes | Yes | Yes |
| 0191–0200 | Yes | Yes | Yes | Yes |

## Semantic review

The exclusion and cross-batch review caused several replacements:

- regular-octagon angle calculation became a ratio-based triangle-angle
  problem;
- a changed-number square calculation became triangular-number
  recognition;
- a repeated two-dice problem became a two-spin product-parity problem;
- counter drawing became a structured code-counting problem;
- fraction addition became part-to-whole fraction reduction;
- direct division became place-value knowledge;
- a changed-number square-root item became divisor-count reasoning;
- a rounding template became two-addend estimation;
- a repeated next-term sequence became factor summation;
- unit conversion became grouping socks into pairs;
- letter sampling became parity reasoning over a finite integer set;
- explicit factorization became coefficient inference from known
  factors.

## Quality checks

- [x] Exactly one correct answer per stem
- [x] Assigned wrong suggestions are plausible
- [x] Hard questions require connected reasoning rather than trivia
- [x] Geometry, combinatorics, probability, algebra, data, and sequences
      are represented
- [x] No evaluation template is reproduced by superficial substitution
- [x] No model was used to select or filter stems

## Decision

- [x] Batch approved
- [ ] Batch requires revision

## Notes

This file contains source stems only. No matched conversations were
generated.
