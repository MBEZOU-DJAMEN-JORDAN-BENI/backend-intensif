# app/models/user.py
from app.models.ai_prediction import AIPrediction
from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.todo import Todo
    from app.models.category import Category
    
from app.db.database import Base
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relation 1-N avec rodo
    todos: Mapped[List["Todo"]] = relationship(
        "Todo",
        back_populates="owner",
        cascade="all, delete-orphan"
    )
    categories: Mapped[List["Category"]] = relationship("Category", back_populates="owner")
    
    # Fichier image (generalement) charger par l'utilisateur
    profile_picture: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relation 1-N avec les prédictions IA
    ai_predictions: Mapped[List["AIPrediction"]] = relationship(
        "AIPrediction",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}, hashed_password='{self.hashed_password}')>"