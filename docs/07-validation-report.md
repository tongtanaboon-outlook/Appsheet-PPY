# 07 — รายงานตรวจความครบถ้วน (Validation Report)

รายงานนี้ผลิตจากการรันคำสั่งจริง ณ เวลาที่สร้าง ไม่ได้เขียนด้วยมือ

## ผลการตรวจ

```
[PASS] schema/tables count == 90 - got 90
[PASS] schema/columns count == 2304 - got 2304
[PASS] schema/views count == 115 - got 115
[PASS] schema/actions count == 214 - got 214
[PASS] schema/slices count == 8 - got 8
[PASS] schema/format_rules count == 11 - got 11
[PASS] every table has columns
[PASS] relations point at known tables
[PASS] type qualifier payloads are JSON - 0 bad
[PASS] actions point at a known table
[PASS] every action declares its target table
[PASS] views carry a known view type
[PASS] expressions flagged for manual review are listed - 2: ข้อมูลการวางบิล :: สถานะการอนุมัติ, ScanDocs :: สรุปยอด
[PASS] every column has a type
[PASS] data dictionary covers every table - 0 missing: 
[PASS] data dictionary covers every column - 0 missing: 
[PASS] erd covers every relation - 0 missing: 
[PASS] formula catalog covers every computed column - 0 missing: 
[PASS] bot inventory covers every bot table - 0 missing: 
[PASS] data manifest lists every business table - manifest=29
[PASS] data csv files are declared in the manifest
[PASS] one documentation file per business table - 29 files
[PASS] one documentation file per bot table - 61 files
[PASS] one documentation file per format rule - 11 files
[PASS] generated documentation is in sync with the schema - 0 file(s) out of sync

All checks passed.

```

**ผ่านทั้งหมด** — repo พร้อมนำขึ้น GitHub

## เกณฑ์ที่ใช้ตรวจ (และทำไมต้องมี)

| เกณฑ์ | กันปัญหาอะไร |
|---|---|
| จำนวนตาราง/คอลัมน์/views/actions/slices/rules ตรงกับที่ PDF ประกาศ | กันการดึงข้อมูลตกหล่นตอนแปลง PDF |
| ทุกตารางมีคอลัมน์, ทุกคอลัมน์มีชนิดข้อมูล, ทุกคอลัมน์ผูกกับตารางที่มีจริง | กันคอลัมน์หลุด/ชนิดข้อมูลว่าง |
| ทุกความสัมพันธ์ชี้ไปยังตารางที่มีจริง | กันชื่อตารางเพี้ยนจากการตัดบรรทัดใน PDF |
| Type Qualifier ทุกตัว parse เป็น JSON ได้ | กันการตัดค่ากลางโครงสร้าง |
| action ทุกตัวชี้ตารางเป้าหมายถูกต้อง / มีชนิดคำสั่ง / view มีชนิดที่รู้จัก | กัน field ของ action/view เลื่อนตำแหน่ง (จุดที่ PDF วาง label กลาง value) |
| พจนานุกรม/ERD/สูตร/บอท ครอบคลุมทุกตาราง ทุกคอลัมน์ ทุกความสัมพันธ์ | กันเอกสารตกหล่น |
| เอกสารที่ generate อัตโนมัติตรงกับ schema | กันเอกสารเก่าค้างเมื่อ schema เปลี่ยน |
| data/manifest.json ครบ 29 ตารางธุรกิจ + header ของ CSV ตรง schema | กันข้อมูลแถวผิดคอลัมน์เมื่อนำเข้า |

## ประสิทธิภาพของชั้น deterministic

การแยก PDF → schema ทำด้วย `scripts/extract_appsheet.py` ซึ่ง **ไม่ใช้ AI เลย**
ใช้หลัก 3 อย่าง: ลำดับ field ที่ AppSheet กำหนดไว้ตายตัว · รูปแบบค่า (JSON / formula / token)
· การตรวจ balance (วงเล็บปีกกาและวงเล็บเหลี่ยม)

ผลคือ **นับได้แม่นยำ 100 ตามตัวเลขที่ PDF ประกาศไว้เอง** ทำให้ชั้นเอกสาร
ที่สร้างต่อยอด (พจนานุกรม, ERD, แคตตาล็อกสูตร) **ไม่มีทางตกหล่น**

## รายการที่ยังค้าง (ไม่บล็อกการใช้งาน)

| รายการ | สถานะ | ต้องทำอะไร |
|---|---|---|
| ข้อมูลระดับแถว (rows) | ยังไม่มี | export จาก AppSheet / Google Sheets ตาม `data/README.md` |
| นิยามบอท (event/trigger/schedule) | ไม่มีใน PDF | AppSheet -> Automations -> Bots -> export -> `app/automations.json` |
| คอลัมน์ที่สูตรอาจไม่ครบ (PDF วาดทับตารางคุณสมบัติ) | 2 คอลัมน์ | ตรวจในแอป: `ข้อมูลการวางบิล.สถานะการอนุมัติ`, `ScanDocs.สรุปยอด` (ติดธงไว้ที่คอลัมน์ `needs_review`) |
| คำอธิบายเชิงธุรกิจรายคอลัมน์ | สร้างแบบอัตโนมัติจากชื่อ+ชนิด+สูตร | ถ้าต้องการระดับมืออาชีพ ค่อยเขียนทับ (ไฟล์ยัง generate ใหม่ได้ทันที) |

## วิธีตรวจซ้ำ

```bash
python3 scripts/validate_repo.py --repo .
```

CI (`.github/workflows/ci.yml`) รันคำสั่งนี้ทุก push และ pull request
