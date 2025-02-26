from sqlalchemy.ext.asyncio import create_async_engine
import os
import sys
from dotenv import load_dotenv

# Loyiha ildiz papkasini `sys.path` ga qo‘shish
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from models.models import Base  # models.py dan bazaviy classni import qilamiz

# config.py o'rniga to'g'ridan-to'g'ri .env dan o'qiymiz
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

connectable = create_async_engine(
    DATABASE_URL,  # Asyncpg bilan to'g'ri formatda ulanish
    pool_pre_ping=True
)

target_metadata = Base.metadata  # Alembic uchun metadata o‘rnatamiz