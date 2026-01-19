from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from splqlalchemy.orm import Session

from app.db.database import get_db
from app.services.file_service import FileService
from app.services.user_service import UserService
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/profile-picture", status_code=status.HTTP_200_OK)
async def upload_profile_picture(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.profile_picture:
       FileService.delete_file(current_user.profile_picture, destination="profiles")

    filename = await FileService.save_profile_picture(file, user_id=current_user.id)
    
    current_user.profile_picture = filename
    db.commit()
    db.refresh(current_user)
    
    return {
        "message": "Profile picture uploaded successfully.",
        "filename": filename,
        "url": f"upload/profiles/{filename}"
    }
    
@router.delete("/profile-picture", status_code=status.HTTP_200_OK)
async def delete_profile_picture(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.profile_picture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No profile picture to delete."
        )
    
    FileService.delete_file(current_user.profile_picture, destination="profiles")
    
    current_user.profile_picture = None
    db.commit()
    db.refresh(current_user)
    
    return {
        "message": "Profile picture deleted successfully."
    }
    
    
    