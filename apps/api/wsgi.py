"""Punkt wejścia produkcyjnego. Uruchom np. przez `gunicorn wsgi:app`."""

from app import create_app

app = create_app()
