from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from pydantic import BaseModel

from app.models.models import User
from app.db.database import get_db
from app.api.auth import get_current_user

router = APIRouter()

# Foydalanuvchi yaratish uchun schema
class UserCreate(BaseModel):
    full_name: str
    phone: str
    email: Optional[str] = None
    password: str

# Foydalanuvchi ma'lumotlarini qaytarish uchun schema
class UserResponse(BaseModel):
    id: int
    full_name: str
    phone: str
    email: Optional[str] = None
    
    class Config:
        orm_mode = True

# Yangi foydalanuvchi yaratish
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Telefon raqami mavjudligini tekshirish
    query = select(User).where(User.phone == user_data.phone)
    result = await db.execute(query)
    existing_user = result.scalars().first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu telefon raqami bilan ro'yxatdan o'tilgan"
        )
    
    # Yangi foydalanuvchi yaratish
    # Haqiqiy loyihada parol hash qilinadi
    new_user = User(
        full_name=user_data.full_name,
        phone=user_data.phone,
        email=user_data.email,
        password_hash=user_data.password  # Haqiqiy loyihada: get_password_hash(user_data.password)
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user

# Barcha foydalanuvchilarni olish (faqat admin uchun)
@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Bu yerda admin tekshiruvi bo'lishi kerak
    
    query = select(User).offset(skip).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()
    
    return users

# Foydalanuvchi ma'lumotlarini ID bo'yicha olish
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Faqat o'z ma'lumotlarini yoki admin ko'ra oladi
    if current_user.id != user_id:
        # Admin tekshiruvi
        pass
    
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Foydalanuvchi topilmadi"
        )
    
    return user 