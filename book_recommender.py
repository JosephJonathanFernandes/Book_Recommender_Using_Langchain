"""Entry point to run the Gradio app."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.append(str(SRC))

from book_recommender import run_app


if __name__ == "__main__":
    run_app()
