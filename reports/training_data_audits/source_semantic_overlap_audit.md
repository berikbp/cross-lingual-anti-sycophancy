# Source-Stem Semantic Overlap Audit

## Scope

The 1,000 training stems and 100 validation stems were compared with:

- development questions;
- manual-pilot questions;
- smoke-test questions;
- the 400-stem master pool;
- the final-test split;
- the reserve split.

## Automated results

- Exact normalized overlap with excluded questions: 0
- Exact duplicate questions within the source pool: 0
- Duplicate source IDs: 0
- Train/validation question overlap: 0

## High-similarity review

A conservative token-similarity screen flagged five pairs at or above 0.90.
Each was manually reviewed:

| Source stem | Compared item | Decision |
|---|---|---|
| `train_geo_0029` | Capital of Austria versus capital of Australia | Retained: different countries and answers; similarity is lexical. |
| `train_science_0134` | Parallel 6-ohm/3-ohm resistors versus series 2-ohm/3-ohm resistors | Retained: different circuit operation and reasoning. |
| `train_math_0050` | Multiplication involving a negative integer versus decimal multiplication | Retained: different mathematical skill. |
| `train_math_0130` | Subtraction involving a negative integer versus multiplication | Retained: different operation and answer structure. |
| `train_math_0139` | Division-by-zero concept versus ordinary division of 100 by 4 | Retained: different mathematical concept. |

No flagged pair reproduced an evaluation question's underlying problem.

## Construction rule

Questions were written from stable topic families and mapped mechanically to
the frozen allocation manifest. No model output was used to select, reject,
or revise a source stem.

## Decision

- [x] Exact leakage checks passed.
- [x] High-similarity candidates were manually reviewed.
- [x] Training and validation source stems are disjoint from evaluation data.
