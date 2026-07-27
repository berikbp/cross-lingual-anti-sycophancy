from __future__ import annotations

import json
import statistics
from pathlib import Path
from typing import Any

from transformers import AutoTokenizer


MODEL_NAME = "Qwen/Qwen3-4B-Instruct-2507"

PATHS = {
    "control_train": Path(
        "data/training/control/train.jsonl"
    ),
    "anti_train": Path(
        "data/training/anti_sycophancy/train.jsonl"
    ),
    "control_validation": Path(
        "data/training/control/validation.jsonl"
    ),
    "anti_validation": Path(
        "data/training/anti_sycophancy/validation.jsonl"
    ),
}

OUTPUT_PATH = Path(
    "reports/training_data_audits/"
    "conversation_length_stats.json"
)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]


def main() -> None:
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME,
        use_fast=True,
        local_files_only=True,
    )
    stats: dict[str, dict[str, float | int]] = {}

    for label, path in PATHS.items():
        lengths: list[int] = []

        for record in load_jsonl(path):
            text = tokenizer.apply_chat_template(
                record["messages"],
                tokenize=False,
                add_generation_prompt=False,
            )
            token_ids = tokenizer(
                text,
                add_special_tokens=False,
            )["input_ids"]
            lengths.append(len(token_ids))

        stats[label] = {
            "count": len(lengths),
            "mean_tokens": round(
                statistics.fmean(lengths),
                3,
            ),
            "median_tokens": round(
                statistics.median(lengths),
                3,
            ),
            "max_tokens": max(lengths),
            "min_tokens": min(lengths),
        }

    stats["train_condition_difference"] = {
        "mean_anti_minus_control": round(
            float(stats["anti_train"]["mean_tokens"])
            - float(
                stats["control_train"]["mean_tokens"]
            ),
            3,
        ),
        "max_anti_minus_control": (
            int(stats["anti_train"]["max_tokens"])
            - int(stats["control_train"]["max_tokens"])
        ),
    }

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    OUTPUT_PATH.write_text(
        json.dumps(stats, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
