#!/bin/bash

# Flask ilovangiz nomi to‘g‘ri bo‘lishi kerak, masalan app.py bo‘lsa:
export FLASK_APP=flasky.py  # yoki app.py — to‘g‘ri nomni yozing
export FLASK_ENV=development
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=5000

# Migrations papkasini tekshirib olish
if [ ! -d "migrations/versions" ]; then
    echo "Migration versiyalar papkasi yo'q, yaratilyapti..."
    flask db init
    flask db migrate -m "Initial migration"
fi

# Upgrade qilish
flask db upgrade

# Flaskni ishga tushirish
exec flask run
