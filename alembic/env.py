from sqlalchemy.ext.asyncio import create_async_engine
import os
from dotenv import load_dotenv

# config.py o'rniga to'g'ridan-to'g'ri .env dan o'qiymiz
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

connectable = create_async_engine(
    DATABASE_URL,  # Asyncpg bilan to'g'ri formatda ulanish
    pool_pre_ping=True
)
