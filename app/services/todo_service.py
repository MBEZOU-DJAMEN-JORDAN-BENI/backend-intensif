from operator import or_
from typing import Optional
from sqlalchemy.orm import Session
from math import ceil

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
    def get_paginated(
        db: Session,
        user_id: int, 
        skip: int = 0,
        limit: int = 20
    ) -> tuple:
        items = db.query(Todo)\
            .filter(Todo.user_id == user_id)\
            .offset(skip)\
            .limit(limit)\
            .all()
            
        total = db.query(Todo)\
            .filter(Todo.user_id == user_id)\
            .count()

        return items, total
    
    @staticmethod
    def serach_and_filter(
        db: Session,
        user_id: int,   
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
        done: Optional[bool] = None
    ) -> tuple:
        query = db.query(Todo).filter(Todo.user_id == user_id)
        
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(Todo.title.ilike(search_filter), Todo.description.ilike(search_filter))
            )
        
        if done is not None:
            query = query.filter(Todo.done == done)
        
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        
        return items, total
    
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
        