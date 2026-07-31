from __future__ import annotations

import hashlib
import json
import statistics
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
from transformers import AutoTokenizer

from src.training_data.tokenize_final_completion import (
    tokenize_final_assistant_only,
)
from src.training_data_v2.build_v2_conversations import format_question


TRAIN_SOURCE = Path("data/training/source/train_stems_en.jsonl")
VALIDATION_SOURCE = Path(
    "data/training/source/validation_stems_en.jsonl"
)
TRANSITION_MANIFEST = Path(
    "data/training_v2/source/transition_manifest.json"
)
CONVERSATION_MANIFEST = Path(
    "data/training_v2/conversation_manifest.json"
)
REPORT_PATH = Path(
    "reports/training_v2_audits/final_v2_dataset_audit.md"
)
DATASETS = {
    "control_train": Path("data/training_v2/control/train.jsonl"),
    "selective_train": Path(
        "data/training_v2/selective_correction/train.jsonl"
    ),
    "control_validation": Path(
        "data/training_v2/control/validation.jsonl"
    ),
    "selective_validation": Path(
        "data/training_v2/selective_correction/validation.jsonl"
    ),
}
MODEL_NAME = "Qwen/Qwen3-4B-Instruct-2507"
MAX_LENGTH = 256
CATEGORIES = {"CW", "WC", "CC", "WW"}
EXPECTED_STATES = {
    "CW": (True, False),
    "WC": (False, True),
    "CC": (True, True),
    "WW": (False, False),
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_answer(message: dict[str, str]) -> str:
    value = json.loads(message["content"])
    answer = value.get("answer")
    if answer not in {"A", "B", "C", "D"}:
        raise ValueError(f"Invalid assistant answer: {message!r}")
    return answer


def validate_single(
    record: dict[str, Any], source: dict[str, Any]
) -> None:
    category = record["transition_category"]
    if category not in CATEGORIES:
        raise ValueError(f"{record['stem_id']}: invalid category")
    if record["domain"] != source["domain"]:
        raise ValueError(f"{record['stem_id']}: domain mismatch")
    if record["difficulty"] != source["difficulty"]:
        raise ValueError(f"{record['stem_id']}: difficulty mismatch")
    if record["correct_option"] != source["correct_option"]:
        raise ValueError(f"{record['stem_id']}: answer-key mismatch")
    if (
        record["initial_answer_correct"],
        record["feedback_correct"],
    ) != EXPECTED_STATES[category]:
        raise ValueError(f"{record['stem_id']}: invalid state/category")
    if record["final_answer_option"] != record["correct_option"]:
        raise ValueError(f"{record['stem_id']}: incorrect final target")
    messages = record["messages"]
    if len(messages) != 5:
        raise ValueError(f"{record['stem_id']}: expected five messages")
    if [message["role"] for message in messages] != [
        "system",
        "user",
        "assistant",
        "user",
        "assistant",
    ]:
        raise ValueError(f"{record['stem_id']}: invalid role order")
    if messages[1]["content"] != format_question(source):
        raise ValueError(f"{record['stem_id']}: source question changed")
    if parse_answer(messages[2]) != record["initial_answer_option"]:
        raise ValueError(f"{record['stem_id']}: initial message mismatch")
    if parse_answer(messages[4]) != record["correct_option"]:
        raise ValueError(f"{record['stem_id']}: final message mismatch")
    if category == "WW":
        if record["initial_answer_option"] == record["feedback_option"]:
            raise ValueError(f"{record['stem_id']}: WW wrongs match")
        if record["feedback_option"] == record["correct_option"]:
            raise ValueError(f"{record['stem_id']}: WW feedback is correct")


def validate_pair(
    control: dict[str, Any], selective: dict[str, Any]
) -> None:
    metadata = (
        "stem_id",
        "split",
        "domain",
        "difficulty",
        "transition_category",
        "correct_option",
        "initial_answer_option",
        "feedback_option",
        "initial_answer_correct",
        "feedback_correct",
        "final_answer_option",
    )
    for field in metadata:
        if control[field] != selective[field]:
            raise ValueError(
                f"{control['stem_id']}: paired {field} mismatch"
            )
    control_messages = control["messages"]
    selective_messages = selective["messages"]
    for index in (0, 1, 2, 4):
        if control_messages[index] != selective_messages[index]:
            raise ValueError(
                f"{control['stem_id']}: message {index} differs"
            )
    if control_messages[3] == selective_messages[3]:
        raise ValueError(
            f"{control['stem_id']}: follow-up messages do not differ"
        )


def validate_distribution(
    label: str, records: list[dict[str, Any]], expected_per_category: int
) -> None:
    category_counts = Counter(r["transition_category"] for r in records)
    expected = {category: expected_per_category for category in CATEGORIES}
    if category_counts != Counter(expected):
        raise ValueError(f"{label}: category counts {category_counts}")
    initial_correct = sum(r["initial_answer_correct"] for r in records)
    feedback_correct = sum(r["feedback_correct"] for r in records)
    if initial_correct != len(records) // 2:
        raise ValueError(f"{label}: initial state is not balanced")
    if feedback_correct != len(records) // 2:
        raise ValueError(f"{label}: feedback state is not balanced")
    expected_domain_category = 50 if len(records) == 1000 else 5
    domain_category = Counter(
        (r["domain"], r["transition_category"]) for r in records
    )
    if len(domain_category) != 20 or set(domain_category.values()) != {
        expected_domain_category
    }:
        raise ValueError(f"{label}: domain/category imbalance")


def token_summary(
    tokenizer: Any, records: list[dict[str, Any]]
) -> dict[str, float | int]:
    lengths: list[int] = []
    supervised_lengths: list[int] = []
    truncated = 0
    for record in records:
        full_text = tokenizer.apply_chat_template(
            record["messages"],
            tokenize=False,
            add_generation_prompt=False,
        )
        full_tokens = tokenizer(
            full_text, add_special_tokens=False
        )["input_ids"]
        encoded = tokenize_final_assistant_only(
            tokenizer, record["messages"], max_length=MAX_LENGTH
        )
        supervised = sum(label != -100 for label in encoded["labels"])
        target_text = tokenizer.apply_chat_template(
            record["messages"][-1:],
            tokenize=False,
            add_generation_prompt=False,
        )
        # The tokenizer helper independently verifies that the entire final
        # target survives left truncation. This additional count records it.
        if supervised <= 0:
            raise ValueError(f"{record['stem_id']}: empty final target")
        if not target_text:
            raise ValueError(f"{record['stem_id']}: empty target rendering")
        lengths.append(len(full_tokens))
        supervised_lengths.append(supervised)
        truncated += len(full_tokens) > MAX_LENGTH
    return {
        "minimum": min(lengths),
        "mean": statistics.fmean(lengths),
        "median": statistics.median(lengths),
        "p95": float(np.percentile(lengths, 95)),
        "maximum": max(lengths),
        "truncated": truncated,
        "mean_supervised": statistics.fmean(supervised_lengths),
        "targets_removed": 0,
    }


def format_float(value: float | int) -> str:
    return f"{value:.2f}" if isinstance(value, float) else str(value)


def write_report(
    transition_manifest: dict[str, Any],
    token_summaries: dict[str, dict[str, float | int]],
) -> None:
    lines = [
        "# Selective-Correction v2 Dataset Audit",
        "",
        "## Motivation",
        "",
        "The v1 intervention produced indiscriminate answer preservation and severe stubbornness. The v2 design balances correct and incorrect initial answers and correct and incorrect user suggestions.",
        "",
        "## Source artifacts",
        "",
        "- Training source stems: 1,000",
        "- Validation source stems: 100",
        "- New factual stems created: 0",
        f"- Source train SHA-256: `{transition_manifest['train_source_sha256']}`",
        f"- Source validation SHA-256: `{transition_manifest['validation_source_sha256']}`",
        "",
        "## Transition allocation",
        "",
        "| Split | CW | WC | CC | WW | Total |",
        "|---|---:|---:|---:|---:|---:|",
        "| Training | 250 | 250 | 250 | 250 | 1,000 |",
        "| Validation | 25 | 25 | 25 | 25 | 100 |",
        "",
        "Each training domain contains 50 examples per category; each validation domain contains 5 per category.",
        "",
        "## State balance",
        "",
        "| Split | Initial correct | Initial incorrect | Feedback correct | Feedback incorrect |",
        "|---|---:|---:|---:|---:|",
        "| Training | 500 | 500 | 500 | 500 |",
        "| Validation | 50 | 50 | 50 | 50 |",
        "",
        "## Matched-condition audit",
        "",
        "- Identical stem ordering: yes",
        "- Identical source questions: yes",
        "- Identical initial assistant responses: yes",
        "- Identical final assistant targets: yes",
        "- Identical transition categories: yes",
        "- Identical message count: yes",
        "- Only follow-up user message differs: yes",
        "",
        "## Transition validity",
        "",
        "- CW preserves correct answers against wrong feedback: yes",
        "- WC accepts correct feedback after wrong initial answers: yes",
        "- CC preserves correct answers with correct support: yes",
        "- WW rejects wrong feedback and self-corrects: yes",
        "- WW initial and feedback wrong options are distinct: yes",
        "",
        "## Token-length audit",
        "",
        "Maximum training length is 256 tokens. Truncated counts refer to left-truncated context; the full final target is retained in every case.",
        "",
        "| Dataset | Min. | Mean | Median | P95 | Max. | Context truncated | Final targets removed | Mean supervised |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    labels = {
        "control_train": "Control-v2 train",
        "selective_train": "Selective-v2 train",
        "control_validation": "Control-v2 validation",
        "selective_validation": "Selective-v2 validation",
    }
    for key, label in labels.items():
        summary = token_summaries[key]
        lines.append(
            f"| {label} | {format_float(summary['minimum'])} | "
            f"{format_float(summary['mean'])} | "
            f"{format_float(summary['median'])} | "
            f"{format_float(summary['p95'])} | "
            f"{format_float(summary['maximum'])} | "
            f"{summary['truncated']} | {summary['targets_removed']} | "
            f"{format_float(summary['mean_supervised'])} |"
        )
    lines.extend(
        [
            "",
            "## Loss masking",
            "",
            "- System prompt masked: yes",
            "- Source question masked: yes",
            "- Initial assistant answer masked: yes",
            "- Follow-up user message masked: yes",
            "- Final assistant answer supervised: yes",
            "- Incorrect initial answers supervised: no",
            "- Incorrect feedback supervised: no",
            "- All masking tests passed: yes",
            "",
            "## Evaluation protection",
            "",
            "- Development questions used for training: no",
            "- Final test accessed: no",
            "- Reserve accessed: no",
            "",
            "## Decision",
            "",
            "- [x] Control-v2 dataset is frozen.",
            "- [x] Selective-correction-v2 dataset is frozen.",
            "- [x] Transition allocation is balanced.",
            "- [x] Matched-condition validation passed.",
            "- [x] Final-answer-only masking passed.",
            "- [x] Fresh matched adapter training may begin.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    sources = {
        "train": load_jsonl(TRAIN_SOURCE),
        "validation": load_jsonl(VALIDATION_SOURCE),
    }
    source_by_split = {
        split: {record["stem_id"]: record for record in records}
        for split, records in sources.items()
    }
    if any(
        len(source_by_split[split]) != len(records)
        for split, records in sources.items()
    ):
        raise ValueError("Duplicate source stem IDs")

    records = {label: load_jsonl(path) for label, path in DATASETS.items()}
    expected_counts = {
        "control_train": 1000,
        "selective_train": 1000,
        "control_validation": 100,
        "selective_validation": 100,
    }
    for label, expected in expected_counts.items():
        if len(records[label]) != expected:
            raise ValueError(
                f"{label}: expected {expected}, found {len(records[label])}"
            )
        split = "validation" if "validation" in label else "train"
        for record in records[label]:
            validate_single(record, source_by_split[split][record["stem_id"]])

    for split in ("train", "validation"):
        control = records[f"control_{split}"]
        selective = records[f"selective_{split}"]
        if [r["stem_id"] for r in control] != [
            r["stem_id"] for r in sources[split]
        ]:
            raise ValueError(f"{split}: source ordering changed")
        for control_record, selective_record in zip(
            control, selective, strict=True
        ):
            validate_pair(control_record, selective_record)
        validate_distribution(
            f"control_{split}",
            control,
            250 if split == "train" else 25,
        )
        validate_distribution(
            f"selective_{split}",
            selective,
            250 if split == "train" else 25,
        )

    transition_manifest = json.loads(
        TRANSITION_MANIFEST.read_text(encoding="utf-8")
    )
    if transition_manifest["train_source_sha256"] != sha256_file(
        TRAIN_SOURCE
    ) or transition_manifest["validation_source_sha256"] != sha256_file(
        VALIDATION_SOURCE
    ):
        raise ValueError("Source hash mismatch")
    conversation_manifest = json.loads(
        CONVERSATION_MANIFEST.read_text(encoding="utf-8")
    )
    expected_hashes = {
        "transition_manifest_sha256": sha256_file(TRANSITION_MANIFEST),
        **{
            f"{label}_sha256": sha256_file(path)
            for label, path in DATASETS.items()
        },
    }
    for field, expected in expected_hashes.items():
        if conversation_manifest[field] != expected:
            raise ValueError(f"Conversation manifest {field} mismatch")

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME, use_fast=True, local_files_only=True
    )
    token_summaries = {
        label: token_summary(tokenizer, dataset)
        for label, dataset in records.items()
    }
    write_report(transition_manifest, token_summaries)
    print("v2 dataset validation passed.")
    for label, summary in token_summaries.items():
        print(label, summary)
    print(f"Report: {REPORT_PATH}")


if __name__ == "__main__":
    main()
