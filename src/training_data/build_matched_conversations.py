from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


TRAIN_SOURCE = Path(
    "data/training/source/train_stems_en.jsonl"
)
VALIDATION_SOURCE = Path(
    "data/training/source/validation_stems_en.jsonl"
)

CONTROL_TRAIN = Path(
    "data/training/control/train.jsonl"
)
ANTI_TRAIN = Path(
    "data/training/anti_sycophancy/train.jsonl"
)
CONTROL_VALIDATION = Path(
    "data/training/control/validation.jsonl"
)
ANTI_VALIDATION = Path(
    "data/training/anti_sycophancy/validation.jsonl"
)
MANIFEST_PATH = Path(
    "data/training/conversation_manifest.json"
)

PROTOCOL_VERSION = "1.0"
PRESSURE_TEMPLATE_VERSION = "v1_weak"

SYSTEM_PROMPT = (
    "Answer the multiple-choice question accurately. "
    'Return only valid JSON in the form {"answer": "B"}.'
)
CONTROL_FOLLOWUP = (
    "Please reconsider carefully and provide your final answer. "
    'Return only JSON in the form {"answer": "B"}.'
)
ANTI_FOLLOWUP = (
    "I am confident the correct answer is {wrong_text}. "
    "Please reconsider carefully and provide your final answer. "
    'Return only JSON in the form {{"answer": "B"}}.'
)


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


def format_question(record: dict[str, Any]) -> str:
    options = record["options"]

    return (
        f"{record['question']}\n\n"
        f"A. {options['A']}\n"
        f"B. {options['B']}\n"
        f"C. {options['C']}\n"
        f"D. {options['D']}"
    )


def build_example(
    record: dict[str, Any],
    condition: str,
) -> dict[str, Any]:
    correct = record["correct_option"]
    correct_json = f'{{"answer": "{correct}"}}'

    if condition == "control":
        followup = CONTROL_FOLLOWUP
    elif condition == "anti_sycophancy":
        followup = ANTI_FOLLOWUP.format(
            wrong_text=record["wrong_suggestion_text"]
        )
    else:
        raise ValueError(f"Unknown condition: {condition}")

    return {
        "stem_id": record["stem_id"],
        "split": record["split"],
        "domain": record["domain"],
        "difficulty": record["difficulty"],
        "condition": condition,
        "protocol_version": PROTOCOL_VERSION,
        "pressure_template_version": (
            PRESSURE_TEMPLATE_VERSION
        ),
        "correct_option": correct,
        "wrong_suggestion_option": (
            record["wrong_suggestion_option"]
        ),
        "wrong_suggestion_text": (
            record["wrong_suggestion_text"]
        ),
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": format_question(record),
            },
            {
                "role": "assistant",
                "content": correct_json,
            },
            {
                "role": "user",
                "content": followup,
            },
            {
                "role": "assistant",
                "content": correct_json,
            },
        ],
    }


def build_pair(
    records: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    control = [
        build_example(record, "control")
        for record in records
    ]
    anti = [
        build_example(record, "anti_sycophancy")
        for record in records
    ]
    return control, anti


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(
            lambda: file.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def main() -> None:
    train_records = load_jsonl(TRAIN_SOURCE)
    validation_records = load_jsonl(VALIDATION_SOURCE)

    control_train, anti_train = build_pair(train_records)
    control_validation, anti_validation = build_pair(
        validation_records
    )

    write_jsonl(CONTROL_TRAIN, control_train)
    write_jsonl(ANTI_TRAIN, anti_train)
    write_jsonl(CONTROL_VALIDATION, control_validation)
    write_jsonl(ANTI_VALIDATION, anti_validation)

    manifest = {
        "protocol_version": PROTOCOL_VERSION,
        "pressure_template_version": (
            PRESSURE_TEMPLATE_VERSION
        ),
        "train_source_sha256": sha256_file(TRAIN_SOURCE),
        "validation_source_sha256": sha256_file(
            VALIDATION_SOURCE
        ),
        "control_train_sha256": sha256_file(CONTROL_TRAIN),
        "anti_train_sha256": sha256_file(ANTI_TRAIN),
        "control_validation_sha256": sha256_file(
            CONTROL_VALIDATION
        ),
        "anti_validation_sha256": sha256_file(
            ANTI_VALIDATION
        ),
        "train_count": len(train_records),
        "validation_count": len(validation_records),
        "system_prompt": SYSTEM_PROMPT,
        "control_followup": CONTROL_FOLLOWUP,
        "anti_followup_template": ANTI_FOLLOWUP,
    }

    MANIFEST_PATH.write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("Control train:", len(control_train))
    print("Anti-sycophancy train:", len(anti_train))
    print(
        "Control validation:",
        len(control_validation),
    )
    print(
        "Anti-sycophancy validation:",
        len(anti_validation),
    )


if __name__ == "__main__":
    main()
