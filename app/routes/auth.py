from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.users import UserCreate, UserResponse
from app.services.user_service import UserService
from app.models.user import User
from app.auth.security import create_access_token, verify_token
from datetime import timedelta
1
router = APIRouter(prefix="/auth", tags=["authentication"])

# CONFIGURATION OAuth2 Indique à FastAPI où obtenir le token, tokenUrl doit correspondre à la route de login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# ROUTE REGISTER

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Vérifier si le username existe déjà
    existing_user = UserService.get_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Vérifier si l'email existe déjà
    existing_email = UserService.get_by_email(db, user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Créer le user
    return UserService.create(db, user_data)

# ============================================
# ROUTE LOGIN
# ============================================

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Authentifier l'utilisateur
    user = UserService.authenticate(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Créer le token JWT
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=30)
    )
    
    # Format standard OAuth2
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# ============================================
# DEPENDENCY : Récupérer l'utilisateur courant
# ============================================

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    # Vérifier le token
    user_id = verify_token(token)
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Récupérer le user
    user = UserService.get_by_id(db, user_id)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user

# ROUTE /ME (utilisateur courant)
@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):

    return current_user