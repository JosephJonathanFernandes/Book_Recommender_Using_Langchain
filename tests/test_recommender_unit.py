import pytest
from src.book_recommender.recommender import BookRecommender

def test_recommend_returns_error_for_empty_input():
    recommender = BookRecommender()
    result, hints, books = recommender.recommend("")
    assert "Please describe your interests" in result
    assert books == []
