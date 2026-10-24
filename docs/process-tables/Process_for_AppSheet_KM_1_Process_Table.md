# Process for AppSheet_KM - 1 Process Table

<!-- table: Process for AppSheet_KM - 1 Process Table -->
<!-- bot: Process for AppSheet_KM - 1 Process Table -->

> **ตารางของระบบอัตโนมัติ (bot)** — ไม่ใช่ข้อมูลธุรกิจ

| คุณสมบัติ | ค่า |
|---|---|
| ชนิด | bot |
| ที่มาข้อมูล | `native` |
| source_path | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/261d0ba4-8cde-454c-bb42cbd0b03b5c66/State Table` |
| จำนวนคอลัมน์ | 51 |
| เห็นใน UI | `NEVER` |

## คอลัมน์ทั้งหมด

| # | ชื่อคอลัมน์ | ประเภท | คำอธิบาย | สูตร / ค่าเริ่มต้น | Key |
|---:|---|---|---|---|:---:|
| 1 | `Instance Id` | Text | คอลัมน์ข้อความ — **Key ของแถว** | — | ✅ |
| 2 | `head` | LongText | คอลัมน์ข้อความยาว | — |  |
| 3 | `ID_SCGนครหลวงJWDภูมิภาค` | Text | คอลัมน์ข้อความ | — |  |
| 4 | `วันที่ส่งสินค้า` | Date | คอลัมน์วันที่ — แก้ไขได้ตามเงื่อนไข | — |  |
| 5 | `เวลาที่ส่งสินค้า` | Time | คอลัมน์เวลา — แก้ไขได้ตามเงื่อนไข | — |  |
| 6 | `จุดส่งสินค้าปลายทาง` | LatLong | คอลัมน์พิกัด GPS — ตรวจความถูกต้องตามเงื่อนไข; แก้ไขได้ตามเงื่อนไข | — |  |
| 7 | `ชื่อ - นามสกุล` | Text | คอลัมน์ข้อความ | — |  |
| 8 | `ทะเบียนรถ` | Text | คอลัมน์ข้อความ | — |  |
| 9 | `Shipment No` | Number | คอลัมน์ตัวเลข — ตรวจความถูกต้องตามเงื่อนไข | — |  |
| 10 | `Invoice No` | EnumList | คอลัมน์ตัวเลือกหลาย — ตรวจความถูกต้องตามเงื่อนไข; แก้ไขได้ตามเงื่อนไข | — |  |
| 11 | `รูปถ่ายบิลส่งสินค้า` | Image | คอลัมน์รูปภาพ | — |  |
| 12 | `รหัสลูกค้า` | Text | คอลัมน์ข้อความ — แก้ไขได้ตามเงื่อนไข; แสดงผลตามเงื่อนไข | — |  |
| 13 | `ชื่อเจ้าของสินค้า` | Text | คอลัมน์ข้อความ — แก้ไขได้ตามเงื่อนไข; แสดงผลตามเงื่อนไข | — |  |
| 14 | `ชื่อปลายทาง` | Text | คอลัมน์ข้อความ — แก้ไขได้ตามเงื่อนไข; แสดงผลตามเงื่อนไข | — |  |
| 15 | `Email พนักงาน` | Email | คอลัมน์อีเมล — แก้ไขได้ตามเงื่อนไข | — |  |
| 16 | `LAT` | Decimal | คอลัมน์ทศนิยม | — |  |
| 17 | `LONG` | Decimal | คอลัมน์ทศนิยม | — |  |
| 18 | `ID_Doc_Return` | Ref | คอลัมน์อ้างอิงตารางอื่น — อ้างอิง → `Doc_Return` (คอลัมน์เป้าหมาย: ID_Doc_Return); แก้ไขได้ตามเงื่อนไข | — |  |
| 19 | `คลังสินค้า เอสซีจี เจดับเบิ้ลยูดี วังน้อย` | LatLong | คอลัมน์พิกัด GPS | — |  |
| 20 | `ที่อยู่ปลายทาง` | LongText | คอลัมน์ข้อความยาว — แก้ไขได้ตามเงื่อนไข; แสดงผลตามเงื่อนไข | — |  |
| 21 | `รูปสินค้าตอนส่ง` | Image | คอลัมน์รูปภาพ | — |  |
| 22 | `รูปหน้าร้าน / บ้าน` | Image | คอลัมน์รูปภาพ | — |  |
| 23 | `หมายเหตุ` | LongText | คอลัมน์ข้อความยาว — แสดงผลตามเงื่อนไข | — |  |
| 24 | `เดือน` | Text | คอลัมน์ข้อความ | — |  |
| 25 | `ระยะทางจากคลัง_Km` | Decimal | คอลัมน์ทศนิยม | — |  |
| 26 | `ชื่อที่อยู่จาก_LatLong` | LongText | คอลัมน์ข้อความยาว | — |  |
| 27 | `SM_Link_SCG` | Ref | คอลัมน์อ้างอิงตารางอื่น — อ้างอิง → `ตารางงานประจำวัน` (คอลัมน์เป้าหมาย: ID_งานประจำวัน) | — |  |
| 28 | `ID_พนักงาน` | Ref | คอลัมน์อ้างอิงตารางอื่น — อ้างอิง → `ข้อมูลพนักงาน` (คอลัมน์เป้าหมาย: ID_พนักงาน); แก้ไขได้ตามเงื่อนไข; แสดงผลตามเงื่อนไข | — |  |
| 29 | `พิกัดตอนกดบันทึกงาน` | LatLong | คอลัมน์พิกัด GPS | — |  |
| 30 | `เวลาเริ่มกรอกงาน` | Time | คอลัมน์เวลา | — |  |
| 31 | `เวลาบันทึกงานสำเร็จ` | Time | คอลัมน์เวลา | — |  |
| 32 | `ระยะขยับจากจุดเริ่มต้น_เมตร` | Decimal | คอลัมน์ทศนิยม | — |  |
| 33 | `ระยะเวลาใช้งาน_นาที` | Duration | คอลัมน์ระยะเวลา | — |  |
| 34 | `ความเร็วการเคลื่อนที่_เมตร_นาที` | Decimal | คอลัมน์ทศนิยม | — |  |
| 35 | `ผลการตรวจสอบงานส่ง` | Enum | คอลัมน์ตัวเลือกเดียว | — |  |
| 36 | `เหตุผิดปกติที่ตรวจพบ` | EnumList | คอลัมน์ตัวเลือกหลาย | — |  |
| 37 | `เวลาถ่ายรูปหน้าร้าน_หน้าบ้าน` | Time | คอลัมน์เวลา | — |  |
| 38 | `SYNC_STATUS` | Text | คอลัมน์ข้อความ | — |  |
| 39 | `MD_LINK` | Text | คอลัมน์ข้อความ | — |  |
| 40 | `MATCH_KEY` | Text | คอลัมน์ข้อความ | — |  |
| 41 | `POINTS_AT_TIME` | Number | คอลัมน์ตัวเลข | — |  |
| 42 | `STATUS` | Text | คอลัมน์ข้อความ | — |  |
| 43 | `เจ้าของสินค้า//ชื่อปลาย ทาง//Lat_Long//Inv No` | LongText | คอลัมน์ข้อความยาว | — |  |
| 44 | `Document_Return` | LongText | คอลัมน์ข้อความยาว | — |  |
| 45 | `Image_Document_Return` | List | คอลัมน์รายการอ้างอิง | — |  |
| 46 | `ที่อยู่ปลายทาง_LatLong_Api` | LatLong | คอลัมน์พิกัด GPS | — |  |
| 47 | `Related สรุปเบิกส่วนต่างs` | List | คอลัมน์รายการอ้างอิง | — |  |
| 48 | `Related ทำเบิกส่วนต่างScgวังน้อยs` | List | คอลัมน์รายการอ้างอิง | — |  |
| 49 | `พิกัดตอนกดบันทึก_เปลี่ยนแล้ว` | Yes/No | คอลัมน์ใช่/ไม่ใช่ | — |  |
| 50 | `AppSheet___KM` | Ref | คอลัมน์อ้างอิงตารางอื่น — อ้างอิง → `AppSheet___KM Output` (คอลัมน์เป้าหมาย: InstanceId) | — |  |
| 51 | `New step` | Ref | คอลัมน์อ้างอิงตารางอื่น — อ้างอิง → `New step Output 2` (คอลัมน์เป้าหมาย: InstanceId) | — |  |

<!-- col: Process for AppSheet_KM - 1 Process Table :: Instance Id -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: head -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: ID_SCGนครหลวงJWDภูมิภาค -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: วันที่ส่งสินค้า -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: เวลาที่ส่งสินค้า -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: จุดส่งสินค้าปลายทาง -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: ชื่อ - นามสกุล -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: ทะเบียนรถ -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: Shipment No -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: Invoice No -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: รูปถ่ายบิลส่งสินค้า -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: รหัสลูกค้า -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: ชื่อเจ้าของสินค้า -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: ชื่อปลายทาง -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: Email พนักงาน -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: LAT -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: LONG -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: ID_Doc_Return -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: คลังสินค้า เอสซีจี เจดับเบิ้ลยูดี วังน้อย -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: ที่อยู่ปลายทาง -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: รูปสินค้าตอนส่ง -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: รูปหน้าร้าน / บ้าน -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: หมายเหตุ -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: เดือน -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: ระยะทางจากคลัง_Km -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: ชื่อที่อยู่จาก_LatLong -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: SM_Link_SCG -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: ID_พนักงาน -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: พิกัดตอนกดบันทึกงาน -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: เวลาเริ่มกรอกงาน -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: เวลาบันทึกงานสำเร็จ -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: ระยะขยับจากจุดเริ่มต้น_เมตร -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: ระยะเวลาใช้งาน_นาที -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: ความเร็วการเคลื่อนที่_เมตร_นาที -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: ผลการตรวจสอบงานส่ง -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: เหตุผิดปกติที่ตรวจพบ -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: เวลาถ่ายรูปหน้าร้าน_หน้าบ้าน -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: SYNC_STATUS -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: MD_LINK -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: MATCH_KEY -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: POINTS_AT_TIME -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: STATUS -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: เจ้าของสินค้า//ชื่อปลาย ทาง//Lat_Long//Inv No -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: Document_Return -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: Image_Document_Return -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: ที่อยู่ปลายทาง_LatLong_Api -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: Related สรุปเบิกส่วนต่างs -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: Related ทำเบิกส่วนต่างScgวังน้อยs -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: พิกัดตอนกดบันทึก_เปลี่ยนแล้ว -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: AppSheet___KM -->
<!-- col: Process for AppSheet_KM - 1 Process Table :: New step -->
