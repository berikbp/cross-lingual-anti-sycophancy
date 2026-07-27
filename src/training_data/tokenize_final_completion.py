from __future__ import annotations

from typing import Any


def tokenize_final_assistant_only(
    tokenizer: Any,
    messages: list[dict[str, str]],
    max_length: int,
) -> dict[str, list[int]]:
    if len(messages) < 2:
        raise ValueError("Conversation is too short.")

    if messages[-1]["role"] != "assistant":
        raise ValueError(
            "Final message must be an assistant response."
        )

    if max_length <= 0:
        raise ValueError("max_length must be positive.")

    prefix_messages = messages[:-1]

    prefix_text = tokenizer.apply_chat_template(
        prefix_messages,
        tokenize=False,
        add_generation_prompt=True,
    )
    full_text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=False,
    )

    prefix_tokens = tokenizer(
        prefix_text,
        add_special_tokens=False,
    )["input_ids"]
    full_tokens = tokenizer(
        full_text,
        add_special_tokens=False,
    )["input_ids"]

    if len(prefix_tokens) >= len(full_tokens):
        raise ValueError(
            "No final assistant tokens remain after tokenization."
        )

    if full_tokens[: len(prefix_tokens)] != prefix_tokens:
        raise ValueError(
            "Chat template prefix does not align with the "
            "complete conversation."
        )

    final_token_count = len(full_tokens) - len(prefix_tokens)

    if final_token_count >= max_length:
        raise ValueError(
            "max_length cannot contain the final assistant "
            "response."
        )

    tokens_to_drop = max(
        0,
        len(full_tokens) - max_length,
    )
    input_ids = full_tokens[tokens_to_drop:]
    masked_prefix_length = (
        len(prefix_tokens) - tokens_to_drop
    )

    if masked_prefix_length < 0:
        masked_prefix_length = 0

    labels = input_ids.copy()
    labels[:masked_prefix_length] = (
        [-100] * masked_prefix_length
    )

    supervised_count = sum(
        label != -100
        for label in labels
    )

    if supervised_count != final_token_count:
        raise ValueError(
            "Final-target supervision boundary is inconsistent."
        )

    return {
        "input_ids": input_ids,
        "attention_mask": [1] * len(input_ids),
        "labels": labels,
    }
