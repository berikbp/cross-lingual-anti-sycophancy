# English Development Evaluation v2

## Primary results

| Model | Initial | B0 | B1 | B2 | B3 | Pressure loss |
|---|---:|---:|---:|---:|---:|---:|
| Control-v2 | 99/100 (99.0%) | 99/100 (99.0%) | 99/100 (99.0%) | 98/100 (98.0%) | 99/100 (99.0%) | 1.0 pp |
| Selective-v2 | 98/100 (98.0%) | 98/100 (98.0%) | 98/100 (98.0%) | 98/100 (98.0%) | 99/100 (99.0%) | 0.0 pp |

Primary contrast (Control-v2 pressure loss minus Selective-v2 pressure loss): **1.0 pp**.

## Selectivity metrics

| Model | Harmful B2 flips | Exact wrong B2 | Changed to wrong B2 | Beneficial B3 correction | Stubbornness | Neutral self-correction | Correct preservation under B2 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Control-v2 | 1/99 (1.0%) | 2/100 (2.0%) | 1/100 (1.0%) | 0/1 (0.0%) | 1/1 (100.0%) | 0/1 (0.0%) | 98/99 (99.0%) |
| Selective-v2 | 0/98 (0.0%) | 2/100 (2.0%) | 0/100 (0.0%) | 1/2 (50.0%) | 1/2 (50.0%) | 0/2 (0.0%) | 98/98 (100.0%) |

## Answer preservation

| Model | Initial state | B0 | B1 | B2 | B3 |
|---|---|---:|---:|---:|---:|
| Control-v2 | Correct | 99/99 (100.0%) | 99/99 (100.0%) | 98/99 (99.0%) | 99/99 (100.0%) |
| Control-v2 | Incorrect | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| Selective-v2 | Correct | 98/98 (100.0%) | 98/98 (100.0%) | 98/98 (100.0%) | 98/98 (100.0%) |
| Selective-v2 | Incorrect | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) | 1/2 (50.0%) |

## Paired comparisons

- Pressure-loss common support: 100 stems.
- Paired pressure-loss effect: 1.0 pp.
- Bootstrap 95% CI: [0.0, 3.0] pp.
- Selective-v2 improved/worsened/unchanged: 1/0/99 stems.
- Common initially-incorrect denominator for B3: 1 stem(s).
- Common-denominator Control-v2 B3 correction: 0/1 (0.0%).
- Common-denominator Selective-v2 B3 correction: 0/1 (0.0%).
- Paired B3 correction effect: 0.0 pp; bootstrap 95% CI [0.0, 0.0] pp.

## Parseability and common support

All initial and branch responses for both v2 conditions were parseable. Common-support accuracy therefore equals all-record accuracy.

## Readiness decision

**Proceed cautiously to Stage 18.** Selective-v2 meets the frozen engineering and behavioral thresholds: capability is retained, its B2 harmful-flip rate does not exceed Control-v2, and it corrects 1/2 initially incorrect answers under B3 rather than reproducing v1's 22/22 stubbornness. However, the correction denominator is only two stems (one on the common denominator), so this is readiness evidence, not a strong development-set efficacy claim.

The frozen final test and reserve were not accessed.
