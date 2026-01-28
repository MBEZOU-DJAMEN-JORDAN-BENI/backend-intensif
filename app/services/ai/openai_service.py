from openai import AsyncOpenAI
from sqlalchemy.orm import Session
from typing import Optional, List, Dict

from app.core.config import settings
from app.services.ai.prediction_tracker import PredictionTracker

client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY,
)

class OpenAIService:
    @staticmethod
    async def generate_completion(
        prompt: str,
        system_message: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        db: Optional[Session] = None,
        user_id: Optional[int] = None,
        prediction_type: str = "completion"
    ) -> str:
        messages = []
        # Message system
        if system_message:
            messages.append({"role": "system", "content": system_message})
        # Message user
        messages.append({"role": "user", "content": prompt})

        try:
            response = await client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                temperature=temperature or settings.OPENAI_TEMPERATURE,
                max_tokens=max_tokens or settings.OPENAI_MAX_TOKENS,
            )
            # Log prediction if db and user_id are provided
            content = response.choices[0].message.content.strip()
            if db and user_id:
                cost = PredictionTracker.calculate_cost(
                    model=settings.OPENAI_MODEL,
                    prompt_tokens=response.usage.prompt_tokens,
                    completion_tokens=response.usage.completion_tokens
                )
                # Logger 
                PredictionTracker.log_prediction(
                    db=db,
                    user_id=user_id,
                    prediction_type=prediction_type,
                    prompt=prompt,
                    response=content,
                    prediction_metadata={
                        "model": settings.OPENAI_MODEL,
                        "temperature": temperature or settings.OPENAI_TEMPERATURE,
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens
                    },
                    cost_cents=cost
                )
                
            return content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
        
    @staticmethod
    async def generate_todo_suggestions(
        context: str,
        num_suggestions: int = 3
    ) -> List[str]:
        
        systems_message = """ Tu es un assistant de productivite intelligent.
        Tu génères des suggestions de tâches (todos) concrètes et actionnables.
        Chaque suggestion doit être :
        - Précise et actionnable
        - Réaliste
        - Formulée comme une tâche (verbe d'action)
        
        Réponds UNIQUEMENT avec les suggestions, une par ligne, sans numérotation."""
        
        prompt = f""" Genere {num_suggestions} suggestions de tâches pour atteindre cet objectif :

{context}

Suggestions :"""
        
        response = await OpenAIService.generate_completion(
            prompt=prompt,
            system_message=systems_message,
            temperature=0.7
        )
        
        suggestions = [
            line.strip()
            for line in response.split("\n")
            if line.strip()
        ]
        
        return suggestions[:num_suggestions]
    
    @staticmethod
    async def analyze_todo_priority(
        title: str,
        description: str
    ) -> Dict[str, any]:
        system_message = """Tu es un expert en gestion de projet.
        Analyse la priorité d'une tâche basée sur son titre et sa description.
        
        Réponds UNIQUEMENT en JSON avec cette structure :
        {
            "priority": "high" | "medium" | "low",
            "reasoning": "Explication courte",
            "estimated_time": nombre_de_minutes
        }"""
        
        prompt = f""" Analyse cette tache :
Titre : {title} 
Description : {description}
        
Analyse :"""

        response = await OpenAIService.generate_completion(
            prompt=prompt,
            system_message=system_message,
            temperature=0.3
        )
        import json
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "priority": "medium",
                "reasoning": "Analyse impossible",
                "estimated_time": 30
            }
            
    @staticmethod
    async def improve_todo_description(
        title: str, 
        description: str
    )-> str:
        system_message = """ Tu es un expert en productivite.
        Tu ameliores les description de taches pour les rendre:
        - Plus claires et precises
        - Plus actionnables
        - Mieux structurees
        
        Garde le meme sens mais ameliore la fomulation.
        Reponds UNIQUEMENT avec la description amelioree. """
        
        prompt = f""" Ameliore la description de cette tache :

Titre: {title}
Description actuelle : {description}

Description améliorée :"""

        return await OpenAIService.generate_completion(
            prompt=prompt,
            system_message=system_message,
            temperature=0.5
        ) 
        
    @staticmethod
    async def chat_with_history(
        user_message: str,
        conversation_history: List[Dict[str, str]] = None
    ) -> str:
        system_message = """Tu es un assistant de productivité amical et utile.
        Tu aides les utilisateurs à gérer leurs tâches et à être plus productifs.
        Sois concis mais chaleureux."""
        
        messages = [{"role": "system", "content": system_message}]
        
        # Ajouter l'historique
        if conversation_history:
            messages.extend(conversation_history)
        
        # Ajouter le nouveau message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            response = await client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"Erreur chat : {str(e)}")