from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.categories import CategoryCreate, CategoryResponse, CategoryUpdate
from app.services.category_service import CategoryService
from app.db.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.models.category import Category
 
# APIRputer() : Permet de grouper ddes des routes dans un module separe
router = APIRouter(prefix="/categories", tags=["categories"])

# Base de Donnee temporaire
categories_db = []

# 1.GET /categories - Liste toutes les taches de l'utilisateur connecter
@router.get("/", response_model=List[CategoryResponse])
async def get_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    return CategoryService.get_all(db, current_user.id)


# 2. POST /categories - Creer une categorie
@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    return CategoryService.create(db, category, current_user.id)


# 3. GET /categories/{category_id} - Recuperer une categorie
@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: int, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    
    return CategoryService.get_by_id(db, category_id, user_id=current_user.id)

 
# 4. PUT /categories/{category_id} - Mise a jour complete
@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int, 
    category_update: CategoryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
      
    return CategoryService.update(db, category_id, category_update, user_id=current_user.id)


# 5. DELETE /categories/{category_id} - Supprimer une categorie
@router.delete("/{category_id}", status_code=204)
async def delete_todo(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    
    return CategoryService.delete(db, category_id, user_id=current_user.id)
        
    