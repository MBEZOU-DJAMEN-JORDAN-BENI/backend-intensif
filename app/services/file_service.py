import time
import os
import uuid
import aiofiles
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
from PIL import Image
from io import BytesIO

from app.core.config import settings

class FileService:
    @staticmethod
    def validate_file(file: UploadFile) -> None:
        extension = file.filename.split(".")[-1].lower()
        if extension not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type '{extension}' is not allowed. The allowed types are: {settings.ALLOWED_EXTENSIONS}"
            )
            
    @staticmethod
    async def save_upload_file(
        file: UploadFile, 
        destination: str = "profiles"
    ) -> str:
        FileService.validate_file(file)
        
        extension = file.filename.split('.')[-1].lower()
        filename = f"{uuid.uuid4()}.{extension}"
        file_path = Path(settings.UPLOAD_DIRECTORY) / destination / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        content = await file.read()
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File size exceeds the maximum limit. Maximum allowed size is {settings.MAX_FILE_SIZE} bytes."
            )
            
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
            
        return filename
    
    @staticmethod
    async def save_profile_picture(
        file: UploadFile,
        user_id: int
    ) -> str:
        FileService.validate_file(file)
        
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is not a valid image."
            )
            
        # Lire le cotenu du fichier image
        content = await file.read()
        try:
            image = Image.open(BytesIO(content))
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is not a valid image."
            )
        
        # Gestion du mode de couleurs    
        if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.convert("RGBA").split()[3]) # 3rd channel is the alpha channel
            image = background
        elif image.mode != "RGB":
            image = image.convert("RGB")
            
        # Redimensionner l'image
        image = image.resize((300, 300))
        
        # Sauvegarder l'image redimensionnée
        timestamp = int(time.time())
        filename = f"user_{user_id}_{timestamp}.jpg"
        
        file_path = Path(settings.UPLOAD_DIRECTORY) / "profiles" / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Sauvegarder l'image en un format specifique
        image.save(file_path, "JPEG", quality=85)
        
        return filename
    
    @staticmethod
    def delete_file(filename: str, destination: str = "profiles") -> None:
        file_path = Path(settings.UPLOAD_DIRECTORY) / destination / filename
        if file_path.exists():
            file_path.unlink()
            return True
        return False
    