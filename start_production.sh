#!/bin/bash
# start_production.sh

echo " Starting production server..."

# Appliquer les migrations
echo " Running migrations..."
alembic upgrade head

# Démarrer le serveur
echo " Starting Uvicorn..."
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}