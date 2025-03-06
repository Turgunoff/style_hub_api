from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from pydantic import BaseModel
from datetime import date, datetime

from app.models.models import Banner, User
from app.db.database import get_db
from app.api.auth import get_current_client

router = APIRouter()

# Banner ma'lumotlarini qaytarish uchun schema
class BannerResponse(BaseModel):
    id: int
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: bool
    image_url: Optional[str] = None
    
    class Config:
        from_attributes = True
# Barcha bannerlarni olish
@router.get("/", response_model=List[BannerResponse])
async def get_banners(
    active_only: bool = False,
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    today = datetime.now()

    # Banner modelida faqat id, start_date, end_date, is_active, image_url ustunlari bor
    # To'liq Banner obyektini tanlaymiz
    query = select(Banner)

    if active_only:
        query = query.where(
            (Banner.is_active == True) &
            ((Banner.start_date == None) | (Banner.start_date <= today)) &
            ((Banner.end_date == None) | (Banner.end_date >= today))
        )

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    banners = result.scalars().all()  # scalars() orqali Banner obyektlarini olamiz

    return banners

# Banner ma'lumotlarini ID bo'yicha olish
@router.get("/{banner_id}", response_model=BannerResponse)
async def get_banner(
    banner_id: int, 
    db: AsyncSession = Depends(get_db)
):
    # Banner modelida faqat id, start_date, end_date, is_active, image_url ustunlari bor
    query = select(Banner).where(Banner.id == banner_id)
    
    result = await db.execute(query)
    banner = result.scalars().first()  # scalars() orqali Banner obyektini olamiz

    if not banner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Banner topilmadi"
        )

    return banner