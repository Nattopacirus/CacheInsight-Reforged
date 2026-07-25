from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from app.schemas import PresetCreate, PresetResponse
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

@app.get("/api/simulate/{job_id}")
def get_simulation_status(job_id: str, db: Session = Depends(get_db)):
    job = db.query(SimulationJob).filter(SimulationJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    result_data = None
    if job.result:
        try:
            result_data = json.loads(job.result)
        except json.JSONDecodeError:
            result_data = job.result
            
    return {
        "job_id": job.id,
        "status": job.status,
        "progress": job.progress,
        "result": result_data
    }

@app.get("/api/presets", response_model=List[PresetResponse])
def get_presets(db: Session = Depends(get_db)):
    return db.query(models.Preset).order_by(models.Preset.created_at.desc()).all()

@app.post("/api/presets", response_model=PresetResponse, status_code=status.HTTP_201_CREATED)
def create_preset(preset: PresetCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Preset).filter(models.Preset.name == preset.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Preset name already exists")
    
    new_preset = models.Preset(
        name=preset.name,
        cache_size=preset.cache_size,
        block_size=preset.block_size,
        mapping_type=preset.mapping_type,
        n_way=preset.n_way,
        replacement_policy=preset.replacement_policy
    )
    db.add(new_preset)
    db.commit()
    db.refresh(new_preset)
    return new_preset

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

#how to run 
"""
cd backend
venv\Scripts\activate
python -m uvicorn main:app --reload
"""