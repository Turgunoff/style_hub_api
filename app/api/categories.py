from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.models.models import Category, User
from app.db.database import get_db
from app.api.auth import get_current_user

router = APIRouter()

# Kategoriya yaratish uchun schema
class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None

# Kategoriya ma'lumotlarini qaytarish uchun schema
class CategoryResponse(BaseModel):
    id: int
    created_at: datetime
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    
    class Config:
        from_attributes = True

# Yangi kategoriya yaratish (faqat admin uchun)
@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Admin tekshiruvi
    
    # Kategoriya nomini tekshirish
    query = select(Category).where(Category.name == category_data.name)
    result = await db.execute(query)
    existing_category = result.scalars().first()
    
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu nomdagi kategoriya mavjud"
        )
    
    # Yangi kategoriya yaratish
    new_category = Category(
        name=category_data.name,
        description=category_data.description,
        image_url=category_data.image_url
    )
    
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    
    return new_category

# Barcha kategoriyalarni olish
@router.get("/", response_model=List[CategoryResponse])
async def get_categories(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    query = select(Category).offset(skip).limit(limit)
    result = await db.execute(query)
    categories = result.scalars().all()
    
    return categories

# Kategoriya ma'lumotlarini ID bo'yicha olish
@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: int, 
    db: AsyncSession = Depends(get_db)
):
    query = select(Category).where(Category.id == category_id)
    result = await db.execute(query)
    category = result.scalars().first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kategoriya topilmadi"
        )
    
    return category

# Kategoriyani yangilash (faqat admin uchun)
@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category_data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Admin tekshiruvi
    
    query = select(Category).where(Category.id == category_id)
    result = await db.execute(query)
    category = result.scalars().first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kategoriya topilmadi"
        )
    
    # Kategoriyani yangilash
    category.name = category_data.name
    category.description = category_data.description
    category.image_url = category_data.image_url
    
    await db.commit()
    await db.refresh(category)
    
    return category

# Kategoriyani o'chirish (faqat admin uchun)
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Admin tekshiruvi
    
    query = select(Category).where(Category.id == category_id)
    result = await db.execute(query)
    category = result.scalars().first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kategoriya topilmadi"
        )
    
    await db.delete(category)
    await db.commit()
    
    return None 