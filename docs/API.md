# API Documentation

## Overview

This document provides comprehensive API documentation for the Book Recommender application components.

## Table of Contents

- [BookRecommender](#bookrecommender)
- [Google Books API](#google-books-api)
- [Logger](#logger)
- [Analytics](#analytics)
- [UI Components](#ui-components)

---

## BookRecommender

The core recommendation engine that generates personalized book recommendations using LLM and external data sources.

### Class: `BookRecommender`

**Location**: `src/book_recommender/recommender.py`

#### Constructor

```python
BookRecommender(
    default_model: str = "llama-3.1-8b-instant",
    default_temperature: float = 0.8
)
```

**Parameters**:
- `default_model` (str): Default Groq model to use for recommendations
- `default_temperature` (float): Default LLM temperature (0.0-1.0)

**Example**:
```python
from book_recommender.recommender import BookRecommender

recommender = BookRecommender(
    default_model="llama-3.2-11b-text",
    default_temperature=0.7
)
```

#### Methods

##### `recommend()`

Generate book recommendations based on user interests.

```python
recommend(
    user_interest: str,
    genre: str = "",
    exclude_genres: str = "",
    model: str | None = None,
    temperature: float | None = None,
    force_refresh: bool = False
) -> tuple[str, str, list[dict]]
```

**Parameters**:
- `user_interest` (str): User's reading preferences and interests
- `genre` (str, optional): Preferred genre filter
- `exclude_genres` (str, optional): Comma-separated genres to exclude
- `model` (str | None, optional): Override default model
- `temperature` (float | None, optional): Override default temperature
- `force_refresh` (bool): Bypass cache and generate fresh recommendations

**Returns**:
- `tuple[str, str, list[dict]]`:
  - `recommendations` (str): Markdown-formatted recommendation text
  - `hints` (str): Google Books hints used
  - `books` (list[dict]): List of book metadata dicts

**Example**:
```python
rec_text, hints, books = recommender.recommend(
    user_interest="hopeful solarpunk with found family",
    genre="Science Fiction",
    exclude_genres="grimdark, horror",
    temperature=0.9
)

print(rec_text)
# Output: Markdown-formatted recommendations

print(len(books))
# Output: 5 (typically)

print(books[0])
# Output: {
#   'title': 'Book Title',
#   'authors': 'Author Name',
#   'description': '...',
#   'thumbnail': 'https://...',
#   'link': 'https://...'
# }
```

**Caching**:
- Recommendations are cached by (interest, genre, exclude, model, temperature)
- Use `force_refresh=True` to bypass cache
- Cache is in-memory (lost on restart)

**Error Handling**:
- Returns error message string for invalid input
- Logs errors with Sentry integration
- Handles deprecated model gracefully

##### `supported_models()`

Get list of supported Groq models.

```python
@staticmethod
supported_models() -> list[str]
```

**Returns**:
- `list[str]`: List of model names

**Example**:
```python
models = BookRecommender.supported_models()
print(models)
# Output: ['llama-3.1-8b-instant', 'llama-3.2-11b-text', 'llama-3.2-90b-text']
```

---

## Google Books API

Integration with Google Books API for external book data and recommendations.

### Function: `fetch_google_books()`

**Location**: `src/book_recommender/google_books.py`

```python
fetch_google_books(
    query: str,
    genre: str | None = None,
    max_results: int = 5
) -> list[dict[str, str]]
```

**Parameters**:
- `query` (str): Search query for books
- `genre` (str | None, optional): Genre filter
- `max_results` (int): Maximum number of results (default: 5)

**Returns**:
- `list[dict[str, str]]`: List of book metadata dictionaries with keys:
  - `title` (str): Book title
  - `authors` (str): Comma-separated author names
  - `description` (str): Book description
  - `thumbnail` (str): Cover image URL
  - `link` (str): Google Books link

**Example**:
```python
from book_recommender.google_books import fetch_google_books

books = fetch_google_books("solarpunk climate", genre="Science Fiction")

for book in books:
    print(f"{book['title']} by {book['authors']}")
    print(f"  {book['description'][:100]}...")
    print(f"  {book['link']}\n")
```

**Error Handling**:
- Returns empty list on API failure
- Logs errors but doesn't raise exceptions
- 6-second timeout per request

---

## Logger

Structured logging with contextual metadata.

### Function: `setup_logging()`

**Location**: `src/book_recommender/logger.py`

```python
setup_logging(
    level: str = "INFO",
    sentry_dsn: str | None = None,
    enable_console: bool = True,
    log_file: str | None = None
) -> logging.Logger
```

**Parameters**:
- `level` (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `sentry_dsn` (str | None): Optional Sentry DSN for error tracking
- `enable_console` (bool): Enable console logging
- `log_file` (str | None): Optional file path for logs

**Returns**:
- `logging.Logger`: Configured logger instance

**Example**:
```python
from book_recommender.logger import setup_logging

logger = setup_logging(
    level="INFO",
    sentry_dsn="https://...@sentry.io/...",
    log_file="app.log"
)

logger.info(
    "User action",
    extra={
        "query": "sci-fi adventure",
        "model": "llama-3.1-8b-instant",
        "duration_ms": 123.4
    }
)
```

### Function: `get_logger()`

Get the application logger instance.

```python
get_logger() -> logging.Logger
```

**Returns**:
- `logging.Logger`: Application logger

**Example**:
```python
from book_recommender.logger import get_logger

logger = get_logger()
logger.info("Application started")
```

---

## Analytics

Usage analytics tracking for metrics and insights.

### Class: `UsageAnalytics`

**Location**: `src/book_recommender/analytics.py`

#### Constructor

```python
UsageAnalytics(analytics_file: str | None = None)
```

**Parameters**:
- `analytics_file` (str | None): Path to analytics JSON file (default: `~/.book_recommender_analytics.json`)

#### Methods

##### `track_recommendation()`

Track a recommendation generation event.

```python
track_recommendation(
    query: str,
    genre: str | None,
    model: str,
    temperature: float,
    cached: bool,
    duration_ms: float,
    books_count: int
) -> None
```

##### `track_export()`

```python
track_export(format: str) -> None
```

##### `track_rating()`

```python
track_rating(rating: int, query: str) -> None
```

##### `track_share()`

```python
track_share(platform: str) -> None
```

##### `get_stats()`

Get aggregated usage statistics.

```python
get_stats() -> dict[str, Any]
```

**Returns**:
- `dict` with keys:
  - `total_events` (int)
  - `recommendations` (int)
  - `exports` (int)
  - `ratings` (int)
  - `shares` (int)
  - `model_usage` (dict[str, int])
  - `cache_hit_rate` (float)
  - `average_rating` (float)

**Example**:
```python
from book_recommender.analytics import get_analytics

analytics = get_analytics()
stats = analytics.get_stats()

print(f"Total recommendations: {stats['recommendations']}")
print(f"Cache hit rate: {stats['cache_hit_rate']:.1%}")
print(f"Average rating: {stats['average_rating']}/5")
```

---

## UI Components

Gradio interface components and event handlers.

### Function: `build_interface()`

**Location**: `src/book_recommender/ui.py`

```python
build_interface(
    recommender: BookRecommender
) -> tuple[gr.Blocks, str]
```

**Parameters**:
- `recommender` (BookRecommender): Initialized recommender instance

**Returns**:
- `tuple[gr.Blocks, str]`:
  - `demo` (gr.Blocks): Gradio interface
  - `css` (str): CSS styles

**Example**:
```python
from book_recommender.recommender import BookRecommender
from book_recommender.ui import build_interface

recommender = BookRecommender()
demo, css = build_interface(recommender)
demo.launch(css=css)
```

### Function: `run_app()`

**Location**: `src/book_recommender/app.py`

Main entry point to run the application.

```python
run_app() -> None
```

**Example**:
```python
from book_recommender import run_app

if __name__ == "__main__":
    run_app()
```

---

## Configuration

### Environment Variables

**Location**: `.env` file (gitignored)

Required:
- `GROQ_API_KEY`: Your Groq API key

Optional:
- `GROQ_MODEL`: Override default model
- `SENTRY_DSN`: Sentry error tracking DSN

**Example**:
```bash
GROQ_API_KEY=gsk_...
GROQ_MODEL=llama-3.2-11b-text
SENTRY_DSN=https://...@sentry.io/...
```

### Constants

**Location**: `src/book_recommender/config.py`

```python
SUPPORTED_MODELS: list[str]
DEFAULT_TEMPERATURE: float = 0.8
APP_TITLE: str
APP_SUBTITLE: str
CSS: str
```

---

## Error Handling

### Common Errors

**Empty Input**:
```python
rec, hints, books = recommender.recommend("")
# Returns: ("Please describe your interests...", "", [])
```

**NSFW Content**:
```python
rec, hints, books = recommender.recommend("explicit content")
# Returns: ("Please provide a different (non-NSFW) request.", "", [])
```

**API Error**:
```python
# Returns: ("Groq API error: ...", "", [google_books_results])
# Logs error with Sentry
```

**Deprecated Model**:
```python
# Returns: ("Selected Groq model is deprecated. Choose a supported model...", "", [])
```

---

## Testing

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=src/book_recommender

# Specific test
pytest tests/test_recommender.py::test_cache_hit
```

### Mocking

```python
def test_recommend_with_mock(monkeypatch):
    """Test recommendation with mocked API calls."""
    def mock_fetch():
        return [{"title": "Test Book", "authors": "Test Author", ...}]
    
    monkeypatch.setattr("book_recommender.google_books.fetch_google_books", mock_fetch)
    
    recommender = BookRecommender()
    rec, hints, books = recommender.recommend("test query")
    
    assert len(books) == 1
    assert books[0]["title"] == "Test Book"
```

---

## Performance

### Caching

- In-memory cache keyed by (interest, genre, exclude, model, temperature)
- Cache hits return in <1ms
- No cache persistence across restarts

### Latency

- Groq API: 200-500ms typical
- Google Books API: 200-400ms typical
- Total (uncached): 400-900ms
- Total (cached): <1ms

### Rate Limits

- Groq free tier: Generous (exact limits vary by model)
- Google Books: No API key required, public endpoint

---

## Security

### API Keys

- Store in `.env` file (gitignored)
- Never commit to repository
- Use environment variables in production

### Input Validation

- Minimum 3 characters required
- NSFW content blocked via keyword filter
- No code execution in user input

### PII

- User queries truncated in logs (50-100 chars)
- No full text logging
- LocalStorage data stays in browser

---

## Deployment

### Local

```bash
python book_recommender.py
```

### HuggingFace Spaces

```python
# app.py for Spaces
from book_recommender import run_app
run_app()
```

### Docker

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "book_recommender.py"]
```

---

## Support

- Issues: [GitHub Issues](https://github.com/OWNER/REPO/issues)
- Discussions: [GitHub Discussions](https://github.com/OWNER/REPO/discussions)
- Docs: [README.md](../README.md)
