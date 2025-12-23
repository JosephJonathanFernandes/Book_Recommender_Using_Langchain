# Architecture Overview

## Problem Statement
Book Recommender provides intelligent, personalized book recommendations using modern LLM and search APIs. It is designed for extensibility, security, and production-readiness.

## Architecture
- **src/**: Core logic, modularized by responsibility
- **config/**: Configuration and environment setup
- **scripts/**: Automation and utility scripts
- **tests/**: Unit and integration tests
- **docs/**: Design, API, and architecture documentation

### Key Modules
- `app.py`: Application entrypoint
- `recommender.py`: Recommendation engine (SOLID, testable)
- `google_books.py`: External API integration
- `ui.py`: User interface logic
- `analytics.py`: Usage analytics (optional)
- `config.py`: Centralized configuration loader
- `logger.py`: Structured logging

## Design Principles
- Separation of concerns
- SOLID, DRY, Clean Code
- Secure by default (no hardcoded secrets)
- Extensible and testable

## Ownership
- Each module has a clear owner and responsibility
- Contributions follow the guidelines in CONTRIBUTING.md

## Extensibility
- Add new recommenders, data sources, or UIs by following the modular structure

---
For more details, see docs/ and inline code comments.
