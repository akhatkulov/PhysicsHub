#!/bin/bash

# Alembic versiyalar papkasi mavjudligini tekshirib, bo'lmasa yaratish
if [ ! -d "migrations/versions" ]; then
    echo "Migration versiyalar papkasi yo'q, yaratilyapti..."
    flask db init
    flask db migrate -m "Initial migration"
fi

flask db upgrade

# Gunicorn orqali appni ishga tushirish (WSGI faylingiz flasky.py deb taxmin qilinmoqda)
exec gunicorn -b :5000 flasky:app
