# Zenodo publication guide

Version `1.1.3` is the publication package. Earlier tags remain unchanged for
provenance.

## Verify the repository

From the repository root:

```bash
uv sync --frozen
uv run pytest -q
uv run python scripts/check_zenodo_readiness.py
```

The final command must print `Zenodo readiness: PASS`. The checker verifies the
tracked metadata, frozen datasets, adapter files, raw generations, manifests,
and historical and corrected result hashes.

## Build the archives

```bash
./scripts/build_zenodo_bundles.sh
```

The command creates five files under `dist/`:

```text
cross-lingual-anti-sycophancy-1.1.3-source.tar.gz
cross-lingual-anti-sycophancy-1.1.3-raw-results.tar.gz
SOURCE_AND_RESULTS_SHA256SUMS.txt
cross-lingual-anti-sycophancy-1.1.3-adapters.tar.gz
ADAPTER_SHA256SUMS.txt
```

Verify the portable checksum manifests from inside that directory:

```bash
cd dist
sha256sum -c SOURCE_AND_RESULTS_SHA256SUMS.txt
sha256sum -c ADAPTER_SHA256SUMS.txt
cd ..
```

## Main software deposit

Create a Zenodo software record using `.zenodo.json` and upload:

- the source archive;
- the raw-results archive;
- `SOURCE_AND_RESULTS_SHA256SUMS.txt`.

The source code is MIT-licensed. The original datasets, translations, report,
figures, tables, and documentation are dual-licensed under CC BY 4.0 or MIT as
described in `DATA_LICENSE.md`.

## Adapter deposit

Create a separate Zenodo model or software record and upload:

- the adapter archive;
- `ADAPTER_SHA256SUMS.txt`.

The archive contains `APACHE-2.0.txt`, `MODEL_ARTIFACT_LICENSE.md`, both adapter
configurations, both adapter weight files, and their frozen hashes. Link the
adapter record to the software record under Related works.

## After Zenodo assigns the DOIs

Add the software DOI to `CITATION.cff`, `.zenodo.json`, `README.md`, the paper,
and `docs/artifact_inventory.md`. Add the adapter DOI to the inventory and the
software record's related identifiers. Make this as a metadata-only commit; do
not move any published tag.
