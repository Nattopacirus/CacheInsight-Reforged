# แผนการพัฒนา: Phase 1 - โครงสร้างพื้นฐาน (Foundation & Infrastructure)

## สรุป (Summary)

เริ่มต้นสร้างโครงสร้างโปรเจกต์หลักสำหรับ CacheInsight-Reforged เราจะสร้างโฟลเดอร์ `backend` สำหรับแอปพลิเคชัน FastAPI, ตั้งค่าการเชื่อมต่อฐานข้อมูล MS SQL Server ด้วย SQLAlchemy, และสร้างโครงสร้างตาราง (models) ได้แก่ `presets` และ `simulation_jobs` นอกจากนี้ เราจะสร้างโฟลเดอร์ `frontend` และเริ่มต้นสร้างโปรเจกต์ Next.js คู่กับ Tailwind CSS เพื่อใช้เป็นโครงสร้างหน้าจอผู้ใช้ (UI shell)

## เรื่องราวของผู้ใช้งาน (User Story)

ในฐานะนักพัฒนา (Developer)
ฉันต้องการตั้งค่าสคีมาฐานข้อมูลฝั่ง Backend และเตรียมโครงสร้างเฟรมเวิร์กฝั่ง Frontend
เพื่อที่ฉันจะได้มีรากฐานที่มั่นคงสำหรับนำไปสร้างตรรกะการจำลองผลและส่วนประกอบหน้า UI ต่อไป

## ข้อมูลเบื้องต้น (Metadata)

| Field | Value |
|-------|-------|
| ประเภท (Type) | NEW_CAPABILITY |
| ความซับซ้อน (Complexity) | MEDIUM |
| ระบบที่เกี่ยวข้อง (Systems Affected) | backend, frontend, database |
| Jira Issue | N/A |

---

## รูปแบบที่ควรปฏิบัติตาม (Patterns to Follow)

### การตั้งชื่อ (Naming)
```python
# backend/models.py
class Preset(Base):
    __tablename__ = "presets"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    # ...
```

### การเชื่อมต่อฐานข้อมูล (Database Connection)
```python
# backend/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# อย่าลืมติดตั้ง pyodbc และระบุ Connection string ให้ถูกต้อง
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mssql+pyodbc://username:password@localhost/dbname?driver=ODBC+Driver+17+for+SQL+Server"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

---

## ไฟล์ที่ต้องเปลี่ยนแปลง (Files to Change)

| ไฟล์ (File) | การกระทำ (Action) | วัตถุประสงค์ (Purpose) |
|------|--------|---------|
| `backend/requirements.txt` | CREATE | เก็บรายชื่อ Dependencies ของ Python (FastAPI, SQLAlchemy, pyodbc) |
| `backend/.env.example` | CREATE | ไฟล์ตัวอย่างสำหรับการตั้งค่าการเชื่อมต่อฐานข้อมูล |
| `backend/database.py` | CREATE | ตั้งค่า SQLAlchemy engine และ session |
| `backend/models.py` | CREATE | กำหนดโครงสร้างตารางในฐานข้อมูล (`presets`, `simulation_jobs`) |
| `backend/main.py` | CREATE | ไฟล์เริ่มต้น (Entry point) สำหรับแอปพลิเคชัน FastAPI |
| `frontend/` | CREATE | สร้างโปรเจกต์ Next.js ผ่านคำสั่ง `create-next-app` |

---

## งานที่ต้องทำ (Tasks)

ให้ดำเนินการตามลำดับ แต่ละงานเป็นอิสระต่อกันและสามารถตรวจสอบผลลัพธ์ได้

### Task 1: เตรียมสภาพแวดล้อมฝั่ง Backend (Initialize Backend Environment)
- **ไฟล์ (File)**: `backend/requirements.txt`, `backend/main.py`, `backend/.env.example`
- **การกระทำ (Action)**: CREATE
- **การทำงาน (Implement)**: สร้างโฟลเดอร์ backend, ระบุ Dependencies ใน `requirements.txt` (fastapi, uvicorn, sqlalchemy, pyodbc, pydantic, python-dotenv), และสร้างแอปพลิเคชัน FastAPI พื้นฐานใน `main.py` พร้อมด้วย Health check endpoint จากนั้นเตรียมไฟล์ `.env.example` ให้พร้อม
- **การตรวจสอบ (Validate)**: สร้าง Virtual environment รันคำสั่ง `pip install -r requirements.txt` และ `uvicorn main:app --reload` เพื่อทดสอบว่าเซิร์ฟเวอร์เปิดใช้งานได้

### Task 2: ตั้งค่าสคีมาฐานข้อมูล (Setup Database Schema)
- **ไฟล์ (File)**: `backend/database.py`, `backend/models.py`
- **การกระทำ (Action)**: CREATE
- **การทำงาน (Implement)**: สร้างการเชื่อมต่อด้วย SQLAlchemy ใน `database.py` โดยใช้ MS SQL Server connection string สร้างคลาส `Preset` และ `SimulationJob` ใน `models.py` ให้ตรงกับข้อกำหนดใน PRD สุดท้ายเพิ่ม `Base.metadata.create_all` ใน `main.py` เพื่อให้สร้างตารางโดยอัตโนมัติเมื่อเริ่มเปิดแอป
- **การตรวจสอบ (Validate)**: ตั้งค่า Connection string ของ MS SQL ลงในไฟล์ `.env` ที่เครื่อง, รันแอปพลิเคชัน, และตรวจสอบว่าตารางถูกสร้างขึ้นในฐานข้อมูลเรียบร้อยแล้ว

### Task 3: สร้างโครงสร้างเริ่มต้นสำหรับ Next.js (Initialize Frontend Next.js Shell)
- **ไฟล์ (File)**: `frontend/`
- **การกระทำ (Action)**: CREATE
- **การทำงาน (Implement)**: รันคำสั่ง `npx create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"` (แบบ non-interactive) และต้องแน่ใจว่ามีโฟลเดอร์ `public` รวมอยู่ด้วย
- **การตรวจสอบ (Validate)**: เข้าโฟลเดอร์ `cd frontend && npm run dev` และตรวจสอบว่าหน้าแรกของ Next.js เปิดขึ้นที่ `http://localhost:3000` สำเร็จ

---

## การตรวจสอบทั้งหมด (Validation)

```bash
# Backend validation
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload

# Frontend validation
cd frontend
npm run dev
```

---

## เกณฑ์การยอมรับ (Acceptance Criteria)

- [ ] ทุกงานถูกดำเนินการจนครบถ้วน (All tasks completed)
- [ ] Backend FastAPI สามารถเปิดรันได้โดยไม่มีข้อผิดพลาด (Starts without errors)
- [ ] ตารางในฐานข้อมูล (`presets`, `simulation_jobs`) ถูกสร้างขึ้นใน MS SQL Server
- [ ] Frontend Next.js สามารถเปิดรันได้โดยไม่มีข้อผิดพลาด
