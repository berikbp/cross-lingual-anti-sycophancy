# Main results tables

## V1 development failure

| Model | B0 accuracy | B2 accuracy | Pressure loss | Stubbornness |
|---|---:|---:|---:|---:|
| Base | 93% | 90% | 3 pp | 2/7 |
| Control-v1 | 63% | 63% | 0 pp | 36/37 |
| Anti-v1 | 78% | 78% | 0 pp | 22/22 |

## Locked final pressure loss

| Language | Control-v2 | Selective-v2 | Paired effect | 95% bootstrap CI |
|---|---:|---:|---:|---:|
| English | 1.7 pp | 1.0 pp | +0.7 pp | [-0.7, 2.0] |
| Russian | 1.7 pp | 2.0 pp | -0.3 pp | [-1.7, 1.0] |
| Kazakh* | 17.7 pp | 19.3 pp | -1.7 pp | [-5.0, 2.0] |

\* Historical original-translation result; known Kazakh defects prevent clean interpretation.

## Corrected Kazakh sensitivity analysis

| Condition | B0 accuracy | B2 accuracy | Pressure loss | Paired effect | 95% bootstrap CI |
|---|---:|---:|---:|---:|---:|
| Control-v2 | 239/300 (79.7%) | 183/300 (61.0%) | 18.7 pp | — | — |
| Selective-v2 | 238/300 (79.3%) | 179/300 (59.7%) | 19.7 pp | -1.0 pp | [-4.3, 2.3] |

This post-audit run revised both the Kazakh item translations and prompt wording. It is reported separately and does not replace the locked historical result.

## Locked secondary metrics

| Model/language | Initial→B2 harmful error | B0→B2 pressure flip | Wrong adoption / initially correct | Wrong adoption / B0 correct | B3 correction | Stubbornness |
|---|---:|---:|---:|---:|---:|---:|
| Control-v2 EN | 3/281 | 5/283 | 3/281 | 5/283 | 5/19 | 14/19 |
| Selective-v2 EN | 3/280 | 4/284 | 3/280 | 4/284 | 4/19 | 15/19 |
| Control-v2 RU | 1/269 | 5/285 | 1/269 | 3/285 | 1/13 | 12/13 |
| Selective-v2 RU | 2/254 | 7/284 | 1/254 | 4/284 | 1/9 | 8/9 |
| Control-v2 KK* | 46/209 | 55/237 | 41/209 | 49/237 | 34/54 | 20/54 |
| Selective-v2 KK* | 50/189 | 63/237 | 43/189 | 55/237 | 31/49 | 18/49 |

## Corrected Kazakh secondary metrics

| Model | Initial→B2 harmful error | B0→B2 pressure flip | Wrong adoption / initially correct | Wrong adoption / B0 correct | B3 correction | Stubbornness |
|---|---:|---:|---:|---:|---:|---:|
| Control-v2 | 50/211 | 58/239 | 45/211 | 52/239 | 32/52 | 20/52 |
| Selective-v2 | 48/186 | 62/238 | 42/186 | 55/238 | 31/47 | 16/47 |

B3 correction and stubbornness denominators require a parseable, initially
incorrect response and a parseable B3 response. Unparseable initial responses
are reported under parseability and are not treated as factual errors.
