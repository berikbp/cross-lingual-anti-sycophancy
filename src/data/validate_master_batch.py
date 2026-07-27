from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


VALID_OPTIONS = {"A", "B", "C", "D"}

REQUIRED_FIELDS = {
    "stem_id",
    "domain",
    "difficulty",
    "source_type",
    "source_reference",
    "question",
    "options",
    "correct_option",
    "wrong_suggestion_option",
    "wrong_suggestion_text",
    "verified",
    "verification_note",
    "notes",
}


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text


def normalize_option(text: str) -> str:
    return " ".join(text.lower().split())


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"{path}:{line_number}: invalid JSON: {error}"
                ) from error

            record["_line_number"] = line_number
            records.append(record)

    return records


def validate_record(
    record: dict[str, Any],
    path: Path,
) -> list[str]:
    errors: list[str] = []
    line_number = record["_line_number"]
    location = f"{path}:{line_number}"

    missing = REQUIRED_FIELDS - record.keys()

    if missing:
        errors.append(
            f"{location}: missing fields {sorted(missing)}"
        )
        return errors

    if (
        not isinstance(record["question"], str)
        or not record["question"].strip()
    ):
        errors.append(f"{location}: empty question")

    options = record["options"]

    if not isinstance(options, dict):
        errors.append(f"{location}: options must be an object")
        return errors

    if set(options) != VALID_OPTIONS:
        errors.append(
            f"{location}: options must be exactly A, B, C and D"
        )
        return errors

    if any(
        not isinstance(value, str) or not value.strip()
        for value in options.values()
    ):
        errors.append(f"{location}: one or more options are empty")

    normalized_options = [
        normalize_option(value)
        for value in options.values()
    ]

    if len(set(normalized_options)) != 4:
        errors.append(f"{location}: duplicate option text")

    correct = record["correct_option"]
    wrong = record["wrong_suggestion_option"]

    if correct not in VALID_OPTIONS:
        errors.append(f"{location}: invalid correct option")

    if wrong not in VALID_OPTIONS:
        errors.append(f"{location}: invalid wrong option")

    if correct == wrong:
        errors.append(
            f"{location}: correct and wrong options are identical"
        )

    if (
        wrong in options
        and record["wrong_suggestion_text"] != options[wrong]
    ):
        errors.append(
            f"{location}: wrong_suggestion_text does not match "
            f"option {wrong}"
        )

    if record["difficulty"] not in {"easy", "medium", "hard"}:
        errors.append(f"{location}: invalid difficulty")

    if record["verified"] is not True:
        errors.append(f"{location}: verified must be true")

    if (
        not isinstance(record["verification_note"], str)
        or not record["verification_note"].strip()
    ):
        errors.append(f"{location}: missing verification note")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--expected-count", type=int, default=20)
    args = parser.parse_args()

    records = load_jsonl(args.path)
    errors: list[str] = []

    for record in records:
        errors.extend(validate_record(record, args.path))

    stem_ids = [record.get("stem_id") for record in records]

    duplicate_ids = [
        stem_id
        for stem_id, count in Counter(stem_ids).items()
        if count > 1
    ]

    if duplicate_ids:
        errors.append(f"Duplicate stem IDs: {duplicate_ids}")

    questions = [
        normalize_text(record.get("question", ""))
        for record in records
        if record.get("question")
    ]

    duplicate_questions = [
        question
        for question, count in Counter(questions).items()
        if count > 1
    ]

    if duplicate_questions:
        errors.append(
            f"Duplicate questions within batch: {duplicate_questions}"
        )

    if len(records) != args.expected_count:
        errors.append(
            f"Expected {args.expected_count} records, found {len(records)}"
        )

    print(f"File: {args.path}")
    print(f"Records: {len(records)}")
    print(
        "Difficulties:",
        dict(
            Counter(
                record.get("difficulty")
                for record in records
            )
        ),
    )
    print(
        "Correct options:",
        dict(
            Counter(
                record.get("correct_option")
                for record in records
            )
        ),
    )
    print(
        "Wrong options:",
        dict(
            Counter(
                record.get("wrong_suggestion_option")
                for record in records
            )
        ),
    )

    if errors:
        print("\nValidation failed:")

        for error in errors:
            print(f"- {error}")

        raise SystemExit(1)

    print("\nBatch validation passed.")


if __name__ == "__main__":
    main()
