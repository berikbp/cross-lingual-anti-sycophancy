# Zenodo release procedure

The repository is prepared for a `v1.1.0` archival release. The corrected
Kazakh artifact has a compact, hash-bound author-review attestation, and the
separately named translation-and-prompt sensitivity run is complete. The
readiness checker verifies both the historical and corrected artifacts.

## 1. Verify the Kazakh review artifact

The review record is documented in
`docs/translation/kazakh_v2_review_record.md`. Freeze and verify the exact
reviewed JSONL with:

```bash
uv run python -m src.translation.finalize_kazakh_v2
sha256sum -c docs/kazakh_v2_artifact_hashes.txt
```

The finalizer rejects a dataset that does not match its review attestation.

## 2. Run the corrected translation-and-prompt sensitivity evaluation

Use the same three frozen model conditions. This is a post-audit sensitivity
analysis and does not overwrite the original Stage 19 Kazakh results. The
wrapper performs adapter and dataset hash checks, all three runs, result
validation, analysis, and result-hash verification:

```bash
./scripts/run_corrected_kazakh_v2.sh
```

The completed wrapper validates and analyzes the three files, records
`docs/corrected_kazakh_v2_result_hashes.txt`, and writes
`reports/corrected_kazakh_v2_analysis.md`. Report the historical and corrected
Kazakh results side by side. This follow-up revises both the item translations
and the Kazakh prompt wording, so it measures their combined effect and cannot
identify either component separately.

The public claims report the historical and corrected results side by side and
link to `reports/corrected_kazakh_v2_analysis.md`. The readiness checker rejects
stale language that describes the corrected run as pending.

## 3. Run the release audit

Confirm that the author name in `CITATION.cff`, `.zenodo.json`, `LICENSE`, and
the paper is correct; add an ORCID if one should be published. Set
`date-released` in `CITATION.cff` to the actual `v1.1.0` release date. Do not
pre-date an unreleased artifact.

```bash
uv run pytest -q
uv run python -m src.evaluation.validate_final_multilingual_results
uv run python -m src.analysis.analyze_final_multilingual \
  --config configs/analysis/final_analysis_v1.yaml
uv run python scripts/check_zenodo_readiness.py
```

The final command must print `Zenodo readiness: PASS`.

## 4. Create archival bundles

After committing all changes:

```bash
./scripts/build_zenodo_bundles.sh
```

This creates a source archive, a raw-results archive, an adapter archive, and a
checksum file under `dist/`. The extra archives are necessary because Git
intentionally excludes model weights and raw results.

## 5. Publish

1. Push the final commit to `main`.
2. Create the annotated tag `v1.1.0`; do not move the historical `v1.0.0` tag.
3. Create a GitHub Release from `v1.1.0` and attach the source archive, raw
   results archive, and `SHA256SUMS.txt`.
4. Create or connect a Zenodo software deposit and upload those same files.
   Import the metadata from `.zenodo.json`, then verify the author, title,
   license, and description before publishing.
5. Publish the adapter archive in a separate Apache-2.0 model or software
   record (Zenodo or Hugging Face), because its license follows the Apache-2.0
   Qwen base model. Link the two records using related identifiers.
6. Add the issued DOI to `CITATION.cff`, `.zenodo.json`, README, and the paper in
   a DOI-only metadata commit if Zenodo reserves the DOI before publication.
7. Record the final artifact URLs and DOI in `docs/artifact_inventory.md`.

The code is MIT-licensed. Original data, translations, paper, figures, reports,
and documentation are dual-licensed under CC BY 4.0 or MIT under
`DATA_LICENSE.md`. Adapters are Apache-2.0 under
`MODEL_ARTIFACT_LICENSE.md`. Third-party model and dependency licenses remain
unchanged.
