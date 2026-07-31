from __future__ import annotations

import argparse
import gc
import hashlib
import json
import math
import os
import platform
import random
import shutil
import subprocess
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import numpy as np
import torch
import yaml
from datasets import Dataset
from peft import (
    LoraConfig,
    PeftModel,
    get_peft_model,
    prepare_model_for_kbit_training,
)
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    Trainer,
    TrainerCallback,
    TrainingArguments,
    set_seed,
)

from src.training_data.tokenize_final_completion import (
    tokenize_final_assistant_only,
)


Condition = Literal["control_v2", "selective_correction_v2"]

CONFIG_PATH = Path("configs/training/qlora_v2.yaml")
TRANSITION_MANIFEST_PATH = Path(
    "data/training_v2/source/transition_manifest.json"
)
CONVERSATION_MANIFEST_PATH = Path(
    "data/training_v2/conversation_manifest.json"
)

DATA_PATHS: dict[Condition, dict[str, Path]] = {
    "control_v2": {
        "train": Path("data/training_v2/control/train.jsonl"),
        "validation": Path(
            "data/training_v2/control/validation.jsonl"
        ),
    },
    "selective_correction_v2": {
        "train": Path(
            "data/training_v2/selective_correction/train.jsonl"
        ),
        "validation": Path(
            "data/training_v2/selective_correction/validation.jsonl"
        ),
    },
}
OUTPUT_PATHS: dict[Condition, Path] = {
    "control_v2": Path("outputs/adapters/v2/control"),
    "selective_correction_v2": Path(
        "outputs/adapters/v2/selective_correction"
    ),
}
REPORT_PATHS: dict[Condition, Path] = {
    "control_v2": Path("reports/training_runs/v2/control"),
    "selective_correction_v2": Path(
        "reports/training_runs/v2/selective_correction"
    ),
}
CATEGORIES = ("CW", "WC", "CC", "WW")


@dataclass
class FinalCompletionCollator:
    pad_token_id: int

    def __call__(
        self,
        features: list[dict[str, Any]],
    ) -> dict[str, torch.Tensor]:
        maximum_length = max(
            len(feature["input_ids"])
            for feature in features
        )

        input_ids: list[list[int]] = []
        attention_masks: list[list[int]] = []
        labels: list[list[int]] = []

        for feature in features:
            padding_length = (
                maximum_length - len(feature["input_ids"])
            )
            input_ids.append(
                feature["input_ids"]
                + [self.pad_token_id] * padding_length
            )
            attention_masks.append(
                feature["attention_mask"]
                + [0] * padding_length
            )
            labels.append(
                feature["labels"]
                + [-100] * padding_length
            )

        return {
            "input_ids": torch.tensor(
                input_ids,
                dtype=torch.long,
            ),
            "attention_mask": torch.tensor(
                attention_masks,
                dtype=torch.long,
            ),
            "labels": torch.tensor(
                labels,
                dtype=torch.long,
            ),
        }


class MemoryCallback(TrainerCallback):
    def __init__(self) -> None:
        self.peak_allocated_bytes = 0
        self.peak_reserved_bytes = 0

    def on_log(
        self,
        args: TrainingArguments,
        state: Any,
        control: Any,
        logs: dict[str, float] | None = None,
        **kwargs: Any,
    ) -> None:
        del args, state, control, logs, kwargs

        if not torch.cuda.is_available():
            return

        self.peak_allocated_bytes = max(
            self.peak_allocated_bytes,
            torch.cuda.max_memory_allocated(),
        )
        self.peak_reserved_bytes = max(
            self.peak_reserved_bytes,
            torch.cuda.max_memory_reserved(),
        )


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--condition",
        required=True,
        choices=["control_v2", "selective_correction_v2"],
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=CONFIG_PATH,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Train four steps on a balanced eight-record subset.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Delete an existing output directory before training.",
    )
    return parser.parse_args()


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        value = yaml.safe_load(file)

    if not isinstance(value, dict):
        raise ValueError(f"Invalid YAML configuration: {path}")

    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"{path}:{line_number}: {error}"
                ) from error

    return records


def validate_source_records(
    records: list[dict[str, Any]],
    expected_count: int,
    expected_per_category: int,
    label: str,
) -> Counter[str]:
    if len(records) != expected_count:
        raise ValueError(
            f"Expected {expected_count} {label} records, "
            f"found {len(records)}"
        )
    category_counts = Counter(
        record["transition_category"] for record in records
    )
    expected_categories = Counter(
        {
            category: expected_per_category
            for category in CATEGORIES
        }
    )
    if category_counts != expected_categories:
        raise ValueError(
            f"Unexpected {label} category counts: {category_counts}"
        )
    if sum(record["initial_answer_correct"] for record in records) != (
        expected_count // 2
    ):
        raise ValueError(f"{label} initial correctness is not balanced")
    if sum(record["feedback_correct"] for record in records) != (
        expected_count // 2
    ):
        raise ValueError(f"{label} feedback correctness is not balanced")
    for record in records:
        if record["final_answer_option"] != record["correct_option"]:
            raise ValueError(
                f"{record['stem_id']}: final target is incorrect"
            )
    return category_counts


def select_balanced_dry_subset(
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    counts: defaultdict[str, int] = defaultdict(int)
    for record in records:
        category = record["transition_category"]
        if counts[category] < 2:
            selected.append(record)
            counts[category] += 1
        if all(counts[category] == 2 for category in CATEGORIES):
            break
    if len(selected) != 8:
        raise ValueError("Could not construct balanced dry subset.")
    return selected


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(
            lambda: file.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def git_commit() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            text=True,
        ).strip()
    except (
        subprocess.CalledProcessError,
        FileNotFoundError,
    ):
        return None


def select_dtype() -> torch.dtype:
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required.")

    if torch.cuda.is_bf16_supported():
        return torch.bfloat16

    return torch.float16


def configure_reproducibility(seed: int) -> None:
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    set_seed(seed)


def load_tokenizer(
    model_name: str,
    revision: str,
) -> AutoTokenizer:
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        revision=revision,
        use_fast=True,
    )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    tokenizer.padding_side = "right"
    return tokenizer


def load_model(
    config: dict[str, Any],
    compute_dtype: torch.dtype,
) -> AutoModelForCausalLM:
    model_config = config["model"]
    quant_config = config["quantization"]

    bitsandbytes_config = BitsAndBytesConfig(
        load_in_4bit=quant_config["load_in_4bit"],
        bnb_4bit_quant_type=quant_config["quant_type"],
        bnb_4bit_use_double_quant=(
            quant_config["double_quantization"]
        ),
        bnb_4bit_compute_dtype=compute_dtype,
    )

    model = AutoModelForCausalLM.from_pretrained(
        model_config["name"],
        revision=model_config["revision"],
        trust_remote_code=model_config["trust_remote_code"],
        quantization_config=bitsandbytes_config,
        device_map={"": 0},
        dtype=compute_dtype,
    )
    model.config.use_cache = False

    return prepare_model_for_kbit_training(
        model,
        use_gradient_checkpointing=(
            config["training"]["gradient_checkpointing"]
        ),
        gradient_checkpointing_kwargs={
            "use_reentrant": False,
        },
    )


def attach_lora(
    model: AutoModelForCausalLM,
    config: dict[str, Any],
) -> AutoModelForCausalLM:
    lora = config["lora"]
    lora_config = LoraConfig(
        r=lora["rank"],
        lora_alpha=lora["alpha"],
        lora_dropout=lora["dropout"],
        bias=lora["bias"],
        target_modules=lora["target_modules"],
        task_type=lora["task_type"],
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    return model


def tokenize_records(
    tokenizer: AutoTokenizer,
    records: list[dict[str, Any]],
    max_length: int,
) -> Dataset:
    tokenized: list[dict[str, Any]] = []

    for record in records:
        encoded = tokenize_final_assistant_only(
            tokenizer=tokenizer,
            messages=record["messages"],
            max_length=max_length,
        )
        supervised_count = sum(
            label != -100
            for label in encoded["labels"]
        )
        if supervised_count == 0:
            raise RuntimeError(
                f"{record['stem_id']} has no supervised tokens."
            )

        tokenized.append(
            {
                **encoded,
                "stem_id": record["stem_id"],
            }
        )

    return Dataset.from_list(tokenized)


def validate_tokenized_dataset(
    train_dataset: Dataset,
    validation_dataset: Dataset,
    max_length: int,
) -> dict[str, dict[str, float | int]]:
    statistics: dict[str, dict[str, float | int]] = {}

    for label, dataset in (
        ("train", train_dataset),
        ("validation", validation_dataset),
    ):
        lengths = [
            len(record["input_ids"])
            for record in dataset
        ]
        supervised_lengths = [
            sum(
                token != -100
                for token in record["labels"]
            )
            for record in dataset
        ]

        if not lengths:
            raise ValueError(f"Empty {label} dataset.")
        if max(lengths) > max_length:
            raise ValueError(
                f"{label} contains a sequence longer than "
                f"{max_length}."
            )
        if min(supervised_lengths) <= 0:
            raise ValueError(
                f"{label} contains an empty target."
            )

        statistics[label] = {
            "count": len(dataset),
            "min_length": min(lengths),
            "max_length": max(lengths),
            "mean_length": sum(lengths) / len(lengths),
            "mean_supervised_tokens": (
                sum(supervised_lengths)
                / len(supervised_lengths)
            ),
        }
        print(f"{label}: {statistics[label]}")

    return statistics


def create_training_arguments(
    output_dir: Path,
    config: dict[str, Any],
    compute_dtype: torch.dtype,
    dry_run: bool,
) -> TrainingArguments:
    training = config["training"]
    reproducibility = config["reproducibility"]
    common = {
        "output_dir": str(output_dir),
        "per_device_train_batch_size": 1,
        "per_device_eval_batch_size": 1,
        "learning_rate": training["learning_rate"],
        "bf16": compute_dtype == torch.bfloat16,
        "fp16": compute_dtype == torch.float16,
        "optim": training["optimizer"],
        "gradient_checkpointing": (
            training["gradient_checkpointing"]
        ),
        "gradient_checkpointing_kwargs": {
            "use_reentrant": False,
        },
        "report_to": "none",
        "remove_unused_columns": False,
        "seed": reproducibility["seed"],
        "data_seed": reproducibility["data_seed"],
    }

    if dry_run:
        return TrainingArguments(
            **common,
            max_steps=4,
            gradient_accumulation_steps=1,
            logging_steps=1,
            save_strategy="no",
            eval_strategy="no",
        )

    return TrainingArguments(
        **common,
        num_train_epochs=training["epochs"],
        gradient_accumulation_steps=(
            training["gradient_accumulation_steps"]
        ),
        weight_decay=training["weight_decay"],
        warmup_ratio=training["warmup_ratio"],
        lr_scheduler_type=training["lr_scheduler_type"],
        max_grad_norm=training["max_grad_norm"],
        logging_steps=training["logging_steps"],
        eval_strategy=training["eval_strategy"],
        save_strategy=training["save_strategy"],
        save_total_limit=training["save_total_limit"],
        load_best_model_at_end=False,
    )


def save_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            value,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def last_logged_value(
    history: list[dict[str, Any]],
    field: str,
) -> float | None:
    for record in reversed(history):
        if field in record:
            return float(record[field])
    return None


def main() -> None:
    arguments = parse_arguments()
    condition: Condition = arguments.condition
    config = load_yaml(arguments.config)
    training = config["training"]
    model_config = config["model"]
    reproducibility = config["reproducibility"]

    if config["selection"]["checkpoint_rule"] != "final_checkpoint":
        raise ValueError("Checkpoint rule must be final_checkpoint.")
    if config["selection"]["use_validation_for_checkpoint_selection"]:
        raise ValueError("Validation checkpoint selection must be disabled.")

    output_dir = OUTPUT_PATHS[condition]
    report_dir = REPORT_PATHS[condition]
    if arguments.dry_run:
        output_dir = output_dir.with_name(output_dir.name + "_dry_run")
        report_dir = report_dir.with_name(report_dir.name + "_dry_run")

    if output_dir.exists():
        if not arguments.overwrite:
            raise FileExistsError(
                f"{output_dir} already exists. Use --overwrite "
                "only for an intentional rerun."
            )
        shutil.rmtree(output_dir)

    if report_dir.exists():
        if not arguments.overwrite:
            raise FileExistsError(
                f"{report_dir} already exists. Use --overwrite "
                "only for an intentional rerun."
            )
        shutil.rmtree(report_dir)

    configure_reproducibility(reproducibility["seed"])
    train_path = DATA_PATHS[condition]["train"]
    validation_path = DATA_PATHS[condition]["validation"]
    train_records = load_jsonl(train_path)
    validation_records = load_jsonl(validation_path)

    validate_source_records(
        train_records,
        expected_count=1000,
        expected_per_category=250,
        label="training",
    )
    validate_source_records(
        validation_records,
        expected_count=100,
        expected_per_category=25,
        label="validation",
    )

    if arguments.dry_run:
        train_records = select_balanced_dry_subset(train_records)
        validation_records = select_balanced_dry_subset(
            validation_records
        )

    run_category_counts = Counter(
        record["transition_category"] for record in train_records
    )
    run_validation_category_counts = Counter(
        record["transition_category"] for record in validation_records
    )

    expected_train = 8 if arguments.dry_run else 1000
    expected_validation = 8 if arguments.dry_run else 100
    if len(train_records) != expected_train:
        raise ValueError(
            f"Expected {expected_train} train records, "
            f"found {len(train_records)}"
        )
    if len(validation_records) != expected_validation:
        raise ValueError(
            f"Expected {expected_validation} validation records, "
            f"found {len(validation_records)}"
        )

    compute_dtype = select_dtype()
    tokenizer = load_tokenizer(
        model_name=model_config["name"],
        revision=model_config["revision"],
    )
    train_dataset = tokenize_records(
        tokenizer=tokenizer,
        records=train_records,
        max_length=training["max_length"],
    )
    validation_dataset = tokenize_records(
        tokenizer=tokenizer,
        records=validation_records,
        max_length=training["max_length"],
    )
    token_statistics = validate_tokenized_dataset(
        train_dataset,
        validation_dataset,
        max_length=training["max_length"],
    )

    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats()
    model = attach_lora(
        model=load_model(config, compute_dtype),
        config=config,
    )
    memory_callback = MemoryCallback()
    training_arguments = create_training_arguments(
        output_dir=output_dir,
        config=config,
        compute_dtype=compute_dtype,
        dry_run=arguments.dry_run,
    )
    trainer = Trainer(
        model=model,
        args=training_arguments,
        train_dataset=train_dataset,
        eval_dataset=validation_dataset,
        data_collator=FinalCompletionCollator(
            pad_token_id=tokenizer.pad_token_id
        ),
        callbacks=[memory_callback],
    )

    started = time.time()
    train_result = trainer.train()
    runtime_seconds = time.time() - started

    final_dir = output_dir / "final"
    final_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(final_dir)
    tokenizer.save_pretrained(final_dir)
    trainer.save_state()

    base_model = model.unload()
    model = PeftModel.from_pretrained(
        base_model,
        final_dir,
        is_trainable=False,
    )
    model.eval()
    reload_verified = True

    log_history = trainer.state.log_history
    save_json(
        report_dir / "trainer_log_history.json",
        log_history,
    )
    effective_batch_size = (
        training_arguments.per_device_train_batch_size
        * training_arguments.gradient_accumulation_steps
    )
    expected_global_steps = (
        4
        if arguments.dry_run
        else math.ceil(1000 / effective_batch_size)
        * training["epochs"]
    )
    if trainer.state.global_step != expected_global_steps:
        raise RuntimeError(
            f"Expected {expected_global_steps} global steps, "
            f"found {trainer.state.global_step}."
        )

    run_manifest = {
        "experiment_version": "v2",
        "condition": condition,
        "dry_run": arguments.dry_run,
        "protocol_version": config["protocol"]["version"],
        "training_config_version": (
            config["protocol"]["training_config_version"]
        ),
        "model_name": model_config["name"],
        "model_revision": model_config["revision"],
        "config_path": str(arguments.config),
        "config_sha256": sha256_file(arguments.config),
        "transition_manifest_sha256": sha256_file(
            TRANSITION_MANIFEST_PATH
        ),
        "conversation_manifest_sha256": sha256_file(
            CONVERSATION_MANIFEST_PATH
        ),
        "train_path": str(train_path),
        "train_sha256": sha256_file(train_path),
        "validation_path": str(validation_path),
        "validation_sha256": sha256_file(validation_path),
        "train_count": len(train_records),
        "validation_count": len(validation_records),
        "category_counts": dict(run_category_counts),
        "validation_category_counts": dict(
            run_validation_category_counts
        ),
        "initial_correct_count": sum(
            record["initial_answer_correct"]
            for record in train_records
        ),
        "feedback_correct_count": sum(
            record["feedback_correct"] for record in train_records
        ),
        "epochs": training_arguments.num_train_epochs,
        "effective_batch_size": effective_batch_size,
        "expected_global_steps": expected_global_steps,
        "seed": reproducibility["seed"],
        "data_seed": reproducibility["data_seed"],
        "compute_dtype": str(compute_dtype),
        "torch_version": torch.__version__,
        "transformers_version": __import__(
            "transformers"
        ).__version__,
        "python_version": sys.version,
        "platform": platform.platform(),
        "cuda_version": torch.version.cuda,
        "gpu_name": torch.cuda.get_device_name(0),
        "runtime_seconds": runtime_seconds,
        "global_step": trainer.state.global_step,
        "final_training_loss": last_logged_value(
            log_history,
            "train_loss",
        ),
        "final_validation_loss": last_logged_value(
            log_history,
            "eval_loss",
        ),
        "train_metrics": train_result.metrics,
        "token_statistics": token_statistics,
        "peak_allocated_gb": (
            torch.cuda.max_memory_allocated() / 1024**3
        ),
        "peak_reserved_gb": (
            torch.cuda.max_memory_reserved() / 1024**3
        ),
        "callback_peak_allocated_gb": (
            memory_callback.peak_allocated_bytes / 1024**3
        ),
        "callback_peak_reserved_gb": (
            memory_callback.peak_reserved_bytes / 1024**3
        ),
        "git_commit": git_commit(),
        "final_adapter_path": str(final_dir),
        "final_adapter_sha256": sha256_file(
            final_dir / "adapter_model.safetensors"
        ),
        "adapter_reload_verified": reload_verified,
    }
    save_json(
        report_dir / "run_manifest.json",
        run_manifest,
    )

    print("\nTraining completed")
    print("=" * 60)
    print(f"Condition: {condition}")
    print(f"Global step: {trainer.state.global_step}")
    print(f"Runtime: {runtime_seconds:.2f} seconds")
    print(
        "Peak allocated memory: "
        f"{run_manifest['peak_allocated_gb']:.2f} GB"
    )
    print(
        "Peak reserved memory: "
        f"{run_manifest['peak_reserved_gb']:.2f} GB"
    )
    print(f"Final adapter: {final_dir}")
    print(f"Run manifest: {report_dir / 'run_manifest.json'}")

    del trainer
    del model
    gc.collect()
    torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
