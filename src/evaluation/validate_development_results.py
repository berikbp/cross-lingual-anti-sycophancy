from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

from src.evaluation.run_development import (
    BRANCHES,
    build_followups,
)


CONFIG_PATH = Path(
    "configs/evaluation/development_v1.yaml"
)
RESULT_DIRECTORY = Path("results/development_v1")
MANIFEST_ROOT = Path(
    "reports/evaluation_runs/english_development_v1"
)
CONDITIONS = ("base", "control", "anti_sycophancy")
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
        for chunk in iter(
            lambda: file.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)
    return digest.hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]


def main() -> None:
    config = yaml.safe_load(
        CONFIG_PATH.read_text(encoding="utf-8")
    )
    dataset_path = Path(config["dataset"]["path"])
    dataset_records = load_jsonl(dataset_path)
    dataset_by_id = {
        record["stem_id"]: record
        for record in dataset_records
    }
    expected_ids = set(dataset_by_id)
    dataset_sha256 = sha256_file(dataset_path)
    config_sha256 = sha256_file(CONFIG_PATH)
    expected_revision = config["models"]["base"][
        "model_revision"
    ]
    errors: list[str] = []

    for condition in CONDITIONS:
        result_path = RESULT_DIRECTORY / f"{condition}.jsonl"
        manifest_path = (
            MANIFEST_ROOT / condition / "run_manifest.json"
        )
        if not result_path.exists():
            errors.append(f"Missing result file: {result_path}")
            continue
        if not manifest_path.exists():
            errors.append(f"Missing manifest: {manifest_path}")
            continue

        records = load_jsonl(result_path)
        manifest = json.loads(
            manifest_path.read_text(encoding="utf-8")
        )
        pairs = [
            (record.get("stem_id"), record.get("branch"))
            for record in records
        ]
        stem_ids = {record.get("stem_id") for record in records}
        branch_counts = Counter(
            record.get("branch") for record in records
        )

        if len(records) != 400:
            errors.append(
                f"{condition}: expected 400 records, "
                f"found {len(records)}"
            )
        if len(set(pairs)) != 400:
            errors.append(f"{condition}: duplicate result pairs")
        if stem_ids != expected_ids:
            errors.append(f"{condition}: development stem set mismatch")
        if branch_counts != Counter({branch: 100 for branch in BRANCHES}):
            errors.append(
                f"{condition}: branch counts {dict(branch_counts)}"
            )
        if any(
            str(stem_id).startswith("master_")
            for stem_id in stem_ids
        ):
            errors.append(f"{condition}: master-pool stem detected")

        for record in records:
            missing = REQUIRED_FIELDS - record.keys()
            if missing:
                errors.append(
                    f"{condition}/{record.get('stem_id')}/"
                    f"{record.get('branch')}: missing {sorted(missing)}"
                )
                continue
            if record["model_condition"] != condition:
                errors.append(f"{condition}: wrong condition metadata")
            if record["protocol_version"] != "1.0":
                errors.append(f"{condition}: wrong protocol")
            if record["pressure_template_version"] != "v1_weak":
                errors.append(f"{condition}: wrong pressure version")
            if record["evaluation_config_sha256"] != config_sha256:
                errors.append(f"{condition}: config hash mismatch")
            if record["dataset_sha256"] != dataset_sha256:
                errors.append(f"{condition}: dataset hash mismatch")
            if record["model_revision"] != expected_revision:
                errors.append(f"{condition}: model revision mismatch")

            source = dataset_by_id[record["stem_id"]]
            expected_prompt = build_followups(source)[record["branch"]]
            if record["followup_prompt"] != expected_prompt:
                errors.append(
                    f"{condition}/{record['stem_id']}/"
                    f"{record['branch']}: follow-up mismatch"
                )

        for stem_id in expected_ids:
            subset = [
                record
                for record in records
                if record["stem_id"] == stem_id
            ]
            initial_fields = (
                "initial_raw_response",
                "initial_parsed_answer",
                "initial_parseable",
                "initial_correct",
            )
            for field in initial_fields:
                if len({record[field] for record in subset}) != 1:
                    errors.append(
                        f"{condition}/{stem_id}: initial {field} differs"
                    )

        adapter_path_value = config["models"][condition][
            "adapter_path"
        ]
        expected_adapter_sha = None
        if adapter_path_value is not None:
            expected_adapter_sha = sha256_file(
                Path(adapter_path_value)
                / "adapter_model.safetensors"
            )
        if {
            record["adapter_sha256"] for record in records
        } != {expected_adapter_sha}:
            errors.append(f"{condition}: adapter hash mismatch")

        manifest_checks = {
            "condition": condition,
            "dry_run": False,
            "expected_stems": 100,
            "expected_branch_records": 400,
            "dataset_sha256": dataset_sha256,
            "config_sha256": config_sha256,
            "model_revision": expected_revision,
            "adapter_sha256": expected_adapter_sha,
            "output_sha256": sha256_file(result_path),
        }
        for field, expected in manifest_checks.items():
            if manifest.get(field) != expected:
                errors.append(
                    f"{condition} manifest: {field} mismatch"
                )
        if manifest.get("generation") != config["generation"]:
            errors.append(
                f"{condition} manifest: generation settings mismatch"
            )

        print(
            f"{condition}: records={len(records)}, "
            f"stems={len(stem_ids)}, branches={dict(branch_counts)}"
        )

    if errors:
        print("\nDevelopment-result validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("\nDevelopment-result validation passed.")


if __name__ == "__main__":
    main()
