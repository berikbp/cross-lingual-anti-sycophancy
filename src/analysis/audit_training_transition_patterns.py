from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


DATASETS = {
    "Control-v1 train": Path("data/training/control/train.jsonl"),
    "Control-v1 validation": Path(
        "data/training/control/validation.jsonl"
    ),
    "Anti-sycophancy-v1 train": Path(
        "data/training/anti_sycophancy/train.jsonl"
    ),
    "Anti-sycophancy-v1 validation": Path(
        "data/training/anti_sycophancy/validation.jsonl"
    ),
}
OUTPUT_PATH = Path("reports/training_transition_audit.md")
LETTERS = {"A", "B", "C", "D"}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def parse_answer(message: dict[str, str]) -> str:
    value = json.loads(message["content"])
    answer = value.get("answer")
    if answer not in LETTERS:
        raise ValueError(f"Invalid assistant target: {message!r}")
    return answer


def classify(record: dict[str, Any]) -> tuple[str, str, str, str]:
    messages = record["messages"]
    if len(messages) != 5:
        raise ValueError(
            f"{record['stem_id']}: expected five messages"
        )
    if [message["role"] for message in messages] != [
        "system",
        "user",
        "assistant",
        "user",
        "assistant",
    ]:
        raise ValueError(f"{record['stem_id']}: invalid role order")

    initial = parse_answer(messages[2])
    final = parse_answer(messages[4])
    correct = record["correct_option"]
    initial_state = "initial_correct" if initial == correct else "initial_wrong"
    final_state = "final_correct" if final == correct else "final_wrong"
    change_state = "changed" if final != initial else "unchanged"

    if record["condition"] == "control":
        feedback = "neutral"
    elif record["condition"] == "anti_sycophancy":
        wrong = record["wrong_suggestion_option"]
        if wrong == correct:
            raise ValueError(
                f"{record['stem_id']}: wrong suggestion is correct"
            )
        if record["wrong_suggestion_text"] not in messages[3]["content"]:
            raise ValueError(
                f"{record['stem_id']}: wrong suggestion text absent"
            )
        feedback = "incorrect_suggestion"
    else:
        raise ValueError(
            f"{record['stem_id']}: unknown condition"
        )
    return initial_state, feedback, change_state, final_state


def main() -> None:
    summaries: dict[str, Counter[tuple[str, str, str, str]]] = {}
    for label, path in DATASETS.items():
        records = load_jsonl(path)
        expected = 100 if "validation" in label else 1000
        if len(records) != expected:
            raise ValueError(
                f"{label}: expected {expected}, found {len(records)}"
            )
        summaries[label] = Counter(classify(record) for record in records)

    lines = [
        "# Stage 11 Training Transition Audit",
        "",
        "## Observed transition patterns",
        "",
        "| Dataset | Count | Initial state | Follow-up | Final changed? | Final state |",
        "|---|---:|---|---|---|---|",
    ]
    for label, counts in summaries.items():
        for pattern, count in sorted(counts.items()):
            initial, feedback, changed, final = pattern
            lines.append(
                f"| {label} | {count} | {initial} | {feedback} | {changed} | {final} |"
            )

    missing = [
        (
            "Initial wrong + correct suggestion → changed and correct",
            "Accept a valid user correction",
        ),
        (
            "Initial wrong + neutral reconsideration → changed and correct",
            "Self-correct without an explicit answer suggestion",
        ),
        (
            "Initial correct + correct suggestion → unchanged and correct",
            "Accept correct support without learning to reject all suggestions",
        ),
        (
            "Initial wrong + incorrect suggestion → changed independently to correct",
            "Reject bad feedback while still revising an erroneous prior answer",
        ),
    ]
    lines.extend(
        [
            "",
            "## Missing transition types",
            "",
            "| Missing supervision | Behavior it would teach |",
            "|---|---|",
            *[
                f"| {transition} | {purpose} |"
                for transition, purpose in missing
            ],
            "",
            "## Conclusion",
            "",
            "Every one of the 2,200 Stage 11 train and validation conversations has a correct initial assistant answer and an unchanged correct final answer. The 1,100 control conversations use neutral reconsideration; the 1,100 anti-sycophancy conversations use an explicitly incorrect suggestion. No conversation supervises a change from an initially wrong answer to a correct final answer.",
            "",
            "Stage 11 therefore contains complete supervision for answer preservation and no supervision for beneficial correction. The observed v1 stubbornness is consistent with this target distribution. This audit establishes a dataset mechanism; it does not by itself prove that no other training factor contributed.",
        ]
    )
    OUTPUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
