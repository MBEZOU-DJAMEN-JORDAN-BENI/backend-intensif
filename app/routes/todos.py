from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.todos import TodoCreate, TodoResponse, TodoUpdate
from app.services.todo_service import TodoService
from app.database import get_db
from app.routes.auth import get_current_user
from app.models.user import User
from app.models.todo import Todo

# APIRputer() : Permet de grouper ddes des routes dans un module separe
router = APIRouter(prefix="/todos", tags=["todos"])

# Base de Donnee temporaire
todos_db = []

# 1.GET /todos - Liste toutes les taches de l'utilisateur connecter
@router.get("/", response_model=List[TodoResponse])
async def get_todos(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    return db.query(Todo).filter(Todo.user_id == current_user.id).all()


# 2. POST /todos - Creer une tache
@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo: TodoCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_todo = Todo(
        **todo.model_dump(),
        user_id=current_user.id
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


# 3. GET /todos/{todo_id} - Recuperer une tache
@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: int, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    db_todo = db.querry(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    ).first()
    
    if not db_todo:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    return db_todo

 
# 4. PUT /todos/{todo_id} - Mise a jour complete
@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int, 
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    ).first()
    
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    update_data = todo_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)
        
    db.commit()
    db.refresh(db_todo)    
    return db_todo


# 5. DELETE /todos/{todo_id} - Supprimer une tache
@router.delete("/{todo_id}", status_code=204)
async def delete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    db_todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    ).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    
    db.delete(db_todo)
    db.commit()
    return None
        
    