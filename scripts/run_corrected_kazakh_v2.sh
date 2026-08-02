#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

test -f data/final/test_kk_v2.jsonl
test -f data/final/kazakh_v2_manifest.json

sha256sum -c docs/kazakh_v2_artifact_hashes.txt
sha256sum -c docs/trained_v2_adapter_hashes.txt
uv run python -m pytest -q

for condition in base control_v2 selective_correction_v2; do
  echo "== Running corrected Kazakh / $condition =="
  uv run python -m src.evaluation.run_final_multilingual \
    --condition "$condition" \
    --language kk \
    --config configs/evaluation/corrected_kazakh_v2.yaml \
    --prompts configs/evaluation/prompts_corrected_kazakh_v2.json
done

uv run python -m src.evaluation.validate_corrected_kazakh_v2_results
uv run python -m src.analysis.analyze_corrected_kazakh_v2
sha256sum -c docs/corrected_kazakh_v2_result_hashes.txt

echo "Corrected Kazakh v2 sensitivity evaluation completed."
