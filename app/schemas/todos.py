from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# SCHEMA 1 : Creation d'un todo (entree)
class TodoCreate(BaseModel):
    title: str
    description: str
    priority:int = 1


# SCHEMA 2 : Reponse d'un todo (sortie)
class TodoResponse(BaseModel):
    id: int 
    title: str
    description: str
    priority: int
    done: bool
    user_id: int
    created_at: datetime
    update_at: datetime
        
    # Configuration interne du modele Pydantic
    class Config:
        form_attributes = True
        
    
# SCHEMA 3 : mise a jour partielle (optionnel)
class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    done: Optional[bool] = None
    
    
    
 