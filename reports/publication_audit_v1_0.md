# Publication audit of v1.0.0

## Status

The `v1.0.0` tag is preserved as the historical release. It is not the
publication-ready Zenodo artifact. Corrections are being prepared on
`publication-audit-v1.1.0`; the original datasets, results, hashes, and tag will
not be overwritten.

## Issue register

| Issue | Severity | Affected files | Scientific impact | Required correction | Status |
|---|---|---|---|---|---|
| Kazakh records contain semantic and language defects despite a completed-review claim | Critical | `data/final/test_kk.jsonl`, Kazakh batches, translation audit, paper, README, claims | Original Kazakh effects cannot be cleanly attributed to model behavior or language capability | Withdraw the review claim; complete native review of all 300 records; preserve a per-stem change log; freeze `test_kk_v2.jsonl`; run a separately named corrected-Kazakh sensitivity evaluation | Open; claims qualified |
| Harmful-flip implementation used initial correctness while prose defined B0 correctness | Critical | analysis code and outputs, paper, tables, hashes | Secondary harmful-flip and conditional wrong-adoption metrics were mislabeled; primary pressure loss was unaffected | Report `initial_to_b2_harmful_error` and `b0_to_b2_pressure_flip` separately, with corresponding wrong-adoption denominators; regenerate derived artifacts | Closed: metrics split, tested, regenerated, and rehashed |
| Final-result validator and run manifests omit advertised provenance checks | High | final validator, evaluator, run manifests | Artifact validation is weaker than described | Validate hashes, metadata, per-stem branches, datasets, prompts, adapters, model revision, and generation settings; preserve historical outputs | Open |
| Raw records contain absolute dataset paths | High | evaluator and raw final outputs | Byte hashes are installation-path dependent | Store repository-relative paths in future runs; do not rewrite historical raw files | Open |
| License and citation metadata are missing | Blocking | repository root, README | Reuse terms and citation are undefined | Add explicit code, data, translation, paper, and documentation licensing plus `CITATION.cff` | Open |
| Adapter weights and raw generations lack public download locations | High | reproducibility guide and inventory | A fresh clone cannot run all hash checks | Publish external artifacts with URLs and checksums; distinguish clone-only from external-artifact checks | Open |
| Paper is an extended report without citations or bibliography | Medium | `paper/paper.md` | Not ready to present as a full academic paper | Expand with references and methodology or relabel as a technical report | Open |
| Packaging and model metadata contain placeholders or omissions | Medium | `pyproject.toml`, `main.py`, `configs/model.yaml` | Public repository appears unfinished and dependencies are fragile | Fix metadata and 4-bit key; declare direct dependencies; replace template CLI | Open |
| Visual evidence is incomplete | Medium | `paper/figures/` | Main experimental story and uncertainty are harder to assess | Add pipeline, v1/v2 recovery, and paired-effect forest figures | Open |
| No GitHub Release exists for the historical tag | Medium | GitHub release metadata | Zenodo cannot archive the intended corrected release workflow | Create an actual `v1.1.0` GitHub Release after all blocking corrections | Open |

## Frozen interpretation during correction

The original Kazakh evaluation remains part of the historical record. It will
be reported with an explicit translation-quality limitation. A corrected run
will use a separate label such as `corrected_kazakh_v2`; it will be a
post-publication-audit sensitivity analysis, not a replacement for Stage 19.

The primary Control-v2 minus Selective-v2 pressure-loss calculation was not
affected by the harmful-flip labeling error. The secondary metrics have now
been recomputed under explicit initial-to-B2 and B0-to-B2 definitions.

## Release gate

Zenodo publication is blocked until every critical and blocking issue above is
closed, the corrected artifacts are audited, and a new `v1.1.0` release is
created. Presentation improvements follow the scientific corrections.
