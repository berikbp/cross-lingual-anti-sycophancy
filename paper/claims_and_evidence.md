# Claims and evidence

| Claim | Evidence | Strength |
|---|---|---|
| V1 learned indiscriminate preservation | Control-v1 and Anti-v1 lost factual capability and rejected 36/37 and 22/22 correct-feedback opportunities | Strong |
| Balanced v2 training restored factual capability | Development B0 accuracy recovered to 99% and 98% | Strong |
| Selective-v2 slightly reduced English pressure loss | Paired effect +0.7 pp, CI includes zero | Weak |
| Selective-v2 improved multilingual pressure resistance | Macro effect -0.4 pp; all language CIs include zero | Not supported |
| English-only behavioral training transferred reliably | Russian and Kazakh did not favor Selective-v2 | Not supported |
| The original Kazakh condition exhibited larger pressure loss | V2 pressure loss was 17.7-19.3 pp on the original Kazakh translations versus 1.0-2.0 pp in English/Russian | Descriptive only; known translation defects prevent clean attribution |
| Balanced transitions prevented v1-level collapse | V2 capability and correction behavior were substantially better than v1 | Supported |

Central claim: balanced selective-correction supervision prevented the severe stubbornness produced by naive answer-preservation training, but did not yield a clear reduction in multilingual pressure-induced answer changes.

Publication-audit qualification: the balanced transition design was shared by
both v2 conditions, so capability restoration is attributed to that shared
design rather than to explicit selective feedback. The study did not establish
a clear Selective-v2 benefit in English; transfer of such a benefit to Russian
or Kazakh was therefore not demonstrated. Original Kazakh results remain
historical and require a corrected-translation sensitivity analysis.
