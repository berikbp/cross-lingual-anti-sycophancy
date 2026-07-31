# Translated Record Schema

Each line in a translated JSONL file is an object with these fields:

```json
{
  "stem_id": "master_math_0042",
  "source_stem_id": "master_math_0042",
  "language": "ru",
  "domain": "mathematics",
  "difficulty": "medium",
  "question": "Translated question",
  "options": {
    "A": "Translated option A",
    "B": "Translated option B",
    "C": "Translated option C",
    "D": "Translated option D"
  },
  "correct_option": "C",
  "wrong_suggestion_option": "B",
  "wrong_suggestion_text": "Translated option B",
  "source_question": "Original English question",
  "source_options": {
    "A": "Original option A",
    "B": "Original option B",
    "C": "Original option C",
    "D": "Original option D"
  },
  "translation_status": "approved",
  "translator_note": "",
  "semantic_review": true,
  "structural_review": true,
  "review_note": ""
}
```

## Status values

- `draft`
- `needs_revision`
- `approved`
- `replacement_required`

## Frozen fields

The following fields must exactly match the aligned English source record:

- `stem_id`
- `source_stem_id`
- `domain`
- `difficulty`
- `correct_option`
- `wrong_suggestion_option`
- `source_question`
- `source_options`

The translated `wrong_suggestion_text` must exactly equal the target-language option at `wrong_suggestion_option`.
