from datetime import datetime, timedelta
from typing import Optional

# Bibliotheque pour generer les tokens
from jose import JWTError, jwt
# Bibliotheque pour hasher les mots de passe 
from passlib.context import CryptContext

from app.config import settings


# CONFIGURATION DU HASHING
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# CONFIGURATION JWT
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256" # Algorithme de chiffrement
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# FONCTION DE HASHING
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

3 # FONCTION JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    
    # Calculer la date d'expiration
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    # Ajouter l'expiration au payload
    to_encode.update({"exp": expire})
    
    # Creer le token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[int]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        
        if user_id is None:
            return None
        return int(user_id)
    except JWTError:
        return None
