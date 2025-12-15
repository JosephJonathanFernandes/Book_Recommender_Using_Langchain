import os
from typing import Dict, List, Optional, Tuple

import gradio as gr
import requests
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

CSS = """
:root {
    --bg: #060b16;
    --panel: #0c1526;
    --border: #1e293b;
    --text: #e2e8f0;
    --muted: #94a3b8;
    --accent: #7dd3fc;
    --accent-strong: #38bdf8;
    --accent-2: #a78bfa;
}
body {background: radial-gradient(circle at 20% 20%, #0b1224, #050914 55%); color: var(--text); font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;}
.panel {background: var(--panel); border: 1px solid var(--border); border-radius: 14px; padding: 18px; box-shadow: 0 20px 40px rgba(0,0,0,0.35);}
.accent {color: var(--accent-strong);}
.btn-primary {background: linear-gradient(120deg,var(--accent-strong),var(--accent-2)); color: #0b1021; font-weight: 700; border: none;}
.pill {display: inline-block; padding: 6px 10px; border-radius: 999px; background: rgba(125,211,252,0.12); color: var(--accent); font-size: 12px; margin-right: 8px;}
.headline {font-size: 26px; font-weight: 800; color: var(--text);}
.subhead {color: var(--muted); margin-top: 6px;}
.label {color: var(--muted); font-size: 13px;}
"""

# Load environment variables from .env when present
load_dotenv()
GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")
# Default to a currently supported Groq model; override via GROQ_MODEL in .env
GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is not set. Add it to a .env file or your environment before running."
    )

# Simple in-memory cache keyed by query + options
CACHE: Dict[str, Tuple[str, str]] = {}


def cache_key(interest: str, genre: str, exclude_genres: str, model: str, temperature: float) -> str:
    return "|".join(
        [
            interest.strip().lower(),
            genre.strip().lower(),
            exclude_genres.strip().lower(),
            model.strip().lower(),
            f"{temperature:.2f}",
        ]
    )


def fetch_google_books(query: str, genre: str, max_results: int = 3) -> List[str]:
    """Fetch a few Google Books suggestions to blend with LLM output."""
    search_terms = query
    if genre:
        search_terms += f" subject:{genre}"
    try:
        resp = requests.get(
            "https://www.googleapis.com/books/v1/volumes",
            params={"q": search_terms, "maxResults": max_results},
            timeout=6,
        )
        resp.raise_for_status()
        data = resp.json()
        items = data.get("items", [])
        results: List[str] = []
        for item in items[:max_results]:
            info = item.get("volumeInfo", {})
            title = info.get("title") or "Unknown title"
            authors = ", ".join(info.get("authors", [])[:2]) or "Unknown author"
            desc = (info.get("description") or "").split(".")[:2]
            desc_text = ". ".join(desc).strip()
            snippet = f"{title} by {authors}"
            if desc_text:
                snippet += f" — {desc_text[:200]}"
            results.append(snippet)
        return results
    except Exception:
        return []


def build_chain(model: str, temperature: float):
    chat_llm = ChatGroq(
        temperature=temperature,
        groq_api_key=GROQ_API_KEY,
        model=model,
    )

    prompt = ChatPromptTemplate.from_template(
        "You are a careful, spoiler-free book recommendation assistant.\n"
        "- Avoid NSFW content.\n"
        "- Do not include plot spoilers.\n"
        "- Keep each reason concise.\n"
        "- Prefer diverse, high-quality picks.\n"
        "- Respect excluded genres.\n"
        "- Blend relevant external suggestions when helpful.\n\n"
        "User interests: {user_interest}\n"
        "Preferred genre: {genre}\n"
        "Excluded genres: {exclude_genres}\n"
        "External suggestions: {external_suggestions}\n\n"
        "Return exactly 5 numbered Markdown lines like:\n"
        "1. **Title** — brief reason (no spoilers)"
    )

    return prompt | chat_llm | StrOutputParser()


def guardrails(user_interest: str) -> Optional[str]:
    blocked = ["nsfw", "porn", "explicit", "gore"]
    text = user_interest.lower()
    if any(bad in text for bad in blocked):
        return "Please provide a different (non-NSFW) request."
    return None


def recommend_books(
    user_interest: str,
    genre: str,
    exclude_genres: str,
    model: str,
    temperature: float,
) -> Tuple[str, str]:
    """Generate five book recommendations with caching and guardrails."""
    if not user_interest or not user_interest.strip():
        return "Please describe your interests to get recommendations.", ""

    violation = guardrails(user_interest)
    if violation:
        return violation, ""

    key = cache_key(user_interest, genre, exclude_genres, model, temperature)
    if key in CACHE:
        return CACHE[key]

    external = fetch_google_books(user_interest, genre)
    external_text = "\n".join([f"- {item}" for item in external]) if external else "- No Google Books hints for this query."

    try:
        chain = build_chain(model, temperature)
        result = chain.invoke(
            {
                "user_interest": user_interest.strip(),
                "genre": genre.strip(),
                "exclude_genres": exclude_genres.strip(),
                "external_suggestions": external_text,
            }
        )
    except Exception as exc:  # pragma: no cover - API/network issues
        msg = str(exc).lower()
        if "decommissioned" in msg:
            return (
                "Selected Groq model is deprecated. Choose a supported model in the dropdown "
                "and try again.",
                "",
            )
        return f"Groq API error: {exc}", ""

    CACHE[key] = (result, external_text)
    return result, external_text


with gr.Blocks() as demo:
    gr.Markdown("<div class='pill'>HCD-first</div>", elem_id="pill-top")
    gr.Markdown(
        "<div class='headline'>📖 Human-Centered Book Recommender</div>"
        "<div class='subhead'>Describe what you feel like reading. We'll blend Groq models with Google Books hints to keep it grounded, concise, and spoiler-free.</div>"
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
                    choices=[
                        "llama-3.1-8b-instant",
                        "llama-3.2-11b-text",
                        "llama-3.2-90b-text",
                    ],
                    value=GROQ_MODEL,
                    scale=2,
                )
                temperature_slider = gr.Slider(
                    minimum=0.0,
                    maximum=1.0,
                    value=0.8,
                    step=0.05,
                    label="Temperature",
                    scale=1,
                )

            btn = gr.Button("Recommend!", elem_classes=["btn-primary"])
            output = gr.Markdown(label="Recommendations", value="")
            external_view = gr.Markdown(label="Google Books hints", value="", elem_classes=["label"])

            btn.click(
                fn=recommend_books,
                inputs=[user_input, genre_dropdown, exclude_genres, model_dropdown, temperature_slider],
                outputs=[output, external_view],
                queue=True,
            )

if __name__ == "__main__":
    demo.launch(css=CSS)
