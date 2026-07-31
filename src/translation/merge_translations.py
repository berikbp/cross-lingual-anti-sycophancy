from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SOURCE_PATH = Path("data/final/test_en.jsonl")
BATCH_ROOT = Path("data/translation/batches")
OUTPUTS = {
    "ru": Path("data/final/test_ru.jsonl"),
    "kk": Path("data/final/test_kk.jsonl"),
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    source = load_jsonl(SOURCE_PATH)
    source_order = [record["stem_id"] for record in source]
    if len(source_order) != 300 or len(set(source_order)) != 300:
        raise ValueError("English source must contain 300 unique stems")

    for language, output_path in OUTPUTS.items():
        records: list[dict[str, Any]] = []
        for batch_number in range(1, 13):
            batch_path = (
                BATCH_ROOT
                / language
                / f"translation_{language}_{batch_number:02d}.jsonl"
            )
            batch = load_jsonl(batch_path)
            if len(batch) != 25:
                raise ValueError(
                    f"{batch_path}: expected 25 records, found {len(batch)}"
                )
            records.extend(batch)

        by_id = {record["stem_id"]: record for record in records}
        if len(records) != 300 or len(by_id) != 300:
            raise ValueError(f"{language}: expected 300 unique records")
        if set(by_id) != set(source_order):
            raise ValueError(f"{language}: source stem set mismatch")
        ordered = [by_id[stem_id] for stem_id in source_order]
        write_jsonl(output_path, ordered)
        print(f"{language}: wrote {len(ordered)} records to {output_path}")


if __name__ == "__main__":
    main()
