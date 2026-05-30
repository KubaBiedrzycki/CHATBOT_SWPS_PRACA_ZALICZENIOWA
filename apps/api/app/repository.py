"""Klient repozytorium naukowego SWPS (DSpace).

Udostępnia wyszukiwanie publikacji przez publiczne REST API DSpace
(`/server/api/discover/search/objects`). Używane jako źródło wiedzy
„na żądanie" — wywoływane przez model dopiero, gdy pytanie tego wymaga.
Korzysta wyłącznie z biblioteki standardowej (bez dodatkowych zależności).
"""

import json
import urllib.parse
import urllib.request

SEARCH_URL = "https://share.swps.edu.pl/server/api/discover/search/objects"
TIMEOUT = 20
# Cloudflare przed repozytorium blokuje domyślny User-Agent urllib (403),
# dlatego podajemy nagłówek przeglądarki.
_HEADERS = {
    "Accept": "application/json",
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
}


def _first(md: dict, *keys: str) -> str:
    """Pierwsza niepusta wartość spośród podanych pól metadanych."""
    for key in keys:
        for entry in md.get(key, []):
            value = (entry.get("value") or "").strip()
            if value and value.lower() != "brak":
                return value
    return ""


def _all(md: dict, *keys: str) -> list[str]:
    """Wszystkie niepuste wartości spośród podanych pól metadanych."""
    out: list[str] = []
    for key in keys:
        for entry in md.get(key, []):
            value = (entry.get("value") or "").strip()
            if value and value.lower() != "brak":
                out.append(value)
    return out


def search(query: str, size: int = 5) -> list[dict]:
    """Wyszukuje pozycje w repozytorium i zwraca uproszczone rekordy."""
    params = urllib.parse.urlencode(
        {"query": query, "size": size, "dsoType": "item"}
    )
    request = urllib.request.Request(f"{SEARCH_URL}?{params}", headers=_HEADERS)
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        data = json.load(response)

    objects = (
        data.get("_embedded", {})
        .get("searchResult", {})
        .get("_embedded", {})
        .get("objects", [])
    )

    results = []
    for obj in objects:
        item = obj.get("_embedded", {}).get("indexableObject", {})
        md = item.get("metadata", {})
        handle = item.get("handle")
        results.append(
            {
                "title": _first(md, "dc.title") or item.get("name", ""),
                "authors": _all(md, "dc.contributor.author", "dc.contributor.editor"),
                "year": _first(md, "dc.date.issued")[:4],
                "abstract": _first(
                    md, "dc.abstract.pl", "dc.description.abstract", "dc.abstract.en"
                ),
                "subjects": _all(md, "dc.subject.pl", "dc.subject.en"),
                "url": _first(md, "dc.identifier.uri")
                or (f"https://share.swps.edu.pl/handle/{handle}" if handle else ""),
            }
        )
    return results


def search_as_text(query: str, size: int = 5) -> str:
    """Wyszukuje i formatuje wyniki jako tekst do przekazania modelowi."""
    try:
        results = search(query, size)
    except Exception as exc:  # sieć/parsowanie — nie wywracamy całego czatu
        return f"(Błąd wyszukiwania w repozytorium SWPS: {exc})"

    if not results:
        return f"(Brak wyników w repozytorium SWPS dla zapytania: „{query}”.)"

    blocks = []
    for i, r in enumerate(results, 1):
        parts = [f"{i}. {r['title']}"]
        if r["authors"]:
            parts.append("Autorzy/redakcja: " + ", ".join(r["authors"][:6]))
        if r["year"]:
            parts.append("Rok: " + r["year"])
        if r["subjects"]:
            parts.append("Słowa kluczowe: " + ", ".join(r["subjects"][:8]))
        if r["abstract"]:
            parts.append("Abstrakt: " + r["abstract"][:600])
        if r["url"]:
            parts.append("Link: " + r["url"])
        blocks.append("\n".join(parts))
    return "\n\n".join(blocks)
