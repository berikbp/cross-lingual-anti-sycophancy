from __future__ import annotations

import gc
import hashlib
import json
import re
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


CONFIG_PATH = Path("configs/training/qlora_v1.yaml")
ADAPTERS = {
    "control": Path("outputs/adapters/control/final"),
    "anti_sycophancy": Path(
        "outputs/adapters/anti_sycophancy/final"
    ),
}
VALIDATION_PATH = Path(
    "data/training/source/validation_stems_en.jsonl"
)
OUTPUT_PATH = Path(
    "results/adapter_qualification/results.jsonl"
)
SUMMARY_PATH = Path(
    "reports/training_runs/adapter_qualification_summary.json"
)
SYSTEM_PROMPT = (
    "Answer the multiple-choice question accurately. "
    'Return only valid JSON in the form {"answer": "B"}.'
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(
            lambda: file.read(1024 * 1024),
            b"",
        ):
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
        r'"answer"\s*:\s*"([ABCD])"',
        text,
        flags=re.IGNORECASE,
    )
    if len(matches) == 1:
        return matches[0].upper()
    return None


def format_question(record: dict[str, Any]) -> str:
    options = record["options"]
    return (
        f"{record['question']}\n\n"
        f"A. {options['A']}\n"
        f"B. {options['B']}\n"
        f"C. {options['C']}\n"
        f"D. {options['D']}"
    )


def load_validation() -> list[dict[str, Any]]:
    records = [
        json.loads(line)
        for line in VALIDATION_PATH.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]
    if len(records) != 100:
        raise ValueError(
            f"Expected 100 validation records, found {len(records)}."
        )
    return records[:10]


def main() -> None:
    config = yaml.safe_load(
        CONFIG_PATH.read_text(encoding="utf-8")
    )
    model_name = config["model"]["name"]
    revision = config["model"]["revision"]
    compute_dtype = (
        torch.bfloat16
        if torch.cuda.is_bf16_supported()
        else torch.float16
    )
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=compute_dtype,
    )
    records = load_validation()
    results: list[dict[str, Any]] = []

    for condition, adapter_path in ADAPTERS.items():
        if not (adapter_path / "adapter_model.safetensors").exists():
            raise FileNotFoundError(
                f"Missing adapter weights: {adapter_path}"
            )

        tokenizer = AutoTokenizer.from_pretrained(
            adapter_path,
            use_fast=True,
        )
        base_model = AutoModelForCausalLM.from_pretrained(
            model_name,
            revision=revision,
            quantization_config=quantization_config,
            device_map={"": 0},
            dtype=compute_dtype,
        )
        model = PeftModel.from_pretrained(
            base_model,
            adapter_path,
        )
        model.eval()

        for record in records:
            messages = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": format_question(record),
                },
            ]
            formatted = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
            )
            inputs = tokenizer(
                formatted,
                return_tensors="pt",
            ).to(model.device)

            with torch.inference_mode():
                generated = model.generate(
                    **inputs,
                    do_sample=False,
                    max_new_tokens=32,
                    pad_token_id=tokenizer.eos_token_id,
                )

            output_tokens = generated[
                0,
                inputs["input_ids"].shape[1] :,
            ]
            raw = tokenizer.decode(
                output_tokens,
                skip_special_tokens=True,
            ).strip()
            parsed = parse_answer(raw)
            results.append(
                {
                    "condition": condition,
                    "stem_id": record["stem_id"],
                    "correct_option": record["correct_option"],
                    "raw_response": raw,
                    "parsed_answer": parsed,
                    "parseable": parsed is not None,
                    "correct": parsed == record["correct_option"],
                }
            )

        del model
        del base_model
        gc.collect()
        torch.cuda.empty_cache()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        for result in results:
            file.write(
                json.dumps(result, ensure_ascii=False) + "\n"
            )

    summary: dict[str, Any] = {
        "protocol_version": config["protocol"]["version"],
        "model_name": model_name,
        "model_revision": revision,
        "validation_path": str(VALIDATION_PATH),
        "validation_sha256": sha256_file(VALIDATION_PATH),
        "subset_rule": "first_10_validation_records",
        "conditions": {},
    }
    for condition, adapter_path in ADAPTERS.items():
        subset = [
            result
            for result in results
            if result["condition"] == condition
        ]
        condition_summary = {
            "count": len(subset),
            "parseable": sum(
                result["parseable"] for result in subset
            ),
            "correct": sum(
                result["correct"] for result in subset
            ),
            "adapter_path": str(adapter_path),
        }
        summary["conditions"][condition] = condition_summary
        print(
            f"{condition}: "
            f"parseable={condition_summary['parseable']}/"
            f"{condition_summary['count']}, "
            f"correct={condition_summary['correct']}/"
            f"{condition_summary['count']}"
        )

    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
