
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.orm import Session

from app.schemas.users import UserResponse, UserUpdate
from app.services.user_service import UserService
from app.models.user import User
from app.api.deps import get_current_user, get_current_admin
from app.db.database import get_db

# APIRouter() : Permet de grouper des routes dans un module séparé
router = APIRouter(tags=["users"])


# 1.GET /users - Liste de tous les utilisateurs (admin seulement)
@router.get("/", response_model=List[UserResponse])
async def get_users(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return UserService.get_all(db)


# 2. GET /users/{user_id} - Récupérer les informations d'un utilisateur
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = UserService.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

  
# 3. PUT /users/{user_id} - Mise à jour d'un utilisateur
@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, 
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Vérifier que l'utilisateur modifie son propre compte ou est admin
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )
    
    updated_user = UserService.update(db, user_id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user


# 4. DELETE /users/{user_id} - Supprimer un utilisateur
@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Vérifier que l'utilisateur supprime son propre compte ou est admin
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user"
        )
    
    deleted = UserService.delete(db, user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return None