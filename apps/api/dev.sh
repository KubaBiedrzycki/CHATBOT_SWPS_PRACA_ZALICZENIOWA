#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

[ -d .venv ] || python3 -m venv .venv
./.venv/bin/pip install -q -r requirements.txt

exec ./.venv/bin/flask --app app run --port 5000 --debug
