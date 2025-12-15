"""Application bootstrap for the book recommender."""

from .config import GROQ_MODEL, require_api_key
from .recommender import BookRecommender
from .ui import build_interface


def run_app() -> None:
    require_api_key()
    recommender = BookRecommender(default_model=GROQ_MODEL)
    demo, css = build_interface(recommender)
    demo.launch(css=css)


__all__ = ["run_app"]
