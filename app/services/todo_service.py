from sqlalchemy.orm import Session

from app.models.todo import Todo
from app.schemas.todos import TodoCreate, TodoUpdate

class TodoService:
    @staticmethod
    def get_all(db: Session):
        return db.query(Todo).all()
    
    @staticmethod
    def get_by_id(db: Session, todo_id: int):
        return db.query(Todo).filter(Todo.id == todo_id).first()
    
    @staticmethod
    def create(db: Session, todo_data: TodoCreate):
        db_todo = Todo(**todo_data.model_dump())
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo) 
        return db_todo
    
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
        