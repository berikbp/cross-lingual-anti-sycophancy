# Kazakh v2 review record

The corrected Kazakh sensitivity dataset contains 300 records in the same
order as the frozen English test. Six defects identified during publication
audit were corrected before review. The corrected text is stored in
`data/final/test_kk_v2.jsonl`, and the before/after changes are recorded in
`reports/translation_audits/kazakh_v2_known_corrections.json`.

Berik Satybaldy reviewed the 300-record corrected artifact on 2026-08-02 and
attested to semantic equivalence, answer preservation, distractor
preservation, and Kazakh language quality. The compact, hash-bound attestation
is stored in
`reports/translation_audits/kazakh_v2_review_attestation.json`.

The release does not include a redundant 300-row approval worksheet. The
attestation is bound to the exact reviewed JSONL by SHA-256. The finalizer
rejects a changed dataset or incomplete attestation.

Freeze and verify the reviewed artifact with:

```bash
uv run python -m src.translation.finalize_kazakh_v2
sha256sum -c docs/kazakh_v2_artifact_hashes.txt
```

The corrected evaluation remains separately labeled and does not overwrite
the historical Stage 19 Kazakh results.
