from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tomllib
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]

CORE_FILES = (
    "LICENSE",
    "DATA_LICENSE.md",
    "APACHE-2.0.txt",
    "MODEL_ARTIFACT_LICENSE.md",
    "CITATION.cff",
    ".zenodo.json",
    "README.md",
    "CHANGELOG.md",
    "paper/paper.md",
    "docs/reproducibility.md",
    "docs/artifact_inventory.md",
    "reports/publication_audit_v1_0.md",
)

PUBLICATION_GATE_FILES = (
    "data/final/test_kk_v2.jsonl",
    "data/final/kazakh_v2_manifest.json",
    "docs/kazakh_v2_artifact_hashes.txt",
    "docs/corrected_kazakh_v2_result_hashes.txt",
    "docs/corrected_kazakh_v2_analysis_hashes.txt",
    "reports/corrected_kazakh_v2_analysis.md",
    "reports/corrected_kazakh_v2_metrics.json",
    "reports/evaluation_runs/corrected_kazakh_v2/validation.json",
    "reports/evaluation_runs/corrected_kazakh_v2/base/kk/run_manifest.json",
    "reports/evaluation_runs/corrected_kazakh_v2/control_v2/kk/run_manifest.json",
    "reports/evaluation_runs/corrected_kazakh_v2/selective_correction_v2/kk/run_manifest.json",
)
PUBLIC_CLAIM_FILES = (
    "README.md",
    "paper/paper.md",
    "paper/claims_and_evidence.md",
    "reports/final_project_report.md",
)

EXTERNAL_ARTIFACTS = (
    "outputs/adapters/v2/control/final/adapter_model.safetensors",
    "outputs/adapters/v2/selective_correction/final/adapter_model.safetensors",
    "results/final_multilingual_v1/base_en.jsonl",
    "results/final_multilingual_v1/base_ru.jsonl",
    "results/final_multilingual_v1/base_kk.jsonl",
    "results/final_multilingual_v1/control_v2_en.jsonl",
    "results/final_multilingual_v1/control_v2_ru.jsonl",
    "results/final_multilingual_v1/control_v2_kk.jsonl",
    "results/final_multilingual_v1/selective_correction_v2_en.jsonl",
    "results/final_multilingual_v1/selective_correction_v2_ru.jsonl",
    "results/final_multilingual_v1/selective_correction_v2_kk.jsonl",
    "results/corrected_kazakh_v2/base_kk.jsonl",
    "results/corrected_kazakh_v2/control_v2_kk.jsonl",
    "results/corrected_kazakh_v2/selective_correction_v2_kk.jsonl",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_hash_file(relative: str) -> list[str]:
    path = ROOT / relative
    if not path.exists():
        return [f"missing hash file: {relative}"]
    failures: list[str] = []
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        try:
            expected, target = line.split(maxsplit=1)
        except ValueError:
            failures.append(f"{relative}:{line_number}: malformed hash line")
            continue
        target_path = ROOT / target.strip()
        if not target_path.exists():
            failures.append(f"{relative}: missing target {target.strip()}")
        elif sha256(target_path) != expected:
            failures.append(f"{relative}: hash mismatch {target.strip()}")
    return failures


def run(command: list[str]) -> tuple[int, str]:
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return result.returncode, result.stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--core-only",
        action="store_true",
        help="Check metadata without requiring the corrected-evaluation gate.",
    )
    arguments = parser.parse_args()
    failures: list[str] = []
    warnings: list[str] = []

    for relative in CORE_FILES:
        if not (ROOT / relative).exists():
            failures.append(f"missing core file: {relative}")

    pyproject: dict[str, Any] = tomllib.loads(
        (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    )
    citation = yaml.safe_load(
        (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    )
    zenodo = json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))
    version = pyproject["project"]["version"]
    if str(citation["version"]) != version:
        failures.append("CITATION.cff and pyproject.toml versions differ")
    if str(zenodo.get("version")) != version:
        failures.append(".zenodo.json and pyproject.toml versions differ")
    if not zenodo.get("creators"):
        failures.append(".zenodo.json has no creators")

    release_text = "\n".join(
        (ROOT / relative).read_text(encoding="utf-8")
        for relative in (
            "README.md",
            "CHANGELOG.md",
            "paper/paper.md",
            "docs/artifact_inventory.md",
            "reports/publication_audit_v1_0.md",
        )
    )
    if "release candidate" in release_text.casefold():
        failures.append("public files still contain release-candidate wording")
    for archive_name in ("raw-results", "adapters"):
        expected_asset = f"{version}-{archive_name}.tar.gz"
        if expected_asset not in release_text:
            failures.append(f"public artifact link missing: {expected_asset}")

    for hash_file in (
        "docs/training_v2_dataset_hashes.txt",
        "docs/trained_v2_adapter_hashes.txt",
        "docs/final_multilingual_artifact_hashes.txt",
        "docs/final_multilingual_result_hashes.txt",
        "docs/final_analysis_hashes.txt",
    ):
        failures.extend(check_hash_file(hash_file))

    for relative in EXTERNAL_ARTIFACTS:
        if not (ROOT / relative).exists():
            failures.append(f"missing external artifact: {relative}")

    if not arguments.core_only:
        if not citation.get("date-released"):
            failures.append(
                "CITATION.cff: add the actual date-released before publication"
            )
        for relative in PUBLICATION_GATE_FILES:
            if not (ROOT / relative).exists():
                failures.append(f"publication gate incomplete: {relative}")
        if all((ROOT / path).exists() for path in PUBLICATION_GATE_FILES):
            failures.extend(check_hash_file("docs/kazakh_v2_artifact_hashes.txt"))
            failures.extend(
                check_hash_file("docs/corrected_kazakh_v2_result_hashes.txt")
            )
            failures.extend(
                check_hash_file("docs/corrected_kazakh_v2_analysis_hashes.txt")
            )
            pending_markers = (
                "being prepared",
                "sensitivity evaluation are pending",
                "pending a corrected",
                "cannot be frozen until",
                "remains to be run",
                "must still be completed",
                "not yet publication-ready",
            )
            for relative in PUBLIC_CLAIM_FILES:
                public_text = (ROOT / relative).read_text(
                    encoding="utf-8"
                ).casefold()
                if "corrected_kazakh_v2" not in public_text:
                    failures.append(
                        f"{relative}: corrected Kazakh analysis not linked"
                    )
                if any(marker in public_text for marker in pending_markers):
                    failures.append(
                        f"{relative}: still describes corrected analysis as pending"
                    )

    status_code, status = run(["git", "status", "--porcelain"])
    if status_code or status:
        message = "Git worktree is not clean; release only after commit."
        if arguments.core_only:
            warnings.append(message)
        else:
            failures.append(message)
    release_tag = f"v{version}"
    tag_code, _ = run(
        ["git", "rev-parse", "-q", "--verify", f"refs/tags/{release_tag}"]
    )
    if tag_code == 0:
        warnings.append(
            f"{release_tag} already exists; do not move a published tag."
        )

    for warning in warnings:
        print(f"WARN: {warning}")
    for failure in failures:
        print(f"FAIL: {failure}")
    if failures:
        print(f"Zenodo readiness: NOT READY ({len(failures)} blocking checks)")
        raise SystemExit(1)
    print("Zenodo readiness: PASS")


if __name__ == "__main__":
    main()
