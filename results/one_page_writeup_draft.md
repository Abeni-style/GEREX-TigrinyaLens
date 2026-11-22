# TigrinyaLens: Testing English-to-Tigrinya Translation Quality

Track: AI + Languages
Team: GEREX — Amaniel Mebrahtom, Ambassador Girmay, Abenezer Shebabaw
Dataset: openlanguagedata/flores_plus, devtest split
Model: facebook/nllb-200-distilled-600M (pretrained inference; no fine-tuning)

## The problem
Tigrinya speakers may rely on machine translation to understand information originally written in English. A fluent-looking output can still change or omit meaning. We investigate the translation quality of one multilingual model and whether an automatic character-overlap metric reflects judgments by Tigrinya speakers.

## What we built
TigrinyaLens translates the same 100 English sentences into Tigrinya and French using NLLB-200. We compare greedy decoding and beam-4 decoding against professional FLORES+ references. The intended user is a Tigrinya-speaking student or community member seeking to understand English text. This is an evaluation prototype, not a guarantee of translation correctness.

## What we added
Three Tigrinya-speaking team members independently reviewed 10 blinded Tigrinya translations for meaning, fluency, and grammar (1-5 scale). We compared the average human scores with sentence-level chrF using Spearman rank correlation and categorized the most frequent translation errors. We also tested `no_repeat_ngram_size=3` as a targeted decoding constraint for repetition loops. The notebook contains this experiment, but no saved before/after corpus score is included in the published result tables, so we do not claim a measured improvement.

## How it works
Data: 100 paired English sentences and corresponding French and Tigrinya references from the devtest split of openlanguagedata/flores_plus.
Model: facebook/nllb-200-distilled-600M.
Evaluation: chrF (primary), BLEU (secondary), greedy decoding, beam search, and an English-copy negative control.

## Results
| Language | Method | chrF | BLEU |
|---|---|---:|---:|
| Tigrinya | English-copy negative control | 0.66 | 0.27 |
| French | English-copy negative control | 25.90 | 1.67 |
| Tigrinya | Greedy decoding | 23.61 | 3.03 |
| Tigrinya | Beam search (4 beams) | 25.17 | 3.98 |
| French | Greedy decoding | 67.56 | 45.39 |
| French | Beam search (4 beams) | 68.97 | 47.00 |

Human evaluation (10 blinded examples, 3 native Tigrinya raters):
- Average scores (1-5 scale): Meaning = 2.47, Fluency = 2.27, Grammar = 2.77, Overall Mean = 2.50 / 5.00.
- Exploratory Spearman correlation with sentence-level chrF: rho = 0.732 (p = 0.016, n = 10).
- Most frequent rater error categories: addition and mistranslation (2), Mistranslation, omission, addition, terminology (2), grammatical error (2).

Lowest-chrF Tigrinya candidate inspected (ID 687, sentence chrF = 1.06):
- English source: Blogs can also help improve student writing. While students often begin their blog experience with sloppy grammar and spelling, the presence of an audience generally changes that.
- NLLB-200 beam output: ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻት ብሉጻ
- FLORES+ reference: ብሎጋት ከምኡውን ናይ ተማሃሮ ናይ ምጽሓፍ ክእለት ንምምሕያሽ ክሕግዙ ይኽእሉ። ተማሃሮ ብዙሕ ጊዜ ናይ ብሎግ ክእለቶም፥ ሰዋሰው ከምኡውን ፣ ናይ ዕዱማት ምንባር ብሓፈሻ እቲ ነገር ይቕይሮ።
- Team verification: The model output repeats a single Tigrinya word over and over instead of translating the sentence, so almost none of the English meaning was preserved. This is a real translation failure (a repetition loop), not just different wording from the reference, which is why the sentence-level chrF is near zero.

## What we would do next
Evaluate more sentences, involve additional independent Tigrinya speakers, inspect more domains, and test additional translation models.

## Sources
- FLORES+: https://huggingface.co/datasets/openlanguagedata/flores_plus
- NLLB-200 model: https://huggingface.co/facebook/nllb-200-distilled-600M
- Hugging Face Datasets and Transformers; PyTorch; SacreBLEU; pandas; NumPy; Matplotlib; SciPy; Gradio.
- AI assistance: ChatGPT and Gemini were used for project planning, notebook drafting, and debugging guidance. The team reviewed and ran the code and completed all human evaluations independently.
