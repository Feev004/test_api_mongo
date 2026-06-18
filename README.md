# test_api_mongo

ตัวอย่างโปรเจกต์ Frontend + Python Backend ที่เชื่อม MongoDB

## โครงสร้าง

- `app.py` : Backend Python Flask เชื่อม MongoDB ที่ `mongodb://localhost:27017/`
- `public/index.html` : Frontend หน้า HTML แสดงรายการและฟอร์มเพิ่มข้อมูล
- `public/app.js` : JavaScript ฝั่ง client เรียก API ของ backend
- `requirements.txt` : รายการ dependency สำหรับ Python

## การติดตั้ง

1. ติดตั้ง dependencies

```powershell
pip install -r requirements.txt
```

2. รัน MongoDB ในเครื่อง

ให้แน่ใจว่า MongoDB รันที่ `mongodb://localhost:27017/`

3. รันเซิร์ฟเวอร์

```powershell
python app.py
```

4. เปิดหน้าเว็บ

เข้าใช้งานที่ `http://localhost:3000`

## การทำงานโดยรวม

1. Frontend (`public/index.html` + `public/app.js`) จะแสดงฟอร์มกรอกชื่อและรายการของ `items`
2. เมื่อกดปุ่มเพิ่มรายการ, frontend จะส่ง request `POST /api/items` พร้อม JSON body `{ "name": "..." }`
3. Backend (`app.py`) รับ request และเชื่อมต่อ MongoDB เพื่อ
   - เพิ่มเอกสารลงใน collection `items`
   - ดึงรายการทั้งหมดจาก collection
   - ลบรายการตาม `_id`
4. MongoDB เก็บข้อมูลในฐานข้อมูล `test_api_db` และ collection `items`
5. Backend จะส่งผลลัพธ์กลับเป็น JSON ให้ frontend แสดงรายการใหม่

## รายละเอียดการทำงานของแต่ละส่วน

### Backend (`app.py`)

- สร้าง Flask app และเปิด CORS เพื่อให้ frontend เรียก API ได้
- เชื่อมต่อ MongoDB ด้วย `MongoClient` ไปยัง `mongodb://localhost:27017/`
- `GET /api/items` : อ่านข้อมูลจาก collection `items` แล้วแปลง `_id` เป็นสตริงก่อนส่งกลับ
- `POST /api/items` : อ่าน JSON request, ตรวจสอบ `name`, แล้วเพิ่มข้อมูลใหม่ลง MongoDB
- `DELETE /api/items/<item_id>` : แปลง `item_id` เป็น `ObjectId` แล้วลบเอกสารจาก MongoDB
- route `/` และ `/<path:path>` ให้บริการไฟล์ frontend จากโฟลเดอร์ `public`

### Frontend (`public/app.js`)

- `loadItems()` : ดึงรายการจาก `GET /api/items` และแสดงใน `<ul>`
- `addItem(name)` : ส่ง `POST /api/items` เพื่อเพิ่มรายการใหม่
- `deleteItem(id)` : ส่ง `DELETE /api/items/:id` เพื่อลบรายการ
- เมื่อผู้ใช้ส่งฟอร์ม จะเรียก `addItem()` และโหลดรายการใหม่อีกครั้ง

### MongoDB

- ใช้ connection string `mongodb://localhost:27017/`
- database ที่ใช้คือ `test_api_db`
- collection ที่ใช้คือ `items`

## API ที่ใช้งาน

- `GET /api/items` : ดึงรายการทั้งหมด
- `POST /api/items` : เพิ่มรายการใหม่ ด้วย payload `{ "name": "..." }`
- `DELETE /api/items/:id` : ลบรายการตาม `_id`
