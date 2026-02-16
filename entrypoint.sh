#!/bin/bash

export FLASK_APP=${FLASK_APP:-flasky.py}
export FLASK_RUN_HOST=${FLASK_RUN_HOST:-0.0.0.0}
export FLASK_RUN_PORT=${FLASK_RUN_PORT:-5000}

# Faqat bir marta: init
if [ ! -d "migrations" ]; then
    echo "[INFO] migrations/ yo‘q, yaratilyapti..."
    flask db init
fi

# Agar `versions/` yo‘q bo‘lsa, `migrate` chaqiramiz
if [ ! -d "migrations/versions" ] || [ -z "$(ls -A migrations/versions)" ]; then
    echo "[INFO] versions/ bo‘sh yoki yo‘q, migrate qilinyapti..."
    flask db migrate -m "Initial migration"
fi

# Upgrade
flask db upgrade

# Flask serverni ishga tushirish
exec flask run
