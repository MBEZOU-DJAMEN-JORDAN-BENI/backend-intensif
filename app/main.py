from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError

from datetime import datetime
import logging

from app.core.config import settings
from app.api.v1.api import api_router

app = FastAPI(
    title="API Backend Intensif",
    description="API REST avec Pydantic, Base de Donnees, Authentification JWT et Alembic",
    version="6.1.3"
)

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
async def validattion_exception_handler(request: Request, exc: RecursionError):
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
            "message": "The operation violatess a database contraint"
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

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version":"1.0.0"
    }

@app.get("/")
async def root():
    return{
        "message": "API Backend Intensif",
        "version": "1.0.0",
        "satus": "online",
        "docs": "/docs",
        "health": "health"
    }
    
