# Book Recommender (LangChain + Gradio + Groq)

A richer Gradio app with an HCD-focused UI that asks for your reading interests and uses a Groq-powered LangChain prompt, blended with Google Books hints, to recommend five books with short reasons.

## Requirements
- Python 3.9+
- `pip install langchain langchain-groq gradio python-dotenv requests`

> Note: LangChain currently shows a warning on Python 3.14 due to pydantic v1 compatibility. For a quieter experience, use Python 3.10–3.12.

## Setup
1. Create a `.env` file in the project root:
   ```
   GROQ_API_KEY="your_groq_api_key_here"
   GROQ_MODEL="llama-3.1-8b-instant"  # optional override; choose a supported model
   ```
2. Install dependencies:
   ```bash
   pip install langchain langchain-groq gradio python-dotenv requests
   ```

## Run
```bash
python book_recommender.py
```
Gradio will open a local browser tab. Enter a short description of your interests, pick a model/temperature, and press "Recommend!". You'll see both the recommendations and the Google Books hints that were blended into the prompt for transparency.

## Notes
- Default model is `llama-3.1-8b-instant`; choose another supported Groq model in the dropdown or via `GROQ_MODEL`.
- Temperature slider controls creativity; lower for safer picks.
- Google Books suggestions are blended for extra grounding; no key required for the public endpoint used here.
- Basic guardrails: spoiler-avoidant and NSFW-filtered; also caches responses per input/settings to save calls.
- To deploy, you can host on Hugging Face Spaces or any service that supports running a Python web app.
