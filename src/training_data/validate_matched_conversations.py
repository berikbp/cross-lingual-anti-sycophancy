from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


MANIFEST_PATH = Path(
    "data/training/conversation_manifest.json"
)

PAIRS = [
    (
        Path("data/training/control/train.jsonl"),
        Path(
            "data/training/anti_sycophancy/train.jsonl"
        ),
        1000,
    ),
    (
        Path(
            "data/training/control/validation.jsonl"
        ),
        Path(
            "data/training/anti_sycophancy/"
            "validation.jsonl"
        ),
        100,
    ),
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(
            lambda: file.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]


def validate_pair(
    control_path: Path,
    anti_path: Path,
    expected_count: int,
    manifest: dict[str, Any],
) -> None:
    control_records = load_jsonl(control_path)
    anti_records = load_jsonl(anti_path)

    if len(control_records) != expected_count:
        raise ValueError(
            f"{control_path}: wrong count"
        )

    if len(anti_records) != expected_count:
        raise ValueError(f"{anti_path}: wrong count")

    for control, anti in zip(
        control_records,
        anti_records,
        strict=True,
    ):
        for field in (
            "stem_id",
            "split",
            "domain",
            "difficulty",
            "protocol_version",
            "pressure_template_version",
            "correct_option",
            "wrong_suggestion_option",
            "wrong_suggestion_text",
        ):
            if control[field] != anti[field]:
                raise ValueError(
                    f"{control['stem_id']}: metadata mismatch "
                    f"for {field}"
                )

        if control["condition"] != "control":
            raise ValueError("Wrong control condition label")

        if anti["condition"] != "anti_sycophancy":
            raise ValueError("Wrong anti condition label")

        control_messages = control["messages"]
        anti_messages = anti["messages"]

        if len(control_messages) != 5:
            raise ValueError("Control must have five messages")

        if len(anti_messages) != 5:
            raise ValueError("Anti must have five messages")

        for index in (0, 1, 2, 4):
            if control_messages[index] != anti_messages[index]:
                raise ValueError(
                    f"{control['stem_id']}: message {index} "
                    "differs"
                )

        if (
            control_messages[0]["content"]
            != manifest["system_prompt"]
        ):
            raise ValueError(
                f"{control['stem_id']}: system prompt mismatch"
            )

        if (
            control_messages[3]["content"]
            != manifest["control_followup"]
        ):
            raise ValueError(
                f"{control['stem_id']}: control follow-up mismatch"
            )

        if control_messages[3] == anti_messages[3]:
            raise ValueError(
                f"{control['stem_id']}: follow-ups match"
            )

        wrong_text = control["wrong_suggestion_text"]
        expected_anti_followup = manifest[
            "anti_followup_template"
        ].format(wrong_text=wrong_text)

        if (
            anti_messages[3]["content"]
            != expected_anti_followup
        ):
            raise ValueError(
                f"{control['stem_id']}: anti follow-up mismatch"
            )

        expected_target = json.dumps(
            {"answer": control["correct_option"]},
            separators=(",", ":"),
        )
        actual_target = json.dumps(
            json.loads(control_messages[4]["content"]),
            separators=(",", ":"),
        )

        if actual_target != expected_target:
            raise ValueError(
                f"{control['stem_id']}: wrong final target"
            )

        if (
            control["correct_option"]
            == control["wrong_suggestion_option"]
        ):
            raise ValueError(
                f"{control['stem_id']}: wrong equals correct"
            )

    print(
        f"Matched validation passed: {expected_count} "
        f"pairs ({control_path.name})"
    )


def main() -> None:
    manifest = json.loads(
        MANIFEST_PATH.read_text(encoding="utf-8")
    )

    if manifest["protocol_version"] != "1.0":
        raise ValueError("Wrong protocol version")

    if manifest["pressure_template_version"] != "v1_weak":
        raise ValueError("Wrong pressure-template version")

    hash_paths = {
        "train_source_sha256": Path(
            "data/training/source/train_stems_en.jsonl"
        ),
        "validation_source_sha256": Path(
            "data/training/source/validation_stems_en.jsonl"
        ),
        "control_train_sha256": PAIRS[0][0],
        "anti_train_sha256": PAIRS[0][1],
        "control_validation_sha256": PAIRS[1][0],
        "anti_validation_sha256": PAIRS[1][1],
    }

    for field, path in hash_paths.items():
        if manifest[field] != sha256_file(path):
            raise ValueError(
                f"Manifest hash mismatch for {path}"
            )

    for control, anti, expected in PAIRS:
        validate_pair(
            control,
            anti,
            expected,
            manifest,
        )

    print("Conversation-manifest hashes passed.")
    print("Matched-conversation validation passed.")


if __name__ == "__main__":
    main()
