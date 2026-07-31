# V2 Adapter Qualification

This is an engineering reload and transition check on eight frozen SFT-validation conversations per adapter. It is not evidence of generalization.

| Adapter | CW | WC | CC | WW | Parseable | Correct |
|---|---:|---:|---:|---:|---:|---:|
| Control-v2 | 1/2 | 2/2 | 2/2 | 1/2 | 8/8 | 6/8 |
| Selective-v2 | 1/2 | 2/2 | 2/2 | 2/2 | 8/8 | 7/8 |

- Base model: `Qwen/Qwen3-4B-Instruct-2507`
- Revision: `cdbee75f17c01a7cc42f958dc650907174af0554`
- Subset rule: first two validation examples per transition category
- Generation: deterministic

## Adapter hashes

- control_v2: `4b0ce354537e718b7998aa35a7bce15f1fa9e1f85b1936969bbaecd285365841`
- selective_correction_v2: `e69e0ed31eed65122274d698634624c1f1b5780a299de7d9e1c580e77b5c04d0`
