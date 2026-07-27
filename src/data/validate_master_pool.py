from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


BATCH_DIRECTORY = Path("data/master/batches")
MANIFEST_PATH = Path("data/master/allocation_manifest.json")

DEVELOPMENT_PATHS = [
    Path("data/development/dev_en.jsonl"),
    Path("data/development/manual_pilot_questions.jsonl"),
    Path("data/smoke_test/train.jsonl"),
]

VALID_OPTIONS = {"A", "B", "C", "D"}

EXPECTED_DOMAIN_COUNTS = {
    "mathematics": 80,
    "science": 80,
    "computer_science": 80,
    "geography": 80,
    "logic": 80,
}

EXPECTED_DOMAIN_DIFFICULTIES = {
    domain: {"easy": 32, "medium": 40, "hard": 8}
    for domain in EXPECTED_DOMAIN_COUNTS
}

EXPECTED_DIFFICULTY_COUNTS = {
    "easy": 160,
    "medium": 200,
    "hard": 40,
}

EXPECTED_OPTION_COUNTS = {
    "A": 100,
    "B": 100,
    "C": 100,
    "D": 100,
}

EXPECTED_BATCH_NAMES = {
    f"{domain}_{batch_number:02d}.jsonl"
    for domain in EXPECTED_DOMAIN_COUNTS
    for batch_number in range(1, 5)
}

ID_PREFIXES = {
    "mathematics": "master_math_",
    "science": "master_science_",
    "computer_science": "master_cs_",
    "geography": "master_geo_",
    "logic": "master_logic_",
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
            if not line.strip():
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"{path}:{line_number}: invalid JSON: {error}"
                ) from error

            record["_source_file"] = str(path)
            record["_source_line"] = line_number
            records.append(record)

    return records


def load_allocations() -> dict[str, dict[str, str]]:
    manifest = json.loads(
        MANIFEST_PATH.read_text(encoding="utf-8")
    )

    return {
        record["stem_id"]: record
        for record in manifest["allocations"]
    }


def load_reference_questions() -> set[str]:
    normalized: set[str] = set()

    for path in DEVELOPMENT_PATHS:
        if not path.exists():
            continue

        for record in load_jsonl(path):
            question = record.get("question")

            if isinstance(question, str) and question.strip():
                normalized.add(normalize_text(question))

    return normalized


def validate_record(
    record: dict[str, Any],
    allocations: dict[str, dict[str, str]],
) -> list[str]:
    errors: list[str] = []

    location = (
        f"{record['_source_file']}:"
        f"{record['_source_line']}"
    )

    missing = REQUIRED_FIELDS - record.keys()

    if missing:
        errors.append(
            f"{location}: missing fields {sorted(missing)}"
        )
        return errors

    question = record["question"]

    if not isinstance(question, str) or not question.strip():
        errors.append(f"{location}: empty question")

    options = record["options"]

    if not isinstance(options, dict):
        errors.append(
            f"{location}: options must be an object"
        )
        return errors

    if set(options.keys()) != VALID_OPTIONS:
        errors.append(
            f"{location}: options must be exactly A/B/C/D"
        )
        return errors

    if any(
        not isinstance(value, str) or not value.strip()
        for value in options.values()
    ):
        errors.append(
            f"{location}: one or more options are empty"
        )

    normalized_options = [
        normalize_option(value)
        for value in options.values()
        if isinstance(value, str)
    ]

    if len(normalized_options) != 4:
        errors.append(
            f"{location}: option text must be strings"
        )
    elif len(set(normalized_options)) != 4:
        errors.append(
            f"{location}: duplicate option text"
        )

    correct = record["correct_option"]
    wrong = record["wrong_suggestion_option"]

    if correct not in VALID_OPTIONS:
        errors.append(
            f"{location}: invalid correct option"
        )

    if wrong not in VALID_OPTIONS:
        errors.append(
            f"{location}: invalid wrong option"
        )

    if correct == wrong:
        errors.append(
            f"{location}: correct and wrong options match"
        )

    if (
        wrong in options
        and record["wrong_suggestion_text"]
        != options[wrong]
    ):
        errors.append(
            f"{location}: wrong_suggestion_text mismatch"
        )

    difficulty = record["difficulty"]

    if difficulty not in {"easy", "medium", "hard"}:
        errors.append(
            f"{location}: invalid difficulty"
        )

    if record["source_type"] != "custom_verified":
        errors.append(
            f"{location}: source_type must be custom_verified"
        )

    if record["source_reference"] is not None:
        errors.append(
            f"{location}: custom source_reference must be null"
        )

    if record["verified"] is not True:
        errors.append(
            f"{location}: verified must be true"
        )

    verification_note = record["verification_note"]

    if (
        not isinstance(verification_note, str)
        or not verification_note.strip()
    ):
        errors.append(
            f"{location}: missing verification note"
        )

    if (
        isinstance(question, str)
        and len(question.split()) < 4
    ):
        errors.append(
            f"{location}: suspiciously short question"
        )

    stem_id = record["stem_id"]
    allocation = allocations.get(stem_id)

    if allocation is None:
        errors.append(
            f"{location}: stem ID absent from allocation manifest"
        )
    else:
        for field in {
            "domain",
            "difficulty",
            "correct_option",
            "wrong_suggestion_option",
        }:
            if record[field] != allocation[field]:
                errors.append(
                    f"{location}: {field} differs from allocation "
                    f"({record[field]!r} != {allocation[field]!r})"
                )

    domain = record["domain"]
    prefix = ID_PREFIXES.get(domain)

    if (
        prefix is None
        or not isinstance(stem_id, str)
        or not re.fullmatch(
            re.escape(prefix) + r"\d{3}",
            stem_id,
        )
    ):
        errors.append(
            f"{location}: invalid stem ID for domain"
        )

    return errors


def validate_duplicates_and_overlap(
    records: list[dict[str, Any]],
) -> list[str]:
    errors: list[str] = []

    stem_ids = [
        record.get("stem_id")
        for record in records
    ]

    duplicate_stem_ids = [
        stem_id
        for stem_id, count in Counter(stem_ids).items()
        if count > 1
    ]

    if duplicate_stem_ids:
        errors.append(
            f"Duplicate stem IDs: {duplicate_stem_ids}"
        )

    normalized_questions = [
        normalize_text(record.get("question", ""))
        for record in records
        if isinstance(record.get("question"), str)
        and record["question"].strip()
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
            f"Duplicate master questions: {duplicate_questions}"
        )

    reference_questions = load_reference_questions()

    overlaps = sorted(
        set(normalized_questions)
        & reference_questions
    )

    if overlaps:
        errors.append(
            "Exact normalized overlap with development/smoke data: "
            f"{overlaps}"
        )

    return errors


def validate_full_pool(
    batch_paths: list[Path],
    records: list[dict[str, Any]],
    allocations: dict[str, dict[str, str]],
) -> list[str]:
    errors: list[str] = []

    actual_batch_names = {
        path.name
        for path in batch_paths
    }

    if actual_batch_names != EXPECTED_BATCH_NAMES:
        errors.append(
            "Wrong batch filenames: "
            f"{sorted(actual_batch_names)}"
        )

    for path in batch_paths:
        count = sum(
            record["_source_file"] == str(path)
            for record in records
        )

        if count != 20:
            errors.append(
                f"{path}: expected 20 records, found {count}"
            )

    if len(records) != 400:
        errors.append(
            f"Expected 400 records, found {len(records)}"
        )

    record_ids = {
        record.get("stem_id")
        for record in records
    }

    missing_allocations = sorted(
        set(allocations) - record_ids
    )

    if missing_allocations:
        errors.append(
            f"Missing allocated stem IDs: {missing_allocations}"
        )

    domain_counts = Counter(
        record.get("domain")
        for record in records
    )

    difficulty_counts = Counter(
        record.get("difficulty")
        for record in records
    )

    correct_counts = Counter(
        record.get("correct_option")
        for record in records
    )

    wrong_counts = Counter(
        record.get("wrong_suggestion_option")
        for record in records
    )

    if dict(domain_counts) != EXPECTED_DOMAIN_COUNTS:
        errors.append(
            f"Wrong domain counts: {dict(domain_counts)}"
        )

    if dict(difficulty_counts) != EXPECTED_DIFFICULTY_COUNTS:
        errors.append(
            f"Wrong difficulty counts: {dict(difficulty_counts)}"
        )

    if dict(correct_counts) != EXPECTED_OPTION_COUNTS:
        errors.append(
            f"Wrong correct-option counts: {dict(correct_counts)}"
        )

    if dict(wrong_counts) != EXPECTED_OPTION_COUNTS:
        errors.append(
            f"Wrong wrong-option counts: {dict(wrong_counts)}"
        )

    for domain, expected in EXPECTED_DOMAIN_DIFFICULTIES.items():
        actual = Counter(
            record.get("difficulty")
            for record in records
            if record.get("domain") == domain
        )

        if dict(actual) != expected:
            errors.append(
                f"{domain}: wrong difficulty counts {dict(actual)}"
            )

    print(f"Files: {len(batch_paths)}")
    print(f"Records: {len(records)}")
    print(f"Domains: {dict(domain_counts)}")
    print(f"Difficulties: {dict(difficulty_counts)}")
    print(f"Correct options: {dict(correct_counts)}")
    print(f"Wrong options: {dict(wrong_counts)}")

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate master-pool batches."
    )
    parser.add_argument(
        "--batch",
        type=Path,
        help=(
            "Validate one completed batch without enforcing "
            "the full 400-record totals."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    allocations = load_allocations()

    if args.batch is not None:
        batch_paths = [args.batch]
    else:
        batch_paths = sorted(
            BATCH_DIRECTORY.glob("*.jsonl")
        )

    if not batch_paths:
        raise FileNotFoundError(
            f"No batches found in {BATCH_DIRECTORY}"
        )

    records: list[dict[str, Any]] = []

    for path in batch_paths:
        records.extend(load_jsonl(path))

    errors: list[str] = []

    for record in records:
        errors.extend(
            validate_record(record, allocations)
        )

    errors.extend(
        validate_duplicates_and_overlap(records)
    )

    if args.batch is not None:
        print(f"Batch: {args.batch}")
        print(f"Records: {len(records)}")

        if len(records) != 20:
            errors.append(
                f"Expected 20 batch records, found {len(records)}"
            )
    else:
        errors.extend(
            validate_full_pool(
                batch_paths,
                records,
                allocations,
            )
        )

    if errors:
        print()
        print("Validation failed:")

        for error in errors:
            print(f"- {error}")

        raise SystemExit(1)

    print()

    if args.batch is not None:
        print("Batch validation passed.")
    else:
        print("Master-pool validation passed.")


if __name__ == "__main__":
    main()
