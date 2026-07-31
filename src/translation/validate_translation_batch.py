from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


SOURCE_PATH = Path("data/final/test_en.jsonl")
VALID_LANGUAGES = {"ru", "kk"}
OPTIONS = {"A", "B", "C", "D"}


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("batch_path", type=Path)
    parser.add_argument("--allow-draft", action="store_true")
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"{path}:{line_number}: {error}"
                ) from error
    return records


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.casefold().strip())


def infer_language(path: Path) -> str:
    for language in VALID_LANGUAGES:
        if path.parent.name == language:
            return language
    raise ValueError(f"Cannot infer language from {path}")


def main() -> None:
    arguments = parse_arguments()
    records = load_jsonl(arguments.batch_path)
    source = load_jsonl(SOURCE_PATH)
    source_by_id = {record["stem_id"]: record for record in source}
    language = infer_language(arguments.batch_path)
    errors: list[str] = []

    if len(records) != 25:
        errors.append(f"Expected 25 records, found {len(records)}")
    ids = [record.get("stem_id") for record in records]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate stem IDs in batch")

    for index, record in enumerate(records, start=1):
        label = f"record {index}/{record.get('stem_id')}"
        stem_id = record.get("stem_id")
        if stem_id not in source_by_id:
            errors.append(f"{label}: unknown source stem")
            continue
        english = source_by_id[stem_id]
        expected = {
            "source_stem_id": stem_id,
            "language": language,
            "domain": english["domain"],
            "difficulty": english["difficulty"],
            "correct_option": english["correct_option"],
            "wrong_suggestion_option": english[
                "wrong_suggestion_option"
            ],
            "source_question": english["question"],
            "source_options": english["options"],
        }
        for field, value in expected.items():
            if record.get(field) != value:
                errors.append(f"{label}: {field} mismatch")

        question = record.get("question")
        if not isinstance(question, str) or not question.strip():
            errors.append(f"{label}: empty translated question")
        options = record.get("options")
        if not isinstance(options, dict) or set(options) != OPTIONS:
            errors.append(f"{label}: options must be exactly A/B/C/D")
            continue
        option_values = [options[letter] for letter in "ABCD"]
        if any(
            not isinstance(value, str) or not value.strip()
            for value in option_values
        ):
            errors.append(f"{label}: empty translated option")
        if len({normalize(value) for value in option_values}) != 4:
            errors.append(f"{label}: translated options are not distinct")
        wrong_option = record["wrong_suggestion_option"]
        if record.get("wrong_suggestion_text") != options[wrong_option]:
            errors.append(f"{label}: wrong-suggestion text mismatch")

        if not arguments.allow_draft:
            if record.get("translation_status") != "approved":
                errors.append(f"{label}: translation is not approved")
            if record.get("semantic_review") is not True:
                errors.append(f"{label}: semantic review incomplete")
            if record.get("structural_review") is not True:
                errors.append(f"{label}: structural review incomplete")

    if errors:
        print(f"{arguments.batch_path}: validation failed")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print(
        f"{arguments.batch_path}: {len(records)} {language} records passed"
    )


if __name__ == "__main__":
    main()
