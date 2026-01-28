from sqlalchemy.orm import Session
from typing import Optional

from app.models.category import Category
from app.schemas.categories import CategoryCreate, CategoryUpdate

import logging

logger = logging.getLogger(__name__)

class CategoryService:
    @staticmethod
    def create(db: Session, category_data: CategoryCreate, user_id: int):
        logger.info(f"Creating category for user {user_id}: {category_data.name}")
        
        try:
            db_category = Category(**category_data.model_dump(), user_id=user_id)
            db.add(db_category)
            db.commit()
            db.refresh(db_category)
            
            logger.info(f"Category created successfully: {db_category}")
            return db_category
        
        except Exception as e:
            logger.error(f"Error creating category: {str(e)}")
            db.rollback()
            raise
        
                    
    @staticmethod
    def get_all(db: Session, user_id: int):
        return db.query(Category).filter(Category.user_id == user_id).all()
    
    @staticmethod
    def get_by_id(db: Session, category_id: int, user_id: int) -> Optional[Category]:
        """Récupère une catégorie par son ID, vérifie qu'elle appartient à l'utilisateur"""
        return db.query(Category).filter(
            Category.id == category_id,
            Category.user_id == user_id
        ).first()
    
    @staticmethod
    def update(db: Session, category_id: int, category_data: CategoryUpdate, user_id: int) -> Optional[Category]:
        """Met à jour une catégorie, vérifie que l'utilisateur en est le propriétaire"""
        db_category = CategoryService.get_by_id(db, category_id, user_id)
        if not db_category:
            return None
        
        # Convertir en dictionnaire
        update_data = category_data.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_category, key, value)
            
        db.commit()
        db.refresh(db_category)
        return db_category

    @staticmethod
    def delete(db: Session, category_id: int, user_id: int) -> bool:
        """Supprime une catégorie, vérifie que l'utilisateur en est le propriétaire"""
        db_category = CategoryService.get_by_id(db, category_id, user_id)
        if not db_category:
            return False
        
        db.delete(db_category)
        db.commit()
        return True
        