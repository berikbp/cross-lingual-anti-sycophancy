from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pytest
from transformers import AutoTokenizer

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.training_data.tokenize_final_completion import (
    tokenize_final_assistant_only,
)


MODEL_NAME = "Qwen/Qwen3-4B-Instruct-2507"
PATHS = {
    "control_v2": Path("data/training_v2/control/train.jsonl"),
    "selective_correction_v2": Path(
        "data/training_v2/selective_correction/train.jsonl"
    ),
}
CATEGORIES = ("CW", "WC", "CC", "WW")


@pytest.fixture(scope="session")
def v2_tokenizer() -> Any:
    return AutoTokenizer.from_pretrained(
        MODEL_NAME, use_fast=True, local_files_only=True
    )


def load_by_category(path: Path) -> dict[str, dict[str, Any]]:
    selected: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        selected.setdefault(record["transition_category"], record)
    assert set(selected) == set(CATEGORIES)
    return selected


def supervised_text(
    tokenizer: Any, encoded: dict[str, list[int]]
) -> str:
    token_ids = [
        token_id
        for token_id, label in zip(
            encoded["input_ids"], encoded["labels"], strict=True
        )
        if label != -100
    ]
    return tokenizer.decode(token_ids, skip_special_tokens=True).strip()


@pytest.mark.parametrize("condition", tuple(PATHS))
@pytest.mark.parametrize("category", CATEGORIES)
def test_v2_only_final_correct_answer_is_supervised(
    v2_tokenizer: Any, condition: str, category: str
) -> None:
    record = load_by_category(PATHS[condition])[category]
    encoded = tokenize_final_assistant_only(
        v2_tokenizer, record["messages"], max_length=256
    )
    labels = encoded["labels"]
    first_supervised = next(
        index for index, label in enumerate(labels) if label != -100
    )
    assert first_supervised > 0
    assert all(label == -100 for label in labels[:first_supervised])
    assert all(label != -100 for label in labels[first_supervised:])

    target = json.loads(record["messages"][-1]["content"])
    decoded_target = json.loads(supervised_text(v2_tokenizer, encoded))
    assert target == {"answer": record["correct_option"]}
    assert decoded_target == target

    if not record["initial_answer_correct"]:
        assert target["answer"] != record["initial_answer_option"]
    if not record["feedback_correct"]:
        assert target["answer"] != record["feedback_option"]


@pytest.mark.parametrize("condition", tuple(PATHS))
@pytest.mark.parametrize("category", CATEGORIES)
def test_v2_truncation_retains_complete_final_target(
    v2_tokenizer: Any, condition: str, category: str
) -> None:
    record = load_by_category(PATHS[condition])[category]
    encoded = tokenize_final_assistant_only(
        v2_tokenizer, record["messages"], max_length=32
    )
    assert len(encoded["input_ids"]) == 32
    decoded_target = json.loads(supervised_text(v2_tokenizer, encoded))
    assert decoded_target == {"answer": record["correct_option"]}
