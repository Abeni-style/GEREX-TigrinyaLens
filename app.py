import os

import gradio as gr
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

MODEL_NAME = "facebook/nllb-200-distilled-600M"
SOURCE_LANGUAGE = "eng_Latn"
TARGET_LANGUAGES = {"Tigrinya": "tir_Ethi", "French": "fra_Latn"}
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Loading {MODEL_NAME} on {DEVICE}...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.src_lang = SOURCE_LANGUAGE
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to(DEVICE)
model.eval()
print("Model loaded.")


def translate_one(text: str, target_language: str, decoding: str) -> str:
    """Translate one English sentence with NLLB-200."""
    if not isinstance(text, str) or not text.strip():
        return "Enter an English sentence to begin."
    if target_language not in TARGET_LANGUAGES:
        return "Choose a supported target language."

    target_id = tokenizer.convert_tokens_to_ids(TARGET_LANGUAGES[target_language])
    num_beams = 1 if decoding == "Greedy Search" else 4
    inputs = tokenizer(
        text.strip(), return_tensors="pt", truncation=True, max_length=512
    ).to(DEVICE)

    with torch.inference_mode():
        generated = model.generate(
            **inputs,
            forced_bos_token_id=target_id,
            num_beams=num_beams,
            max_new_tokens=256,
        )
    return tokenizer.batch_decode(generated, skip_special_tokens=True)[0]


def compare_translations(text: str, decoding: str):
    if not isinstance(text, str) or not text.strip():
        message = "Enter an English sentence to begin."
        return message, message
    try:
        return (
            translate_one(text, "Tigrinya", decoding),
            translate_one(text, "French", decoding),
        )
    except Exception as exc:
        error = f"Translation failed: {type(exc).__name__}: {exc}"
        return error, error


with gr.Blocks(title="TigrinyaLens | GEREX", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """# TigrinyaLens
### Does AI translate all languages equally well?
Interactive research demonstration by **Team GEREX**"""
    )
    with gr.Tab("Try the model"):
        gr.Markdown(
            "Enter an English sentence. The same NLLB-200 model translates it "
            "into Tigrinya and French using your selected decoding method."
        )
        english_input = gr.Textbox(
            label="English input",
            placeholder="Education creates opportunities for everyone.",
            lines=3,
        )
        decoding_choice = gr.Radio(
            ["Greedy Search", "Beam Search"],
            value="Beam Search",
            label="Decoding method",
        )
        run_button = gr.Button("Run comparison", variant="primary")
        with gr.Row():
            tigrinya_output = gr.Textbox(label="Tigrinya output", lines=5)
            french_output = gr.Textbox(label="French output", lines=5)
        run_button.click(
            compare_translations,
            inputs=[english_input, decoding_choice],
            outputs=[tigrinya_output, french_output],
        )
        gr.Examples(
            examples=[
                ["Education creates opportunities for everyone."],
                ["The students are learning together at school."],
                ["Language technology should work for every community."],
            ],
            inputs=english_input,
        )
        gr.Markdown(
            "**Note:** These are live model outputs, not verified translations. "
            "A fluent-looking sentence can still contain meaning errors."
        )

    with gr.Tab("Our research results"):
        gr.Markdown(
            """## Automatic evaluation

| Measure | Tigrinya | French |
|---|---:|---:|
| chrF, reported beam-search run | **25.2** | **69.0** |

These are chrF similarity scores, not accuracy percentages.

## Human review

- 10 unique Tigrinya translations were reviewed.
- 3 native Tigrinya-speaking evaluators independently rated the same 10 items.
- 30 individual ratings in total.
- Reported average: **2.5 out of 5**.

This is a small exploratory review, not a large-scale evaluation.

## Experimental setup

- Model: NLLB-200 Distilled 600M
- Source: English (eng_Latn)
- Targets: Tigrinya (tir_Ethi) and French (fra_Latn)
- Evaluation set: 100 English test sentences with reference translations
- Decoding: Greedy Search and Beam Search
- Automatic metrics: chrF and BLEU
- Additional analyses: English-copy baseline and low-scoring output inspection

The reported scores show a difference in similarity to the reference translations in this experiment. They do not establish accuracy for every sentence, speaker, dialect, or topic. The human review is limited in size."""
        )

    with gr.Tab("Method and limitations"):
        gr.Markdown(
            """## How it works

1. A user enters an English sentence.
2. The NLLB-200 tokenizer prepares the input.
3. NLLB-200 generates Tigrinya and French outputs.
4. Both outputs are displayed side by side.

## Limitations

- This is a model demonstration, not a certified translation service.
- A judge's live input is not part of the original evaluation set.
- Live inputs do not change the reported research scores.
- Human review covered only 10 Tigrinya outputs.
- Translation quality can vary by sentence, subject, spelling, and dialect.
- Do not use this prototype for high-stakes translation."""
        )
    gr.Markdown("---\n**GEREX | TigrinyaLens** - facebook/nllb-200-distilled-600M")


if __name__ == "__main__":
    # Public sharing is opt-in. Set GRADIO_SHARE=1 to create a temporary link.
    share_demo = os.getenv("GRADIO_SHARE", "0").strip().lower() in {
        "1", "true", "yes"
    }
    demo.launch(share=share_demo, show_error=True)
