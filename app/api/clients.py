from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime

from app.models.models import User
from app.db.database import get_db
from app.api.auth import get_current_client
from app.utils.security import get_password_hash

router = APIRouter()

# Mijoz yaratish uchun schema
class ClientCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 6:
            raise ValueError('Parol kamida 6 ta belgidan iborat bo\'lishi kerak')
        return v

# Mijoz ma'lumotlarini qaytarish uchun schema
class ClientResponse(BaseModel):
    id: int
    created_at: datetime
    email: str
    full_name: str
    
    class Config:
        from_attributes = True

@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
async def create_client(client_data: ClientCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Email mavjudligini tekshirish
        query = select(User).where(User.email == client_data.email)
        result = await db.execute(query)
        existing_client = result.scalars().first()
        
        if existing_client:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bu email bilan ro'yxatdan o'tilgan"
            )
        
        # Yangi mijoz yaratish
        hashed_password = get_password_hash(client_data.password)
        new_client = User(
            email=client_data.email,
            password_hash=hashed_password,
            full_name=client_data.full_name
        )
        
        db.add(new_client)
        await db.commit()
        await db.refresh(new_client)
        
        return new_client
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# Barcha mijozlarni olish (faqat admin uchun)
@router.get("/", response_model=List[ClientResponse])
async def get_clients(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db),
    current_client: User = Depends(get_current_client)
):
    # Bu yerda admin tekshiruvi bo'lishi kerak
    
    query = select(User).offset(skip).limit(limit)
    result = await db.execute(query)
    clients = result.scalars().all()
    
    return clients

# Mijoz ma'lumotlarini ID bo'yicha olish
@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: int, 
    db: AsyncSession = Depends(get_db),
    current_client: User = Depends(get_current_client)
):
    # Faqat o'z ma'lumotlarini yoki admin ko'ra oladi
    if current_client.id != client_id:
        # Admin tekshiruvi
        pass
    
    query = select(User).where(User.id == client_id)
    result = await db.execute(query)
    client = result.scalars().first()
    
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mijoz topilmadi"
        )
    
    return client 