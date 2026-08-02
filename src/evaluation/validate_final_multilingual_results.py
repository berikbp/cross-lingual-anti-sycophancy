from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml

from src.evaluation.run_final_multilingual import (
    BRANCHES,
    followups,
    parse_answer,
)


CONFIG_PATH = Path("configs/evaluation/final_multilingual_v1.yaml")
PROMPT_PATH = Path("configs/evaluation/prompts_final_multilingual_v1.json")
RESULT_ROOT = Path("results/final_multilingual_v1")
RUN_ROOT = Path("reports/evaluation_runs/final_multilingual_v1")
RESULT_HASH_PATH = Path("docs/final_multilingual_result_hashes.txt")
FINAL_ARTIFACT_HASH_PATH = Path(
    "docs/final_multilingual_artifact_hashes.txt"
)
ADAPTER_HASH_PATH = Path("docs/trained_v2_adapter_hashes.txt")
REPORT_PATH = RUN_ROOT / "provenance_validation.json"
CONDITIONS = ("base", "control_v2", "selective_correction_v2")
LANGUAGES = ("en", "ru", "kk")

REQUIRED_FIELDS = {
    "protocol_version",
    "evaluation_name",
    "pressure_template_version",
    "model_condition",
    "model_name",
    "model_revision",
    "adapter_path",
    "adapter_sha256",
    "dataset_path",
    "dataset_sha256",
    "prompt_config_sha256",
    "stem_id",
    "domain",
    "difficulty",
    "correct_option",
    "wrong_suggestion_option",
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
    "exact_wrong_adoption",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise ValueError(f"{path}:{line_number}: {error}") from error
    return records


def load_hashes(path: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, filename = line.split(maxsplit=1)
        hashes[filename.strip()] = digest
    return hashes


def adapter_hashes() -> dict[str, str]:
    hashes = load_hashes(ADAPTER_HASH_PATH)
    return {
        "control_v2": hashes[
            "outputs/adapters/v2/control/final/adapter_model.safetensors"
        ],
        "selective_correction_v2": hashes[
            "outputs/adapters/v2/selective_correction/final/adapter_model.safetensors"
        ],
    }


def validate_record(
    record: dict[str, Any],
    *,
    source: dict[str, Any],
    condition: str,
    language: str,
    model_config: dict[str, Any],
    prompt_config: dict[str, str],
    dataset_path: Path,
    dataset_hash: str,
    prompt_hash: str,
    expected_adapter_hash: str | None,
) -> None:
    missing = REQUIRED_FIELDS - set(record)
    if missing:
        raise ValueError(
            f"{condition}/{language}/{source['stem_id']}: missing {sorted(missing)}"
        )
    if record["model_condition"] != condition:
        raise ValueError("Model-condition metadata mismatch")
    if record["model_name"] != model_config["model_name"]:
        raise ValueError("Model-name metadata mismatch")
    if record["model_revision"] != model_config["model_revision"]:
        raise ValueError("Model-revision metadata mismatch")
    if record["adapter_path"] != model_config.get("adapter_path"):
        raise ValueError("Adapter-path metadata mismatch")
    if record["adapter_sha256"] != expected_adapter_hash:
        raise ValueError("Adapter hash mismatch")
    if Path(record["dataset_path"]).resolve() != dataset_path.resolve():
        raise ValueError("Dataset-path metadata mismatch")
    if record["dataset_sha256"] != dataset_hash:
        raise ValueError("Dataset hash mismatch")
    if record["prompt_config_sha256"] != prompt_hash:
        raise ValueError("Prompt hash mismatch")
    if record["protocol_version"] != "2.0":
        raise ValueError("Protocol version mismatch")
    if record["evaluation_name"] != "final_multilingual_v1":
        raise ValueError("Evaluation name mismatch")
    if record["pressure_template_version"] != "v1_weak":
        raise ValueError("Pressure-template version mismatch")

    for field in (
        "stem_id",
        "domain",
        "difficulty",
        "correct_option",
        "wrong_suggestion_option",
    ):
        if record[field] != source[field]:
            raise ValueError(
                f"{condition}/{language}/{source['stem_id']}: {field} mismatch"
            )

    initial = parse_answer(record["initial_raw_response"])
    branch_answer = parse_answer(record["branch_raw_response"])
    if record["initial_parsed_answer"] != initial:
        raise ValueError("Initial parsed answer mismatch")
    if record["initial_parseable"] != (initial is not None):
        raise ValueError("Initial parseability mismatch")
    if record["initial_correct"] != (initial == source["correct_option"]):
        raise ValueError("Initial correctness mismatch")
    if record["branch_parsed_answer"] != branch_answer:
        raise ValueError("Branch parsed answer mismatch")
    if record["branch_parseable"] != (branch_answer is not None):
        raise ValueError("Branch parseability mismatch")
    if record["branch_correct"] != (branch_answer == source["correct_option"]):
        raise ValueError("Branch correctness mismatch")

    expected_changed = (
        initial is not None
        and branch_answer is not None
        and initial != branch_answer
    )
    if record["changed_from_initial"] != expected_changed:
        raise ValueError("Historical changed-from-initial field mismatch")
    expected_wrong_adoption = (
        record["branch"] == "B2"
        and branch_answer == source["wrong_suggestion_option"]
    )
    if record["exact_wrong_adoption"] != expected_wrong_adoption:
        raise ValueError("Exact-wrong-adoption mismatch")
    expected_followup = followups(source, prompt_config)[record["branch"]]
    if record["followup_prompt"] != expected_followup:
        raise ValueError("Frozen follow-up prompt mismatch")


def main() -> None:
    frozen_artifact_hashes = load_hashes(FINAL_ARTIFACT_HASH_PATH)
    for path in (
        CONFIG_PATH,
        PROMPT_PATH,
        Path("data/final/test_en.jsonl"),
        Path("data/final/test_ru.jsonl"),
        Path("data/final/test_kk.jsonl"),
        Path("data/final/multilingual_manifest.json"),
    ):
        expected = frozen_artifact_hashes.get(path.as_posix())
        if expected is None or sha256_file(path) != expected:
            raise ValueError(f"{path}: frozen artifact hash mismatch")

    configuration = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    prompts = load_json(PROMPT_PATH)
    prompt_hash = sha256_file(PROMPT_PATH)
    result_hashes = load_hashes(RESULT_HASH_PATH)
    expected_adapter_hashes = adapter_hashes()
    datasets = {
        language: load_jsonl(Path(configuration["datasets"][language]["path"]))
        for language in LANGUAGES
    }
    dataset_by_id = {
        language: {record["stem_id"]: record for record in records}
        for language, records in datasets.items()
    }
    canonical_ids = [record["stem_id"] for record in datasets["en"]]
    if len(canonical_ids) != 300 or len(set(canonical_ids)) != 300:
        raise ValueError("English final dataset is not 300 unique stems")
    for language in LANGUAGES:
        if [record["stem_id"] for record in datasets[language]] != canonical_ids:
            raise ValueError(f"{language}: canonical ordering mismatch")

    report: dict[str, Any] = {
        "validator_version": "final_multilingual_provenance_v2",
        "historical_raw_schema": True,
        "historical_limitations": [
            "raw records store absolute dataset paths",
            "generation settings are frozen in configuration but not embedded in historical records",
            "historical manifests do not contain every current provenance field",
        ],
        "evaluation_config_path": CONFIG_PATH.as_posix(),
        "evaluation_config_sha256": sha256_file(CONFIG_PATH),
        "prompt_config_path": PROMPT_PATH.as_posix(),
        "prompt_config_sha256": prompt_hash,
        "files": {},
    }
    total = 0
    reference_keys: list[tuple[str, str]] | None = None

    for condition in CONDITIONS:
        model_config = configuration["models"][condition]
        expected_adapter_hash = expected_adapter_hashes.get(condition)
        for language in LANGUAGES:
            result_path = RESULT_ROOT / f"{condition}_{language}.jsonl"
            expected_result_hash = result_hashes[result_path.as_posix()]
            actual_result_hash = sha256_file(result_path)
            if actual_result_hash != expected_result_hash:
                raise ValueError(f"{result_path}: frozen result hash mismatch")

            records = load_jsonl(result_path)
            if len(records) != 1200:
                raise ValueError(f"{result_path}: expected 1200 records")
            keys = [(record["stem_id"], record["branch"]) for record in records]
            expected_keys = [
                (stem_id, branch)
                for stem_id in canonical_ids
                for branch in BRANCHES
            ]
            if keys != expected_keys:
                raise ValueError(f"{result_path}: canonical key ordering mismatch")
            if reference_keys is None:
                reference_keys = keys
            elif keys != reference_keys:
                raise ValueError(f"{result_path}: cross-condition key mismatch")
            if len(set(keys)) != 1200:
                raise ValueError(f"{result_path}: duplicate keys")
            if Counter(record["branch"] for record in records) != {
                branch: 300 for branch in BRANCHES
            }:
                raise ValueError(f"{result_path}: branch imbalance")

            grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
            dataset_path = Path(configuration["datasets"][language]["path"])
            dataset_hash = sha256_file(dataset_path)
            for record in records:
                source = dataset_by_id[language][record["stem_id"]]
                validate_record(
                    record,
                    source=source,
                    condition=condition,
                    language=language,
                    model_config=model_config,
                    prompt_config=prompts[language],
                    dataset_path=dataset_path,
                    dataset_hash=dataset_hash,
                    prompt_hash=prompt_hash,
                    expected_adapter_hash=expected_adapter_hash,
                )
                grouped[record["stem_id"]].append(record)
            for stem_id, subset in grouped.items():
                if {record["branch"] for record in subset} != set(BRANCHES):
                    raise ValueError(f"{result_path}/{stem_id}: incomplete branches")
                initial_fields = {
                    (
                        record["initial_raw_response"],
                        record["initial_parsed_answer"],
                        record["initial_parseable"],
                        record["initial_correct"],
                    )
                    for record in subset
                }
                if len(initial_fields) != 1:
                    raise ValueError(f"{result_path}/{stem_id}: initial mismatch")

            manifest_path = RUN_ROOT / condition / language / "run_manifest.json"
            manifest = load_json(manifest_path)
            manifest_checks = {
                "condition": condition,
                "language": language,
                "model_revision": model_config["model_revision"],
                "dataset_sha256": dataset_hash,
                "prompt_config_sha256": prompt_hash,
                "output_sha256": actual_result_hash,
                "record_count": 1200,
                "dry_run": False,
            }
            for field, expected in manifest_checks.items():
                if manifest.get(field) != expected:
                    raise ValueError(
                        f"{manifest_path}: {field} does not match frozen run"
                    )

            parseable_initials = len(
                {
                    record["stem_id"]
                    for record in records
                    if record["initial_parseable"]
                }
            )
            parseable_branches = sum(
                record["branch_parseable"] for record in records
            )
            report["files"][f"{condition}_{language}"] = {
                "path": result_path.as_posix(),
                "sha256": actual_result_hash,
                "records": 1200,
                "stems": 300,
                "parseable_initials": parseable_initials,
                "parseable_branches": parseable_branches,
                "manifest_path": manifest_path.as_posix(),
                "manifest_validated": True,
            }
            total += len(records)

    if total != 10800:
        raise ValueError(f"Expected 10800 records, found {total}")
    report["total_records"] = total
    report["validation_passed"] = True
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("Final multilingual result and provenance validation passed.")
    print(f"Validated records: {total}")
    print(f"Report: {REPORT_PATH}")


if __name__ == "__main__":
    main()
