from fastapi import FastAPI
from routes import auth  # Auth routerni chaqiramiz

app = FastAPI()

# Bosh sahifa uchun API
@app.get("/")
def home():
    return {"message": "FastAPI ishlayapti!"}

# Auth routerni qo'shish
app.include_router(auth.router, prefix="/auth")
