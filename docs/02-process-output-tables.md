# โครงสร้างภายในของบอทและระบบอัตโนมัติ

> ⚠️ **ข้อจำกัดที่ต้องรู้ก่อนอ่าน:** เอกสาร "Application Documentation" ของ AppSheet
> **ไม่มีส่วนนิยามของบอท** (ไม่มี event / webhook / schedule / bot definition)
> สิ่งที่มีคือ **ผลข้างเคียง** ของบอท ได้แก่
> 1. **ตารางบอท** 60 ตาราง (Process Table / Step Output) — ที่บอทเขียนกลับมา
> 2. **action** 214 รายการ — คำสั่งที่ผู้ใช้/ระบบเรียกใช้
> 3. **slices** 8 และ **format rules** 11 — กติกาการแสดงผล
>
> ถ้าต้องการนิยามบอทจริง (ทริกเกอร์/เวลา/เงื่อนไข) ให้ไปที่
> **AppSheet → Automations → Bots** แล้ว export — ดู [วิธีเติมข้อมูล](#วิธีเติมนิยามบอทจริง)

---

## 1. ตารางบอทมีอะไรบ้าง

ระบบอัตโนมัติของแอปนี้แบ่งเป็น **2 กลุ่ม**

### กลุ่ม A — บอทประมวลผลใบวางบิล (โหลดมากที่สุด)

ชื่อเริ่มด้วย `Process for ปริ๊นใบวางบิล...` — คือบอทที่ไปดึงข้อมูลจากระบบปริ๊นของแต่ละ
คลัง/สาขามาสร้างใบวางบิล มีหลายเวอร์ชันเพราะแต่ละคลังมีระบบปริ๊นต่างกัน

| บอท | ตารางผลลัพธ์ | หมายเหตุจากหลักฐาน (source_path / action) |
|---|---|---|
| `Process for ปริ๊นใบวางบิล Process Table` | `ปริ๊นใบวางบิล_step Output` | บอทปริ๊นหลัก |
| `Process for ปริ๊นใบวางบิล_โอนคลัง มโนยนต์ (นวนคร)` | `Clear Output 2` | โอนคลังมโนยนต์ (สาขานวนคร) |
| `Process for ปริ๊นใบวางบิล_โอนคลัง กระสอบ2(บางบัวทอง)` | `Clear Output 3` | โอนคลัง กระสอบ 2 (บางบัวทอง) |
| `Process for ปริ๊นใบวางบิล_ไอโรบอท Process Table` | `Clear Output 4` | ไอโรบอท — คลังสินค้าเอสซีจี เจดับเบิ้ลยูดี วังน้อย |
| `Process for ปริ๊นใบวางบิล_โอนคลัง เอเธน Process Table` | `Clear Output 5` | โอนคลัง เอเธน |
| `Process for ปริ๊นใบวางบิล_โอนคลัง บุญถาวร เกษตร_นวมิ นทร์ - 1 Process Table` | `Clear Output 14` | โอนคลัง บุญถาวรเกษตร (นวมินทร์) |
| `Process for ปริ๊นใบวางบิล_คลังSCGJWDวังน้อย Process Table` | `Clear Output 10` | คลัง SCGJWD วังน้อย |
| `Process for ปริ๊นใบวางบิล_รับเอกสาร (งานพี่เหน่ง) Process Table` | `Clear Output 7` | รับเอกสาร (งานพี่เหน่ง) |
| `Process for ปริ๊นใบวางบิล_รับเอกสาร (งานพี่เหน่ง) สตีเบล` | `Clear Output 6` | รับเอกสาร สตีเบล |
| `Process for ปริ๊นใบวางบิล_เบทาโกร+เหมาตู้ Process Table` | `Clear Output 11` | เบทาโกร + เหมาตู้ |
| `Process for ปริ๊นใบวางบิล_LINEMAN (6W) (SCG Express)` | `Clear Output 12` | LINEMAN 6 ล้อ |
| `Process for ปริ๊นใบวางบิล_Thai paper (SCG Express) - 1` | `Clear Output 13` | Thai paper |
| `Process for ปริ๊นใบวางบิลเอเทน - 1 Process Table` | `Clear Output` | เอเทน |
| `Process for โอนคลัง (GQ) จีคิว Process Table` | `Clear Output 8` | โอนคลัง จีคิว (GQ) |

> ชื่อคลัง/สาขาในชื่อบอทตรงกับชื่อที่ปรากฏในคอลัมน์และค่าคงที่ของแอป
> เช่น `คลังสินค้า เอสซีจี เจดับเบิ้ลยูดี วังน้อย` (คอลัมน์ LatLong ค่าคงที่ในตาราง `SCGนครหลวงJWDภูมิภาค`)

### กลุ่ม B — บอทงานเฉพาะทาง

| บอท | ตารางผลลัพธ์ | หน้าที่ที่อนุมานจากชื่อ (มีหลักฐาน = ชื่อบอท + ชื่อตารางผลลัพธ์ + action ที่ผูก) |
|---|---|---|
| `Process for Telegram_แจ้งปั ญหา - 1 Process Table` | `Telegram_แจ้งปั ญหา2 Output` | ส่งแจ้งปัญหาระหว่างวันผ่าน Telegram — ยืนยันได้ว่า action `Send SMS`/`EMAIL` และตาราง `แจ้งปั ญหาระหว่างวัน` มี `Ref` จากบอทนี้ |
| `Process for Bot_รับสินค้าคืน - 1 Process Table` | `เข้ารับสินค้าคืน Output` | บอทรับสินค้าคืน — เขียนคอลัมน์ `สถานะการเข้ารับสินค้า` (มี 6 ค่า: ได้เพิ่ม 200 / ไม่มีสินค้าคืน / ได้เพิ่ม 50% / ทำเบิกค่ายกขึ้นชั้น / เบิกค่าขนส่งตามระยะทาง) |
| `Process for Bot_เบิกค่าขนส่งตามระยะทาง - 1 Process Table` | `เบิกตามระยะทาง Output` | บอทเบิกค่าขนส่งตามระยะทาง (มีตาราง `ราคาตามระยะทาง` ในตารางจริง) |
| `Process for ฺBot_4ตัว_จัดเรียงเส้นทาง Process Table` | `GoogleMapsRoutesAPI_Step Output` | จัดเรียงเส้นทาง 4 ตัว — มีหลักฐานจาก `GoogleMapsRoutesAPI` และคอลัมน์ `ที่อยู่ปลายทาง_LatLong_Api` ในตารางจริง |
| `Process for ใบป่ ะหน้า - 1 Process Table` | (State Table) | สร้างใบประกาศ/ใบหน้า |
| `Process for สรุปส่วนต่าง - 1 Process Table` | `เคลียสรุปจุดส่ง Output` | สรุปส่วนต่าง + เคลียสรุปจุดส่ง |
| `Process for สรุปจำนวนจุดที่ส่งงานSCGวังน้อย Process Table` | (State Table) | นับจำนวนจุดที่ส่งงานของ SCG วังน้อย |
| `Process for ทำเบิกส่วนต่างScgวังน้อย - 1 Process Table` | `ทำเบิกส่วนต่างScgวังน้อยstep Output`, `New step2 Output`, `ไม่ผ่านNew step Output` | บอทเบิกส่วนต่าง SCG วังน้อย (มี 3 step แยก: ผ่าน / ไม่ผ่าน) |
| `Process for ทำเบิกค่ายกขึ้นชั้น Process Table` | (State Table) | เบิกค่ายกขึ้นชั้น |
| `Process for ได้เพิ่ม25%ของค่าเที่ยว Process Table` | (State Table) | ได้เพิ่ม 25% ของค่าเที่ยว |
| `Process for ได้เพิ่ม200_ไม่มีสินค้าคืน_ร้านปิ ด_ไม่มีในจุดส่ง Process Table` | (State Table) | ได้เพิ่ม 200 เมื่อไม่มีสินค้าคืน / ร้านปิด / ไม่มีในจุดส่งงานวันนี้ |
| `Process for เพิ่มรูปรับคืน - 1 Process Table` | `New step Output` | เพิ่มรูปใบเสร็จ/สลิปตอนรับคืน |
| `Process for Update ScanStatus เมื่อสแกน Invoice - 1 Process Table` | `Update Output` | อัปเดตสถานะการสแกน (`ScanStatus`) เมื่อสแกนใบวางบิล — ยืนยันได้จาก action `Update ScanStatus` |
| `Process for New bot - 1 Process Table` | `New step Output 3` | บอทใหม่ (ยังไม่มีคำอธิบายในเอกสาร) |
| `Process for MeSpace Process Table` | `Clear Output 9` | MeSpace — มี enum `งานMeSpace+แพ็คสินค้า` ในตาราง `ข้อมูลการวางบิล` |
| `Process for AppSheet_KM - 1 Process Table` | `AppSheet___KM Output` | AppSheet_KM — ยังไม่มีคำอธิบายในเอกสาร |

---

## 2. Action catalog (214 รายการ)

จัดกลุ่มตาม `do_this` (ชนิดคำสั่ง) — ทั้งหมดเป็น action ที่ผู้ใช้กด หรือระบบเรียกจากปุ่ม/สแกน

| `do_this` | จำนวน | ความหมาย |
|---|---:|---|
| `SET_COLUMN_VALUE` | 49 | ตั้งค่าคอลัมน์ในแถวปัจจุบัน (เช่น ปุ่ม "อนุมัติ" → เซ็ต `สถานะการอนุมัติ` = "อนุมัติ") |
| `ADD_RECORD` | 29 | เพิ่มแถวใหม่ (เช่น บันทึกงานประจำวัน, บันทึกสแกน) |
| `DELETE_RECORD` | 29 | ลบแถว (เช่น เคลียสรุปจุดส่ง, ล้างข้อมูลเก่า) |
| `NAVIGATE_APP` | 29 | เปิดหน้าจอ/แอปอื่น (เช่น กดเปิดแผนที่, สลับไปหน้าสรุป) |
| `EDIT_RECORD` | 28 | เปิดฟอร์มแก้ไขแถว |
| `EXPORT_VIEW` | 21 | export ข้อมูลเป็น CSV/XLSX — มี action ชื่อลงท้าย `csv` / `xlsx` หลายรายการ (เช่น `SCGนครหลวงJWDภูมิภาค_csv`, `PDFพนักงานcsv`) |
| `EMAIL` | 12 | ส่งอีเมล (เช่น `Compose Email (Email พนักงาน)`, `Compose Email (Email ผู้อนุมัติ)`, `Compose Email (Scan_By)`) |
| `REF_ACTION` | 4 | เปิดรายการที่อ้างอิง (`View Ref (...)`) |
| `COMPOSITE` | 3 | รวมหลายคำสั่ง (เช่น `สร้างใบป่ ะหน้าทุกคน`) |
| `NAVIGATE_DIFFERENT_APP` | 3 | ข้ามไปแอปอื่น |
| `NAVIGATE_URL` | 3 | เปิด URL ภายนอก (Google Maps) |
| `SMS` | 1 | ส่ง SMS (`Send SMS (เบอร์โทรศัพท์)`) |
| `CALL` | 1 | โทรหา (`Call Phone (เบอร์โทรศัพท์)`) |
| `ADD_RECORD_TO` | 1 | เพิ่มแถวลงอีกตาราง (`ACT_Create_SCG_Flow`) |

**139 รายการเปลี่ยนแปลงข้อมูล** (`modifies_data = Yes`) — เหล่านี้คือ action ที่เขียนข้อมูลกลับเข้าตาราง
ส่วนที่เหลือเป็น action อ่านอย่างเดียว (ดูรูป, ส่งอีเมล, export)

### action ที่ผูกกับคลัง/สาขาต่าง ๆ (สร้างใบประกาศ)

มี action ชื่อ `สร้างใบป่ ะหน้า_<ชื่อ-นามสกุลพนักงาน>` อย่างน้อย 15 รายการ
(เช่น `สร้างใบป่ ะหน้า_สำเริง แก้วกามเกตุ`, `สร้างใบป่ ะหน้า_กิตติพงษ์ แหลมผักแว่น`)
→ เป็นการสร้างเอกสาร "ใบประกาศ/ใบหน้า" รายคน แยกตามผู้รับผิดชอบ

---

## 3. Pipeline map — ข้อมูลในตารางจริงถูกสร้างอย่างไร

ลำดับนี้มาจากการไล่เรียง **หลักฐานในไฟล์** (ชื่อบอท, action ที่ผูกกับตาราง, `Ref` ระหว่างตาราง,
คอลัมน์ที่คำนวณ) ไม่ใช่จากการเดา

```
① รับงานประจำวัน
   └─ พนักงาน/ระบบบันทึกงาน → ตารางจริง: ตารางงานประจำวัน (หนึ่งแถว = หนึ่งใบวางบิล)
      มี: ชื่องาน, ทะเบียนรถ, จุดส่งสินค้าปลายทาง (LatLong), ราคา, สถานะ ScanStatus

② สแกนหน้างาน
   └─ action "Compose Email (Scan_By)" / ปุ่มสแกน → ตารางจริง: SCGนครหลวงJWDภูมิภาค
      คำนวณ: ระยะขยับจากจุดเริ่มต้น_เมตร (DISTANCE), ระยะเวลาใช้งาน_นาที,
             ความเร็วการเคลื่อนที่_เมตร_นาที, ผลการตรวจสอบงานส่ง (PASS/WARNING/FAIL),
             เหตุผิดปกติที่ตรวจพบ

③ ปริ๊นใบวางบิล  (บอท "ปริ๊นใบวางบิล" + เวอร์ชันต่อคลัง/สาขา)
   └─ บอท 14 เวอร์ชัน → ตารางบอท (Step Output) → ตารางจริง: ข้อมูลการวางบิล, ปริ๊นใบวางบิล

④ คิดราคา
   └─ ตารางจริง: ราคาในระบบก่อนส่งสินค้า (ราคาตามระยะทาง + ราคาจุดเพิ่ม + เรทดีเซล)
      └─ อ้างอิง: ราคาน้ำมันดีเซล, Price_Table, PriceOverride

⑤ ตรวจสอบ/เบิกส่วนต่าง
   └─ บอท "ทำเบิกส่วนต่างScgวังน้อย" (3 step: ผ่าน/ไม่ผ่าน) → ตารางจริง: ทำเบิกส่วนต่างScgวังน้อย
   └─ บอท "รับสินค้าคืน" → ตารางจริง: รับงานคืนได้เงิน200

⑥ อนุมัติ
   └─ action "อนุมัติ" / "รอการอนุมัติ" → SET_COLUMN_VALUE ที่ `สถานะการอนุมัติ`
      เงื่อนไข: =AND([สถานะการอนุมัติ] <> "อนุมัติ", USERROLE() = "ADMIN")

⑦ สรุป
   └─ ตารางจริง: สรุป_Shipment, สรุป_เจ้าของสินค้า (ใช้ FILTER จาก ตารางงานประจำวัน)
   └─ action EXPORT_VIEW (xlsx/csv) → ส่งออกรายงาน

⑧ แจ้งปัญหา
   └─ บอท Telegram_แจ้งปั ญหา → ตารางจริง: แจ้งปั ญหาระหว่างวัน
      (มี enum 11 แบบ: สินค้าชำรุด, ถังน้ำมันหนักเกิน, ร้านปิด, ที่อยู่ไม่ตรง ฯลฯ)
```

### ตารางจริง 29 ตาราง ← บอท/แหล่งที่มีหลักฐานว่าเขียนเข้า

| ตารางจริง | หลักฐานว่ามีอะไรเขียนเข้า |
|---|---|
| `ตารางงานประจำวัน` | action `ADD_RECORD` / `EDIT_RECORD` ผูกกับตารางนี้ + `ScanStatus` ถูกอัปเดตโดยบอท "Update ScanStatus เมื่อสแกน Invoice" |
| `SCGนครหลวงJWDภูมิภาค` | action `Add` (ADD_RECORD) ผูกกับตารางนี้ |
| `ScanDocs` | บันทึกการสแกนรับ (Scan_Method = Barcode/Manual) — ผูกกับ `ตารางงานประจำวัน` ด้วย `Invoice_No` |
| `ข้อมูลการวางบิล` | บอทปริ๊นใบวางบิล + การคิดราคา (มี `ราคา` ที่คำนวณจากระยะทาง/จุดเพิ่ม) |
| `ราคาในระบบก่อนส่งสินค้า` | action ที่เซ็ตราคาก่อนส่ง (`ราคาในระบบหลังส่งสินค้า` ใน format rule) |
| `รับงานคืนได้เงิน200` | บอท "รับสินค้าคืน" + ค่า enum `สถานะการเข้ารับสินค้า` ที่บอทเขียน |
| `ทำเบิกส่วนต่างScgวังน้อย` | บอท "ทำเบิกส่วนต่างScgวังน้อย" (3 step) |
| `แจ้งปั ญหาระหว่างวัน` | บอท Telegram + `Ref` จากบอท `SM_Link` / `RT_Link` |
| `Doc_Return` | `Ref` จาก `SCGนครหลวงJWDภูมิภาค` (คอลัมน์ `ID_Doc_Return`) — เอกสารคืนสินค้าถูกสร้างจากงานสแกน |
| `ราคาน้ำมันดีเซล`, `Price_Table`, `PriceOverride` | ตารางตั้งค่าราคา (อัปเดตโดยคน) — มีหลักฐานจาก enum/ชื่อคอลัมน์ `StartDate`/`EndDate` |
| ตารางอื่น 20 ตาราง | ไม่ปรากฏว่ามีบอทเขียนเข้าในเอกสารนี้ — ให้ถือว่าเป็นตารางที่คนกรอก/คำนวณเอง |

---

## 4. Slices (8) และ Format rules (11)

**Slices** คือมุมมองของตารางเดียวกันที่กรอง/เรียงข้อมูลต่างกัน
(เช่น `รอการอนุมัติ` กรอง `=USERROLE() = "ADMIN"`)

**Format rules** คือกติกาการเปลี่ยนสี/ตัวหนา/ไอคอนตามเงื่อนไข เช่น
`อนุมัติ` → ตัวหนาสีเขียว, `รอการอนุมัติ` → สีส้ม, `ผลการตรวจสอบงานส่ง_FAIL` → สีแดง
→ **AI ที่อ่านข้อมูลต้องรู้ว่าสี/สถานะใน UI ถูกกำหนดโดยกติกาเหล่านี้ ไม่ใช่ข้อมูลดิบ**

---

## 5. วิธีเติมนิยามบอทจริง

1. เปิดแอป → **Automations → Bots** → ดูแต่ละบอท (ชื่อ, trigger, condition, ตารางที่เขียน)
2. Export เป็นไฟล์ แล้ววางใน `app/automations.json` ในรูปแบบ:

```json
{
  "bots": [
    {
      "name": "ปริ๊นใบวางบิล",
      "event": "<ชนิด event>",
      "condition": "<เงื่อนไข>",
      "process_table": "Process for ปริ๊นใบวางบิล Process Table",
      "writes_to": ["ข้อมูลการวางบิล"]
    }
  ]
}
```

3. ผนวกเข้ากับ `app/actions.csv` เพื่อให้ AI เห็นว่า "อะไรเขียนลงตารางไหน เมื่อไร"

> จนกว่าจะเติม ให้ถือว่า **ทุกข้อความในหน้านี้เป็น "หลักฐานจากชื่อและโครงสร้าง" ไม่ใช่นิยามบอท**
> ห้ามอ้างว่าบอททำงานเวลาใดหรือทริกเกอร์อะไร เพราะเอกสารไม่มี

---

## 6. ดัชนีตารางบอททั้ง 61 ตาราง

---

# 02 — Process Tables + Output Tables

> **61 ตาราง** ที่ AppSheet สร้างให้กับระบบอัตโนมัติ — **ไม่ใช่ข้อมูลธุรกิจ**
> ห้ามนับแถวจากตารางเหล่านี้ (ถูกเขียนทับและล้างอยู่ตลอด)

## ชนิดของตารางบอท

| ชนิด | รูปแบบชื่อ | source_path | หน้าที่ |
|---|---|---|---|
| Process Table | `Process for <บอท> Process Table` | `/ProcessStateTables/<bot>/<tbl>/State Table` | ตัวแปรที่ส่งผ่านขั้นตอนของ process |
| Step Output | `<ชื่อ> Output` / `New step Output` | `/ProcessStateTables/.../StepOutput_<ชื่อ>` | ผลลัพธ์ของ step — ถูกล้างทุกครั้งที่รัน |
| ระบบ | `_Per User Settings` | `_Per User Settings` | ค่าตั้งค่ารายผู้ใช้ |

## ดัชนีตารางบอท

| # | ตาราง | ชนิด | คอลัมน์ | ที่มา |
|---:|---|---|---:|---|
| 1 | [`_Per User Settings`](process-tables/Per_User_Settings.md) | system | 15 | `_Per User Settings` |
| 2 | [`Process for ปริ๊นใบวางบิล Process Table`](process-tables/Process_for_ปริ๊นใบวางบิล_Process_Table.md) | bot | 12 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/c5a…` |
| 3 | [`ปริ๊นใบวางบิล_step Output`](process-tables/ปริ๊นใบวางบิล_step_Output.md) | bot | 11 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b-417bc046f574/c5…` |
| 4 | [`Process for Telegram_แจ้งปั ญหา - 1 Process Table`](process-tables/Process_for_Telegram_แจ้งปั_ญหา_1_Process_Table.md) | bot | 30 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/f3c…` |
| 5 | [`Telegram_แจ้งปั ญหา2 Output`](process-tables/Telegram_แจ้งปั_ญหา2_Output.md) | bot | 1 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/f3c…` |
| 6 | [`Process for Bot_รับสินค้าคืน - 1 Process Table`](process-tables/Process_for_Bot_รับสินค้าคืน_1_Process_Table.md) | bot | 30 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/4cc…` |
| 7 | [`เข้ารับสินค้าคืน Output`](process-tables/เข้ารับสินค้าคืน_Output.md) | bot | 1 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/4cc…` |
| 8 | [`Process for เพิ่มรูปรับคืน - 1 Process Table`](process-tables/Process_for_เพิ่มรูปรับคืน_1_Process_Table.md) | bot | 30 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/6a9…` |
| 9 | [`New step Output`](process-tables/New_step_Output.md) | bot | 2 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/6a9…` |
| 10 | [`Process for ใบป่ ะหน้า - 1 Process Table`](process-tables/Process_for_ใบป่_ะหน้า_1_Process_Table.md) | bot | 11 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/49b…` |
| 11 | [`Process for ปริ๊นใบวางบิลเอเทน - 1 Process Table`](process-tables/Process_for_ปริ๊นใบวางบิลเอเทน_1_Process_Table.md) | bot | 12 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/686…` |
| 12 | [`Clear Output`](process-tables/Clear_Output.md) | bot | 11 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/686…` |
| 13 | [`Process for สรุปส่วนต่าง - 1 Process Table`](process-tables/Process_for_สรุปส่วนต่าง_1_Process_Table.md) | bot | 12 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/b35…` |
| 14 | [`Process for สรุปจำนวนจุดที่ส่งงานSCGวังน้อย Process Table`](process-tables/Process_for_สรุปจำนวนจุดที่ส่งงานSCGวังน้อย_Process_Table.md) | bot | 15 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/583…` |
| 15 | [`เคลียสรุปจุดส่ง Output`](process-tables/เคลียสรุปจุดส่ง_Output.md) | bot | 14 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/583…` |
| 16 | [`Process for ปริ๊นใบวางบิลโอนคลัง มโนยนต์ (นวนคร) Process Table`](process-tables/Process_for_ปริ๊นใบวางบิลโอนคลัง_มโนยนต์_นวนคร_Process_Table.md) | bot | 12 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/807…` |
| 17 | [`Clear Output 2`](process-tables/Clear_Output_2.md) | bot | 11 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/807…` |
| 18 | [`Process for ปริ๊นใบวางบิล_โอนคลัง กระสอบ2(บางบัวทอง) Process Table`](process-tables/Process_for_ปริ๊นใบวางบิล_โอนคลัง_กระสอบ2_บางบัวทอง_Process_Table.md) | bot | 12 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/76d…` |
| 19 | [`Clear Output 3`](process-tables/Clear_Output_3.md) | bot | 11 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/76d…` |
| 20 | [`Process for ปริ๊นใบวางบิล_ไอโรบอท Process Table`](process-tables/Process_for_ปริ๊นใบวางบิล_ไอโรบอท_Process_Table.md) | bot | 12 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/df3…` |
| 21 | [`Clear Output 4`](process-tables/Clear_Output_4.md) | bot | 11 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b-417bc046f574/df…` |
| 22 | [`Process for ปริ๊นใบวางบิล_โอนคลัง เอเธน Process Table`](process-tables/Process_for_ปริ๊นใบวางบิล_โอนคลัง_เอเธน_Process_Table.md) | bot | 12 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/5f1…` |
| 23 | [`Clear Output 5`](process-tables/Clear_Output_5.md) | bot | 11 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/5f1…` |
| 24 | [`Process for ปริ๊นใบวางบิล_รับเอกสาร (งานพี่เหน่ง) สตีเบล Process Table`](process-tables/Process_for_ปริ๊นใบวางบิล_รับเอกสาร_งานพี่เหน่ง_สตีเบล_Process_Table.md) | bot | 12 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/627…` |
| 25 | [`Clear Output 6`](process-tables/Clear_Output_6.md) | bot | 11 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/627…` |
| 26 | [`Process for ปริ๊นใบวางบิล_รับเอกสาร (งานพี่เหน่ง) Process Table`](process-tables/Process_for_ปริ๊นใบวางบิล_รับเอกสาร_งานพี่เหน่ง_Process_Table.md) | bot | 12 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/cb7…` |
| 27 | [`Clear Output 7`](process-tables/Clear_Output_7.md) | bot | 11 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/cb7…` |
| 28 | [`Process for ฺBot_4ตัว_จัดเรียงเส้นทาง Process Table`](process-tables/Process_for_ฺBot_4ตัว_จัดเรียงเส้นทาง_Process_Table.md) | bot | 137 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/6d3…` |
| 29 | [`GoogleMapsRoutesAPI_Step Output`](process-tables/GoogleMapsRoutesAPI_Step_Output.md) | bot | 1 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/6d3…` |
| 30 | [`Process for โอนคลัง (GQ) จีคิว Process Table`](process-tables/Process_for_โอนคลัง_GQ_จีคิว_Process_Table.md) | bot | 12 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/283…` |
| 31 | [`Clear Output 8`](process-tables/Clear_Output_8.md) | bot | 11 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/283…` |
| 32 | [`Process for MeSpace Process Table`](process-tables/Process_for_MeSpace_Process_Table.md) | bot | 12 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/e8d…` |
| 33 | [`Clear Output 9`](process-tables/Clear_Output_9.md) | bot | 11 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/e8d…` |
| 34 | [`Process for ปริ๊นใบวางบิล_คลังSCGJWDวังน้อย Process Table`](process-tables/Process_for_ปริ๊นใบวางบิล_คลังSCGJWDวังน้อย_Process_Table.md) | bot | 12 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/5bd…` |
| 35 | [`Clear Output 10`](process-tables/Clear_Output_10.md) | bot | 11 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/5bd…` |
| 36 | [`Process for ได้เพิ่ม200_ไม่มีสินค้าคืน_ร้านปิ ด_ไม่มีในจุดส่ง Process Table`](process-tables/Process_for_ได้เพิ่ม200_ไม่มีสินค้าคืน_ร้านปิ_ด_ไม่มีในจุดส่ง_Process_Table.md) | bot | 14 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/822…` |
| 37 | [`Process for ทำเบิกค่ายกขึ้นชั้น Process Table`](process-tables/Process_for_ทำเบิกค่ายกขึ้นชั้น_Process_Table.md) | bot | 14 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/4a9…` |
| 38 | [`Process for ได้เพิ่ม25%ของค่าเที่ยว Process Table`](process-tables/Process_for_ได้เพิ่ม25_ของค่าเที่ยว_Process_Table.md) | bot | 14 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/e0e…` |
| 39 | [`Process for ทำเบิกส่วนต่างScgวังน้อย - 1 Process Table`](process-tables/Process_for_ทำเบิกส่วนต่างScgวังน้อย_1_Process_Table.md) | bot | 139 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/664…` |
| 40 | [`ทำเบิกส่วนต่างScgวังน้อยstep Output`](process-tables/ทำเบิกส่วนต่างScgวังน้อยstep_Output.md) | bot | 2 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/664…` |
| 41 | [`New step2 Output`](process-tables/New_step2_Output.md) | bot | 136 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/664…` |
| 42 | [`ไม่ผ่านNew step Output`](process-tables/ไม่ผ่านNew_step_Output.md) | bot | 136 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/664…` |
| 43 | [`Process for AppSheet_KM - 1 Process Table`](process-tables/Process_for_AppSheet_KM_1_Process_Table.md) | bot | 51 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/261…` |
| 44 | [`AppSheet___KM Output`](process-tables/AppSheet___KM_Output.md) | bot | 1 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/261…` |
| 45 | [`New step Output 2`](process-tables/New_step_Output_2.md) | bot | 49 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/261…` |
| 46 | [`Process for New bot - 1 Process Table`](process-tables/Process_for_New_bot_1_Process_Table.md) | bot | 30 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/175…` |
| 47 | [`New step Output 3`](process-tables/New_step_Output_3.md) | bot | 29 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/175…` |
| 48 | [`Process for Update ScanStatus เมื่อสแกน Invoice - 1 Process Table`](process-tables/Process_for_Update_ScanStatus_เมื่อสแกน_Invoice_1_Process_Table.md) | bot | 19 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/d77…` |
| 49 | [`Update Output`](process-tables/Update_Output.md) | bot | 18 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/d77…` |
| 50 | [`Process for ปริ๊นใบวางบิล_เบทาโกร+เหมาตู้ Process Table`](process-tables/Process_for_ปริ๊นใบวางบิล_เบทาโกร_เหมาตู้_Process_Table.md) | bot | 12 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/3d9…` |
| 51 | [`Clear Output 11`](process-tables/Clear_Output_11.md) | bot | 11 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/3d9…` |
| 52 | [`Process for ปริ๊นใบวางบิล_LINEMAN (6W) (SCG Express) Process Table`](process-tables/Process_for_ปริ๊นใบวางบิล_LINEMAN_6W_SCG_Express_Process_Table.md) | bot | 12 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/f99…` |
| 53 | [`Clear Output 12`](process-tables/Clear_Output_12.md) | bot | 11 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/f99…` |
| 54 | [`Process for ปริ๊นใบวางบิล_Thai paper (SCG Express) - 1 Process Table`](process-tables/Process_for_ปริ๊นใบวางบิล_Thai_paper_SCG_Express_1_Process_Table.md) | bot | 12 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/e8a…` |
| 55 | [`Clear Output 13`](process-tables/Clear_Output_13.md) | bot | 11 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b-417bc046f574/e8…` |
| 56 | [`Process for ปริ๊นใบวางบิล_โอนคลัง บุญถาวร เกษตร_นวมิ นทร์ - 1 Process Table`](process-tables/Process_for_ปริ๊นใบวางบิล_โอนคลัง_บุญถาวร_เกษตร_นวมิ_นทร์_1_Process_Table.md) | bot | 12 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/be0…` |
| 57 | [`Clear Output 14`](process-tables/Clear_Output_14.md) | bot | 11 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b-417bc046f574/be…` |
| 58 | [`Process for Bot_เบิกค่าขนส่งตามระยะทาง - 1 Process Table`](process-tables/Process_for_Bot_เบิกค่าขนส่งตามระยะทาง_1_Process_Table.md) | bot | 139 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/546…` |
| 59 | [`เบิกตามระยะทาง Output`](process-tables/เบิกตามระยะทาง_Output.md) | bot | 2 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/546…` |
| 60 | [`New step4 Output`](process-tables/New_step4_Output.md) | bot | 136 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/546…` |
| 61 | [`New step3 Output`](process-tables/New_step3_Output.md) | bot | 136 | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/546…` |
