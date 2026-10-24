# Process for Bot_รับสินค้าคืน - 1 Process Table

<!-- table: Process for Bot_รับสินค้าคืน - 1 Process Table -->
<!-- bot: Process for Bot_รับสินค้าคืน - 1 Process Table -->

> **ตารางของระบบอัตโนมัติ (bot)** — ไม่ใช่ข้อมูลธุรกิจ

| คุณสมบัติ | ค่า |
|---|---|
| ชนิด | bot |
| ที่มาข้อมูล | `native` |
| source_path | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/4cc2cf19-b0ad-44d8-bf1e-c82109753063/State Table` |
| จำนวนคอลัมน์ | 30 |
| เห็นใน UI | `NEVER` |

## คอลัมน์ทั้งหมด

| # | ชื่อคอลัมน์ | ประเภท | คำอธิบาย | สูตร / ค่าเริ่มต้น | Key |
|---:|---|---|---|---|:---:|
| 1 | `Instance Id` | Text | คอลัมน์ข้อความ — **Key ของแถว** | — | ✅ |
| 2 | `ID_รับงานคืนได้เงิน200` | Text | คอลัมน์ข้อความ | — |  |
| 3 | `สถานะการเข้ารับสินค้า` | Enum | คอลัมน์ตัวเลือกเดียว | — |  |
| 4 | `วันที่เข้ารับ` | Date | คอลัมน์วันที่ — แก้ไขได้ตามเงื่อนไข | — |  |
| 5 | `ชื่อ - นามสกุล` | Text | คอลัมน์ข้อความ | — |  |
| 6 | `ทะเบียนรถ` | Text | คอลัมน์ข้อความ | — |  |
| 7 | `Shipment (หลัก)` | Number | คอลัมน์ตัวเลข — ตรวจความถูกต้องตามเงื่อนไข; แสดงผลตามเงื่อนไข | — |  |
| 8 | `Shipment (รับคืน)` | Number | คอลัมน์ตัวเลข — แสดงผลตามเงื่อนไข | — |  |
| 9 | `เลขที่เอกสารรับคืน` | Text | คอลัมน์ข้อความ — ตรวจความถูกต้องตามเงื่อนไข; แสดงผลตามเงื่อนไข | — |  |
| 10 | `จำนวนสินค้า` | Number | คอลัมน์ตัวเลข — แสดงผลตามเงื่อนไข | — |  |
| 11 | `Shipment No` | Number | คอลัมน์ตัวเลข — ตรวจความถูกต้องตามเงื่อนไข; แสดงผลตามเงื่อนไข | — |  |
| 12 | `Invoice No` | EnumList | คอลัมน์ตัวเลือกหลาย — ตรวจความถูกต้องตามเงื่อนไข; แสดงผลตามเงื่อนไข | — |  |
| 13 | `ชื่อเจ้าของสินค้า` | Text | คอลัมน์ข้อความ | — |  |
| 14 | `รหัสลูกค้า` | Text | คอลัมน์ข้อความ | — |  |
| 15 | `ชื่อลูกค้าที่เข้ารับ` | Text | คอลัมน์ข้อความ | — |  |
| 16 | `รูปสินค้า` | Image | คอลัมน์รูปภาพ | — |  |
| 17 | `รูปบิลรับคืน` | Image | คอลัมน์รูปภาพ | — |  |
| 18 | `หมายเหตุ` | LongText | คอลัมน์ข้อความยาว — แสดงผลตามเงื่อนไข | — |  |
| 19 | `รูปจุดที่ส่งงาน` | Image | คอลัมน์รูปภาพ — แสดงผลตามเงื่อนไข | — |  |
| 20 | `Lat / Long` | LatLong | คอลัมน์พิกัด GPS | — |  |
| 21 | `Email พนักงาน` | Email | คอลัมน์อีเมล — แก้ไขได้ตามเงื่อนไข | — |  |
| 22 | `ราคา` | Price | คอลัมน์ราคา — แก้ไขได้ตามเงื่อนไข; แสดงผลตามเงื่อนไข | — |  |
| 23 | `สร้างPDFรับคืน` | Yes/No | คอลัมน์ใช่/ไม่ใช่ — แก้ไขได้ตามเงื่อนไข; แสดงผลตามเงื่อนไข | — |  |
| 24 | `TimeChange` | ChangeCounter | คอลัมน์ตัวนับการเปลี่ยนแปลง | — |  |
| 25 | `ตรวจสอบก่อนบันทึกข้อมูล` | Number | คอลัมน์ตัวเลข — ตรวจความถูกต้องตามเงื่อนไข | — |  |
| 26 | `เดือน` | Text | คอลัมน์ข้อความ | — |  |
| 27 | `ID_พนักงาน` | Ref | คอลัมน์อ้างอิงตารางอื่น — อ้างอิง → `ข้อมูลพนักงาน` (คอลัมน์เป้าหมาย: ID_พนักงาน); แก้ไขได้ตามเงื่อนไข; แสดงผลตามเงื่อนไข | — |  |
| 28 | `LINK_IMAGE` | Text | คอลัมน์ข้อความ | — |  |
| 29 | `รายชื่อจุดส่งในตารางงานประจำวัน` | LongText | คอลัมน์ข้อความยาว | — |  |
| 30 | `เข้ารับสินค้าคืน` | Ref | คอลัมน์อ้างอิงตารางอื่น — อ้างอิง → `เข้ารับสินค้าคืน Output` (คอลัมน์เป้าหมาย: InstanceId) | — |  |

<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: Instance Id -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: ID_รับงานคืนได้เงิน200 -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: สถานะการเข้ารับสินค้า -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: วันที่เข้ารับ -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: ชื่อ - นามสกุล -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: ทะเบียนรถ -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: Shipment (หลัก) -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: Shipment (รับคืน) -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: เลขที่เอกสารรับคืน -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: จำนวนสินค้า -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: Shipment No -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: Invoice No -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: ชื่อเจ้าของสินค้า -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: รหัสลูกค้า -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: ชื่อลูกค้าที่เข้ารับ -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: รูปสินค้า -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: รูปบิลรับคืน -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: หมายเหตุ -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: รูปจุดที่ส่งงาน -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: Lat / Long -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: Email พนักงาน -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: ราคา -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: สร้างPDFรับคืน -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: TimeChange -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: ตรวจสอบก่อนบันทึกข้อมูล -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: เดือน -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: ID_พนักงาน -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: LINK_IMAGE -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: รายชื่อจุดส่งในตารางงานประจำวัน -->
<!-- col: Process for Bot_รับสินค้าคืน - 1 Process Table :: เข้ารับสินค้าคืน -->
