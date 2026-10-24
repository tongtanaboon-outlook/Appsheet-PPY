# Acknowledge_Logs

<!-- table: Acknowledge_Logs -->

> **ตารางธุรกิจ** — มีข้อมูลจริงอยู่ใน Google Sheet `Acknowledge_Logs`

| คุณสมบัติ | ค่า |
|---|---|
| ชนิดตาราง | ตารางจริง (business) |
| ที่มาข้อมูล | `google` |
| จำนวนคอลัมน์ | 11 |
| Key | `ID_รับทราบ` |
| คอลัมน์คำนวณอัตโนมัติ | 7 |
| เห็นใน UI | `ALWAYS` |
| สิทธิ์แก้ไข | `ALL_CHANGES` |

## คอลัมน์ทั้งหมด

| # | ชื่อคอลัมน์ | ประเภท | คำอธิบาย | สูตร / ค่าเริ่มต้น | Key | Ref ไปยัง |
|---:|---|---|---|---|:---:|---|
| 1 | `_RowNumber` | Number | คอลัมน์ตัวเลข — ซ่อนใน UI | — |  | — |
| 2 | `ID_รับทราบ` | Text | คอลัมน์ข้อความ — **Key ของแถว**; มีค่าเริ่มต้นเมื่อสร้างแถว | `UNIQUEID()` | ✅ | — |
| 3 | `ID_ประกาศ` | Ref | คอลัมน์อ้างอิงตารางอื่น — อ้างอิง → `Announcements` (คอลัมน์เป้าหมาย: ID_ประกาศ); มีค่าเริ่มต้นเมื่อสร้างแถว | `=MAXROW( "Announcements", "วันที่ประกาศ", NOT(IN([ID_ประกาศ], SELECT(Acknowledge_Logs[ID_ประกาศ], [Email พนัก…` |  | Announcements |
| 4 | `วันที่และเวลารับทราบ` | DateTime | คอลัมน์วันที่และเวลา — มีค่าเริ่มต้นเมื่อสร้างแถว | `=NOW()` |  | — |
| 5 | `Email พนักงาน` | Email | คอลัมน์อีเมล — มีค่าเริ่มต้นเมื่อสร้างแถว | `=USEREMAIL()` |  | — |
| 6 | `ชื่อ - นามสกุล` | Text | คอลัมน์ข้อความ — มีค่าเริ่มต้นเมื่อสร้างแถว | `=LOOKUP(USEREMAIL(), "ข้อมูลพนักงาน", "Email พนักงาน", "ชื่อ นามสกุล")` |  | — |
| 7 | `ทะเบียนรถ` | Text | คอลัมน์ข้อความ — มีค่าเริ่มต้นเมื่อสร้างแถว | `=LOOKUP(USEREMAIL(), "ข้อมูลพนักงาน", "Email พนักงาน", "ทะเบียนรถ")` |  | — |
| 8 | `เลือกเพื่อยืนยัน` | Enum | คอลัมน์ตัวเลือกเดียว | — |  | — |
| 9 | `หมายเหตุ` | LongText | คอลัมน์ข้อความยาว — แสดงผลตามเงื่อนไข | — |  | — |
| 10 | `ลงชื่อพนักงาน` | Signature | คอลัมน์ลายเซ็น | — |  | — |
| 11 | `ข้อความประกาศ` | Show | คอลัมน์ข้อความแสดงผล — คำนวณอัตโนมัติ; แสดงผลตามเงื่อนไข | `=CONCATENATE( " ประกาศ/แจ้งเตือน" "เรื่อง: ", [ID_ประกาศ]. [หัวข้อประกาศ], " ---------------------- ", [ID_ปร…` |  | — |

<!-- col: Acknowledge_Logs :: _RowNumber -->
<!-- col: Acknowledge_Logs :: ID_รับทราบ -->
<!-- col: Acknowledge_Logs :: ID_ประกาศ -->
<!-- col: Acknowledge_Logs :: วันที่และเวลารับทราบ -->
<!-- col: Acknowledge_Logs :: Email พนักงาน -->
<!-- col: Acknowledge_Logs :: ชื่อ - นามสกุล -->
<!-- col: Acknowledge_Logs :: ทะเบียนรถ -->
<!-- col: Acknowledge_Logs :: เลือกเพื่อยืนยัน -->
<!-- col: Acknowledge_Logs :: หมายเหตุ -->
<!-- col: Acknowledge_Logs :: ลงชื่อพนักงาน -->
<!-- col: Acknowledge_Logs :: ข้อความประกาศ -->

## สูตรในตารางนี้

### ID_รับทราบ

<!-- formula: Acknowledge_Logs :: ID_รับทราบ -->

**ค่าเริ่มต้น**

```
UNIQUEID()
```

- **Reset_If**: `No`

### ID_ประกาศ

<!-- formula: Acknowledge_Logs :: ID_ประกาศ -->

**ค่าเริ่มต้น**

```
=MAXROW( "Announcements", "วันที่ประกาศ", NOT(IN([ID_ประกาศ], SELECT(Acknowledge_Logs[ID_ประกาศ], [Email พนักงาน] = USEREMAIL()))) )
```

- **Reset_If**: `No`

### วันที่และเวลารับทราบ

<!-- formula: Acknowledge_Logs :: วันที่และเวลารับทราบ -->

**ค่าเริ่มต้น**

```
=NOW()
```

- **Reset_If**: `No`

### Email พนักงาน

<!-- formula: Acknowledge_Logs :: Email พนักงาน -->

**ค่าเริ่มต้น**

```
=USEREMAIL()
```

- **Reset_If**: `No`

### ชื่อ - นามสกุล

<!-- formula: Acknowledge_Logs :: ชื่อ - นามสกุล -->

**ค่าเริ่มต้น**

```
=LOOKUP(USEREMAIL(), "ข้อมูลพนักงาน", "Email พนักงาน", "ชื่อ นามสกุล")
```

- **Reset_If**: `No`

### ทะเบียนรถ

<!-- formula: Acknowledge_Logs :: ทะเบียนรถ -->

**ค่าเริ่มต้น**

```
=LOOKUP(USEREMAIL(), "ข้อมูลพนักงาน", "Email พนักงาน", "ทะเบียนรถ")
```

- **Reset_If**: `No`

### ข้อความประกาศ

<!-- formula: Acknowledge_Logs :: ข้อความประกาศ -->

**App formula**

```
=CONCATENATE( " ประกาศ/แจ้งเตือน" "เรื่อง: ", [ID_ประกาศ]. [หัวข้อประกาศ], " ---------------------- ", [ID_ประกาศ].[เนื้อหาประกาศ], " --------------------- ", [ID_ประกาศ].[Note], )
```

- **Show_If**: `=CONTEXT("ViewType") ="Form"`
- **Reset_If**: `No`

## ความสัมพันธ์

**อ้างอิงออกไป** (คอลัมน์ของตารางนี้ → ตารางอื่น)

- `ID_ประกาศ` → `Announcements` (key: `ID_ประกาศ`)
<!-- rel: Acknowledge_Logs -> Announcements -->

- ไม่มีตารางอื่นอ้างอิงกลับมา
