#!/usr/bin/env bash
set -euo pipefail

export UV_CACHE_DIR="${UV_CACHE_DIR:-/tmp/multilingual-sycophancy-uv-cache}"

echo "== Stage 19 preflight =="
nvidia-smi
uv run python - <<'PY'
import torch
assert torch.cuda.is_available(), "CUDA is not available in this terminal"
assert torch.cuda.device_count() >= 1
print(f"CUDA device: {torch.cuda.get_device_name(0)}")
PY

sha256sum -c docs/final_multilingual_artifact_hashes.txt
sha256sum -c docs/trained_v2_adapter_hashes.txt
uv run python -m src.translation.validate_multilingual_final
uv run pytest -q

CONFIG="configs/evaluation/final_multilingual_v1.yaml"

run_eval() {
  local condition="$1"
  local language="$2"
  echo "== Running ${condition} / ${language} =="
  uv run python -m src.evaluation.run_final_multilingual \
    --condition "${condition}" \
    --language "${language}" \
    --config "${CONFIG}"
}

run_eval base en
run_eval base ru
run_eval base kk
run_eval control_v2 en
run_eval control_v2 ru
run_eval control_v2 kk
run_eval selective_correction_v2 en
run_eval selective_correction_v2 ru
run_eval selective_correction_v2 kk

echo "== Validating locked results =="
uv run python -m src.evaluation.validate_final_multilingual_results

sha256sum \
  results/final_multilingual_v1/base_en.jsonl \
  results/final_multilingual_v1/base_ru.jsonl \
  results/final_multilingual_v1/base_kk.jsonl \
  results/final_multilingual_v1/control_v2_en.jsonl \
  results/final_multilingual_v1/control_v2_ru.jsonl \
  results/final_multilingual_v1/control_v2_kk.jsonl \
  results/final_multilingual_v1/selective_correction_v2_en.jsonl \
  results/final_multilingual_v1/selective_correction_v2_ru.jsonl \
  results/final_multilingual_v1/selective_correction_v2_kk.jsonl \
  > docs/final_multilingual_result_hashes.txt

sha256sum -c docs/final_multilingual_result_hashes.txt
echo "Stage 19 locked evaluation completed successfully."
