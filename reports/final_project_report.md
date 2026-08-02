# Final project report

## Completion

The original 21-stage experiment completed, but the repository is not yet publication-ready. A publication audit identified substantive defects in the original Kazakh translations and an ambiguity in secondary harmful-change metrics. The historical data and results remain frozen while corrections are prepared.

## Experimental history

```text
original anti-sycophancy hypothesis
→ v1 answer-preservation intervention
→ severe stubbornness and capability loss
→ transition-pattern diagnosis
→ balanced v2 redesign
→ capability restoration
→ locked multilingual null result
```

## Frozen counts

- English master pool: 400 stems
- Final test/reserve: 300/100
- V2 training/validation: 1,000/100 conversations per condition
- Languages: English, Russian, Kazakh
- Final model-language conditions: 9
- Final stored branch records: 10,800

## Findings

V1 showed that a model can appear resistant by refusing to revise any answer. The shared v2 transition design restored factual capability and avoided the most severe preservation shortcut. Explicit selective feedback did not deliver a reliable primary benefit in the currently interpretable English and Russian comparisons: the Control-minus-Selective pressure-loss effect was +0.7 pp in English and -0.3 pp in Russian, and both confidence intervals contained zero.

The original Kazakh evaluation is retained as a historical result but is confounded by known translation defects. A full native review and separately named corrected-Kazakh sensitivity evaluation are pending. No claim about inherent Kazakh pressure sensitivity or cross-lingual transfer should be based on the original Kazakh run.

## Deviations

The original plan proceeded directly from v1 to multilingual evaluation. Development results exposed stubbornness, so the project added a documented diagnosis, a balanced v2 intervention, and a second development gate. Translation used Google Translate GTX for drafts under an explicit amendment. The initial Kazakh review failed to detect substantive semantic and language defects.

## Release readiness

Core datasets, configurations, scripts, manifests, analysis outputs, reports, and hashes are tracked. Adapter weights and raw generations remain outside Git and do not yet have public download locations. Zenodo and `v1.1.0` release are blocked until the publication-audit issue register is closed.
