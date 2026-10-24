# Process for New bot - 1 Process Table

<!-- table: Process for New bot - 1 Process Table -->
<!-- bot: Process for New bot - 1 Process Table -->

> **ตารางของระบบอัตโนมัติ (bot)** — ไม่ใช่ข้อมูลธุรกิจ

| คุณสมบัติ | ค่า |
|---|---|
| ชนิด | bot |
| ที่มาข้อมูล | `native` |
| source_path | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/175bb876-5ac2-498d-858713e27591d256/State Table` |
| จำนวนคอลัมน์ | 30 |
| เห็นใน UI | `NEVER` |

## คอลัมน์ทั้งหมด

| # | ชื่อคอลัมน์ | ประเภท | คำอธิบาย | สูตร / ค่าเริ่มต้น | Key |
|---:|---|---|---|---|:---:|
| 1 | `Instance Id` | Text | คอลัมน์ข้อความ — **Key ของแถว** | — | ✅ |
| 2 | `ID_แจ้งปั ญหาระหว่างวัน` | Text | คอลัมน์ข้อความ | — |  |
| 3 | `กดปุ่ มนี้เพื่อส่งข้อมูลแจ้งปั ญหา` | Yes/No | คอลัมน์ใช่/ไม่ใช่ — ตรวจความถูกต้องตามเงื่อนไข; แสดงผลตามเงื่อนไข | — |  |
| 4 | `ข้อมูลการแจ้งปั ญหา` | Enum | คอลัมน์ตัวเลือกเดียว | — |  |
| 5 | `รูป1` | Image | คอลัมน์รูปภาพ | — |  |
| 6 | `รูป2` | Image | คอลัมน์รูปภาพ | — |  |
| 7 | `รูป3` | Image | คอลัมน์รูปภาพ | — |  |
| 8 | `หมายเหตุ` | LongText | คอลัมน์ข้อความยาว | — |  |
| 9 | `วันที่+เวลา` | DateTime | คอลัมน์วันที่และเวลา — แก้ไขได้ตามเงื่อนไข | — |  |
| 10 | `ชื่อ - นามสกุล` | Text | คอลัมน์ข้อความ | — |  |
| 11 | `ทะเบียนรถ` | Text | คอลัมน์ข้อความ | — |  |
| 12 | `รหัสผู้รับเหมา` | Text | คอลัมน์ข้อความ — แสดงผลตามเงื่อนไข | — |  |
| 13 | `ชื่อผู้รับเหมา` | Text | คอลัมน์ข้อความ — แสดงผลตามเงื่อนไข | — |  |
| 14 | `Shipment No` | Number | คอลัมน์ตัวเลข — ตรวจความถูกต้องตามเงื่อนไข | — |  |
| 15 | `Invoice No` | EnumList | คอลัมน์ตัวเลือกหลาย — ตรวจความถูกต้องตามเงื่อนไข | — |  |
| 16 | `รหัสลูกค้า` | Text | คอลัมน์ข้อความ — แสดงผลตามเงื่อนไข | — |  |
| 17 | `ชื่อปลายทาง` | Text | คอลัมน์ข้อความ — แสดงผลตามเงื่อนไข | — |  |
| 18 | `ใส่ข้อมูลการแจ้งปั ญหา เพื่อนับจุดส่งงาน` | LongText | คอลัมน์ข้อความยาว — แสดงผลตามเงื่อนไข | — |  |
| 19 | `เพิ่มรูปแคปหน้าจอ นำกลับคืนคลัง` | Image | คอลัมน์รูปภาพ | — |  |
| 20 | `อัพเดตข้อมูลการแจ้งปั ญหา ไป ตารางส่ง งานSCG` | Yes/No | คอลัมน์ใช่/ไม่ใช่ — ตรวจความถูกต้องตามเงื่อนไข; แสดงผลตามเงื่อนไข | — |  |
| 21 | `Lat/Long` | LatLong | คอลัมน์พิกัด GPS | — |  |
| 22 | `LatLong_ตรวจสอบ` | LatLong | คอลัมน์พิกัด GPS | — |  |
| 23 | `Email พนักงาน` | Email | คอลัมน์อีเมล — แก้ไขได้ตามเงื่อนไข | — |  |
| 24 | `เดือน` | Text | คอลัมน์ข้อความ | — |  |
| 25 | `SM_Link` | Ref | คอลัมน์อ้างอิงตารางอื่น — อ้างอิง → `ตารางงานประจำวัน` (คอลัมน์เป้าหมาย: ID_งานประจำวัน) | — |  |
| 26 | `RT_Link` | Ref | คอลัมน์อ้างอิงตารางอื่น — อ้างอิง → `ข้อมูลงานRT` (คอลัมน์เป้าหมาย: ID_RT) | — |  |
| 27 | `SCGนครหลวงJWDภูมิภาค_ID` | Text | คอลัมน์ข้อความ | — |  |
| 28 | `ID_พนักงาน` | Ref | คอลัมน์อ้างอิงตารางอื่น — อ้างอิง → `ข้อมูลพนักงาน` (คอลัมน์เป้าหมาย: ID_พนักงาน); แก้ไขได้ตามเงื่อนไข; แสดงผลตามเงื่อนไข | — |  |
| 29 | `LINK_Image_แจ้งปั ญหา` | Text | คอลัมน์ข้อความ | — |  |
| 30 | `New step` | Ref | คอลัมน์อ้างอิงตารางอื่น — อ้างอิง → `New step Output 3` (คอลัมน์เป้าหมาย: InstanceId) | — |  |

<!-- col: Process for New bot - 1 Process Table :: Instance Id -->
<!-- col: Process for New bot - 1 Process Table :: ID_แจ้งปั ญหาระหว่างวัน -->
<!-- col: Process for New bot - 1 Process Table :: กดปุ่ มนี้เพื่อส่งข้อมูลแจ้งปั ญหา -->
<!-- col: Process for New bot - 1 Process Table :: ข้อมูลการแจ้งปั ญหา -->
<!-- col: Process for New bot - 1 Process Table :: รูป1 -->
<!-- col: Process for New bot - 1 Process Table :: รูป2 -->
<!-- col: Process for New bot - 1 Process Table :: รูป3 -->
<!-- col: Process for New bot - 1 Process Table :: หมายเหตุ -->
<!-- col: Process for New bot - 1 Process Table :: วันที่+เวลา -->
<!-- col: Process for New bot - 1 Process Table :: ชื่อ - นามสกุล -->
<!-- col: Process for New bot - 1 Process Table :: ทะเบียนรถ -->
<!-- col: Process for New bot - 1 Process Table :: รหัสผู้รับเหมา -->
<!-- col: Process for New bot - 1 Process Table :: ชื่อผู้รับเหมา -->
<!-- col: Process for New bot - 1 Process Table :: Shipment No -->
<!-- col: Process for New bot - 1 Process Table :: Invoice No -->
<!-- col: Process for New bot - 1 Process Table :: รหัสลูกค้า -->
<!-- col: Process for New bot - 1 Process Table :: ชื่อปลายทาง -->
<!-- col: Process for New bot - 1 Process Table :: ใส่ข้อมูลการแจ้งปั ญหา เพื่อนับจุดส่งงาน -->
<!-- col: Process for New bot - 1 Process Table :: เพิ่มรูปแคปหน้าจอ นำกลับคืนคลัง -->
<!-- col: Process for New bot - 1 Process Table :: อัพเดตข้อมูลการแจ้งปั ญหา ไป ตารางส่ง งานSCG -->
<!-- col: Process for New bot - 1 Process Table :: Lat/Long -->
<!-- col: Process for New bot - 1 Process Table :: LatLong_ตรวจสอบ -->
<!-- col: Process for New bot - 1 Process Table :: Email พนักงาน -->
<!-- col: Process for New bot - 1 Process Table :: เดือน -->
<!-- col: Process for New bot - 1 Process Table :: SM_Link -->
<!-- col: Process for New bot - 1 Process Table :: RT_Link -->
<!-- col: Process for New bot - 1 Process Table :: SCGนครหลวงJWDภูมิภาค_ID -->
<!-- col: Process for New bot - 1 Process Table :: ID_พนักงาน -->
<!-- col: Process for New bot - 1 Process Table :: LINK_Image_แจ้งปั ญหา -->
<!-- col: Process for New bot - 1 Process Table :: New step -->
