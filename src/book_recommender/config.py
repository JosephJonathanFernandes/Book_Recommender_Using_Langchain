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
    --success: #4ade80;
    --shadow: rgba(0,0,0,0.3);
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
    --success: #22c55e;
    --shadow: rgba(0,0,0,0.08);
}
* {transition: background-color 0.2s ease, border-color 0.2s ease, color 0.2s ease, transform 0.15s ease;}
.gradio-container, body {background: radial-gradient(circle at 20% 20%, #0b1224, #050914 55%) !important; color: var(--text) !important; font-family: 'Inter', 'Segoe UI', system-ui, sans-serif !important; margin: 0; line-height: 1.6;}
:root[data-theme='light'] .gradio-container, :root[data-theme='light'] body {background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%) !important;}
.panel {background: var(--panel); border: 1px solid var(--border); border-radius: 20px; padding: 24px; box-shadow: 0 20px 40px var(--shadow); backdrop-filter: blur(10px);}
.panel ul, .panel li, .panel p {color: var(--text) !important;}
.panel ul {margin: 12px 0; padding-left: 20px;}
.panel li {margin: 8px 0; line-height: 1.5;}
.accent {color: var(--accent-strong);}
.btn-primary {background: linear-gradient(135deg,var(--accent-strong),var(--accent-2)) !important; color: #ffffff !important; font-weight: 700; border: none !important; min-height: 48px; border-radius: 12px; cursor: pointer; box-shadow: 0 4px 12px rgba(56,189,248,0.3);}
.btn-primary:hover {transform: translateY(-2px); box-shadow: 0 6px 20px rgba(56,189,248,0.4);}
.btn-primary:active {transform: translateY(0);}
.pill {display: inline-block; padding: 8px 16px; border-radius: 999px; background: linear-gradient(135deg, rgba(125,211,252,0.15), rgba(167,139,250,0.15)); color: var(--accent); font-size: 13px; font-weight: 600; margin-right: 8px; border: 1px solid var(--accent);}
.headline {font-size: 32px; font-weight: 900; color: var(--text) !important; letter-spacing: -0.5px; margin-bottom: 8px;}
.subhead {color: var(--muted) !important; margin-top: 6px; font-size: 15px; line-height: 1.6;}
.label {color: var(--muted) !important; font-size: 14px; font-weight: 600; margin-bottom: 8px;}
.cards {display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; margin-top: 16px;}
.card {background: var(--panel); border: 1px solid var(--border); border-radius: 16px; padding: 0; box-shadow: 0 8px 24px var(--shadow); overflow: hidden; min-height: 140px; cursor: pointer;}
.card:hover {transform: translateY(-4px); box-shadow: 0 12px 32px var(--shadow); border-color: var(--accent);}
.card img {width: 100%; height: 200px; object-fit: cover; margin-bottom: 0; background: linear-gradient(135deg, var(--border), var(--panel));}
.card > a {text-decoration: none; display: block;}
.card > a > div {padding: 16px;}
.card h4 {margin: 0 0 8px 0; font-size: 17px; font-weight: 700; color: var(--text) !important; line-height: 1.4;}
.card p {margin: 4px 0; color: var(--muted) !important; font-size: 13px; line-height: 1.5;}
.toolbar {display: flex; flex-wrap: wrap; gap: 12px; align-items: center; margin-top: 16px;}
.ghost-btn {background: var(--panel) !important; border: 1px solid var(--border) !important; color: var(--text) !important; border-radius: 12px; padding: 10px 16px; min-height: 48px; cursor: pointer; font-weight: 600;}
.ghost-btn:hover {background: var(--border) !important; transform: translateY(-1px);}
.ghost-btn:active {transform: translateY(0);}
.status-msg {padding: 12px; margin: 8px 0; border-radius: 8px; font-size: 14px; text-align: center; background: rgba(125,211,252,0.1); border: 1px solid var(--accent);}
input[type="text"], textarea, select {background: var(--panel) !important; border: 2px solid var(--border) !important; color: var(--text) !important; border-radius: 12px !important; padding: 12px !important; font-size: 14px !important;}
input[type="text"]:focus, textarea:focus, select:focus {border-color: var(--accent) !important; outline: none !important; box-shadow: 0 0 0 3px rgba(56,189,248,0.1) !important;}
.accordion {border: 1px solid var(--border) !important; border-radius: 12px !important; margin: 12px 0 !important;}
@media (max-width: 768px) {
  .panel {padding: 18px; border-radius: 16px;}
  .toolbar {flex-direction: column; align-items: stretch;}
  .ghost-btn, .btn-primary {width: 100%;}
  .headline {font-size: 26px;}
  .cards {grid-template-columns: 1fr;}
}
"""

def require_api_key() -> None:
    """Ensure the Groq API key is set before the app starts."""
    if not GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to a .env file or your environment before running."
        )
