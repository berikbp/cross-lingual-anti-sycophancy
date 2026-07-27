from __future__ import annotations

import json
import random
from collections import Counter
from pathlib import Path


OUTPUT_PATH = Path("data/master/allocation_manifest.json")

SEED = 20260727

DOMAINS = {
    "mathematics": "master_math",
    "science": "master_science",
    "computer_science": "master_cs",
    "geography": "master_geo",
    "logic": "master_logic",
}

DIFFICULTIES = (
    ["easy"] * 32
    + ["medium"] * 40
    + ["hard"] * 8
)

OPTION_LETTERS = ["A", "B", "C", "D"]

# Starting with seven copies of each of the 12 valid ordered pairs
# gives 84 pairs. Reducing one pair in every correct-letter row and
# every wrong-letter column produces 80 pairs with perfectly balanced
# marginals: 20 occurrences of each correct and wrong letter.
SIX_COUNT_PAIRS = {
    ("A", "B"),
    ("B", "A"),
    ("C", "D"),
    ("D", "C"),
}


def create_letter_pairs() -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []

    for correct in OPTION_LETTERS:
        for wrong in OPTION_LETTERS:
            if wrong == correct:
                continue

            pair_count = (
                6
                if (correct, wrong) in SIX_COUNT_PAIRS
                else 7
            )

            pairs.extend(
                [(correct, wrong)] * pair_count
            )

    if len(pairs) != 80:
        raise AssertionError(
            f"Expected 80 letter pairs, found {len(pairs)}"
        )

    return pairs


def main() -> None:
    rng = random.Random(SEED)

    allocations: list[dict[str, str]] = []

    for domain, prefix in DOMAINS.items():
        difficulties = DIFFICULTIES.copy()
        rng.shuffle(difficulties)

        pairs = create_letter_pairs()
        rng.shuffle(pairs)

        for index in range(80):
            correct_option, wrong_option = pairs[index]

            allocations.append(
                {
                    "stem_id": f"{prefix}_{index + 1:03d}",
                    "domain": domain,
                    "difficulty": difficulties[index],
                    "correct_option": correct_option,
                    "wrong_suggestion_option": wrong_option,
                }
            )

    correct_counts = Counter(
        record["correct_option"]
        for record in allocations
    )
    wrong_counts = Counter(
        record["wrong_suggestion_option"]
        for record in allocations
    )
    difficulty_counts = Counter(
        record["difficulty"]
        for record in allocations
    )
    domain_counts = Counter(
        record["domain"]
        for record in allocations
    )

    manifest = {
        "seed": SEED,
        "count": len(allocations),
        "domain_counts": dict(domain_counts),
        "difficulty_counts": dict(difficulty_counts),
        "correct_option_counts": dict(correct_counts),
        "wrong_option_counts": dict(wrong_counts),
        "allocations": allocations,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Created {len(allocations)} allocations")
    print(f"Domains: {dict(domain_counts)}")
    print(f"Difficulties: {dict(difficulty_counts)}")
    print(f"Correct options: {dict(correct_counts)}")
    print(f"Wrong options: {dict(wrong_counts)}")
    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
