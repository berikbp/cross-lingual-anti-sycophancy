# Corrected Kazakh v2 sensitivity analysis

This post-audit analysis uses the author-reviewed corrected Kazakh translation and the frozen language-revised Kazakh prompts. It does not replace the historical Stage 19 Kazakh evaluation.

| Condition | B0 accuracy | B2 accuracy | Pressure loss |
|---|---:|---:|---:|
| base | 185/300 (61.7%) | 78/300 (26.0%) | 35.7 pp |
| control_v2 | 239/300 (79.7%) | 183/300 (61.0%) | 18.7 pp |
| selective_correction_v2 | 238/300 (79.3%) | 179/300 (59.7%) | 19.7 pp |

Paired Control-v2 minus Selective-v2 effect: -1.0 pp (95% bootstrap CI -4.3 to 2.3 pp).
The paired contributions favored Selective-v2 on 10 stems, Control-v2 on 14, and were unchanged on 276.

## Selective-behavior checks

| Condition | B0-to-B2 pressure flip | Exact wrong adoption among B0-correct | B3 beneficial correction | B3 stubbornness | B0/B2 parseable |
|---|---:|---:|---:|---:|---:|
| control_v2 | 58/239 (24.3%) | 52/239 (21.8%) | 32/52 (61.5%) | 20/52 (38.5%) | 300/300; 300/300 |
| selective_correction_v2 | 62/238 (26.1%) | 55/238 (23.1%) | 31/47 (66.0%) | 16/47 (34.0%) | 300/300; 300/300 |

Historical original-translation losses were 17.7 pp (Control-v2) and 19.3 pp (Selective-v2). Corrected losses are 18.7 and 19.7 pp.

The corrected run reaches the same substantive conclusion as the historical run: it does not show a Selective-v2 pressure-resistance advantage. Both v2 conditions accepted many valid B3 corrections, so this null result is not explained by the near-total stubbornness seen in v1.

Interpret differences from the historical run as sensitivity to the combined translation-and-prompt language correction, not as a preregistered replacement of the locked result or as the isolated effect of either change.
