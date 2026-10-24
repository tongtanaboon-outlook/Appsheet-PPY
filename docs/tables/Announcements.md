# Announcements

<!-- table: Announcements -->

> **ตารางธุรกิจ** — มีข้อมูลจริงอยู่ใน Google Sheet `Announcements`

| คุณสมบัติ | ค่า |
|---|---|
| ชนิดตาราง | ตารางจริง (business) |
| ที่มาข้อมูล | `google` |
| จำนวนคอลัมน์ | 7 |
| Key | `ID_ประกาศ` |
| คอลัมน์คำนวณอัตโนมัติ | 3 |
| เห็นใน UI | `ALWAYS` |
| สิทธิ์แก้ไข | `ALL_CHANGES` |

## คอลัมน์ทั้งหมด

| # | ชื่อคอลัมน์ | ประเภท | คำอธิบาย | สูตร / ค่าเริ่มต้น | Key | Ref ไปยัง |
|---:|---|---|---|---|:---:|---|
| 1 | `_RowNumber` | Number | คอลัมน์ตัวเลข — ซ่อนใน UI | — |  | — |
| 2 | `ID_ประกาศ` | Text | คอลัมน์ข้อความ — **Key ของแถว**; มีค่าเริ่มต้นเมื่อสร้างแถว | `UNIQUEID()` | ✅ | — |
| 3 | `วันที่ประกาศ` | Date | คอลัมน์วันที่ — มีค่าเริ่มต้นเมื่อสร้างแถว | `=TODAY()` |  | — |
| 4 | `หัวข้อประกาศ` | Enum | คอลัมน์ตัวเลือกเดียว | — |  | — |
| 5 | `เนื้อหาประกาศ` | LongText | คอลัมน์ข้อความยาว | — |  | — |
| 6 | `Note` | LongText | คอลัมน์ข้อความยาว | — |  | — |
| 7 | `Related Acknowledge_Logs` | List | คอลัมน์รายการอ้างอิง — คำนวณอัตโนมัติ | `REF_ROWS("Acknowledge_Logs", "ID_ประกาศ")` |  | — |

<!-- col: Announcements :: _RowNumber -->
<!-- col: Announcements :: ID_ประกาศ -->
<!-- col: Announcements :: วันที่ประกาศ -->
<!-- col: Announcements :: หัวข้อประกาศ -->
<!-- col: Announcements :: เนื้อหาประกาศ -->
<!-- col: Announcements :: Note -->
<!-- col: Announcements :: Related Acknowledge_Logs -->

## สูตรในตารางนี้

### ID_ประกาศ

<!-- formula: Announcements :: ID_ประกาศ -->

**ค่าเริ่มต้น**

```
UNIQUEID()
```

- **Reset_If**: `No`

### วันที่ประกาศ

<!-- formula: Announcements :: วันที่ประกาศ -->

**ค่าเริ่มต้น**

```
=TODAY()
```

- **Reset_If**: `No`

### Related Acknowledge_Logs

<!-- formula: Announcements :: Related Acknowledge_Logs -->

**App formula**

```
REF_ROWS("Acknowledge_Logs", "ID_ประกาศ")
```

- **Reset_If**: `No`

## ความสัมพันธ์

- ไม่มีคอลัมน์ Ref ที่ชี้ออกไปยังตารางอื่น

**ถูกอ้างอิงจากตารางอื่น**

- `Acknowledge_Logs`.`ID_ประกาศ` → `Announcements`
