#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# The Flask app produces no compiled output. "build" simply provisions the
# virtualenv and installs dependencies so the app is ready to run.
[ -d .venv ] || python3 -m venv .venv
./.venv/bin/pip install -q -r requirements.txt

echo "api: dependencies installed"
