# 04 - Views / Actions / Format Rules / Slices

ชั้น UX ของแอป - กำหนดว่า *ผู้ใช้เห็นอะไร กดอะไรได้ และข้อมูลถูกเน้น/เปลี่ยนสีอย่างไร*

* **Views** 115 - **Actions** 214 - **Format Rules** 11 - **Slices** 8

## Format Rules (11 รายการ)

กติกาที่เปลี่ยนสี/ตัวหนา/ไอคอนตามเงื่อนไข - **สีและสถานะใน UI ไม่ใช่ข้อมูลดิบ**

| # | กติกา | ใช้กับข้อมูล | เงื่อนไข | รูปแบบ |
|---:|---|---|---|---|
| 1 | [`อนุมัติ`](rules/อนุมัติ.md) | `ข้อมูลการวางบิล` | `=[สถานะการอนุมัติ] = "อนุมัติ"` | `{"textColor":"green","highlightColor":"green","textSize":1.1,"underline":false,"strikethr…` |
| 2 | [`รอการอนุมัติ`](rules/รอการอนุมัติ.md) | `ข้อมูลการวางบิล` | `=[สถานะการอนุมัติ] = "รอการอนุมัติ"` | `{"textColor":"orange","highlightColor":"orange","textSize":1.1,"underline":false,"striket…` |
| 3 | [`แจ้งเตือนราคาหลังวิ่งงาน`](rules/แจ้งเตือนราคาหลังวิ่งงาน.md) | `ข้อมูลการวางบิล` | `=AND( [ราคาในระบบหลังส่งสินค้า] <> [ราคา], OR( [ชื่องาน] = "นครหลวง", [ชื่องาน] = "โอนคลัง พว", [ชื่องาน] = "โอนคลัง นำ…` | `{"textColor":"red","highlightColor":"red","textSize":1.0,"underline":false,"strikethrough…` |
| 4 | [`แจ้งเตือนเช็คราคาแล้วปกติ`](rules/แจ้งเตือนเช็คราคาแล้วปกติ.md) | `ข้อมูลการวางบิล` | `=IF([ราคาในระบบหลังส่งสินค้า] = [ราคา], TRUE, FALSE)` | `{"textColor":"green","highlightColor":"green","textSize":1.2,"underline":false,"strikethr…` |
| 5 | [`ทำเบิกได้`](rules/ทำเบิกได้.md) | `ทำเบิกส่วนต่างScgวังน้อย` | `=[ขออนุมัติเบิกค่าขนส่งส่วนเพิ่ม] >0` | `{"textColor":"green","highlightColor":"green","textSize":1.0,"underline":false,"strikethr…` |
| 6 | [`ทำเบิกไม่ได้`](rules/ทำเบิกไม่ได้.md) | `ทำเบิกส่วนต่างScgวังน้อย` | `=[ขออนุมัติเบิกค่าขนส่งส่วนเพิ่ม] < 0` | `{"textColor":"red","highlightColor":"red","textSize":1.0,"underline":false,"strikethrough…` |
| 7 | [`เตือนตรวจสอบ RW`](rules/เตือนตรวจสอบ_RW.md) | `SCGนครหลวงJWDภูมิภาค` | `=IN([Invoice No],ข้อมูลงานRW[เลขที่เอกสาร])` | `{"textColor":"red","highlightColor":"red","textSize":1.3,"underline":false,"strikethrough…` |
| 8 | [`Green_Done`](rules/Green_Done.md) | `ตารางงานประจำวัน` | `=[ScanStatus] = "สแกนแล้ว"` | `{"textColor":"green","highlightColor":"green","textSize":1.0,"underline":false,"strikethr…` |
| 9 | [`ผลการตรวจสอบงานส่ง_FAIL`](rules/ผลการตรวจสอบงานส่ง_FAIL.md) | `SCGนครหลวงJWDภูมิภาค` | `=[ผลการตรวจสอบงานส่ง] = "FAIL"` | `{"textColor":"primaryText","highlightColor":"red","textSize":1.0,"underline":false,"strik…` |
| 10 | [`สแกนรับแล้ว`](rules/สแกนรับแล้ว.md) | `ตารางงานประจำวัน` | `=[ScanStatus] = "สแกนรับแล้ว"` | `{"textColor":"green","highlightColor":"green","textSize":1.0,"underline":false,"strikethr…` |
| 11 | [`รอสแกน`](rules/รอสแกน.md) | `ตารางงานประจำวัน` | `=[ScanStatus] <> "สแกนรับแล้ว"` | `{"textColor":"red","highlightColor":"red","textSize":1.0,"underline":false,"strikethrough…` |

## Actions (214 รายการ) แยกตามชนิดคำสั่ง

| `do_this` | จำนวน | ความหมาย |
|---|---:|---|
| `SET_COLUMN_VALUE` | 49 | ตั้งค่าคอลัมน์ในแถว (เช่น ปุ่มอนุมัติ) |
| `ADD_RECORD` | 29 | เพิ่มแถวใหม่ |
| `EDIT_RECORD` | 29 | เปิดฟอร์มแก้ไข |
| `DELETE_RECORD` | 29 | ลบแถว |
| `NAVIGATE_APP` | 29 | เปิดหน้าจอ/แอปอื่น |
| `EXPORT_VIEW` | 21 | export CSV/XLSX |
| `EMAIL` | 12 | ส่งอีเมล |
| `REF_ACTION` | 4 | เปิดรายการที่อ้างอิง |
| `COMPOSITE` | 3 | รวมหลายคำสั่ง |
| `NAVIGATE_DIFFERENT_APP` | 3 | ข้ามไปแอปอื่น |
| `NAVIGATE_URL` | 3 | เปิด URL ภายนอก |
| `CALL` | 1 | โทรหา |
| `SMS` | 1 | ส่ง SMS |
| `ADD_RECORD_TO` | 1 | เพิ่มแถวลงอีกตาราง |

### Action ที่แก้ไขข้อมูล (modifies data)

| action | ชนิด | ตารางเป้าหมาย | คอลัมน์ |
|---|---|---|---|
| `Add` | `ADD_RECORD` | `SCGนครหลวงJWDภูมิภาค` | `` |
| `Add` | `ADD_RECORD` | `ข้อมูลการเข้าบำรุงรักษา` | `` |
| `Add` | `ADD_RECORD` | `ข้อมูลการวางบิล` | `` |
| `อนุมัติ` | `SET_COLUMN_VALUE` | `ข้อมูลการวางบิล` | `สถานะการอนุมัติ` |
| `รอการอนุมัติ` | `SET_COLUMN_VALUE` | `ข้อมูลการวางบิล` | `สถานะการอนุมัติ` |
| `Edit` | `EDIT_RECORD` | `ข้อมูลการวางบิล` | `` |
| `Edit` | `EDIT_RECORD` | `ปริ๊นใบวางบิล` | `` |
| `Edit` | `EDIT_RECORD` | `PDFพนักงาน` | `` |
| `Add` | `ADD_RECORD` | `ปริ๊นใบวางบิล` | `` |
| `Add` | `ADD_RECORD` | `PDFพนักงาน` | `` |
| `Clear` | `SET_COLUMN_VALUE` | `ปริ๊นใบวางบิล` | `ชื่องาน` |
| `CLEAR 2` | `SET_COLUMN_VALUE` | `PDFพนักงาน` | `ชื่อ - นามสกุล` |
| `Edit` | `EDIT_RECORD` | `SCGนครหลวงJWDภูมิภาค` | `` |
| `Edit` | `EDIT_RECORD` | `แจ้งปั ญหาระหว่างวัน` | `` |
| `Add` | `ADD_RECORD` | `แจ้งปั ญหาระหว่างวัน` | `` |
| `Add` | `ADD_RECORD` | `ราคาน้ำมันดีเซล` | `` |
| `Delete` | `DELETE_RECORD` | `ข้อมูลพนักงาน` | `` |
| `Edit` | `EDIT_RECORD` | `ข้อมูลพนักงาน` | `` |
| `Add` | `ADD_RECORD` | `ข้อมูลพนักงาน` | `` |
| `Add` | `ADD_RECORD` | `ข้อมูลชื่องานต้นทางปลายทาง` | `` |
| `Add` | `ADD_RECORD` | `รับงานคืนได้เงิน200` | `` |
| `Delete` | `DELETE_RECORD` | `ข้อมูลชื่องานต้นทางปลายทาง` | `` |
| `Edit` | `EDIT_RECORD` | `ข้อมูลชื่องานต้นทางปลายทาง` | `` |
| `Delete` | `DELETE_RECORD` | `ข้อมูลงานRT` | `` |
| `Edit` | `EDIT_RECORD` | `ข้อมูลงานRT` | `` |
| `Add` | `ADD_RECORD` | `ข้อมูลงานRT` | `` |
| `Delete` | `DELETE_RECORD` | `ตารางงานประจำวัน` | `` |
| `Edit` | `EDIT_RECORD` | `ตารางงานประจำวัน` | `` |
| `Delete` | `DELETE_RECORD` | `ราคาน้ำมันดีเซล` | `` |
| `Edit` | `EDIT_RECORD` | `ราคาน้ำมันดีเซล` | `` |
| `Delete` | `DELETE_RECORD` | `ราคาในระบบก่อนส่งสินค้า` | `` |
| `Edit` | `EDIT_RECORD` | `ราคาในระบบก่อนส่งสินค้า` | `` |
| `Delete` | `DELETE_RECORD` | `หน้าหลัก` | `` |
| `Edit` | `EDIT_RECORD` | `หน้าหลัก` | `` |
| `Delete` | `DELETE_RECORD` | `ปริ๊นใบวางบิล` | `` |
| `Delete` | `DELETE_RECORD` | `PDFพนักงาน` | `` |
| `Add` | `ADD_RECORD` | `ตารางงานประจำวัน` | `` |
| `Add` | `ADD_RECORD` | `ราคาในระบบก่อนส่งสินค้า` | `` |
| `Add` | `ADD_RECORD` | `หน้าหลัก` | `` |
| `Delete` | `DELETE_RECORD` | `ข้อมูลการวางบิล` | `` |
| `Delete` | `DELETE_RECORD` | `SCGนครหลวงJWDภูมิภาค` | `` |
| `Delete` | `DELETE_RECORD` | `ข้อมูลการเข้าบำรุงรักษา` | `` |
| `Edit` | `EDIT_RECORD` | `ข้อมูลการเข้าบำรุงรักษา` | `` |
| `Delete` | `DELETE_RECORD` | `แจ้งปั ญหาระหว่างวัน` | `` |
| `Delete` | `DELETE_RECORD` | `รับงานคืนได้เงิน200` | `` |
| `Edit` | `EDIT_RECORD` | `รับงานคืนได้เงิน200` | `` |
| `สร้างใบป่ ะหน้า_สำเริง แก้วกามเกตุ` | `SET_COLUMN_VALUE` | `PDFพนักงาน` | `ชื่อ - นามสกุล` |
| `สร้างใบป่ ะหน้าทุกคน` | `COMPOSITE` | `PDFพนักงาน` | `` |
| `Clearหน้าจอ` | `SET_COLUMN_VALUE` | `PDFพนักงาน` | `ชื่อ - นามสกุล` |
| `สร้างใบป่ ะหน้า_สุทิศ นันพนัก` | `SET_COLUMN_VALUE` | `PDFพนักงาน` | `ชื่อ - นามสกุล` |
| `สร้างใบป่ ะหน้า_เอกรัฐ อนุรักษ์` | `SET_COLUMN_VALUE` | `PDFพนักงาน` | `ชื่อ - นามสกุล` |
| `สร้างใบป่ ะหน้า_สุด พันพม่า` | `SET_COLUMN_VALUE` | `PDFพนักงาน` | `ชื่อ - นามสกุล` |
| `สร้างใบป่ ะหน้า_ธวัชชัย หนูมา` | `SET_COLUMN_VALUE` | `PDFพนักงาน` | `ชื่อ - นามสกุล` |
| `สร้างใบป่ ะหน้า_ปราโมทย์ เรียนพิษ` | `SET_COLUMN_VALUE` | `PDFพนักงาน` | `ชื่อ - นามสกุล` |
| `สร้างใบป่ ะหน้า_กฤษฎา พิญญะดำ` | `SET_COLUMN_VALUE` | `PDFพนักงาน` | `ชื่อ - นามสกุล` |
| `สร้างใบป่ ะหน้า_กิตติพงษ์ แหลมผักแว่น` | `SET_COLUMN_VALUE` | `PDFพนักงาน` | `ชื่อ - นามสกุล` |
| `สร้างใบป่ ะหน้า_จักรภัทร วงทอง` | `SET_COLUMN_VALUE` | `PDFพนักงาน` | `ชื่อ - นามสกุล` |
| `สร้างใบป่ ะหน้า_พีระพล รูปแก้ว` | `SET_COLUMN_VALUE` | `PDFพนักงาน` | `ชื่อ - นามสกุล` |
| `สร้างใบป่ ะหน้า_อชิตพล ยังยิ้ม` | `SET_COLUMN_VALUE` | `PDFพนักงาน` | `ชื่อ - นามสกุล` |
| `สร้างใบป่ ะหน้า_ธีรยุทธ นราทอง` | `SET_COLUMN_VALUE` | `PDFพนักงาน` | `ชื่อ - นามสกุล` |
| `สร้างใบป่ ะหน้า_จิรายุ โคตรวงษ์` | `SET_COLUMN_VALUE` | `PDFพนักงาน` | `ชื่อ - นามสกุล` |
| `สร้างใบป่ ะหน้า_ทัดเทพ พรมมา` | `SET_COLUMN_VALUE` | `PDFพนักงาน` | `ชื่อ - นามสกุล` |
| `Delete` | `DELETE_RECORD` | `FILTER` | `` |
| `Edit` | `EDIT_RECORD` | `FILTER` | `` |
| `Add` | `ADD_RECORD` | `FILTER` | `` |
| `cLeAR_รับคืน` | `SET_COLUMN_VALUE` | `FILTER` | `STARTDATE` |
| `Delete` | `DELETE_RECORD` | `Price_Table` | `` |
| `Edit` | `EDIT_RECORD` | `Price_Table` | `` |
| `Add` | `ADD_RECORD` | `Price_Table` | `` |
| `สร้างใบป่ ะหน้า_พงศธร หมวดไธสง` | `SET_COLUMN_VALUE` | `PDFพนักงาน` | `ชื่อ - นามสกุล` |
| `สร้างใบป่ ะหน้า_เกียรติศักดิ์ พินิจเมือง` | `SET_COLUMN_VALUE` | `PDFพนักงาน` | `ชื่อ - นามสกุล` |
| `Delete` | `DELETE_RECORD` | `สรุปเบิกส่วนต่าง` | `` |
| `Edit` | `EDIT_RECORD` | `สรุปเบิกส่วนต่าง` | `` |
| `Add` | `ADD_RECORD` | `สรุปเบิกส่วนต่าง` | `` |
| `Clearหน้าจอสรุปส่วนต่าง` | `SET_COLUMN_VALUE` | `สรุปเบิกส่วนต่าง` | `วันที่เริ่มต้น` |
| `Delete` | `DELETE_RECORD` | `Doc_Return` | `` |
| `Edit` | `EDIT_RECORD` | `Doc_Return` | `` |
| `Delete` | `DELETE_RECORD` | `Image_Doc_Return` | `` |
| `Edit` | `EDIT_RECORD` | `Image_Doc_Return` | `` |
| `Add` | `ADD_RECORD` | `Doc_Return` | `` |
| `Add` | `ADD_RECORD` | `Image_Doc_Return` | `` |
| `สร้างใบป่ ะหน้า_เกียรติศักดิ์ ยอมใหญ่` | `SET_COLUMN_VALUE` | `PDFพนักงาน` | `ชื่อ - นามสกุล` |
| `เคลียสรุปจุดส่ง Action - 1` | `SET_COLUMN_VALUE` | `FILTER` | `EXPORT TO Excel(สรุปจำนวนจุดส่งงาน)` |
| `ไอโรบอท` | `SET_COLUMN_VALUE` | `ปริ๊นใบวางบิล` | `ชื่องาน` |
| `รับเอกสาร (งานพี่เหน่ง)` | `SET_COLUMN_VALUE` | `ปริ๊นใบวางบิล` | `ชื่องาน` |
| `โอนคลัง เอเธน` | `SET_COLUMN_VALUE` | `ปริ๊นใบวางบิล` | `ชื่องาน` |
| `โอนคลัง กระสอบ2(บางบัวทอง)` | `SET_COLUMN_VALUE` | `ปริ๊นใบวางบิล` | `ชื่องาน` |
| `คลังSCGJWDวังน้อย` | `SET_COLUMN_VALUE` | `ปริ๊นใบวางบิล` | `ชื่องาน` |
| `MeSpace` | `SET_COLUMN_VALUE` | `ปริ๊นใบวางบิล` | `ชื่องาน` |
| `โอนคลัง มโนยนต์ (นวนคร)` | `SET_COLUMN_VALUE` | `ปริ๊นใบวางบิล` | `ชื่องาน` |
| `โอนคลัง (GQ) จีคิว` | `SET_COLUMN_VALUE` | `ปริ๊นใบวางบิล` | `ชื่องาน` |
| `ปริ๊นวางบิลทุกงาน` | `COMPOSITE` | `ปริ๊นใบวางบิล` | `` |
| `เคลียหน้าจอ` | `SET_COLUMN_VALUE` | `ปริ๊นใบวางบิล` | `ชื่องาน` |
| `Delete` | `DELETE_RECORD` | `ทำเบิกส่วนต่างScgวังน้อย` | `` |
| `Edit` | `EDIT_RECORD` | `ทำเบิกส่วนต่างScgวังน้อย` | `` |
| `Add` | `ADD_RECORD` | `ทำเบิกส่วนต่างScgวังน้อย` | `` |
| `รับเอกสาร (งานพี่เหน่ง) สตีเบล` | `SET_COLUMN_VALUE` | `ปริ๊นใบวางบิล` | `ชื่องาน` |
| `CLEAR_ปริ๊นใบวางบิล_Action` | `SET_COLUMN_VALUE` | `ปริ๊นใบวางบิล` | `ชื่องาน` |
| `เพิ่มข้อมูลแจ้งปั ญหาในจุดส่งงาน` | `ADD_RECORD_TO` | `แจ้งปั ญหาระหว่างวัน` | `` |
| `อัพเดตค่าสถานะผ่านการตรวจสอบ` | `SET_COLUMN_VALUE` | `ทำเบิกส่วนต่างScgวังน้อย` | `สถานะ` |
| `อัพเดตสถานะไม่ผ่านการตรวจสอบ` | `SET_COLUMN_VALUE` | `ทำเบิกส่วนต่างScgวังน้อย` | `สถานะ` |
| `ปุ่ มเปิ ดYes 2` | `SET_COLUMN_VALUE` | `ทำเบิกส่วนต่างScgวังน้อย` | `สร้างPDFเบิกส่วนต่าง` |
| `Edit` | `EDIT_RECORD` | `ข้อมูลงานRW` | `` |
| `Add` | `ADD_RECORD` | `ข้อมูลงานRW` | `` |
| `Delete` | `DELETE_RECORD` | `สร้างเอกสาร` | `` |
| `Edit` | `EDIT_RECORD` | `สร้างเอกสาร` | `` |
| `Add` | `ADD_RECORD` | `สร้างเอกสาร` | `` |
| `Mark_As_Delivered` | `SET_COLUMN_VALUE` | `ตารางงานประจำวัน` | `DeliveryStatus` |
| `Mark_As_Delivered_not` | `SET_COLUMN_VALUE` | `ตารางงานประจำวัน` | `DeliveryStatus` |
| `ACT_Create_SCG_Flow` | `COMPOSITE` | `แจ้งปั ญหาระหว่างวัน` | `` |
| `Delete` | `DELETE_RECORD` | `ข้อมูลงานRW` | `` |
| `สร้างใบป่ ะหน้า_สิทธิชัย ทิศวงค์` | `SET_COLUMN_VALUE` | `PDFพนักงาน` | `ชื่อ - นามสกุล` |
| `Delete` | `DELETE_RECORD` | `ScanDocs` | `` |
| `Edit` | `EDIT_RECORD` | `ScanDocs` | `` |
| `Add` | `ADD_RECORD` | `ScanDocs` | `` |
| `Update ScanStatus` | `SET_COLUMN_VALUE` | `ตารางงานประจำวัน` | `ScanStatus` |
| `Delete` | `DELETE_RECORD` | `สรุป_เจ้าของสินค้า` | `` |
| `Edit` | `EDIT_RECORD` | `สรุป_เจ้าของสินค้า` | `` |
| `Add` | `ADD_RECORD` | `สรุป_เจ้าของสินค้า` | `` |
| `Delete` | `DELETE_RECORD` | `สรุป_Shipment` | `` |
| `Edit` | `EDIT_RECORD` | `สรุป_Shipment` | `` |
| `Add` | `ADD_RECORD` | `สรุป_Shipment` | `` |
| `Delete` | `DELETE_RECORD` | `PriceOverride` | `` |
| `Edit` | `EDIT_RECORD` | `PriceOverride` | `` |
| `Add` | `ADD_RECORD` | `PriceOverride` | `` |
| `เบทาโกร+เหมาตู้` | `SET_COLUMN_VALUE` | `ปริ๊นใบวางบิล` | `ชื่องาน` |
| `Thai paper (SCG Express)` | `SET_COLUMN_VALUE` | `ปริ๊นใบวางบิล` | `ชื่องาน` |
| `LINEMAN (6W) (SCG Express)` | `SET_COLUMN_VALUE` | `ปริ๊นใบวางบิล` | `ชื่องาน` |
| `โอนคลัง บุญถาวร เกษตร_นวมินทร์` | `SET_COLUMN_VALUE` | `ปริ๊นใบวางบิล` | `ชื่องาน` |
| `ปุ่ มเปิ ดYes_ราคาตามระยะทาง` | `SET_COLUMN_VALUE` | `ทำเบิกส่วนต่างScgวังน้อย` | `สร้างPDFเบิกตามระยะทาง` |
| `Delete` | `DELETE_RECORD` | `ส่งงานที่ยังไม่มีข้อมูลในระบบ` | `` |
| `Edit` | `EDIT_RECORD` | `ส่งงานที่ยังไม่มีข้อมูลในระบบ` | `` |
| `Add` | `ADD_RECORD` | `ส่งงานที่ยังไม่มีข้อมูลในระบบ` | `` |
| `Delete` | `DELETE_RECORD` | `Acknowledge_Logs` | `` |
| `Edit` | `EDIT_RECORD` | `Acknowledge_Logs` | `` |
| `Delete` | `DELETE_RECORD` | `Announcements` | `` |
| `Edit` | `EDIT_RECORD` | `Announcements` | `` |
| `Add` | `ADD_RECORD` | `Acknowledge_Logs` | `` |
| `Add` | `ADD_RECORD` | `Announcements` | `` |
| `สร้างใบป่ ะหน้า_ไนยชน วงศ์บุญมา` | `SET_COLUMN_VALUE` | `PDFพนักงาน` | `ชื่อ - นามสกุล` |

## Views (115 รายการ)

| # | ชื่อ view | ชนิด | ตำแหน่ง | เมนู |
|---:|---|---|---|---:|
| 1 | `Scan` | form | left | 1 |
| 2 | `หน้าหลัก` | gallery | right | 1 |
| 3 | `ฟอร์มรับทราบประกาศ` | form | right | 1 Show if |
| 4 | `รอการอนุมัติ` | table | right most | 1 Show if |
| 5 | `📦 สรุป_Shipment` | deck | menu | 1 |
| 6 | `📦 สรุปรับเอกสาร` | deck | menu | 1 |
| 7 | `🧾ที่สแกนรับ ✅` | table | menu | 1 |
| 8 | `Acknowledge_Logs_Table` | table | menu | 1 |
| 9 | `Document_Return` | table | menu | 1 |
| 10 | `FILTER` | detail | menu | 1 Show if |
| 11 | `Image_Document_Return` | table | menu | 1 |
| 12 | `Monitor_Dashboard` | table | menu | 1 |
| 13 | `PriceOverride` | table | menu | 1 |
| 14 | `SCGนครหลวงJWDภูมิภาค` | table | menu | 1 |
| 15 | `View ราคาไม่ตรง list` | table | menu | 1 |
| 16 | `ข้อมูลการเข้าบำรุงรักษา` | table | menu | 1 |
| 17 | `ข้อมูลการวางบิล` | table | menu | 1 Show if |
| 18 | `ข้อมูลการวางบิลแต่ละคน` | table | menu | 1 |
| 19 | `ข้อมูลงานRT` | table | menu | 1 |
| 20 | `ข้อมูลงานRW` | table | menu | 1 |
| 21 | `ข้อมูลชื่องานต้นทางปลายทาง` | table | menu | 1 |
| 22 | `ข้อมูลพนักงาน` | table | menu | 1 |
| 23 | `ค่าใช้จ่าย` | table | menu | 1 |
| 24 | `แจ้งปั ญหา` | table | menu | 1 |
| 25 | `ตารางงานประจำวัน` | table | menu | 1 |
| 26 | `ตารางราคา` | table | menu | 1 |
| 27 | `ทำเบิกส่วนต่างScgวังน้อย` | table | menu | 1 |
| 28 | `รับงานคืนได้เงิน200` | table | menu | 1 |
| 29 | `ราคาน้ำมันดีเซล` | table | menu | 1 |
| 30 | `ราคาในระบบก่อนส่งสินค้า` | table | menu | 1 |
| 31 | `สร้างรายงาน` | detail | menu | 1 Show if |
| 32 | `สร้างเอกสาร` | table | menu | 1 |
| 33 | `สรุปจำนวนจุดส่งสินค้า` | table | menu | 1 |
| 34 | `สรุปเบิกส่วนต่าง` | table | menu | 1 |
| 35 | `สรุปใบป่ ะหน้าคนขับ` | detail | menu | 1 Show if |
| 36 | `Acknowledge_Logs_Detail` | detail | ref | 1 |
| 37 | `Acknowledge_Logs_Form` | form | ref | 1 |
| 38 | `Acknowledge_Logs_Inline` | table | ref | 1 |
| 39 | `Announcements_Detail` | detail | ref | 1 |
| 40 | `Announcements_Form` | form | ref | 1 |
| 41 | `Doc_Return_Detail` | detail | ref | 1 |
| 42 | `Doc_Return_Form` | form | ref | 1 |
| 43 | `FILTER_Detail` | detail | ref | 1 |
| 44 | `FILTER_Form` | form | ref | 1 |
| 45 | `Image_Doc_Return_Detail` | detail | ref | 1 |
| 46 | `Image_Doc_Return_Form` | form | ref | 1 |
| 47 | `Image_Doc_Return_Inline` | deck | ref | 1 |
| 48 | `PDFชื่องาน_Detail` | detail | ref | 1 |
| 49 | `PDFชื่องาน_Form` | form | ref | 1 |
| 50 | `PDFพนักงาน_Detail` | detail | ref | 1 |
| 51 | `PDFพนักงาน_Form` | form | ref | 1 |
| 52 | `Price_Table_Detail` | detail | ref | 1 |
| 53 | `Price_Table_Form` | form | ref | 1 |
| 54 | `PriceOverride_Detail` | detail | ref | 1 |
| 55 | `PriceOverride_Form` | form | ref | 1 |
| 56 | `ScanDocs_Detail` | detail | ref | 1 |
| 57 | `ScanDocs_Form` | form | ref | 1 |
| 58 | `ScanDocs_Inline` | table | ref | 1 |
| 59 | `SCGนครหลวงJWDภูมิภาค_Detail` | detail | ref | 1 |
| 60 | `SCGนครหลวงJWDภูมิภาค_Form` | form | ref | 1 |
| 61 | `SCGนครหลวงJWDภูมิภาค_Inline` | table | ref | 1 |
| 62 | `Slice_Monitor_Today_Detail` | detail | ref | 1 |
| 63 | `Slice_Monitor_Today_Form` | form | ref | 1 |
| 64 | `View ราคาไม่ตรง_Detail` | detail | ref | 1 |
| 65 | `ข้อมูลการเข้าบำรุงรักษา_Detail` | detail | ref | 1 |
| 66 | `ข้อมูลการเข้าบำรุงรักษา_Form` | form | ref | 1 |
| 67 | `ข้อมูลการเข้าบำรุงรักษา_Inline` | deck | ref | 1 |
| 68 | `ข้อมูลการวางของแต่ละคน_Detail` | detail | ref | 1 |
| 69 | `ข้อมูลการวางของแต่ละคน_Form` | form | ref | 1 |
| 70 | `ข้อมูลการวางบิล_Detail` | detail | ref | 1 |
| 71 | `ข้อมูลการวางบิล_Form` | form | ref | 1 |
| 72 | `ข้อมูลการวางบิล_Inline` | deck | ref | 1 |
| 73 | `ข้อมูลงานRT_Detail` | detail | ref | 1 |
| 74 | `ข้อมูลงานRT_Form` | form | ref | 1 |
| 75 | `ข้อมูลงานRW_Detail` | detail | ref | 1 |
| 76 | `ข้อมูลงานRW_Form` | form | ref | 1 |
| 77 | `ข้อมูลชื่องานต้นทางปลายทาง_Detail` | detail | ref | 1 |
| 78 | `ข้อมูลชื่องานต้นทางปลายทาง_Form` | form | ref | 1 |
| 79 | `ข้อมูลพนักงาน_Detail` | detail | ref | 1 |
| 80 | `ข้อมูลพนักงาน_Form` | form | ref | 1 |
| 81 | `ค้างสแกนวันนี้และเมื่อวาน_Detail` | detail | ref | 1 |
| 82 | `ค้างสแกนวันนี้และเมื่อวาน_Form` | form | ref | 1 |
| 83 | `แจ้งปั ญหาระหว่างวัน_Detail` | detail | ref | 1 |
| 84 | `แจ้งปั ญหาระหว่างวัน_Form` | form | ref | 1 |
| 85 | `แจ้งปั ญหาระหว่างวัน_Inline` | deck | ref | 1 |
| 86 | `ตารางงานประจำวัน_Detail` | detail | ref | 1 |
| 87 | `ตารางงานประจำวัน_Form` | form | ref | 1 |
| 88 | `ทำเบิกส่วนต่างScgวังน้อย_Detail` | detail | ref | 1 |
| 89 | `ทำเบิกส่วนต่างScgวังน้อย_Form` | form | ref | 1 |
| 90 | `ทำเบิกส่วนต่างScgวังน้อย_Inline` | table | ref | 1 |
| 91 | `รอการอนุมัติ_Detail` | detail | ref | 1 |
| 92 | `รอการอนุมัติ_Form` | form | ref | 1 |
| 93 | `รับงานคืนได้เงิน200_Detail` | detail | ref | 1 |
| 94 | `รับงานคืนได้เงิน200_Form` | form | ref | 1 |
| 95 | `รับงานคืนได้เงิน200_Inline` | deck | ref | 1 |
| 96 | `ราคาน้ำมันดีเซล_Detail` | detail | ref | 1 |
| 97 | `ราคาน้ำมันดีเซล_Form` | form | ref | 1 |
| 98 | `ราคาในระบบก่อนส่งสินค้า_Detail` | detail | ref | 1 |
| 99 | `ราคาในระบบก่อนส่งสินค้า_Form` | form | ref | 1 |
| 100 | `ส่งงานที่ยังไม่มีข้อมูลในระบบ_Detail` | detail | ref | 1 |
| 101 | `ส่งงานที่ยังไม่มีข้อมูลในระบบ_Form` | form | ref | 1 |
| 102 | `ส่งงานที่ยังไม่มีข้อมูลในระบบ_Inline` | deck | ref | 1 |
| 103 | `สร้างเอกสาร_Detail` | detail | ref | 1 |
| 104 | `สร้างเอกสาร_Form` | form | ref | 1 |
| 105 | `สรุป_Shipment_Detail` | detail | ref | 1 |
| 106 | `สรุป_Shipment_Form` | form | ref | 1 |
| 107 | `สรุป_เจ้าของสินค้า_Detail` | detail | ref | 1 |
| 108 | `สรุป_เจ้าของสินค้า_Form` | form | ref | 1 |
| 109 | `สรุปงานประจำวัน_Detail` | detail | ref | 1 |
| 110 | `สรุปงานประจำวัน_Form` | form | ref | 1 |
| 111 | `สรุปเบิกส่วนต่าง_Detail` | detail | ref | 1 |
| 112 | `สรุปเบิกส่วนต่าง_Form` | form | ref | 1 |
| 113 | `สรุปเบิกส่วนต่าง_Inline` | table | ref | 1 |
| 114 | `หน้าหลัก_Detail` | detail | ref | 1 |
| 115 | `หน้าหลัก_Form` | form | ref | 1 |

## Slices (8 รายการ)

| # | ชื่อ slice | ตาราง | เงื่อนไขกรอง | update mode |
|---:|---|---|---|---|
| 1 | `รอการอนุมัติ` | `ข้อมูลการวางบิล` | `=USERROLE()= "ADMIN"` | `ALL_CHANGES` |
| 2 | `ข้อมูลการวางของแต่ละคน` | `ข้อมูลการวางบิล` | `=OR(USERROLE() = "ADMIN", [Email พนักงาน] = USEREMAIL())` | `ADDS_ONLY` |
| 3 | `View ราคาไม่ตรง` | `ข้อมูลการวางบิล` | `=AND( [ราคาในระบบหลังส่งสินค้า] <> [ราคา], OR( [ชื่องาน] = "นครหลวง", [ชื่องาน] = "โอนคลัง พว", [ชื่องาน] = "…` | `READ_ONLY` |
| 4 | `สรุปงานประจำวัน` | `ตารางงานประจำวัน` | `=[ลำดับแรก] = TRUE` | `ALL_CHANGES` |
| 5 | `Slice_Monitor_Today` | `ตารางงานประจำวัน` | `=[ID_งานประจำวัน] = LOOKUP( MIN( SELECT( ตารางงานประจำ วัน[_ROWNUMBER], AND( [Shipment No] = [_THISROW].[Ship…` | `ALL_CHANGES` |
| 6 | `SM_Today_User` | `ALWAYS` | `ADDS_AND_UPDATES` | `ตารางงานประจำวัน` |
| 7 | `ค้างสแกนวันนี้และเมื่อวาน` | `ตารางงานประจำวัน` | `=AND( IN([Plan Delivery], LIST(TODAY(), TODAY() - 1)), [ScanStatus] <> "สแกนรับแล้ว" )` | `ALL_CHANGES` |
| 8 | `SM_Today_User 2` | `ตารางงานประจำวัน` | `=IF(USERROLE() = "ADMIN",true, AND( [Plan Delivery] = TODAY(), [Email พนักงาน] = USEREMAIL() ) )` | `ADDS_AND_UPDATES` |
