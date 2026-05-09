#!/bin/bash
# PhysicsHub deploy script
#
# Usage:
#   ./deploy.sh              # full deploy: pull + deps + migrate + restart
#   ./deploy.sh --no-pull    # skip git pull (deploy current checkout)
#   ./deploy.sh --no-restart # skip systemd service restart
#
# Talab qilinadigan env (.env yoki shell):
#   SECRET_KEY  — production uchun majburiy

set -euo pipefail

PULL=true
RESTART=true
for arg in "$@"; do
    case "$arg" in
        --no-pull) PULL=false ;;
        --no-restart) RESTART=false ;;
        -h|--help)
            sed -n '2,11p' "$0"
            exit 0
            ;;
    esac
done

# Always run from the project root (script's dir)
cd "$(dirname "$(readlink -f "$0")")"

log() { echo -e "\033[1;36m[deploy]\033[0m $*"; }
err() { echo -e "\033[1;31m[deploy]\033[0m $*" >&2; }

# 1) Git pull
if $PULL; then
    log "git pull (fast-forward only)..."
    git pull --ff-only
else
    log "git pull skipped (--no-pull)"
fi

# 2) Detect and activate virtualenv
VENV=""
for candidate in \
    "$PWD/venv" \
    "$PWD/.venv" \
    "$PWD/../env" \
    "/home/physicshub/web/physicshub.uz/public_html/env"; do
    if [ -d "$candidate" ] && [ -f "$candidate/bin/activate" ]; then
        VENV="$(realpath "$candidate")"
        break
    fi
done

if [ -n "$VENV" ]; then
    log "activating venv: $VENV"
    # shellcheck disable=SC1091
    source "$VENV/bin/activate"
else
    log "no venv detected, using system python ($(command -v python3))"
fi

# 3) Install/upgrade dependencies
log "pip install -r requirements.txt..."
pip install --upgrade pip >/dev/null
pip install -r requirements.txt

# 4) Apply DB migrations
export FLASK_APP="${FLASK_APP:-flasky.py}"
export FLASK_CONFIG="${FLASK_CONFIG:-production}"
log "flask db upgrade..."
flask db upgrade

# 5) Ensure runtime directories
log "ensuring static dirs (lessons, gifs, pics, labs)..."
mkdir -p app/static/lessons app/static/gifs app/static/pics app/static/labs

# 6) Production sanity check on SECRET_KEY
if [ "${FLASK_CONFIG}" = "production" ]; then
    if [ -z "${SECRET_KEY:-}" ] && ! grep -q '^SECRET_KEY=' .env 2>/dev/null; then
        err "WARNING: SECRET_KEY .env'da ham, env'da ham topilmadi — production'da xato beradi"
    fi
fi

# 7) Restart systemd service (if installed)
if $RESTART; then
    if systemctl list-unit-files 2>/dev/null | grep -q '^physicshub\.service'; then
        log "restarting physicshub.service..."
        if [ "$EUID" -ne 0 ]; then
            sudo systemctl restart physicshub.service
        else
            systemctl restart physicshub.service
        fi
        sleep 1
        if systemctl is-active --quiet physicshub.service; then
            log "service is active"
        else
            err "service failed to start — check: journalctl -u physicshub.service -n 50"
            exit 1
        fi
    elif [ -f docker-compose.yml ] && command -v docker >/dev/null && docker compose ps --services 2>/dev/null | grep -q '^web$'; then
        log "docker compose: rebuild web service..."
        docker compose up -d --build web
    else
        log "systemd service yo'q va docker-compose ham topilmadi — restart skipped"
    fi
else
    log "service restart skipped (--no-restart)"
fi

log "✓ deploy yakunlandi"
