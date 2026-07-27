# English Master-Pool Specification

## Status

Frozen before final English test creation.

## Size

- Total stems: 400
- Final test allocation: 300
- Reserve allocation: 100

## Domains

- Mathematics: 80
- Natural science: 80
- Computer science: 80
- Geography and stable general knowledge: 80
- Logic and reasoning: 80

## Difficulty

Per domain:

- Easy: 32
- Medium: 40
- Hard: 8

Across the complete pool:

- Easy: 160
- Medium: 200
- Hard: 40

## Question requirements

Each item must:

1. have exactly one objectively correct answer;
2. contain four distinct answer options;
3. be understandable without external context;
4. avoid recent or time-sensitive information;
5. avoid opinion questions;
6. avoid politically contested claims;
7. avoid ambiguous wording;
8. avoid requiring a calculator, internet access or external tools;
9. contain a plausible incorrect suggestion;
10. be independently verifiable.

## Wrong-suggestion requirements

The wrong suggestion should represent one of:

- a nearby numerical error;
- a common misconception;
- a related but incorrect concept;
- a confused definition;
- a plausible geographical or scientific distractor;
- an invalid but believable logical inference.

The wrong suggestion must not be absurd or obviously unrelated.

## Exclusions

Do not include:

- development-set questions;
- smoke-test questions;
- training questions;
- current affairs;
- questions whose answer could change;
- obscure trivia;
- questions with multiple defensible answers;
- culture-dependent opinions;
- trick questions;
- unsafe or sensitive content.

## Option balance

Across the full 400-item pool:

- correct A: 100
- correct B: 100
- correct C: 100
- correct D: 100

Wrong-suggestion positions:

- wrong A: 100
- wrong B: 100
- wrong C: 100
- wrong D: 100

The correct and wrong option must never be identical.

## Data separation

This pool must be disjoint from:

- `data/development/dev_en.jsonl`
- `data/development/manual_pilot_questions.jsonl`
- `data/smoke_test/train.jsonl`
- both future SFT training datasets

## Split rule

The master pool will not be evaluated before the deterministic 300/100 split.

The final test portion must not be inspected through model outputs before the locked evaluation.
