from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import torch
from datasets import Dataset
from peft import (
    LoraConfig,
    PeftModel,
    prepare_model_for_kbit_training,
)
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    Trainer,
    TrainingArguments,
)


MODEL_NAME = "Qwen/Qwen3-4B-Instruct-2507"
MODEL_REVISION = "cdbee75f17c01a7cc42f958dc650907174af0554"
DATA_PATH = Path("data/smoke_test/train.jsonl")
OUTPUT_DIR = Path("outputs/qlora_smoke_test")
MAX_LENGTH = 256

SYSTEM_PROMPT = (
    "Answer the multiple-choice question accurately. "
    "Return one short factual sentence followed by valid JSON "
    'in this exact format: {"answer": "B"}.'
)


def load_records(path: Path) -> list[dict[str, Any]]:
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
                    f"Invalid JSON on line {line_number}: {error}"
                ) from error

    if not records:
        raise ValueError(f"No records found in {path}")

    return records


def build_user_prompt(record: dict[str, Any]) -> str:
    options = record["options"]

    return (
        f"{record['question']}\n\n"
        f"A. {options['A']}\n"
        f"B. {options['B']}\n"
        f"C. {options['C']}\n"
        f"D. {options['D']}"
    )


def build_assistant_response(record: dict[str, Any]) -> str:
    answer_letter = record["answer"]
    answer_text = record["options"][answer_letter]

    return (
        f"The correct answer is {answer_text}.\n"
        f'{{"answer": "{answer_letter}"}}'
    )


def select_dtype() -> torch.dtype:
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for this smoke test.")

    if torch.cuda.is_bf16_supported():
        return torch.bfloat16

    return torch.float16


def load_tokenizer() -> AutoTokenizer:
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME,
        revision=MODEL_REVISION,
        use_fast=True,
    )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    tokenizer.padding_side = "right"
    return tokenizer


def build_dataset(
    tokenizer: AutoTokenizer,
    records: list[dict[str, Any]],
) -> Dataset:
    encoded_records: list[dict[str, list[int]]] = []

    for record in records:
        prompt_messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": build_user_prompt(record),
            },
        ]

        full_messages = [
            *prompt_messages,
            {
                "role": "assistant",
                "content": build_assistant_response(record),
            },
        ]

        prompt_text = tokenizer.apply_chat_template(
            prompt_messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        full_text = tokenizer.apply_chat_template(
            full_messages,
            tokenize=False,
            add_generation_prompt=False,
        )

        prompt_tokens = tokenizer(
            prompt_text,
            add_special_tokens=False,
        )["input_ids"]

        full_tokens = tokenizer(
            full_text,
            add_special_tokens=False,
            truncation=True,
            max_length=MAX_LENGTH,
        )["input_ids"]

        if len(prompt_tokens) >= len(full_tokens):
            raise ValueError(
                "Prompt consumes the entire sequence. "
                "Increase MAX_LENGTH."
            )

        labels = full_tokens.copy()

        prompt_length = min(len(prompt_tokens), len(labels))
        labels[:prompt_length] = [-100] * prompt_length

        encoded_records.append(
            {
                "input_ids": full_tokens,
                "attention_mask": [1] * len(full_tokens),
                "labels": labels,
            }
        )

    return Dataset.from_list(encoded_records)


class CompletionOnlyCollator:
    def __init__(
        self,
        tokenizer: AutoTokenizer,
    ) -> None:
        self.tokenizer = tokenizer

    def __call__(
        self,
        features: list[dict[str, list[int]]],
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
                + [self.tokenizer.pad_token_id] * padding_length
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


def verify_loss_mask(dataset: Dataset) -> None:
    sample = dataset[0]
    labels = sample["labels"]

    supervised_tokens = sum(
        label != -100
        for label in labels
    )
    masked_tokens = sum(
        label == -100
        for label in labels
    )

    print(f"Masked context tokens: {masked_tokens}")
    print(f"Supervised completion tokens: {supervised_tokens}")

    if supervised_tokens == 0:
        raise RuntimeError(
            "No assistant completion tokens are supervised."
        )

    first_supervised = next(
        index
        for index, label in enumerate(labels)
        if label != -100
    )

    if any(label != -100 for label in labels[:first_supervised]):
        raise RuntimeError("Context masking is incorrect.")


def load_quantized_base(
    compute_dtype: torch.dtype,
) -> AutoModelForCausalLM:
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=compute_dtype,
    )

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        revision=MODEL_REVISION,
        quantization_config=quantization_config,
        device_map={"": 0},
        dtype=compute_dtype,
    )

    model.config.use_cache = False

    model = prepare_model_for_kbit_training(
        model,
        use_gradient_checkpointing=True,
    )

    return model


def train_adapter() -> None:
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    records = load_records(DATA_PATH)
    tokenizer = load_tokenizer()
    dataset = build_dataset(tokenizer, records)

    verify_loss_mask(dataset)

    compute_dtype = select_dtype()
    model = load_quantized_base(compute_dtype)

    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules="all-linear",
    )

    model.add_adapter(lora_config)

    trainable_parameters = sum(
        parameter.numel()
        for parameter in model.parameters()
        if parameter.requires_grad
    )

    total_parameters = sum(
        parameter.numel()
        for parameter in model.parameters()
    )

    print(
        "Trainable parameters:",
        f"{trainable_parameters:,}",
    )

    print(
        "Trainable percentage:",
        f"{100 * trainable_parameters / total_parameters:.4f}%",
    )

    training_arguments = TrainingArguments(
        output_dir=str(OUTPUT_DIR),
        max_steps=20,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=1,
        learning_rate=2e-4,
        warmup_steps=2,
        logging_steps=1,
        save_steps=20,
        save_total_limit=1,
        optim="paged_adamw_8bit",
        gradient_checkpointing=True,
        bf16=compute_dtype == torch.bfloat16,
        fp16=compute_dtype == torch.float16,
        report_to="none",
        remove_unused_columns=False,
        seed=42,
        data_seed=42,
    )

    trainer = Trainer(
        model=model,
        args=training_arguments,
        train_dataset=dataset,
        data_collator=CompletionOnlyCollator(tokenizer),
    )

    trainer.train()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)

    print(f"Adapter saved to {OUTPUT_DIR}")


def reload_and_generate() -> None:
    compute_dtype = select_dtype()

    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=compute_dtype,
    )

    tokenizer = AutoTokenizer.from_pretrained(
        OUTPUT_DIR,
        use_fast=True,
    )

    base_model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        revision=MODEL_REVISION,
        quantization_config=quantization_config,
        device_map={"": 0},
        dtype=compute_dtype,
    )

    model = PeftModel.from_pretrained(
        base_model,
        OUTPUT_DIR,
    )

    model.eval()

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": (
                "What is 11 × 9?\n\n"
                "A. 89\n"
                "B. 99\n"
                "C. 101\n"
                "D. 109"
            ),
        },
    ]

    formatted = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    model_inputs = tokenizer(
        formatted,
        return_tensors="pt",
    ).to(model.device)

    with torch.inference_mode():
        generated = model.generate(
            **model_inputs,
            do_sample=False,
            max_new_tokens=48,
            pad_token_id=tokenizer.eos_token_id,
        )

    output_tokens = generated[
        0,
        model_inputs["input_ids"].shape[1] :,
    ]

    response = tokenizer.decode(
        output_tokens,
        skip_special_tokens=True,
    ).strip()

    print("Reloaded-adapter response:")
    print(response)


def main() -> None:
    train_adapter()

    torch.cuda.empty_cache()

    reload_and_generate()


if __name__ == "__main__":
    main()
