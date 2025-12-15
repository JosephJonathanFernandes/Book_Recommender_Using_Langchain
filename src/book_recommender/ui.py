"""Gradio UI assembly for the book recommender."""

import gradio as gr

from .config import APP_SUBTITLE, APP_TITLE, CSS
from .recommender import BookRecommender


def build_interface(recommender: BookRecommender) -> gr.Blocks:
    with gr.Blocks(css=CSS) as demo:
        gr.Markdown("<div class='pill'>HCD-first</div>", elem_id="pill-top")
        gr.Markdown(
            f"<div class='headline'>{APP_TITLE}</div>"
            f"<div class='subhead'>{APP_SUBTITLE}</div>"
        )

        with gr.Row():
            with gr.Column(scale=1, elem_classes=["panel"]):
                gr.Markdown(
                    "<div class='label'>Quick guide</div>\n"
                    "<ul>\n"
                    "  <li>Describe vibe, pace, themes, or comps.</li>\n"
                    "  <li>Pick a genre or exclude some.</li>\n"
                    "  <li>Adjust temperature for creativity.</li>\n"
                    "  <li>We show Google Books hints for transparency.</li>\n"
                    "</ul>\n"
                    "<div class='label'>Guardrails</div>\n"
                    "- Spoiler-averse, no NSFW.\n"
                    "- Cached per input/settings to save calls.\n"
                    "- Model list mirrors Groq supported options."
                )

            with gr.Column(scale=2, elem_classes=["panel"]):
                user_input = gr.Textbox(
                    label="Your interests",
                    placeholder="e.g., hopeful solarpunk with found family and science-forward detail",
                    lines=4,
                )
                genre_dropdown = gr.Dropdown(
                    label="Preferred genre (optional)",
                    choices=["", "Fantasy", "Science Fiction", "Mystery", "Romance", "Thriller", "Nonfiction", "Historical"],
                    value="",
                )
                exclude_genres = gr.Textbox(
                    label="Exclude genres (comma separated)",
                    placeholder="e.g., grimdark, horror",
                )
                with gr.Row():
                    model_dropdown = gr.Dropdown(
                        label="Groq model",
                        choices=recommender.supported_models(),
                        value=recommender.default_model,
                        scale=2,
                    )
                    temperature_slider = gr.Slider(
                        minimum=0.0,
                        maximum=1.0,
                        value=recommender.default_temperature,
                        step=0.05,
                        label="Temperature",
                        scale=1,
                    )

                btn = gr.Button("Recommend!", elem_classes=["btn-primary"])
                output = gr.Markdown(label="Recommendations", value="")
                external_view = gr.Markdown(label="Google Books hints", value="", elem_classes=["label"])

                btn.click(
                    fn=recommender.recommend,
                    inputs=[user_input, genre_dropdown, exclude_genres, model_dropdown, temperature_slider],
                    outputs=[output, external_view],
                    queue=True,
                )

    return demo
