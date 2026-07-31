# Selective-Correction v2 Training Specification

## Motivation

The v1 datasets always presented a correct initial assistant answer and always supervised the same answer after the follow-up.

The resulting adapters learned indiscriminate answer preservation rather than selective resistance to incorrect pressure.

The v2 datasets introduce both correct and incorrect initial assistant answers and both correct and incorrect user suggestions.

## Experimental conditions

### Control-v2

The user asks the assistant to reconsider neutrally.

### Selective-correction-v2

The user explicitly suggests an answer that may be correct or incorrect.

## Matching

For every source stem, the two conditions use identical:

- source question;
- answer options;
- stem ID;
- domain;
- difficulty;
- transition category;
- initial assistant answer;
- final assistant answer;
- final correct target;
- message count;
- dataset ordering.

Only the follow-up user message differs.

## Source data

Reuse the frozen Stage 11 source files:

- `data/training/source/train_stems_en.jsonl`
- `data/training/source/validation_stems_en.jsonl`

No new factual stems are created.

## Dataset sizes

- Control-v2 training: 1,000
- Selective-correction-v2 training: 1,000
- Control-v2 validation: 100
- Selective-correction-v2 validation: 100

## Transition categories

### CW — Correct initial, wrong user suggestion

- Initial assistant answer: correct
- User suggestion: wrong
- Final assistant answer: correct
- Desired behavior: preserve the correct answer

### WC — Wrong initial, correct user suggestion

- Initial assistant answer: wrong
- User suggestion: correct
- Final assistant answer: correct
- Desired behavior: accept beneficial correction

### CC — Correct initial, correct user suggestion

- Initial assistant answer: correct
- User suggestion: correct
- Final assistant answer: correct
- Desired behavior: preserve a correct answer without reflexively rejecting feedback

### WW — Wrong initial, wrong user suggestion

- Initial assistant answer: wrong
- User suggestion: a different wrong option
- Final assistant answer: correct
- Desired behavior: reject incorrect feedback and self-correct

## Transition balance

Training:

- CW: 250
- WC: 250
- CC: 250
- WW: 250

Validation:

- CW: 25
- WC: 25
- CC: 25
- WW: 25

Within every training domain:

- CW: 50
- WC: 50
- CC: 50
- WW: 50

Within every validation domain:

- CW: 5
- WC: 5
- CC: 5
- WW: 5

## Final targets

Every final assistant target is the objectively correct answer.

The initial assistant response may be correct or deliberately incorrect depending on the assigned transition category.

## Loss masking

Only the final assistant message contributes to the training loss.

The following messages are masked:

- system prompt;
- source question;
- initial assistant response;
- follow-up user message.

Incorrect initial answers and incorrect user suggestions must never be supervised.

## Model initialization

Both v2 adapters will be trained independently from the frozen base model.

The v1 adapter weights will not be used as initialization.

## Evaluation restrictions

The frozen final test and reserve remain inaccessible.

The first evaluation of v2 will use the existing 100-question English development set.

## Frozen proportions

CW, WC, CC, and WW each comprise exactly 25% of both splits. These proportions may not be changed after v2 development results are observed. Any later rebalancing requires a separately named v3 experiment.
