from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SOURCE_PATH = Path("data/final/test_en.jsonl")
OUTPUT_ROOT = Path("data/translation/batches")
BATCH_SIZE = 25
LANGUAGES = ("ru", "kk")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"{path}:{line_number}: {error}"
                ) from error
    return records


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")


def make_template(
    record: dict[str, Any], language: str
) -> dict[str, Any]:
    return {
        "stem_id": record["stem_id"],
        "source_stem_id": record["stem_id"],
        "language": language,
        "domain": record["domain"],
        "difficulty": record["difficulty"],
        "question": "",
        "options": {"A": "", "B": "", "C": "", "D": ""},
        "correct_option": record["correct_option"],
        "wrong_suggestion_option": record["wrong_suggestion_option"],
        "wrong_suggestion_text": "",
        "source_question": record["question"],
        "source_options": record["options"],
        "translation_status": "draft",
        "translator_note": "",
        "semantic_review": False,
        "structural_review": False,
        "review_note": "",
    }


def main() -> None:
    records = load_jsonl(SOURCE_PATH)
    if len(records) != 300:
        raise ValueError(
            f"Expected 300 English records, found {len(records)}"
        )
    if len({record["stem_id"] for record in records}) != 300:
        raise ValueError("English source contains duplicate stem IDs")

    for language in LANGUAGES:
        translated = [make_template(record, language) for record in records]
        for start in range(0, len(translated), BATCH_SIZE):
            batch_number = start // BATCH_SIZE + 1
            path = (
                OUTPUT_ROOT
                / language
                / f"translation_{language}_{batch_number:02d}.jsonl"
            )
            write_jsonl(path, translated[start : start + BATCH_SIZE])

    print("Created 12 Russian and 12 Kazakh batches.")


if __name__ == "__main__":
    main()
