from __future__ import annotations

import hashlib
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


TRAIN_SOURCE = Path("data/training/source/train_stems_en.jsonl")
VALIDATION_SOURCE = Path(
    "data/training/source/validation_stems_en.jsonl"
)
OUTPUT_PATH = Path(
    "data/training_v2/source/transition_manifest.json"
)
SEED = 20260802
CATEGORIES = ("CW", "WC", "CC", "WW")
LETTERS = ("A", "B", "C", "D")
EXPECTED_DOMAINS = {
    "mathematics",
    "science",
    "computer_science",
    "geography",
    "logic",
}


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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def select_alternative_wrong(record: dict[str, Any]) -> str:
    correct = record["correct_option"]
    primary_wrong = record["wrong_suggestion_option"]
    candidates = [
        letter
        for letter in LETTERS
        if letter not in {correct, primary_wrong}
    ]
    if len(candidates) != 2:
        raise ValueError(
            f"{record['stem_id']}: invalid correct/wrong allocation"
        )
    digest = hashlib.sha256(record["stem_id"].encode("utf-8")).digest()
    return candidates[digest[0] % len(candidates)]


def build_split(
    records: list[dict[str, Any]],
    split: str,
    per_category_per_domain: int,
    rng: random.Random,
) -> list[dict[str, Any]]:
    by_domain: dict[str, list[dict[str, Any]]] = defaultdict(list)
    source_ids: set[str] = set()
    for record in records:
        if record["stem_id"] in source_ids:
            raise ValueError(f"Duplicate stem ID: {record['stem_id']}")
        source_ids.add(record["stem_id"])
        if record["split"] != split:
            raise ValueError(
                f"{record['stem_id']}: expected split {split}"
            )
        by_domain[record["domain"]].append(record)

    if set(by_domain) != EXPECTED_DOMAINS:
        raise ValueError(f"Unexpected domains: {sorted(by_domain)}")

    allocations: list[dict[str, Any]] = []
    for domain in sorted(by_domain):
        domain_records = sorted(
            by_domain[domain], key=lambda item: item["stem_id"]
        )
        expected = per_category_per_domain * len(CATEGORIES)
        if len(domain_records) != expected:
            raise ValueError(
                f"{split}/{domain}: expected {expected}, "
                f"found {len(domain_records)}"
            )

        category_sequence = [
            category
            for category in CATEGORIES
            for _ in range(per_category_per_domain)
        ]
        rng.shuffle(category_sequence)

        for record, category in zip(
            domain_records, category_sequence, strict=True
        ):
            correct = record["correct_option"]
            primary_wrong = record["wrong_suggestion_option"]
            if correct not in LETTERS or primary_wrong not in LETTERS:
                raise ValueError(f"{record['stem_id']}: invalid option")
            if correct == primary_wrong:
                raise ValueError(
                    f"{record['stem_id']}: wrong option is correct"
                )
            alternate_wrong = select_alternative_wrong(record)
            if category == "CW":
                initial_option, feedback_option = correct, primary_wrong
            elif category == "WC":
                initial_option, feedback_option = primary_wrong, correct
            elif category == "CC":
                initial_option, feedback_option = correct, correct
            elif category == "WW":
                initial_option = primary_wrong
                feedback_option = alternate_wrong
            else:  # pragma: no cover
                raise ValueError(f"Unknown category: {category}")

            allocations.append(
                {
                    "stem_id": record["stem_id"],
                    "split": split,
                    "domain": domain,
                    "transition_category": category,
                    "correct_option": correct,
                    "initial_answer_option": initial_option,
                    "feedback_option": feedback_option,
                    "primary_wrong_option": primary_wrong,
                    "alternate_wrong_option": alternate_wrong,
                }
            )

    source_order = {
        record["stem_id"]: index for index, record in enumerate(records)
    }
    allocations.sort(key=lambda item: source_order[item["stem_id"]])
    return allocations


def print_distribution(label: str, records: list[dict[str, Any]]) -> None:
    print(f"\n{label}\n{'=' * 60}")
    print("Records:", len(records))
    print(
        "Categories:",
        dict(Counter(r["transition_category"] for r in records)),
    )
    print(
        "Initial answers:",
        dict(Counter(r["initial_answer_option"] for r in records)),
    )
    print(
        "Feedback answers:",
        dict(Counter(r["feedback_option"] for r in records)),
    )
    domain_categories = Counter(
        (r["domain"], r["transition_category"]) for r in records
    )
    print("Domain/category counts:")
    for key in sorted(domain_categories):
        print(f"  {key}: {domain_categories[key]}")


def main() -> None:
    train = load_jsonl(TRAIN_SOURCE)
    validation = load_jsonl(VALIDATION_SOURCE)
    if len(train) != 1000 or len(validation) != 100:
        raise ValueError(
            f"Unexpected source counts: train={len(train)}, "
            f"validation={len(validation)}"
        )
    if {r["stem_id"] for r in train} & {
        r["stem_id"] for r in validation
    }:
        raise ValueError("Train and validation stem IDs overlap")

    rng = random.Random(SEED)
    train_allocations = build_split(train, "train", 50, rng)
    validation_allocations = build_split(
        validation, "validation", 5, rng
    )
    manifest = {
        "version": "selective_correction_v2",
        "seed": SEED,
        "train_source_path": str(TRAIN_SOURCE),
        "train_source_sha256": sha256_file(TRAIN_SOURCE),
        "validation_source_path": str(VALIDATION_SOURCE),
        "validation_source_sha256": sha256_file(VALIDATION_SOURCE),
        "train_count": len(train_allocations),
        "validation_count": len(validation_allocations),
        "allocations": train_allocations + validation_allocations,
    }
    OUTPUT_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print_distribution("Train", train_allocations)
    print_distribution("Validation", validation_allocations)
    print(f"\nManifest: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
