from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.todos import TodoCreate, TodoResponse, TodoUpdate
from app.services.todo_service import TodoService
from app.db.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.models.category import Category
 
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
    
    return TodoService.get_all(db, current_user.id)


# 2. POST /todos - Creer une tache
@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo: TodoCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # On verifie que la categorie appartient bien a l'utilisateur courant
    if todo.category_id:
        category = db.query(Category).filter(
            Category.id == todo.category_id,
            Category.user_id == current_user.id
        ).first()
        
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with id {todo.category_id} not found for the current user"
            )

    return TodoService.create(db, todo, current_user.id)


# 3. GET /todos/{todo_id} - Recuperer une tache
@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: int, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    
    return TodoService.get_by_id(db, todo_id, user_id=current_user.id)

 
# 4. PUT /todos/{todo_id} - Mise a jour complete
@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int, 
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
       
    return TodoService.update(db, todo_id, todo_update, user_id=current_user.id)


# 5. DELETE /todos/{todo_id} - Supprimer une tache
@router.delete("/{todo_id}", status_code=204)
async def delete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    
    return TodoService.delete(db, todo_id, user_id=current_user.id)
        
    