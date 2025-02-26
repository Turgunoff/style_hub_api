import os
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv

# .env faylni yuklash
load_dotenv()

# DATABASE_URL ni olish
DATABASE_URL = os.getenv("DATABASE_URL")

# Async connection uchun create_async_engine ishlatamiz
engine = create_async_engine(DATABASE_URL)

async def test_connection():
    try:
        async with engine.connect() as connection:
            print("✅ Database successfully connected!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")

# Asinxron kodni ishga tushirish
import asyncio
asyncio.run(test_connection())
