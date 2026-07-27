# Mathematics Batch 02 Review

## File

`data/master/batches/mathematics_02.jsonl`

## Automated checks

- [x] Valid JSONL
- [x] Exactly 20 records
- [x] Allocation fields preserved
- [x] Four non-empty distinct options per question
- [x] Correct and wrong options differ
- [x] Wrong-suggestion text matches assigned option
- [x] Every record is marked verified
- [x] Every record contains a verification note
- [x] No exact overlap with excluded questions
- [x] No duplicate within completed mathematics batches

## Manual answer review

| Stem ID | Correct answer verified | Verification checked | Approved |
|---|---:|---:|---:|
| `master_math_021` | Yes | Yes | Yes |
| `master_math_022` | Yes | Yes | Yes |
| `master_math_023` | Yes | Yes | Yes |
| `master_math_024` | Yes | Yes | Yes |
| `master_math_025` | Yes | Yes | Yes |
| `master_math_026` | Yes | Yes | Yes |
| `master_math_027` | Yes | Yes | Yes |
| `master_math_028` | Yes | Yes | Yes |
| `master_math_029` | Yes | Yes | Yes |
| `master_math_030` | Yes | Yes | Yes |
| `master_math_031` | Yes | Yes | Yes |
| `master_math_032` | Yes | Yes | Yes |
| `master_math_033` | Yes | Yes | Yes |
| `master_math_034` | Yes | Yes | Yes |
| `master_math_035` | Yes | Yes | Yes |
| `master_math_036` | Yes | Yes | Yes |
| `master_math_037` | Yes | Yes | Yes |
| `master_math_038` | Yes | Yes | Yes |
| `master_math_039` | Yes | Yes | Yes |
| `master_math_040` | Yes | Yes | Yes |

## Distractor review

Each assigned wrong suggestion was traced to a specific error, including cancellation of successive percentage changes, ignoring order of operations, dividing a ratio by the wrong number of parts, sign errors, confusing reciprocal with additive inverse, using tax amount instead of total price, failing to distribute a coefficient, and reporting a quotient as a remainder. Units and equivalent numerical forms were checked for uniqueness.

## Overlap review

- `master_math_021` uses successive opposing percentage changes; the development set contains only a single discount and a separate compound-interest balance.
- `master_math_033` recovers an original quantity from a known post-decrease value, unlike the development percentage-of and sale-price questions.
- `master_math_034` applies the product-of-powers law, rather than directly evaluating one small exponent.
- `master_math_035` tests division by a fraction, not integer division or fraction addition.
- `master_math_038` calculates tax and then total price; the development item calculates a discounted sale price.
- The original draft linear-equation and fraction-addition items were removed because they were too close to development questions.

No retained item is an obvious paraphrase of an excluded question.

## Decision

- [x] Batch approved
- [ ] Batch requires revision

## Reviewer notes

Reviewed without model evaluation. Batch difficulty is 8 easy, 10 medium, and 2 hard, exactly as allocated.
