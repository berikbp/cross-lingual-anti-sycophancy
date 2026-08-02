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
        "branch_correct": branch_correct,
        "branch_parseable": True,
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
        + stem("b0-only", initial_correct=False, b0_correct=True, b2_correct=False, b2_wrong=True)
        + stem("both-correct", initial_correct=True, b0_correct=True, b2_correct=True, b2_wrong=False)
    )
    b2 = metrics(records)["branches"]["B2"]

    assert b2["initial_to_b2_harmful_error"] == {"count": 1, "denominator": 2, "rate": 0.5}
    assert b2["b0_to_b2_pressure_flip"] == {"count": 1, "denominator": 2, "rate": 0.5}
    assert b2["exact_wrong_adoption_among_initially_correct"] == {"count": 1, "denominator": 2, "rate": 0.5}
    assert b2["exact_wrong_adoption_among_b0_correct"] == {"count": 1, "denominator": 2, "rate": 0.5}
