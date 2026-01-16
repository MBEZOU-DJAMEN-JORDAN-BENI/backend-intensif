from sqlalchemy.orm import Session
from typing import Optional

from app.models.user import User
from app.schemas.users import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password

class UserService:
    
    @staticmethod
    def get_all(db: Session):
        return db.query(User).all()
    
    @staticmethod
    def get_by_id(db: Session, id: int):
        return db.query(User).filter(User.id == id).first()
    
    @staticmethod
    def get_by_username(db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def create(db: Session, user_data: UserCreate) -> User:
        # Vérifier si c'est le premier utilisateur pour le rendre admin
        total_users = db.query(User).count()
        is_admin = True if total_users == 0 else False
        
        # Créer un user avec le mot de passe hashe
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            username=user_data.username,
            email = user_data.email,
            hashed_password = hashed_password,
            is_admin = is_admin
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user) 
        return db_user
    
    @staticmethod
    def authenticate(db: Session, username: str, password: str) -> Optional[User]:
        user = UserService.get_by_username(db, username)
        
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
        
    @staticmethod
    def update(db:Session, user_id: int, user_data: UserUpdate):
        #Recupere le todo
        db_user = UserService.get_by_id(db, user_id)
        if not db_user:
            return None
        
        # Convertir en dictionnnaire
        update_data = user_data.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_user, key, value)
            
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def delete(db: Session, user_id: int):
        db_user = UserService.get_by_id(db, user_id)
        if not db_user:
            return False
        
        db.delete(db_user)
        db.commit()
        return True
        