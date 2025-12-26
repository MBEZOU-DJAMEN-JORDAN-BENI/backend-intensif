from typing import Dict, List
from fastapi import FastAPI
from app.routes import todos, users, auth

app = FastAPI(
    title="API Backend Intensif",
    description="API REST avec Pydantic",
    version="2.0.0"
)

app.include_router(auth.router)
app.include_router(users.router)  
app.include_router(todos.router)


@app.get("/")
async def root():
    return {"message": "API v2.0 avec Pydantic"}

