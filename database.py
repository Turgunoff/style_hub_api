import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# .env fayldagi o'zgaruvchilarni yuklash
load_dotenv()

# .env fayldan DATABASE_URL ni olish
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy database engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Session yaratish
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()

# Dependency: Database sessiyani olish
async def get_db():
    async with SessionLocal() as session:
        yield session
