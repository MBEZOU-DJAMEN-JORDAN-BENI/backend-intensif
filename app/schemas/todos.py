from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# SCHEMA 1 : Creation d'un todo (entree)
class TodoCreate(BaseModel):
    title: str
    description: str
    priority:int = 1
    category_id: Optional[int] = None


# SCHEMA 2 : Reponse d'un todo (sortie)
class TodoResponse(BaseModel):
    id: int 
    title: str
    description: str
    priority: int
    done: bool
    user_id: int
    category_id: Optional[int] = None
    created_at: datetime
    update_at: datetime
        
    # Configuration interne du modele Pydantic
    class Config:
        from_attributes = True
        
    
# SCHEMA 3 : mise a jour partielle (optionnel)
class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    done: Optional[bool] = None
    priority: Optional[int] = None
    category_id: Optional[int] = None
    