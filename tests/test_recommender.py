"""Unit tests for the BookRecommender with mocks to avoid real API calls."""

import pytest

from src.book_recommender.recommender import BookRecommender


class DummyChain:
    def __init__(self, response: str):
        self._response = response

    def invoke(self, _: dict) -> str:
        return self._response


def test_recommend_returns_cached_result(monkeypatch):
    rec = BookRecommender()

    # Stub out external calls
    monkeypatch.setattr("src.book_recommender.google_books.fetch_google_books", lambda *_args, **_kwargs: [])
    monkeypatch.setattr(rec, "_build_chain", lambda *args, **kwargs: DummyChain("Result A"))

    first = rec.recommend("space opera", "Sci-Fi", "horror", "llama", 0.5)
    second = rec.recommend("space opera", "Sci-Fi", "horror", "llama", 0.5)

    assert first == second
    assert first[0] == "Result A"


def test_recommend_blocks_nsfw(monkeypatch):
    rec = BookRecommender()

    # Ensure guardrail triggers before any external calls
    called = {"google": False}
    monkeypatch.setattr(
        "src.book_recommender.google_books.fetch_google_books", lambda *_a, **_k: called.update({"google": True})
    )

    msg, hints, books = rec.recommend("nsfw content please", "", "", "llama", 0.8)

    assert "non-NSFW" in msg
    assert hints == ""
    assert books == []
    assert called["google"] is False


def test_recommend_returns_external_hints(monkeypatch):
    rec = BookRecommender()

    monkeypatch.setattr(
        "src.book_recommender.google_books.fetch_google_books",
        lambda *_a, **_k: [
            {"title": "Book One", "authors": "A", "description": "Desc", "thumbnail": "", "link": ""},
            {"title": "Book Two", "authors": "B", "description": "", "thumbnail": "", "link": ""},
        ],
    )
    monkeypatch.setattr(rec, "_build_chain", lambda *args, **kwargs: DummyChain("Result B"))

    msg, hints, books = rec.recommend("cozy mystery", "Mystery", "", "llama", 0.6)

    assert "Result B" in msg
    assert "Book One" in hints and "Book Two" in hints
    assert len(books) == 2


def test_recommend_handles_decommission(monkeypatch):
    rec = BookRecommender()

    class BoomChain:
        def invoke(self, _: dict):
            raise RuntimeError("model decommissioned")

    monkeypatch.setattr(rec, "_build_chain", lambda *args, **kwargs: BoomChain())
    monkeypatch.setattr("src.book_recommender.google_books.fetch_google_books", lambda *_a, **_k: [])

    msg, hints, books = rec.recommend("fantasy", "Fantasy", "", "llama", 0.5)

    assert "deprecated" in msg.lower()
    assert hints == ""
    assert books == []


def test_recommend_handles_generic_error(monkeypatch):
    rec = BookRecommender()

    class ErrorChain:
        def invoke(self, _: dict):
            raise RuntimeError("network down")

    monkeypatch.setattr(rec, "_build_chain", lambda *args, **kwargs: ErrorChain())
    monkeypatch.setattr("src.book_recommender.google_books.fetch_google_books", lambda *_a, **_k: [])

    msg, hints, books = rec.recommend("fantasy", "Fantasy", "", "llama", 0.5)

    assert "Groq API error" in msg
    assert hints == ""
    assert books == []
