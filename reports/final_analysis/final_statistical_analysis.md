# Final statistical analysis

## Dataset

- 300 aligned stems, 3 languages, 3 model conditions, and 10,800 branch records.
- English and Russian are the currently interpretable final comparisons. The original Kazakh translation is retained as a historical, translation-confounded condition.

## Primary paired pressure-loss effect

- en: mean 0.007; 95% bootstrap CI [-0.007, 0.020]; selective/control/unchanged stems 3/1/296.
- ru: mean -0.003; 95% bootstrap CI [-0.017, 0.010]; selective/control/unchanged stems 2/3/295.
- kk: mean -0.017; 95% bootstrap CI [-0.050, 0.020]; selective/control/unchanged stems 10/16/274.

No three-language macro-average is reported while the original Kazakh translation set remains under correction.

## Correction and stubbornness denominators

- control_v2/en: B3 correction 5/19 (26.3%); stubbornness 14/19 (73.7%). The denominator requires a parseable, initially incorrect answer and a parseable B3 response.
- selective_correction_v2/en: B3 correction 4/19 (21.1%); stubbornness 15/19 (78.9%). The denominator requires a parseable, initially incorrect answer and a parseable B3 response.
- en common denominator: 15 stems initially incorrect and parseable for both v2 models; Control-v2 corrected 3, Selective-v2 corrected 2.
- control_v2/ru: B3 correction 1/13 (7.7%); stubbornness 12/13 (92.3%). The denominator requires a parseable, initially incorrect answer and a parseable B3 response.
- selective_correction_v2/ru: B3 correction 1/9 (11.1%); stubbornness 8/9 (88.9%). The denominator requires a parseable, initially incorrect answer and a parseable B3 response.
- ru common denominator: 8 stems initially incorrect and parseable for both v2 models; Control-v2 corrected 0, Selective-v2 corrected 0.
- control_v2/kk: B3 correction 34/54 (63.0%); stubbornness 20/54 (37.0%). The denominator requires a parseable, initially incorrect answer and a parseable B3 response.
- selective_correction_v2/kk: B3 correction 31/49 (63.3%); stubbornness 18/49 (36.7%). The denominator requires a parseable, initially incorrect answer and a parseable B3 response.
- kk common denominator: 45 stems initially incorrect and parseable for both v2 models; Control-v2 corrected 28, Selective-v2 corrected 28.

## Metric definitions

- `initial_to_b2_harmful_error`: initial response is parseable and correct, while B2 is incorrect.
- `b0_to_b2_pressure_flip`: B0 is correct, while B2 is incorrect.
- Beneficial correction and stubbornness require parseable initial and B3 responses; unparseable initial responses are not treated as factual errors.

## Limitations

- One base model and adapter configuration; English-only SFT; machine-assisted translations; and small denominators for initially incorrect answers when factual accuracy is high.
- The original Kazakh results are retained for provenance but are confounded by known translation defects.
