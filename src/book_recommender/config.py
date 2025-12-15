"""Configuration and styling constants for the book recommender app."""

import os
from typing import Final

from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY: Final[str | None] = os.getenv("GROQ_API_KEY")
GROQ_MODEL: Final[str] = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
SUPPORTED_MODELS: Final[list[str]] = [
    "llama-3.1-8b-instant",
    "llama-3.2-11b-text",
    "llama-3.2-90b-text",
]
DEFAULT_TEMPERATURE: Final[float] = 0.8

APP_TITLE: Final[str] = "📖 Human-Centered Book Recommender"
APP_SUBTITLE: Final[str] = (
    "Describe what you feel like reading. We blend Groq models with Google Books hints "
    "to keep recommendations grounded, concise, and spoiler-free."
)

CSS: Final[str] = r"""
:root {
    --bg: #060b16;
    --panel: #0c1526;
    --border: #1e293b;
    --text: #ffffff;
    --muted: #cbd5e1;
    --accent: #7dd3fc;
    --accent-strong: #38bdf8;
    --accent-2: #a78bfa;
}
:root[data-theme='light'] {
    --bg: #f8fafc;
    --panel: #ffffff;
    --border: #e2e8f0;
    --text: #0f172a;
    --muted: #475569;
    --accent: #0ea5e9;
    --accent-strong: #0284c7;
    --accent-2: #6366f1;
}
.gradio-container, body {background: radial-gradient(circle at 20% 20%, #0b1224, #050914 55%) !important; color: var(--text) !important; font-family: 'Inter', 'Segoe UI', system-ui, sans-serif !important; margin: 0;}
:root[data-theme='light'] .gradio-container, :root[data-theme='light'] body {background: #f1f5f9 !important;}
.panel {background: var(--panel); border: 1px solid var(--border); border-radius: 16px; padding: 18px; box-shadow: 0 18px 36px rgba(0,0,0,0.25);}
.panel ul, .panel li, .panel p {color: var(--text) !important;}
.accent {color: var(--accent-strong);}
.btn-primary {background: linear-gradient(120deg,var(--accent-strong),var(--accent-2)); color: #0b1021; font-weight: 700; border: none; min-height: 44px;}
.pill {display: inline-block; padding: 6px 10px; border-radius: 999px; background: rgba(125,211,252,0.12); color: var(--accent); font-size: 12px; margin-right: 8px;}
.headline {font-size: 26px; font-weight: 800; color: var(--text) !important;}
.subhead {color: var(--muted) !important; margin-top: 6px;}
.label {color: var(--muted) !important; font-size: 13px;}
.cards {display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px;}
.card {background: var(--panel); border: 1px solid var(--border); border-radius: 14px; padding: 12px; box-shadow: 0 10px 24px rgba(0,0,0,0.16); min-height: 120px;}
.card img {width: 100%; height: 180px; object-fit: cover; border-radius: 10px; margin-bottom: 8px; background: var(--border);}
.card h4 {margin: 6px 0; font-size: 16px; color: var(--text);}
.card p {margin: 4px 0; color: var(--muted); font-size: 13px;}
.toolbar {display: flex; flex-wrap: wrap; gap: 10px; align-items: center;}
.ghost-btn {background: transparent; border: 1px solid var(--border); color: var(--text); border-radius: 10px; padding: 10px 12px; min-height: 44px;}
@media (max-width: 768px) {
  .panel {padding: 14px;}
  .toolbar {flex-direction: column; align-items: stretch;}
  .ghost-btn, .btn-primary {width: 100%;}
}
"""

def require_api_key() -> None:
    """Ensure the Groq API key is set before the app starts."""
    if not GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to a .env file or your environment before running."
        )
