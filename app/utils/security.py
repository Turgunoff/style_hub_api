import bcrypt
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt

from app.core.config import settings

def get_password_hash(password: str) -> str:
    """Parolni hashlash"""
    salt = bcrypt.gensalt(rounds=settings.PWD_SALT_ROUNDS)
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Parolni tekshirish"""
    return bcrypt.checkpw(
        plain_password.encode(),
        hashed_password.encode()
    )

def create_token(data: dict, expires_delta: Optional[timedelta] = None, is_refresh: bool = False) -> str:
    """Token yaratish (access yoki refresh)"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        if is_refresh:
            expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "type": "refresh" if is_refresh else "access"
    })
    
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_token(token: str, is_refresh: bool = False) -> dict:
    """Tokenni tekshirish va payload qaytarish"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != ("refresh" if is_refresh else "access"):
            raise JWTError("Invalid token type")
        return payload
    except JWTError:
        return None