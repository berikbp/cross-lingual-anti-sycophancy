from __future__ import annotations

import json
from pathlib import Path
from typing import Any


BATCH_DIR = Path("data/training/batches")

TRAIN_OUTPUT = Path(
    "data/training/source/train_stems_en.jsonl"
)

VALIDATION_OUTPUT = Path(
    "data/training/source/validation_stems_en.jsonl"
)


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


def write_jsonl(
    path: Path,
    records: list[dict[str, Any]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )


def main() -> None:
    train_records: list[dict[str, Any]] = []

    for index in range(1, 21):
        path = BATCH_DIR / f"train_{index:02d}.jsonl"
        batch = load_jsonl(path)

        if len(batch) != 50:
            raise ValueError(
                f"{path} has {len(batch)} records, expected 50"
            )

        train_records.extend(batch)

    validation_records: list[dict[str, Any]] = []

    for index in range(1, 3):
        path = (
            BATCH_DIR
            / f"validation_{index:02d}.jsonl"
        )
        batch = load_jsonl(path)

        if len(batch) != 50:
            raise ValueError(
                f"{path} has {len(batch)} records, expected 50"
            )

        validation_records.extend(batch)

    if len(train_records) != 1000:
        raise ValueError(
            "Expected 1000 train records, "
            f"found {len(train_records)}"
        )

    if len(validation_records) != 100:
        raise ValueError(
            "Expected 100 validation records, "
            f"found {len(validation_records)}"
        )

    train_ids = {
        record["stem_id"]
        for record in train_records
    }
    validation_ids = {
        record["stem_id"]
        for record in validation_records
    }

    if len(train_ids) != 1000:
        raise ValueError("Duplicate training IDs detected.")

    if len(validation_ids) != 100:
        raise ValueError("Duplicate validation IDs detected.")

    if not train_ids.isdisjoint(validation_ids):
        raise ValueError(
            "Training and validation stem IDs overlap."
        )

    write_jsonl(TRAIN_OUTPUT, train_records)
    write_jsonl(VALIDATION_OUTPUT, validation_records)

    print(f"Train stems: {len(train_records)}")
    print(f"Validation stems: {len(validation_records)}")


if __name__ == "__main__":
    main()
