from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles 
from sqlalchemy.exc import IntegrityError

from datetime import datetime, timezone
import logging
import os

from app.core.config import settings
from app.api.v1.api import api_router
from app.api.v2.endpoints import ai

app = FastAPI(
    title="API Backend Intensif",
    description="API REST avec Pydantic, Base de Donnees, Authentification JWT et Alembic",
    version="6.1.3"
)

# Gestion des chemins de fichiers pour les uploads
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# =============================
# CONFIGURATION DU LOGGING
# =============================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==============================
#    GESTIONNAIRES D'ERREURS
# ===============================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "message": "Validation error"
        }
    )
    
@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request: Request, exc:IntegrityError):
    logger.error(f"Database integrity error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": "Database constraint violation",
            "message": "The operation violates a database constraint"
        }
    )    
    
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc:Exception):
    logger.error(f"Unhandler exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "message": "An unexpected error occurred"
        }
    )  
    
# =====================================
# CONFIGURATION CORS
# ==================================== 

app.add_middleware(
    CORSMiddleware,
    
    # Liste des origines autorisees
    allow_origins=settings.ALLOWED_ORIGINS,
    
    #Autoriser les coojies et l'authentification
    allow_credentials=True,
    
    # Methodes HTTP autorisees
    allow_methods=["*"],# Toutes les methodes (GET, POST, PUT, DELETE)
    
    # Headers autorises
    allow_headers=["*"], # Tous les headers autorises
)   

# ===========================================
# ENREGISTREMENT DES ROUTES 
# ===========================================

app.include_router(api_router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v2")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "6.1.3"
    }

@app.get("/")
async def root():
    return {
        "message": "API Backend Intensif",
        "version": "6.1.3",
        "status": "online",
        "docs": "/docs",
        "health": "/health"
    }
    
