#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")/.."
if [ ! -d .venv ]; then python3 -m venv .venv; fi
. .venv/bin/activate
python -m pip install -r requirements.txt
exec python -m uvicorn backend.web:app --host 0.0.0.0 --port "${FISHYLLAMA_PORT:-8000}"
