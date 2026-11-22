# TigrinyaLens

<p align="center">
  <strong>Does AI translate all languages equally well?</strong><br/>
  An evaluation of English-to-Tigrinya and English-to-French translation.
</p>

<p align="center">
  <a href="https://colab.research.google.com/github/Abeni-style/GEREX-TigrinyaLens/blob/main/notebooks/TigrinyaLens_Colab_Demo.ipynb">
    <img alt="Open live demo in Colab" src="https://colab.research.google.com/assets/colab-badge.svg">
  </a>
  <a href="https://colab.research.google.com/github/Abeni-style/GEREX-TigrinyaLens/blob/main/notebooks/TigrinyaLens_Research.ipynb">
    <img alt="Open research notebook in Colab" src="https://img.shields.io/badge/Research_Notebook-Open_in_Colab-F9AB00?logo=googlecolab&logoColor=white">
  </a>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white">
  <img alt="Model" src="https://img.shields.io/badge/Model-NLLB--200-6B4FBB">
  <img alt="Project" src="https://img.shields.io/badge/Team-GEREX-222222">
</p>

> **Project status:** Student research prototype and interactive demonstration. TigrinyaLens is not a certified translation service.

TigrinyaLens was developed by **Team GEREX** for the **Veritas AI International High School Hackathon 2026**, in the AI + Languages track. The project received the **High Honors Award**.

The project investigates how one multilingual translation model performs on the same English test sentences when translating into Tigrinya and French. It combines automatic comparison against FLORES+ reference translations with a small, blinded review by native Tigrinya-speaking team members.

## Contents

- [Project question](#project-question)
- [Explore the project](#explore-the-project)
- [How the system works](#how-the-system-works)
- [Research design](#research-design)
- [Reported results](#reported-results)
- [Human evaluation](#human-evaluation)
- [Reproduce the experiment](#reproduce-the-experiment)
- [Run the live demo](#run-the-live-demo)
- [Repository structure](#repository-structure)
- [Limitations and responsible use](#limitations-and-responsible-use)
- [Sources and acknowledgements](#sources-and-acknowledgements)
- [FAQ](#faq)
- [Team](#team)

## Project question

**Does a multilingual AI model provide comparable translation quality across languages with different levels of digital-resource availability?**

We compare English-to-Tigrinya and English-to-French outputs from the same pretrained model, using aligned examples and the same evaluation approach. French is used as a comparison language in this experiment; the findings should not be generalized to all languages or all translation systems.

## Explore the project

[**Open the project results dashboard**](https://Abeni-style.github.io/GEREX-TigrinyaLens/) *(available after GitHub Pages is enabled for the `/docs` folder; setup instructions are below).*

| Resource | What it is |
|---|---|
| [**Live demo notebook**](notebooks/TigrinyaLens_Colab_Demo.ipynb) | Launch the interactive translator so a visitor can enter an English sentence and compare Tigrinya and French outputs. |
| [**Research notebook**](notebooks/TigrinyaLens_Research.ipynb) | Re-run dataset loading, sentence alignment, model inference, automatic metrics, low-score inspection, and the blinded human-evaluation workflow. |
| [**Python app**](app.py) | Gradio application used by the live demo. |
| [**Dependencies**](requirements.txt) | Packages needed for the live demo. |
| [**Research dependencies**](requirements-research.txt) | Packages used by the complete evaluation notebook. |

### Choose what you want to do

- **I want to try a translation:** [Launch the live demo in Google Colab](https://colab.research.google.com/github/Abeni-style/GEREX-TigrinyaLens/blob/main/notebooks/TigrinyaLens_Colab_Demo.ipynb).
- **I want to inspect or reproduce the research:** [Open the research notebook in Google Colab](https://colab.research.google.com/github/Abeni-style/GEREX-TigrinyaLens/blob/main/notebooks/TigrinyaLens_Research.ipynb).
- **I want to inspect the implementation:** open [app.py](app.py) or the [research notebook](notebooks/TigrinyaLens_Research.ipynb).

## How the system works

The project has two connected but separate workflows:

~~~mermaid
flowchart TD
    A["FLORES+ devtest split"] --> B["Align English, Tigrinya and French by sentence ID"]
    B --> C["Select 100 shared examples"]
    C --> D["NLLB-200 Distilled 600M"]
    D --> E["Greedy decoding"]
    D --> F["Beam search: 4 beams"]
    E --> G["Compare with reference translations"]
    F --> G
    G --> H["chrF and BLEU"]
    F --> I["Select 10 Tigrinya outputs"]
    I --> J["Three independent native-speaker evaluators"]
    J --> K["Compare human ratings with automatic scores"]
~~~

The **live demo** is a separate inference interface. It accepts new English text and sends it to the same model. New demo inputs are not part of the 100-sentence benchmark and do not change the research results.

### Team-added experiment

Beyond the core comparison and native-speaker review, the research notebook includes a targeted test of `no_repeat_ngram_size=3` to investigate whether a decoding constraint can reduce repetition loops. The experiment code is included in the notebook. The current published metric tables do not contain a saved before/after corpus score for this intervention, so the repository does **not** claim that it improved translation quality.

## Research design

| Component | Setting |
|---|---|
| Model | `facebook/nllb-200-distilled-600M` |
| Dataset | FLORES+ |
| Hugging Face dataset ID | `openlanguagedata/flores_plus` |
| Split | `devtest` |
| Source language | English (`eng_Latn`) |
| Target languages | Tigrinya (`tir_Ethi`) and French (`fra_Latn`) |
| Evaluation sample | 100 shared sentence IDs, aligned across all three languages |
| Sampling | Random seed 42 |
| Decoding methods | Greedy decoding (`num_beams=1`) and beam search (`num_beams=4`) |
| Primary automatic metric | chrF |
| Secondary automatic metric | BLEU |
| Baseline | English-copy negative control |

The notebook uses the pretrained model for inference. It does **not** train or fine-tune NLLB-200. The three language datasets are aligned by sentence ID so the English source examples correspond to both target-language references.

The English-copy baseline simply leaves the English sentence untranslated. It is a negative control, not a competing translation model.

## Reported results

The reported beam-search chrF scores from the experiment are:

| Target language | chrF |
|---|---:|
| Tigrinya | **25.2** |
| French | **69.0** |

**Interpretation:** chrF measures character n-gram similarity between a model output and its reference translation. These values are **not accuracy percentages** and should not be described as the percentage of sentences translated correctly.

The difference is an observation from this particular dataset, sample, model, and evaluation setup. It does not establish that every French translation is better than every Tigrinya translation, or that the same gap applies to all domains and speakers.

<details>
<summary><strong>What is chrF?</strong></summary>

chrF is an automatic text-generation metric based on character n-gram precision and recall. It can be useful for morphologically rich languages, but it remains a reference-based proxy. A valid translation can receive a lower score when it uses wording different from the single reference.

</details>

<details>
<summary><strong>What is BLEU?</strong></summary>

BLEU is a reference-based metric based on modified n-gram precision with a brevity penalty. In this project it is reported as a secondary metric. Neither BLEU nor chrF is a direct measurement of human understanding.

</details>

## Human evaluation

The team also conducted a small, blinded review of **10 NLLB-200 Tigrinya beam-search outputs**.

- **Evaluators:** three native Tigrinya-speaking team members.
- **Procedure:** all three evaluators independently assessed the same 10 outputs.
- **Blinding:** the FLORES+ reference translations and automatic chrF scores were hidden during rating.
- **Criteria:** meaning, fluency, and grammar.
- **Scale:** whole-number ratings from 1 to 5 for each criterion.
- **Assessment count:** 30 evaluator-example assessments, producing 90 criterion-level scores.
- **Reported overall mean:** **2.5 / 5**.

This is exploratory evidence from a small sample, not a representative survey of Tigrinya speakers. Human assessment and automatic metrics answer related but different questions.

## Download the recorded experiment outputs

The [results folder](results/) contains the team's recorded metrics, charts, translation examples, anonymized human ratings, and a draft write-up. Start with the [results guide](results/README.md).

| Artifact | Contents |
|---|---|
| [Automatic metrics](results/translation_metrics.csv) | chrF and BLEU by language and decoding method |
| [Baseline comparison](results/translation_metrics_with_baseline.csv) | Model results alongside the English-copy negative control |
| [chrF chart](results/chrf_comparison.png) | Visual comparison of language scores |
| [Human ratings](results/human_ratings_all.csv) | 30 anonymized ratings from three evaluators |
| [Human summary](results/human_ratings_summary.csv) | Per-example mean ratings and chrF |
| [Human/chrF correlation](results/human_chrf_correlation.csv) | Exploratory Spearman analysis |
| [Low-scoring examples](results/tigrinya_five_lowest_chrf.csv) · [French](results/french_five_lowest_chrf.csv) | Examples selected for manual inspection |
| [Experiment metadata](results/experiment_metadata.json) | Reproducibility settings and library versions |
| [Write-up draft](results/one_page_writeup_draft.md) | Automatically populated report draft |

The exact reported beam-search chrF values are 25.17 for Tigrinya and 68.97 for French (rounded to 25.2 and 69.0 in the presentation). The mean human rating was 2.50/5 across 10 unique Tigrinya translations, each independently reviewed by three evaluators. The overall mean-rating Spearman correlation was approximately 0.732 (p = 0.016, n = 10); with only ten unique examples, this is exploratory.

Some CSVs contain dataset-derived text and human assessment records. Follow the FLORES+ terms, cite the dataset, and do not redistribute data beyond what its terms allow. Individual rater contact details are not published.

## Reproduce the experiment

[**Open the research notebook in Colab**](https://colab.research.google.com/github/Abeni-style/GEREX-TigrinyaLens/blob/main/notebooks/TigrinyaLens_Research.ipynb)

1. Open the research notebook in Google Colab.
2. Select a GPU runtime if one is available. CPU execution may take substantially longer.
3. Run the setup and import cells.
4. The notebook may offer an optional Hugging Face login. The model and dataset are public resources; do not paste an access token into a code cell or commit one to GitHub.
5. Run the dataset, alignment, model inference, and evaluation cells in order.
6. Complete the blinded rating task only with the actual independent ratings from all three evaluators.
7. Review the generated tables and charts, then download the output folder if needed.

The notebook uses a fixed random seed and checks that the same 100 IDs exist in English, Tigrinya, and French. Re-running the notebook can regenerate model outputs and metrics, but results can still depend on library versions, hardware, and the exact model/dataset revision.

### Outputs generated by the research notebook

The notebook saves items such as:

- Translation metrics and baseline comparison CSV files.
- All 100 aligned source/reference/model-output rows.
- Five lowest-chrF candidate examples for each target language.
- Human-rating summaries and exploratory correlation results after the three rating files are supplied.
- chrF comparison chart and human-rating chart.
- Experiment metadata and a draft project write-up.

Low chrF examples are **candidates for manual inspection**, not automatically verified translation errors.

## Run the live demo

The live interface lets a visitor enter a new English sentence, choose a decoding method, and receive both Tigrinya and French outputs from the same NLLB-200 model.

[**Launch the demo notebook in Colab**](https://colab.research.google.com/github/Abeni-style/GEREX-TigrinyaLens/blob/main/notebooks/TigrinyaLens_Colab_Demo.ipynb)

1. Open the demo notebook.
2. Select a GPU runtime if available.
3. Run the cells from top to bottom.
4. Wait for the model to download and load.
5. Open the temporary Gradio URL printed by the app.
6. Keep the Colab runtime active while the link is in use.

### Run locally

Use Python 3.10 or newer.

~~~bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python app.py
~~~

The app opens a local Gradio address in the terminal. Public sharing is disabled by default. To intentionally create a temporary public Gradio link, set `GRADIO_SHARE=1` before launching the app. Anyone with that link may be able to access the running demo while it is active. Do not enter private or sensitive text.

## Publish the project dashboard with GitHub Pages

The interactive results dashboard is stored at `docs/index.html`. To publish it as a website:

1. Open the repository on GitHub.
2. Select **Settings**.
3. In the left sidebar, select **Pages** under **Code and automation**.
4. Under **Build and deployment**, set **Source** to **Deploy from a branch**.
5. Set the branch to **main** and the folder to **/docs**.
6. Click **Save**.
7. Wait for the Pages deployment to complete, then open [the project website](https://Abeni-style.github.io/GEREX-TigrinyaLens/).

The dashboard is a static research summary. Its **Try the live model demo** link launches the separate Colab/Gradio app; it does not run the model inside GitHub Pages.

## Repository structure

~~~text
GEREX-TigrinyaLens/
├── app.py
├── requirements.txt
├── requirements-research.txt
├── README.md
└── notebooks/
    ├── TigrinyaLens_Colab_Demo.ipynb
    └── TigrinyaLens_Research.ipynb
~~~

## Limitations and responsible use

- NLLB-200 can produce fluent-looking translations that contain meaning, grammar, or omission errors.
- Automatic metrics compare outputs with references; they do not fully measure whether a person understands the translation.
- The human evaluation covers only 10 Tigrinya outputs and three evaluators.
- The benchmark covers one model, one dataset split, one 100-example sample, and two target languages.
- The live demo's user-entered sentences are not benchmark observations.
- Results may vary with model revisions, preprocessing, decoding settings, library versions, and hardware.
- Do not rely on this prototype for medical, legal, emergency, financial, or other high-stakes translation.

## Sources and acknowledgements

- **FLORES+:** [Hugging Face dataset repository](https://huggingface.co/datasets/openlanguagedata/flores_plus)
- **NLLB-200 Distilled 600M:** [Hugging Face model card](https://huggingface.co/facebook/nllb-200-distilled-600M)
- **Libraries:** Hugging Face Datasets and Transformers, PyTorch, SacreBLEU, pandas, NumPy, Matplotlib, SciPy, and Gradio.
- **AI assistance:** ChatGPT and Gemini were used for project planning, notebook drafting, and debugging guidance. The team is responsible for reviewing, running, interpreting, and explaining the work.

Review the dataset terms and the NLLB model card's license and usage restrictions before deploying or redistributing a hosted version. The model weights are downloaded at runtime and are not stored in this repository.

## License and reuse

The original code and documentation authored for this repository by Team GEREX are released under the **MIT License**. See [LICENSE](LICENSE). This permission applies only to the project code and documentation covered by that file. It does **not** relicense or grant additional rights to the NLLB-200 model or weights, the FLORES+ dataset, third-party libraries, logos, names, or other external material. Each of those remains subject to its own license, terms, and usage restrictions. The team should verify ownership and permission for any material contributed by third parties before reusing it.

## FAQ

<details>
<summary><strong>Does running the Colab notebook automatically commit changes to GitHub?</strong></summary>

No. The notebook clones or reads the repository in a temporary Colab runtime. Running cells launches the model and demo; it does not automatically push edits to the GitHub repository.

If you edit a file and want to keep that change, use Colab's **File → Save a copy in GitHub** option where available, or commit and push the changes using Git. Review the diff before committing.

</details>

<details>
<summary><strong>Does the public Gradio link stay online permanently?</strong></summary>

No. The link is temporary and depends on the Colab session or local process staying active. It stops working when the runtime disconnects or the app shuts down.

</details>

<details>
<summary><strong>Are live demo translations included in the reported scores?</strong></summary>

No. The scores come from the fixed research evaluation. Live inputs are separate examples and do not alter the 100-example benchmark.

</details>

<details>
<summary><strong>Is this a translation service?</strong></summary>

No. It is an educational research prototype for inspecting model behaviour. Outputs are unverified and may be wrong.

</details>

## Team

**GEREX** — TigrinyaLens research project.

- Amaniel Mebrahtom
- Ambassador Girmay
- Abenezer Shebabaw

Kallamino Special High School, Ethiopia.

