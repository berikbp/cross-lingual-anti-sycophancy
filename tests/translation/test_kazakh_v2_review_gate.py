from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.translation.build_kazakh_v2_review_draft import CORRECTIONS
from src.translation.finalize_kazakh_v2 import load_jsonl, validate_review
from src.translation.import_kazakh_v2_native_review import (
    import_review,
    load_worksheet,
)


def test_known_corrections_are_explicit_and_versioned() -> None:
    assert set(CORRECTIONS) == {
        "master_logic_023",
        "master_geo_078",
        "master_science_053",
        "master_logic_039",
        "master_logic_054",
        "master_geo_042",
    }


def test_review_draft_cannot_be_frozen_as_approved() -> None:
    english = load_jsonl(Path("data/final/test_en.jsonl"))
    draft = load_jsonl(
        Path("data/translation/review/kazakh_v2_review_draft.jsonl")
    )
    assert len(draft) == 300
    assert all(record["human_reviewed"] is False for record in draft)
    assert all(
        record["translation_status"] == "needs_native_review"
        for record in draft
    )
    assert all(
        "native review pending" in record["translator_note"]
        for record in draft
    )
    with pytest.raises(ValueError, match="review is incomplete"):
        validate_review(english, draft)


def test_change_log_hash_matches_review_draft() -> None:
    log = json.loads(
        Path(
            "reports/translation_audits/kazakh_v2_known_corrections.json"
        ).read_text(encoding="utf-8")
    )
    assert log["known_correction_count"] == 6
    assert len(log["changes"]) == 6


def test_pending_native_worksheet_cannot_be_imported() -> None:
    draft = load_jsonl(
        Path("data/translation/review/kazakh_v2_review_draft.jsonl")
    )
    worksheet = load_worksheet(
        Path("reports/translation_audits/kazakh_v2_native_review.csv")
    )
    assert len(worksheet) == 300
    with pytest.raises(ValueError, match="semantic_equivalence is not yes"):
        import_review(draft, worksheet)


def test_explicit_complete_worksheet_imports_review_metadata() -> None:
    draft = load_jsonl(
        Path("data/translation/review/kazakh_v2_review_draft.jsonl")
    )
    worksheet = [
        dict(row)
        for row in load_worksheet(
            Path("reports/translation_audits/kazakh_v2_native_review.csv")
        )
    ]
    for row in worksheet:
        for field in (
            "semantic_equivalence",
            "answer_preserved",
            "distractors_preserved",
            "language_quality",
        ):
            row[field] = "yes"
        row["decision"] = "approved"
        row["reviewer"] = "Test Reviewer"
        row["review_date"] = "2026-08-02"
        row["review_note"] = "Approved in unit-test fixture."

    reviewed = import_review(draft, worksheet)
    assert len(reviewed) == 300
    assert all(record["human_reviewed"] is True for record in reviewed)
    assert all(record["translation_status"] == "approved" for record in reviewed)
    assert reviewed[0]["human_reviewer"] == "Test Reviewer"
