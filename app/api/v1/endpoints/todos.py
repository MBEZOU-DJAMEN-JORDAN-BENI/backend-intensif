from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from math import ceil

from app.schemas.todos import TodoCreate, TodoResponse, TodoUpdate
from app.schemas.common import PaginatedResponse
from app.services.todo_service import TodoService
from app.db.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.category import Category
 
# APIRouter() : Permet de grouper des routes dans un module séparé
router = APIRouter(tags=["todos"])


# 1.GET /todos - Liste toutes les taches de l'utilisateur connecter
@router.get("/", response_model=PaginatedResponse[TodoResponse])
async def get_todos(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    limit = min(limit, 100)  # Limite maximale de 100 pour la taille de la page
    
    items, total = TodoService.get_paginated(
        db,
        current_user.id,
        skip,
        limit
    )
    page = (skip // limit) + 1
    total_pages = ceil(total / limit) if limit > 0 else 0
    
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=limit,
        total_pages=total_pages
    )


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


# 3. GET /todos/search - Recuperer une tache
@router.get("/search", response_model=PaginatedResponse[TodoResponse])
async def search_todos(
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    done: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    limit = min(limit, 100)  # Limite maximale de 100 pour la taille de la page
    
    items, total = TodoService.search_and_filter(
        db,
        current_user.id,
        skip,
        limit,
        search,
        done
    )
    page = (skip // limit) + 1
    total_pages = ceil(total / limit) if limit > 0 else 0   
    
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=limit,
        total_pages=total_pages
    )

 
# 4. PUT /todos/{todo_id} - Mise à jour d'une tâche
@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int, 
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_todo = TodoService.update(db, todo_id, todo_update, user_id=current_user.id)
    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return updated_todo


# 5. DELETE /todos/{todo_id} - Supprimer une tâche
@router.delete("/{todo_id}", status_code=204)
async def delete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    deleted = TodoService.delete(db, todo_id, user_id=current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return None