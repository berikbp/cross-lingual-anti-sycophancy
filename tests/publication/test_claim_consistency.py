from __future__ import annotations

import json
import tomllib
from pathlib import Path

import pytest
import yaml


def test_primary_effects_match_frozen_analysis_and_public_table() -> None:
    paired = json.loads(
        Path("reports/final_analysis/paired_effects.json").read_text(
            encoding="utf-8"
        )
    )
    expected = {
        "en": (0.006666666666666667, -0.006666666666666667, 0.02),
        "ru": (-0.0033333333333333335, -0.016666666666666666, 0.01),
        "kk": (-0.016666666666666666, -0.05, 0.02),
    }
    for language, (mean, low, high) in expected.items():
        assert paired[language]["mean"] == pytest.approx(mean)
        assert paired[language]["ci_95"] == pytest.approx([low, high])

    table = Path("paper/tables/main_results.md").read_text(encoding="utf-8")
    assert "| English | 1.7 pp | 1.0 pp | +0.7 pp | [-0.7, 2.0] |" in table
    assert "| Russian | 1.7 pp | 2.0 pp | -0.3 pp | [-1.7, 1.0] |" in table
    assert "Historical original-translation result" in table


def test_correction_denominators_match_parseable_support() -> None:
    transitions = json.loads(
        Path("reports/final_analysis/transition_metrics.json").read_text(
            encoding="utf-8"
        )
    )
    expected = {
        "control_v2_en": (5, 19),
        "selective_correction_v2_en": (4, 19),
        "control_v2_ru": (1, 13),
        "selective_correction_v2_ru": (1, 9),
        "control_v2_kk": (34, 54),
        "selective_correction_v2_kk": (31, 49),
    }
    for condition, (count, denominator) in expected.items():
        value = transitions[condition]["branches"]["B3"][
            "beneficial_correction"
        ]
        assert (value["count"], value["denominator"]) == (
            count,
            denominator,
        )

    public_text = "\n".join(
        Path(path).read_text(encoding="utf-8")
        for path in (
            "README.md",
            "paper/paper.md",
            "paper/tables/main_results.md",
            "paper/claims_and_evidence.md",
            "reports/final_project_report.md",
        )
    )
    for stale in ("5/20", "33/46", "19/31", "89/111", "68/91"):
        assert stale not in public_text
    assert "macro-average was -0.4" not in public_text


def test_secondary_table_matches_regenerated_transition_metrics() -> None:
    transitions = json.loads(
        Path("reports/final_analysis/transition_metrics.json").read_text(
            encoding="utf-8"
        )
    )
    table = Path("paper/tables/main_results.md").read_text(encoding="utf-8")
    labels = {
        "control_v2_en": "Control-v2 EN",
        "selective_correction_v2_en": "Selective-v2 EN",
        "control_v2_ru": "Control-v2 RU",
        "selective_correction_v2_ru": "Selective-v2 RU",
        "control_v2_kk": "Control-v2 KK*",
        "selective_correction_v2_kk": "Selective-v2 KK*",
    }
    for key, label in labels.items():
        b2 = transitions[key]["branches"]["B2"]
        b3 = transitions[key]["branches"]["B3"]
        values = (
            b2["initial_to_b2_harmful_error"],
            b2["b0_to_b2_pressure_flip"],
            b2["exact_wrong_adoption_among_initially_correct"],
            b2["exact_wrong_adoption_among_b0_correct"],
            b3["beneficial_correction"],
            b3["stubbornness"],
        )
        cells = " | ".join(
            f"{value['count']}/{value['denominator']}" for value in values
        )
        assert f"| {label} | {cells} |" in table


def test_release_versions_and_licenses_are_consistent() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    citation = yaml.safe_load(Path("CITATION.cff").read_text(encoding="utf-8"))
    zenodo = json.loads(Path(".zenodo.json").read_text(encoding="utf-8"))
    assert pyproject["project"]["version"] == "1.1.2"
    assert str(citation["version"]) == "1.1.2"
    assert zenodo["license"] == "mit"
    assert Path("LICENSE").exists()
    assert Path("DATA_LICENSE.md").exists()
    assert Path("MODEL_ARTIFACT_LICENSE.md").exists()


def test_public_release_wording_and_artifact_links_are_current() -> None:
    public = "\n".join(
        Path(path).read_text(encoding="utf-8")
        for path in (
            "README.md",
            "paper/paper.md",
            "docs/artifact_inventory.md",
            "reports/publication_audit_v1_0.md",
        )
    )
    assert "release candidate" not in public.casefold()
    assert "1.1.2-adapters.tar.gz" in public
    assert "1.1.2-raw-results.tar.gz" in public


def test_original_kazakh_claim_is_qualified_everywhere_public() -> None:
    for path in (
        "README.md",
        "paper/paper.md",
        "paper/claims_and_evidence.md",
        "reports/final_project_report.md",
    ):
        text = Path(path).read_text(encoding="utf-8").casefold()
        assert "kazakh" in text
        assert "translation" in text
    audit_manifest = json.loads(
        Path("data/final/multilingual_manifest_audit_v1_1.json").read_text(
            encoding="utf-8"
        )
    )
    assert audit_manifest["kazakh_semantic_review_established"] is False
    assert audit_manifest["historical_artifacts_modified"] is False


def test_release_figures_exist() -> None:
    for filename in (
        "experimental_pipeline.svg",
        "v1_v2_capability_recovery.svg",
        "paired_effect_forest.svg",
    ):
        path = Path("paper/figures") / filename
        assert path.exists() and path.stat().st_size > 500


def test_bundle_checksums_are_portable() -> None:
    script = Path("scripts/build_zenodo_bundles.sh").read_text(
        encoding="utf-8"
    )
    assert 'source_name="$(basename "$source_archive")"' in script
    assert 'results_name="$(basename "$results_archive")"' in script
    assert 'adapter_name="$(basename "$adapter_archive")"' in script
    assert "  cd dist\n" in script
