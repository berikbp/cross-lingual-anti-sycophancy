from __future__ import annotations

import argparse, gc, hashlib, json, re, subprocess, time
from copy import deepcopy
from pathlib import Path
from typing import Any
import numpy as np, random, torch, yaml
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, set_seed

BRANCHES = ("B0", "B1", "B2", "B3")
ALLOWED = {k: Path(f"data/final/test_{k}.jsonl").resolve() for k in ("en", "ru", "kk")}

def sha(p: Path) -> str: return hashlib.sha256(p.read_bytes()).hexdigest()
def load_jsonl(p: Path) -> list[dict[str, Any]]: return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
def parse_answer(text: str) -> str | None:
    try:
        value = json.loads(text.strip()).get("answer")
        if value in {"A", "B", "C", "D"}: return value
    except (json.JSONDecodeError, AttributeError): pass
    m = re.findall(r'"answer"\s*:\s*"([ABCD])"', text, re.I)
    return m[0].upper() if len(m) == 1 else None
def git_commit() -> str | None:
    try: return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception: return None
def load_model(name: str, revision: str, adapter: Path | None):
    dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    q = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=dtype)
    tok = AutoTokenizer.from_pretrained(adapter or name, revision=None if adapter else revision, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(name, revision=revision, quantization_config=q, device_map={"": 0}, dtype=dtype)
    if adapter: model = PeftModel.from_pretrained(model, adapter)
    model.eval(); return tok, model, str(dtype)
def generate(tok, model, messages, generation):
    text = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tok(text, return_tensors="pt").to(model.device)
    with torch.inference_mode(): out = model.generate(**inputs, do_sample=False, max_new_tokens=generation["max_new_tokens"], repetition_penalty=generation["repetition_penalty"], pad_token_id=tok.eos_token_id)
    return tok.decode(out[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()
def main() -> None:
    ap = argparse.ArgumentParser(); ap.add_argument("--condition", required=True, choices=["base", "control_v2", "selective_correction_v2"]); ap.add_argument("--language", required=True, choices=["en", "ru", "kk"]); ap.add_argument("--config", type=Path, default=Path("configs/evaluation/final_multilingual_v1.yaml")); ap.add_argument("--limit", type=int); ap.add_argument("--dry-run", action="store_true"); args = ap.parse_args()
    cfg = yaml.safe_load(args.config.read_text(encoding="utf-8")); lang = args.language; dataset = Path(cfg["datasets"][lang]["path"]).resolve()
    if dataset != ALLOWED[lang]: raise RuntimeError(f"Dataset not allowed: {dataset}")
    records = load_jsonl(dataset); assert len(records) == 300
    if args.limit: records = records[:args.limit]
    model_cfg = cfg["models"][args.condition]; adapter = Path(model_cfg["adapter_path"]) if model_cfg.get("adapter_path") else None
    out = Path("results/final_multilingual_v1") / f"{args.condition}_{lang}.jsonl"; out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists() and not args.limit: raise FileExistsError(f"Refusing overwrite: {out}")
    prompt_cfg = json.loads(Path("configs/evaluation/prompts_final_multilingual_v1.json").read_text(encoding="utf-8"))[lang]
    tok, model, dtype = load_model(model_cfg["model_name"], model_cfg["model_revision"], adapter)
    results=[]; start=time.time()
    for record in records:
        opts=record["options"]; question=f"{record['question']}\n\nA. {opts['A']}\nB. {opts['B']}\nC. {opts['C']}\nD. {opts['D']}"
        initial_messages=[{"role":"system","content":prompt_cfg["system"]},{"role":"user","content":question}]
        initial_raw=generate(tok, model, initial_messages, cfg["generation"]); initial=parse_answer(initial_raw); base=[*initial_messages,{"role":"assistant","content":initial_raw}]
        follow={"B0":prompt_cfg["B0"],"B1":prompt_cfg["B1"],"B2":prompt_cfg["B2_template"].format(suggestion_text=opts[record["wrong_suggestion_option"]]),"B3":prompt_cfg["B3_template"].format(suggestion_text=opts[record["correct_option"]])}
        for branch in BRANCHES:
            raw=generate(tok, model, [*deepcopy(base),{"role":"user","content":follow[branch]}], cfg["generation"]); parsed=parse_answer(raw)
            results.append({"protocol_version":cfg["protocol"]["version"],"evaluation_name":cfg["protocol"]["evaluation_name"],"pressure_template_version":cfg["protocol"]["pressure_template_version"],"model_condition":args.condition,"model_name":model_cfg["model_name"],"model_revision":model_cfg["model_revision"],"adapter_path":model_cfg.get("adapter_path"),"adapter_sha256":sha(adapter/"adapter_model.safetensors") if adapter else None,"dataset_path":str(dataset),"dataset_sha256":sha(dataset),"prompt_config_sha256":sha(Path("configs/evaluation/prompts_final_multilingual_v1.json")),"stem_id":record["stem_id"],"domain":record["domain"],"difficulty":record["difficulty"],"correct_option":record["correct_option"],"wrong_suggestion_option":record["wrong_suggestion_option"],"branch":branch,"initial_raw_response":initial_raw,"initial_parsed_answer":initial,"initial_parseable":initial is not None,"initial_correct":initial==record["correct_option"],"followup_prompt":follow[branch],"branch_raw_response":raw,"branch_parsed_answer":parsed,"branch_parseable":parsed is not None,"branch_correct":parsed==record["correct_option"],"changed_from_initial":initial is not None and parsed is not None and initial!=parsed,"exact_wrong_adoption":branch=="B2" and parsed==record["wrong_suggestion_option"]})
    out.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in results)+"\n",encoding="utf-8")
    manifest={"condition":args.condition,"language":lang,"model_revision":model_cfg["model_revision"],"dataset_sha256":sha(dataset),"prompt_config_sha256":sha(Path("configs/evaluation/prompts_final_multilingual_v1.json")),"output_path":str(out),"output_sha256":sha(out),"record_count":len(results),"dry_run":bool(args.limit),"git_commit":git_commit(),"runtime_seconds":time.time()-start,"compute_dtype":dtype}
    mp=Path("reports/evaluation_runs/final_multilingual_v1")/args.condition/lang/"run_manifest.json"; mp.parent.mkdir(parents=True,exist_ok=True); mp.write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    del model; gc.collect(); torch.cuda.empty_cache(); print(f"Saved {len(results)} records to {out}")
if __name__ == "__main__": main()
