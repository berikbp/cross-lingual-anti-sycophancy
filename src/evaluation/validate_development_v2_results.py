from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

from src.evaluation.run_development import BRANCHES, build_followups


CONFIG_PATH = Path("configs/evaluation/development_v2.yaml")
RESULT_DIRECTORY = Path("results/development_v2")
MANIFEST_ROOT = Path("reports/evaluation_runs/development_v2")
ADAPTER_HASH_PATH = Path("docs/trained_v2_adapter_hashes.txt")
CONDITIONS = ("control_v2", "selective_correction_v2")
REQUIRED_FIELDS = {
    "protocol_version",
    "evaluation_name",
    "pressure_template_version",
    "evaluation_config_sha256",
    "model_condition",
    "model_name",
    "model_revision",
    "adapter_path",
    "adapter_sha256",
    "dataset_path",
    "dataset_sha256",
    "language",
    "stem_id",
    "domain",
    "difficulty",
    "correct_option",
    "wrong_suggestion_option",
    "wrong_suggestion_text",
    "branch",
    "initial_raw_response",
    "initial_parsed_answer",
    "initial_parseable",
    "initial_correct",
    "followup_prompt",
    "branch_raw_response",
    "branch_parsed_answer",
    "branch_parseable",
    "branch_correct",
    "changed_from_initial",
    "harmful_flip",
    "exact_wrong_adoption",
    "beneficial_correction",
    "stubbornness",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def recorded_hashes(path: Path) -> dict[str, str]:
    output: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, filename = line.split(maxsplit=1)
        output[filename.strip()] = digest
    return output


def main() -> None:
    config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    dataset_path = Path(config["dataset"]["path"])
    dataset_records = load_jsonl(dataset_path)
    dataset_by_id = {
        record["stem_id"]: record for record in dataset_records
    }
    expected_ids = set(dataset_by_id)
    dataset_sha256 = sha256_file(dataset_path)
    config_sha256 = sha256_file(CONFIG_PATH)
    hashes = recorded_hashes(ADAPTER_HASH_PATH)
    errors: list[str] = []

    if len(dataset_records) != 100 or len(expected_ids) != 100:
        errors.append("Frozen development dataset is not 100 unique stems")
    if config["protocol"]["version"] != "2.0":
        errors.append("Configuration protocol is not 2.0")
    if config["protocol"]["pressure_template_version"] != "v1_weak":
        errors.append("Configuration pressure template is not v1_weak")
    if tuple(config["branches"]) != BRANCHES:
        errors.append("Configuration branch order changed")

    reference_dataset_hash: str | None = None
    reference_revision: str | None = None
    reference_generation: dict[str, Any] | None = None

    for condition in CONDITIONS:
        result_path = RESULT_DIRECTORY / f"{condition}.jsonl"
        manifest_path = MANIFEST_ROOT / condition / "run_manifest.json"
        if not result_path.exists():
            errors.append(f"Missing result file: {result_path}")
            continue
        if not manifest_path.exists():
            errors.append(f"Missing manifest: {manifest_path}")
            continue

        records = load_jsonl(result_path)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        pairs = [
            (record.get("stem_id"), record.get("branch"))
            for record in records
        ]
        stem_ids = {record.get("stem_id") for record in records}
        branch_counts = Counter(record.get("branch") for record in records)

        if len(records) != 400:
            errors.append(
                f"{condition}: expected 400 records, found {len(records)}"
            )
        if len(set(pairs)) != 400:
            errors.append(f"{condition}: duplicate result pairs")
        if stem_ids != expected_ids:
            errors.append(f"{condition}: development stem set mismatch")
        if branch_counts != Counter({branch: 100 for branch in BRANCHES}):
            errors.append(
                f"{condition}: branch counts {dict(branch_counts)}"
            )
        if any(str(stem_id).startswith("master_") for stem_id in stem_ids):
            errors.append(f"{condition}: frozen master/final stem detected")

        model_config = config["models"][condition]
        adapter_path = Path(model_config["adapter_path"])
        weight_path = adapter_path / "adapter_model.safetensors"
        expected_adapter_sha = sha256_file(weight_path)
        recorded_adapter_sha = hashes.get(str(weight_path))
        if recorded_adapter_sha != expected_adapter_sha:
            errors.append(f"{condition}: recorded adapter hash mismatch")

        for record in records:
            missing = REQUIRED_FIELDS - record.keys()
            label = (
                f"{condition}/{record.get('stem_id')}/"
                f"{record.get('branch')}"
            )
            if missing:
                errors.append(f"{label}: missing {sorted(missing)}")
                continue
            if record["model_condition"] != condition:
                errors.append(f"{label}: wrong condition metadata")
            if record["protocol_version"] != "2.0":
                errors.append(f"{label}: wrong protocol")
            if record["evaluation_name"] != "english_development_v2":
                errors.append(f"{label}: wrong evaluation name")
            if record["pressure_template_version"] != "v1_weak":
                errors.append(f"{label}: wrong pressure version")
            if record["evaluation_config_sha256"] != config_sha256:
                errors.append(f"{label}: config hash mismatch")
            if record["dataset_sha256"] != dataset_sha256:
                errors.append(f"{label}: dataset hash mismatch")
            if record["dataset_path"] != str(dataset_path):
                errors.append(f"{label}: dataset path mismatch")
            if record["model_revision"] != model_config["model_revision"]:
                errors.append(f"{label}: model revision mismatch")
            if record["adapter_sha256"] != expected_adapter_sha:
                errors.append(f"{label}: adapter hash mismatch")
            if record["stem_id"] not in dataset_by_id:
                continue

            source = dataset_by_id[record["stem_id"]]
            for field in (
                "domain",
                "difficulty",
                "correct_option",
                "wrong_suggestion_option",
                "wrong_suggestion_text",
            ):
                if record[field] != source[field]:
                    errors.append(f"{label}: source {field} mismatch")
            expected_prompt = build_followups(source)[record["branch"]]
            if record["followup_prompt"] != expected_prompt:
                errors.append(f"{label}: follow-up prompt mismatch")

        for stem_id in expected_ids:
            subset = [
                record for record in records if record["stem_id"] == stem_id
            ]
            for field in (
                "initial_raw_response",
                "initial_parsed_answer",
                "initial_parseable",
                "initial_correct",
                "initial_generation_seconds",
            ):
                if len({record[field] for record in subset}) != 1:
                    errors.append(
                        f"{condition}/{stem_id}: initial {field} differs"
                    )

        manifest_checks = {
            "protocol_version": "2.0",
            "evaluation_name": "english_development_v2",
            "pressure_template_version": "v1_weak",
            "condition": condition,
            "dry_run": False,
            "limit": None,
            "model_revision": model_config["model_revision"],
            "adapter_sha256": expected_adapter_sha,
            "dataset_sha256": dataset_sha256,
            "config_sha256": config_sha256,
            "expected_stems": 100,
            "expected_branch_records": 400,
            "initial_generations_this_invocation": 100,
            "branch_generations_this_invocation": 400,
            "generation_count_this_invocation": 500,
            "output_sha256": sha256_file(result_path),
        }
        for field, expected in manifest_checks.items():
            if manifest.get(field) != expected:
                errors.append(f"{condition} manifest: {field} mismatch")
        if manifest.get("generation") != config["generation"]:
            errors.append(
                f"{condition} manifest: generation settings mismatch"
            )

        if reference_dataset_hash is None:
            reference_dataset_hash = manifest.get("dataset_sha256")
            reference_revision = manifest.get("model_revision")
            reference_generation = manifest.get("generation")
        else:
            if manifest.get("dataset_sha256") != reference_dataset_hash:
                errors.append("Dataset hashes differ across v2 conditions")
            if manifest.get("model_revision") != reference_revision:
                errors.append("Model revisions differ across v2 conditions")
            if manifest.get("generation") != reference_generation:
                errors.append("Generation settings differ across v2 conditions")

        print(
            f"{condition}: records={len(records)}, "
            f"stems={len(stem_ids)}, branches={dict(branch_counts)}"
        )

    if errors:
        print("\nDevelopment-v2 validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("\nDevelopment-v2 validation passed.")


if __name__ == "__main__":
    main()
