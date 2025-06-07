FROM python:3.11-slim

ENV APP_HOME=/app
WORKDIR $APP_HOME

COPY . .

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    gettext

RUN pip install --upgrade pip && pip install -r requirements.txt

# Flask app uchun environment variable'lar
ENV FLASK_APP=flasky.py
ENV FLASK_ENV=development

# Avval database migratsiyalarini bajarib olamiz, keyin app ni ishga tushiramiz
CMD flask db upgrade && flask run --host=0.0.0.0
