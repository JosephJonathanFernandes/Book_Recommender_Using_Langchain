# Linting, Formatting, Pre-commit, and CI Recommendations

## Linting & Formatting
- **Ruff**: Fast Python linter (`ruff check src/ tests/`)
- **Black**: Code formatter (`black src/ tests/`)
- **Type hints**: Required for all public functions

## Pre-commit Hooks
- Use [pre-commit](https://pre-commit.com/) with `.pre-commit-config.yaml` (already included)
- Hooks: ruff, black, trailing-whitespace, end-of-file-fixer, ggshield (secrets)
- Install: `pre-commit install`

## CI Pipeline
- **GitHub Actions**: See `.github/workflows/ci.yml`
  - Runs on push/PR to main/master
  - Matrix: Python 3.10, 3.12
  - Steps: checkout, setup Python, install dev dependencies, lint (ruff), format check (black), run tests (pytest)
- **Coverage goal**: 80%+

## Security
- **ggshield**: Pre-commit and CI secret scanning
- **.env.example**: Never commit real secrets

---
For details, see [CONTRIBUTING.md](../CONTRIBUTING.md) and [SECURITY.md](../SECURITY.md).
