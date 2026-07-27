from __future__ import annotations

import json
import random
from collections import Counter
from pathlib import Path


OUTPUT_PATH = Path(
    "data/training/source/training_allocation_manifest.json"
)

SEED = 20260801

DOMAINS = {
    "mathematics": "math",
    "science": "science",
    "computer_science": "cs",
    "geography": "geo",
    "logic": "logic",
}

TRAIN_PER_DOMAIN = 200
VALIDATION_PER_DOMAIN = 20

TRAIN_DIFFICULTIES_PER_DOMAIN = (
    ["easy"] * 80
    + ["medium"] * 100
    + ["hard"] * 20
)

VALIDATION_DIFFICULTIES_PER_DOMAIN = (
    ["easy"] * 8
    + ["medium"] * 10
    + ["hard"] * 2
)

LETTERS = ["A", "B", "C", "D"]


def make_pairs(count: int) -> list[tuple[str, str]]:
    if count % 4 != 0:
        raise ValueError("Count must be divisible by four.")

    valid_pairs = [
        (correct, wrong)
        for correct in LETTERS
        for wrong in LETTERS
        if wrong != correct
    ]

    complete_rounds, remainder = divmod(count, len(valid_pairs))
    pairs = valid_pairs * complete_rounds

    # A count divisible by four leaves 0, 4, or 8 pairs after
    # complete 12-pair rounds. Each added derangement round uses
    # every correct and wrong letter exactly once.
    for offset in range(1, remainder // len(LETTERS) + 1):
        pairs.extend(
            (
                correct,
                LETTERS[(index + offset) % len(LETTERS)],
            )
            for index, correct in enumerate(LETTERS)
        )

    if len(pairs) != count:
        raise AssertionError("Pair allocation has the wrong size.")

    correct_counts = Counter(correct for correct, _ in pairs)
    wrong_counts = Counter(wrong for _, wrong in pairs)
    expected = Counter({letter: count // 4 for letter in LETTERS})

    if correct_counts != expected or wrong_counts != expected:
        raise AssertionError("Option marginals are not balanced.")

    return pairs


def create_split_allocations(
    split: str,
    per_domain: int,
    difficulties_per_domain: list[str],
    rng: random.Random,
) -> list[dict[str, str]]:
    allocations: list[dict[str, str]] = []
    id_split = "val" if split == "validation" else split

    for domain, prefix in DOMAINS.items():
        difficulties = difficulties_per_domain.copy()
        pairs = make_pairs(per_domain)

        rng.shuffle(difficulties)
        rng.shuffle(pairs)

        for index in range(per_domain):
            correct, wrong = pairs[index]

            allocations.append(
                {
                    "stem_id": (
                        f"{id_split}_{prefix}_{index + 1:04d}"
                    ),
                    "split": split,
                    "domain": domain,
                    "difficulty": difficulties[index],
                    "correct_option": correct,
                    "wrong_suggestion_option": wrong,
                }
            )

    return allocations


def main() -> None:
    rng = random.Random(SEED)

    train = create_split_allocations(
        split="train",
        per_domain=TRAIN_PER_DOMAIN,
        difficulties_per_domain=TRAIN_DIFFICULTIES_PER_DOMAIN,
        rng=rng,
    )

    validation = create_split_allocations(
        split="validation",
        per_domain=VALIDATION_PER_DOMAIN,
        difficulties_per_domain=(
            VALIDATION_DIFFICULTIES_PER_DOMAIN
        ),
        rng=rng,
    )

    all_records = train + validation

    manifest = {
        "seed": SEED,
        "train_count": len(train),
        "validation_count": len(validation),
        "allocations": all_records,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT_PATH.write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    print("Train:", len(train))
    print("Validation:", len(validation))
    print(
        "Train domains:",
        dict(Counter(record["domain"] for record in train)),
    )
    print(
        "Train difficulties:",
        dict(Counter(record["difficulty"] for record in train)),
    )
    print(
        "Train correct options:",
        dict(Counter(record["correct_option"] for record in train)),
    )
    print(
        "Train wrong options:",
        dict(
            Counter(
                record["wrong_suggestion_option"]
                for record in train
            )
        ),
    )
    print(
        "Validation correct options:",
        dict(
            Counter(
                record["correct_option"]
                for record in validation
            )
        ),
    )
    print(
        "Validation wrong options:",
        dict(
            Counter(
                record["wrong_suggestion_option"]
                for record in validation
            )
        ),
    )


if __name__ == "__main__":
    main()
