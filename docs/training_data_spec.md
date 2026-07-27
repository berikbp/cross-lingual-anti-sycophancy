# Training Data Specification

## Purpose

Create two matched English supervised fine-tuning datasets:

1. conversational factual-SFT control;
2. anti-sycophancy SFT.

The datasets must differ mainly in whether the user applies an incorrect
factual suggestion.

## Sizes

- Training stems: 1,000
- Validation stems: 100
- Control training conversations: 1,000
- Anti-sycophancy training conversations: 1,000
- Control validation conversations: 100
- Anti-sycophancy validation conversations: 100

## Domains

Each training dataset contains:

- mathematics: 200
- science: 200
- computer science: 200
- geography: 200
- logic: 200

Each validation dataset contains:

- mathematics: 20
- science: 20
- computer science: 20
- geography: 20
- logic: 20

## Difficulty

Training:

- easy: 400
- medium: 500
- hard: 100

Validation:

- easy: 40
- medium: 50
- hard: 10

## Data separation

Training and validation questions must be disjoint from:

- `data/development/dev_en.jsonl`
- `data/development/manual_pilot_questions.jsonl`
- `data/smoke_test/train.jsonl`
- `data/master/master_en.jsonl`
- `data/final/test_en.jsonl`
- `data/final/reserve_en.jsonl`

Training and validation stems must also be mutually disjoint.

## Shared structure

For each stem, both datasets use:

- the same system prompt;
- the same multiple-choice question;
- the same answer options;
- the same initial assistant response;
- the same correct final answer;
- the same JSON output format;
- the same number of conversational turns.

## Control condition

The user asks the assistant to reconsider neutrally without suggesting an
answer.

The assistant preserves or gives the correct answer.

## Anti-sycophancy condition

The user explicitly suggests one incorrect option.

The assistant rejects the misleading suggestion and gives the correct answer.

## Loss masking

Training loss is calculated only on the final assistant response.

The following context must be masked:

- system message;
- original user question;
- initial assistant response;
- follow-up user message.

The deliberately wrong suggestion must never become a supervised target.

## Output format

The final assistant response uses:

`{"answer": "B"}`

A short factual sentence may precede the JSON only if the same format is used
in both datasets.

## Matching constraints

The control and anti-sycophancy datasets must have identical:

- stem IDs;
- domains;
- difficulty labels;
- answer positions;
- initial assistant responses;
- final correct answers;
- system prompts;
- number of examples;
- dataset ordering.

Only the follow-up user message differs.

## Prohibited design choices

Do not:

- train the anti-sycophancy dataset on only one answer letter;
- make control examples one-turn while anti-sycophancy examples are multi-turn;
- supervise incorrect prior assistant responses;
- reuse final-test questions;
- select training examples based on final-test performance;
- use authority prompts in the MVP;
- include Russian or Kazakh training examples in the primary experiment.
