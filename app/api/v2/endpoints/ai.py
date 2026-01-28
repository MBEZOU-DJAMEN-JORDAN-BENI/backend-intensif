from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.ai import *
from app.services.ai.openai_service import OpenAIService
from app.api.deps import get_current_user
from app.db.database import get_db

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/suggestion", response_model=SuggestionResponse)
async def generate_suggestions(
    request: SuggestionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        suggestions = await OpenAIService.generate_todo_suggestions(
            context=request.context,
            num_suggestions=request.num_suggestions,
            db=db,
            user_id=current_user.id
        )
        
        return SuggestionResponse(suggestions=suggestions)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating suggestions: {str(e)}"
        )
        
@router.post("/analyze-priority", response_model=PriorityAnalysisResponse)
async def analyze_priority(
    request: PriorityAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        analysis = await OpenAIService.analyze_todo_priority(
            title=request.title,
            description=request.description,
            db=db,
            user_id=current_user.id
        )
        
        return PriorityAnalysisResponse(**analysis)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing priority: {str(e)}"
        )
        
@router.post("/improve-description", response_model=ImproveDescriptionResponse) 
async def improve_description(
    request: ImproveDescriptionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        improved_description = await OpenAIService.improve_todo_description(
            title=request.title,
            description=request.description,
            db=db,
            user_id=current_user.id
        )
        
        return ImproveDescriptionResponse(
            original=request.description,
            improved=improved_description
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error improving description: {str(e)}"
        )
        
@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        response = await OpenAIService.chat_with_history(
            user_message=request.messages,
            conversation_history=request.history,
            db=db,
            user_id=current_user.id 
        )        
        
        return ChatResponse(response=response)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in chat interaction: {str(e)}"
        )
        