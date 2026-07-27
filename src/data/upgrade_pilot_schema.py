from __future__ import annotations

import json
from pathlib import Path
from typing import Any


INPUT_PATH = Path(
    "data/development/manual_pilot_questions.jsonl"
)

OUTPUT_PATH = Path(
    "data/development/dev_en.jsonl"
)


def infer_difficulty(record: dict[str, Any]) -> str:
    # The original pilot intentionally used simple qualification questions.
    return "easy"


def main() -> None:
    upgraded_records: list[dict[str, Any]] = []

    with INPUT_PATH.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Invalid JSON on line {line_number}: {error}"
                ) from error

            wrong_option = record["wrong_suggestion_option"]

            upgraded_records.append(
                {
                    "stem_id": record["stem_id"],
                    "domain": record["domain"],
                    "difficulty": infer_difficulty(record),
                    "source_type": "custom",
                    "source_reference": None,
                    "question": record["question"],
                    "options": record["options"],
                    "correct_option": record["correct_option"],
                    "wrong_suggestion_option": wrong_option,
                    "wrong_suggestion_text": (
                        record["options"][wrong_option]
                    ),
                    "verified": True,
                    "notes": "Reused from the 20-stem manual pilot.",
                }
            )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        for record in upgraded_records:
            file.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )

    print(
        f"Saved {len(upgraded_records)} records to {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()
