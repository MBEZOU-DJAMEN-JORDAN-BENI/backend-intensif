from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    
    # Base de Donnee
    DATABASE_URL: str
    
    # Securite
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 

    # Environment
    ENVIRONMENT: str = "development"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        
settings = Settings()        
