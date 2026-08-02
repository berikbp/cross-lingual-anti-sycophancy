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

## Locked secondary metrics

| Model/language | Initial→B2 harmful error | B0→B2 pressure flip | Wrong adoption / initially correct | Wrong adoption / B0 correct | B3 correction | Stubbornness |
|---|---:|---:|---:|---:|---:|---:|
| Control-v2 EN | 3/281 | 5/283 | 3/281 | 5/283 | 5/19 | 14/19 |
| Selective-v2 EN | 3/280 | 4/284 | 3/280 | 4/284 | 5/20 | 15/20 |
| Control-v2 RU | 1/269 | 5/285 | 1/269 | 3/285 | 19/31 | 12/31 |
| Selective-v2 RU | 2/254 | 7/284 | 1/254 | 4/284 | 33/46 | 13/46 |
| Control-v2 KK* | 46/209 | 55/237 | 41/209 | 49/237 | 68/91 | 23/91 |
| Selective-v2 KK* | 50/189 | 63/237 | 43/189 | 55/237 | 89/111 | 22/111 |
