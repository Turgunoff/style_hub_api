from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI ishlayapti!"}

@app.get("/user/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": "Ali", "age": 25}

from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

@app.post("/create-user/")
def create_user(user: User):
    return {"message": f"Foydalanuvchi {user.name} yaratildi!", "age": user.age}
