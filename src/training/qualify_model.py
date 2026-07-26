from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

MODEL_NAME = 'Qwen/Qwen3-4B-Instruct-2507'
OUTPUT_PATH = Path('results/model_qualifacation/inference_results.json')

@dataclass
class Question:
    question_id: str
    language: str
    prompt: str
    correct_answer: str
    


QUESTIONS = [
     Question(question_id="en_math_001", language="en", prompt=("What is 19 × 7?\n\n""A. 126\n""B. 133\n""C. 137\n""D. 143"), correct_answer="B"),
     Question(question_id="en_science_001", language="en", prompt=("Which planet is closest to the Sun?\n\n""A. Venus\n""B. Earth\n""C. Mercury\n""D. Mars"), correct_answer="C"),
     Question(question_id="ru_math_001", language="ru", prompt=("Сколько будет 19 × 7?\n\n""A. 126\n""B. 133\n""C. 137\n""D. 143"), correct_answer="B"),
     Question(question_id="ru_science_001", language="ru", prompt=("Какая планета находится ближе всего к Солнцу?\n\n""A. Венера\n""B. Земля\n""C. Меркурий\n""D. Марс"), correct_answer="C"),
     Question(question_id="kk_math_001", language="kk", prompt=("19 × 7 нешеге тең?\n\n""A. 126\n""B. 133\n""C. 137\n""D. 143"), correct_answer="B"),
     Question(question_id="kk_science_001", language="kk", prompt=("Күнге ең жақын орналасқан ғаламшар қайсы?\n\n""A. Шолпан\n""B. Жер\n""C. Меркурий\n""D. Марс"), correct_answer="C"),
]

SYSTEM_PROMPT = (
    'Answer the multiple choice question. '
    'Return only valid JSON in this format: {"answer": "B"}. '
    'The answer must be exactly A, B, C, or D.'
)

def select_compute_dtype() -> torch.dtype:
    if not torch.cuda.is_available():
        raise ValueError("CUDA is not available, cannot select compute dtype")
    
    if torch.cuda.is_bf16_supported():
        return torch.bfloat16
    
    return torch.float16

def parse_answer(text: str) -> str | None:
    try:
        value = json.loads(text.strip())
        answer = value.get('answer')
        
        if answer in {'A', 'B', 'C', 'D'}:
            return answer
    except (json.JSONDecodeError, AttributeError):
        pass
    
    match = re.search( r'[\"\']?answer[\"\']?\s*:\s*[\"\']?([ABCD])[\"\']?', text, flags=re.IGNORECASE, )

    if match:
        return match.group(1).upper()

    return None

def load_model() -> tuple[AutoTokenizer, AutoModelForCausalLM]:
    compute_dtype = select_compute_dtype()

    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=compute_dtype,
        bnb_4bit_quant_type='nf4',
        bnb_4bit_use_double_quant=True,
    )

    print(f"Loading {MODEL_NAME}")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)
    

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=quantization_config,
        device_map="auto",
        torch_dtype=compute_dtype,
        
    )
    model.eval()
    return tokenizer, model


def generate_answer(tokenizer: AutoTokenizer, model: AutoModelForCausalLM, question: Question) -> dict[str, Any]:
    messages = [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': question.prompt}
    ]

    formatted = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    model_inputs = tokenizer(formatted, return_tensors='pt').to(model.device)

    start_time = time.perf_counter()

    with torch.inference_mode():
        generated = model.generate(
            **model_inputs,
            do_sample=False,
            max_new_tokens=32,
            pad_token_id=tokenizer.eos_token_id
        )

    elapsed = time.perf_counter() - start_time

    generated_tokens = generated[0, model_inputs['input_ids'].shape[1] :] 
    raw_response = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()

    parsed_answer = parse_answer(raw_response)

    return { 
        "question_id": question.question_id, 
        "language": question.language, 
        "correct_answer": question.correct_answer, 
        "raw_response": raw_response, 
        "parsed_answer": parsed_answer, 
        "is_correct": parsed_answer == question.correct_answer, 
        "parseable": parsed_answer is not None, 
        "generation_seconds": round(elapsed, 3)
    }   


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    tokenizer, model = load_model()

    results = []

    for question in QUESTIONS:
        result = generate_answer(tokenizer, model, question)
        results.append(result)
        
        print(
            f"Question {question.question_id} ({question.language}): {result['is_correct']}"
            f" parsed: {result['parsed_answer']}, raw: {result['raw_response']}"
            f" in {result['generation_seconds']:.2f}s"
            f"Correct: {question.correct_answer}"
        )
    
    with OUTPUT_PATH.open('w', encoding='utf-8') as f:
        for result in results:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')
    
    parseable_count = sum(result["parseable"] for result in results) 
    correct_count = sum(result["is_correct"] for result in results) 
    
    print(f"Saved results to: {OUTPUT_PATH}")
    print(f"Parseable: {parseable_count}/{len(results)}") 
    print(f"Correct: {correct_count}/{len(results)}") 

if __name__ == "__main__": main()