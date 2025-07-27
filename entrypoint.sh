#!/bin/bash

# Alembic versiyalar papkasi mavjudligini tekshirib, bo'lmasa yaratish
if [ ! -d "migrations/versions" ]; then
    echo "Migration versiyalar papkasi yo'q, yaratilyapti..."
    flask db init
    flask db migrate -m "Initial migration"
fi

flask db upgrade

export FLASK_APP=flasky
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=5000
exec flask run

