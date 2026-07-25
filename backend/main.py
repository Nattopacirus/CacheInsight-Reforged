from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form, Depends, HTTPException, status
from database import engine, Base, get_db
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from sqlalchemy import text
from models import SimulationJob
from app.worker import run_simulation_job
import json
import os
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

@app.post("/api/simulate", status_code=status.HTTP_202_ACCEPTED)
async def simulate(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    config: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        config_dict = json.loads(config)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON config")

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are allowed")

    # 1. สร้าง Job
    new_job = SimulationJob(status="Pending", progress=0)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    job_id = new_job.id

    # 2. เซฟไฟล์
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{job_id}.csv"
    
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 3. เรียก background task
    background_tasks.add_task(run_simulation_job, job_id, file_path, config_dict)

    return {
        "job_id": job_id,
        "status": "Pending",
        "message": "Simulation started in background"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

#how to run 
"""
cd backend
venv\Scripts\activate
python -m uvicorn main:app --reload
"""