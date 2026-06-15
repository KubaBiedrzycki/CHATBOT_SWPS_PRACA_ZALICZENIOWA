# Kulinarny Chatbot — Baza wiedzy

To jest zwykły plik wiedzy. Chatbot wykorzystuje wszystko z folderu
`knowledge/` jako kontekst podczas odpowiadania na pytania.
Edytuj ten plik lub dodaj kolejne pliki `.md`, aby rozszerzyć wiedzę kulinarną asystenta.

## O projekcie

Kulinarny Chatbot to demonstracyjny asystent zbudowany w monorepo Turborepo:
frontend webowy w Next.js (`apps/web`) komunikujący się z backendem
Flask + model językowy (`apps/api`). Asystent posiada zintegrowanego klienta API
bazy TheMealDB, dzięki czemu potrafi na żądanie dynamicznie wyszukiwać przepisy, 
składniki i instrukcje gotowania.

## Najczęściej zadawane pytania

**P: W czym może pomóc ten asystent?**
O: W wyszukiwaniu konkretnych przepisów kulinarnych (dzięki połączeniu z TheMealDB), 
odpowiadaniu na pytania w oparciu o statyczne dokumenty zapisane w folderze
`knowledge/`, a także w ogólnych poradach kuchennych i kulinarnych.

**P: Jak dodać więcej statycznej wiedzy?**
O: Umieść nowy plik `.md` w folderze `apps/api/knowledge/`. Zostanie on
automatycznie wczytany przy następnym uruchomieniu API. To doskonałe miejsce na 
np. przeliczniki miar kuchennych, tabele zamienników czy podstawy dietetyki.

**P: Kto utrzymuje ten projekt?**
O: Kacper Kulawik (79650) i Jakub Biedrzycki (76619)

