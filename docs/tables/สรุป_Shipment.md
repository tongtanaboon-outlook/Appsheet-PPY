# สรุป_Shipment

<!-- table: สรุป_Shipment -->

> **ตารางธุรกิจ** — มีข้อมูลจริงอยู่ใน Google Sheet `สรุป_Shipment`

| คุณสมบัติ | ค่า |
|---|---|
| ชนิดตาราง | ตารางจริง (business) |
| ที่มาข้อมูล | `google` |
| จำนวนคอลัมน์ | 14 |
| Key | `ShipmentKey` |
| คอลัมน์คำนวณอัตโนมัติ | 6 |
| เห็นใน UI | `ALWAYS` |
| สิทธิ์แก้ไข | `ALL_CHANGES` |

## คอลัมน์ทั้งหมด

| # | ชื่อคอลัมน์ | ประเภท | คำอธิบาย | สูตร / ค่าเริ่มต้น | Key | Ref ไปยัง |
|---:|---|---|---|---|:---:|---|
| 1 | `_RowNumber` | Number | คอลัมน์ตัวเลข — ซ่อนใน UI | — |  | — |
| 2 | `ShipmentKey` | Text | คอลัมน์ข้อความ — **Key ของแถว** | — | ✅ | — |
| 3 | `ShipmentNo` | Number | คอลัมน์ตัวเลข | — |  | — |
| 4 | `TruckLicense` | Text | คอลัมน์ข้อความ | — |  | — |
| 5 | `PlanDelivery` | Date | คอลัมน์วันที่ | — |  | — |
| 6 | `จำนวน_ทั้งหมด` | Number | คอลัมน์ตัวเลข | — |  | — |
| 7 | `จำนวน_E-POD_ทั้งหมด` | Number | คอลัมน์ตัวเลข | — |  | — |
| 8 | `LastUpdated` | DateTime | คอลัมน์วันที่และเวลา | — |  | — |
| 9 | `รายการ_ทั้งหมด` | List | คอลัมน์รายการอ้างอิง — คำนวณอัตโนมัติ | `=FILTER( "ตารางงานประจำวัน", [Shipment No] = [_THISROW]. [ShipmentNo] )` |  | — |
| 10 | `รายการ_สแกนแล้ว` | List | คอลัมน์รายการอ้างอิง — คำนวณอัตโนมัติ | `=FILTER( "ตารางงานประจำวัน", AND( [Shipment No] = [_THISROW].[ShipmentNo], [ScanStatus] = "สแกนรับแล้ว" ) )` |  | — |
| 11 | `รายการ_รอสแกน` | List | คอลัมน์รายการอ้างอิง — คำนวณอัตโนมัติ | `=FILTER( "ตารางงานประจำวัน", AND( [Shipment No] = [_THISROW].[ShipmentNo], OR( ISBLANK([ScanStatus]), [ScanSt…` |  | — |
| 12 | `จำนวน_สแกนแล้ว` | Number | คอลัมน์ตัวเลข — คำนวณอัตโนมัติ | `=COUNT( UNIQUE( SELECT( ตารางงานประจำวัน[Invoice No], AND( [Shipment No] = [_THISROW].[ShipmentNo], [ScanStat…` |  | — |
| 13 | `จำนวน_รอสแกน` | Number | คอลัมน์ตัวเลข — คำนวณอัตโนมัติ | `=[จำนวน_ทั้งหมด] - [จำนวน_สแกนแล้ว]` |  | — |
| 14 | `สรุปยอด` | Text | คอลัมน์ข้อความ — คำนวณอัตโนมัติ; ซ่อนใน UI | `=" "&[จำนวน_ทั้งหมด] &" "&[จำนวน_สแกนแล้ว] &" "&` |  | — |

<!-- col: สรุป_Shipment :: _RowNumber -->
<!-- col: สรุป_Shipment :: ShipmentKey -->
<!-- col: สรุป_Shipment :: ShipmentNo -->
<!-- col: สรุป_Shipment :: TruckLicense -->
<!-- col: สรุป_Shipment :: PlanDelivery -->
<!-- col: สรุป_Shipment :: จำนวน_ทั้งหมด -->
<!-- col: สรุป_Shipment :: จำนวน_E-POD_ทั้งหมด -->
<!-- col: สรุป_Shipment :: LastUpdated -->
<!-- col: สรุป_Shipment :: รายการ_ทั้งหมด -->
<!-- col: สรุป_Shipment :: รายการ_สแกนแล้ว -->
<!-- col: สรุป_Shipment :: รายการ_รอสแกน -->
<!-- col: สรุป_Shipment :: จำนวน_สแกนแล้ว -->
<!-- col: สรุป_Shipment :: จำนวน_รอสแกน -->
<!-- col: สรุป_Shipment :: สรุปยอด -->

## สูตรในตารางนี้

### รายการ_ทั้งหมด

<!-- formula: สรุป_Shipment :: รายการ_ทั้งหมด -->

**App formula**

```
=FILTER( "ตารางงานประจำวัน", [Shipment No] = [_THISROW]. [ShipmentNo] )
```

- **Reset_If**: `No`

### รายการ_สแกนแล้ว

<!-- formula: สรุป_Shipment :: รายการ_สแกนแล้ว -->

**App formula**

```
=FILTER( "ตารางงานประจำวัน", AND( [Shipment No] = [_THISROW].[ShipmentNo], [ScanStatus] = "สแกนรับแล้ว" ) )
```

- **Reset_If**: `No`

### รายการ_รอสแกน

<!-- formula: สรุป_Shipment :: รายการ_รอสแกน -->

**App formula**

```
=FILTER( "ตารางงานประจำวัน", AND( [Shipment No] = [_THISROW].[ShipmentNo], OR( ISBLANK([ScanStatus]), [ScanStatus] <> "สแกนรับแล้ว" ) ) )
```

- **Reset_If**: `No`

### จำนวน_สแกนแล้ว

<!-- formula: สรุป_Shipment :: จำนวน_สแกนแล้ว -->

**App formula**

```
=COUNT( UNIQUE( SELECT( ตารางงานประจำวัน[Invoice No], AND( [Shipment No] = [_THISROW].[ShipmentNo], [ScanStatus] = "สแกนรับแล้ว" ) ) ) )
```

- **Reset_If**: `No`

### จำนวน_รอสแกน

<!-- formula: สรุป_Shipment :: จำนวน_รอสแกน -->

**App formula**

```
=[จำนวน_ทั้งหมด] - [จำนวน_สแกนแล้ว]
```

- **Reset_If**: `No`

### สรุปยอด

<!-- formula: สรุป_Shipment :: สรุปยอด -->

**App formula**

```
=" "&[จำนวน_ทั้งหมด] &" "&[จำนวน_สแกนแล้ว] &" "&
```

- **Reset_If**: `0`

## ความสัมพันธ์

- ไม่มีคอลัมน์ Ref ที่ชี้ออกไปยังตารางอื่น

- ไม่มีตารางอื่นอ้างอิงกลับมา
