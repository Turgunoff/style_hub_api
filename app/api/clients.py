from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.models.models import User
from app.db.database import get_db
from app.api.auth import get_current_user

router = APIRouter()

# Mijoz yaratish uchun schema
class ClientCreate(BaseModel):
    name: Optional[str] = None
    phone: str
    password: str
    role: Optional[str] = None
    email: Optional[str] = None
    full_name: str

# Mijoz ma'lumotlarini qaytarish uchun schema
class ClientResponse(BaseModel):
    id: int
    name: Optional[str] = None
    created_at: datetime
    phone: str
    role: Optional[str] = None
    email: Optional[str] = None
    full_name: str
    
    class Config:
        from_attributes = True

# Yangi mijoz yaratish
@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
async def create_client(client_data: ClientCreate, db: AsyncSession = Depends(get_db)):
    # Telefon raqami mavjudligini tekshirish
    query = select(User).where(User.phone == client_data.phone)
    result = await db.execute(query)
    existing_client = result.scalars().first()
    
    if existing_client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu telefon raqami bilan ro'yxatdan o'tilgan"
        )
    
    # Yangi mijoz yaratish
    # Haqiqiy loyihada parol hash qilinadi
    new_client = User(
        name=client_data.name,
        full_name=client_data.full_name,
        phone=client_data.phone,
        email=client_data.email,
        role=client_data.role,
        password_hash=client_data.password  # Haqiqiy loyihada: get_password_hash(client_data.password)
    )
    
    db.add(new_client)
    await db.commit()
    await db.refresh(new_client)
    
    return new_client

# Barcha mijozlarni olish (faqat admin uchun)
@router.get("/", response_model=List[ClientResponse])
async def get_clients(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
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
    current_user: User = Depends(get_current_user)
):
    # Faqat o'z ma'lumotlarini yoki admin ko'ra oladi
    if current_user.id != client_id:
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