from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.models import User  # User modelini import qilamiz
from database import get_db  # DB sessiyasini olish uchun funksiya

app = FastAPI()

# Token olish uchun schema
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Yashirin kalit va algoritm
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    """
    Token orqali foydalanuvchini tekshirish.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token noto‘g‘ri")
        
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        user = result.scalars().first()

        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Foydalanuvchi topilmadi")

        return {"status": "logged_in", "user_id": user.id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Yaroqsiz token")

@app.get("/check-auth/")
async def check_auth(user: dict = Depends(get_current_user)):
    """
    Foydalanuvchi tizimga kirganmi yoki yo‘qligini tekshiradi.
    """
    return user
