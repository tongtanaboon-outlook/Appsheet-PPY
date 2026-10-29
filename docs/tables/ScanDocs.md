# ScanDocs

<!-- table: ScanDocs -->

> **ตารางธุรกิจ** — มีข้อมูลจริงอยู่ใน Google Sheet `ScanDocs`

| คุณสมบัติ | ค่า |
|---|---|
| ชนิดตาราง | ตารางจริง (business) |
| ที่มาข้อมูล | `google` |
| จำนวนคอลัมน์ | 18 |
| Key | `ID_ScanDocs` |
| คอลัมน์คำนวณอัตโนมัติ | 14 |
| เห็นใน UI | `ALWAYS` |
| สิทธิ์แก้ไข | `ALL_CHANGES` |

> ⚠️ **ต้องตรวจสูตรในแอป**: คอลัมน์นี้มีค่าที่ PDF วาดทับกับตารางคุณสมบัติ ของคอลัมน์เอง ทำให้สูตรที่คัดลอกมาอาจไม่ครบ — `สรุปยอด` (ดูคอลัมน์ `needs_review` ใน `app/columns.csv`)

## คอลัมน์ทั้งหมด

| # | ชื่อคอลัมน์ | ประเภท | คำอธิบาย | สูตร / ค่าเริ่มต้น | Key | Ref ไปยัง |
|---:|---|---|---|---|:---:|---|
| 1 | `_RowNumber` | Number | คอลัมน์ตัวเลข — ซ่อนใน UI | — |  | — |
| 2 | `ID_ScanDocs` | Text | คอลัมน์ข้อความ — **Key ของแถว**; มีค่าเริ่มต้นเมื่อสร้างแถว | `UNIQUEID()` | ✅ | — |
| 3 | `Scan_Invoice` | Text | คอลัมน์ข้อความ — ตรวจความถูกต้องตามเงื่อนไข; แสดงผลตามเงื่อนไข | — |  | — |
| 4 | `Select_Invoice` | Enum | คอลัมน์ตัวเลือกเดียว — ตรวจความถูกต้องตามเงื่อนไข; แสดงผลตามเงื่อนไข | — |  | — |
| 5 | `Scan_DateTime` | DateTime | คอลัมน์วันที่และเวลา — มีค่าเริ่มต้นเมื่อสร้างแถว | `=NOW()` |  | — |
| 6 | `Scan_By` | Email | คอลัมน์อีเมล — มีค่าเริ่มต้นเมื่อสร้างแถว; **ข้อมูลอ่อนไหว (PII)** | `=USEREMAIL()` |  | — |
| 7 | `Scan_Method` | Enum | คอลัมน์ตัวเลือกเดียว — มีค่าเริ่มต้นเมื่อสร้างแถว | `=IF(ISNOTBLANK([Select_Invoice]), "Manual", "Barcode")` |  | — |
| 8 | `Invoice_No` | Ref | คอลัมน์อ้างอิงตารางอื่น — อ้างอิง → `ตารางงานประจำวัน` (คอลัมน์เป้าหมาย: ID_งานประจำวัน); คำนวณอัตโนมัติ; ตรวจความถูกต้องตามเงื่อนไข | `=ANY( SELECT(ตารางงานประจำวัน[ID_งานประจำวัน], [Invoice No] = IF(ISNOTBLANK([Scan_Invoice]), [Scan_Invoice], …` |  | ตารางงานประจำวัน |
| 9 | `ชื่อเจ้าของสินค้า` | Text | คอลัมน์ข้อความ — มีค่าเริ่มต้นเมื่อสร้างแถว | `=[Invoice_No].[ชื่อเจ้าของสินค้า]` |  | — |
| 10 | `ทะเบียนรถ` | Text | คอลัมน์ข้อความ — มีค่าเริ่มต้นเมื่อสร้างแถว | `=[Invoice_No].[ทะเบียนรถ]` |  | — |
| 11 | `Shipment No` | Text | คอลัมน์ข้อความ — มีค่าเริ่มต้นเมื่อสร้างแถว | `=[Invoice_No].[Shipment No]` |  | — |
| 12 | `วันที่ส่งสินค้า` | Date | คอลัมน์วันที่ — มีค่าเริ่มต้นเมื่อสร้างแถว | `=[Invoice_No].[Plan Delivery]` |  | — |
| 13 | `หมายเหตุการรับเอกสาร` | LongText | คอลัมน์ข้อความยาว — แสดงผลตามเงื่อนไข | — |  | — |
| 14 | `จำนวน_ทั้งหมด` | Number | คอลัมน์ตัวเลข — คำนวณอัตโนมัติ | `=COUNT( UNIQUE( SELECT( ตารางงานประจำวัน[Invoice No], [Plan Delivery] = [_THISROW].[เลือกวันที่] ) ) )` |  | — |
| 15 | `จำนวน_สแกนแล้ว` | Number | คอลัมน์ตัวเลข — คำนวณอัตโนมัติ | `=COUNT( UNIQUE( SELECT( ตารางงานประจำวัน[Invoice No], AND( [Plan Delivery] = [_THISROW].[เลือกวันที่], [ScanS…` |  | — |
| 16 | `จำนวน_รอสแกน` | Number | คอลัมน์ตัวเลข — คำนวณอัตโนมัติ | `=[จำนวน_ทั้งหมด] - [จำนวน_สแกนแล้ว]` |  | — |
| 17 | `สรุปยอด` | Text | คอลัมน์ข้อความ — คำนวณอัตโนมัติ | `= " " & [จำนวน_ทั้งหมด] & " [จำนวน_รอสแกน] Yes No No 0 No No No No No Yes Yes en-GB Yes No No 📋 ✅ " & [จำนวน_…` |  | — |
| 18 | `เลือกวันที่` | Date | คอลัมน์วันที่ — คำนวณอัตโนมัติ | `=IF( TOTALHOURS(NOW() - TODAY()) >= 16, TODAY(), TODAY() 1)` |  | — |

<!-- col: ScanDocs :: _RowNumber -->
<!-- col: ScanDocs :: ID_ScanDocs -->
<!-- col: ScanDocs :: Scan_Invoice -->
<!-- col: ScanDocs :: Select_Invoice -->
<!-- col: ScanDocs :: Scan_DateTime -->
<!-- col: ScanDocs :: Scan_By -->
<!-- col: ScanDocs :: Scan_Method -->
<!-- col: ScanDocs :: Invoice_No -->
<!-- col: ScanDocs :: ชื่อเจ้าของสินค้า -->
<!-- col: ScanDocs :: ทะเบียนรถ -->
<!-- col: ScanDocs :: Shipment No -->
<!-- col: ScanDocs :: วันที่ส่งสินค้า -->
<!-- col: ScanDocs :: หมายเหตุการรับเอกสาร -->
<!-- col: ScanDocs :: จำนวน_ทั้งหมด -->
<!-- col: ScanDocs :: จำนวน_สแกนแล้ว -->
<!-- col: ScanDocs :: จำนวน_รอสแกน -->
<!-- col: ScanDocs :: สรุปยอด -->
<!-- col: ScanDocs :: เลือกวันที่ -->

## สูตรในตารางนี้

### ID_ScanDocs

<!-- formula: ScanDocs :: ID_ScanDocs -->

**ค่าเริ่มต้น**

```
UNIQUEID()
```

- **Reset_If**: `No`

### Scan_DateTime

<!-- formula: ScanDocs :: Scan_DateTime -->

**ค่าเริ่มต้น**

```
=NOW()
```

- **Reset_If**: `No`

### Scan_By

<!-- formula: ScanDocs :: Scan_By -->

**ค่าเริ่มต้น**

```
=USEREMAIL()
```

- **Reset_If**: `No`

### Scan_Method

<!-- formula: ScanDocs :: Scan_Method -->

**ค่าเริ่มต้น**

```
=IF(ISNOTBLANK([Select_Invoice]), "Manual", "Barcode")
```

- **Reset_If**: `=ISBLANK([_THIS])`
- **ค่าที่เลือกได้**: `['Barcode', 'Manual']`

### Invoice_No

<!-- formula: ScanDocs :: Invoice_No -->

**App formula**

```
=ANY( SELECT(ตารางงานประจำวัน[ID_งานประจำวัน], [Invoice No] = IF(ISNOTBLANK([Scan_Invoice]), [Scan_Invoice], [Select_Invoice]) ) )
```

- **Valid_If**: `=AND( ISNOTBLANK([_THIS]), IN( LOOKUP([_THIS], "ตารางงานประจำวัน", "ID_งานประจำวัน","Plan Delivery"), LIST(TODAY(), TODAY() - 1) ), ISBLANK( SELECT(ScanDocs[ID_ScanDocs], AND( [Invoice_No] = [_THIS], [ID_ScanDocs] <> [_THISROW].[ID_ScanDocs] ) ) ) )`
- **Reset_If**: `No`

### ชื่อเจ้าของสินค้า

<!-- formula: ScanDocs :: ชื่อเจ้าของสินค้า -->

**ค่าเริ่มต้น**

```
=[Invoice_No].[ชื่อเจ้าของสินค้า]
```

- **Reset_If**: `No`

### ทะเบียนรถ

<!-- formula: ScanDocs :: ทะเบียนรถ -->

**ค่าเริ่มต้น**

```
=[Invoice_No].[ทะเบียนรถ]
```

- **Reset_If**: `No`

### Shipment No

<!-- formula: ScanDocs :: Shipment No -->

**ค่าเริ่มต้น**

```
=[Invoice_No].[Shipment No]
```

- **Reset_If**: `No`

### วันที่ส่งสินค้า

<!-- formula: ScanDocs :: วันที่ส่งสินค้า -->

**ค่าเริ่มต้น**

```
=[Invoice_No].[Plan Delivery]
```

- **Reset_If**: `No`

### จำนวน_ทั้งหมด

<!-- formula: ScanDocs :: จำนวน_ทั้งหมด -->

**App formula**

```
=COUNT( UNIQUE( SELECT( ตารางงานประจำวัน[Invoice No], [Plan Delivery] = [_THISROW].[เลือกวันที่] ) ) )
```

- **Reset_If**: `No`

### จำนวน_สแกนแล้ว

<!-- formula: ScanDocs :: จำนวน_สแกนแล้ว -->

**App formula**

```
=COUNT( UNIQUE( SELECT( ตารางงานประจำวัน[Invoice No], AND( [Plan Delivery] = [_THISROW].[เลือกวันที่], [ScanStatus] = "สแกนรับแล้ว" ) ) ) )
```

- **Reset_If**: `No`

### จำนวน_รอสแกน

<!-- formula: ScanDocs :: จำนวน_รอสแกน -->

**App formula**

```
=[จำนวน_ทั้งหมด] - [จำนวน_สแกนแล้ว]
```

- **Reset_If**: `No`

### สรุปยอด

<!-- formula: ScanDocs :: สรุปยอด -->

**App formula**

```
= " " & [จำนวน_ทั้งหมด] & " [จำนวน_รอสแกน] Yes No No 0 No No No No No Yes Yes en-GB Yes No No 📋 ✅ " & [จำนวน_สแกนแล้ว] & " ⏳ " &
```


### เลือกวันที่

<!-- formula: ScanDocs :: เลือกวันที่ -->

**App formula**

```
=IF( TOTALHOURS(NOW() - TODAY()) >= 16, TODAY(), TODAY() 1)
```

- **Reset_If**: `No`

## ความสัมพันธ์

**อ้างอิงออกไป** (คอลัมน์ของตารางนี้ → ตารางอื่น)

- `Invoice_No` → `ตารางงานประจำวัน` (key: `ID_งานประจำวัน`)
<!-- rel: ScanDocs -> ตารางงานประจำวัน -->

- ไม่มีตารางอื่นอ้างอิงกลับมา
