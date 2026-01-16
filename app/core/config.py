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
    
    @property
    def sqlalchemy_database_url(self) -> str:
        """
        Corrige l'URL pour SQLAlchemy (Postgres exigence postgresql://)
        """
        url = self.DATABASE_URL
        if url and url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # Permet de ne pas planter si une variable manque en local 
        # mais est présente sur Railway
        extra = "ignore"
        
settings = Settings()        
