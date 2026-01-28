from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.categories import CategoryCreate, CategoryResponse, CategoryUpdate
from app.services.category_service import CategoryService
from app.db.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.category import Category
 
# APIRouter() : Permet de grouper des routes dans un module séparé
router = APIRouter(tags=["categories"])


# 1.GET /categories - Liste toutes les catégories de l'utilisateur connecté
@router.get("/", response_model=List[CategoryResponse])
async def get_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return CategoryService.get_all(db, current_user.id)


# 2. POST /categories - Créer une catégorie
@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return CategoryService.create(db, category, current_user.id)


# 3. GET /categories/{category_id} - Récupérer une catégorie
@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: int, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    category = CategoryService.get_by_id(db, category_id, user_id=current_user.id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category

 
# 4. PUT /categories/{category_id} - Mise à jour d'une catégorie
@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int, 
    category_update: CategoryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_category = CategoryService.update(db, category_id, category_update, user_id=current_user.id)
    if not updated_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return updated_category


# 5. DELETE /categories/{category_id} - Supprimer une catégorie
@router.delete("/{category_id}", status_code=204)
async def delete_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    deleted = CategoryService.delete(db, category_id, user_id=current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return None