# CacheInsight-Reforged: เรื่องราวของผู้ใช้งาน (User Stories)

เอกสารนี้รวบรวม User Stories ที่จัดโครงสร้างมาจาก PRD โดยแบ่งตามระยะเวลาการดำเนินงาน (Implementation Phase)

---

## Phase 1: โครงสร้างพื้นฐาน (Foundation & Infrastructure)

### [STORY-1] สร้างโครงสร้างสคีมาฐานข้อมูล MS SQL (Setup MS SQL Database Schema)
**ประเภท**: Technical
**Jira Type**: Task
**ลำดับความสำคัญ**: High
**ความซับซ้อน**: Medium
**Phase**: Phase 1
**Labels**: `backend`, `database`

### คำอธิบาย (Description)
ในฐานะนักพัฒนาหลังบ้าน (Backend developer) ฉันต้องการสร้างสคีมาฐานข้อมูลบน MS SQL (ตาราง Presets, Simulation_Jobs) เพื่อให้แอปพลิเคชันมีโครงสร้างพื้นฐานในการจัดเก็บข้อมูลประวัติและการตั้งค่าต่างๆ ของ Cache

### เกณฑ์การยอมรับ (Acceptance Criteria)
- [ ] สามารถเชื่อมต่อฐานข้อมูล MS SQL Server ผ่าน SQLAlchemy ได้สำเร็จ
- [ ] มีสคริปต์ Migration หรือโมเดล SQLAlchemy สำหรับตาราง `presets` และ `simulation_jobs`
- [ ] ตารางถูกสร้างบน MS SQL Server ในเครื่อง Local ได้อย่างสมบูรณ์

### ข้อมูลทางเทคนิค (Technical Notes)
- ใช้ไดรเวอร์ `pyodbc` หรือไดรเวอร์สำหรับ SQL Server ที่เทียบเท่า
- โครงสร้างสคีมาต้องตรงกับส่วนที่ 4 ในข้อกำหนดดั้งเดิม (เช่น `simulation_jobs.config` ต้องเป็น JSON)

### ความเกี่ยวข้อง (Dependencies)
- ถูกบล็อกโดย (Blocked by): ไม่มี
- บล็อกงาน (Blocks): [STORY-3], [STORY-4], [STORY-11]

---

### [STORY-2] สร้างโครงสร้างเริ่มต้นสำหรับ Next.js & Tailwind UI (Initialize Next.js & Tailwind UI Shell)
**ประเภท**: Technical
**Jira Type**: Task
**ลำดับความสำคัญ**: High
**ความซับซ้อน**: Small
**Phase**: Phase 1
**Labels**: `frontend`, `ui`

### คำอธิบาย (Description)
ในฐานะนักพัฒนาหน้าบ้าน (Frontend developer) ฉันต้องการสร้างโครงสร้างโปรเจกต์ Next.js และตั้งค่า Tailwind CSS เพื่อใช้เป็นรากฐานในการสร้างคอมโพเนนต์และหน้า UI ต่างๆ

### เกณฑ์การยอมรับ (Acceptance Criteria)
- [ ] โปรเจกต์ Next.js ถูกสร้างขึ้นสำเร็จในไดเรกทอรี Frontend
- [ ] Tailwind CSS ได้รับการกำหนดค่าและทำงานได้ปกติ
- [ ] มีโครงสร้างหน้าเว็บพื้นฐาน (ประกอบด้วย Header, Main Content area, Footer)

### ข้อมูลทางเทคนิค (Technical Notes)
- ตั้งค่าระบบ Routing พื้นฐานหากจำเป็น
- เตรียมโฟลเดอร์ `public/` ให้พร้อมสำหรับการดึงไฟล์ Markdown มาแสดงผลในภายหลัง

### ความเกี่ยวข้อง (Dependencies)
- ถูกบล็อกโดย (Blocked by): ไม่มี
- บล็อกงาน (Blocks): [STORY-6], [STORY-7], [STORY-8], [STORY-9]

---

## Phase 2: ระบบจำลองผลหลัก (Core Simulation Engine)

### [STORY-3] พอร์ตตรรกะจำลองการทำงานของ Cache เป็น Python (Port Cache Simulation Logic to Python)
**ประเภท**: Feature
**Jira Type**: Story
**ลำดับความสำคัญ**: High
**ความซับซ้อน**: Large
**Phase**: Phase 2
**Labels**: `backend`, `algorithm`

### คำอธิบาย (Description)
ในฐานะนักศึกษา ฉันต้องการให้ระบบจำลองการทำงานบน Python สามารถคำนวณค่า Hit และ Miss ของ Cache ได้เหมือนกับต้นฉบับภาษา C++ อย่างถูกต้อง เพื่อให้ผลลัพธ์ทางการศึกษามีความแม่นยำ

### เกณฑ์การยอมรับ (Acceptance Criteria)
- [ ] สร้างคลาสหรือฟังก์ชันใน Python สำหรับจำลอง Direct Mapped cache สำเร็จ
- [ ] สร้างคลาสหรือฟังก์ชันใน Python สำหรับจำลอง Set-Associative (LRU) cache สำเร็จ
- [ ] สร้างคลาสหรือฟังก์ชันใน Python สำหรับจำลอง Fully Associative (LRU) cache สำเร็จ
- [ ] มี Unit tests เพื่อเปรียบเทียบผลลัพธ์ของ Python กับไฟล์ `cachesim.cpp` และทดสอบผ่าน 100%

### ข้อมูลทางเทคนิค (Technical Notes)
- การแปลงเลขฐานสิบหกเป็นฐานสอง และการแยก Tag/Index/Offset จะต้องตรงกับการคำนวณ Bitwise ในภาษา C++ ทุกประการ
- ลอจิกการทำงานของ LRU ต้องใช้ตัวนับเวลา (Global time) จำลองให้ตรงกับลอจิกของ C++

### ความเกี่ยวข้อง (Dependencies)
- ถูกบล็อกโดย (Blocked by): ไม่มี
- บล็อกงาน (Blocks): [STORY-4]

---

### [STORY-4] สร้าง Background Worker และ API สำหรับอัปโหลดไฟล์ (Implement Background Worker & File Upload API)
**ประเภท**: Feature
**Jira Type**: Story
**ลำดับความสำคัญ**: High
**ความซับซ้อน**: Large
**Phase**: Phase 2
**Labels**: `backend`, `api`, `async`

### คำอธิบาย (Description)
ในฐานะนักศึกษา ฉันต้องการอัปโหลดไฟล์จำลองข้อมูลขนาดใหญ่ที่จะถูกนำไปประมวลผลอยู่เบื้องหลัง (Background) เพื่อที่เบราว์เซอร์ของฉันจะได้ไม่ค้างระหว่างที่กำลังรอผลลัพธ์

### เกณฑ์การยอมรับ (Acceptance Criteria)
- [ ] Endpoint `POST /api/simulate` สามารถรับไฟล์ `.csv` และ JSON Payload (การตั้งค่า) ได้
- [ ] API สร้างคิวงานใหม่ลงในตาราง `simulation_jobs` และตอบกลับด้วย `job_id` ในทันที
- [ ] `BackgroundTask` ของ FastAPI (ซึ่งใช้ `ProcessPoolExecutor`) เริ่มทำงานอ่านไฟล์และจำลองผล
- [ ] Background task อัปเดตความคืบหน้า (Progress) ลงฐานข้อมูลทุกๆ 10,000 บรรทัด เพื่อลดปัญหาคอขวดที่ DB
- [ ] ไฟล์ที่ถูกอัปโหลดจะถูกลบทิ้งเมื่อการจำลองเสร็จสมบูรณ์หรือล้มเหลว

### ข้อมูลทางเทคนิค (Technical Notes)
- จำกัดค่า `max_workers` ของ `ProcessPoolExecutor` ไว้ที่ 1 หรือ 2 ตัว เพื่อป้องกันปัญหา RAM/CPU เต็มพิกัดบนเครื่อง Local

### ความเกี่ยวข้อง (Dependencies)
- ถูกบล็อกโดย (Blocked by): [STORY-1], [STORY-3]
- บล็อกงาน (Blocks): [STORY-5], [STORY-6]

---

### [STORY-5] สร้าง API สำหรับดึงสถานะงาน (Implement Status Polling API)
**ประเภท**: Feature
**Jira Type**: Story
**ลำดับความสำคัญ**: High
**ความซับซ้อน**: Small
**Phase**: Phase 2
**Labels**: `backend`, `api`

### คำอธิบาย (Description)
ในฐานะนักพัฒนาหน้าบ้าน (Frontend developer) ฉันต้องการ API สำหรับดึงสถานะงานที่กำลังประมวลผล เพื่อนำไปแสดงผลบนแถบ Progress bar ให้ผู้ใช้เห็น

### เกณฑ์การยอมรับ (Acceptance Criteria)
- [ ] Endpoint `GET /api/simulate/{job_id}` สามารถคืนค่าสถานะปัจจุบันของคิวงานได้ (Pending, Processing, Completed, Failed)
- [ ] API คืนค่าเปอร์เซ็นต์ความคืบหน้า (คำนวณจากบรรทัดที่ทำเสร็จเทียบกับบรรทัดทั้งหมด)
- [ ] ถ้างายเสร็จสิ้น (Completed) API จะต้องส่งผลลัพธ์การจำลอง (Hit Rate, Miss Rate, Total Accesses) กลับมาด้วย

### ข้อมูลทางเทคนิค (Technical Notes)
- ค้นหาข้อมูลจากตาราง `simulation_jobs` ด้วย UUID

### ความเกี่ยวข้อง (Dependencies)
- ถูกบล็อกโดย (Blocked by): [STORY-4]
- บล็อกงาน (Blocks): [STORY-7]

---

### [STORY-11] API สำหรับการจัดการ Preset (Preset Management API)
**ประเภท**: Feature
**Jira Type**: Story
**ลำดับความสำคัญ**: Medium
**ความซับซ้อน**: Small
**Phase**: Phase 2
**Labels**: `backend`, `api`

### คำอธิบาย (Description)
ในฐานะอาจารย์ผู้สอน ฉันต้องการ API เพื่อจัดเก็บและดึงข้อมูลการตั้งค่า Cache เพื่อให้ระบบหน้าบ้านนำไปสร้างระบบ Preset ดึงค่ากลับมาใช้ได้อย่างรวดเร็ว

### เกณฑ์การยอมรับ (Acceptance Criteria)
- [ ] Endpoint `POST /api/presets` บันทึกค่าล่วงหน้าลงฐานข้อมูลสำเร็จ
- [ ] Endpoint `GET /api/presets` ดึงรายการ Preset ทั้งหมดออกมาได้สำเร็จ
- [ ] การป้องกันและรับมือข้อผิดพลาด (Constraints) ของฐานข้อมูล (เช่น ชื่อห้ามซ้ำ) จัดการได้ดีและคืนค่าเป็น Error 400

### ข้อมูลทางเทคนิค (Technical Notes)
- ต้องมีการตรวจสอบเงื่อนไข Cache Size และ Block Size (ต้องเป็น Power of 2) ในฝั่งของ Endpoint นี้ด้วย

### ความเกี่ยวข้อง (Dependencies)
- ถูกบล็อกโดย (Blocked by): [STORY-1]
- บล็อกงาน (Blocks): [STORY-12]

---

## Phase 3: การเชื่อมต่อระบบหน้าบ้าน (Frontend Integration)

### [STORY-6] หน้า UI สำหรับแบบฟอร์มและการตรวจสอบข้อมูล (Form Validation and Submission UI)
**ประเภท**: Feature
**Jira Type**: Story
**ลำดับความสำคัญ**: High
**ความซับซ้อน**: Medium
**Phase**: Phase 3
**Labels**: `frontend`, `ui`

### คำอธิบาย (Description)
ในฐานะผู้ใช้ ฉันต้องการให้ระบบหน้าบ้าน (UI) ตรวจสอบความถูกต้องของข้อมูล (เช่น Cache Size ต้องเป็น Power of 2) ก่อนกดยืนยัน เพื่อไม่ให้ฉันรันงานผิดพลาดและส่งผลให้ผลลัพธ์คลาดเคลื่อน

### เกณฑ์การยอมรับ (Acceptance Criteria)
- [ ] มีแบบฟอร์มที่ประกอบด้วย Cache Size, Block Size, Mapping Type และ N-way (ถ้าจำเป็น)
- [ ] ระบบตรวจสอบข้อมูลบนหน้าเว็บจะไม่ยอมให้กดส่งแบบฟอร์ม หากค่าต่างๆ ไม่ใช่ Power of 2
- [ ] แบบฟอร์มมีปุ่มสำหรับอัปโหลดไฟล์ `.csv`
- [ ] แบบฟอร์มเมื่อกดยืนยันแล้วสามารถยิง `POST /api/simulate` และได้รับ `job_id` มาอย่างถูกต้อง

### ข้อมูลทางเทคนิค (Technical Notes)
- ใช้ React Hook Form หรือไลบรารีที่คล้ายกันเพื่อทำ Validation
- ต้องมีข้อความ Error แจ้งเตือนอย่างชัดเจนใต้ช่องกรอกข้อมูลที่ผิดพลาด

### ความเกี่ยวข้อง (Dependencies)
- ถูกบล็อกโดย (Blocked by): [STORY-2], [STORY-4]
- บล็อกงาน (Blocks): [STORY-7]

---

### [STORY-7] แถบความคืบหน้า (Progress Bar UI - Polling)
**ประเภท**: Feature
**Jira Type**: Story
**ลำดับความสำคัญ**: High
**ความซับซ้อน**: Medium
**Phase**: Phase 3
**Labels**: `frontend`, `ui`

### คำอธิบาย (Description)
ในฐานะนักศึกษา ฉันต้องการเห็น Progress bar ระหว่างที่ระบบกำลังประมวลผล เพื่อให้ฉันรู้ว่าคอมไม่ได้ค้างหรือพังไปแล้ว

### เกณฑ์การยอมรับ (Acceptance Criteria)
- [ ] เมื่อได้รับ `job_id` ระบบหน้าเว็บจะเริ่มการ Polling ไปยัง `GET /api/simulate/{job_id}` ทุกๆ 1-2 วินาที
- [ ] แถบความคืบหน้าจะขยับตามเปอร์เซ็นต์ที่ API ตอบกลับมา
- [ ] การ Polling จะหยุดอัตโนมัติเมื่อสถานะเปลี่ยนเป็น Completed หรือ Failed

### ข้อมูลทางเทคนิค (Technical Notes)
- สามารถใช้ `useInterval` หรือจัดการ interval loop ธรรมดาด้วย `useEffect` บน React

### ความเกี่ยวข้อง (Dependencies)
- ถูกบล็อกโดย (Blocked by): [STORY-2], [STORY-5], [STORY-6]
- บล็อกงาน (Blocks): [STORY-8]

---

### [STORY-8] หน้าแสดงผลลัพธ์และตารางประวัติ (Results Visualization and History Table)
**ประเภท**: Feature
**Jira Type**: Story
**ลำดับความสำคัญ**: High
**ความซับซ้อน**: Medium
**Phase**: Phase 3
**Labels**: `frontend`, `ui`

### คำอธิบาย (Description)
ในฐานะผู้ใช้ ฉันต้องการดูผลการจำลองและประวัติการทดสอบในอดีตทั้งหมด เพื่อเปรียบเทียบดูว่าการตั้งค่า Cache ที่ต่างกันให้ผลลัพธ์ที่แตกต่างกันบนไฟล์เดียวกันอย่างไร

### เกณฑ์การยอมรับ (Acceptance Criteria)
- [ ] เมื่อจำลองผลเสร็จสิ้น หน้าเว็บจะแสดงเปอร์เซ็นต์ Hit Rate, Miss Rate และ Total Accesses เด่นชัด
- [ ] หน้าเว็บสามารถดึงข้อมูลจาก `/api/history` (หรือลิสต์จากตาราง `simulation_jobs`) มาแสดงบนตารางประวัติ
- [ ] ตารางแสดงงานที่ทำเสร็จในอดีต ข้อมูลการตั้งค่า และเปอร์เซ็นต์ Hit Rate

### ข้อมูลทางเทคนิค (Technical Notes)
- อาจจะต้องเพิ่ม Endpoint `GET /api/history` แบบง่ายๆ ถ้าระบบเดิมใน Story 5 ยังไม่ได้ครอบคลุมไว้

### ความเกี่ยวข้อง (Dependencies)
- ถูกบล็อกโดย (Blocked by): [STORY-2], [STORY-7]
- บล็อกงาน (Blocks): ไม่มี

---

### [STORY-12] เมนูเลือก Preset (Preset Selection UI)
**ประเภท**: Feature
**Jira Type**: Story
**ลำดับความสำคัญ**: Medium
**ความซับซ้อน**: Small
**Phase**: Phase 3
**Labels**: `frontend`, `ui`

### คำอธิบาย (Description)
ในฐานะอาจารย์ผู้สอน ฉันต้องการหน้า UI สำหรับกดเลือก, สร้าง, หรือลบ ค่า Preset ที่ถูกบันทึกไว้ เพื่อจะได้ดึงข้อมูล Cache ที่ต้องใช้สาธิตมาใส่ในช่องกรอกได้อย่างรวดเร็ว

### เกณฑ์การยอมรับ (Acceptance Criteria)
- [ ] มี Dropdown menu สำหรับกดเลือก Preset ที่มีอยู่ ข้อมูลในช่องจะถูกเติมอัตโนมัติเมื่อกดเลือก
- [ ] มีปุ่ม "Save current configuration as Preset" เพื่อบันทึกค่าในช่องปัจจุบันเป็น Preset ใหม่
- [ ] Preset ที่ดึงมาสามารถคงอยู่แม้จะโหลดหน้าเว็บใหม่ (โหลดมาจาก Backend)

### ข้อมูลทางเทคนิค (Technical Notes)
- ดึงข้อมูลและเชื่อมโยงกับ Endpoint จาก [STORY-11]

### ความเกี่ยวข้อง (Dependencies)
- ถูกบล็อกโดย (Blocked by): [STORY-2], [STORY-11]
- บล็อกงาน (Blocks): ไม่มี

---

## Phase 4: เนื้อหาเพื่อการศึกษาและความสมบูรณ์ (Educational Content & Polish)

### [STORY-9] หน้าต่างให้ความรู้แบบ Modal Popups (Educational Markdown Modal Popups)
**ประเภท**: Feature
**Jira Type**: Story
**ลำดับความสำคัญ**: Medium
**ความซับซ้อน**: Medium
**Phase**: Phase 4
**Labels**: `frontend`, `ui`, `education`

### คำอธิบาย (Description)
ในฐานะนักศึกษา ฉันต้องการปุ่ม "ข้อมูล (Info)" เมื่อกดแล้วจะแสดงหน้าต่าง Popup ทฤษฎีเรื่องเทคนิค Cache Mapping เพื่อที่ฉันจะได้ทำความเข้าใจแนวคิดที่อยู่เบื้องหลังการจำลอง

### เกณฑ์การยอมรับ (Acceptance Criteria)
- [ ] ปุ่ม "Info" ถูกวางไว้ใกล้กับจุดให้เลือกรูปแบบ Cache Mapping 
- [ ] เมื่อกดปุ่ม หน้าต่าง Modal แบบ Popup จะเด้งขึ้นมา
- [ ] Modal นี้ใช้งาน `react-markdown` ในการนำเข้าเนื้อหาจากไฟล์ `.md` ภายในโฟลเดอร์ `public/` มาแสดงผล
- [ ] หากมีรูปภาพในไฟล์ Markdown รูปต้องแสดงผลภายใน Modal อย่างสมบูรณ์และถูกต้อง

### ข้อมูลทางเทคนิค (Technical Notes)
- อาจต้องใช้แพ็กเกจ `remark-gfm` กรณีที่ Markdown มีตารางหรือการจัดรูปแบบซับซ้อน

### ความเกี่ยวข้อง (Dependencies)
- ถูกบล็อกโดย (Blocked by): [STORY-2]
- บล็อกงาน (Blocks): [STORY-10]

---

### [STORY-10] จัดเตรียมเนื้อหา Markdown (Create Educational Markdown Content)
**ประเภท**: Technical
**Jira Type**: Task
**ลำดับความสำคัญ**: Medium
**ความซับซ้อน**: Small
**Phase**: Phase 4
**Labels**: `content`

### คำอธิบาย (Description)
ในฐานะผู้สอน ฉันต้องการจัดเตรียมไฟล์ Markdown และรูปภาพอธิบายทฤษฎี Cache ไว้ในโฟลเดอร์ `/public` เพื่อให้หน้าต่าง Popup มีเนื้อหาที่สมบูรณ์และถูกต้องสำหรับนำไปใช้แสดงผล

### เกณฑ์การยอมรับ (Acceptance Criteria)
- [ ] สร้างไฟล์ Markdown อธิบายว่า "Cache Memory คืออะไร"
- [ ] สร้างไฟล์ Markdown อธิบายแต่ละเทคนิค: Direct Mapped, Fully Associative, Set-Associative
- [ ] นำรูปภาพหรือไดอะแกรมมาใส่ใน `public/images/` และระบุตำแหน่ง Path ในไฟล์ Markdown ให้ถูกต้อง

### ข้อมูลทางเทคนิค (Technical Notes)
- ใช้ภาษาในการอธิบายให้ชัดเจนและเข้าใจง่ายสำหรับนักศึกษา

### ความเกี่ยวข้อง (Dependencies)
- ถูกบล็อกโดย (Blocked by): [STORY-9]
- บล็อกงาน (Blocks): ไม่มี

---

### [STORY-13] ทดสอบประสิทธิภาพด้วยข้อมูล 1,000,000 บรรทัด (Load Testing with 1,000,000 Addresses)
**ประเภท**: Spike
**Jira Type**: Task
**ลำดับความสำคัญ**: High
**ความซับซ้อน**: Medium
**Phase**: Phase 4
**Labels**: `testing`, `performance`

### คำอธิบาย (Description)
ในฐานะนักพัฒนา ฉันต้องการทดสอบการทำงานของระบบตั้งแต่ต้นจนจบ (End-to-End) โดยใช้ไฟล์ CSV ที่มีข้อมูลระดับ 1,000,000 บรรทัด เพื่อให้แน่ใจว่าระบบบรรลุข้อกำหนด Non-functional Requirement ที่ตั้งไว้ (ต้องไม่มีอาการหน้า UI ค้าง หรือ HTTP Timeouts)

### เกณฑ์การยอมรับ (Acceptance Criteria)
- [ ] อัปโหลดไฟล์ CSV 1M addresses สำเร็จ
- [ ] แถบความคืบหน้า (Progress bar) ทำงานไหลลื่น ไม่มี HTTP 504 Timeouts เด้งขึ้นมา
- [ ] ฝั่ง Backend มีการใช้งาน Memory ภายในขอบเขตที่เหมาะสม (< 100MB ต่อ 1 Worker)
- [ ] ผลลัพธ์ Hit/Miss สุดท้ายที่ได้ถูกตรวจสอบแล้วว่าตรงกับการทำงานของภาษา C++ 100%

### ข้อมูลทางเทคนิค (Technical Notes)
- ตรวจสอบ Task Manager / Resource Monitor รันคู่กันไปในขณะทำการทดสอบ
- ถ้าการทำ Database writes ยังกินเวลามากเกินไป ให้ปรับเพิ่ม Batch ของการอัปเดต (เช่น จากอัปเดตทุก 10k บรรทัด เปลี่ยนเป็นทุก 50k บรรทัด)

### ความเกี่ยวข้อง (Dependencies)
- ถูกบล็อกโดย (Blocked by): [STORY-3], [STORY-4], [STORY-7], [STORY-8]
- บล็อกงาน (Blocks): ไม่มี
