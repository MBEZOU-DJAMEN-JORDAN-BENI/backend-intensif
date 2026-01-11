# Image de base (Python 3.12)
FROM python:3.12-slim

# Définit le dossier de travail dans le conteneur
WORKDIR /app

# Exécute une commande lors de la construction de l'image
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copie des fichiers de ton ordinateur vers le conteneur
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code de l'application
COPY . .

# Indique que le conteneur écoute sur ce port
EXPOSE 8000

# Commande à exécuter au démarrage du conteneur
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "$PORT"]

