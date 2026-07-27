# Training Source Batch 01 Review

## File

`data/training/batches/train_01.jsonl`

## Scope

- Split: training
- Domain: mathematics
- Stem IDs: `train_math_0001` through `train_math_0050`
- Records: 50
- Model evaluation performed: no

## Automated checks

- [x] Valid JSONL
- [x] Exactly 50 records
- [x] Frozen allocation fields preserved
- [x] Four distinct, non-empty options per record
- [x] Correct and wrong-suggestion options differ
- [x] Wrong-suggestion text exactly matches its assigned option
- [x] Every record is marked verified
- [x] Every record has a verification note
- [x] No duplicate stem IDs
- [x] No duplicate questions within the batch
- [x] No exact normalized overlap with the frozen exclusion corpus

Validator:

```text
python src/training_data/validate_source_batch.py \
  data/training/batches/train_01.jsonl
```

Result:

```text
Records: 50
Source-batch validation passed.
```

## Allocation summary

| Field | Distribution |
|---|---|
| Difficulty | easy 18, medium 28, hard 4 |
| Correct option | A 8, B 13, C 13, D 16 |
| Wrong-suggestion option | A 15, B 10, C 12, D 13 |

These counts follow the frozen randomized allocation. Balance is enforced
over the complete 1,000-stem training split rather than within each
50-record batch.

## Manual answer review

| Stem IDs | Correct answer verified | Verification checked | Distractors checked | Approved |
|---|---:|---:|---:|---:|
| `train_math_0001`–`train_math_0010` | Yes | Yes | Yes | Yes |
| `train_math_0011`–`train_math_0020` | Yes | Yes | Yes | Yes |
| `train_math_0021`–`train_math_0030` | Yes | Yes | Yes | Yes |
| `train_math_0031`–`train_math_0040` | Yes | Yes | Yes | Yes |
| `train_math_0041`–`train_math_0050` | Yes | Yes | Yes | Yes |

The review recalculated each answer independently from the verification
note and checked that no distractor was also correct under the stated
conditions.

## Semantic-overlap review

Every new question was compared with the 940 entries in
`excluded_training_questions.txt`. A string-similarity screen was used
only to prioritize manual review; similarity scores were not treated as
proof of duplication.

The initial draft contained several items that were too close in
structure to excluded questions. They were replaced before approval,
including:

- parallelogram area with an L-shaped composite-area problem;
- a changed-mean problem with a consecutive-integer sum problem;
- a linear equation with a rate-and-time problem;
- repeated simple expression evaluation with function evaluation;
- supplementary-angle calculation with vertical-angle reasoning;
- fraction division with mixed-number subtraction;
- a basic linear inequality with an absolute-value inequality;
- a percent conversion with a powers-of-ten question;
- sequential discounts with a fractional tank-capacity problem, and
  then the tank-capacity draft with a wire-and-rectangle problem after
  the domain-level exclusion review found a structurally similar
  evaluation item;
- a cone-volume template with a sphere surface-area inference.

Remaining similarity flags were manually accepted only when they shared
broad mathematical vocabulary but required a different operation or
concept. Examples include:

- sector area versus circle circumference;
- cone volume versus cylinder volume;
- surface area versus solid volume;
- midpoint versus slope;
- interquartile range versus range or median;
- fraction-to-decimal versus decimal-to-fraction conversion.

No item reproduces an excluded question by changing only names, numbers,
or superficial wording.

## Quality review

- [x] Each problem has one objectively correct answer.
- [x] Units are present and consistent where needed.
- [x] Hard items require connected steps rather than obscure knowledge.
- [x] Assigned wrong suggestions represent plausible calculation or
      concept errors.
- [x] Questions are solvable without calculators, internet access, or
      specialist mathematics.
- [x] No development, smoke-test, master, final-test, or reserve item is
      reused.

## Decision

- [x] Batch approved
- [ ] Batch requires revision

## Reviewer notes

This is a source-stem batch only. No control or anti-sycophancy
conversation files were generated, and no model was run on these stems.
The batch was revalidated during the full 200-stem mathematics audit
after the domain-level semantic replacements.
