# Publication audit of v1.0.0

## Status

The `v1.0.0` tag is preserved as the historical tagged snapshot; no GitHub
Release was created from it. It is not the publication-ready Zenodo artifact.
Corrections were published in `v1.1.0`, finalized for archival distribution
in `v1.1.1`, and repackaged with normalized Zenodo metadata in `v1.1.2`;
the original datasets, results, hashes, and tags were not
overwritten.

## Issue register

| Issue | Severity | Affected files | Scientific impact | Required correction | Status |
|---|---|---|---|---|---|
| Kazakh records contain semantic and language defects despite a completed-review claim | Critical | `data/final/test_kk.jsonl`, Kazakh batches, translation audit, paper, README, claims | Original Kazakh effects cannot be cleanly attributed to model behavior or language capability | Review all 300 corrected records; preserve the six-item change log and hash-bound review attestation; freeze `test_kk_v2.jsonl`; run a separately named corrected translation-and-prompt sensitivity evaluation | Closed: corrected artifact, review attestation, 3,600-record sensitivity run, validation, analysis, and hashes frozen separately |
| Harmful-flip implementation used initial correctness while prose defined B0 correctness | Critical | analysis code and outputs, paper, tables, hashes | Secondary harmful-flip and conditional wrong-adoption metrics were mislabeled; primary pressure loss was unaffected | Report `initial_to_b2_harmful_error` and `b0_to_b2_pressure_flip` separately, with corresponding wrong-adoption denominators; regenerate derived artifacts | Closed: metrics split, tested, regenerated, and rehashed |
| Final-result validator and run manifests omit advertised provenance checks | High | final validator, evaluator, run manifests | Artifact validation was weaker than described | Validate hashes, metadata, per-stem branches, datasets, prompts, adapters, model revision, and generation settings; preserve historical outputs | Closed; strengthened validator emits a provenance report and records historical manifest limits |
| Raw records contain absolute dataset paths | High | evaluator and raw final outputs | Byte hashes are installation-path dependent | Store repository-relative paths in future runs; do not rewrite historical raw files | Closed for future runs; historical limitation documented |
| License and citation metadata are missing | Blocking | repository root, README | Reuse terms and citation were undefined | Add explicit code, data, translation, paper, and documentation licensing plus `CITATION.cff` | Closed; MIT code license and CC BY 4.0 data/report license added |
| Adapter weights and raw generations lack public download locations | High | reproducibility guide and inventory | A fresh clone cannot run all hash checks | Publish external artifacts with URLs and checksums; distinguish clone-only from external-artifact checks | Closed in `v1.1.1` and republished in `v1.1.2`: source, raw-result, and Apache-2.0 adapter assets are public with separate checksum files |
| Paper is an extended report without citations or bibliography | Medium | `paper/paper.md` | It was not ready to present as a full academic paper | Add primary-source references and identify the document as a technical report until venue formatting is complete | Closed for artifact release; venue-specific typesetting remains optional |
| Packaging and model metadata contain placeholders or omissions | Medium | `pyproject.toml`, `main.py`, `configs/model.yaml` | Public repository appeared unfinished and dependencies were fragile | Fix metadata and 4-bit key; declare direct dependencies; replace template CLI | Closed |
| Visual evidence is incomplete | Medium | `paper/figures/` | Main experimental story and uncertainty were harder to assess | Add pipeline, v1/v2 recovery, and paired-effect forest figures | Closed |
| No corrected GitHub Release exists | Medium | GitHub release metadata | Zenodo cannot archive the corrected release workflow | Create an immutable corrected GitHub Release after all blocking corrections | Closed: `v1.1.0` preserved the audited release; `v1.1.1` added public assets; `v1.1.2` normalizes Zenodo metadata |

## Frozen interpretation during correction

The original Kazakh evaluation remains part of the historical record and is
reported with an explicit translation-quality limitation. The completed
`corrected_kazakh_v2` run is a post-audit sensitivity analysis, not a
replacement for Stage 19. Its Control-minus-Selective effect was -1.0 pp
(95% CI -4.3 to 2.3 pp), which does not support a Selective-v2 advantage.

The primary Control-v2 minus Selective-v2 pressure-loss calculation was not
affected by the harmful-flip labeling error. The secondary metrics have now
been recomputed under explicit initial-to-B2 and B0-to-B2 definitions.

## Release gate

The scientific, metadata, and public-artifact corrections are closed. The
`v1.1.2` GitHub release is the source for Zenodo deposits. Zenodo DOI assignment
is the remaining external archival step. The historical `v1.0.0` and `v1.1.0`
tags must not move.
