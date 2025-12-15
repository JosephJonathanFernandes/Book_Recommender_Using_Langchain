"""Google Books lookup helpers."""

from typing import List

import requests

GOOGLE_BOOKS_ENDPOINT = "https://www.googleapis.com/books/v1/volumes"


def fetch_google_books(query: str, genre: str, max_results: int = 3) -> List[str]:
    """Fetch a few Google Books suggestions to blend with LLM output.

    Uses the public endpoint; no API key required for this lightweight lookup.
    """
    search_terms = query
    if genre:
        search_terms += f" subject:{genre}"
    try:
        resp = requests.get(
            GOOGLE_BOOKS_ENDPOINT,
            params={"q": search_terms, "maxResults": max_results},
            timeout=6,
        )
        resp.raise_for_status()
        data = resp.json()
        items = data.get("items", [])
        results: List[str] = []
        for item in items[:max_results]:
            info = item.get("volumeInfo", {})
            title = info.get("title") or "Unknown title"
            authors = ", ".join(info.get("authors", [])[:2]) or "Unknown author"
            desc = (info.get("description") or "").split(".")[:2]
            desc_text = ". ".join(desc).strip()
            snippet = f"{title} by {authors}"
            if desc_text:
                snippet += f" — {desc_text[:200]}"
            results.append(snippet)
        return results
    except Exception:
        return []
