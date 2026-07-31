# Multilingual Final Evaluation Specification

## Purpose

Create frozen Russian and Kazakh translations of the 300-question English final evaluation set.

## Languages

- English: source language
- Russian: translated language
- Kazakh: translated language using Cyrillic script

## Source artifact

- English source: `data/final/test_en.jsonl`
- Expected records: 300
- Source split manifest: `data/final/split_manifest.json`

## Translation principles

Each translation must preserve:

- the factual meaning of the question;
- the correct answer;
- the assigned wrong suggestion;
- option order;
- answer labels A/B/C/D;
- domain;
- difficulty;
- stem identity;
- reasoning requirements;
- level of specificity.

Translations must not add hints, explanations, definitions, or context absent from the English source.

## Allowed adaptations

A translation may adjust:

- grammar;
- word order;
- punctuation;
- natural terminology;
- measurement notation;
- culturally unnatural phrasing.

An adaptation must not change the answer or reduce the reasoning required.

## Prohibited changes

Do not:

- reorder options;
- replace distractors with easier distractors;
- simplify hard questions;
- add explanatory context;
- translate proper nouns incorrectly;
- change mathematical expressions;
- alter scientific units;
- change logical quantifiers;
- use Russian words inside Kazakh unless the term is accepted technical usage or explicitly documented;
- select translation wording based on model performance.

## Translation workflow

1. Translate from the frozen English source.
2. Conduct structural validation.
3. Conduct semantic review.
4. Record ambiguities or defects.
5. Replace a source stem only when an objective pre-inference defect cannot be repaired safely.
6. Freeze files and hashes before model evaluation.

## Evaluation restrictions

During translation and review:

- no base-model inference;
- no adapter inference;
- no comparison of model performance;
- no prompt calibration;
- no use of final questions for training.

## Replacement policy

Reserve replacements are allowed only for:

- objectively incorrect English answer keys;
- irreparable ambiguity;
- duplicate final-test content;
- translation impossibility without changing the tested concept;
- culturally or linguistically invalid option structure.

Every replacement must be documented before inference.
