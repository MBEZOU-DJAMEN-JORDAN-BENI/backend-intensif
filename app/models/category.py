from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.todo import Todo
    
from app.db.database import Base

class Category(Base):
    __tablename__ = "categories"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Cle etrnagere
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False) 
    
    # Relations
    owner: Mapped["User"] = relationship("User", back_populates="categories")
    todos: Mapped[list["Todo"]] = relationship("Todo", back_populates="category")
