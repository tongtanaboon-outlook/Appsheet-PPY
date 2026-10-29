# AGENTS.md — คู่มือสำหรับ AI Agent ที่จะวิเคราะห์ข้อมูลชุดนี้

> อ่านไฟล์นี้ก่อนตอบคำถามใด ๆ เกี่ยวกับข้อมูลของแอปนี้
> ที่มา: AppSheet app **เผ่าปั ญญาทรานสปอร์ต** (หจก. เผ่าปัญญา ทรานสปอร์ต)
> ลูกค้าหลักในระบบ: SCG Express / SCGJWD (JWD) — งานขนส่งสินค้าและจัดจำหน่ายโลจิสติกส์
> แหล่งข้อมูล: เอกสาร "Application Documentation" ของ AppSheet (อยู่ใน `source/`)

---

## 1. ข้อเท็จจริงพื้นฐาน (อ้างอิงได้จาก `app/meta.json`)

| สิ่ง | จำนวน |
|---|---:|
| ตารางทั้งหมด | 90 |
| — ตารางธุรกิจ (มีข้อมูลจริง) | 29 |
| — ตารางของระบบอัตโนมัติ (บอท) | 60 |
| — ตารางระบบ (`_Per User Settings`) | 1 |
| คอลัมน์ทั้งหมด | 2304 |
| คอลัมน์ที่คำนวณอัตโนมัติ | 319 |
| ความสัมพันธ์ Ref (ตาราง→ตาราง) | 80 |
| Views | 115 |
| Actions | 214 |
| Slices | 8 |
| Format rules | 11 |

**ข้อมูลระดับแถว (rows) ยังไม่มีใน repo** — `data/` จะเติมเมื่อมีการ export
(ดู `data/README.md` มี 3 วิธี) ดังนั้นตอนนี้คุณวิเคราะห์ "โครงสร้าง" ได้ล้วน
แต่ยังคำนวณตัวเลขทางธุรกิจจริงไม่ได้

---

## 2. โครงสร้างโฟลเดอร์

```
docs/
├── 00-overview.md                      ภาพรวมแอป + โครงสร้างทั่วไป
├── 01-main-tables.md                   📋 สารบัญตารางจริง 29 ตาราง
├── 02-process-output-tables.md         🤖 วิเคราะห์บอท + สารบัญตารางบอท 61 ตาราง
├── 03-columns-and-formulas.md          ตาราง + คอลัมน์ + สูตรทั้งหมด 319 รายการ
├── 04-views-actions-rules-slices.md    Views / Actions / Format Rules / Slices
├── 05-erd.md                           ความสัมพันธ์ 80 รายการ + mermaid
├── 06-glossary.md                      อภิธานศัพท์ไทย-อังกฤษ
├── 07-validation-report.md             ผลตรวจความครบถ้วน
├── 08-ai-starter-prompts.md            พรอมต์พร้อมใช้ 8 แบบ
├── 09-location-check-design.md         ออกแบบฟีเจอร์ตรวจตำแหน่ง (20 ม. + ปุ่มยืนยัน)
├── tables/          ← 29 ไฟล์ md  (ตารางจริง ทีละตาราง)
├── process-tables/  ← 61 ไฟล์ md  (ตารางบอท ทีละตาราง)
└── rules/           ← 11 ไฟล์ md  (Format Rule ทีละกติกา)

app/          ← ชั้นข้อมูลดิบ machine-readable
  meta.json            ตัวเลขสรุป + metadata ของแอป
  tables.csv           90 ตาราง (kind = business|bot|system, source_path, security_filter)
  columns.csv          2304 คอลัมน์ (type, app_formula, initial_value, valid_if, ref_table ...)
  computed_columns.csv 319 คอลัมน์ที่มีสูตร/ค่าเริ่มต้น
  relations.csv        80 ความสัมพันธ์ Ref
  views.csv actions.csv slices.csv format_rules.csv
  table_groups.json    รายชื่อตารางแยกตามกลุ่ม
  tables.json          ทุกอย่างรวมกัน (ตาราง → คอลัมน์ → ค่าทั้งหมด)

data/         ← ข้อมูลระดับแถว (CSV) + manifest.json (สัญญาไฟล์)
scripts/      ← เครื่องมือ (ดึงข้อมูล / สร้างเอกสาร / ตรวจความครบถ้วน)
source/       ← PDF ต้นฉบับ
```

> 💡 **ทางลัดสำหรับ AI:** ถ้าต้องทำงานกับตารางเดียว ให้เปิด
> `docs/tables/<ชื่อตาราง>.md` ไฟล์เดียวจบ — ได้คอลัมน์ สูตร เงื่อนไข
> และความสัมพันธ์ครบ ไม่ต้องเปิด CSV 2304 แถว

## 3. ⭐ ตารางจริง vs ตารางบอท — อ่านตรงนี้ก่อนวิเคราะห์

| | ตารางจริง (29) | ตารางบอท (60 + 1 ระบบ) |
|---|---|---|
| `kind` | `business` | `bot` / `system` |
| Data Source | `google` / `google_tables` | `native` |
| source_path | ชื่อแอป (Google Sheet) | `/ProcessStateTables/...` |
| Visible | `ALWAYS` | `NEVER` |
| เก็บอะไร | ข้อมูลงานจริง (งาน/บิล/พนักงาน/รถ/เอกสาร) | state machine ของ automation |
| วิเคราะห์เป็นข้อมูลธุรกิจได้ | ✅ | ❌ |

**ตารางบอทคืออะไร**

* `Process for … Process Table` — ตารางตั้งค่า/ตัวแปรของ process
* `Process for … State Table` — ขั้นตอน (step) ของ process
* `… Output` / `Clear Output` / `New step Output` — ผลลัพธ์ของแต่ละ step
* ชื่อตารางบอทบอก "เจ้าของ" ได้เป็นน้อย เช่น `Process for ปริ๊นใบวางบิล Process Table`
  → บอทที่ปริ๊นใบวางบิล

**ทำไมต้องแยก**: ตารางบอทถูกเขียนทับและล้างอยู่ตลอด (Clear Output) และมีแถวซ้ำ
ถ้าเอาไปรวมกับตารางจริงจะได้ตัวเลขผิดทันที — ให้ใช้ตารางบอทเป็น "คำอธิบายว่า
ข้อมูลในตารางจริงถูกสร้างขึ้นอย่างไร" ไม่ใช่เป็นแหล่งข้อมูลหลัก

---

## 4. วิธีอ่าน schema

```python
import csv, json, pathlib
R = pathlib.Path(".")                      # รันจากรากของ repo

tables   = list(csv.DictReader((R/"app/tables.csv").open(encoding="utf-8")))
columns  = list(csv.DictReader((R/"app/columns.csv").open(encoding="utf-8")))
relations= list(csv.DictReader((R/"app/relations.csv").open(encoding="utf-8")))

biz = [t for t in tables if t["kind"] == "business"]
cols_of = lambda name: [c for c in columns if c["table"] == name]

# ตารางที่มีคอลัมน์คำนวณสูงสุด
sorted(biz, key=lambda t: -int(t["computed_column_count"]))[:5]

# สูตรทั้งหมดของตารางหนึ่ง
for c in cols_of("SCGนครหลวงJWDภูมิภาค"):
    if c["app_formula"]:
        print(c["name"], "->", c["app_formula"])

# ความสัมพันธ์ของตาราง
[rel for rel in relations if rel["from_table"] == "ตารางงานประจำวัน"]
```

ด้วย pandas:

```python
import pandas as pd
tables  = pd.read_csv("app/tables.csv")
columns = pd.read_csv("app/columns.csv")
biz_cols = columns[columns.table_kind == "business"]
biz_cols.groupby("table")["name"].count().sort_values(ascending=False)
```

---

## 5. ตัวอย่างคำถามที่ตอบได้ / ยังตอบไม่ได้

| คำถาม | ตอบได้ตอนนี้? | ต้องมีอะไรเพิ่ม |
|---|---|---|
| โครงสร้างข้อมูลมีตารางอะไรบ้าง | ✅ `app/tables.csv` | — |
| คอลัมน์ไหนคำนวณราคาเอง | ✅ `app/computed_columns.csv` | — |
| ตารางไหนเชื่อมกับตารางไหน | ✅ `app/relations.csv` | — |
| บอทไหนเขียนข้อมูลลงตารางไหน | ✅ บางส่วน `docs/04` | นิยามบอทจริงจาก AppSheet → Automations |
| รายได้/ต้นทุน/จำนวนงานรายเดือน | ❌ | ข้อมูลแถวใน `data/` |
| งานไหนค้างสแกน | ❌ | ข้อมูลแถวใน `data/` |
| ตารางไหนยังไม่มีข้อมูลเลย | ❌ | ข้อมูลแถวใน `data/` |

---

## 6. ข้อจำกัดและความเสี่ยง (ต้องบอกผู้ใช้เสมอ)

1. **ไม่มีข้อมูลแถว** — ทุกคำตอบเชิงตัวเลขยังตอบไม่ได้ อย่าแต่งตัวเลข
2. **PDF ไม่มีนิยามบอท** — AppSheet "Application Documentation" ไม่มีส่วน
   Automation/Bot (event, webhook, schedule) มีแต่ผลข้างเคียงของบอท
   (ตาราง Process/Output และ action) ดู `docs/02-process-output-tables.md`
3. **ตารางบอทเป็น state machine** — ห้ามนับแถวจากตารางบอทเป็นธุรกิจ
4. **PII** — มีชื่อ-นามสกุล, เบอร์โทร, ทะเบียนรถ, อีเมล, พิกัด GPS, ที่อยู่ปลายทาง
   และข้อมูลลูกค้า/ผู้รับเหมา → **ปกปิด/รวมกลุ่มก่อนส่งออกนอกองค์กร**
   (คอลัมน์ที่ติดธง `sensitive_data=Yes` ใน `app/columns.csv`)
5. **สูตรมาจาก PDF** — ค่าที่มีเครื่องหมายคำพูดและสูตรอาจคัดลอกมาไม่ครบ 100%
   เมื่อเทียบกับตัวจริงใน AppSheet ให้ถือ `app/columns.csv` เป็นหลัก แต่ถ้าจะใช้สูตร
   ใน production ให้ตรวจใน AppSheet อีกครั้ง
6. **ชื่อที่มีเว้นวรรค** — ชื่อตาราง/คอลัมน์บางตัวมีเว้นวรรคภายใน (เช่น
   `Process for โอนคลัง บุญถาวร เกษตร_นวมิ นทร์ - 1 Process Table`) ให้ quote เสมอ

---

## 7. มารยาทของ agent (บังคับ)

1. **ห้ามเดา schema** — ถ้าไม่แน่ใจว่าคอลัมน์ชื่ออะไร ให้เปิด `app/columns.csv` ดู
2. **อ้างอิง path เสมอ** — ทุกข้อสรุปควรบอกว่ามาจากไฟล์ไหน
3. **แยกข้อเท็จจริงกับข้อสันนิษฐาน** — ถ้าอนุมานจากชื่อ ให้เขียนว่า "น่าจะเป็น..."
   และอ้างหลักฐานที่ใช้
4. **ถ้าข้อมูลไม่มี ให้บอกว่าไม่มี** พร้อมบอกว่าต้องมีอะไรเพิ่ม (ดูตารางข้อ 5)
5. **อย่าแก้ `app/` ด้วยมือ** — ถ้าต้องแก้ schema ให้แก้ `scripts/extract_appsheet.py`
   แล้วรันใหม่ (ต้องได้ตัวเลขตรงตาม PDF ทุกครั้ง)
6. **หลังแก้เอกสาร ให้รัน** `python3 scripts/validate_repo.py` — ถ้าไม่ผ่าน ห้ามส่งงาน

---

## 8. คำสั่งที่ใช้บ่อย

```bash
python3 scripts/validate_repo.py          # ตรวจความครบถ้วนทั้ง repo (CI ใช้อันนี้)
python3 scripts/make_docs.py              # สร้างเอกสารจาก schema ใหม่ทั้งหมด
python3 scripts/make_docs.py --check      # ตรวจว่าเอกสารที่ generate ไว้ยังตรงกับ schema
python3 scripts/make_data_manifest.py     # สร้าง data/manifest.json ใหม่
python3 scripts/pull_data.py --help       # ตัวดึงข้อมูลจริง (3 วิธี)
./scripts/publish_to_github.sh <remote>   # ตรวจคุณภาพแล้ว push ขึ้น GitHub
```

---

## 9. เส้นทางของข้อมูล (data lineage) — สรุปสั้น ๆ

```
ลูกค้า/ผู้ใช้แอป
   ↓  บันทึกงานประจำวัน + สแกนใบวางบิล
ตารางจริง: ตารางงานประจำวัน / SCGนครหลวงJWDภูมิภาค / ScanDocs
   ↓  bot ปริ๊นใบวางบิล, bot จัดเรียงเส้นทาง, bot เบิกค่า
ตารางจริง: ข้อมูลการวางบิล / สรุปเบิกส่วนต่าง / ทำเบิกส่วนต่างScgวังน้อย
   ↓  bot เคลียสรุปจุดส่ง, bot ราคาน้ำมัน, bot อนุมัติ
ตารางจริง: ราคาในระบบก่อนส่งสินค้า / รับงานคืนได้เงิน200 / ข้อมูลงานRT, RW
   ↓
ตารางสรุป: สรุป_Shipment / สรุป_เจ้าของสินค้า / หน้าหลัก
```

รายละเอียดและหลักฐานอยู่ใน `docs/02-process-output-tables.md`

---

## 10. เครื่องมือที่มีให้ใช้

| ไฟล์ | ทำอะไร |
|---|---|
| `scripts/extract_appsheet.py` | แปลง PDF (pdftotext) → schema JSON (deterministic 100%) |
| `scripts/pdf_geometry.py` | ดึงพิกัดข้อความจาก PDF เพื่อ reconstruct ค่าที่ถูกตัดบรรทัด |
| `scripts/build_schema.py` | schema → `app/*.csv` + `app/*.json` + แยกตารางจริง/บอท |
| `scripts/make_docs.py` | สร้างเอกสารทั้งหมดจาก schema (ไม่มีทางตกหล่น) |
| `scripts/validate_repo.py` | เกณฑ์ผ่าน/ไม่ผ่านของทั้ง repo |
| `scripts/pull_data.py` | ดึงข้อมูลแถวจริง (Google Sheets / AppSheet API / export เอง) |
| `scripts/publish_to_github.sh` | ตรวจคุณภาพแล้ว push ขึ้น GitHub |
