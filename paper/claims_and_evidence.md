# Claims and evidence

| Claim | Evidence | Strength |
|---|---|---|
| V1 learned indiscriminate preservation | Control-v1 and Anti-v1 lost factual capability and rejected 36/37 and 22/22 correct-feedback opportunities | Strong |
| The shared balanced v2 transition design restored factual capability relative to v1 | Development B0 accuracy recovered to 99% and 98% for Control-v2 and Selective-v2 | Strong within this model and training setup |
| Selective-v2 slightly reduced English pressure loss | Paired effect +0.7 pp, CI includes zero | Weak |
| Selective-v2 improved pressure resistance | English +0.7 pp and Russian -0.3 pp; both CIs include zero | Not supported |
| English-only behavioral training transferred reliably | No clear Selective-v2 benefit was established in English or Russian | Not demonstrated |
| The original Kazakh condition exhibited larger pressure loss | V2 pressure loss was 17.7-19.3 pp on the original Kazakh translations versus 1.0-2.0 pp in English/Russian | Descriptive only; known translation defects prevent clean attribution |
| Selective-v2 improved pressure resistance on the corrected Kazakh sensitivity run | Control-minus-Selective paired effect was -1.0 pp, 95% CI -4.3 to 2.3 pp | Not supported |
| V2 avoided the near-total v1 stubbornness failure on corrected Kazakh | B3 beneficial correction was 32/52 for Control-v2 and 31/47 for Selective-v2 | Supported descriptively |
| Balanced transitions prevented v1-level capability collapse | Both v2 adapters recovered high B0 accuracy | Supported |
| V2 established reliable correction selectivity | Parseable initially incorrect denominators were small and B3 correction did not consistently favor Selective-v2 | Not supported |

Central claim: the shared balanced v2 transition design repaired the v1 capability collapse. Explicit selective-feedback training did not show a reliable pressure-resistance advantage over the matched Control-v2 condition.

Publication-audit qualification: the balanced transition design was shared by
both v2 conditions, so capability restoration is attributed to that shared
design rather than to explicit selective feedback. The study did not establish
a clear Selective-v2 benefit in English; transfer of such a benefit to Russian
or Kazakh was therefore not demonstrated. The original Kazakh result remains
historical. The separately labeled corrected sensitivity run also did not
favor Selective-v2, and it does not replace the locked result.
Full sensitivity results are in
`reports/corrected_kazakh_v2_analysis.md`.
