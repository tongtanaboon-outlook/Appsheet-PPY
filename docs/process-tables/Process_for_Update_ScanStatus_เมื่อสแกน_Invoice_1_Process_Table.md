# Process for Update ScanStatus เมื่อสแกน Invoice - 1 Process Table

<!-- table: Process for Update ScanStatus เมื่อสแกน Invoice - 1 Process Table -->
<!-- bot: Process for Update ScanStatus เมื่อสแกน Invoice - 1 Process Table -->

> **ตารางของระบบอัตโนมัติ (bot)** — ไม่ใช่ข้อมูลธุรกิจ

| คุณสมบัติ | ค่า |
|---|---|
| ชนิด | bot |
| ที่มาข้อมูล | `native` |
| source_path | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/d77c3cd8-7325-4d1b-8dd00a391dcc374c/State Table` |
| จำนวนคอลัมน์ | 19 |
| เห็นใน UI | `NEVER` |

## คอลัมน์ทั้งหมด

| # | ชื่อคอลัมน์ | ประเภท | คำอธิบาย | สูตร / ค่าเริ่มต้น | Key |
|---:|---|---|---|---|:---:|
| 1 | `Instance Id` | Text | คอลัมน์ข้อความ — **Key ของแถว** | — | ✅ |
| 2 | `ID_ScanDocs` | Text | คอลัมน์ข้อความ | — |  |
| 3 | `Scan_Invoice` | Text | คอลัมน์ข้อความ — ตรวจความถูกต้องตามเงื่อนไข; แสดงผลตามเงื่อนไข | — |  |
| 4 | `Select_Invoice` | Enum | คอลัมน์ตัวเลือกเดียว — ตรวจความถูกต้องตามเงื่อนไข; แสดงผลตามเงื่อนไข | — |  |
| 5 | `Scan_DateTime` | DateTime | คอลัมน์วันที่และเวลา | — |  |
| 6 | `Scan_By` | Email | คอลัมน์อีเมล | — |  |
| 7 | `Scan_Method` | Enum | คอลัมน์ตัวเลือกเดียว | — |  |
| 8 | `Invoice_No` | Ref | คอลัมน์อ้างอิงตารางอื่น — อ้างอิง → `ตารางงานประจำวัน` (คอลัมน์เป้าหมาย: ID_งานประจำวัน); ตรวจความถูกต้องตามเงื่อนไข | — |  |
| 9 | `ชื่อเจ้าของสินค้า` | Text | คอลัมน์ข้อความ | — |  |
| 10 | `ทะเบียนรถ` | Text | คอลัมน์ข้อความ | — |  |
| 11 | `Shipment No` | Text | คอลัมน์ข้อความ | — |  |
| 12 | `วันที่ส่งสินค้า` | Date | คอลัมน์วันที่ | — |  |
| 13 | `หมายเหตุการรับเอกสาร` | LongText | คอลัมน์ข้อความยาว — แสดงผลตามเงื่อนไข | — |  |
| 14 | `จำนวน_ทั้งหมด` | Number | คอลัมน์ตัวเลข | — |  |
| 15 | `จำนวน_สแกนแล้ว` | Number | คอลัมน์ตัวเลข | — |  |
| 16 | `จำนวน_รอสแกน` | Number | คอลัมน์ตัวเลข | — |  |
| 17 | `สรุปยอด` | Text | คอลัมน์ข้อความ | — |  |
| 18 | `เลือกวันที่` | Date | คอลัมน์วันที่ | — |  |
| 19 | `Update` | Ref | คอลัมน์อ้างอิงตารางอื่น — อ้างอิง → `Update Output` (คอลัมน์เป้าหมาย: InstanceId) | — |  |

<!-- col: Process for Update ScanStatus เมื่อสแกน Invoice - 1 Process Table :: Instance Id -->
<!-- col: Process for Update ScanStatus เมื่อสแกน Invoice - 1 Process Table :: ID_ScanDocs -->
<!-- col: Process for Update ScanStatus เมื่อสแกน Invoice - 1 Process Table :: Scan_Invoice -->
<!-- col: Process for Update ScanStatus เมื่อสแกน Invoice - 1 Process Table :: Select_Invoice -->
<!-- col: Process for Update ScanStatus เมื่อสแกน Invoice - 1 Process Table :: Scan_DateTime -->
<!-- col: Process for Update ScanStatus เมื่อสแกน Invoice - 1 Process Table :: Scan_By -->
<!-- col: Process for Update ScanStatus เมื่อสแกน Invoice - 1 Process Table :: Scan_Method -->
<!-- col: Process for Update ScanStatus เมื่อสแกน Invoice - 1 Process Table :: Invoice_No -->
<!-- col: Process for Update ScanStatus เมื่อสแกน Invoice - 1 Process Table :: ชื่อเจ้าของสินค้า -->
<!-- col: Process for Update ScanStatus เมื่อสแกน Invoice - 1 Process Table :: ทะเบียนรถ -->
<!-- col: Process for Update ScanStatus เมื่อสแกน Invoice - 1 Process Table :: Shipment No -->
<!-- col: Process for Update ScanStatus เมื่อสแกน Invoice - 1 Process Table :: วันที่ส่งสินค้า -->
<!-- col: Process for Update ScanStatus เมื่อสแกน Invoice - 1 Process Table :: หมายเหตุการรับเอกสาร -->
<!-- col: Process for Update ScanStatus เมื่อสแกน Invoice - 1 Process Table :: จำนวน_ทั้งหมด -->
<!-- col: Process for Update ScanStatus เมื่อสแกน Invoice - 1 Process Table :: จำนวน_สแกนแล้ว -->
<!-- col: Process for Update ScanStatus เมื่อสแกน Invoice - 1 Process Table :: จำนวน_รอสแกน -->
<!-- col: Process for Update ScanStatus เมื่อสแกน Invoice - 1 Process Table :: สรุปยอด -->
<!-- col: Process for Update ScanStatus เมื่อสแกน Invoice - 1 Process Table :: เลือกวันที่ -->
<!-- col: Process for Update ScanStatus เมื่อสแกน Invoice - 1 Process Table :: Update -->
