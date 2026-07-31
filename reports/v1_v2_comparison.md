# v1–v2 English Development Comparison

## What changed

v1 supervised only correct initial answers followed by unchanged correct final answers. Both adapters learned near-total answer preservation, including preservation of incorrect answers when B3 supplied the correct answer. v2 reused the same factual stems but balanced correct/incorrect initial answers and correct/incorrect feedback through CW, WC, CC, and WW transitions.

## Direct comparison

| Model | Initial | B0 | B2 | Pressure loss | Harmful flips | Beneficial correction | Stubbornness |
|---|---:|---:|---:|---:|---:|---:|---:|
| Base | 93/100 (93.0%) | 93/100 (93.0%) | 90/100 (90.0%) | 3.0 pp | 3/93 (3.2%) | 5/7 (71.4%) | 2/7 (28.6%) |
| Control-v1 | 63/100 (63.0%) | 63/100 (63.0%) | 63/100 (63.0%) | 0.0 pp | 0/63 (0.0%) | 1/37 (2.7%) | 36/37 (97.3%) |
| Anti-v1 | 78/100 (78.0%) | 78/100 (78.0%) | 78/100 (78.0%) | 0.0 pp | 0/78 (0.0%) | 0/22 (0.0%) | 22/22 (100.0%) |
| Control-v2 | 99/100 (99.0%) | 99/100 (99.0%) | 98/100 (98.0%) | 1.0 pp | 1/99 (1.0%) | 0/1 (0.0%) | 1/1 (100.0%) |
| Selective-v2 | 98/100 (98.0%) | 98/100 (98.0%) | 98/100 (98.0%) | 0.0 pp | 0/98 (0.0%) | 1/2 (50.0%) | 1/2 (50.0%) |

## Interpretation

v2 restored factual capability relative to both v1 adapters: Control-v2 B0 accuracy is 99% and Selective-v2 B0 accuracy is 98%, compared with 63% and 78% for Control-v1 and Anti-v1. Selective-v2 also reduced B3 stubbornness from Anti-v1's 22/22 to 1/2 and made one beneficial correction. It resisted all B2 harmful flips (0/98), while Control-v2 had one harmful flip (1/99).

The evidence supports correction selectivity more than v1 did, but the v2 adapters made very few initial errors. Consequently, the beneficial-correction comparison has low denominator support and must not be presented as a precise estimate.

## Final-readiness decision

Proceed cautiously to Stage 18. All engineering gates pass, Selective-v2 retains capability, does not increase harmful flips, reaches the predeclared 50% beneficial-correction threshold, and is materially less stubborn than Anti-v1. The locked multilingual evaluation remains necessary to estimate the effect on a larger, untouched sample.
