# TigrinyaLens

**Does AI translate all languages equally well?**

TigrinyaLens is a student research project by **Team GEREX** comparing English-to-Tigrinya and English-to-French translation using Meta's NLLB-200 Distilled 600M model. The project combines automatic evaluation with a small human review of Tigrinya outputs.

> **Project status:** Research prototype and interactive demonstration. This is not a certified translation service.

## Repository contents

- `app.py` - Gradio app for live English-to-Tigrinya and English-to-French translation.
- `notebooks/TigrinyaLens_Colab_Demo.ipynb` - Google Colab launcher for the interactive app.
- `requirements.txt` - Python dependencies.

## Try the demo

[**Open the notebook in Google Colab**](https://colab.research.google.com/github/Abeni-style/GEREX-TigrinyaLens/blob/main/notebooks/TigrinyaLens_Colab_Demo.ipynb)

1. Open the notebook in Colab.
2. Select a GPU runtime if one is available.
3. Run each cell from top to bottom.
4. Open the temporary Gradio URL printed by the final cell.
5. Keep the Colab runtime active while the demo is being used.

The first run downloads the NLLB-200 model. CPU execution is supported, but may be slow.

### Run locally

Use Python 3.10 or newer.

~~~bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
~~~

Open the local Gradio address shown in your terminal. Public sharing is disabled by default. To deliberately create a temporary public Gradio link, set GRADIO_SHARE=1 before starting the app. Anyone with that link may be able to use the running demo, so only enable it when needed.

## What visitors can test

1. Enter an English sentence.
2. Select Greedy Search or Beam Search.
3. Generate Tigrinya and French outputs from the same NLLB-200 model.
4. Compare both outputs side by side.
5. Read the reported findings, method, and limitations.

Live inputs are demonstration examples. They are **not** added to the original evaluation set and do not change the reported research scores.

## Reported findings

| Measure | Tigrinya | French |
|---|---:|---:|
| chrF, reported beam-search run | **25.2** | **69.0** |

These are chrF similarity scores, **not accuracy percentages**. They indicate character n-gram similarity against the reference translations used in the experiment. They do not mean that the model is correct 25.2% or 69.0% of the time.

### Human review of Tigrinya outputs

- 10 unique Tigrinya translations were reviewed.
- 3 native Tigrinya-speaking evaluators independently rated the same 10 items.
- This produced 30 individual ratings.
- The reported average was **2.5 out of 5**.

This is a small exploratory review. It should not be presented as representative of all Tigrinya speakers, dialects, or topics.

## Experimental setup

- **Model:** facebook/nllb-200-distilled-600M
- **Source language:** English (eng_Latn)
- **Target languages:** Tigrinya (tir_Ethi) and French (fra_Latn)
- **Evaluation set:** 100 English test sentences with corresponding reference translations
- **Decoding methods:** Greedy Search and Beam Search
- **Automatic metrics:** chrF and BLEU
- **Additional analyses:** English-copy baseline and inspection of low-scoring translations

## Dataset citation verification required

The earlier experiment code shared by the team referenced the Hugging Face dataset loader facebook/flores, while the hackathon submission's credits listed FLORES+. These labels should not be treated as interchangeable. Before claiming exact reproducibility, inspect the original executed notebook, identify the dataset and configuration actually loaded, and update the final report, notebook, and credits to cite that exact source. This repository deliberately does not guess which citation is correct.

## Limitations and responsible use

- A fluent-looking translation may still change or omit the source meaning.
- Automatic metrics such as chrF and BLEU are proxies and cannot replace native-speaker review.
- The human review covers only 10 Tigrinya outputs and three evaluators.
- Results depend on the test data, reference translations, preprocessing, and decoding settings.
- Live user-entered sentences are not benchmark results.
- Do not rely on this prototype for medical, legal, emergency, or other high-stakes translation.

## Model

The app downloads facebook/nllb-200-distilled-600M from Hugging Face at runtime. Review the [model card and its license/usage restrictions](https://huggingface.co/facebook/nllb-200-distilled-600M) before deploying or redistributing a hosted version. No model weights are stored in this repository.

## Team

**GEREX** - TigrinyaLens research project.
