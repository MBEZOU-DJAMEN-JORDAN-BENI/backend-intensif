from sqlalchemy.orm import Session

from app.models.todo import Todo
from app.schemas.todos import TodoCreate, TodoUpdate

import logging

logger = logging.getLogger(__name__)

class TodoService:
    @staticmethod
    def create(db: Session, todo_data: TodoCreate, user_id: int):
        logger.info(f"Creating todo for user {user_id}: {todo_data.title}")
        
        try:
            db_todo = Todo(**todo_data.model_dump(), user_id=user_id)
            db.add(db_todo)
            db.commit()
            db.refresh(db_todo)
            
            logger.info(f"Todo created successfully: {db_todo}")
            return db_todo
        
        except Exception as e:
            logger.info(f"Error creating todo: {str(e)}")
            db.rollback()
            raise
        
                    
    @staticmethod
    def get_all(db: Session, user_id: int):
        return db.query(Todo).filter(Todo.user_id == user_id).all()
    
    @staticmethod
    def get_by_id(db: Session, todo_id: int):
        return db.query(Todo).filter(Todo.id == todo_id).first()
    
    @staticmethod
    def update(db:Session, todo_id: int, todo_data: TodoUpdate):
        #Recupere le todo
        db_todo = TodoService.get_by_id(db, todo_id)
        if not db_todo:
            return None
        
        # Convertir en dictionnnaire
        update_data = todo_data.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_todo, key, value)
            
        db.commit()
        db.refresh(db_todo)
        return db_todo

    @staticmethod
    def delete(db: Session, todo_id: int):
        db_todo = TodoService.get_by_id(db, todo_id)
        if not db_todo:
            return False
        
        db.delete(db_todo)
        db.commit()
        return True
        