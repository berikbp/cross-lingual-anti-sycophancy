from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.analysis.analyze_final_multilingual import metrics


def record(stem: str, branch: str, *, initial_correct: bool, branch_correct: bool, wrong: bool = False) -> dict:
    return {
        "language": "en",
        "stem_id": stem,
        "branch": branch,
        "initial_correct": initial_correct,
        "initial_parseable": True,
        "initial_parsed_answer": "A" if initial_correct else "B",
        "branch_correct": branch_correct,
        "branch_parseable": True,
        "branch_parsed_answer": "A" if branch_correct else "B",
        "changed_from_initial": initial_correct != branch_correct,
        "exact_wrong_adoption": wrong,
    }


def stem(stem_id: str, *, initial_correct: bool, b0_correct: bool, b2_correct: bool, b2_wrong: bool) -> list[dict]:
    return [
        record(stem_id, "B0", initial_correct=initial_correct, branch_correct=b0_correct),
        record(stem_id, "B1", initial_correct=initial_correct, branch_correct=initial_correct),
        record(stem_id, "B2", initial_correct=initial_correct, branch_correct=b2_correct, wrong=b2_wrong),
        record(stem_id, "B3", initial_correct=initial_correct, branch_correct=True),
    ]


def test_initial_and_b0_harmful_metrics_use_distinct_denominators() -> None:
    records = (
        stem("initial-only", initial_correct=True, b0_correct=False, b2_correct=False, b2_wrong=True)
        + stem("initial-only-2", initial_correct=True, b0_correct=False, b2_correct=False, b2_wrong=True)
        + stem("b0-only", initial_correct=False, b0_correct=True, b2_correct=False, b2_wrong=True)
        + stem("both-correct", initial_correct=True, b0_correct=True, b2_correct=True, b2_wrong=False)
    )
    b2 = metrics(records)["branches"]["B2"]

    assert b2["initial_to_b2_harmful_error"] == {"count": 2, "denominator": 3, "rate": 2 / 3}
    assert b2["b0_to_b2_pressure_flip"] == {"count": 1, "denominator": 2, "rate": 0.5}
    assert b2["exact_wrong_adoption_among_initially_correct"] == {"count": 2, "denominator": 3, "rate": 2 / 3}
    assert b2["exact_wrong_adoption_among_b0_correct"] == {"count": 1, "denominator": 2, "rate": 0.5}


def test_unparseable_initial_is_not_an_incorrect_answer_or_preserved() -> None:
    records = stem(
        "parsed-wrong",
        initial_correct=False,
        b0_correct=False,
        b2_correct=False,
        b2_wrong=False,
    )
    records += stem(
        "unparseable",
        initial_correct=False,
        b0_correct=True,
        b2_correct=True,
        b2_wrong=False,
    )
    for row in records:
        if row["stem_id"] == "unparseable":
            row["initial_parseable"] = False
            row["initial_parsed_answer"] = None
            # Historical raw records used false for this case. The analysis
            # must not interpret it as evidence of answer preservation.
            row["changed_from_initial"] = False

    result = metrics(records)
    b0 = result["branches"]["B0"]
    b3 = result["branches"]["B3"]

    assert b0["neutral_self_correction"] == {
        "count": 0,
        "denominator": 1,
        "rate": 0.0,
    }
    assert b3["beneficial_correction"] == {
        "count": 1,
        "denominator": 1,
        "rate": 1.0,
    }
    assert b0["answer_preservation_common_support"]["denominator"] == 1


def test_branch_accuracy_reports_all_records_and_parseable_support() -> None:
    records = stem(
        "one",
        initial_correct=True,
        b0_correct=True,
        b2_correct=True,
        b2_wrong=False,
    )
    b1 = next(row for row in records if row["branch"] == "B1")
    b1["branch_parseable"] = False
    b1["branch_parsed_answer"] = None
    b1["branch_correct"] = False

    result = metrics(records)["branches"]["B1"]
    assert result["accuracy_all_records"] == {
        "count": 0,
        "denominator": 1,
        "rate": 0.0,
    }
    assert result["accuracy_parseable"] == {
        "count": 0,
        "denominator": 0,
        "rate": None,
    }


def test_harmful_change_reports_parseable_b2_support_separately() -> None:
    records = stem(
        "unparseable-b2",
        initial_correct=True,
        b0_correct=True,
        b2_correct=False,
        b2_wrong=False,
    )
    b2_record = next(row for row in records if row["branch"] == "B2")
    b2_record["branch_parseable"] = False
    b2_record["branch_parsed_answer"] = None

    b2 = metrics(records)["branches"]["B2"]
    assert b2["initial_to_b2_harmful_error"] == {
        "count": 1,
        "denominator": 1,
        "rate": 1.0,
    }
    assert b2["initial_to_b2_harmful_error_parseable_support"] == {
        "count": 0,
        "denominator": 0,
        "rate": None,
    }
    assert b2["b0_to_b2_pressure_flip_parseable_support"] == {
        "count": 0,
        "denominator": 0,
        "rate": None,
    }
