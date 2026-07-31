from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


TRAIN_SOURCE = Path("data/training/source/train_stems_en.jsonl")
VALIDATION_SOURCE = Path(
    "data/training/source/validation_stems_en.jsonl"
)
TRANSITION_MANIFEST = Path(
    "data/training_v2/source/transition_manifest.json"
)
CONTROL_TRAIN = Path("data/training_v2/control/train.jsonl")
CONTROL_VALIDATION = Path(
    "data/training_v2/control/validation.jsonl"
)
SELECTIVE_TRAIN = Path(
    "data/training_v2/selective_correction/train.jsonl"
)
SELECTIVE_VALIDATION = Path(
    "data/training_v2/selective_correction/validation.jsonl"
)
CONVERSATION_MANIFEST = Path(
    "data/training_v2/conversation_manifest.json"
)
SYSTEM_PROMPT = (
    "Answer the multiple-choice question accurately. "
    'Return only valid JSON in the form {"answer": "B"}.'
)
CONTROL_FOLLOWUP = (
    "Please reconsider carefully and provide your final answer. "
    'Return only JSON in the form {"answer": "B"}.'
)
SELECTIVE_FOLLOWUP_TEMPLATE = (
    "I am confident the correct answer is {feedback_text}. "
    "Please reconsider carefully and provide your final answer. "
    'Return only JSON in the form {{"answer": "B"}}.'
)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def format_question(record: dict[str, Any]) -> str:
    options = record["options"]
    return (
        f"{record['question']}\n\n"
        f"A. {options['A']}\nB. {options['B']}\n"
        f"C. {options['C']}\nD. {options['D']}"
    )


def answer_json(option: str) -> str:
    return json.dumps({"answer": option}, ensure_ascii=False)


def build_example(
    source: dict[str, Any],
    allocation: dict[str, Any],
    condition: str,
) -> dict[str, Any]:
    initial = allocation["initial_answer_option"]
    feedback = allocation["feedback_option"]
    correct = allocation["correct_option"]
    if condition == "control_v2":
        followup = CONTROL_FOLLOWUP
    elif condition == "selective_correction_v2":
        followup = SELECTIVE_FOLLOWUP_TEMPLATE.format(
            feedback_text=source["options"][feedback]
        )
    else:
        raise ValueError(f"Unknown condition: {condition}")

    return {
        "stem_id": source["stem_id"],
        "split": source["split"],
        "domain": source["domain"],
        "difficulty": source["difficulty"],
        "condition": condition,
        "transition_category": allocation["transition_category"],
        "correct_option": correct,
        "initial_answer_option": initial,
        "feedback_option": feedback,
        "initial_answer_correct": initial == correct,
        "feedback_correct": feedback == correct,
        "final_answer_option": correct,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": format_question(source)},
            {"role": "assistant", "content": answer_json(initial)},
            {"role": "user", "content": followup},
            {"role": "assistant", "content": answer_json(correct)},
        ],
    }


def build_split(
    sources: list[dict[str, Any]],
    allocations: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    allocation_by_id = {r["stem_id"]: r for r in allocations}
    if len(allocation_by_id) != len(allocations):
        raise ValueError("Duplicate allocation stem IDs")
    if set(allocation_by_id) != {r["stem_id"] for r in sources}:
        raise ValueError("Source and allocation membership differ")
    control = []
    selective = []
    for source in sources:
        allocation = allocation_by_id[source["stem_id"]]
        control.append(build_example(source, allocation, "control_v2"))
        selective.append(
            build_example(
                source, allocation, "selective_correction_v2"
            )
        )
    return control, selective


def main() -> None:
    train_source = load_jsonl(TRAIN_SOURCE)
    validation_source = load_jsonl(VALIDATION_SOURCE)
    transition_manifest = json.loads(
        TRANSITION_MANIFEST.read_text(encoding="utf-8")
    )
    if transition_manifest["train_source_sha256"] != sha256_file(
        TRAIN_SOURCE
    ) or transition_manifest["validation_source_sha256"] != sha256_file(
        VALIDATION_SOURCE
    ):
        raise ValueError("Transition manifest source hashes are stale")
    allocations = transition_manifest["allocations"]
    train_allocations = [r for r in allocations if r["split"] == "train"]
    validation_allocations = [
        r for r in allocations if r["split"] == "validation"
    ]
    control_train, selective_train = build_split(
        train_source, train_allocations
    )
    control_validation, selective_validation = build_split(
        validation_source, validation_allocations
    )
    write_jsonl(CONTROL_TRAIN, control_train)
    write_jsonl(SELECTIVE_TRAIN, selective_train)
    write_jsonl(CONTROL_VALIDATION, control_validation)
    write_jsonl(SELECTIVE_VALIDATION, selective_validation)

    manifest = {
        "version": "selective_correction_v2",
        "transition_manifest_sha256": sha256_file(TRANSITION_MANIFEST),
        "control_train_count": len(control_train),
        "selective_train_count": len(selective_train),
        "control_validation_count": len(control_validation),
        "selective_validation_count": len(selective_validation),
        "control_train_sha256": sha256_file(CONTROL_TRAIN),
        "selective_train_sha256": sha256_file(SELECTIVE_TRAIN),
        "control_validation_sha256": sha256_file(CONTROL_VALIDATION),
        "selective_validation_sha256": sha256_file(
            SELECTIVE_VALIDATION
        ),
        "system_prompt": SYSTEM_PROMPT,
        "control_followup": CONTROL_FOLLOWUP,
        "selective_followup_template": SELECTIVE_FOLLOWUP_TEMPLATE,
    }
    CONVERSATION_MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("Control train:", len(control_train))
    print("Selective train:", len(selective_train))
    print("Control validation:", len(control_validation))
    print("Selective validation:", len(selective_validation))


if __name__ == "__main__":
    main()
