from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func  
from typing import List, Optional
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

@router.get("/", response_model=List[CategoryResponse])
async def get_categories(
    db: AsyncSession = Depends(get_db),
    name: Optional[str] = None,  # Filtrlash uchun
    sort_by: Optional[str] = "id",  # Default holatda ID bo‘yicha saralanadi
    order: Optional[str] = "asc",  # Default tartib (oshish tartibida)
):
    query = (
        select(
            Category.id,
            Category.created_at,
            Category.name,
            Category.description,
            Category.image_url,
            func.count(Barber.id).label("barber_count"),
        )
        .outerjoin(Barber, Category.id == Barber.category_id)
        .group_by(Category.id, Category.created_at, Category.name, Category.description, Category.image_url)
    )

    # **Nomi bo‘yicha filtr**
    if name:
        query = query.where(Category.name.ilike(f"%{name}%"))

    # **Saralash (Dynamic Order by)**
    sort_column = {
        "id": Category.id,
        "name": Category.name,
        "barber_count": func.count(Barber.id),
        "created_at": Category.created_at,
    }.get(sort_by, Category.id)  # Default: ID bo‘yicha tartiblash

    if order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    result = await db.execute(query)
    categories = result.all()

    return [
        {
            "id": row.id,
            "created_at": row.created_at,
            "name": row.name,
            "description": row.description,
            "image_url": row.image_url,
            "barber_count": row.barber_count,
        }
        for row in categories
    ]
