from sqlalchemy import Integer, String, Text, DateTime, Float, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.database import Base

class AIPrediction(Base):
    __tablename__ = "ai_predictions"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    prediction_type: Mapped[str] = mapped_column(String(50), nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    response: Mapped[str] = mapped_column(Text, nullable=True)
    prediction_metadata: Mapped[dict] = mapped_column(JSON, nullable=True)

    cost_cents: Mapped[float] = mapped_column(Float, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="ai_predictions")
    
    def __repr__(self):
        return f"<AIPrediction(id={self.id}, user_id={self.user_id}, prediction_type='{self.prediction_type}')>"
    