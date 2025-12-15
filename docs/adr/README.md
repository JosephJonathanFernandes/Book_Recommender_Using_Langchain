# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) for the Book Recommender project.

## What is an ADR?

An Architecture Decision Record (ADR) is a document that captures an important architectural decision made along with its context and consequences.

## ADR Format

Each ADR follows this structure:

- **Title**: Short descriptive title
- **Status**: Proposed | Accepted | Deprecated | Superseded
- **Date**: When the decision was made
- **Context**: What is the issue that we're seeing that is motivating this decision?
- **Decision**: What is the change that we're proposing and/or doing?
- **Consequences**: What becomes easier or more difficult to do because of this change?

## ADR List

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [001](001-modular-architecture.md) | Modular Package Architecture | Accepted | 2025-12-15 |
| [002](002-groq-api-selection.md) | Use Groq API for LLM | Accepted | 2025-12-15 |
| [003](003-gradio-ui-framework.md) | Gradio for UI Framework | Accepted | 2025-12-15 |
| [004](004-local-storage-persistence.md) | Browser LocalStorage for Persistence | Accepted | 2025-12-15 |
| [005](005-structured-logging.md) | Structured Logging with Context | Accepted | 2025-12-15 |

## Creating a New ADR

1. Copy the [template](000-template.md)
2. Name it with the next number: `NNN-short-title.md`
3. Fill in all sections
4. Submit as part of your PR
5. Update the table above

## References

- [Michael Nygard's ADR article](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [ADR GitHub organization](https://adr.github.io/)
