# Reproducibility

Install the frozen environment with `uv sync`. Adapter weights are not tracked in Git. They must be regenerated with the frozen Stage 16 scripts or downloaded from a separately documented model repository.

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

Recreate the deterministic analysis:

```bash
uv run python -m src.analysis.analyze_final_multilingual
sha256sum -c docs/final_analysis_hashes.txt
```

The raw final generations are excluded from Git by repository policy. Their SHA-256 values are stored in `docs/final_multilingual_result_hashes.txt`; place the nine files under `results/final_multilingual_v1/` before validating or analyzing them.

The locked evaluation can be run on a CUDA-capable machine with:

```bash
./scripts/run_stage19_locked.sh
```

That command performs preflight hash checks, executes all nine model-language conditions, validates 10,800 records, and records result hashes.
