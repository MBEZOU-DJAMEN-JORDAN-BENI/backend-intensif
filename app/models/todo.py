
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from datetime import datetime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.user import User
    from app.models.category import Category

from app.db.database import Base

# ===========================================
# MODELE TODO (TABLE DANS LA BASE DE DONNEES)
# ===========================================

class Todo(Base):
    __tablename__ = "todos"
    
    # COLONNES DE LA TABLE
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500))
    priority: Mapped[int] = mapped_column(Integer, default=1) # 1=basse, 2=moyenne et 3=haute
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    update_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    
    # Cle Etrnagere
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), nullable=True)
    
    #Relationship enver les users
    owner: Mapped["User"] = relationship("User", back_populates="todos")
    category: Mapped["Category"] = relationship("Category", back_populates="todos")
    
    #  METHODE __repr__ (Optionnelle mais utile)
    def __repr__(self):
        return f"<Todo(id={self.id}, title='{self.title}', user_id = {self.user_id})>" 