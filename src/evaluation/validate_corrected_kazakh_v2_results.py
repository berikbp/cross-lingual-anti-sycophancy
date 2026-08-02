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


CONFIG = Path("configs/evaluation/corrected_kazakh_v2.yaml")
PROMPTS = Path("configs/evaluation/prompts_corrected_kazakh_v2.json")
DATASET = Path("data/final/test_kk_v2.jsonl")
DATASET_MANIFEST = Path("data/final/kazakh_v2_manifest.json")
ENGLISH_SOURCE = Path("data/final/test_en.jsonl")
ROOT = Path("results/corrected_kazakh_v2")
RUN_ROOT = Path("reports/evaluation_runs/corrected_kazakh_v2")
HASH_OUTPUT = Path("docs/corrected_kazakh_v2_result_hashes.txt")
REPORT = RUN_ROOT / "validation.json"
CONDITIONS = ("base", "control_v2", "selective_correction_v2")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def adapter_hashes() -> dict[str, str]:
    result: dict[str, str] = {}
    for line in Path("docs/trained_v2_adapter_hashes.txt").read_text(
        encoding="utf-8"
    ).splitlines():
        digest, path = line.split(maxsplit=1)
        if path.endswith("control/final/adapter_model.safetensors"):
            result["control_v2"] = digest
        elif path.endswith(
            "selective_correction/final/adapter_model.safetensors"
        ):
            result["selective_correction_v2"] = digest
    return result


def main() -> None:
    configuration = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    prompts = json.loads(PROMPTS.read_text(encoding="utf-8"))["kk"]
    manifest = json.loads(DATASET_MANIFEST.read_text(encoding="utf-8"))
    if manifest["author_review_complete"] is not True:
        raise ValueError("Corrected Kazakh author review is not complete.")
    if sha256(DATASET) != manifest["kazakh_sha256"]:
        raise ValueError("Corrected Kazakh dataset hash mismatch.")
    if sha256(ENGLISH_SOURCE) != manifest["english_sha256"]:
        raise ValueError("Frozen English source hash mismatch.")
    if manifest.get("historical_kazakh_results_replaced") is not False:
        raise ValueError("Historical Kazakh results must not be replaced.")

    source = load_jsonl(DATASET)
    if len(source) != 300:
        raise ValueError("Corrected Kazakh dataset must have 300 records.")
    source_by_id = {record["stem_id"]: record for record in source}
    canonical_keys = [
        (record["stem_id"], branch)
        for record in source
        for branch in BRANCHES
    ]
    config_hash = sha256(CONFIG)
    prompt_hash = sha256(PROMPTS)
    dataset_hash = sha256(DATASET)
    adapters = adapter_hashes()
    report: dict[str, Any] = {"files": {}}
    hash_lines: list[str] = []

    for condition in CONDITIONS:
        model = configuration["models"][condition]
        path = ROOT / f"{condition}_kk.jsonl"
        records = load_jsonl(path)
        keys = [(record["stem_id"], record["branch"]) for record in records]
        if len(records) != 1200 or keys != canonical_keys:
            raise ValueError(f"{path}: incomplete or incorrectly ordered records")
        if len(set(keys)) != 1200:
            raise ValueError(f"{path}: duplicate keys")
        if Counter(record["branch"] for record in records) != {
            branch: 300 for branch in BRANCHES
        }:
            raise ValueError(f"{path}: branch imbalance")

        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        expected_adapter = adapters.get(condition)
        for record in records:
            item = source_by_id[record["stem_id"]]
            expected = {
                "protocol_version": "2.1",
                "evaluation_name": "corrected_kazakh_v2",
                "pressure_template_version": (
                    "v1_weak_kazakh_language_revision"
                ),
                "language": "kk",
                "model_condition": condition,
                "model_name": model["model_name"],
                "model_revision": model["model_revision"],
                "adapter_path": model.get("adapter_path"),
                "adapter_sha256": expected_adapter,
                "dataset_path": DATASET.as_posix(),
                "dataset_sha256": dataset_hash,
                "evaluation_config_path": CONFIG.as_posix(),
                "evaluation_config_sha256": config_hash,
                "prompt_config_path": PROMPTS.as_posix(),
                "prompt_config_sha256": prompt_hash,
                "generation": configuration["generation"],
            }
            for field, value in expected.items():
                if record.get(field) != value:
                    raise ValueError(f"{path}: {field} mismatch")
            for field in (
                "domain",
                "difficulty",
                "correct_option",
                "wrong_suggestion_option",
            ):
                if record[field] != item[field]:
                    raise ValueError(f"{path}: {record['stem_id']} {field} mismatch")
            initial = parse_answer(record["initial_raw_response"])
            branch = parse_answer(record["branch_raw_response"])
            checks = (
                record["initial_parsed_answer"] == initial,
                record["initial_parseable"] == (initial is not None),
                record["initial_correct"] == (initial == item["correct_option"]),
                record["branch_parsed_answer"] == branch,
                record["branch_parseable"] == (branch is not None),
                record["branch_correct"] == (branch == item["correct_option"]),
                record["changed_from_initial"]
                == (None if initial is None or branch is None else initial != branch),
                record["exact_wrong_adoption"]
                == (
                    record["branch"] == "B2"
                    and branch == item["wrong_suggestion_option"]
                ),
                record["followup_prompt"]
                == followups(item, prompts)[record["branch"]],
            )
            if not all(checks):
                raise ValueError(f"{path}: derived-field mismatch")
            grouped[record["stem_id"]].append(record)

        for stem_id, subset in grouped.items():
            initial_states = {
                (
                    record["initial_raw_response"],
                    record["initial_parsed_answer"],
                )
                for record in subset
            }
            if len(initial_states) != 1:
                raise ValueError(f"{path}: {stem_id} initial branch mismatch")

        result_hash = sha256(path)
        manifest_path = RUN_ROOT / condition / "kk" / "run_manifest.json"
        run_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        expected_manifest = {
            "condition": condition,
            "language": "kk",
            "model_name": model["model_name"],
            "model_revision": model["model_revision"],
            "adapter_path": model.get("adapter_path"),
            "adapter_sha256": expected_adapter,
            "dataset_path": DATASET.as_posix(),
            "dataset_sha256": dataset_hash,
            "prompt_config_path": PROMPTS.as_posix(),
            "prompt_config_sha256": prompt_hash,
            "evaluation_config_path": CONFIG.as_posix(),
            "evaluation_config_sha256": config_hash,
            "generation": configuration["generation"],
            "seed": configuration["reproducibility"]["seed"],
            "output_path": path.as_posix(),
            "output_sha256": result_hash,
            "record_count": 1200,
            "stem_count": 300,
            "dry_run": False,
        }
        for field, expected_value in expected_manifest.items():
            if run_manifest.get(field) != expected_value:
                raise ValueError(f"{manifest_path}: {field} mismatch")
        report["files"][condition] = {
            "path": path.as_posix(),
            "sha256": result_hash,
            "records": len(records),
            "manifest": manifest_path.as_posix(),
        }
        hash_lines.append(f"{result_hash}  {path}")

    report.update(
        {
            "records": 3600,
            "dataset_sha256": dataset_hash,
            "prompt_sha256": prompt_hash,
            "config_sha256": config_hash,
            "validation_passed": True,
        }
    )
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    HASH_OUTPUT.write_text("\n".join(hash_lines) + "\n", encoding="utf-8")
    print("Corrected Kazakh v2 result validation passed.")


if __name__ == "__main__":
    main()
