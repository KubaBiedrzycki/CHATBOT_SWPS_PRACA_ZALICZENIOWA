# CHATBOT SWPS — Baza wiedzy

To jest zwykły plik wiedzy. Chatbot wykorzystuje wszystko z folderu
`knowledge/` jako kontekst podczas odpowiadania na pytania.
Edytuj ten plik lub dodaj kolejne pliki `.md`, aby rozszerzyć wiedzę asystenta.

## O projekcie

CHATBOT SWPS to demonstracyjny asystent zbudowany w monorepo Turborepo:
frontend webowy w Next.js (`apps/web`) komunikujący się z backendem
Flask + Claude (`apps/api`).

## Najczęściej zadawane pytania

**P: W czym może pomóc ten asystent?**
O: W odpowiadaniu na pytania w oparciu o dokumenty zapisane w folderze
`knowledge/`, a także w zwykłej rozmowie.

**P: Jak dodać więcej wiedzy?**
O: Umieść nowy plik `.md` w folderze `apps/api/knowledge/`. Zostanie on
automatycznie wczytany przy następnym uruchomieniu API.

**P: Kto utrzymuje ten projekt?**
O: Zespół projektowy. Zaktualizuj tę odpowiedź o prawdziwe dane kontaktowe.

## Uwagi

Zastąp tę przykładową treść swoją rzeczywistą wiedzą: dokumentacją
produktu, regulaminami, FAQ, przewodnikami wdrożeniowymi lub czymkolwiek,
do czego asystent powinien mieć dostęp.
