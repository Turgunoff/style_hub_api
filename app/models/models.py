from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Enum, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum
from datetime import datetime
from app.db.database import Base  # Import Base from app.db.database

# Buyurtma statusi uchun ENUM
class AppointmentStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"

# 1. Foydalanuvchilar jadvali (Clients)
class User(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    phone = Column(String, unique=True, nullable=True)  # phone maydoni ixtiyoriy
    password_hash = Column(Text, nullable=False)
    role = Column(String, nullable=True)  # role ixtiyoriy
    email = Column(String, unique=True, nullable=False)  # email majburiy
    full_name = Column(String, nullable=False)  # full_name majburiy
    
    appointments = relationship("Appointment", back_populates="user")

# 2. Xizmat kategoriyalari jadvali (Categories)
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)

    services = relationship("Service", back_populates="category")
    barbers = relationship("Barber", back_populates="category")

# 3. Xizmatlar jadvali (Services)
class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    duration = Column(Integer, nullable=False)  # Xizmat davomiyligi (minut)

    category = relationship("Category", back_populates="services")
    appointments = relationship("Appointment", back_populates="service")

# 4. Buyurtmalar jadvali (Appointments)
class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    barber_id = Column(Integer, ForeignKey("barbers.id"), nullable=True)  # Barber ID qo'shamiz
    appointment_time = Column(DateTime, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.pending)

    user = relationship("User", back_populates="appointments")
    service = relationship("Service", back_populates="appointments")
    barber = relationship("Barber", back_populates="appointments")  # Barber bilan bog'laymiz

# Barber modeli
class Barber(Base):
    __tablename__ = "barbers"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    bio = Column(String, nullable=True)
    experience = Column(Integer, nullable=True)
    rating = Column(Float, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Barber bilan bog'liq bo'lgan buyurtmalar
    appointments = relationship("Appointment", back_populates="barber")
    category = relationship("Category", back_populates="barbers")

# Banner modeli
class Banner(Base):
    __tablename__ = "banners"

    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    image_url = Column(String, nullable=True)
