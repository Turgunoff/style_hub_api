from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta
from typing import Optional

from app.models.models import User
from app.db.database import get_db
from app.core.config import settings
from app.utils.security import (
    get_password_hash,
    verify_password,
    create_token,
    verify_token
)

# Router yaratish
router = APIRouter()

# Token olish uchun schema
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_client(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
    is_refresh: bool = False
) -> User:
    """Token orqali mijozni tekshirish"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autentifikatsiya talab qilinadi"
        )

    payload = verify_token(token, is_refresh)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token yaroqsiz yoki muddati tugagan"
        )

    client_id = payload.get("sub")
    if not client_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token noto'g'ri"
        )

    try:
        client_id = int(client_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token noto'g'ri"
        )

    query = select(User).where(User.id == client_id)
    result = await db.execute(query)
    client = result.scalars().first()

    if client is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mijoz topilmadi"
        )

    return client

@router.post("/token")
async def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Login qilish va tokenlar olish"""
    # Mijozni telefon raqami orqali qidirish
    query = select(User).where(User.phone == form_data.username)
    result = await db.execute(query)
    client = result.scalars().first()

    if not client:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Telefon raqami yoki parol noto'g'ri",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Parolni tekshirish
    if not verify_password(form_data.password, client.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Telefon raqami yoki parol noto'g'ri",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Access va Refresh tokenlarni yaratish
    access_token = create_token(data={"sub": str(client.id)})
    refresh_token = create_token(data={"sub": str(client.id)}, is_refresh=True)

    # Refresh tokenni cookie sifatida saqlash
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "client": {
            "id": client.id,
            "full_name": client.full_name,
            "phone": client.phone
        }
    }

@router.post("/refresh")
async def refresh_access_token(
    response: Response,
    refresh_token: Optional[str] = Cookie(None),
    db: AsyncSession = Depends(get_db)
):
    """Refresh token orqali yangi access token olish"""
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token topilmadi"
        )

    client = await get_current_client(refresh_token, db, is_refresh=True)
    
    # Yangi tokenlarni yaratish
    new_access_token = create_token(data={"sub": str(client.id)})
    new_refresh_token = create_token(data={"sub": str(client.id)}, is_refresh=True)

    # Yangi refresh tokenni cookie sifatida saqlash
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }

@router.post("/logout")
async def logout(response: Response):
    """Tizimdan chiqish"""
    response.delete_cookie(key="refresh_token")
    return {"message": "Muvaffaqiyatli chiqish amalga oshirildi"}

@router.get("/me")
async def read_clients_me(current_client: User = Depends(get_current_client)):
    """Joriy mijoz ma'lumotlarini olish"""
    return {
        "status": "logged_in",
        "client": {
            "id": current_client.id,
            "full_name": current_client.full_name,
            "phone": current_client.phone
        }
    }

@router.get("/check")
async def check_auth(current_client: User = Depends(get_current_client)):
    """Autentifikatsiya holatini tekshirish"""
    return {
        "status": "logged_in",
        "client_id": current_client.id
    } 