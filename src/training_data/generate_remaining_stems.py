from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from cs_source_items import build_cs_items
from geography_source_items import build_geography_items
from logic_source_items import build_logic_items
from math_validation_items import build_math_validation_items
from science_source_items import build_science_items
from source_items import Item, assert_item_bank


MANIFEST_PATH = Path(
    "data/training/source/training_allocation_manifest.json"
)

BATCH_DIRECTORY = Path("data/training/batches")

LETTERS = ("A", "B", "C", "D")

TRAIN_BATCHES = {
    "science": range(5, 9),
    "computer_science": range(9, 13),
    "geography": range(13, 17),
    "logic": range(17, 21),
}


def make_record(
    allocation: dict[str, str],
    item: Item,
) -> dict[str, Any]:
    correct_letter = allocation["correct_option"]
    wrong_letter = allocation["wrong_suggestion_option"]

    options: dict[str, str] = {
        correct_letter: item.correct,
        wrong_letter: item.wrong,
    }

    remaining_letters = [
        letter
        for letter in LETTERS
        if letter not in options
    ]

    options[remaining_letters[0]] = item.distractor_1
    options[remaining_letters[1]] = item.distractor_2
    options = {
        letter: options[letter]
        for letter in LETTERS
    }

    return {
        "stem_id": allocation["stem_id"],
        "split": allocation["split"],
        "domain": allocation["domain"],
        "difficulty": allocation["difficulty"],
        "question": item.question,
        "options": options,
        "correct_option": correct_letter,
        "wrong_suggestion_option": wrong_letter,
        "wrong_suggestion_text": options[wrong_letter],
        "verified": True,
        "verification_note": item.verification_note,
        "notes": "",
    }


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


def prepare_banks() -> dict[str, dict[str, list[Item]]]:
    banks = {
        "mathematics": build_math_validation_items(),
        "science": build_science_items(),
        "computer_science": build_cs_items(),
        "geography": build_geography_items(),
        "logic": build_logic_items(),
    }

    assert_item_bank(
        banks["mathematics"],
        expected_easy=8,
        expected_medium=10,
        expected_hard=2,
    )

    for domain in (
        "science",
        "computer_science",
        "geography",
        "logic",
    ):
        assert_item_bank(
            banks[domain],
            expected_easy=88,
            expected_medium=110,
            expected_hard=22,
        )

    return banks


def main() -> None:
    manifest = json.loads(
        MANIFEST_PATH.read_text(encoding="utf-8")
    )
    allocations: list[dict[str, str]] = manifest["allocations"]
    banks = prepare_banks()
    positions: dict[tuple[str, str], int] = defaultdict(int)
    generated: dict[str, dict[str, Any]] = {}

    for allocation in allocations:
        domain = allocation["domain"]

        if (
            allocation["split"] == "train"
            and domain == "mathematics"
        ):
            continue

        key = (domain, allocation["difficulty"])
        index = positions[key]
        items = banks[domain][allocation["difficulty"]]

        if index >= len(items):
            raise ValueError(f"Item bank exhausted for {key}")

        generated[allocation["stem_id"]] = make_record(
            allocation,
            items[index],
        )
        positions[key] += 1

    for domain, batch_numbers in TRAIN_BATCHES.items():
        domain_allocations = [
            allocation
            for allocation in allocations
            if (
                allocation["split"] == "train"
                and allocation["domain"] == domain
            )
        ]

        for offset, batch_number in enumerate(batch_numbers):
            batch_allocations = domain_allocations[
                offset * 50 : (offset + 1) * 50
            ]
            records = [
                generated[allocation["stem_id"]]
                for allocation in batch_allocations
            ]
            path = (
                BATCH_DIRECTORY
                / f"train_{batch_number:02d}.jsonl"
            )
            write_jsonl(path, records)
            print(f"Wrote {len(records)} records to {path}")

    validation_allocations = [
        allocation
        for allocation in allocations
        if allocation["split"] == "validation"
    ]

    for offset in range(2):
        batch_allocations = validation_allocations[
            offset * 50 : (offset + 1) * 50
        ]
        records = [
            generated[allocation["stem_id"]]
            for allocation in batch_allocations
        ]
        path = (
            BATCH_DIRECTORY
            / f"validation_{offset + 1:02d}.jsonl"
        )
        write_jsonl(path, records)
        print(f"Wrote {len(records)} records to {path}")


if __name__ == "__main__":
    main()
