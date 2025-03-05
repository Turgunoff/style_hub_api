import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import Optional
from functools import lru_cache

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
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS sozlamalari
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    # Password hashlash sozlamalari
    PWD_HASH_ALGORITHM: str = "bcrypt"
    PWD_SALT_ROUNDS: int = 12
    
    class Config:
        case_sensitive = True
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings() 