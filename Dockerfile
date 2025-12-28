# Dockerfile

# SYNTAXE : FROM image:tag
# EXPLICATION : Image de base (Python 3.12)
FROM python:3.12-slim

# SYNTAXE : WORKDIR /chemin
# EXPLICATION : Définit le dossier de travail dans le conteneur
WORKDIR /app

# SYNTAXE : RUN commande
# EXPLICATION : Exécute une commande lors de la construction de l'image
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# SYNTAXE : COPY source destination
# EXPLICATION : Copie des fichiers de ton ordinateur vers le conteneur
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code de l'application
COPY . .

# SYNTAXE : EXPOSE port
# EXPLICATION : Indique que le conteneur écoute sur ce port
EXPOSE 8000

# SYNTAXE : CMD ["commande", "arg1", "arg2"]
# EXPLICATION : Commande à exécuter au démarrage du conteneur
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

#### Fichier : `.dockerignore`
# .dockerignore

# Python
__pycache__/
*.py[cod]
*$py.class
venv/
env/

# Database
*.db
*.sqlite3

# Environment
.env
.env.local

# Tests
htmlcov/
.pytest_cache/
.coverage

# IDE
.vscode/
.idea/

# Git
.git/
.gitignore

# Alembic
alembic/versions/*.pyc

# Logs
logs/
*.log