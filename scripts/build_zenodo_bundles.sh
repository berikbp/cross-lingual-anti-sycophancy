#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

uv run python scripts/check_zenodo_readiness.py

mkdir -p dist
release_version="$(uv run python -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["project"]["version"])')"
source_archive="dist/cross-lingual-anti-sycophancy-${release_version}-source.tar.gz"
results_archive="dist/cross-lingual-anti-sycophancy-${release_version}-raw-results.tar.gz"
adapter_archive="dist/cross-lingual-anti-sycophancy-${release_version}-adapters.tar.gz"
source_name="$(basename "$source_archive")"
results_name="$(basename "$results_archive")"
adapter_name="$(basename "$adapter_archive")"
adapter_stage="$(mktemp -d dist/adapter-package.XXXXXX)"

cleanup() {
  rm -rf "$adapter_stage"
}

trap cleanup EXIT

git archive \
  --format=tar.gz \
  --prefix="cross-lingual-anti-sycophancy-${release_version}/" \
  --output="$source_archive" \
  HEAD

tar -czf "$results_archive" \
  results/final_multilingual_v1 \
  results/corrected_kazakh_v2 \
  docs/final_multilingual_result_hashes.txt \
  docs/corrected_kazakh_v2_result_hashes.txt

for condition in control selective_correction; do
  source_directory="outputs/adapters/v2/${condition}/final"
  destination_directory="${adapter_stage}/${source_directory}"
  mkdir -p "$destination_directory"
  cp \
    "$source_directory/adapter_model.safetensors" \
    "$source_directory/adapter_config.json" \
    "$source_directory/tokenizer.json" \
    "$source_directory/chat_template.jinja" \
    "$source_directory/tokenizer_config.json" \
    "$destination_directory/"
done

cp model_cards/control_v2.md \
  "$adapter_stage/outputs/adapters/v2/control/final/README.md"
cp model_cards/selective_correction_v2.md \
  "$adapter_stage/outputs/adapters/v2/selective_correction/final/README.md"
mkdir -p "$adapter_stage/docs"
cp docs/trained_v2_adapter_hashes.txt "$adapter_stage/docs/"
cp APACHE-2.0.txt MODEL_ARTIFACT_LICENSE.md "$adapter_stage/"

tar -czf "$adapter_archive" -C "$adapter_stage" \
  outputs \
  docs \
  APACHE-2.0.txt \
  MODEL_ARTIFACT_LICENSE.md

(
  cd dist
  sha256sum "$source_name" "$results_name" \
    > SOURCE_AND_RESULTS_SHA256SUMS.txt
  sha256sum "$adapter_name" > ADAPTER_SHA256SUMS.txt
)

echo "Zenodo bundles created in dist/."
echo "Upload source, raw results, and their checksum file to the software deposit."
echo "Upload the adapter archive and its checksum file to a linked Apache-2.0 record."
