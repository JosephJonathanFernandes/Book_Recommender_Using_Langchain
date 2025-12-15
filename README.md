# 📚 AI Book Recommender

> **Your personal AI librarian powered by Groq's lightning-fast LLMs**

Stop drowning in endless book lists. Get personalized recommendations that actually match your taste—no more "top 10 books everyone's reading" nonsense.

## ✨ What Makes This Different?

- **🚀 Blazing Fast**: Groq LLMs deliver recommendations in <1 second
- **🎯 Actually Personal**: Tell us your mood, favorite tropes, or that oddly specific thing you're looking for
- **📖 Real Books**: Grounded in Google Books API—no hallucinated titles
- **🎨 Beautiful UI**: Dark mode, smooth animations, export to PDF, share on social
- **🔒 Privacy First**: Your reading list stays in your browser (LocalStorage), no backend tracking
- **📊 Transparent**: See exactly what hints the AI used and how it thinks

## 🎮 Features

### Core Experience
- **Smart Recommendations**: Genre filtering, exclusions, temperature control
- **Google Books Integration**: Real covers, links, descriptions
- **Export**: Download as JSON or PDF for later
- **Reading List**: Save books you're interested in (stored locally)
- **Rating System**: 5-star feedback helps you track what worked
- **Social Sharing**: Tweet, post to Facebook, or share on LinkedIn

### Developer Features
- **Structured Logging**: Context-rich logs with query/model/duration tracking
- **Usage Analytics**: Track recommendation patterns, cache hit rates, ratings
- **Error Monitoring**: Optional Sentry integration for production
- **Comprehensive Docs**: API docs, ADRs, contributing guidelines

## 🚀 Quick Start

### 1. Get a Groq API Key
Sign up at [console.groq.com](https://console.groq.com) (free tier is generous)

### 2. Install
```bash
# Clone the repo
git clone <your-repo-url>
cd book_recommender_using_ai

# Set up environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# Install dependencies
pip install -r requirements.txt
```

### 3. Run
```bash
python book_recommender.py
```

Visit `http://localhost:7860` and start exploring! 🎉

## 💡 Usage Examples

**Vibe-based search**:
> "cozy fantasy with found family, no romance, cottagecore vibes"

**Mood matching**:
> "something hopeful to read after a rough week"

**Specific tropes**:
> "science fiction with time loops and competent protagonists"

**Anti-recommendations**:
> "literary fiction but NOT depressing, exclude books about dying"

## 🛠️ Development

### Setup
```bash
pip install -r requirements-dev.txt
pre-commit install
```

### Testing
```bash
# Run all tests
pytest

# With coverage
pytest --cov=src/book_recommender

# Watch mode
pytest-watch
```

### Code Quality
```bash
# Lint & format
pre-commit run --all-files

# Just formatting
black src/ tests/

# Just linting
ruff check src/ tests/
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📚 Documentation

- **[API Documentation](docs/API.md)**: Complete API reference for all components
- **[Contributing Guide](CONTRIBUTING.md)**: Setup, testing, code style, PR process
- **[Architecture Decisions](docs/adr/)**: Why we made the technical choices we did

## 🏗️ Architecture

```
book_recommender_using_ai/
├── book_recommender.py          # Entry point
├── src/book_recommender/
│   ├── app.py                   # App initialization
│   ├── recommender.py           # Core recommendation logic
│   ├── google_books.py          # Google Books API integration
│   ├── ui.py                    # Gradio interface
│   ├── config.py                # Constants and CSS
│   ├── logger.py                # Structured logging
│   └── analytics.py             # Usage tracking
└── tests/                       # Test suite
```

**Key Design Decisions**:
- [Why Groq over OpenAI?](docs/adr/002-groq-api-selection.md) → Speed + cost
- [Why Gradio over Streamlit?](docs/adr/003-gradio-ui-framework.md) → Rapid prototyping
- [Why LocalStorage?](docs/adr/004-local-storage-persistence.md) → Privacy-first
- [Why structured logging?](docs/adr/005-structured-logging.md) → Production observability

## 🔧 Configuration

### Environment Variables
```bash
# Required
GROQ_API_KEY=gsk_...

# Optional
GROQ_MODEL=llama-3.2-11b-text    # Override default model
SENTRY_DSN=https://...            # Error tracking
```

### Supported Models
- `llama-3.1-8b-instant` (default) - Fast, balanced
- `llama-3.2-11b-text` - Better quality, slightly slower
- `llama-3.2-90b-text` - Highest quality, slower

## 📊 Analytics & Observability

Track how your recommendations perform:
- Cache hit rates
- Model usage patterns
- Average ratings
- Export frequency

View stats in `~/.book_recommender_analytics.json`

## 🚢 Deployment

### Hugging Face Spaces
```python
# Works out of the box - just set GROQ_API_KEY in Space settings
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

## 🤝 Contributing

We love contributions! Check out [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- Code style guide
- Testing requirements
- PR process

## 📄 License

MIT (or your preferred license)

## 🙏 Acknowledgments

Built with:
- [Groq](https://groq.com) - Lightning-fast LLM inference
- [Gradio](https://gradio.app) - Beautiful ML interfaces
- [Google Books API](https://developers.google.com/books) - Book metadata

---

**Made with ❤️ for book lovers who are tired of generic recommendations**
