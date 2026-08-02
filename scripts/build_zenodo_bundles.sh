#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

uv run python scripts/check_zenodo_readiness.py

mkdir -p dist
release_version="$(uv run python -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["project"]["version"])')"
source_archive="dist/cross-lingual-anti-sycophancy-${release_version}-source.tar.gz"
results_archive="dist/cross-lingual-anti-sycophancy-${release_version}-raw-results.tar.gz"
adapter_archive="dist/cross-lingual-anti-sycophancy-${release_version}-adapters.tar.gz"

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

tar -czf "$adapter_archive" \
  outputs/adapters/v2/control/final \
  outputs/adapters/v2/selective_correction/final \
  docs/trained_v2_adapter_hashes.txt \
  APACHE-2.0.txt \
  MODEL_ARTIFACT_LICENSE.md

sha256sum "$source_archive" "$results_archive" \
  > dist/SOURCE_AND_RESULTS_SHA256SUMS.txt
sha256sum "$adapter_archive" > dist/ADAPTER_SHA256SUMS.txt

echo "Zenodo bundles created in dist/."
echo "Upload source, raw results, and their checksum file to the software deposit."
echo "Upload the adapter archive and its checksum file to a linked Apache-2.0 record."
