from __future__ import annotations

from urllib.parse import urlparse

import requests


YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be", "music.youtube.com"}


def is_url(value: str) -> bool:
    try:
        parsed = urlparse(value)
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
    except Exception:
        return False


def youtube_metadata(reference: str) -> dict:
    if not is_url(reference):
        return {
            "source_type": "title_or_artist",
            "reference": reference.strip(),
            "title": reference.strip(),
            "author_name": None,
            "url": None,
        }

    parsed = urlparse(reference)
    host = parsed.netloc.lower()
    if host not in YOUTUBE_HOSTS:
        return {
            "source_type": "url",
            "reference": reference.strip(),
            "title": None,
            "author_name": None,
            "url": reference.strip(),
        }

    try:
        resp = requests.get(
            "https://www.youtube.com/oembed",
            params={"url": reference, "format": "json"},
            timeout=8,
        )
        resp.raise_for_status()
        data = resp.json()
        return {
            "source_type": "youtube",
            "reference": reference.strip(),
            "title": data.get("title"),
            "author_name": data.get("author_name"),
            "url": reference.strip(),
        }
    except Exception:
        return {
            "source_type": "youtube",
            "reference": reference.strip(),
            "title": None,
            "author_name": None,
            "url": reference.strip(),
        }
