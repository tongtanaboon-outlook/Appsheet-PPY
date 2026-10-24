# Image_Doc_Return

<!-- table: Image_Doc_Return -->

> **ตารางธุรกิจ** — มีข้อมูลจริงอยู่ใน Google Sheet `Image_Doc_Return`

| คุณสมบัติ | ค่า |
|---|---|
| ชนิดตาราง | ตารางจริง (business) |
| ที่มาข้อมูล | `google` |
| จำนวนคอลัมน์ | 4 |
| Key | `ID_Image_Doc_Return` |
| คอลัมน์คำนวณอัตโนมัติ | 1 |
| เห็นใน UI | `ALWAYS` |
| สิทธิ์แก้ไข | `ALL_CHANGES` |

## คอลัมน์ทั้งหมด

| # | ชื่อคอลัมน์ | ประเภท | คำอธิบาย | สูตร / ค่าเริ่มต้น | Key | Ref ไปยัง |
|---:|---|---|---|---|:---:|---|
| 1 | `_RowNumber` | Number | คอลัมน์ตัวเลข — ซ่อนใน UI | — |  | — |
| 2 | `ID_Image_Doc_Return` | Text | คอลัมน์ข้อความ — **Key ของแถว**; มีค่าเริ่มต้นเมื่อสร้างแถว | `=UNIQUEID()` | ✅ | — |
| 3 | `ID_Doc_Return` | Ref | คอลัมน์อ้างอิงตารางอื่น — อ้างอิง → `Doc_Return` (คอลัมน์เป้าหมาย: ID_Doc_Return) | — |  | Doc_Return |
| 4 | `Image_Document_Return` | Image | คอลัมน์รูปภาพ | — |  | — |

<!-- col: Image_Doc_Return :: _RowNumber -->
<!-- col: Image_Doc_Return :: ID_Image_Doc_Return -->
<!-- col: Image_Doc_Return :: ID_Doc_Return -->
<!-- col: Image_Doc_Return :: Image_Document_Return -->

## สูตรในตารางนี้

### ID_Image_Doc_Return

<!-- formula: Image_Doc_Return :: ID_Image_Doc_Return -->

**ค่าเริ่มต้น**

```
=UNIQUEID()
```

- **Reset_If**: `No`

## ความสัมพันธ์

**อ้างอิงออกไป** (คอลัมน์ของตารางนี้ → ตารางอื่น)

- `ID_Doc_Return` → `Doc_Return` (key: `ID_Doc_Return`)
<!-- rel: Image_Doc_Return -> Doc_Return -->

- ไม่มีตารางอื่นอ้างอิงกลับมา
