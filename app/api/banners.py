from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from pydantic import BaseModel
from datetime import date, datetime

from app.models.models import Banner, User
from app.db.database import get_db
from app.api.auth import get_current_user

router = APIRouter()

# Banner yaratish uchun schema
class BannerCreate(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: bool = True
    link_url: Optional[str] = None
    title: str
    image_url: Optional[str] = None
    description: Optional[str] = None

# Banner ma'lumotlarini qaytarish uchun schema
class BannerResponse(BaseModel):
    id: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: bool
    link_url: Optional[str] = None
    title: str
    image_url: Optional[str] = None
    description: Optional[str] = None
    
    class Config:
        from_attributes = True

# Yangi banner yaratish (faqat admin uchun)
@router.post("/", response_model=BannerResponse, status_code=status.HTTP_201_CREATED)
async def create_banner(
    banner_data: BannerCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Admin tekshiruvi
    
    # Yangi banner yaratish
    new_banner = Banner(
        start_date=banner_data.start_date,
        end_date=banner_data.end_date,
        is_active=banner_data.is_active,
        link_url=banner_data.link_url,
        title=banner_data.title,
        image_url=banner_data.image_url,
        description=banner_data.description
    )
    
    db.add(new_banner)
    await db.commit()
    await db.refresh(new_banner)
    
    return new_banner

# Barcha bannerlarni olish
@router.get("/", response_model=List[BannerResponse])
async def get_banners(
    active_only: bool = False,
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    if active_only:
        # Faqat faol bannerlarni olish
        today = datetime.now().date()
        query = select(Banner).where(
            (Banner.is_active == True) &
            ((Banner.start_date == None) | (Banner.start_date <= today)) &
            ((Banner.end_date == None) | (Banner.end_date >= today))
        ).offset(skip).limit(limit)
    else:
        # Barcha bannerlarni olish
        query = select(Banner).offset(skip).limit(limit)
    
    result = await db.execute(query)
    banners = result.scalars().all()
    
    return banners

# Banner ma'lumotlarini ID bo'yicha olish
@router.get("/{banner_id}", response_model=BannerResponse)
async def get_banner(
    banner_id: int, 
    db: AsyncSession = Depends(get_db)
):
    query = select(Banner).where(Banner.id == banner_id)
    result = await db.execute(query)
    banner = result.scalars().first()
    
    if not banner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Banner topilmadi"
        )
    
    return banner

# Bannerni yangilash (faqat admin uchun)
@router.put("/{banner_id}", response_model=BannerResponse)
async def update_banner(
    banner_id: int,
    banner_data: BannerCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Admin tekshiruvi
    
    query = select(Banner).where(Banner.id == banner_id)
    result = await db.execute(query)
    banner = result.scalars().first()
    
    if not banner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Banner topilmadi"
        )
    
    # Bannerni yangilash
    banner.start_date = banner_data.start_date
    banner.end_date = banner_data.end_date
    banner.is_active = banner_data.is_active
    banner.link_url = banner_data.link_url
    banner.title = banner_data.title
    banner.image_url = banner_data.image_url
    banner.description = banner_data.description
    
    await db.commit()
    await db.refresh(banner)
    
    return banner

# Bannerni o'chirish (faqat admin uchun)
@router.delete("/{banner_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_banner(
    banner_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Admin tekshiruvi
    
    query = select(Banner).where(Banner.id == banner_id)
    result = await db.execute(query)
    banner = result.scalars().first()
    
    if not banner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Banner topilmadi"
        )
    
    await db.delete(banner)
    await db.commit()
    
    return None 