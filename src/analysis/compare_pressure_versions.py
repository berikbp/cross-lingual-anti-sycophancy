from __future__ import annotations

import json
from pathlib import Path
from typing import Any


V1_PATH = Path(
    "results/development/original_model_en.jsonl"
)

V2_PATH = Path(
    "results/development/original_model_en_v2_strong.jsonl"
)


def load_records(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def summarize(
    records: list[dict[str, Any]],
    label: str,
) -> None:
    b0 = [
        record
        for record in records
        if record["condition"] == "b0_matched_control"
    ]

    b2 = [
        record
        for record in records
        if record["condition"] == "b2_wrong_suggestion"
    ]

    initial_by_stem = {
        record["stem_id"]: record["initial_correct"]
        for record in records
    }

    initial_correct = sum(initial_by_stem.values())

    b0_accuracy = sum(
        record["final_correct"]
        for record in b0
    )

    b2_accuracy = sum(
        record["final_correct"]
        for record in b2
    )

    b0_harmful = sum(
        record["harmful_flip"]
        for record in b0
    )

    b2_harmful = sum(
        record["harmful_flip"]
        for record in b2
    )

    b2_exact = sum(
        record["flip_to_suggested_wrong"]
        for record in b2
    )

    parseable = sum(
        record["parseable"]
        for record in records
    )

    print(label)
    print("-" * 50)
    print(
        f"Initial accuracy: "
        f"{initial_correct}/{len(initial_by_stem)}"
    )
    print(f"B0 accuracy: {b0_accuracy}/{len(b0)}")
    print(f"B2 accuracy: {b2_accuracy}/{len(b2)}")
    print(
        "Pressure loss:",
        f"{100 * (b0_accuracy - b2_accuracy) / len(b0):.1f} pp",
    )
    print(f"B0 harmful flips: {b0_harmful}")
    print(f"B2 harmful flips: {b2_harmful}")
    print(f"B2 exact wrong adoptions: {b2_exact}")
    print(
        "Conditional harmful-flip rates:",
        f"B0={100 * b0_harmful / initial_correct:.2f}%,",
        f"B2={100 * b2_harmful / initial_correct:.2f}%",
    )
    print(
        f"Parseability: {parseable}/{len(records)}"
    )
    print()


def main() -> None:
    summarize(load_records(V1_PATH), "v1 weak pressure")
    summarize(load_records(V2_PATH), "v2 strong pressure")


if __name__ == "__main__":
    main()
