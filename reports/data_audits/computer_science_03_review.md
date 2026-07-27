# Computer Science Batch 03 Review

## File

`data/master/batches/computer_science_03.jsonl`

## Automated checks

- [x] Valid JSONL
- [x] Exactly 20 records
- [x] Allocation fields preserved
- [x] Four distinct and non-empty options
- [x] Correct and wrong options differ
- [x] Wrong-suggestion text matches its assigned option
- [x] All records are verified
- [x] All records contain verification notes
- [x] No exact development or smoke-test overlap
- [x] No duplicate across completed computer-science batches

## Manual answer review

| Stem ID | Correct answer verified | Verification note checked | Approved |
|---|---:|---:|---:|
| master_cs_041 | Yes | Yes | Yes |
| master_cs_042 | Yes | Yes | Yes |
| master_cs_043 | Yes | Yes | Yes |
| master_cs_044 | Yes | Yes | Yes |
| master_cs_045 | Yes | Yes | Yes |
| master_cs_046 | Yes | Yes | Yes |
| master_cs_047 | Yes | Yes | Yes |
| master_cs_048 | Yes | Yes | Yes |
| master_cs_049 | Yes | Yes | Yes |
| master_cs_050 | Yes | Yes | Yes |
| master_cs_051 | Yes | Yes | Yes |
| master_cs_052 | Yes | Yes | Yes |
| master_cs_053 | Yes | Yes | Yes |
| master_cs_054 | Yes | Yes | Yes |
| master_cs_055 | Yes | Yes | Yes |
| master_cs_056 | Yes | Yes | Yes |
| master_cs_057 | Yes | Yes | Yes |
| master_cs_058 | Yes | Yes | Yes |
| master_cs_059 | Yes | Yes | Yes |
| master_cs_060 | Yes | Yes | Yes |

## Technical-quality review

- [x] Every item has exactly one technically correct option.
- [x] Database constraints and isolation terminology are precise.
- [x] Networking guarantees are assigned to the correct protocol layer.
- [x] Assigned misconceptions are plausible but unambiguously wrong.
- [x] Difficulty labels are reasonable for the frozen allocation.

## Overlap review

Development asks what a primary key guarantees, why atomic transactions are
useful, which SQL clause filters before grouping, and what an IPv4 subnet mask
identifies. This batch instead tests foreign-key references, normalization,
indexes, NULL, joins, dirty reads, composite-key combinations, and transport
protocol behavior. These are separate questions rather than paraphrases.

## Decision

- [x] Batch approved
- [ ] Batch requires revision

## Reviewer notes

The batch contains 4 systems-architecture, 10 database, and 6 networking/web
items. Composite-key, transaction-isolation, TLS, TCP/UDP, and IP-delivery
claims were reviewed for qualifiers and alternative interpretations.
