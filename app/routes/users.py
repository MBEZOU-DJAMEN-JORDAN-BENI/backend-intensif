from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.orm import Session

from app.schemas.users import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService
from app.models.user import User
from app.routes.auth import get_current_user
from app.database import get_db

# APIRputer() : Permet de grouper ddes des routes dans un module separe
router = APIRouter(prefix="/users", tags=["users"])

# Base de Donnee temporaire
users_db = []

# 1.GET /users - Liste de tous les utilisatuers 
@router.get("/", response_model=List[UserResponse])
async def get_users(
    current_user: User = Depends(get_current_user),
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
    db_user = UserService.get_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return db_user

 
# 4. PUT /users/{user_id} - Mise a jour complete
@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, 
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="YOu can only update your own profile"
        )
        
    db_user = UserService.update(db, user_id, user_update)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# 5. DELETE /users/{user_id} - Supprimer une utilisateur
@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own account"
        )
        
    success = UserService.delete(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return None
        
    