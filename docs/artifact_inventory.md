# Artifact inventory

| Artifact | Path | Git | Hash | Release availability |
|---|---|---:|---:|---|
| English final set | `data/final/test_en.jsonl` | Yes | Yes | Source archive |
| Russian final set | `data/final/test_ru.jsonl` | Yes | Yes | Source archive |
| Original Kazakh set | `data/final/test_kk.jsonl` | Yes | Yes | Historical source archive; translation-confounded |
| Corrected Kazakh review draft | `data/translation/review/kazakh_v2_review_draft.jsonl` | Yes | In correction log | Not an approved evaluation artifact |
| Kazakh native-review worksheet | `reports/translation_audits/kazakh_v2_native_review.csv` | Yes | Git object hash | Pending 300-row human approval |
| Historical-manifest qualification | `data/final/multilingual_manifest_audit_v1_1.json` | Yes | Git object hash | Source archive |
| Corrected Kazakh set | `data/final/test_kk_v2.jsonl` | Pending | Required | Blocked on native review |
| Control-v2 adapter | `outputs/adapters/v2/control/final` | No | Yes | Zenodo external-artifact archive |
| Selective-v2 adapter | `outputs/adapters/v2/selective_correction/final` | No | Yes | Zenodo external-artifact archive |
| Raw Stage 19 outputs | `results/final_multilingual_v1/` | No | Yes | Zenodo external-artifact archive |
| Corrected Kazakh outputs | `results/corrected_kazakh_v2/` | No | Required | Pending sensitivity run |
| Historical run manifests | `reports/evaluation_runs/final_multilingual_v1/` | Yes | Provenance report | Source archive |
| Analysis outputs | `reports/final_analysis/` | Yes | Yes | Source archive |
| Multilingual manifest | `data/final/multilingual_manifest.json` | Yes | Yes | Source archive |

The Zenodo DOI and final download URLs are added only after a deposit is
reserved. Until then, no document claims that ignored artifacts are publicly
downloadable. Use `scripts/build_zenodo_bundles.sh` after the readiness checker
passes.
