#!/bin/bash
set -e

export FLASK_APP=${FLASK_APP:-flasky.py}

# One-time init
if [ ! -d "migrations" ]; then
    echo "[INFO] migrations/ not found, initializing..."
    flask db init
fi

if [ ! -d "migrations/versions" ] || [ -z "$(ls -A migrations/versions 2>/dev/null)" ]; then
    echo "[INFO] versions/ empty, generating initial migration..."
    flask db migrate -m "Initial migration" || true
fi

flask db upgrade

# Run server
if [ "${FLASK_DEBUG:-0}" = "1" ]; then
    echo "[INFO] Starting Flask dev server (debug mode)..."
    exec flask run --host=0.0.0.0 --port=5000
else
    echo "[INFO] Starting Gunicorn (production)..."
    exec gunicorn -b 0.0.0.0:5000 -w "${GUNICORN_WORKERS:-4}" --access-logfile - --error-logfile - flasky:app
fi
