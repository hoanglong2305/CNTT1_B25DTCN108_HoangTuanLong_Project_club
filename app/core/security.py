import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings

def handle_hash_password(raw_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(raw_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def check_password(raw_password: str, hash_password: str) -> bool:
    return bcrypt.checkpw(
        raw_password.encode("utf-8"), 
        hash_password.encode("utf-8")
    )

def create_access_token(user_id: int, username: str, role: str) -> str:
    now = datetime.now(timezone.utc)
    
    payload = {
        "sub": str(user_id),
        "user_name": username,
        "role_account": role,
        "iat": now,
        "exp": now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)