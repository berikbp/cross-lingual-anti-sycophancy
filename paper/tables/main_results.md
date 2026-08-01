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
| Kazakh | 17.7 pp | 19.3 pp | -1.7 pp | [-5.0, 2.0] |
| Macro-average | — | — | -0.4 pp | — |

## Locked secondary metrics

| Model/language | B0 | B2 | Harmful flips | Wrong adoption | B3 correction | Stubbornness |
|---|---:|---:|---:|---:|---:|---:|
| Control-v2 EN | 283/300 | 278/300 | 3/281 | 11/300 | 5/19 | 14/19 |
| Selective-v2 EN | 284/300 | 281/300 | 3/280 | 8/300 | 5/20 | 15/20 |
| Control-v2 RU | 285/300 | 280/300 | 1/269 | 11/300 | 19/31 | 12/31 |
| Selective-v2 RU | 284/300 | 278/300 | 2/254 | 13/300 | 33/46 | 13/46 |
| Control-v2 KK | 237/300 | 184/300 | 46/209 | 89/300 | 68/91 | 23/91 |
| Selective-v2 KK | 237/300 | 179/300 | 50/189 | 94/300 | 89/111 | 22/111 |
