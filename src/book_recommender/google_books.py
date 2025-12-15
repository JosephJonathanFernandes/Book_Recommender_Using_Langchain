"""Google Books lookup helpers."""

from typing import Dict, List

import requests

GOOGLE_BOOKS_ENDPOINT = "https://www.googleapis.com/books/v1/volumes"


def fetch_google_books(query: str, genre: str, max_results: int = 4) -> List[Dict[str, str]]:
    """Fetch Google Books suggestions (title, authors, description, link, thumbnail).

    Uses the public endpoint; no API key required for this lightweight lookup.
    Returns a list of dicts to enable richer UI cards.
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
        results: List[Dict[str, str]] = []
        for item in items[:max_results]:
            info = item.get("volumeInfo", {})
            title = info.get("title") or "Unknown title"
            authors = ", ".join(info.get("authors", [])[:2]) or "Unknown author"
            desc = (info.get("description") or "").split(".")[:2]
            desc_text = ". ".join(desc).strip()
            thumb = (info.get("imageLinks") or {}).get("thumbnail", "")
            link = info.get("infoLink", "")
            results.append(
                {
                    "title": title,
                    "authors": authors,
                    "description": desc_text[:220] if desc_text else "",
                    "thumbnail": thumb,
                    "link": link,
                }
            )
        return results
    except Exception:
        return []
