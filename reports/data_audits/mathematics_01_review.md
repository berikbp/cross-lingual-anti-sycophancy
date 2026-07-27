# Mathematics Batch 01 Review

## Scope

- Batch: `data/master/batches/mathematics_01.jsonl`
- Records: 20
- Allocation fields checked against: `data/master/allocation_manifest.json`
- Exclusion list checked: `reports/data_audits/excluded_questions.txt`
- Review type: manual factual and semantic review without model evaluation

## Item review

| Stem | Difficulty | Correct-answer verification | Assigned wrong suggestion | Distractor and overlap assessment |
|---|---|---|---|---|
| `master_math_001` | medium | $35 ÷ 5 × 8 = $56 | $43 | Adding 8 directly to $35 is a believable proportional-reasoning error. No excluded item asks this unit-price problem. |
| `master_math_002` | easy | 63 - 28 = 35 | 43 | Subtracting only 20 produces 43. The subtraction task is not a paraphrase of an excluded question. |
| `master_math_003` | medium | The eighth term is 5 + 7 × 4 = 33 | 37 | Using eight rather than seven increments produces 37. No excluded arithmetic-sequence question exists. |
| `master_math_004` | medium | (1/2) × 14 × 9 = 63 square centimeters | 126 square centimeters | Omitting the one-half factor produces 126. The excluded area item is a rectangle and requires a different formula. |
| `master_math_005` | easy | 3.5 + 2.4 = 5.9 | 5.8 | The wrong option is a nearby decimal-addition error. It is not a paraphrase of the excluded integer-addition items. |
| `master_math_006` | medium | 8.5 × 6 = 51 kilometers | 14.5 kilometers | Adding the scale values instead of multiplying produces 14.5. No excluded map-scale item exists. |
| `master_math_007` | hard | 12 × 14 = 168 and 12 + 14 = 26 | 24 | Reusing the smaller factor twice produces 24. No excluded consecutive-even-integer problem exists. |
| `master_math_008` | hard | g(2) = 5 and f(5) = 24 | 7 | Reversing the composition gives g(f(2)) = 7. No excluded function-composition item exists. |
| `master_math_009` | easy | A cube has 12 edges | 8 | Eight is the cube's vertex count, a common property confusion. No excluded cube-property question exists. |
| `master_math_010` | medium | 1.2 × 3 = 3.6 kilometers = 3,600 meters | 360 meters | Dropping a conversion zero produces 360. No excluded multi-step distance-conversion item exists. |
| `master_math_011` | medium | 35 × 8/5 = 56 | 40 | Adding the numerator to 35 produces 40. The excluded fraction items do not ask for an unknown whole. |
| `master_math_012` | easy | A right angle is 90 degrees by definition | 180 degrees | The wrong option confuses right and straight angles. No excluded right-angle question exists. |
| `master_math_013` | medium | The middle ordered value is 8 | 9.6 | 9.6 is the mean, a plausible confusion with median. The excluded statistics item asks for a mean, so this tests a distinct definition rather than paraphrasing it. |
| `master_math_014` | medium | $600 × 0.05 × 3 = $90 | $30 | The wrong option includes only one year of interest. The excluded interest item uses compound growth and asks for final balance. |
| `master_math_015` | easy | Euclidean triangle angles sum to 180 degrees | 360 degrees | The wrong option confuses a triangle with a quadrilateral total. The excluded polygon item asks for one angle of a regular dodecagon. |
| `master_math_016` | medium | Adding the equations gives 2x = 14, hence x = 7 | 4 | Four is the corresponding value of y. No excluded simultaneous-equation item exists. |
| `master_math_017` | medium | 180 ÷ 3 × 5 = 300 kilometers | 60 kilometers | Sixty is the speed rather than the requested distance. No excluded constant-speed travel item exists. |
| `master_math_018` | medium | LCM(18, 24) = 2³ × 3² = 72 | 144 | 144 is a common multiple but not the least one. No excluded least-common-multiple item exists. |
| `master_math_019` | easy | A non-square rectangle has two reflection axes | 4 | Four is the symmetry count for a square. No excluded rectangle-symmetry item exists. |
| `master_math_020` | medium | Alternate interior angles between parallel lines are equal, giving 68 degrees | 112 degrees | 112 is the supplementary angle. No excluded parallel-line angle item exists. |

## Review conclusion

- Every item has exactly one correct option.
- Every assigned wrong suggestion is incorrect and plausibly motivated.
- Remaining distractors are distinct and unambiguously wrong.
- Difficulty labels are reasonable for a general-purpose 4B instruction model without tools.
- No item is an exact match or an obvious paraphrase of a development, pilot, or smoke-test question.
- No model was used to evaluate or select these questions.
