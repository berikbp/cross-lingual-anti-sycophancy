from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pytest
from transformers import AutoTokenizer

sys.path.insert(
    0,
    str(
        Path(__file__).resolve().parents[2]
        / "src"
        / "training_data"
    ),
)

from tokenize_final_completion import (  # noqa: E402
    tokenize_final_assistant_only,
)


MODEL_NAME = "Qwen/Qwen3-4B-Instruct-2507"

CONTROL_PATH = Path(
    "data/training/control/train.jsonl"
)
ANTI_PATH = Path(
    "data/training/anti_sycophancy/train.jsonl"
)


@pytest.fixture(scope="session")
def tokenizer() -> Any:
    return AutoTokenizer.from_pretrained(
        MODEL_NAME,
        use_fast=True,
        local_files_only=True,
    )


def load_first(path: Path) -> dict[str, Any]:
    first_line = next(
        line
        for line in path.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    )
    return json.loads(first_line)


def supervised_text(
    tokenizer: Any,
    encoded: dict[str, list[int]],
) -> str:
    supervised_ids = [
        token_id
        for token_id, label in zip(
            encoded["input_ids"],
            encoded["labels"],
            strict=True,
        )
        if label != -100
    ]

    return tokenizer.decode(
        supervised_ids,
        skip_special_tokens=True,
    ).strip()


@pytest.mark.parametrize(
    "path",
    [CONTROL_PATH, ANTI_PATH],
)
def test_only_final_assistant_is_supervised(
    tokenizer: Any,
    path: Path,
) -> None:
    example = load_first(path)
    encoded = tokenize_final_assistant_only(
        tokenizer=tokenizer,
        messages=example["messages"],
        max_length=512,
    )
    labels = encoded["labels"]
    first_supervised = next(
        index
        for index, label in enumerate(labels)
        if label != -100
    )

    assert first_supervised > 0
    assert all(
        label == -100
        for label in labels[:first_supervised]
    )
    assert all(
        label != -100
        for label in labels[first_supervised:]
    )

    decoded = supervised_text(tokenizer, encoded)
    target = json.loads(example["messages"][-1]["content"])

    assert target == {
        "answer": example["correct_option"]
    }
    assert json.dumps(target) in decoded


def test_initial_assistant_answer_is_masked(
    tokenizer: Any,
) -> None:
    example = load_first(ANTI_PATH)
    messages = example["messages"]
    encoded = tokenize_final_assistant_only(
        tokenizer=tokenizer,
        messages=messages,
        max_length=512,
    )
    prefix_text = tokenizer.apply_chat_template(
        messages[:-1],
        tokenize=False,
        add_generation_prompt=True,
    )
    prefix_length = len(
        tokenizer(
            prefix_text,
            add_special_tokens=False,
        )["input_ids"]
    )

    assert all(
        label == -100
        for label in encoded["labels"][:prefix_length]
    )


def test_wrong_suggestion_is_never_supervised(
    tokenizer: Any,
) -> None:
    example = load_first(ANTI_PATH)
    encoded = tokenize_final_assistant_only(
        tokenizer=tokenizer,
        messages=example["messages"],
        max_length=512,
    )
    decoded = supervised_text(tokenizer, encoded)
    parsed_target = json.loads(
        example["messages"][-1]["content"]
    )

    assert parsed_target["answer"] != (
        example["wrong_suggestion_option"]
    )
    assert example["wrong_suggestion_text"] not in decoded


def test_control_and_anti_supervise_same_target(
    tokenizer: Any,
) -> None:
    control = load_first(CONTROL_PATH)
    anti = load_first(ANTI_PATH)
    control_encoded = tokenize_final_assistant_only(
        tokenizer,
        control["messages"],
        max_length=512,
    )
    anti_encoded = tokenize_final_assistant_only(
        tokenizer,
        anti["messages"],
        max_length=512,
    )

    assert supervised_text(
        tokenizer,
        control_encoded,
    ) == supervised_text(
        tokenizer,
        anti_encoded,
    )


def test_truncation_preserves_final_target(
    tokenizer: Any,
) -> None:
    example = load_first(ANTI_PATH)
    encoded = tokenize_final_assistant_only(
        tokenizer=tokenizer,
        messages=example["messages"],
        max_length=32,
    )
    decoded = supervised_text(tokenizer, encoded)

    assert len(encoded["input_ids"]) == 32
    assert json.dumps(
        {
            "answer": example["correct_option"],
        }
    ) in decoded


def test_final_message_must_be_assistant(
    tokenizer: Any,
) -> None:
    with pytest.raises(
        ValueError,
        match="Final message",
    ):
        tokenize_final_assistant_only(
            tokenizer=tokenizer,
            messages=[
                {
                    "role": "user",
                    "content": "Question",
                },
                {
                    "role": "user",
                    "content": "Follow-up",
                },
            ],
            max_length=32,
        )
