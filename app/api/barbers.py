from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from pydantic import BaseModel

from app.models.models import Barber, User
from app.db.database import get_db
from app.api.auth import get_current_client

router = APIRouter()

# Barber yaratish uchun schema
class BarberCreate(BaseModel):
    full_name: str
    phone: str
    email: Optional[str] = None
    bio: Optional[str] = None
    experience: Optional[int] = None
    rating: Optional[float] = None
    category_id: Optional[int] = None
    image_url: Optional[str] = None

# Barber ma'lumotlarini qaytarish uchun schema
class BarberResponse(BaseModel):
    id: int
    full_name: str
    phone: str
    email: Optional[str] = None
    bio: Optional[str] = None
    experience: Optional[int] = None
    rating: Optional[float] = None
    category_id: Optional[int] = None
    image_url: Optional[str] = None
    
    class Config:
        from_attributes = True

# Yangi barber yaratish (faqat admin uchun)
@router.post("/", response_model=BarberResponse, status_code=status.HTTP_201_CREATED)
async def create_barber(
    barber_data: BarberCreate, 
    db: AsyncSession = Depends(get_db),
    current_client: User = Depends(get_current_client)
):
    # Admin tekshiruvi
    
    # Telefon raqami mavjudligini tekshirish
    query = select(Barber).where(Barber.phone == barber_data.phone)
    result = await db.execute(query)
    existing_barber = result.scalars().first()
    
    if existing_barber:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu telefon raqami bilan barber ro'yxatdan o'tilgan"
        )
    
    # Yangi barber yaratish
    new_barber = Barber(
        full_name=barber_data.full_name,
        phone=barber_data.phone,
        email=barber_data.email,
        bio=barber_data.bio,
        experience=barber_data.experience,
        rating=barber_data.rating,
        category_id=barber_data.category_id,
        image_url=barber_data.image_url
    )
    
    db.add(new_barber)
    await db.commit()
    await db.refresh(new_barber)
    
    return new_barber

# Barcha barberlarni olish
@router.get("/", response_model=List[BarberResponse])
async def get_barbers(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    # is_active ustunini ishlatmasdan barcha barberlarni olish
    query = select(Barber).offset(skip).limit(limit)
    result = await db.execute(query)
    barbers = result.scalars().all()
    
    return barbers

# Barber ma'lumotlarini ID bo'yicha olish
@router.get("/{barber_id}", response_model=BarberResponse)
async def get_barber(
    barber_id: int, 
    db: AsyncSession = Depends(get_db)
):
    query = select(Barber).where(Barber.id == barber_id)
    result = await db.execute(query)
    barber = result.scalars().first()
    
    if not barber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Barber topilmadi"
        )
    
    return barber

# Barberni yangilash (faqat admin uchun)
@router.put("/{barber_id}", response_model=BarberResponse)
async def update_barber(
    barber_id: int,
    barber_data: BarberCreate,
    db: AsyncSession = Depends(get_db),
    current_client: User = Depends(get_current_client)
):
    # Admin tekshiruvi
    
    query = select(Barber).where(Barber.id == barber_id)
    result = await db.execute(query)
    barber = result.scalars().first()
    
    if not barber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Barber topilmadi"
        )
    
    # Barberni yangilash
    barber.full_name = barber_data.full_name
    barber.phone = barber_data.phone
    barber.email = barber_data.email
    barber.bio = barber_data.bio
    barber.experience = barber_data.experience
    barber.rating = barber_data.rating
    barber.category_id = barber_data.category_id
    barber.image_url = barber_data.image_url
    
    await db.commit()
    await db.refresh(barber)
    
    return barber

# Barberni o'chirish (faqat admin uchun)
@router.delete("/{barber_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_barber(
    barber_id: int,
    db: AsyncSession = Depends(get_db),
    current_client: User = Depends(get_current_client)
):
    # Admin tekshiruvi
    
    query = select(Barber).where(Barber.id == barber_id)
    result = await db.execute(query)
    barber = result.scalars().first()
    
    if not barber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Barber topilmadi"
        )
    
    # Barberni to'liq o'chirib tashlash
    await db.delete(barber)
    await db.commit()
    
    return None 