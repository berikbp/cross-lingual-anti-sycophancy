from __future__ import annotations

import json
from pathlib import Path
from typing import Any


INPUT_PATHS = [
    Path("data/development/dev_en.jsonl"),
    Path("data/development/manual_pilot_questions.jsonl"),
    Path("data/smoke_test/train.jsonl"),
    Path("data/master/master_en.jsonl"),
    Path("data/final/test_en.jsonl"),
    Path("data/final/reserve_en.jsonl"),
]

OUTPUT_PATH = Path(
    "reports/training_data_audits/excluded_training_questions.txt"
)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    if not path.exists():
        return records

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                records.append(json.loads(line))

    return records


def main() -> None:
    lines: list[str] = []

    for path in INPUT_PATHS:
        for record in load_jsonl(path):
            question = record.get("question")

            if question:
                lines.append(
                    f"{path}\t{record.get('stem_id', '')}\t{question}"
                )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT_PATH.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote {len(lines)} excluded questions")
    print(f"Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
