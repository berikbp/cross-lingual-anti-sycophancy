from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path
from typing import Any


MASTER_PATH = Path("data/master/master_en.jsonl")
TEST_PATH = Path("data/final/test_en.jsonl")
RESERVE_PATH = Path("data/final/reserve_en.jsonl")
MANIFEST_PATH = Path("data/final/split_manifest.json")

SEED = 20260727
TEST_SIZE = 300
RESERVE_SIZE = 100


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
                    f"Invalid JSON on line {line_number}: {error}"
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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def main() -> None:
    records = load_jsonl(MASTER_PATH)

    expected_size = TEST_SIZE + RESERVE_SIZE

    if len(records) != expected_size:
        raise ValueError(
            f"Expected {expected_size} records, found {len(records)}"
        )

    stem_ids = [record["stem_id"] for record in records]

    if len(stem_ids) != len(set(stem_ids)):
        raise ValueError("Duplicate stem IDs detected.")

    random_generator = random.Random(SEED)
    shuffled = records.copy()
    random_generator.shuffle(shuffled)

    test_records = shuffled[:TEST_SIZE]
    reserve_records = shuffled[
        TEST_SIZE : TEST_SIZE + RESERVE_SIZE
    ]

    write_jsonl(TEST_PATH, test_records)
    write_jsonl(RESERVE_PATH, reserve_records)

    manifest = {
        "seed": SEED,
        "master_count": len(records),
        "test_count": len(test_records),
        "reserve_count": len(reserve_records),
        "master_sha256": sha256_file(MASTER_PATH),
        "test_sha256": sha256_file(TEST_PATH),
        "reserve_sha256": sha256_file(RESERVE_PATH),
        "test_stem_ids": [
            record["stem_id"]
            for record in test_records
        ],
        "reserve_stem_ids": [
            record["stem_id"]
            for record in reserve_records
        ],
    }

    MANIFEST_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    MANIFEST_PATH.write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Master: {len(records)}")
    print(f"Test: {len(test_records)}")
    print(f"Reserve: {len(reserve_records)}")
    print(f"Manifest: {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
