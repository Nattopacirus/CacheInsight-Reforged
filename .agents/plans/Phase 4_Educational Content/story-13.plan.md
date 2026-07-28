# แผนการพัฒนา: STORY-13 - ทดสอบประสิทธิภาพด้วยข้อมูล 1,000,000 บรรทัด (Load Testing)

## สรุป (Summary)
แผนนี้คือขั้นตอนสุดท้ายของโปรเจกต์ (Phase 4) ซึ่งมีเป้าหมายเป็น Spike/Task สำหรับการทดสอบ (Testing) ระบบตั้งแต่ต้นจนจบ (End-to-End) ว่าโครงสร้างสถาปัตยกรรมใหม่แบบ Background Worker (FastAPI + Async Polling) ที่เราวางไว้ สามารถรับมือกับการประมวลผลไฟล์ Address ขนาด 1 ล้านบรรทัดได้จริง โดยหน้าเว็บต้องไม่ค้าง (No UI Freezes) และ API ต้องไม่เกิดการหมดเวลา (No HTTP 504 Timeouts) รวมถึงการกิน RAM ของ Backend ต้องสมเหตุสมผล

## เรื่องราวของผู้ใช้งาน (User Story)
ในฐานะนักพัฒนา
ฉันต้องการทดสอบการทำงานของระบบตั้งแต่ต้นจนจบ (End-to-End) โดยใช้ไฟล์ CSV ที่มีข้อมูลระดับ 1,000,000 บรรทัด
เพื่อให้แน่ใจว่าระบบบรรลุข้อกำหนด Non-functional Requirement ที่ตั้งไว้ (ต้องไม่มีอาการหน้า UI ค้าง หรือ HTTP Timeouts)

## ข้อมูลเบื้องต้น (Metadata)
| Field | Value |
|-------|-------|
| ประเภท (Type) | SPIKE / PERFORMANCE |
| ความซับซ้อน (Complexity) | MEDIUM |
| ระบบที่เกี่ยวข้อง (Systems Affected) | full-stack (Load Testing, Memory Profiling) |
| Jira Issue | STORY-13 |
| Source Control | พัฒนาบน `main` branch ได้เลย ไม่ต้องสร้าง branch ใหม่ |

---

## คุณสมบัติและรูปแบบการทดสอบ (Testing Procedures)

### 1. การเตรียมข้อมูล (Data Preparation)
- เนื่องจากไฟล์ที่มี Address 1 ล้านบรรทัดอาจจะใหญ่เกินกว่าจะอัปโหลดไว้ใน Git เราจะต้องสร้าง Script สั้นๆ ด้วย Python (เช่น `generate_test_data.py`) เพื่อสร้างไฟล์ `1M_addresses.csv` ที่เต็มไปด้วย Hex Address แบบสุ่ม (Random) หรือแบบลำดับ (Sequential) จำนวน 1,000,000 บรรทัด สำหรับใช้ทดสอบ

### 2. การวัดผลระหว่างจำลอง (Performance Profiling)
- **Frontend**: สังเกตการณ์หน้าเว็บ (DevTools) ว่าการยิง API แบบ Polling ดึงแถบ Progress Bar ทำให้บราวเซอร์กระตุกหรือไม่
- **Backend (Memory)**: รัน Backend ด้วย Uvicorn และเปิด Task Manager หรือ Resource Monitor เพื่อสังเกตการณ์ RAM ที่ Worker ใช้ (ตั้งเป้าไว้ที่ < 100MB ต่อ 1 Worker)
- **Backend (Speed)**: เช็กความเร็วในการ Insert ลง Database ถ้าช้าเกินไป (เช่น ใช้เวลามากกว่า 10-20 วินาที) เราจะต้องไปปรับแก้โค้ดในตัวแปร `BATCH_UPDATE_SIZE` ในไฟล์ `worker.py` (เช่น ปรับจากอัปเดตทุก 10,000 บรรทัด เป็น 50,000 บรรทัด)

### 3. การเปรียบเทียบผลลัพธ์ความถูกต้อง (Accuracy Validation)
- รันไฟล์ `1M_addresses.csv` เดียวกันนี้ด้วยโปรแกรมภาษา C++ ต้นฉบับ (`cachesim.cpp`)
- นำตัวเลข Hits และ Misses สุดท้ายมาเทียบกับบนหน้าเว็บ Result Dashboard หากตรงกันแบบ 100% (Bit-perfect match) ถือว่าระบบผ่านการทดสอบ

---

## ไฟล์ที่ต้องเปลี่ยนแปลง (Files to Change)

| ไฟล์ (File) | การกระทำ (Action) | วัตถุประสงค์ (Purpose) |
|------|--------|---------|
| `backend/tests/generate_data.py` | CREATE | สร้างสคริปต์สำหรับ Generate ไฟล์ CSV ขนาด 1M |
| `backend/app/worker.py` | UPDATE (Optional) | ปรับขนาด Batch Size หากการบันทึก Database ช้าเกินไป |

---

## งานที่ต้องทำ (Tasks)

### Task 1: สร้าง Script สำหรับจำลองไฟล์ CSV 1,000,000 บรรทัด
- เขียน Python script สุ่มเลขฐานสิบหก (Hex) จำนวน 1 ล้านชุด และเซฟลงไฟล์ `.csv` (มี Header เพื่อจำลองสถานการณ์จริง)
- นำไฟล์ที่ได้ไปรันกับโปรแกรม C++ เดิมเพื่อจดบันทึกตัวเลข Hit/Miss เอาไว้เป็น Ground Truth

### Task 2: รัน Load Test และสังเกตการณ์ระบบ
- รันโปรเจกต์ (เปิด Backend และ Frontend)
- อัปโหลดไฟล์ที่หน้าเว็บ กดเริ่มจำลอง
- สังเกต RAM ของ Process `python.exe` ใน Task Manager ขณะประมวลผล ว่าบวมเกิน 100MB หรือไม่
- เช็กแท็บ Network ในเบราว์เซอร์ ว่าคำสั่ง Polling ถูกยกเลิก (Timeout) ไปกลางคันหรือไม่

### Task 3: ประเมินและปรับจูน (Tuning)
- ถ้าระบบใช้เวลาจำลองนานเพราะคอขวดที่ I/O (Database) ให้เข้าไปปรับลอจิกใน `backend/app/worker.py` โดยเพิ่มตัวเลขจำนวนบรรทัดต่อการเซฟ 1 ครั้ง เพื่อลดภาระของ SQL Server
- เทียบตัวเลข Result บนจอ UI กับตัวเลขใน Task 1 ว่าตรงกันหรือไม่

---

## เกณฑ์การยอมรับ (Acceptance Criteria)
- [ ] สคริปต์สามารถสร้างไฟล์ CSV 1M addresses ได้สำเร็จ
- [ ] อัปโหลดไฟล์เข้าสู่ระบบ และสั่งจำลองข้อมูลได้โดยที่หน้าเว็บไม่ค้างหรือเกิด HTTP Timeouts
- [ ] แถบความคืบหน้า (Progress bar) ทำงานได้ไหลลื่น อัปเดต % จาก 0 ถึง 100 ได้สมบูรณ์
- [ ] Memory ของฝั่ง Backend ระหว่างประมวลผลถูกควบคุมอยู่ในขอบเขต (< 100MB)
- [ ] ผลลัพธ์ Hits/Misses สุดท้ายที่แสดงบน UI หรือใน Database ตรงกับการรัน C++ ต้นฉบับ 100%
