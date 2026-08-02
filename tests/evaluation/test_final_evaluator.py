from __future__ import annotations

from pathlib import Path

import pytest

from src.evaluation.run_final_multilingual import (
    EXPECTED_GENERATION,
    followups,
    output_path,
    validate_locked_configuration,
)


def test_dry_run_uses_isolated_output_root() -> None:
    assert output_path(
        "base", "en", dry_run=True, explicit=None
    ) == Path("results/final_multilingual_v1_dry/base_en.jsonl")
    assert output_path(
        "base", "en", dry_run=False, explicit=None
    ) == Path("results/final_multilingual_v1/base_en.jsonl")


def test_explicit_output_takes_precedence() -> None:
    destination = Path("/tmp/final-evaluator-test.jsonl")
    assert (
        output_path("base", "en", dry_run=True, explicit=destination)
        == destination
    )


def test_corrected_kazakh_uses_a_separate_result_root() -> None:
    assert output_path(
        "base",
        "kk",
        dry_run=False,
        explicit=None,
        evaluation_name="corrected_kazakh_v2",
    ) == Path("results/corrected_kazakh_v2/base_kk.jsonl")


def test_followups_insert_only_frozen_option_text() -> None:
    record = {
        "options": {"A": "alpha", "B": "beta", "C": "gamma", "D": "delta"},
        "correct_option": "C",
        "wrong_suggestion_option": "B",
    }
    prompts = {
        "B0": "neutral",
        "B1": "doubt",
        "B2_template": "wrong: {suggestion_text}",
        "B3_template": "correct: {suggestion_text}",
    }
    result = followups(record, prompts)
    assert result == {
        "B0": "neutral",
        "B1": "doubt",
        "B2": "wrong: beta",
        "B3": "correct: gamma",
    }


def test_locked_configuration_rejects_generation_or_branch_changes() -> None:
    configuration = {
        "branches": ["B0", "B1", "B2", "B3"],
        "generation": dict(EXPECTED_GENERATION),
        "models": {
            "base": {"model_name": "model", "model_revision": "sha"},
            "control_v2": {
                "model_name": "model",
                "model_revision": "sha",
            },
        },
    }
    validate_locked_configuration(configuration)

    changed_generation = {
        **configuration,
        "generation": {**EXPECTED_GENERATION, "do_sample": True},
    }
    with pytest.raises(ValueError, match="generation"):
        validate_locked_configuration(changed_generation)

    changed_branches = {**configuration, "branches": ["B0", "B2"]}
    with pytest.raises(ValueError, match="branch"):
        validate_locked_configuration(changed_branches)
