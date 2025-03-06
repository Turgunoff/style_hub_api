from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.models.models import User, Category, Service, Appointment, AppointmentStatus
from app.db.database import get_db
from app.api.auth import get_current_client

router = APIRouter()

# Buyurtma yaratish uchun schema
class AppointmentCreate(BaseModel):
    service_id: int
    appointment_time: datetime

# Buyurtma ma'lumotlarini qaytarish uchun schema
class AppointmentResponse(BaseModel):
    id: int
    user_id: int
    service_id: int
    appointment_time: datetime
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Yangi buyurtma yaratish
@router.post("/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    appointment_data: AppointmentCreate, 
    db: AsyncSession = Depends(get_db),
    current_client: User = Depends(get_current_client)
):
    # Xizmat mavjudligini tekshirish
    query = select(Service).where(Service.id == appointment_data.service_id)
    result = await db.execute(query)
    service = result.scalars().first()
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Xizmat topilmadi"
        )
    
    # Vaqt bo'sh ekanligini tekshirish
    # Bu yerda vaqt bo'sh ekanligini tekshirish logikasi bo'lishi kerak
    
    # Yangi buyurtma yaratish
    new_appointment = Appointment(
        user_id=current_client.id,
        service_id=appointment_data.service_id,
        appointment_time=appointment_data.appointment_time,
        status=AppointmentStatus.pending
    )
    
    db.add(new_appointment)
    await db.commit()
    await db.refresh(new_appointment)
    
    return new_appointment

# Foydalanuvchining barcha buyurtmalarini olish
@router.get("/my", response_model=List[AppointmentResponse])
async def get_my_appointments(
    skip: int = 0, 
    limit: int = 100, 
    status: Optional[AppointmentStatus] = None,
    db: AsyncSession = Depends(get_db),
    current_client: User = Depends(get_current_client)
):
    if status:
        query = select(Appointment).where(
            Appointment.user_id == current_client.id,
            Appointment.status == status
        ).offset(skip).limit(limit)
    else:
        query = select(Appointment).where(
            Appointment.user_id == current_client.id
        ).offset(skip).limit(limit)
    
    result = await db.execute(query)
    appointments = result.scalars().all()
    
    return appointments

# Barcha buyurtmalarni olish (faqat admin uchun)
@router.get("/", response_model=List[AppointmentResponse])
async def get_appointments(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db),
    current_client: User = Depends(get_current_client)
):
    # Bu yerda admin tekshiruvi bo'lishi kerak
    
    query = select(Appointment).offset(skip).limit(limit)
    result = await db.execute(query)
    appointments = result.scalars().all()
    
    return appointments

# Buyurtma ma'lumotlarini ID bo'yicha olish
@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(
    appointment_id: int, 
    db: AsyncSession = Depends(get_db),
    current_client: User = Depends(get_current_client)
):
    query = select(Appointment).where(Appointment.id == appointment_id)
    result = await db.execute(query)
    appointment = result.scalars().first()
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Buyurtma topilmadi"
        )
    
    # Faqat o'z buyurtmasini yoki admin ko'ra oladi
    if appointment.user_id != current_client.id:
        # Admin tekshiruvi
        pass
    
    return appointment

# Buyurtma statusini yangilash
@router.put("/{appointment_id}/status", response_model=AppointmentResponse)
async def update_appointment_status(
    appointment_id: int,
    status: AppointmentStatus,
    db: AsyncSession = Depends(get_db),
    current_client: User = Depends(get_current_client)
):
    query = select(Appointment).where(Appointment.id == appointment_id)
    result = await db.execute(query)
    appointment = result.scalars().first()
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Buyurtma topilmadi"
        )
    
    # Faqat o'z buyurtmasini yoki admin o'zgartira oladi
    if appointment.user_id != current_client.id:
        # Admin tekshiruvi
        pass
    
    # Statusni yangilash
    appointment.status = status
    
    await db.commit()
    await db.refresh(appointment)
    
    return appointment

# Buyurtmani bekor qilish
@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_db),
    current_client: User = Depends(get_current_client)
):
    query = select(Appointment).where(Appointment.id == appointment_id)
    result = await db.execute(query)
    appointment = result.scalars().first()
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Buyurtma topilmadi"
        )
    
    # Faqat o'z buyurtmasini yoki admin o'zgartira oladi
    if appointment.user_id != current_client.id:
        # Admin tekshiruvi
        pass
    
    # Buyurtmani bekor qilish
    appointment.status = AppointmentStatus.cancelled
    
    await db.commit()
    
    return None 