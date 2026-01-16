
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.orm import Session

from app.schemas.users import UserResponse, UserUpdate
from app.services.user_service import UserService
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user, get_current_admin
from app.db.database import get_db

# APIRputer() : Permet de grouper ddes des routes dans un module separe
router = APIRouter(prefix="/users", tags=["users"])

# Base de Donnee temporaire
users_db = []

# 1.GET /users - Liste de tous les utilisatuers 
@router.get("/", response_model=List[UserResponse])
async def get_users(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return UserService.get_all(db)


# 3. GET /users/{user_id} - Recuperer les information d'un utilisateur
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    return UserService.get_by_id(db, user_id)

  
# 4. PUT /users/{user_id} - Mise a jour complete
@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, 
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
     
    return UserService.update(db, user_id, user_update)


# 5. DELETE /users/{user_id} - Supprimer une utilisateur
@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    return UserService.delete(db, user_id)
        
    