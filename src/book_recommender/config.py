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

def require_api_key() -> None:
    """Ensure the Groq API key is set before the app starts."""
    if not GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to a .env file or your environment before running."
        )
