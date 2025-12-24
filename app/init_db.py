from app.database import engine, Base
from app.models.todo import Todo
from app.models.user import User

def init_db():
    print("Creation des Tables dans la base de donnees...")
    Base.metadata.create_all(bind=engine)
    print("Table crees avec succes !")
    
if __name__ == "__main__":
    init_db()    