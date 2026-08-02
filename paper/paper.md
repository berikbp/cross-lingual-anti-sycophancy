# When anti-sycophancy training becomes stubbornness: a multilingual study in English, Russian, and Kazakh

> **Publication-audit notice:** this historical report includes results from
> the original Kazakh translation set. A later audit identified substantive
> translation defects and a labeling mismatch in a secondary harmful-change
> metric. The metric labels and denominators have since been corrected; the
> primary pressure-loss calculation was unaffected. Kazakh interpretation still
> requires correction before publication. See `reports/publication_audit_v1_0.md`.

## Abstract

Large language models sometimes abandon correct answers when users confidently suggest incorrect alternatives. We test whether supervised fine-tuning can reduce this behavior and whether any improvement transfers from English to Russian and Kazakh. We evaluate a 4B instruction model with paired multiple-choice interactions containing neutral reconsideration, doubt, incorrect suggestions, and correct suggestions.

Our first intervention rewarded preservation of correct initial answers. It eliminated harmful changes on a development set, but factual accuracy fell and the adapters became almost completely unwilling to accept correct feedback. We then trained fresh adapters on balanced transitions containing correct and incorrect initial answers as well as correct and incorrect feedback. This restored factual capability and reduced the severe stubbornness seen in v1.

On the locked English and Russian evaluations, Selective-v2 did not clearly outperform its matched Control-v2 adapter. The paired pressure-loss effect was +0.7 percentage points in English and -0.3 in Russian, and both bootstrap confidence intervals included zero. The original Kazakh translation set produced a -1.7-point effect, but known translation defects prevent clean interpretation; that result is retained as historical evidence pending a corrected sensitivity run. Reducing answer changes is therefore not sufficient evidence of better alignment. The shared balanced transition design repaired a shortcut, but an explicit selective-feedback benefit was not established.

## 1. Introduction

Factual sycophancy occurs when a model changes an answer to agree with a user's stated belief even when that belief is wrong. The behavior is easy to measure in multiple-choice settings, but the obvious metric can mislead. A model that never revises itself will resist incorrect pressure perfectly while also rejecting valid corrections.

This distinction motivated three questions. Can matched anti-sycophancy SFT reduce pressure-induced factual changes? Does an English-trained effect transfer to Russian and Kazakh? Can the model resist bad feedback while accepting good feedback? Kazakh is especially useful here because multilingual alignment studies rarely include it and because weaker base-language capability may interact with social pressure.

We contribute matched control and intervention adapters, a documented stubbornness failure, a balanced redesign, and locked paired English and Russian analyses with artifact hashes. The original Kazakh evaluation is retained as a translation-confounded historical analysis. The main result is negative but informative: the redesign repaired capability and stubbornness, yet explicit selective feedback did not improve the currently interpretable primary comparisons.

## 2. Related work

Prior work on sycophancy has examined agreement with user beliefs, answer changes after challenges such as "are you sure?", and synthetic preference or instruction data intended to improve resistance. Multilingual work asks whether alignment behavior learned in a high-resource language transfers to languages with different training coverage. Our experiment connects these questions to correction selectivity. We treat resistance and willingness to update as separate properties rather than assuming that fewer answer changes are always better.

## 3. Problem formulation

Each stem receives one initial answer. Four independent branches then start from that same conversational state: B0 asks for neutral reconsideration, B1 expresses doubt, B2 confidently suggests an assigned wrong option, and B3 confidently suggests the correct option.

We define pressure loss as `Accuracy(B0) - Accuracy(B2)`. Harmful flips are B0-correct stems that become incorrect under B2. Exact wrong adoption records whether B2 equals the assigned suggestion. For initially incorrect answers, beneficial correction is a correct B3 response and stubbornness is a remaining incorrect response. We also report parseability, neutral self-correction, and answer preservation. A zero pressure loss is desirable only when it does not come from indiscriminate preservation.

## 4. Experimental setup

The base model is Qwen/Qwen3-4B-Instruct-2507 at frozen revision `cdbee75f17c01a7cc42f958dc650907174af0554`. Both conditions use 4-bit NF4 QLoRA, rank 8, alpha 16, dropout 0.05, three epochs, an effective batch size of eight, and identical seeds. Loss is applied only to the final assistant turn. Evaluation used greedy decoding with frozen generation settings, branches are independent, and the final checkpoint is selected without evaluation-based checkpoint choice.

## 5. Data

The English master pool contains 400 verified questions across mathematics, science, computer science, geography, and logic. A fixed-seed split produced 300 test and 100 reserve stems with balanced answer positions. The final test was translated into Russian and Kazakh from machine-assisted drafts. The first review preserved stem order and answer metadata but failed to detect several substantive Kazakh defects. The original Kazakh results are therefore retained with a translation-quality limitation pending a complete native review and separately labeled sensitivity evaluation. Development, training, validation, master, final, and reserve sets were kept separate.

## 6. V1 intervention and failure

Every v1 training example began with a correct assistant answer and supervised the same answer after a neutral or misleading follow-up. The simplest rule was to copy the previous answer. On development, B0 accuracy was 93% for the base model, 63% for Control-v1, and 78% for Anti-v1. Control-v1 rejected 36 of 37 correct-feedback opportunities; Anti-v1 rejected all 22. Their zero B2 pressure loss was produced by stubbornness, not selective reasoning.

## 7. V2 selective-correction intervention

V2 reused the verified stems but balanced four transition types: correct initial/wrong feedback (CW), wrong initial/correct feedback (WC), correct initial/correct feedback (CC), and wrong initial/wrong feedback (WW). Each category contributed 250 training examples. Initial correctness and feedback correctness were both balanced 50/50. Control-v2 used neutral reconsideration while Selective-v2 received explicit feedback; initial answers, final targets, ordering, masking, and all training settings matched. Both adapters started from the base model rather than v1.

## 8. Development results

V2 restored development capability: B0 accuracy reached 99% for Control-v2 and 98% for Selective-v2. This was enough to rule out the v1 collapse, but it left only one and two initially incorrect cases respectively. Development therefore supplied little evidence about correction acceptance and justified only cautious progression to the locked test.

## 9. Locked final results

Control-v2 pressure loss was 1.7 points in English and 1.7 in Russian. Selective-v2 loss was 1.0 and 2.0 points. The paired Control-minus-Selective effect was +0.7 points in English (95% bootstrap CI -0.7 to 2.0) and -0.3 in Russian (-1.7 to 1.0). Neither interval excluded zero.

On the original Kazakh translation set, Control-v2 and Selective-v2 pressure loss was 17.7 and 19.3 points, with a paired effect of -1.7 points (-5.0 to 2.0). These historical numbers are not combined with English and Russian because known translation defects prevent clean interpretation.

Both v2 adapters were fully parseable on B0 and B2. For Control-v2 and Selective-v2 respectively, initial-to-B2 harmful errors were 3/281 versus 3/280 in English and 1/269 versus 2/254 in Russian. B0-to-B2 pressure flips were 5/283 versus 4/284 in English and 5/285 versus 7/284 in Russian. Exact wrong adoption is reported separately for initially correct and B0-correct denominators in the results tables. The available results do not support a general Selective-v2 advantage.

Correction denominators differed because initial accuracy differed by condition and language. Selective-v2 corrected 5/20 initially wrong English cases, 33/46 Russian cases, and 89/111 Kazakh cases under B3. Control-v2 corrected 5/19, 19/31, and 68/91. These descriptive results show that v2 was not universally frozen, but they do not isolate a causal selectivity benefit because the denominators are model-specific.

## 10. Discussion

V1 demonstrates a measurement failure: resistance can be faked by never changing an answer. V2 repaired that shortcut and restored factual performance, but repair did not guarantee an intervention benefit. The primary comparison was near zero overall and inconsistent by language.

The models exhibited substantially larger pressure loss on the original Kazakh translation set. Known translation defects and lower language capability prevent clean attribution to pressure sensitivity, model knowledge, or language representation. The original result is descriptive and will be reported alongside a separately named corrected-Kazakh sensitivity analysis rather than silently replaced.

## 11. Limitations

We used one base model, one model size, one LoRA configuration, and one training seed. The task is multiple-choice factual QA rather than open-ended conversation. Training was English-only. Russian and Kazakh evaluations were produced from machine-assisted translations. The initial Kazakh review did not detect several substantive defects. V2 was designed after observing the v1 development failure. Initially incorrect denominators were small when accuracy was high. The prompts use weak explicit pressure rather than authority or real-world stakes. Translation-specific effects and unequal language capability remain possible confounds.

## 12. Conclusion

Naive anti-sycophancy SFT reduced answer changes by making the model stubborn. The shared balanced v2 transition design repaired the v1 capability collapse, but explicit selective-feedback training did not provide clear evidence of improved pressure resistance over a matched control on the locked multilingual evaluation. Future interventions should measure both resistance to incorrect feedback and willingness to accept valid correction.
