# Final project report

## Completion

The original 21-stage experiment and the post-audit corrections are complete. A publication audit identified substantive defects in the original Kazakh translations and an ambiguity in secondary harmful-change metrics. The historical data and results remain frozen. The corrected Kazakh artifact, separate sensitivity run, and revised secondary metrics are versioned alongside them rather than replacing them.

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
- Corrected Kazakh sensitivity conditions: 3
- Corrected Kazakh sensitivity records: 3,600

## Findings

V1 showed that a model can appear resistant by refusing to revise any answer. The shared v2 transition design restored factual capability and avoided the most severe preservation shortcut. Explicit selective feedback did not deliver a reliable primary benefit in the currently interpretable English and Russian comparisons: the Control-minus-Selective pressure-loss effect was +0.7 pp in English and -0.3 pp in Russian, and both confidence intervals contained zero.

The original Kazakh evaluation is retained as a historical result but is confounded by known translation defects. In the corrected translation-and-prompt sensitivity run, Control-v2 pressure loss was 18.7 pp and Selective-v2 loss was 19.7 pp. The paired effect was -1.0 pp (95% bootstrap CI -4.3 to 2.3 pp). This separately named run also does not support a Selective-v2 pressure-resistance benefit. Because both translations and prompt wording changed, it does not isolate either component. See `reports/corrected_kazakh_v2_analysis.md`.

The corrected run did not reproduce v1-level stubbornness: B3 beneficial correction was 32/52 for Control-v2 and 31/47 for Selective-v2. This supports the narrower conclusion that the shared v2 transition design repaired the severe preservation shortcut, not that explicit selective feedback improved pressure resistance.

## Deviations

The original plan proceeded directly from v1 to multilingual evaluation. Development results exposed stubbornness, so the project added a documented diagnosis, a balanced v2 intervention, and a second development gate. Translation used Google Translate GTX for drafts under an explicit amendment. The initial Kazakh review failed to detect substantive semantic and language defects.

## Release readiness

Core datasets, configurations, scripts, manifests, analysis outputs, reports,
and hashes are tracked. Release metadata, code/data licenses, a strengthened
provenance validator, and a supplemental-artifact bundler are now present.
Adapter weights and raw generations remain outside Git and are published as
checksummed release assets by the Zenodo packaging workflow.

The scientific correction gate is closed. The release checker verifies the
historical and corrected datasets, raw outputs, analyses, manifests, licenses,
and citation metadata before archival bundles are built.
