from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


DATA_PATH = Path("data/development/dev_en.jsonl")

VALID_OPTIONS = {"A", "B", "C", "D"}

EXPECTED_DOMAIN_DIFFICULTIES = {
    domain: {"easy": 8, "medium": 10, "hard": 2}
    for domain in {
        "mathematics",
        "science",
        "computer_science",
        "geography",
        "logic",
    }
}

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
    "notes",
}


def validate_record(
    record: dict[str, Any],
    line_number: int,
) -> list[str]:
    errors: list[str] = []

    missing = REQUIRED_FIELDS - record.keys()

    if missing:
        errors.append(
            f"Line {line_number}: missing fields {sorted(missing)}"
        )
        return errors

    options = record["options"]

    if set(options.keys()) != VALID_OPTIONS:
        errors.append(
            f"Line {line_number}: options must be exactly A/B/C/D"
        )

    correct = record["correct_option"]
    wrong = record["wrong_suggestion_option"]

    if correct not in VALID_OPTIONS:
        errors.append(
            f"Line {line_number}: invalid correct option {correct}"
        )

    if wrong not in VALID_OPTIONS:
        errors.append(
            f"Line {line_number}: invalid wrong option {wrong}"
        )

    if correct == wrong:
        errors.append(
            f"Line {line_number}: correct and wrong options match"
        )

    if (
        wrong in options
        and record["wrong_suggestion_text"] != options[wrong]
    ):
        errors.append(
            f"Line {line_number}: wrong suggestion text "
            "does not match its option"
        )

    if not record["question"].strip():
        errors.append(
            f"Line {line_number}: empty question"
        )

    if len(set(options.values())) != 4:
        errors.append(
            f"Line {line_number}: duplicate option text"
        )

    if record["difficulty"] not in {
        "easy",
        "medium",
        "hard",
    }:
        errors.append(
            f"Line {line_number}: invalid difficulty"
        )

    if record["verified"] is not True:
        errors.append(
            f"Line {line_number}: record not verified"
        )

    return errors


def main() -> None:
    records: list[dict[str, Any]] = []
    errors: list[str] = []

    with DATA_PATH.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                errors.append(
                    f"Line {line_number}: invalid JSON: {error}"
                )
                continue

            records.append(record)
            errors.extend(
                validate_record(record, line_number)
            )

    stem_ids = [record["stem_id"] for record in records]
    duplicate_ids = [
        stem_id
        for stem_id, count in Counter(stem_ids).items()
        if count > 1
    ]

    if duplicate_ids:
        errors.append(
            f"Duplicate stem IDs: {duplicate_ids}"
        )

    normalized_questions = [
        " ".join(record["question"].lower().split())
        for record in records
    ]

    duplicate_questions = [
        question
        for question, count in Counter(
            normalized_questions
        ).items()
        if count > 1
    ]

    if duplicate_questions:
        errors.append(
            f"Duplicate questions: {duplicate_questions}"
        )

    domain_counts = Counter(
        record["domain"]
        for record in records
    )

    difficulty_counts = Counter(
        record["difficulty"]
        for record in records
    )

    correct_option_counts = Counter(
        record["correct_option"]
        for record in records
    )

    wrong_option_counts = Counter(
        record["wrong_suggestion_option"]
        for record in records
    )

    domain_difficulty_counts = {
        domain: Counter(
            record["difficulty"]
            for record in records
            if record["domain"] == domain
        )
        for domain in EXPECTED_DOMAIN_DIFFICULTIES
    }

    if len(records) != 100:
        errors.append(
            f"Expected 100 records, found {len(records)}"
        )

    for domain, expected in EXPECTED_DOMAIN_DIFFICULTIES.items():
        actual = domain_difficulty_counts[domain]

        if dict(actual) != expected:
            errors.append(
                f"Domain {domain}: expected difficulties "
                f"{expected}, found {dict(actual)}"
            )

    expected_option_counts = Counter(
        {"A": 25, "B": 25, "C": 25, "D": 25}
    )

    if correct_option_counts != expected_option_counts:
        errors.append(
            "Correct options are not balanced: "
            f"{dict(correct_option_counts)}"
        )

    if wrong_option_counts != expected_option_counts:
        errors.append(
            "Wrong suggestions are not balanced: "
            f"{dict(wrong_option_counts)}"
        )

    print(f"Total records: {len(records)}")
    print(f"Domains: {dict(domain_counts)}")
    print(f"Difficulties: {dict(difficulty_counts)}")
    print(
        "Correct-option distribution:",
        dict(correct_option_counts),
    )
    print(
        "Wrong-option distribution:",
        dict(wrong_option_counts),
    )

    if errors:
        print()
        print("Validation failed:")

        for error in errors:
            print(f"- {error}")

        raise SystemExit(1)

    print()
    print("Dataset validation passed.")


if __name__ == "__main__":
    main()
