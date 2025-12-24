from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://dev_user:dev_password@localhost:5432/backend_intensif"
    # Cle secrete pour JWT 
    SECRET_KEY: str = "votre-cle-secrete-super-longue-et-aleatoire"

    class Config:
        env_file = ".env"
        
settings = Settings()        
