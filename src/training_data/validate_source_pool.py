from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


TRAIN_PATH = Path(
    "data/training/source/train_stems_en.jsonl"
)
VALIDATION_PATH = Path(
    "data/training/source/validation_stems_en.jsonl"
)
MANIFEST_PATH = Path(
    "data/training/source/training_allocation_manifest.json"
)
EXCLUSION_PATH = Path(
    "reports/training_data_audits/excluded_training_questions.txt"
)

LETTERS = {"A", "B", "C", "D"}

EXPECTED_TRAIN_DOMAINS = {
    "mathematics": 200,
    "science": 200,
    "computer_science": 200,
    "geography": 200,
    "logic": 200,
}
EXPECTED_VALIDATION_DOMAINS = {
    domain: 20
    for domain in EXPECTED_TRAIN_DOMAINS
}


def normalize(text: str) -> str:
    text = re.sub(r"\s+", " ", text.lower().strip())
    return re.sub(r"[^\w\s]", "", text)


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


def load_exclusions() -> set[str]:
    questions: set[str] = set()

    for line in EXCLUSION_PATH.read_text(
        encoding="utf-8"
    ).splitlines():
        parts = line.split("\t", maxsplit=2)

        if len(parts) == 3:
            questions.add(normalize(parts[2]))

    return questions


def validate_distribution(
    records: list[dict[str, Any]],
    *,
    split: str,
) -> None:
    if split == "train":
        expected_count = 1000
        expected_domains = EXPECTED_TRAIN_DOMAINS
        expected_difficulties = {
            "easy": 400,
            "medium": 500,
            "hard": 100,
        }
        expected_options = {
            letter: 250
            for letter in LETTERS
        }
    else:
        expected_count = 100
        expected_domains = EXPECTED_VALIDATION_DOMAINS
        expected_difficulties = {
            "easy": 40,
            "medium": 50,
            "hard": 10,
        }
        expected_options = {
            letter: 25
            for letter in LETTERS
        }

    if len(records) != expected_count:
        raise ValueError(
            f"{split}: expected {expected_count}, "
            f"found {len(records)}"
        )

    domains = Counter(
        record["domain"]
        for record in records
    )
    difficulties = Counter(
        record["difficulty"]
        for record in records
    )
    correct = Counter(
        record["correct_option"]
        for record in records
    )
    wrong = Counter(
        record["wrong_suggestion_option"]
        for record in records
    )

    if dict(domains) != expected_domains:
        raise ValueError(
            f"{split}: wrong domain counts {dict(domains)}"
        )

    if dict(difficulties) != expected_difficulties:
        raise ValueError(
            f"{split}: wrong difficulty counts "
            f"{dict(difficulties)}"
        )

    if dict(correct) != expected_options:
        raise ValueError(
            f"{split}: wrong correct options {dict(correct)}"
        )

    if dict(wrong) != expected_options:
        raise ValueError(
            f"{split}: wrong wrong options {dict(wrong)}"
        )

    print()
    print(split.title())
    print("=" * 60)
    print("Records:", len(records))
    print("Domains:", dict(domains))
    print("Difficulties:", dict(difficulties))
    print("Correct options:", dict(correct))
    print("Wrong suggestions:", dict(wrong))


def main() -> None:
    train = load_jsonl(TRAIN_PATH)
    validation = load_jsonl(VALIDATION_PATH)
    records = train + validation

    manifest = json.loads(
        MANIFEST_PATH.read_text(encoding="utf-8")
    )
    allocations = manifest["allocations"]

    if len(records) != len(allocations):
        raise ValueError(
            "Merged source count does not match allocation count"
        )

    for record, allocation in zip(
        records,
        allocations,
        strict=True,
    ):
        for field in (
            "stem_id",
            "split",
            "domain",
            "difficulty",
            "correct_option",
            "wrong_suggestion_option",
        ):
            if record[field] != allocation[field]:
                raise ValueError(
                    f"{record['stem_id']}: allocation mismatch "
                    f"for {field}"
                )

        options = record["options"]

        if set(options) != LETTERS:
            raise ValueError(
                f"{record['stem_id']}: invalid option letters"
            )

        if len(set(options.values())) != 4:
            raise ValueError(
                f"{record['stem_id']}: duplicate options"
            )

        if (
            record["correct_option"]
            == record["wrong_suggestion_option"]
        ):
            raise ValueError(
                f"{record['stem_id']}: correct equals wrong"
            )

        if (
            record["wrong_suggestion_text"]
            != options[record["wrong_suggestion_option"]]
        ):
            raise ValueError(
                f"{record['stem_id']}: wrong text mismatch"
            )

        if record["verified"] is not True:
            raise ValueError(
                f"{record['stem_id']}: not verified"
            )

        if not record["verification_note"].strip():
            raise ValueError(
                f"{record['stem_id']}: no verification note"
            )

    ids = [record["stem_id"] for record in records]

    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate source stem IDs")

    normalized_questions = [
        normalize(record["question"])
        for record in records
    ]

    duplicates = [
        question
        for question, count in Counter(
            normalized_questions
        ).items()
        if count > 1
    ]

    if duplicates:
        raise ValueError(
            f"Duplicate source questions: {duplicates}"
        )

    overlaps = sorted(
        set(normalized_questions)
        & load_exclusions()
    )

    if overlaps:
        raise ValueError(
            f"Evaluation overlaps: {overlaps}"
        )

    validate_distribution(train, split="train")
    validate_distribution(validation, split="validation")

    print()
    print("Source-pool validation passed.")


if __name__ == "__main__":
    main()
