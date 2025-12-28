from fastapi import FastAPI, Request, status
from fatsapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError

import logging

from app.db.config import settings
from app.routes import todos, users, auth

app = FastAPI(
    title="API Backend Intensif",
    description="API REST avec Pydantic, Base de Donnees et Alembic",
    version="4.0.0"
)

app.include_router(auth.router)
app.include_router(users.router)  
app.include_router(todos.router)

# =============================
# CONFIGURATION DU LOGGING
# =============================

logging.basicConfig(
    level=logging.INFO,
    fromat='%(asctime)s - %(name)s - %(levlename)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==============================
#    GESTIONNAIRES D'ERREURS
# ===============================

@app.exception_handler(RequestValidationError)
async def validattion_exception_handler(request: Request, exc: RecursionError):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "message": "Validation error"
        }
    )
    
@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request: Request, exc:IntegrityError):
    logger.error(f"Database integrity error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_400_UNPROCESSSABLE_ENTITY,
        content={
            "detail": "Database constraint violation",
            "message": "The operation violatess a database contraint"
        }
    )    
    
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc:Exception):
    logger.error(f"Unhandler exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_UNPROCESSSABLE_ENTITY,
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
    allow_origins=settings.ALLPWED_ORIGINS,
    
    #Autoriser les coojies et l'authentification
    allow_credentials=True,
    
    # Methodes HTTP autorisees
    allow_methods=["*"],# Toutes les methodes (GET, POST, PUT, DELETE)
    
    # Headers autorises
    allow_headers=["*"], # Tous les headers autorises
)   
    