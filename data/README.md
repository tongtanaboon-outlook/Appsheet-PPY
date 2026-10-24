# data/ — ข้อมูลแถวจริงของตารางธุรกิจ (29 ตาราง)

โฟลเดอร์นี้เก็บ **ข้อมูลระดับแถว** ของตารางธุรกิจทั้ง 29 ตาราง (ตารางที่ `Data Source = google`)
ส่วนตารางบอท (60 ตาราง) **ไม่ดึงข้อมูลมา** เพราะเป็นตารางชั่วคราวของ automation —
ดูรายละเอียดที่ `docs/04-bots-and-automations.md`

## สัญญาข้อมูล (contract)

* ชื่อไฟล์ = slug ของชื่อตารางใน AppSheet (ตาราง `SCGนครหลวงJWDภูมิภาค` → `SCGนครหลวงJWDภูมิภาค.csv`)
* คอลัมน์เรียงตาม `app/columns.csv` ของตารางนั้น ๆ
* ทุกไฟล์ต้องประกาศไว้ใน `data/manifest.json` — CI จะตรวจให้

## วิธีดึงข้อมูล 3 ทาง (เลือกทางใดทางหนึ่ง)

### 1) Google Sheets (แนะนำ — เร็วและครบที่สุด)

ตารางธุรกิจทั้งหมดอยู่ในสเปรดชีตเดียวกัน (แต่ละตาราง = 1 worksheet)
หา Spreadsheet ID จาก AppSheet: **Data → Sources** → คัดลอก URL ของ Google Sheet

```bash
pip install google-api-python-client google-auth
# สร้าง service account (JSON) แล้วแชร์สเปรดชีตให้ service account อ่านได้
cp service-account.json config.local.json     # อยู่ใน .gitignore แล้ว
python scripts/pull_data.py --mode sheets --spreadsheet-id <SPREADSHEET_ID>
```

### 2) AppSheet REST API (ไม่ต้องใช้สิทธิ์ Google)

เอา API key จาก URL ของแอป: `https://appsheet.app/<APP_ID>?appServiceId=<API_KEY>`

```bash
python scripts/pull_data.py --mode appsheet --app-id <APP_ID> --api-key <API_KEY>
```

> หมายเหตุ: AppSheet API คืนข้อมูลทีละแถวและช้ากว่า ข้อมูลอาจไม่ครบทุกแถว
> ถ้าต้องการข้อมูลเต็ม ให้ใช้ทาง 1 หรือ 3

### 3) ส่งออกจากตัว AppSheet (ไม่ต้องมี credential เลย)

ในแอป: **Data → (เมนูตาราง) → Export → CSV** ทำทีละตาราง
แล้วบันทึกไฟล์ลง `data/` ตามชื่อใน `data/manifest.json`

## ตรวจสอบความครบถ้วน

```bash
python scripts/validate_repo.py
```

CI จะตรวจว่าไฟล์ CSV ที่มีอยู่ตรงกับที่ประกาศใน manifest และว่า schema ครบทั้ง 90 ตาราง / 2304 คอลัมน์
