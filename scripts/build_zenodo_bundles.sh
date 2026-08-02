#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

uv run python scripts/check_zenodo_readiness.py

mkdir -p dist
git archive \
  --format=tar.gz \
  --prefix=cross-lingual-anti-sycophancy-1.1.0/ \
  --output=dist/cross-lingual-anti-sycophancy-1.1.0-source.tar.gz \
  HEAD

tar -czf dist/cross-lingual-anti-sycophancy-1.1.0-raw-results.tar.gz \
  results/final_multilingual_v1 \
  results/corrected_kazakh_v2 \
  docs/final_multilingual_result_hashes.txt \
  docs/corrected_kazakh_v2_result_hashes.txt

tar -czf dist/cross-lingual-anti-sycophancy-1.1.0-adapters.tar.gz \
  outputs/adapters/v2/control/final \
  outputs/adapters/v2/selective_correction/final \
  docs/trained_v2_adapter_hashes.txt \
  APACHE-2.0.txt \
  MODEL_ARTIFACT_LICENSE.md

sha256sum dist/*.tar.gz > dist/SHA256SUMS.txt

echo "Zenodo bundles created in dist/."
echo "Upload the source and raw-results archives to the software deposit."
echo "Publish the Apache-2.0 adapter archive separately and link both records."
