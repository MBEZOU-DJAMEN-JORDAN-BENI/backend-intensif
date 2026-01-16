from pydantic import BaseModel, Field
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.todos import TodoResponse

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    
class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int  
    name: str
    user_id: int
    
    class Config:
        from_attributes = True
        

class CategoryWithTodos(CategoryResponse):
    todos: List["TodoResponse"] = []

    class Config:
        from_attributes = True
        
class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50)

