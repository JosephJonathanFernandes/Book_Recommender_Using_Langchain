"""Usage analytics tracking for the book recommender app."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class UsageAnalytics:
    """Track usage analytics locally with optional external service support."""

    def __init__(self, analytics_file: Optional[str] = None):
        """
        Initialize analytics tracker.
        
        Args:
            analytics_file: Path to store analytics data (default: .analytics.json)
        """
        if analytics_file is None:
            analytics_file = str(Path.home() / ".book_recommender_analytics.json")
        
        self.analytics_file = analytics_file
        self._ensure_file()

    def _ensure_file(self) -> None:
        """Ensure analytics file exists."""
        if not os.path.exists(self.analytics_file):
            with open(self.analytics_file, "w") as f:
                json.dump({"events": [], "sessions": []}, f)

    def _read_data(self) -> Dict[str, Any]:
        """Read analytics data from file."""
        try:
            with open(self.analytics_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"events": [], "sessions": []}

    def _write_data(self, data: Dict[str, Any]) -> None:
        """Write analytics data to file."""
        with open(self.analytics_file, "w") as f:
            json.dump(data, f, indent=2)

    def track_event(
        self,
        event_name: str,
        properties: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Track an analytics event.
        
        Args:
            event_name: Name of the event (e.g., "recommendation_generated")
            properties: Additional properties for the event
        """
        data = self._read_data()
        
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event_name,
            "properties": properties or {},
        }
        
        data["events"].append(event)
        
        # Keep only last 1000 events
        data["events"] = data["events"][-1000:]
        
        self._write_data(data)

    def track_recommendation(
        self,
        query: str,
        genre: Optional[str],
        model: str,
        temperature: float,
        cached: bool,
        duration_ms: float,
        books_count: int,
    ) -> None:
        """Track a recommendation generation event."""
        self.track_event(
            "recommendation_generated",
            {
                "query_length": len(query),
                "genre": genre or "none",
                "model": model,
                "temperature": temperature,
                "cached": cached,
                "duration_ms": duration_ms,
                "books_count": books_count,
            },
        )

    def track_export(self, format: str) -> None:
        """Track an export action."""
        self.track_event("export", {"format": format})

    def track_rating(self, rating: int, query: str) -> None:
        """Track a rating submission."""
        self.track_event(
            "rating_submitted",
            {"rating": rating, "query_length": len(query)},
        )

    def track_share(self, platform: str) -> None:
        """Track a social share action."""
        self.track_event("social_share", {"platform": platform})

    def track_reading_list_save(self) -> None:
        """Track saving to reading list."""
        self.track_event("reading_list_save", {})

    def get_stats(self) -> Dict[str, Any]:
        """
        Get usage statistics.
        
        Returns:
            Dictionary with usage stats
        """
        data = self._read_data()
        events = data.get("events", [])
        
        if not events:
            return {
                "total_events": 0,
                "recommendations": 0,
                "exports": 0,
                "ratings": 0,
                "shares": 0,
            }
        
        recommendations = [e for e in events if e["event"] == "recommendation_generated"]
        exports = [e for e in events if e["event"] == "export"]
        ratings = [e for e in events if e["event"] == "rating_submitted"]
        shares = [e for e in events if e["event"] == "social_share"]
        
        stats = {
            "total_events": len(events),
            "recommendations": len(recommendations),
            "exports": len(exports),
            "ratings": len(ratings),
            "shares": len(shares),
            "first_event": events[0]["timestamp"] if events else None,
            "last_event": events[-1]["timestamp"] if events else None,
        }
        
        # Model usage
        if recommendations:
            model_usage = {}
            for rec in recommendations:
                model = rec["properties"].get("model", "unknown")
                model_usage[model] = model_usage.get(model, 0) + 1
            stats["model_usage"] = model_usage
        
        # Cache hit rate
        if recommendations:
            cached_count = sum(
                1 for r in recommendations if r["properties"].get("cached", False)
            )
            stats["cache_hit_rate"] = cached_count / len(recommendations)
        
        # Average rating
        if ratings:
            avg_rating = sum(r["properties"]["rating"] for r in ratings) / len(ratings)
            stats["average_rating"] = round(avg_rating, 2)
        
        return stats


# Global analytics instance
_analytics: Optional[UsageAnalytics] = None


def get_analytics() -> UsageAnalytics:
    """Get or create the global analytics instance."""
    global _analytics
    if _analytics is None:
        _analytics = UsageAnalytics()
    return _analytics
