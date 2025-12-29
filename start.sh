#!/bin/bash

echo " Demarrage de Backend Intensif"

# Arreter les conteneurs existants
docker-compose down

# Construire les images
docker-compose build

# Demarer les services
docker-compose up -d

# Attendre que la DB soit prete
echo " Attente de PostgreSQL..."
sleep 5

# Appliquer les migrations
echo " Application des migrations..."
docker-compose exec -T app alembic upgrade head

# Afficher les logs
echo "Application demarree sur http://localhost:8000"
docker-compose logs -f