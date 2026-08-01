# Final project report

## Completion

Stages 1 through 21 are complete. The project constructed and audited the data, trained matched v1 and v2 adapters, ran development diagnostics, translated and froze the final set, completed 10,800 locked branch evaluations, and produced deterministic paired analysis.

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

V1 showed that a model can appear resistant by refusing to revise any answer. V2 restored factual capability and avoided the most severe preservation shortcut. It did not deliver a reliable primary benefit: the Control-minus-Selective pressure-loss effect was +0.7 pp in English, -0.3 pp in Russian, and -1.7 pp in Kazakh; the macro-average was -0.4 pp, and all language confidence intervals contained zero. Kazakh was descriptively more pressure-sensitive for both v2 models.

## Deviations

The original plan proceeded directly from v1 to multilingual evaluation. Development results exposed stubbornness, so the project added a documented diagnosis, a balanced v2 intervention, and a second development gate. Translation used Google Translate GTX for drafts under an explicit amendment, followed by human semantic and structural review.

## Release readiness

Core datasets, configurations, scripts, manifests, analysis outputs, reports, and hashes are tracked. Adapter weights and raw generations remain outside Git; their hashes are recorded. The repository is ready for a tagged research release after the final audit.
