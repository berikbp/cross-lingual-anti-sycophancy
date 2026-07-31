# Stage 11 Training Transition Audit

## Observed transition patterns

| Dataset | Count | Initial state | Follow-up | Final changed? | Final state |
|---|---:|---|---|---|---|
| Control-v1 train | 1000 | initial_correct | neutral | unchanged | final_correct |
| Control-v1 validation | 100 | initial_correct | neutral | unchanged | final_correct |
| Anti-sycophancy-v1 train | 1000 | initial_correct | incorrect_suggestion | unchanged | final_correct |
| Anti-sycophancy-v1 validation | 100 | initial_correct | incorrect_suggestion | unchanged | final_correct |

## Missing transition types

| Missing supervision | Behavior it would teach |
|---|---|
| Initial wrong + correct suggestion → changed and correct | Accept a valid user correction |
| Initial wrong + neutral reconsideration → changed and correct | Self-correct without an explicit answer suggestion |
| Initial correct + correct suggestion → unchanged and correct | Accept correct support without learning to reject all suggestions |
| Initial wrong + incorrect suggestion → changed independently to correct | Reject bad feedback while still revising an erroneous prior answer |

## Conclusion

Every one of the 2,200 Stage 11 train and validation conversations has a correct initial assistant answer and an unchanged correct final answer. The 1,100 control conversations use neutral reconsideration; the 1,100 anti-sycophancy conversations use an explicitly incorrect suggestion. No conversation supervises a change from an initially wrong answer to a correct final answer.

Stage 11 therefore contains complete supervision for answer preservation and no supervision for beneficial correction. The observed v1 stubbornness is consistent with this target distribution. This audit establishes a dataset mechanism; it does not by itself prove that no other training factor contributed.
