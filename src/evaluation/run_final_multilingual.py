from __future__ import annotations

import argparse
import gc
import hashlib
import json
import platform
import random
import re
import subprocess
import time
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
import torch
import yaml
from peft import PeftModel
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    set_seed,
)


BRANCHES = ("B0", "B1", "B2", "B3")
DEFAULT_CONFIG = Path("configs/evaluation/final_multilingual_v1.yaml")
DEFAULT_PROMPTS = Path(
    "configs/evaluation/prompts_final_multilingual_v1.json"
)
ALLOWED_EVALUATIONS = {
    "final_multilingual_v1": {
        language: Path(f"data/final/test_{language}.jsonl").resolve()
        for language in ("en", "ru", "kk")
    },
    "corrected_kazakh_v2": {
        "kk": Path("data/final/test_kk_v2.jsonl").resolve(),
    },
}
EXPECTED_GENERATION = {
    "do_sample": False,
    "temperature": 0.0,
    "max_new_tokens": 32,
    "repetition_penalty": 1.0,
}
REQUIRED_PROMPT_KEYS = {
    "system",
    "B0",
    "B1",
    "B2_template",
    "B3_template",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def parse_answer(text: str) -> str | None:
    try:
        value = json.loads(text.strip()).get("answer")
        if value in {"A", "B", "C", "D"}:
            return value
    except (json.JSONDecodeError, AttributeError):
        pass
    matches = re.findall(r'"answer"\s*:\s*"([ABCD])"', text, re.I)
    return matches[0].upper() if len(matches) == 1 else None


def git_commit() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True
        ).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--condition",
        required=True,
        choices=["base", "control_v2", "selective_correction_v2"],
    )
    parser.add_argument("--language", required=True, choices=["en", "ru", "kk"])
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--prompts", type=Path, default=DEFAULT_PROMPTS)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def output_path(
    condition: str,
    language: str,
    *,
    dry_run: bool,
    explicit: Path | None,
    evaluation_name: str = "final_multilingual_v1",
) -> Path:
    if explicit is not None:
        return explicit
    root = (
        Path(f"results/{evaluation_name}_dry")
        if dry_run
        else Path(f"results/{evaluation_name}")
    )
    return root / f"{condition}_{language}.jsonl"


def load_model(name: str, revision: str, adapter: Path | None):
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for the locked final evaluator.")
    dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    quantization = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=dtype,
    )
    tokenizer = AutoTokenizer.from_pretrained(
        adapter or name,
        revision=None if adapter else revision,
        use_fast=True,
    )
    model = AutoModelForCausalLM.from_pretrained(
        name,
        revision=revision,
        quantization_config=quantization,
        device_map={"": 0},
        dtype=dtype,
    )
    if adapter:
        model = PeftModel.from_pretrained(model, adapter)
    model.eval()
    return tokenizer, model, str(dtype)


def generate(tokenizer, model, messages, generation: dict[str, Any]) -> str:
    formatted = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(formatted, return_tensors="pt").to(model.device)
    with torch.inference_mode():
        generated = model.generate(
            **inputs,
            do_sample=False,
            max_new_tokens=generation["max_new_tokens"],
            repetition_penalty=generation["repetition_penalty"],
            pad_token_id=tokenizer.eos_token_id,
        )
    output = generated[0, inputs["input_ids"].shape[1] :]
    return tokenizer.decode(output, skip_special_tokens=True).strip()


def format_question(record: dict[str, Any]) -> str:
    options = record["options"]
    return (
        f"{record['question']}\n\n"
        f"A. {options['A']}\n"
        f"B. {options['B']}\n"
        f"C. {options['C']}\n"
        f"D. {options['D']}"
    )


def followups(
    record: dict[str, Any], prompt_config: dict[str, str]
) -> dict[str, str]:
    options = record["options"]
    return {
        "B0": prompt_config["B0"],
        "B1": prompt_config["B1"],
        "B2": prompt_config["B2_template"].replace(
            "{suggestion_text}",
            options[record["wrong_suggestion_option"]],
        ),
        "B3": prompt_config["B3_template"].replace(
            "{suggestion_text}", options[record["correct_option"]]
        ),
    }


def validate_locked_configuration(configuration: dict[str, Any]) -> None:
    if tuple(configuration.get("branches", ())) != BRANCHES:
        raise ValueError("Frozen branch list or ordering changed.")
    if configuration.get("generation") != EXPECTED_GENERATION:
        raise ValueError("Frozen generation configuration changed.")
    revisions = {
        model["model_revision"]
        for model in configuration.get("models", {}).values()
    }
    names = {
        model["model_name"]
        for model in configuration.get("models", {}).values()
    }
    if len(revisions) != 1 or len(names) != 1:
        raise ValueError("Model name or revision is not matched across runs.")


def main() -> None:
    arguments = parse_arguments()
    if arguments.dry_run != (arguments.limit is not None):
        raise ValueError("Use --dry-run and --limit together.")
    if arguments.limit is not None and arguments.limit <= 0:
        raise ValueError("--limit must be positive.")
    if arguments.output is not None and not arguments.dry_run:
        raise ValueError("--output is allowed only for isolated dry runs.")

    configuration = yaml.safe_load(
        arguments.config.read_text(encoding="utf-8")
    )
    validate_locked_configuration(configuration)
    language = arguments.language
    evaluation_name = configuration["protocol"]["evaluation_name"]
    if evaluation_name not in ALLOWED_EVALUATIONS:
        raise RuntimeError(f"Evaluation not allowlisted: {evaluation_name}")
    if language not in ALLOWED_EVALUATIONS[evaluation_name]:
        raise RuntimeError(
            f"Language {language} is not allowed for {evaluation_name}."
        )
    configured_dataset = Path(configuration["datasets"][language]["path"])
    resolved_dataset = configured_dataset.resolve()
    if resolved_dataset != ALLOWED_EVALUATIONS[evaluation_name][language]:
        raise RuntimeError(f"Dataset not allowed: {resolved_dataset}")

    records = load_jsonl(resolved_dataset)
    expected_records = configuration["datasets"][language]["expected_records"]
    if len(records) != expected_records:
        raise ValueError(
            f"Expected {expected_records} records, found {len(records)}"
        )
    if arguments.limit is not None:
        records = records[: arguments.limit]

    destination = output_path(
        arguments.condition,
        language,
        dry_run=arguments.dry_run,
        explicit=arguments.output,
        evaluation_name=evaluation_name,
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise FileExistsError(f"Refusing to overwrite: {destination}")

    all_prompts = json.loads(arguments.prompts.read_text(encoding="utf-8"))
    prompt_config = all_prompts[language]
    if set(prompt_config) != REQUIRED_PROMPT_KEYS:
        raise ValueError("Frozen prompt keys changed or are incomplete.")
    model_config = configuration["models"][arguments.condition]
    adapter = (
        Path(model_config["adapter_path"])
        if model_config.get("adapter_path")
        else None
    )

    seed = int(configuration.get("reproducibility", {}).get("seed", 42))
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    set_seed(seed)

    started_at = datetime.now(UTC)
    start_time = time.time()
    tokenizer, model, compute_dtype = load_model(
        model_config["model_name"], model_config["model_revision"], adapter
    )
    results: list[dict[str, Any]] = []
    generation = configuration["generation"]
    config_hash = sha256_file(arguments.config)
    prompt_hash = sha256_file(arguments.prompts)
    adapter_hash = (
        sha256_file(adapter / "adapter_model.safetensors")
        if adapter
        else None
    )

    for record_index, record in enumerate(records, start=1):
        initial_messages = [
            {"role": "system", "content": prompt_config["system"]},
            {"role": "user", "content": format_question(record)},
        ]
        initial_raw = generate(
            tokenizer, model, initial_messages, generation
        )
        initial = parse_answer(initial_raw)
        common_state = [
            *initial_messages,
            {"role": "assistant", "content": initial_raw},
        ]
        branch_prompts = followups(record, prompt_config)

        for branch in BRANCHES:
            branch_messages = [
                *deepcopy(common_state),
                {"role": "user", "content": branch_prompts[branch]},
            ]
            raw = generate(tokenizer, model, branch_messages, generation)
            parsed = parse_answer(raw)
            results.append(
                {
                    "protocol_version": configuration["protocol"]["version"],
                    "evaluation_name": configuration["protocol"][
                        "evaluation_name"
                    ],
                    "pressure_template_version": configuration["protocol"][
                        "pressure_template_version"
                    ],
                    "language": language,
                    "model_condition": arguments.condition,
                    "model_name": model_config["model_name"],
                    "model_revision": model_config["model_revision"],
                    "adapter_path": model_config.get("adapter_path"),
                    "adapter_sha256": adapter_hash,
                    "dataset_path": configured_dataset.as_posix(),
                    "dataset_sha256": sha256_file(resolved_dataset),
                    "evaluation_config_path": arguments.config.as_posix(),
                    "evaluation_config_sha256": config_hash,
                    "prompt_config_path": arguments.prompts.as_posix(),
                    "prompt_config_sha256": prompt_hash,
                    "generation": generation,
                    "stem_id": record["stem_id"],
                    "domain": record["domain"],
                    "difficulty": record["difficulty"],
                    "correct_option": record["correct_option"],
                    "wrong_suggestion_option": record[
                        "wrong_suggestion_option"
                    ],
                    "branch": branch,
                    "initial_raw_response": initial_raw,
                    "initial_parsed_answer": initial,
                    "initial_parseable": initial is not None,
                    "initial_correct": initial == record["correct_option"],
                    "followup_prompt": branch_prompts[branch],
                    "branch_raw_response": raw,
                    "branch_parsed_answer": parsed,
                    "branch_parseable": parsed is not None,
                    "branch_correct": parsed == record["correct_option"],
                    "changed_from_initial": (
                        None
                        if initial is None or parsed is None
                        else initial != parsed
                    ),
                    "exact_wrong_adoption": (
                        branch == "B2"
                        and parsed == record["wrong_suggestion_option"]
                    ),
                }
            )

        if record_index % 10 == 0 or record_index == len(records):
            print(
                f"{arguments.condition}/{language}: "
                f"{record_index}/{len(records)} stems",
                flush=True,
            )

    temporary = destination.with_suffix(destination.suffix + ".tmp")
    temporary.write_text(
        "\n".join(json.dumps(item, ensure_ascii=False) for item in results)
        + "\n",
        encoding="utf-8",
    )
    temporary.replace(destination)

    finished_at = datetime.now(UTC)
    manifest = {
        "condition": arguments.condition,
        "language": language,
        "model_name": model_config["model_name"],
        "model_revision": model_config["model_revision"],
        "adapter_path": model_config.get("adapter_path"),
        "adapter_sha256": adapter_hash,
        "dataset_path": configured_dataset.as_posix(),
        "dataset_sha256": sha256_file(resolved_dataset),
        "prompt_config_path": arguments.prompts.as_posix(),
        "prompt_config_sha256": prompt_hash,
        "evaluation_config_path": arguments.config.as_posix(),
        "evaluation_config_sha256": config_hash,
        "generation": generation,
        "seed": seed,
        "output_path": destination.as_posix(),
        "output_sha256": sha256_file(destination),
        "record_count": len(results),
        "stem_count": len(records),
        "dry_run": arguments.dry_run,
        "git_commit": git_commit(),
        "started_at_utc": started_at.isoformat(),
        "finished_at_utc": finished_at.isoformat(),
        "runtime_seconds": time.time() - start_time,
        "compute_dtype": compute_dtype,
        "gpu_name": torch.cuda.get_device_name(0),
        "torch_version": torch.__version__,
        "cuda_version": torch.version.cuda,
        "python_version": platform.python_version(),
        "parseable_initials": len(
            {r["stem_id"] for r in results if r["initial_parseable"]}
        ),
        "parseable_branches": sum(r["branch_parseable"] for r in results),
    }
    manifest_root = (
        Path(f"reports/evaluation_runs/{evaluation_name}_dry")
        if arguments.dry_run
        else Path(f"reports/evaluation_runs/{evaluation_name}")
    )
    manifest_path = (
        manifest_root
        / arguments.condition
        / language
        / "run_manifest.json"
    )
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    del model
    gc.collect()
    torch.cuda.empty_cache()
    print(f"Saved {len(results)} records to {destination}")


if __name__ == "__main__":
    main()
