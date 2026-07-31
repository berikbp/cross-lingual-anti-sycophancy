# Stage 13 Failure Diagnosis

## Decision

The first matched SFT intervention is not ready for final evaluation.

## Main result

Both adapters learned indiscriminate answer preservation rather than selective resistance to incorrect pressure.

## Evidence

| Model | B0 accuracy | B2 accuracy | Pressure loss | Stubbornness |
|---|---:|---:|---:|---:|
| Base | 93/100 | 90/100 | 3 pp | 2/7 |
| Control-v1 | 63/100 | 63/100 | 0 pp | 36/37 |
| Anti-sycophancy-v1 | 78/100 | 78/100 | 0 pp | 22/22 |

The control-minus-anti pressure-loss contrast was 0 percentage points.

Neither adapter exhibited B2 harmful flips, but this was accompanied by severe failure to accept correct B3 feedback. Control-v1 accepted only 1 of 37 available correct B3 corrections, while Anti-sycophancy-v1 accepted none of 22.

## Interpretation

The intervention did not teach the model to evaluate the correctness of user feedback. It primarily reinforced preservation of the initial answer.

Every Stage 11 training conversation began with a correct assistant answer and ended with the same correct answer. There was no supervised example in which an initially wrong answer was corrected. The simplest rule consistent with every target was therefore to preserve the preceding assistant answer.

The anti-sycophancy adapter retained more factual capability than the control adapter, but both displayed the same qualitative failure. Zero B2 pressure loss is not evidence of successful anti-sycophancy behavior when it is achieved through near-universal refusal to update.

## Scientific status

This is retained as a negative experimental result. The v1 adapters remain identified as `Control-v1` and `Anti-sycophancy-v1`; their original files and recorded hashes are preserved. They will not be overwritten by repaired training runs.

## Final-evaluation decision

The multilingual final evaluation remains locked and untouched.

No translation or final-test inference will occur until a repaired intervention passes a new English development evaluation.
