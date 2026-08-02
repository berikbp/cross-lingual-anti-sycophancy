from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from src.translation.build_kazakh_v2_review_draft import CORRECTIONS
from src.translation.finalize_kazakh_v2 import (
    ATTESTATION,
    ENGLISH,
    REVIEWED,
    load_jsonl,
    sha256,
    validate_review,
)


EXPECTED_FIELDS = {
    "stem_id",
    "source_stem_id",
    "language",
    "domain",
    "difficulty",
    "question",
    "options",
    "correct_option",
    "wrong_suggestion_option",
    "wrong_suggestion_text",
    "translation_status",
    "translation_method",
}


def load_attestation() -> dict:
    return json.loads(ATTESTATION.read_text(encoding="utf-8"))


def test_known_corrections_are_explicit_and_versioned() -> None:
    assert set(CORRECTIONS) == {
        "master_logic_023",
        "master_geo_078",
        "master_science_053",
        "master_logic_039",
        "master_logic_054",
        "master_geo_042",
    }


def test_reviewed_dataset_has_a_minimal_schema() -> None:
    records = load_jsonl(REVIEWED)
    assert len(records) == 300
    assert all(set(record) == EXPECTED_FIELDS for record in records)
    assert all(record["translation_status"] == "approved" for record in records)


def test_review_attestation_matches_the_reviewed_dataset() -> None:
    attestation = load_attestation()
    assert attestation["record_count"] == 300
    assert attestation["reviewed_sha256"] == sha256(REVIEWED)
    assert attestation["reviewer"] == "Berik Satybaldy"
    assert all(attestation["review_scope"].values())


def test_reviewed_dataset_passes_freeze_validation() -> None:
    validate_review(
        load_jsonl(ENGLISH),
        load_jsonl(REVIEWED),
        load_attestation(),
    )


def test_tampered_dataset_fails_attestation_hash() -> None:
    reviewed = copy.deepcopy(load_jsonl(REVIEWED))
    reviewed[0]["question"] += " өзгертілді"
    with pytest.raises(ValueError, match="attestation hash"):
        validate_review(load_jsonl(ENGLISH), reviewed, load_attestation())


def test_change_log_records_all_six_corrections() -> None:
    log = json.loads(
        Path(
            "reports/translation_audits/kazakh_v2_known_corrections.json"
        ).read_text(encoding="utf-8")
    )
    assert log["known_correction_count"] == 6
    assert len(log["changes"]) == 6
