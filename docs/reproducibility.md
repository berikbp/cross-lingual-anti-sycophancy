# Reproducibility

Install the frozen environment with `uv sync --frozen`.

The repository has two reproducibility levels:

1. **Fresh-clone checks** use tracked datasets, configurations, scripts,
   manifests, reports, and analysis code.
2. **Full inference checks** additionally require the two adapter directories
   and nine raw Stage 19 JSONL files. They are excluded from Git and must be
   regenerated or downloaded from the release's external-artifact archive.

Run the audits from the repository root:

```bash
uv run pytest -q
uv run python -m src.training_data_v2.validate_v2_datasets
uv run python -m src.translation.validate_multilingual_final
uv run python -m src.evaluation.validate_final_multilingual_results
sha256sum -c docs/training_v2_dataset_hashes.txt
sha256sum -c docs/trained_v2_adapter_hashes.txt
sha256sum -c docs/final_multilingual_artifact_hashes.txt
sha256sum -c docs/final_multilingual_result_hashes.txt
sha256sum -c docs/final_analysis_hashes.txt
```

Recreate the fixed-seed analysis:

```bash
uv run python -m src.analysis.analyze_final_multilingual \
  --config configs/analysis/final_analysis_v1.yaml
sha256sum -c docs/final_analysis_hashes.txt
```

The raw final generations are excluded from Git by repository policy. Their
SHA-256 values are stored in `docs/final_multilingual_result_hashes.txt`; place
the nine files under `results/final_multilingual_v1/` before validating or
analyzing them. The validator verifies hashes, record membership, answer
metadata, prompts, model revision, adapter provenance, and branch consistency.

The locked evaluation can be run on a CUDA-capable machine with:

```bash
./scripts/run_stage19_locked.sh
```

That command performs preflight hash checks, executes all nine model-language conditions, validates 10,800 records, and records result hashes.

The historical raw records contain absolute working-directory paths because
that evaluator version serialized resolved paths. Their hashes therefore
validate the frozen original files, but a new run on another machine will not
be byte-identical solely because of path provenance. The current evaluator
stores repository-relative paths for all future runs.

Release-specific checks and bundle creation are documented in
[zenodo_release.md](zenodo_release.md).
