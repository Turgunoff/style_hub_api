# Sartaroshxona API

## Loyiha haqida

Sartaroshxona API - sartaroshxona xizmatlarini bron qilish uchun dastur. Foydalanuvchilar:

- Xizmatlarni ko'rish
- Sartaroshlarni tanlash
- Uchrashuv vaqtini belgilash imkoniyatlariga ega

## O'rnatish

### Talab qilinadigan dasturlar

- Python 3.8+
- PostgreSQL ma'lumotlar bazasi

### O'rnatish bosqichlari

1. Repozitoriyani klonlash

   ```bash
   git clone https://github.com/Turgunoff/sartaroshxona_api.git
   cd sartaroshxona_api
   ```

2. Virtual muhitni yaratish va faollashtirish

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows uchun: venv\Scripts\activate
   ```

3. Kerakli kutubxonalarni o'rnatish

   ```bash
   pip install -r requirements.txt
   ```

4. Muhit faylini yaratish

   ```bash
   cp .env.example .env
   ```

   Keyin `.env` faylini o'zingizning ma'lumotlar bazasi ma'lumotlari va boshqa sozlamalar bilan to'ldiring.

5. Ma'lumotlar bazasini sozlash

   ```bash
   alembic upgrade head
   ```

6. Dasturni ishga tushirish
   ```bash
   uvicorn app.main:app --reload
   ```

## Muhit o'zgaruvchilari

Asosiy katalogda quyidagi o'zgaruvchilar bilan `.env` faylini yarating:

DATABASE_URL=postgresql://username:password@localhost:5432/sartaroshxona
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
