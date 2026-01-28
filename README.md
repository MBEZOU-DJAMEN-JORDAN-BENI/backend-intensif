# 🚀 API Backend Intensif

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

Une API REST robuste et performante développée avec **FastAPI**, intégrant une gestion de base de données asynchrone, une authentification JWT sécurisée et des fonctionnalités avancées d'IA.

---

## ✨ Fonctionnalités Clés

- 🔐 **Authentification JWT** : Gestion sécurisée des sessions utilisateurs (Login, Register, Me).
- 📝 **Gestion de Todos** : CRUD complet avec pagination et filtrage par catégorie.
- 📁 **Catégories Personnalisées** : Organisation des tâches par catégories.
- 📤 **Upload de Fichiers** : Système de téléchargement de fichiers avec stockage local.
- 🤖 **Intégration IA** : Endpoints dédiés pour des services d'Intelligence Artificielle (v2).
- 🛠 **Migrations de BD** : Gestion fluide du schéma avec **Alembic**.
- 🧪 **Tests Automatisés** : Suite de tests complète avec **Pytest**.
- 🐳 **Docker Ready** : Déploiement simplifié avec Docker et Docker Compose.

---

## 🛠 Stack Technique

- **Framework** : [FastAPI](https://fastapi.tiangolo.com/)
- **Validation** : [Pydantic v2](https://docs.pydantic.dev/)
- **ORM** : [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
- **Base de Données** : PostgreSQL / SQLite (via SQLAlchemy)
- **Migrations** : [Alembic](https://alembic.sqlalchemy.org/)
- **Sécurité** : Python-JOSE (JWT), Passlib (Bcrypt)
- **Asynchrone** : AnyIO, Uvicorn, Httpx

---

## 🚀 Installation et Démarrage

### Préréglages

- Python 3.10+
- (Optionnel) Docker & Docker Compose

### 1. Cloner le dépôt

```bash
git clone <votre-url-repo>
cd backend-intensif
```

### 2. Configuration de l'environnement

Copiez le fichier d'exemple et adaptez les variables (Clé secrète, URL BD, etc.) :

```bash
cp .env.example .env
```

### 3. Installation des dépendances

Il est recommandé d'utiliser un environnement virtuel :

```bash
python -m venv venv
source venv/bin/activate  # Sur Linux/macOS
# venv\Scripts\activate   # Sur Windows

pip install -r requirements.txt
```

### 4. Appliquer les migrations

```bash
alembic upgrade head
```

### 5. Lancer l'application

```bash
# Mode développement avec auto-reload
./start.sh
```

L'API sera disponible sur : `http://localhost:8000`

---

## 📖 Documentation de l'API

Une fois le serveur lancé, accédez aux documentations interactives :

- **Swagger UI** : `http://localhost:8000/docs`
- **ReDoc** : `http://localhost:8000/redoc`

---

## 📂 Structure du Projet

```text
.
├── app/
│   ├── api/            # Endpoints de l'API (v1, v2/ai)
│   ├── core/           # Configuration globale (sécurité, settings)
│   ├── db/             # Session et base de données
│   ├── models/         # Modèles SQLAlchemy
│   ├── schemas/        # Schémas Pydantic (DTOs)
│   ├── services/       # Logique métier
│   └── main.py         # Point d'entrée de l'application
├── alembic/            # Scripts de migration
├── tests/              # Tests unitaires et d'intégration
├── uploads/            # Fichiers téléchargés par les utilisateurs
├── Dockerfile          # Configuration Docker
└── docker-compose.yml  # Orchestration des services
```

---

## 🐳 Déploiement avec Docker

```bash
docker-compose up --build
```

---

## 🧪 Tests

```bash
pytest
```

---

## 👨‍💻 Auteur

**MBEZOU DJAMEN Jordan Beni alias Bedane MD**

---

_Développé avec ❤️ pour l'apprentissage intensif du Backend._
