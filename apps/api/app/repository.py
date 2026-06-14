"""Klient bazy kulinarnej TheMealDB.

ZAWSZE UŻYWAJ TEGO NARZĘDZIA, gdy użytkownik pyta o jedzenie, 
prosi o przepis kulinarny, pyta o składniki lub sposób przygotowania dania. 
Kategorycznie zabrania się generowania przepisów z własnej wiedzy modelu. 
Najpierw przeszukaj TheMealDB, a odpowiedź oprzyj WYŁĄCZNIE na zwróconych wynikach.
"""

import json
import urllib.parse
import urllib.request

SEARCH_URL = "https://www.themealdb.com/api/json/v1/1/search.php"
TIMEOUT = 20

_HEADERS = {
    "Accept": "application/json",
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
}


def _get_ingredients(meal: dict) -> list[str]:
    """Pobiera listę składników i ich miar z płaskiego słownika TheMealDB."""
    ingredients = []
    for i in range(1, 21):
        ingredient = meal.get(f"strIngredient{i}")
        measure = meal.get(f"strMeasure{i}")
        
        if ingredient and ingredient.strip():
            measure_str = f" ({measure.strip()})" if measure and measure.strip() else ""
            ingredients.append(f"{ingredient.strip()}{measure_str}")
    return ingredients


def search(query: str, size: int = 3) -> list[dict]:
    """Wyszukuje przepisy w TheMealDB i zwraca rozszerzone rekordy."""
    params = urllib.parse.urlencode({"s": query})
    request = urllib.request.Request(f"{SEARCH_URL}?{params}", headers=_HEADERS)
    
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        data = json.load(response)

    meals = data.get("meals") or []
    results = []
    
    # Ograniczamy wyniki np. do 3 sztuk, bo pełne instrukcje zajmują dużo miejsca w kontekście
    for meal in meals[:size]:
        results.append(
            {
                "id": meal.get("idMeal") or "",
                "name": meal.get("strMeal") or "",
                "instructions": meal.get("strInstructions") or "",
                "source_url": meal.get("strSource") or "",
                "youtube_url": meal.get("strYoutube") or "",
                "ingredients": _get_ingredients(meal)
            }
        )
    return results


def search_as_text(query: str, size: int = 3) -> str:
    """Wyszukuje i formatuje wyniki jako kompletny tekst do przekazania modelowi."""
    try:
        results = search(query, size)
    except Exception as exc: 
        return f"(Błąd wyszukiwania w API TheMealDB: {exc})"

    if not results:
        return f"(Brak wyników w TheMealDB dla zapytania: „{query}”.)"

    blocks = []
    for i, r in enumerate(results, 1):
        parts = [f"{i}. {r['name']}"]
            
        if r["ingredients"]:
            parts.append("Składniki: " + ", ".join(r["ingredients"]))
            
        if r["instructions"]:
            # Kluczowa zmiana: Zwracamy modelowi PEŁNY tekst bez ucinania. 
            # Dzięki temu LLM może podyktować użytkownikowi kompletny przepis.
            parts.append("Instrukcje gotowania:\n" + r["instructions"].strip())
            
        # Dostarczamy kompletne linki, o które poprosiłeś
        links = []
        if r["source_url"]:
            links.append(f"Źródło przepisu: {r['source_url']}")
        if r["id"]:
            links.append(f"Strona TheMealDB: https://www.themealdb.com/meal.php?c={r['id']}")
        if r["youtube_url"]:
            links.append(f"Wideo (YouTube): {r['youtube_url']}")
            
        if links:
            parts.append("Przydatne linki:\n- " + "\n- ".join(links))
            
        blocks.append("\n".join(parts))
        
    return "\n\n".join(blocks)