# Final Statistical Analysis

## Dataset

- 300 aligned stems, 3 languages, 3 model conditions, and 10,800 branch records.

## Primary paired pressure-loss effect

- en: mean 0.007; 95% bootstrap CI [-0.007, 0.020]; selective/control/unchanged stems 3/1/296.
- ru: mean -0.003; 95% bootstrap CI [-0.017, 0.010]; selective/control/unchanged stems 2/3/295.
- kk: mean -0.017; 95% bootstrap CI [-0.050, 0.020]; selective/control/unchanged stems 10/16/274.

No three-language macro-average is reported while the original Kazakh translation set remains under correction.

## Limitations

- One base model and adapter configuration; English-only SFT; machine-assisted translations; and small denominators for initially incorrect answers when factual accuracy is high.
- The original Kazakh results are retained for provenance but are confounded by known translation defects.
