from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.todos import TodoResponse

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(...,min_length=8, max_length=50) 
       
class UserResponse(UserBase):
    id: int
    username: str
    email: str
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True
        
            
class UserWithTodos(UserResponse):
    todos: List["TodoResponse"] = []    
    
    class Config:
        from_attributes = True
        
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None    
    