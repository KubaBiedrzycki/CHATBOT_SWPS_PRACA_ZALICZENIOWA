"""Wczytuje główny plik wiedzy (general.md) jako stały kontekst chatbota.

Wiedza szczegółowa nie jest trzymana lokalnie ani ładowana w całości —
jest doczytywana na żądanie z repozytorium naukowego SWPS (DSpace) przez
narzędzie wyszukiwania (patrz app/repository.py).
"""

from pathlib import Path

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"
MAIN_FILE = "general.md"


def _load_main() -> str:
    path = KNOWLEDGE_DIR / MAIN_FILE
    return path.read_text(encoding="utf-8").strip() if path.is_file() else ""


# Wczytywane raz przy imporcie. Treść jest stała, więc pozostaje
# buforowalna w prompt cache.
MAIN_KNOWLEDGE = _load_main()
