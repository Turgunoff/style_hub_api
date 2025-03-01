from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func  
from typing import List
from pydantic import BaseModel
from datetime import datetime

from app.models.models import Category, Barber  
from app.db.database import get_db

router = APIRouter()

# Kategoriya ma'lumotlarini qaytarish uchun schema
class CategoryResponse(BaseModel):
    id: int
    created_at: datetime
    name: str
    description: str | None
    image_url: str | None
    barber_count: int  # Qo‘shildi

    class Config:
        from_attributes = True

# 📌 Barcha kategoriyalarni olish (limit va skip yo'q)
@router.get("/", response_model=List[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    query = (
        select(
            Category.id,
            Category.created_at,
            Category.name,
            Category.description,
            Category.image_url,
            func.count(Barber.id).label("barber_count")
        )
        .outerjoin(Barber, Category.id == Barber.category_id)
        .group_by(Category.id, Category.created_at, Category.description, Category.image_url)
        .order_by(func.count(Barber.id).desc())  # 📌 Barberlar soni bo‘yicha kamayish tartibida saralash
    )

    result = await db.execute(query)
    categories = result.all()

    return [
        {
            "id": row.id,
            "created_at": row.created_at,
            "name": row.name,
            "description": row.description,
            "image_url": row.image_url,
            "barber_count": row.barber_count
        }
        for row in categories
    ]
