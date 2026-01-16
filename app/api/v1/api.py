from fastapi import APIRouter
# On importe les routeurs de chaque module
from app.api.v1.endpoints import auth, users, todos, categories

# On crée le routeur principal pour la V1
api_router = APIRouter()

# On "branche" les sous-routeurs sur le routeur principal
# On peut ajouter des préfixes ici pour éviter de les répéter dans les fichiers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(todos.router, prefix="/todos", tags=["todos"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])