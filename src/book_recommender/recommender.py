"""Core recommendation logic and chaining."""

from __future__ import annotations

from typing import Dict, Tuple

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from .config import DEFAULT_TEMPERATURE, GROQ_API_KEY, SUPPORTED_MODELS
from .google_books import fetch_google_books


class BookRecommender:
    """Encapsulates caching, guardrails, and LLM invocation."""

    def __init__(self, default_model: str = SUPPORTED_MODELS[0], default_temperature: float = DEFAULT_TEMPERATURE) -> None:
        self.default_model = default_model
        self.default_temperature = default_temperature
        self.cache: Dict[str, Tuple[str, str]] = {}

    @staticmethod
    def _cache_key(interest: str, genre: str, exclude_genres: str, model: str, temperature: float) -> str:
        return "|".join(
            [
                interest.strip().lower(),
                genre.strip().lower(),
                exclude_genres.strip().lower(),
                model.strip().lower(),
                f"{temperature:.2f}",
            ]
        )

    @staticmethod
    def _guardrails(user_interest: str) -> str | None:
        blocked = ["nsfw", "porn", "explicit", "gore"]
        text = user_interest.lower()
        if any(bad in text for bad in blocked):
            return "Please provide a different (non-NSFW) request."
        return None

    @staticmethod
    def _build_chain(model: str, temperature: float):
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

    def recommend(
        self,
        user_interest: str,
        genre: str,
        exclude_genres: str,
        model: str | None = None,
        temperature: float | None = None,
    ) -> Tuple[str, str]:
        """Generate five book recommendations and the external hints used."""
        if not user_interest or not user_interest.strip():
            return "Please describe your interests to get recommendations.", ""

        violation = self._guardrails(user_interest)
        if violation:
            return violation, ""

        model_name = model or self.default_model
        temp = temperature if temperature is not None else self.default_temperature

        key = self._cache_key(user_interest, genre, exclude_genres, model_name, temp)
        if key in self.cache:
            return self.cache[key]

        external = fetch_google_books(user_interest, genre)
        external_text = "\n".join([f"- {item}" for item in external]) if external else "- No Google Books hints for this query."

        try:
            chain = self._build_chain(model_name, temp)
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
                    "Selected Groq model is deprecated. Choose a supported model in the dropdown and try again.",
                    "",
                )
            return f"Groq API error: {exc}", ""

        self.cache[key] = (result, external_text)
        return result, external_text

    @staticmethod
    def supported_models() -> list[str]:
        return SUPPORTED_MODELS
