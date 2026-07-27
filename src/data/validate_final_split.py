from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


MASTER_PATH = Path("data/master/master_en.jsonl")
TEST_PATH = Path("data/final/test_en.jsonl")
RESERVE_PATH = Path("data/final/reserve_en.jsonl")
MANIFEST_PATH = Path("data/final/split_manifest.json")


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
                    f"{path}:{line_number}: invalid JSON: {error}"
                ) from error

    return records


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def describe(
    label: str,
    records: list[dict[str, Any]],
) -> None:
    print()
    print(label)
    print("=" * 60)
    print("Records:", len(records))
    print(
        "Domains:",
        dict(Counter(record["domain"] for record in records)),
    )
    print(
        "Difficulties:",
        dict(Counter(record["difficulty"] for record in records)),
    )
    print(
        "Correct options:",
        dict(Counter(record["correct_option"] for record in records)),
    )
    print(
        "Wrong suggestions:",
        dict(
            Counter(
                record["wrong_suggestion_option"]
                for record in records
            )
        ),
    )


def main() -> None:
    master = load_jsonl(MASTER_PATH)
    test = load_jsonl(TEST_PATH)
    reserve = load_jsonl(RESERVE_PATH)

    manifest = json.loads(
        MANIFEST_PATH.read_text(encoding="utf-8")
    )

    assert len(master) == 400
    assert len(test) == 300
    assert len(reserve) == 100

    master_ids = {record["stem_id"] for record in master}
    test_ids = {record["stem_id"] for record in test}
    reserve_ids = {record["stem_id"] for record in reserve}

    assert len(master_ids) == 400
    assert len(test_ids) == 300
    assert len(reserve_ids) == 100

    assert test_ids.isdisjoint(reserve_ids)
    assert test_ids | reserve_ids == master_ids

    assert manifest["master_count"] == 400
    assert manifest["test_count"] == 300
    assert manifest["reserve_count"] == 100

    assert manifest["master_sha256"] == sha256_file(MASTER_PATH)
    assert manifest["test_sha256"] == sha256_file(TEST_PATH)
    assert manifest["reserve_sha256"] == sha256_file(RESERVE_PATH)

    assert manifest["test_stem_ids"] == [
        record["stem_id"] for record in test
    ]

    assert manifest["reserve_stem_ids"] == [
        record["stem_id"] for record in reserve
    ]

    describe("Master", master)
    describe("Final test", test)
    describe("Reserve", reserve)

    print()
    print("Final-split validation passed.")


if __name__ == "__main__":
    main()
