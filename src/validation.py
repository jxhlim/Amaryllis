from __future__ import annotations

from urllib.parse import urlparse


def looks_like_pinterest_board(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return False
    if "pinterest." not in parsed.netloc:
        return False
    parts = [part for part in parsed.path.split("/") if part]
    return len(parts) >= 2
