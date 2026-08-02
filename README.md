# Multilingual anti-sycophancy

## Summary

This repository studies whether English supervised fine-tuning can reduce pressure-induced factual answer changes in English, Russian, and Kazakh.

A naive answer-preservation intervention reduced answer changes by making the model stubborn. A shared balanced v2 transition design restored factual capability, but Selective-v2 did not clearly outperform the matched Control-v2 condition on pressure resistance.

## Main results

| Language | Control-v2 pressure loss | Selective-v2 pressure loss | Paired effect |
|---|---:|---:|---:|
| English | 1.7 pp | 1.0 pp | +0.7 pp |
| Russian | 1.7 pp | 2.0 pp | -0.3 pp |
| Kazakh, original translation* | 17.7 pp | 19.3 pp | -1.7 pp |
| Kazakh, corrected sensitivity analysis** | 18.7 pp | 19.7 pp | -1.0 pp |

All bootstrap confidence intervals included zero.

\* The original Kazakh values are retained for provenance, but known translation defects prevent clean interpretation.

\** The [corrected Kazakh analysis](reports/corrected_kazakh_v2_analysis.md) is a post-audit sensitivity run, not a replacement for the locked result. It revised both the item translations and Kazakh prompt wording, so it cannot identify the effect of either change alone.

## Design

```text
data construction
      ↓
matched SFT datasets
      ↓
v1 adapters → stubbornness diagnosis
      ↓
balanced v2 datasets and fresh adapters
      ↓
locked English/Russian/Kazakh evaluation
      ↓
fixed-seed paired analysis
```

The locked evaluation contains the same 300 stem IDs in each language and four independent branches per stem: neutral reconsideration, doubt, an incorrect suggestion, and a correct suggestion. Structural alignment is verified; semantic alignment of the historical Kazakh translations is not assumed. Three model conditions produced 10,800 stored branch records. The separately named corrected Kazakh sensitivity run added 3,600 records without overwriting the locked files.

![Experimental pipeline from the v1 failure through the v2 redesign and locked evaluation](paper/figures/experimental_pipeline.svg)

![Paired Control-v2 minus Selective-v2 pressure-loss effects with 95% confidence intervals](paper/figures/paired_effect_forest.svg)

## Repository map

- `configs/`: frozen training, evaluation, and analysis settings
- `data/`: source stems, matched conversations, and multilingual evaluation files
- `src/`: construction, training, evaluation, validation, and analysis code
- `reports/`: audits, run manifests, and frozen results
- `paper/`: paper draft, tables, and figures
- `docs/`: protocols, hashes, inventory, and reproduction instructions

## Reproduction

Create the environment with `uv sync`, then follow [docs/reproducibility.md](docs/reproducibility.md). Adapter weights are excluded from Git; regenerate them with the frozen training scripts or obtain them separately if a release location is provided.

The original ignored adapter and generation artifacts are present in the
author's working archive and have frozen checksums. The Zenodo release workflow
packages them separately from the Git source archive; see
[docs/zenodo_release.md](docs/zenodo_release.md).

## Limitations

The study evaluates one 4B model, one QLoRA configuration, one training seed, English-only fine-tuning, and multiple-choice factual questions.

The original Kazakh translation set contains known semantic and language defects. Its results are retained for transparency but should not be used alone to draw conclusions about Kazakh-language pressure sensitivity or cross-lingual transfer. The corrected sensitivity run reached the same directional result: Selective-v2 did not outperform Control-v2. Because both the translations and prompt wording were revised, the difference between the two Kazakh runs cannot be attributed to either change alone.

Secondary harmful-change metrics are reported separately as initial-to-B2 harmful error and B0-to-B2 pressure flip. The primary pressure-loss calculation was unaffected by this labeling correction.

Detailed correction tracking is available in the [v1.0.0 audit report](reports/publication_audit_v1_0.md).

## Citation and license

Use [CITATION.cff](CITATION.cff) for citation metadata. Source code is licensed
under the [MIT License](LICENSE). Original datasets, translations, paper,
figures, reports, and documentation are dual-licensed under
[CC BY 4.0 or MIT](DATA_LICENSE.md). The v2 adapter artifacts are
[Apache-2.0](MODEL_ARTIFACT_LICENSE.md), matching the upstream Qwen model.
Third-party models and dependencies retain their upstream licenses.

Run the publication-readiness checker before building a release:

```bash
uv run python scripts/check_zenodo_readiness.py
```

The corrected sensitivity evaluation is frozen. The checker now verifies its
dataset, raw-result, and analysis hashes alongside the historical artifacts.
