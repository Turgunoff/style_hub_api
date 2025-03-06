from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from pydantic import BaseModel

from app.models.models import Service, Category, User
from app.db.database import get_db
from app.api.auth import get_current_client

router = APIRouter()

# Xizmat yaratish uchun schema
class ServiceCreate(BaseModel):
    category_id: int
    name: str
    description: Optional[str] = None
    price: float
    duration: int  # Xizmat davomiyligi (minut)

# Xizmat ma'lumotlarini qaytarish uchun schema
class ServiceResponse(BaseModel):
    id: int
    category_id: int
    name: str
    description: Optional[str] = None
    price: float
    duration: int
    
    class Config:
        from_attributes = True

# Yangi xizmat yaratish (faqat admin uchun)
@router.post("/", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
async def create_service(
    service_data: ServiceCreate, 
    db: AsyncSession = Depends(get_db),
    current_client: User = Depends(get_current_client)
):
    # Admin tekshiruvi
    
    # Kategoriya mavjudligini tekshirish
    query = select(Category).where(Category.id == service_data.category_id)
    result = await db.execute(query)
    category = result.scalars().first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kategoriya topilmadi"
        )
    
    # Yangi xizmat yaratish
    new_service = Service(
        category_id=service_data.category_id,
        name=service_data.name,
        description=service_data.description,
        price=service_data.price,
        duration=service_data.duration
    )
    
    db.add(new_service)
    await db.commit()
    await db.refresh(new_service)
    
    return new_service

# Barcha xizmatlarni olish
@router.get("/", response_model=List[ServiceResponse])
async def get_services(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    query = select(Service).offset(skip).limit(limit)
    result = await db.execute(query)
    services = result.scalars().all()
    
    return services

# Xizmat ma'lumotlarini ID bo'yicha olish
@router.get("/{service_id}", response_model=ServiceResponse)
async def get_service(
    service_id: int, 
    db: AsyncSession = Depends(get_db)
):
    query = select(Service).where(Service.id == service_id)
    result = await db.execute(query)
    service = result.scalars().first()
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Xizmat topilmadi"
        )
    
    return service

# Xizmatni yangilash (faqat admin uchun)
@router.put("/{service_id}", response_model=ServiceResponse)
async def update_service(
    service_id: int,
    service_data: ServiceCreate,
    db: AsyncSession = Depends(get_db),
    current_client: User = Depends(get_current_client)
):
    # Admin tekshiruvi
    
    # Xizmatni tekshirish
    query = select(Service).where(Service.id == service_id)
    result = await db.execute(query)
    service = result.scalars().first()
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Xizmat topilmadi"
        )
    
    # Kategoriyani tekshirish
    query = select(Category).where(Category.id == service_data.category_id)
    result = await db.execute(query)
    category = result.scalars().first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kategoriya topilmadi"
        )
    
    # Xizmatni yangilash
    service.category_id = service_data.category_id
    service.name = service_data.name
    service.description = service_data.description
    service.price = service_data.price
    service.duration = service_data.duration
    
    await db.commit()
    await db.refresh(service)
    
    return service

# Xizmatni o'chirish (faqat admin uchun)
@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(
    service_id: int,
    db: AsyncSession = Depends(get_db),
    current_client: User = Depends(get_current_client)
):
    # Admin tekshiruvi
    
    query = select(Service).where(Service.id == service_id)
    result = await db.execute(query)
    service = result.scalars().first()
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Xizmat topilmadi"
        )
    
    await db.delete(service)
    await db.commit()
    
    return None 