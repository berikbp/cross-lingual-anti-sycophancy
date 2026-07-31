# Translation Assistance Amendment

## Status

Stage 18 translation is incomplete:

- Russian approved: 200/300
- Russian remaining: 100
- Kazakh approved: 0/300
- Kazakh remaining: 300

No evaluation-model inference has occurred.

## Clarification of the no-inference restriction

The original restriction prohibited model inference during final-test preparation.
This amendment distinguishes between evaluation-model inference and translation assistance.

## Prohibited inference

The frozen base evaluation model, Control-v1, Anti-sycophancy-v1, Control-v2, and Selective-correction-v2 may not access final-test, reserve, or translated final-test records before locked evaluation. Their outputs may not be used to assess difficulty, choose wording, identify favorable translations, select replacements, tune prompts, alter answer keys, or filter records.

## Permitted translation assistance

A separate external translation system may create draft Russian or Kazakh translations only. Machine-generated translations are not approved until human review. The translation system must not answer questions, evaluate correctness, rank distractors, rewrite questions for model behavior, or receive development/model-performance results.

## Human-review requirement

Every machine-assisted translation requires structural, semantic-equivalence, answer-preservation, distractor-preservation, and language-quality review. Reviewers must confirm that correct and wrong-suggestion options, ordering, hints, and reasoning requirements are unchanged.

## Disclosure

The final report will state the translation system, version or access date when available, languages using assistance, that all translations received manual review, and that evaluation models did not participate.

## Freeze rule

No model evaluation may begin until all 600 translated records are approved, batch reviews are complete, multilingual alignment passes, hashes are recorded, and translation artifacts are committed and pushed.
