from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ENGLISH = Path("data/final/test_en.jsonl")
OUTPUT = Path("data/final/test_kk_v2.jsonl")
MANIFEST = Path("data/final/kazakh_v2_manifest.json")
HASH_FILE = Path("docs/kazakh_v2_artifact_hashes.txt")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_review(
    source: list[dict[str, Any]],
    reviewed: list[dict[str, Any]],
) -> None:
    if len(source) != 300 or len(reviewed) != 300:
        raise ValueError("Expected 300 aligned English and Kazakh records.")

    for english, kazakh in zip(source, reviewed, strict=True):
        stem_id = english["stem_id"]
        if kazakh["stem_id"] != stem_id or kazakh["source_stem_id"] != stem_id:
            raise ValueError(f"{stem_id}: alignment mismatch")
        for field in (
            "domain",
            "difficulty",
            "correct_option",
            "wrong_suggestion_option",
        ):
            if kazakh[field] != english[field]:
                raise ValueError(f"{stem_id}: {field} changed")
        if kazakh.get("source_question") != english["question"]:
            raise ValueError(f"{stem_id}: embedded source question changed")
        if kazakh.get("source_options") != english["options"]:
            raise ValueError(f"{stem_id}: embedded source options changed")
        required_true = (
            kazakh.get("semantic_review") is True,
            kazakh.get("structural_review") is True,
            kazakh.get("human_reviewed") is True,
        )
        if not all(required_true):
            raise ValueError(f"{stem_id}: review is incomplete")
        if kazakh.get("translation_status") != "approved":
            raise ValueError(f"{stem_id}: status is not approved")
        if not str(kazakh.get("human_reviewer", "")).strip():
            raise ValueError(f"{stem_id}: human reviewer is missing")
        if not str(kazakh.get("human_review_date", "")).strip():
            raise ValueError(f"{stem_id}: review date is missing")
        if not str(kazakh.get("review_note", "")).strip():
            raise ValueError(f"{stem_id}: review note is missing")
        if kazakh["wrong_suggestion_text"] != kazakh["options"][
            kazakh["wrong_suggestion_option"]
        ]:
            raise ValueError(f"{stem_id}: wrong-suggestion text mismatch")
        if len({value.strip().casefold() for value in kazakh["options"].values()}) != 4:
            raise ValueError(f"{stem_id}: translated options are not distinct")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Freeze a fully native-reviewed Kazakh v2 artifact."
    )
    parser.add_argument("--reviewed", type=Path, required=True)
    arguments = parser.parse_args()

    source = load_jsonl(ENGLISH)
    reviewed = load_jsonl(arguments.reviewed)
    validate_review(source, reviewed)

    OUTPUT.write_text(
        "\n".join(json.dumps(record, ensure_ascii=False) for record in reviewed)
        + "\n",
        encoding="utf-8",
    )
    manifest = {
        "version": "kazakh_translation_corrected_sensitivity_v2",
        "records": 300,
        "reviewed_input_path": arguments.reviewed.as_posix(),
        "reviewed_input_sha256": sha256(arguments.reviewed),
        "english_path": str(ENGLISH),
        "english_sha256": sha256(ENGLISH),
        "kazakh_path": str(OUTPUT),
        "kazakh_sha256": sha256(OUTPUT),
        "native_review_complete": True,
        "human_reviewers": sorted(
            {record["human_reviewer"] for record in reviewed}
        ),
        "human_review_dates": sorted(
            {record["human_review_date"] for record in reviewed}
        ),
        "translation_method": "machine_assisted_with_native_review",
        "historical_kazakh_results_replaced": False,
    }
    MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    HASH_FILE.write_text(
        f"{sha256(OUTPUT)}  {OUTPUT}\n{sha256(MANIFEST)}  {MANIFEST}\n",
        encoding="utf-8",
    )
    print(f"Frozen corrected Kazakh records: {len(reviewed)}")


if __name__ == "__main__":
    main()
