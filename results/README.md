# TigrinyaLens research artifacts

These files are outputs from the team's recorded FLORES+ / NLLB-200 experiment. They are provided to make the reported analysis easier to inspect.

## Main automatic results

- `translation_metrics.csv` — chrF and BLEU for greedy and beam-search decoding.
- `translation_metrics_with_baseline.csv` — the same model results plus the English-copy negative control.
- `chrf_comparison.png` — chart of corpus chrF scores.
- `experiment_metadata.json` — dataset, model, sample size, decoding and environment details.

The reported beam-search corpus chrF scores are 25.17 for Tigrinya and 68.97 for French (rounded in the presentation to 25.2 and 69.0). These are similarity scores, not accuracy percentages.

## Translation examples

- `all_translations.csv` — 100 English inputs, model outputs, and reference translations for both target languages.
- `tigrinya_five_lowest_chrf.csv` and `french_five_lowest_chrf.csv` — five lowest-scoring candidate examples per language.

A low chrF score is a prompt for human inspection; it does not by itself prove an incorrect translation. These files contain dataset-derived text. Reuse or redistribution must follow the FLORES+ terms and attribution requirements.

## Human evaluation

- `human_ratings_all.csv` — 30 anonymized evaluator-example assessments: three evaluators independently rated the same 10 unique Tigrinya translations.
- `human_ratings_summary.csv` — per-example averages and the associated reference/chrF for analysis.
- `human_chrf_correlation.csv` — exploratory Spearman correlations between human ratings and sentence-level chrF.
- `human_error_categories.csv` — evaluator-reported error categories.
- `human_rating_vs_chrf.png` — scatter plot of human ratings against sentence-level chrF.
- `human_evaluation_templates.zip` — blank blinded rating sheets and instructions for future replications.

The reported overall mean human rating was 2.50/5. The overall mean-rating correlation with sentence-level chrF was approximately rho = 0.732 (p = 0.016, n = 10). Because the human review contains only 10 unique translations, treat these statistics as exploratory rather than conclusive.

The individual raters are labelled Rater 1, Rater 2 and Rater 3. Their personal contact details are not included in the current published files.

## Draft report

- `one_page_writeup_draft.md` — report draft populated from the recorded experiment outputs. Review it before reuse or submission.

## Additional decoding experiment

The research notebook also tests `no_repeat_ngram_size=3` as a targeted intervention for repeated phrase loops. The code is present in the notebook, but the current published metric tables do not contain a saved before/after corpus score for this intervention. Do not describe it as a demonstrated improvement without rerunning and recording that comparison.
