# Final English Split Audit

## Protocol

- Protocol version: 1.0
- Split seed: 20260727
- Master size: 400
- Final test size: 300
- Reserve size: 100
- Model evaluation performed before split: no

## Master artifact

- File: `data/master/master_en.jsonl`
- SHA-256: `96e2bafddf7b78ff7b291d6eacc16ca18e2eb592aeb83b4cb5f78d9296361f7d`

## Final test artifact

- File: `data/final/test_en.jsonl`
- SHA-256: `e3c0574fff68e14d70fbc395e4a5624bc0d68b545ab2a8ae36f516f33c74d429`

## Reserve artifact

- File: `data/final/reserve_en.jsonl`
- SHA-256: `e614e349ba6c7459abe2b3deb2f5c68b30fcdd671986ffb505134e9315aceaf9`

## Membership audit

- [x] Master contains 400 unique stems
- [x] Test contains 300 unique stems
- [x] Reserve contains 100 unique stems
- [x] Test and reserve are disjoint
- [x] Test union reserve equals master
- [x] Manifest ordering matches output files
- [x] Manifest hashes match physical files

## Final-test distribution

### Domains

| Domain | Count |
|---|---:|
| Mathematics | 65 |
| Science | 56 |
| Computer science | 59 |
| Geography | 60 |
| Logic | 60 |
| **Total** | **300** |

### Difficulty

| Difficulty | Count |
|---|---:|
| Easy | 117 |
| Medium | 154 |
| Hard | 29 |
| **Total** | **300** |

### Correct-option positions

| Option | Count |
|---|---:|
| A | 75 |
| B | 66 |
| C | 86 |
| D | 73 |
| **Total** | **300** |

### Wrong-suggestion positions

| Option | Count |
|---|---:|
| A | 69 |
| B | 79 |
| C | 69 |
| D | 83 |
| **Total** | **300** |

## Reserve distribution

### Domains

| Domain | Count |
|---|---:|
| Mathematics | 15 |
| Science | 24 |
| Computer science | 21 |
| Geography | 20 |
| Logic | 20 |
| **Total** | **100** |

### Difficulty

| Difficulty | Count |
|---|---:|
| Easy | 43 |
| Medium | 46 |
| Hard | 11 |
| **Total** | **100** |

### Correct-option positions

| Option | Count |
|---|---:|
| A | 25 |
| B | 34 |
| C | 14 |
| D | 27 |
| **Total** | **100** |

### Wrong-suggestion positions

| Option | Count |
|---|---:|
| A | 31 |
| B | 21 |
| C | 31 |
| D | 17 |
| **Total** | **100** |

## Distribution interpretation

The deterministic shuffle produced modest random imbalance. Every domain has
at least 56 final-test items, each correct and wrong option appears at least
66 and 69 times respectively in the final test, and hard questions occur in
both final test and reserve. Following the frozen rule, the seed was not
changed to optimize these counts.

## Decision

- [x] The deterministic final split is frozen.
- [x] No model has evaluated the master, test, or reserve questions.
- [x] Final-test questions may not be used for development or training.
- [x] Reserve replacements are permitted only for pre-evaluation factual, duplication, or translation failures.
