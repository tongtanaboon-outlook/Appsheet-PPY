# Price_Table

<!-- table: Price_Table -->

> **ตารางธุรกิจ** — มีข้อมูลจริงอยู่ใน Google Sheet `Price_Table`

| คุณสมบัติ | ค่า |
|---|---|
| ชนิดตาราง | ตารางจริง (business) |
| ที่มาข้อมูล | `google` |
| จำนวนคอลัมน์ | 8 |
| Key | `ID_Price Table` |
| คอลัมน์คำนวณอัตโนมัติ | 1 |
| เห็นใน UI | `ALWAYS` |
| สิทธิ์แก้ไข | `ALL_CHANGES` |

## คอลัมน์ทั้งหมด

| # | ชื่อคอลัมน์ | ประเภท | คำอธิบาย | สูตร / ค่าเริ่มต้น | Key | Ref ไปยัง |
|---:|---|---|---|---|:---:|---|
| 1 | `_RowNumber` | Number | คอลัมน์ตัวเลข — ซ่อนใน UI | — |  | — |
| 2 | `ชื่องาน` | Text | คอลัมน์ข้อความ | — |  | — |
| 3 | `ID_Price Table` | Text | คอลัมน์ข้อความ — **Key ของแถว**; มีค่าเริ่มต้นเมื่อสร้างแถว | `UNIQUEID()` | ✅ | — |
| 4 | `เรทน้ำมัน_Minimum` | Decimal | คอลัมน์ทศนิยม | — |  | — |
| 5 | `เรทน้ำมัน_Maximum` | Decimal | คอลัมน์ทศนิยม | — |  | — |
| 6 | `ระยะทาง_Minimum` | Number | คอลัมน์ตัวเลข | — |  | — |
| 7 | `ระยะทาง_Maximum` | Number | คอลัมน์ตัวเลข | — |  | — |
| 8 | `Price` | Decimal | คอลัมน์ทศนิยม | — |  | — |

<!-- col: Price_Table :: _RowNumber -->
<!-- col: Price_Table :: ชื่องาน -->
<!-- col: Price_Table :: ID_Price Table -->
<!-- col: Price_Table :: เรทน้ำมัน_Minimum -->
<!-- col: Price_Table :: เรทน้ำมัน_Maximum -->
<!-- col: Price_Table :: ระยะทาง_Minimum -->
<!-- col: Price_Table :: ระยะทาง_Maximum -->
<!-- col: Price_Table :: Price -->

## สูตรในตารางนี้

### ID_Price Table

<!-- formula: Price_Table :: ID_Price Table -->

**ค่าเริ่มต้น**

```
UNIQUEID()
```

- **Reset_If**: `No`

## ความสัมพันธ์

- ไม่มีคอลัมน์ Ref ที่ชี้ออกไปยังตารางอื่น

- ไม่มีตารางอื่นอ้างอิงกลับมา
