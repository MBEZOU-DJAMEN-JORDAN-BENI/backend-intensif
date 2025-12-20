from fastapi import APIRouter, HTTPException
from typing import Dict, List

# APIRputer() : Permet de grouper ddes des routes dans un module separe
router = APIRouter(prefix="/todos", tags=["todos"])

# Base de Donnee temporaire
todos_db = []

# 1.GET /todos - Liste toutes les taches 
@router.get("/")
async def get_todos():
    return todos_db


# 2. POST /todos - Creer une tache
@router.post("/", status_code=201)
async def create_todo(title: str, description: str):
    new_todo = {
        "id": len(todos_db) + 1,
        "title": title,
        "description": description,
        "done": False
    }
    todos_db.append(new_todo)
    return new_todo


# 3. GET /todos/{todo_id} - Recuperer une tache
@router.get("/{todo_id}")
async def get_todo(todo_id: int):
    for todo in todos_db:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")



# 4. PATCH /todos/{todo_id} - Marquer comme fait/non fait
@router.patch("/{todo_id}")
async def toggle_todo(todo_id: int):
    for todo in todos_db:
        if todo["id"] == todo_id:
            todo["done"] = not todo["done"]
            return todo
    raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
 

# 5. DELETE /todos/{todo_id} - Supprimer une tache
@router.delete("/{todo_id}", status_code=204)
async def delete_todo(todo_id: int):
    global todos_db
    
# Verifier que le todo existe
    todo_exists = any(todo["id"] == todo_id for todo in todos_db) 
    if not todo_exists:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
       
    todos_db = [todo for todo in todos_db if todo["id"] != todo_id]
    for index, todo in enumerate(todos_db, start=1):
        todo["id"] = index
    return None
        
    