from sqlalchemy.orm import Session
from typing import Optional, Dict
import json

from app.models.ai_prediction import AIPrediction

class PredictionTracker:
    @staticmethod
    def log_prediction(
        db: Session,
        user_id: int,
        prediction_type: str,
        prompt: str,
        response: str,
        prediction_metadata: Optional[Dict] = None,
        cost_cents: float = 0.0
    ) -> AIPrediction:
        prediction = AIPrediction(
            user_id=user_id,
            prediction_type=prediction_type,
            prompt=prompt,
            response=response,
            prediction_metadata=prediction_metadata or {},
            cost_cents=cost_cents
        )
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        return prediction
    
    @staticmethod
    def get_user_predictions(
        db: Session,
        user_id: int,
        prediction_type: Optional[str] = None,
        limit: int = 50
    ):
        """ Récupère l'historique des prédictions d'un utilisateur. """
        
        query = db.query(AIPrediction).filter(AIPrediction.user_id == user_id)
        if prediction_type:
            query = query.filter(AIPrediction.prediction_type == prediction_type)
        
        return query.order_by(AIPrediction.created_at.desc()).limit(limit).all()

    @staticmethod
    def calculate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
        pricing = {
            "gpt-4o-mini": {
                "input": 0.015,   # $0.15/1M = $0.015/1000
                "output": 0.06    # $0.60/1M = $0.06/1000
            },
            "gpt-4o": {
                "input": 0.25,    # $2.50/1M
                "output": 1.0     # $10/1M
            }
        }
        
        if model not in pricing:
            model = "gpt-4o-mini"  # Fallback
        
        input_cost = (prompt_tokens / 1000) * pricing[model]["input"]
        output_cost = (completion_tokens / 1000) * pricing[model]["output"]
        
        return round(input_cost + output_cost, 4)