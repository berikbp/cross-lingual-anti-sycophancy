from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ENGLISH = Path("data/final/test_en.jsonl")
REVIEWED = Path("data/final/test_kk_v2.jsonl")
ATTESTATION = Path(
    "reports/translation_audits/kazakh_v2_review_attestation.json"
)
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


def records_sha256(records: list[dict[str, Any]]) -> str:
    payload = (
        "\n".join(json.dumps(record, ensure_ascii=False) for record in records)
        + "\n"
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_review(
    source: list[dict[str, Any]],
    reviewed: list[dict[str, Any]],
    attestation: dict[str, Any],
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
        if kazakh.get("translation_status") != "approved":
            raise ValueError(f"{stem_id}: status is not approved")
        if kazakh["wrong_suggestion_text"] != kazakh["options"][
            kazakh["wrong_suggestion_option"]
        ]:
            raise ValueError(f"{stem_id}: wrong-suggestion text mismatch")
        normalized_options = {
            value.strip().casefold() for value in kazakh["options"].values()
        }
        if len(normalized_options) != 4:
            raise ValueError(f"{stem_id}: translated options are not distinct")

    if attestation.get("record_count") != 300:
        raise ValueError("Review attestation does not cover 300 records.")
    if attestation.get("reviewed_sha256") != records_sha256(reviewed):
        raise ValueError("Review attestation hash does not match the dataset.")
    if not str(attestation.get("reviewer", "")).strip():
        raise ValueError("Review attestation has no reviewer.")
    if not str(attestation.get("review_date", "")).strip():
        raise ValueError("Review attestation has no review date.")
    checks = attestation.get("review_scope", {})
    required_checks = (
        "semantic_equivalence",
        "answer_preservation",
        "distractor_preservation",
        "language_quality",
    )
    if any(checks.get(field) is not True for field in required_checks):
        raise ValueError("Review attestation is incomplete.")


def main() -> None:
    source = load_jsonl(ENGLISH)
    reviewed = load_jsonl(REVIEWED)
    attestation = json.loads(ATTESTATION.read_text(encoding="utf-8"))
    validate_review(source, reviewed, attestation)

    manifest = {
        "version": "kazakh_translation_corrected_sensitivity_v2",
        "records": 300,
        "review_attestation_path": ATTESTATION.as_posix(),
        "review_attestation_sha256": sha256(ATTESTATION),
        "english_path": str(ENGLISH),
        "english_sha256": sha256(ENGLISH),
        "kazakh_path": str(OUTPUT),
        "kazakh_sha256": sha256(OUTPUT),
        "author_review_complete": True,
        "human_reviewers": [attestation["reviewer"]],
        "human_review_dates": [attestation["review_date"]],
        "translation_method": "machine_assisted_with_author_review",
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
