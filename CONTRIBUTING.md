# Contributing to Book Recommender

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Code Style](#code-style)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. Please be respectful and considerate in all interactions.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/book_recommender_using_ai.git
   cd book_recommender_using_ai
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/book_recommender_using_ai.git
   ```

## Development Setup

### Prerequisites

- Python 3.10+ (tested on 3.10 and 3.12)
- Git
- A Groq API key (get one at [console.groq.com](https://console.groq.com))

### Installation

1. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements-dev.txt
   ```

3. **Set up environment variables**:
   ```bash
   # Copy the example .env file
   cp .env.example .env
   
   # Add your Groq API key to .env
   GROQ_API_KEY=your_api_key_here
   ```

4. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

## Making Changes

1. **Create a new branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Make your changes** following the code style guidelines

3. **Test your changes** thoroughly:
   ```bash
   # Run tests
   pytest
   
   # Run linters
   ruff check .
   black --check .
   ```

4. **Commit your changes** using conventional commit format (see below)

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/book_recommender --cov-report=html

# Run specific test file
pytest tests/test_recommender.py
```

### Writing Tests

- Place tests in the `tests/` directory
- Use descriptive test names: `test_<what>_<condition>_<expected>`
- Use fixtures and mocks to avoid external dependencies
- Aim for >80% code coverage

Example:
```python
def test_recommend_returns_error_for_empty_input(recommender):
    """Test that empty input returns appropriate error message."""
    result, hints, books = recommender.recommend("")
    assert "Please describe your interests" in result
    assert books == []
```

## Code Style

This project uses:

- **Black** for code formatting (line length: 100)
- **Ruff** for linting (rules: E, F, I, B, UP, SIM)
- **Type hints** for all function signatures
- **Docstrings** for all public functions and classes

### Style Guidelines

- Use descriptive variable names
- Keep functions focused and small
- Add type hints to all function parameters and returns
- Write docstrings in Google style format
- Use f-strings for string formatting
- Keep imports organized (stdlib, third-party, local)

Example:
```python
def recommend(
    self, 
    user_interest: str, 
    genre: str = "", 
    temperature: float = 0.8
) -> tuple[str, str, list[dict]]:
    """
    Generate book recommendations based on user interests.
    
    Args:
        user_interest: Description of what user wants to read
        genre: Optional preferred genre
        temperature: LLM temperature (0.0-1.0)
    
    Returns:
        Tuple of (recommendations, hints, books)
    """
    ...
```

## Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/):

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes

### Examples

```bash
feat(ui): add dark mode toggle

Add theme toggle radio button that switches between dark and light modes
using CSS custom properties.

Closes #123
```

```bash
fix(recommender): handle None values in genre parameter

The cache key generation was failing when genre was None. Now properly
handles None by converting to empty string.
```

## Pull Request Process

1. **Update your branch** with latest upstream changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request** on GitHub with:
   - Clear title following commit conventions
   - Description of changes made
   - Reference to related issues (if any)
   - Screenshots for UI changes

4. **Wait for review**:
   - CI checks must pass (linting, tests)
   - At least one approval required
   - Address any feedback from reviewers

5. **Merge**:
   - Once approved, the PR will be merged
   - You can delete your feature branch

## Reporting Issues

### Bug Reports

Include:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)
- Error messages/logs
- Screenshots if applicable

### Feature Requests

Include:
- Clear description of the feature
- Use case and benefits
- Possible implementation approach
- Examples or mockups if applicable

## Project Structure

```
book_recommender_using_ai/
├── src/book_recommender/     # Main package
│   ├── __init__.py
│   ├── analytics.py          # Usage analytics
│   ├── app.py                # Application entry point
│   ├── config.py             # Configuration and CSS
│   ├── google_books.py       # Google Books API
│   ├── logger.py             # Structured logging
│   ├── recommender.py        # Core recommendation logic
│   └── ui.py                 # Gradio UI
├── tests/                    # Test suite
├── .github/workflows/        # CI/CD
├── book_recommender.py       # CLI entry point
├── pyproject.toml           # Project metadata
├── requirements.txt         # Runtime dependencies
└── requirements-dev.txt     # Development dependencies
```

## Getting Help

- Check existing [issues](https://github.com/OWNER/REPO/issues)
- Read the [README](README.md)
- Review [documentation](docs/)

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing! 🎉
