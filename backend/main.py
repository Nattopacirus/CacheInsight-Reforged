from fastapi import FastAPI
from database import engine, Base
from contextlib import asynccontextmanager
from sqlalchemy import text
import models

# ---------------------------------------------------------
# 1. ฟังก์ชันทดสอบการเชื่อมต่อ DB
# ---------------------------------------------------------
def test_db_connection():
    try:
        # เปิด Connection และลองสั่ง Query ดึงชื่อ Database ปัจจุบัน
        with engine.connect() as connection:
            result = connection.execute(text("SELECT DB_NAME() AS current_db"))
            db_name = result.scalar()
            print("\n==========================================")
            print(f"✅ เชื่อมต่อได้แล้ว! ชื่อ DB: {db_name}")
            print("==========================================\n")
    except Exception as e:
        print("\n==========================================")
        print(f"❌ เชื่อมต่อ DB ไม่สำเร็จ! Error: {e}")
        print("==========================================\n")

# ---------------------------------------------------------
# 2. Lifespan Event สำหรับจัดการ Startup/Shutdown ใน FastAPI
# ---------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables
    Base.metadata.create_all(bind=engine)
    # ทำงานเมื่อ Server เริ่มต้นขึ้น (Startup)
    test_db_connection()
    yield
    # ทำงานเมื่อ Server ถูกปิดลง (Shutdown)
    engine.dispose()
    print("🔌 ปิดการเชื่อมต่อ Database เรียบร้อยแล้ว")

app = FastAPI(
    title="CacheInsight-Reforged API",
    lifespan=lifespan
)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Backend is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

#how to run 
"""
cd backend
venv\Scripts\activate
python -m uvicorn main:app --reload
"""