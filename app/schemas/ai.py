from pydantic import BaseModel
from typing import Optional, List, Dict

class SuggestionRequest(BaseModel):
    context: str
    num_suggestions: int = 3
    
class SuggestionResponse(BaseModel):
    suggestions: List[str]

class PriorityAnalysisRequest(BaseModel):
    title: str
    description: str
    
class PriorityAnalysisResponse(BaseModel):
    priority: str
    reasoning: str
    estimated_time: int  
    
class ImproveDescriptionRequest(BaseModel):
    title: str
    description: str
    
class ImproveDescriptionResponse(BaseModel):
    original: str
    improved: str
    
class ChatRequest(BaseModel):
    messages: str
    history: Optional[List[Dict[str, str]]] = None
    
class ChatResponse(BaseModel):
    response: str
    
