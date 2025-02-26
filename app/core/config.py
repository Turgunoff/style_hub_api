import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

class Settings(BaseSettings):
    """
    Dastur konfiguratsiyasi uchun asosiy sozlamalar
    """
    # API sozlamalari
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "StyleHub API"
    
    # Ma'lumotlar bazasi sozlamalari
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # JWT sozlamalari
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY .env faylda yo'q! Uni qo'shing.")
    
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS sozlamalari
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    class Config:
        case_sensitive = True

# Sozlamalar obyektini yaratish
settings = Settings() 