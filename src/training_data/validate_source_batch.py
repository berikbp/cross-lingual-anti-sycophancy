from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ALLOCATION_PATH = Path(
    "data/training/source/training_allocation_manifest.json"
)

EXCLUSION_PATH = Path(
    "reports/training_data_audits/excluded_training_questions.txt"
)

VALID_OPTIONS = {"A", "B", "C", "D"}

REQUIRED_FIELDS = {
    "stem_id",
    "split",
    "domain",
    "difficulty",
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
    return re.sub(r"[^\w\s]", "", text)


def normalize_option(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
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


def load_allocations(
) -> tuple[
    dict[str, dict[str, str]],
    dict[str, int],
]:
    manifest = json.loads(
        ALLOCATION_PATH.read_text(encoding="utf-8")
    )

    allocations = {
        record["stem_id"]: record
        for record in manifest["allocations"]
    }

    positions = {
        record["stem_id"]: index
        for index, record in enumerate(
            manifest["allocations"]
        )
    }

    return allocations, positions


def load_excluded_questions() -> set[str]:
    questions: set[str] = set()

    for line in EXCLUSION_PATH.read_text(
        encoding="utf-8"
    ).splitlines():
        parts = line.split("\t", maxsplit=2)

        if len(parts) == 3:
            questions.add(normalize_text(parts[2]))

    return questions


def validate_record(
    record: dict[str, Any],
    path: Path,
    allocations: dict[str, dict[str, str]],
) -> list[str]:
    location = f"{path}:{record['_line_number']}"
    errors: list[str] = []
    missing = REQUIRED_FIELDS - record.keys()

    if missing:
        return [
            f"{location}: missing fields {sorted(missing)}"
        ]

    allocation = allocations.get(record["stem_id"])

    if allocation is None:
        errors.append(f"{location}: unknown stem ID")
    else:
        for field in (
            "split",
            "domain",
            "difficulty",
            "correct_option",
            "wrong_suggestion_option",
        ):
            if record[field] != allocation[field]:
                errors.append(
                    f"{location}: {field} changed; expected "
                    f"{allocation[field]!r}, found {record[field]!r}"
                )

    options = record["options"]

    if not isinstance(options, dict):
        errors.append(f"{location}: options must be an object")
        return errors

    if set(options) != VALID_OPTIONS:
        errors.append(
            f"{location}: options must be exactly A/B/C/D"
        )
        return errors

    if any(
        not isinstance(value, str) or not value.strip()
        for value in options.values()
    ):
        errors.append(f"{location}: empty option")

    if len(
        {
            normalize_option(value)
            for value in options.values()
        }
    ) != 4:
        errors.append(f"{location}: duplicate option text")

    correct = record["correct_option"]
    wrong = record["wrong_suggestion_option"]

    if correct not in VALID_OPTIONS or wrong not in VALID_OPTIONS:
        errors.append(f"{location}: invalid option letter")
    elif correct == wrong:
        errors.append(
            f"{location}: correct and wrong options match"
        )

    if (
        wrong in options
        and record["wrong_suggestion_text"] != options[wrong]
    ):
        errors.append(
            f"{location}: wrong-suggestion text mismatch"
        )

    if (
        not isinstance(record["question"], str)
        or not record["question"].strip()
    ):
        errors.append(f"{location}: empty question")

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
    parser.add_argument("--expected-count", type=int, default=50)
    args = parser.parse_args()

    records = load_jsonl(args.path)
    allocations, allocation_positions = load_allocations()
    exclusions = load_excluded_questions()
    errors: list[str] = []

    for record in records:
        errors.extend(
            validate_record(record, args.path, allocations)
        )

    stem_ids = [record.get("stem_id") for record in records]
    duplicate_ids = [
        stem_id
        for stem_id, count in Counter(stem_ids).items()
        if count > 1
    ]

    if duplicate_ids:
        errors.append(f"Duplicate stem IDs: {duplicate_ids}")

    known_positions = [
        allocation_positions[stem_id]
        for stem_id in stem_ids
        if stem_id in allocation_positions
    ]

    if len(known_positions) == len(stem_ids):
        expected_positions = list(
            range(
                known_positions[0],
                known_positions[0] + len(known_positions),
            )
        )

        if known_positions != expected_positions:
            errors.append(
                "Records are not one contiguous, manifest-ordered "
                "allocation block"
            )

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
            f"Duplicate questions: {duplicate_questions}"
        )

    overlaps = sorted(set(questions) & exclusions)

    if overlaps:
        errors.append(
            f"Exact excluded-question overlaps: {overlaps}"
        )

    if len(records) != args.expected_count:
        errors.append(
            f"Expected {args.expected_count} records, "
            f"found {len(records)}"
        )

    print(f"File: {args.path}")
    print(f"Records: {len(records)}")
    print(
        "Domains:",
        dict(Counter(r.get("domain") for r in records)),
    )
    print(
        "Difficulties:",
        dict(Counter(r.get("difficulty") for r in records)),
    )
    print(
        "Correct options:",
        dict(
            Counter(r.get("correct_option") for r in records)
        ),
    )
    print(
        "Wrong options:",
        dict(
            Counter(
                r.get("wrong_suggestion_option")
                for r in records
            )
        ),
    )

    if errors:
        print()
        print("Validation failed:")

        for error in errors:
            print(f"- {error}")

        raise SystemExit(1)

    print()
    print("Source-batch validation passed.")


if __name__ == "__main__":
    main()
