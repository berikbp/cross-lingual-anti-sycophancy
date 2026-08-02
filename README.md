# Multilingual anti-sycophancy

## Summary

This repository studies whether English supervised fine-tuning can reduce pressure-induced factual answer changes in English, Russian, and Kazakh.

A naive answer-preservation intervention reduced answer changes by making the model stubborn. A shared balanced v2 transition design restored factual capability, but Selective-v2 did not clearly outperform the matched Control-v2 condition on pressure resistance.

## Main results

| Language | Control-v2 pressure loss | Selective-v2 pressure loss | Paired effect |
|---|---:|---:|---:|
| English | 1.7 pp | 1.0 pp | +0.7 pp |
| Russian | 1.7 pp | 2.0 pp | -0.3 pp |
| Kazakh* | 17.7 pp | 19.3 pp | -1.7 pp |

All language-specific bootstrap confidence intervals included zero.

\* The Kazakh values come from the original translation set and are retained as historical results. Translation defects prevent clean interpretation until the corrected Kazakh translation-and-prompt sensitivity evaluation is complete.

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

The final evaluation contains the same 300 stem IDs in each language and four independent branches per stem: neutral reconsideration, doubt, an incorrect suggestion, and a correct suggestion. Structural alignment is verified; semantic alignment of the historical Kazakh translations is not assumed. Three model conditions produced 10,800 stored branch records.

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

The original Kazakh translation set contains known semantic and language defects. Its results are retained for transparency but should not be used to draw conclusions about Kazakh-language pressure sensitivity or cross-lingual transfer. A corrected Kazakh translation-and-prompt sensitivity evaluation is being prepared; because both language artifacts are revised, it will not isolate their individual effects.

Secondary harmful-change metrics are reported separately as initial-to-B2 harmful error and B0-to-B2 pressure flip. The primary pressure-loss calculation was unaffected by this labeling correction.

Detailed correction tracking is available in the [v1.0.0 audit report](reports/publication_audit_v1_0.md).

## Citation and license

Use [CITATION.cff](CITATION.cff) for citation metadata. Source code is licensed
under the [MIT License](LICENSE). Original datasets, translations, paper,
figures, reports, and documentation are dual-licensed under
[CC BY 4.0 or MIT](DATA_LICENSE.md). The v2 adapter artifacts are
[Apache-2.0](MODEL_ARTIFACT_LICENSE.md), matching the upstream Qwen model.
Third-party models and dependencies retain their upstream licenses.

The publication-readiness checker is:

```bash
uv run python scripts/check_zenodo_readiness.py
```

It intentionally fails until the corrected Kazakh artifact has completed an
identified native review and its separately labeled sensitivity evaluation has
been frozen. This protects the historical `v1.0.0` record from silent changes.
