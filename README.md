# 📦 AppSheet → GitHub · Appsheet-PPY

> ชุดข้อมูล **AppSheet app ของ หจก. เผ่าปัญญา ทรานสปอร์ต** (ระบบขนส่งโลจิสติกส์ ลูกค้า SCG Express / SCGJWD)
> แปลงเป็น **โครงสร้างที่ AI ทุกตัวอ่านเข้าใจและวิเคราะห์ต่อได้ทันที**
> — ตาราง · คอลัมน์ · สูตร · ความสัมพันธ์ · บอท · กติกา UI ครบทุกชิ้น

**เอกสารต้นฉบับ:** AppSheet "Application Documentation" (PDF, 1,946 หน้า)
**วันที่สร้าง:** 15/09/2569 · **เวอร์ชันแอป:** 1.004638 · **App ID:** `เผ่าปัญญาทรานสปอร์ต-915154893`

---

## 🚀 เริ่มที่นี่ (สำหรับ AI)

```
อ่าน AGENTS.md ก่อนเสมอ แล้วค่อยเปิด docs/tables/<ชื่อตาราง>.md ของตารางที่ต้องทำงาน
```

* **[`AGENTS.md`](AGENTS.md)** — คู่มือฉบับสั้น: โครงสร้าง repo, อ่าน schema ยังไง,
  ข้อจำกัดที่ต้องระวัง (ตารางบอท, PII, ยังไม่มีข้อมูลแถว), มารยาทการตอบ
* **[`docs/08-ai-starter-prompts.md`](docs/08-ai-starter-prompts.md)** — พรอมต์พร้อมใช้ 8 แบบ
  (สรุปโครงสร้าง · วิเคราะห์สูตรราคา · หางานค้าง · เช็คคุณภาพข้อมูล · ออกแบบฟิลด์ใหม่ · รีวิวโค้ด)

ตัวอย่างเริ่มต้น 5 บรรทัด:

```python
import csv
cols = list(csv.DictReader(open("app/columns.csv", encoding="utf-8")))
for c in cols:
    if c["table"] == "ตารางงานประจำวัน" and c["app_formula"]:
        print(c["name"], "->", c["app_formula"])
```

---

## 📊 ตัวเลขทั้งระบบ

| สิ่ง | จำนวน | หมายเหตุ |
|---|---:|---|
| **ตารางทั้งหมด** | **90** | ตรงกับที่ PDF ประกาศไว้ทุกตัว |
| ├ 📋 **ตารางจริง** (ข้อมูลธุรกิจ) | **29** | `Data Source = google` · `Visible? = ALWAYS` |
| ├ 🤖 **Process + Output Tables** | **60** | `Data Source = native` · `Visible? = NEVER` |
| └ ⚪ ตารางระบบ | 1 | `_Per User Settings` |
| **คอลัมน์** | **2304** | ครบทุกคอลัมน์ของทุกตาราง |
| คอลัมน์คำนวณอัตโนมัติ | 319 | 192 `App formula` + 127 `Initial value` |
| ความสัมพันธ์ระหว่างตาราง | 80 | ทั้งหมดเป็น many-to-one |
| Views / Actions / Slices / Format Rules | 115 / 214 / 8 / 11 | |

---

## 🗂️ โครงสร้างรีโป

```
├── README.md                     ← ไฟล์นี้
├── AGENTS.md                     ← คู่มือสำหรับ AI agent
├── docs/
│   ├── 00-overview.md                   โครงสร้างทั่วไปของแอป
│   ├── 01-main-tables.md                📋 สารบัญตารางจริง 29 ตาราง
│   ├── 02-process-output-tables.md      🤖 วิเคราะห์บอท + สารบัญตารางบอท 61 ตาราง
│   ├── 03-columns-and-formulas.md       ตาราง + คอลัมน์ + สูตรทั้งหมด
│   ├── 04-views-actions-rules-slices.md Views / Actions / Format Rules / Slices
│   ├── 05-erd.md                        ความสัมพันธ์ 80 รายการ + แผนภาพ mermaid
│   ├── 06-glossary.md                   อภิธานศัพท์ไทย-อังกฤษ
│   ├── 07-validation-report.md          ผลตรวจความครบถ้วน
│   ├── 08-ai-starter-prompts.md         พรอมต์พร้อมใช้สำหรับ AI
│   ├── tables/          ← 29 ไฟล์ md   ตารางจริง ทีละตาราง
│   ├── process-tables/  ← 61 ไฟล์ md   ตารางบอท ทีละตาราง
│   └── rules/           ← 11 ไฟล์ md   Format Rule ทีละกติกา
│
├── app/          ← ข้อมูลดิบ machine-readable (สำหรับโค้ด)
│   ├── meta.json            ตัวเลขสรุป + metadata
│   ├── tables.csv           90 ตาราง
│   ├── columns.csv          2304 คอลัมน์
│   ├── computed_columns.csv 319 คอลัมน์คำนวณ
│   ├── relations.csv        80 ความสัมพันธ์
│   ├── views.csv / actions.csv / slices.csv / format_rules.csv
│   ├── table_groups.json    แยกตารางจริง/บอท/ระบบ
│   └── tables.json          รวมทุกอย่างเป็นไฟล์เดียว
│
├── data/         ← ข้อมูลระดับแถว (CSV) + manifest.json
├── scripts/      ← เครื่องมือทำซ้ำได้ทั้งหมด
├── source/       ← PDF ต้นฉบับ
└── .github/workflows/ci.yml
```

---

## 💡 ทำไมโครงสร้างนี้ดีกว่า "ทำเองแบบที่ทำมา"

คุณบอกว่าเดิมทำเอง เติมเอง ศึกาเองจากยูทูป/ถาม AI — วิธีนี้ **ใช้ได้ผล** แต่มีข้อจำกัดที่ชุดนี้แก้ได้:

| ปัญหาเดิม | วิธีแก้ในรีโปนี้ |
|---|---|
| AI ต้องอ่าน CSV 2304 แถวเพื่อรู้ว่าตารางหนึ่งมีอะไรบ้าง | **ไฟล์ md ทีละตาราง** — เปิดไฟล์เดียวจบ ได้คอลัมน์+สูตร+เงื่อนไข+ความสัมพันธ์ครบ |
| ไม่รู้ว่าตารางไหน "ของจริง" ตารางไหน "ของบอท" — AI อาจไปวิเคราะห์ตารางบอทแล้วได้ตัวเลขผิด | **แยกชัดเจน** `kind = business / bot / system` + โฟลเดอร์ `tables/` vs `process-tables/` + คำเตือนในทุกไฟล์ |
| สูตรกับค่าที่ใช้จริงอยู่คนละที่ อาจเพี้ยน | **สูตรมาจากการคัดลอกอัตโนมัติจาก PDF** พร้อมคำอธิบายไทย และตรวจ JSON ผ่านทุกตัว |
| เอกสารทำมาแล้วหลุด/เอกสารไม่ตรงกับ schema | **CI ตรวจทุก push** — 24 เกณฑ์ ถ้าเอกสารตกหล่วง1 รายการก็ fail |
| ทำซ้ำใหม่ทุกครั้งเสียเวลา | **ทุกอย่าง generate ได้** — `python3 scripts/make_docs.py` สร้างเอกสาร 105 ไฟล์ใน ~1 วินาที |
| ไม่รู้ว่าข้อมูลครบจริงไหม | **ตัวเลขจาก PDF เป็นเกณฑ์** — ตรงทุกตัว (90/2304/115/214/8/11) และทำซ้ำได้ byte-identical |

**สิ่งที่ยังทำแทนไม่ได้:** ข้อมูลระดับแถว (rows) — PDF ไม่มี
ต้อง export จาก AppSheet/Google Sheets (ดู [`data/README.md`](data/README.md)) แล้วรีโปนี้จะ
กลายเป็นชุดข้อมูลวิเคราะห์เต็มรูปแบบทันที

---

## 🤖 เรื่องของบอท — อ่านก่อนวิเคราะห์

แอปนี้มี **บอท/automation หลายสิบตัว** ซึ่งสร้างข้อมูลในตารางจริงอัตโนมัติ
PDF ที่ให้มา **ไม่มีนิยามบอท** (ไม่มี event/trigger/schedule) — มีแต่ผลข้างเคียง คือ
ตาราง Process/Output และ action

⇒ ดู [`docs/02-process-output-tables.md`](docs/02-process-output-tables.md) ซึ่งไล่ pipeline จริง
พร้อมบอกชัดว่าอะไรมีหลักฐานและอะไรไม่มี

---

## 🔐 ข้อควรระวังด้านข้อมูลส่วนบุคคล (PII)

ข้อมูลชุดนี้มี **ชื่อ-นามสกุล · เบอร์โทร · ทะเบียนรถ · อีเมล · พิกัด GPS · ที่อยู่ปลายทาง
· ข้อมูลลูกค้า/ผู้รับเหมา**

* คอลัมน์ที่ติดธง PII อยู่ใน `app/columns.csv` คอลัมน์ `sensitive_data`
* ถ้าจะทำรีโปสาธารณะหรือส่งออกนอกองค์กร **ต้องปกปิดข้อมูลส่วนบุคคลก่อน**
* แอปใช้ row security `=OR(USERROLE() = "ADMIN", [Email พนักงาน] = USEREMAIL())`
  → พนักงานเห็นเฉพาะแถวของตัวเอง ผู้ดูแล (ADMIN) เห็นทั้งหมด

---

## ✅ ตรวจคุณภาพ

```bash
python3 scripts/validate_repo.py --repo .
```

24 เกณฑ์ — ครอบคลุมจำนวน record, ความครบถ้วนของเอกสาร, ความถูกต้องของ JSON,
ความสัมพันธ์, alignment ของ action/view, และความสอดคล้องกับ manifest
CI รันอัตโนมัติทุก push และ pull request

ผลล่าสุด: [`docs/07-validation-report.md`](docs/07-validation-report.md)

---

## 🛠 เครื่องมือ

| คำสั่ง | ทำอะไร |
|---|---|
| `python3 scripts/validate_repo.py` | ตรวจความครบถ้วนทั้ง repo (CI ใช้อันนี้) |
| `python3 scripts/make_docs.py` | สร้างเอกสารทั้งหมด 105 ไฟล์ใหม่จาก schema |
| `python3 scripts/make_docs.py --check` | ตรวจว่าเอกสารตรงกับ schema (ไม่ตกหล่น) |
| `python3 scripts/extract_appsheet.py <pdftotext.txt> <out>` | แปลง PDF → schema JSON (deterministic ไม่ใช้ AI) |
| `python3 scripts/build_schema.py <schema_raw.json> <out>` | schema → `app/*.csv` + `app/*.json` + แยกตารางจริง/บอท |
| `python3 scripts/pull_data.py --help` | ดึงข้อมูลแถวจริง (Google Sheets / AppSheet API / export เอง) |
| `python3 scripts/make_data_manifest.py` | สร้าง `data/manifest.json` ใหม่ |
| `./scripts/publish_to_github.sh <remote>` | ตรวจคุณภาพแล้ว push ขึ้น GitHub |

---

## 📄 ที่มาและสัญญาอนุญาต

ทั้งหมดมาจาก **Application Documentation.PDF** ของ AppSheet (เก็บไว้ใน `source/`
เพื่อให้ตรวจสอบย้อนกลับได้) การแยก schema ทำด้วย `scripts/extract_appsheet.py`
(deterministic ไม่ใช้ AI) และตรวจสอบด้วย `scripts/validate_repo.py` ทุกครั้ง

**MIT License** — ดู [LICENSE](LICENSE)
