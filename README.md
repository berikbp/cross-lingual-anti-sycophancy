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

\* The Kazakh values come from the original translation set and are retained as historical results. Translation defects prevent clean interpretation until the corrected Kazakh sensitivity evaluation is complete.

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
deterministic paired analysis
```

The final evaluation contains 300 aligned stems per language and four independent branches per stem: neutral reconsideration, doubt, an incorrect suggestion, and a correct suggestion. Three model conditions produced 10,800 stored branch records.

## Repository map

- `configs/`: frozen training, evaluation, and analysis settings
- `data/`: source stems, matched conversations, and multilingual evaluation files
- `src/`: construction, training, evaluation, validation, and analysis code
- `reports/`: audits, run manifests, and frozen results
- `paper/`: paper draft, tables, and figures
- `docs/`: protocols, hashes, inventory, and reproduction instructions

## Reproduction

Create the environment with `uv sync`, then follow [docs/reproducibility.md](docs/reproducibility.md). Adapter weights are excluded from Git; regenerate them with the frozen training scripts or obtain them separately if a release location is provided.

## Limitations

The study evaluates one 4B model, one QLoRA configuration, one training seed, English-only fine-tuning, and multiple-choice factual questions.

The original Kazakh translation set contains known semantic and language defects. Its results are retained for transparency but should not be used to draw conclusions about Kazakh-language pressure sensitivity or cross-lingual transfer. A corrected Kazakh sensitivity evaluation is being prepared.

A secondary harmful-flip measure is also being recomputed under separate initial-to-B2 and B0-to-B2 definitions. The primary pressure-loss calculation is unaffected.

Detailed correction tracking is available in the [v1.0.0 audit report](reports/publication_audit_v1_0.md).

## Citation and license

Citation metadata and a release license should be added before public archival release.
