# Kazakh v2 native-review protocol

## Purpose

This review repairs the original Kazakh translation without replacing the
historical Stage 19 artifacts. Its output is a separately versioned sensitivity
dataset. No evaluation-model output or development result may be used to choose
translation wording.

## Reviewer

The reviewer must be an identified, proficient native speaker of Kazakh who
can assess academically neutral multiple-choice questions. Record the same
real reviewer name and review date on every row. If more than one person
reviews the file, enter the responsible reviewer for each row and describe the
division of work in the final audit.

## Worksheet

Use `reports/translation_audits/kazakh_v2_native_review.csv`. It contains the
English source and editable Kazakh question and option columns side by side.
For each of the 300 rows:

1. Compare the complete English question and all four options with Kazakh.
2. Correct the `kazakh_question` or `kazakh_A` through `kazakh_D` cells when
   needed; never change answer labels, option order, or metadata.
3. Confirm that the keyed answer remains correct and the assigned wrong option
   remains wrong and plausible.
4. Confirm that distractor distinctions, quantifiers, negation, units,
   notation, and reasoning difficulty are preserved.
5. Set `semantic_equivalence`, `answer_preserved`, `distractors_preserved`, and
   `language_quality` to `yes` only after checking them.
6. Set `decision` to `approved`, add the reviewer and ISO date (`YYYY-MM-DD`),
   and write a concrete review note. A row needing more work stays unapproved.

The original model answers must not be shown to the reviewer during this
process.

## Import and freeze

After all rows are approved:

```bash
uv run python -m src.translation.import_kazakh_v2_native_review
uv run python -m src.translation.finalize_kazakh_v2 \
  --reviewed data/translation/review/kazakh_v2_native_reviewed.jsonl
```

Both commands fail closed on incomplete, anonymous, empty, structurally
changed, or duplicate-option records. Preserve the completed worksheet as the
review log. Then run the separately named `corrected_kazakh_v2` evaluation
described in `docs/zenodo_release.md`.
