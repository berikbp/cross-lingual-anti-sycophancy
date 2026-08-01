# Multilingual anti-sycophancy

> **Publication audit:** `v1.0.0` is preserved as a historical release, not a
> Zenodo-ready artifact. A post-release audit found substantive defects in the
> Kazakh translation set and a labeling mismatch in a secondary harmful-flip
> metric. See `reports/publication_audit_v1_0.md`. The English/Russian primary
> pressure-loss analysis remains usable; original Kazakh results require a
> translation-quality caveat and corrected sensitivity analysis.

## Summary

This repository tests whether English supervised fine-tuning can reduce pressure-induced factual answer changes in English, Russian, and Kazakh. Balanced selective-correction training prevented the severe stubbornness caused by naive answer-preservation SFT, but did not clearly improve multilingual pressure resistance over a matched control.

## Main result

| Language | Control-v2 pressure loss | Selective-v2 pressure loss | Paired effect |
|---|---:|---:|---:|
| English | 1.7 pp | 1.0 pp | +0.7 pp |
| Russian | 1.7 pp | 2.0 pp | -0.3 pp |
| Kazakh | 17.7 pp | 19.3 pp | -1.7 pp |

All language-specific bootstrap confidence intervals included zero. The macro-average effect was -0.4 percentage points.

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

The study uses one 4B model, one QLoRA setup, English-only SFT, machine-assisted translations, and multiple-choice factual questions. The initial translation review did not reliably detect several substantive Kazakh defects; a complete native review is required. No language-specific confidence interval supports a conclusive intervention benefit.

## Citation and license

Citation metadata and a release license should be added before public archival release.
