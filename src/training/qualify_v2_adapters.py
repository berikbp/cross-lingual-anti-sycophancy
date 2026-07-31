from __future__ import annotations

import gc
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import torch
import yaml
from peft import PeftModel
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)


CONFIG_PATH = Path("configs/training/qlora_v2.yaml")
CONDITIONS = {
    "control_v2": {
        "adapter": Path("outputs/adapters/v2/control/final"),
        "validation": Path(
            "data/training_v2/control/validation.jsonl"
        ),
    },
    "selective_correction_v2": {
        "adapter": Path(
            "outputs/adapters/v2/selective_correction/final"
        ),
        "validation": Path(
            "data/training_v2/selective_correction/validation.jsonl"
        ),
    },
}
CATEGORIES = ("CW", "WC", "CC", "WW")
OUTPUT_PATH = Path("results/adapter_qualification_v2/results.jsonl")
REPORT_PATH = Path("reports/adapter_qualification_v2.md")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_answer(text: str) -> str | None:
    try:
        value = json.loads(text.strip())
        answer = value.get("answer")
        if answer in {"A", "B", "C", "D"}:
            return answer
    except (json.JSONDecodeError, AttributeError):
        pass
    matches = re.findall(
        r'"answer"\s*:\s*"([ABCD])"', text, flags=re.IGNORECASE
    )
    return matches[0].upper() if len(matches) == 1 else None


def load_balanced_subset(path: Path) -> list[dict[str, Any]]:
    records = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    selected: list[dict[str, Any]] = []
    counts: defaultdict[str, int] = defaultdict(int)
    for record in records:
        category = record["transition_category"]
        if counts[category] < 2:
            selected.append(record)
            counts[category] += 1
        if all(counts[category] == 2 for category in CATEGORIES):
            break
    if Counter(record["transition_category"] for record in selected) != (
        Counter({category: 2 for category in CATEGORIES})
    ):
        raise ValueError(f"Could not select a balanced subset from {path}")
    return selected


def main() -> None:
    config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    model_name = config["model"]["name"]
    revision = config["model"]["revision"]
    compute_dtype = (
        torch.bfloat16
        if torch.cuda.is_bf16_supported()
        else torch.float16
    )
    quantization = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=compute_dtype,
    )
    results: list[dict[str, Any]] = []

    for condition, paths in CONDITIONS.items():
        adapter_path = paths["adapter"]
        weights = adapter_path / "adapter_model.safetensors"
        if not weights.exists():
            raise FileNotFoundError(f"Missing adapter weights: {weights}")
        tokenizer = AutoTokenizer.from_pretrained(
            adapter_path, use_fast=True
        )
        base_model = AutoModelForCausalLM.from_pretrained(
            model_name,
            revision=revision,
            quantization_config=quantization,
            device_map={"": 0},
            dtype=compute_dtype,
        )
        model = PeftModel.from_pretrained(base_model, adapter_path)
        model.eval()

        for record in load_balanced_subset(paths["validation"]):
            context = record["messages"][:-1]
            formatted = tokenizer.apply_chat_template(
                context,
                tokenize=False,
                add_generation_prompt=True,
            )
            inputs = tokenizer(formatted, return_tensors="pt").to(
                model.device
            )
            with torch.inference_mode():
                generated = model.generate(
                    **inputs,
                    do_sample=False,
                    max_new_tokens=32,
                    pad_token_id=tokenizer.eos_token_id,
                )
            output_tokens = generated[
                0, inputs["input_ids"].shape[1] :
            ]
            raw = tokenizer.decode(
                output_tokens, skip_special_tokens=True
            ).strip()
            parsed = parse_answer(raw)
            correct = parsed == record["correct_option"]
            changed = (
                parsed is not None
                and parsed != record["initial_answer_option"]
            )
            should_change = not record["initial_answer_correct"]
            results.append(
                {
                    "condition": condition,
                    "stem_id": record["stem_id"],
                    "transition_category": record[
                        "transition_category"
                    ],
                    "initial_answer": record["initial_answer_option"],
                    "feedback_answer": record["feedback_option"],
                    "correct_answer": record["correct_option"],
                    "raw_response": raw,
                    "parsed_answer": parsed,
                    "parseable": parsed is not None,
                    "final_correct": correct,
                    "changed": changed,
                    "expected_transition": (
                        correct and changed == should_change
                    ),
                }
            )

        del model
        del base_model
        gc.collect()
        torch.cuda.empty_cache()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        for result in results:
            file.write(json.dumps(result, ensure_ascii=False) + "\n")

    lines = [
        "# V2 Adapter Qualification",
        "",
        "This is an engineering reload and transition check on eight frozen SFT-validation conversations per adapter. It is not evidence of generalization.",
        "",
        "| Adapter | CW | WC | CC | WW | Parseable | Correct |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for condition, paths in CONDITIONS.items():
        subset = [r for r in results if r["condition"] == condition]
        category_values = []
        for category in CATEGORIES:
            category_subset = [
                r
                for r in subset
                if r["transition_category"] == category
            ]
            category_values.append(
                f"{sum(r['expected_transition'] for r in category_subset)}/2"
            )
        parseable = sum(r["parseable"] for r in subset)
        correct = sum(r["final_correct"] for r in subset)
        label = (
            "Control-v2"
            if condition == "control_v2"
            else "Selective-v2"
        )
        lines.append(
            f"| {label} | {' | '.join(category_values)} | "
            f"{parseable}/8 | {correct}/8 |"
        )
        print(
            f"{condition}: parseable={parseable}/8, correct={correct}/8"
        )
    lines.extend(
        [
            "",
            f"- Base model: `{model_name}`",
            f"- Revision: `{revision}`",
            "- Subset rule: first two validation examples per transition category",
            "- Generation: deterministic",
            "",
            "## Adapter hashes",
            "",
        ]
    )
    for condition, paths in CONDITIONS.items():
        weights = paths["adapter"] / "adapter_model.safetensors"
        lines.append(f"- {condition}: `{sha256_file(weights)}`")
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Results: {OUTPUT_PATH}")
    print(f"Report: {REPORT_PATH}")


if __name__ == "__main__":
    main()
