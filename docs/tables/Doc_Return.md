# Doc_Return

<!-- table: Doc_Return -->

> **ตารางธุรกิจ** — มีข้อมูลจริงอยู่ใน Google Sheet `Doc_Return`

| คุณสมบัติ | ค่า |
|---|---|
| ชนิดตาราง | ตารางจริง (business) |
| ที่มาข้อมูล | `google` |
| จำนวนคอลัมน์ | 7 |
| Key | `ID_Doc_Return` |
| คอลัมน์คำนวณอัตโนมัติ | 3 |
| เห็นใน UI | `ALWAYS` |
| สิทธิ์แก้ไข | `ALL_CHANGES` |

## คอลัมน์ทั้งหมด

| # | ชื่อคอลัมน์ | ประเภท | คำอธิบาย | สูตร / ค่าเริ่มต้น | Key | Ref ไปยัง |
|---:|---|---|---|---|:---:|---|
| 1 | `_RowNumber` | Number | คอลัมน์ตัวเลข — ซ่อนใน UI | — |  | — |
| 2 | `ID_Doc_Return` | Text | คอลัมน์ข้อความ — **Key ของแถว**; มีค่าเริ่มต้นเมื่อสร้างแถว | `UNIQUEID()` | ✅ | — |
| 3 | `รหัสลูกค้า` | Text | คอลัมน์ข้อความ | — |  | — |
| 4 | `ชื่อเจ้าของสินค้า` | Text | คอลัมน์ข้อความ | — |  | — |
| 5 | `ข้อความอธิบาย_Document_Return` | LongText | คอลัมน์ข้อความยาว | — |  | — |
| 6 | `Related Image_Doc_Returns` | List | คอลัมน์รายการอ้างอิง — คำนวณอัตโนมัติ | `REF_ROWS("Image_Doc_Return", "ID_Doc_Return")` |  | — |
| 7 | `Related SCGนครหลวงJWDภูมิภาคs` | List | คอลัมน์รายการอ้างอิง — คำนวณอัตโนมัติ | `REF_ROWS("SCGนครหลวงJWDภูมิภาค", "ID_Doc_Return")` |  | — |

<!-- col: Doc_Return :: _RowNumber -->
<!-- col: Doc_Return :: ID_Doc_Return -->
<!-- col: Doc_Return :: รหัสลูกค้า -->
<!-- col: Doc_Return :: ชื่อเจ้าของสินค้า -->
<!-- col: Doc_Return :: ข้อความอธิบาย_Document_Return -->
<!-- col: Doc_Return :: Related Image_Doc_Returns -->
<!-- col: Doc_Return :: Related SCGนครหลวงJWDภูมิภาคs -->

## สูตรในตารางนี้

### ID_Doc_Return

<!-- formula: Doc_Return :: ID_Doc_Return -->

**ค่าเริ่มต้น**

```
UNIQUEID()
```

- **Reset_If**: `No`

### Related Image_Doc_Returns

<!-- formula: Doc_Return :: Related Image_Doc_Returns -->

**App formula**

```
REF_ROWS("Image_Doc_Return", "ID_Doc_Return")
```

- **Reset_If**: `No`

### Related SCGนครหลวงJWDภูมิภาคs

<!-- formula: Doc_Return :: Related SCGนครหลวงJWDภูมิภาคs -->

**App formula**

```
REF_ROWS("SCGนครหลวงJWDภูมิภาค", "ID_Doc_Return")
```

- **Reset_If**: `No`

## ความสัมพันธ์

- ไม่มีคอลัมน์ Ref ที่ชี้ออกไปยังตารางอื่น

**ถูกอ้างอิงจากตารางอื่น**

- `SCGนครหลวงJWDภูมิภาค`.`ID_Doc_Return` → `Doc_Return`
- `Image_Doc_Return`.`ID_Doc_Return` → `Doc_Return`
- `Process for AppSheet_KM - 1 Process Table`.`ID_Doc_Return` → `Doc_Return`
- `New step Output 2`.`ID_Doc_Return` → `Doc_Return`
