# Premiere API avec la methode HTTP GET

from fastapi import FastAPI, HTTPException
from typing import Dict, List
from app.routes import todos

app = FastAPI(
    title="API Backend Intensif",
    description="API Rest professionnelle avec FastAPI",
    version="1.0.0"
)

@app.get("/")
async def root():
    return{
        "message": "Bienvue sur l'API Backend Intensif",
        "status": "online"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Methodes HTTP et Routes Avancees

users_db = []

#=========================================
# METHODES HTTP PRINCIPALES
#========================================

# GET : Recuperation des ressources (liste des utilisateur)
@app.get("/users", response_model=List[Dict])
async def get_users():
    return users_db

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    for index, user in enumerate(users_db):
        if user["id"] == user_id:
            return user
        
# Creer une exception pour prevenir les erreurs 
    raise HTTPException(status_code=404, detail="User not found")


# POST : Creer des ressources
@app.post("/users", status_code=201)
async def create_user(name: str, email: str):
    new_user = {
        "id": len(users_db) + 1,
        "name": name,
        "email": email
    }    
    users_db.append(new_user)
    return new_user

# PUT : Mettre a jour une ressource complete
@app.put("/users/{user_id}")
async def update_user(user_id: int, name: str, email: str):
    for user in users_db:
        if user["id"] == user_id:
            user["name"] = name
            user["email"] = email
            return user
        
    raise HTTPException(status_code=404, detail="User not found")

# DELETE : Suprimer un ressource
@app.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int):
    global users_db
    users_db = [u for u in users_db if u["id"] != user_id]
    for index, user in enumerate(users_db, start=1):
        user["id"] = index
    return None

app.include_router(todos.router)

