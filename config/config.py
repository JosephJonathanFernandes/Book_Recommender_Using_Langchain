import os
from dotenv import load_dotenv

class Config:
    """Centralized configuration loader for Book Recommender."""
    def __init__(self):
        load_dotenv()
        self.google_books_api_key = os.getenv("GOOGLE_BOOKS_API_KEY", "")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        # Add more config as needed

    def validate(self):
        if not self.google_books_api_key:
            raise ValueError("GOOGLE_BOOKS_API_KEY is required. See .env.example.")

config = Config()
