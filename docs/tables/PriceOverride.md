# PriceOverride

<!-- table: PriceOverride -->

> **ตารางธุรกิจ** — มีข้อมูลจริงอยู่ใน Google Sheet `PriceOverride`

| คุณสมบัติ | ค่า |
|---|---|
| ชนิดตาราง | ตารางจริง (business) |
| ที่มาข้อมูล | `google` |
| จำนวนคอลัมน์ | 7 |
| Key | `ID_PriceOverride` |
| คอลัมน์คำนวณอัตโนมัติ | 1 |
| เห็นใน UI | `ALWAYS` |
| สิทธิ์แก้ไข | `ALL_CHANGES` |

## คอลัมน์ทั้งหมด

| # | ชื่อคอลัมน์ | ประเภท | คำอธิบาย | สูตร / ค่าเริ่มต้น | Key | Ref ไปยัง |
|---:|---|---|---|---|:---:|---|
| 1 | `_RowNumber` | Number | คอลัมน์ตัวเลข — ซ่อนใน UI | — |  | — |
| 2 | `ID_PriceOverride` | Text | คอลัมน์ข้อความ — **Key ของแถว**; มีค่าเริ่มต้นเมื่อสร้างแถว | `=UNIQUEID()` | ✅ | — |
| 3 | `StartDate` | Date | คอลัมน์วันที่ | — |  | — |
| 4 | `EndDate` | Date | คอลัมน์วันที่ | — |  | — |
| 5 | `UsePriceDate` | Date | คอลัมน์วันที่ | — |  | — |
| 6 | `JobName` | Text | คอลัมน์ข้อความ — ตรวจความถูกต้องตามเงื่อนไข | — |  | — |
| 7 | `Note` | LongText | คอลัมน์ข้อความยาว | — |  | — |

<!-- col: PriceOverride :: _RowNumber -->
<!-- col: PriceOverride :: ID_PriceOverride -->
<!-- col: PriceOverride :: StartDate -->
<!-- col: PriceOverride :: EndDate -->
<!-- col: PriceOverride :: UsePriceDate -->
<!-- col: PriceOverride :: JobName -->
<!-- col: PriceOverride :: Note -->

## สูตรในตารางนี้

### ID_PriceOverride

<!-- formula: PriceOverride :: ID_PriceOverride -->

**ค่าเริ่มต้น**

```
=UNIQUEID()
```

- **Reset_If**: `No`

## ความสัมพันธ์

- ไม่มีคอลัมน์ Ref ที่ชี้ออกไปยังตารางอื่น

- ไม่มีตารางอื่นอ้างอิงกลับมา
