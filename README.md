# Book Recommender (LangChain + Gradio + Groq)

Human-centered book recommender with Groq LLMs, Google Books grounding, and a transparent Gradio UI.

## Requirements
- Python 3.10–3.12 recommended (LangChain shows pydantic v1 warnings on 3.14).
- Install deps:
   ```bash
   pip install -r requirements.txt
   ```
   For contributors: `pip install -r requirements-dev.txt` and `pre-commit install`.

> Note: LangChain currently shows a warning on Python 3.14 due to pydantic v1 compatibility. For a quieter experience, use Python 3.10–3.12.

## Setup
1. Copy the example env and set your key:
   ```bash
   cp .env.example .env
   # edit .env to add GROQ_API_KEY
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run
```bash
python book_recommender.py
```
Gradio opens locally. Enter interests, pick model/temperature, and you'll see both recommendations and the Google Books hints used for grounding.

## Development
- Lint/format: `pre-commit run --all-files` (ruff + black + hygiene hooks)
- Tests: `pytest`
- Secrets scanning: `pre-commit run ggshield --all-files`
- CI: GitHub Actions runs ruff, black --check, and pytest on push/PR (Python 3.10 & 3.12)

## Notes
- Default model: `llama-3.1-8b-instant` (change via UI or `GROQ_MODEL`).
- Guardrails: spoiler-averse, NSFW-filtered, cached per input/settings.
- Transparency: Google Books hints shown alongside results; no key needed.
- Structure: modular app in `src/book_recommender/` with a thin entrypoint `book_recommender.py`.
- Deployment: works on Hugging Face Spaces or any Python host; ensure env vars are set.
