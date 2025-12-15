"""Structured logging configuration for the book recommender app."""

import logging
import sys
from datetime import datetime
from typing import Any, Dict, Optional

try:
    import sentry_sdk
    from sentry_sdk.integrations.logging import LoggingIntegration
    SENTRY_AVAILABLE = True
except ImportError:
    SENTRY_AVAILABLE = False


class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured JSON-like logs."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with structured data."""
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add extra context if available
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        if hasattr(record, "query"):
            log_data["query"] = record.query
        if hasattr(record, "model"):
            log_data["model"] = record.model
        if hasattr(record, "cached"):
            log_data["cached"] = record.cached
        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Format as readable structured log
        parts = [f"{log_data['timestamp']} [{log_data['level']}] {log_data['message']}"]
        
        context_items = []
        if "query" in log_data:
            context_items.append(f"query={log_data['query'][:50]}")
        if "model" in log_data:
            context_items.append(f"model={log_data['model']}")
        if "cached" in log_data:
            context_items.append(f"cached={log_data['cached']}")
        if "duration_ms" in log_data:
            context_items.append(f"duration={log_data['duration_ms']}ms")
        
        if context_items:
            parts.append(f" | {', '.join(context_items)}")
        
        if "exception" in log_data:
            parts.append(f"\n{log_data['exception']}")
        
        return "".join(parts)


def setup_logging(
    level: str = "INFO",
    sentry_dsn: Optional[str] = None,
    enable_console: bool = True,
    log_file: Optional[str] = None,
) -> logging.Logger:
    """
    Configure structured logging for the application.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        sentry_dsn: Optional Sentry DSN for error tracking
        enable_console: Whether to log to console
        log_file: Optional file path for log output
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("book_recommender")
    logger.setLevel(getattr(logging, level.upper()))
    logger.handlers.clear()

    formatter = StructuredFormatter()

    # Console handler
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Sentry integration
    if sentry_dsn and SENTRY_AVAILABLE:
        sentry_logging = LoggingIntegration(
            level=logging.INFO,
            event_level=logging.ERROR,
        )
        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[sentry_logging],
            traces_sample_rate=0.1,
            profiles_sample_rate=0.1,
        )
        logger.info("Sentry error tracking initialized")
    elif sentry_dsn and not SENTRY_AVAILABLE:
        logger.warning("Sentry DSN provided but sentry-sdk not installed")

    return logger


def get_logger() -> logging.Logger:
    """Get the application logger."""
    return logging.getLogger("book_recommender")
