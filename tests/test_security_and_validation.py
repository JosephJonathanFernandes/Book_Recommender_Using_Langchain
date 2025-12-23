import pytest
from src.book_recommender.recommender import BookRecommender

@pytest.fixture
def recommender():
    return BookRecommender()

def test_recommend_blocks_nsfw(recommender):
    msg, hints, books = recommender.recommend("nsfw content please", "", "", "llama", 0.8)
    assert "non-NSFW" in msg
    assert hints == ""
    assert books == []

def test_recommend_returns_error_for_empty_input(recommender):
    result, hints, books = recommender.recommend("")
    assert "Please describe your interests" in result
    assert books == []
