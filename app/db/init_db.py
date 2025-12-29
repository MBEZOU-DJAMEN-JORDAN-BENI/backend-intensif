from app.models.user import User
from app.models.todo import Todo
from app.models.category import Category
from app.db.database import engine, Base

def init_db():
    print("Creation des Tables dans la base de donnees...")
    Base.metadata.create_all(bind=engine)
    print("Table crees avec succes !")
    
if __name__ == "__main__":
    init_db()    