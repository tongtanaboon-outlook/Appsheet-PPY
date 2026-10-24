# Process for MeSpace Process Table

<!-- table: Process for MeSpace Process Table -->
<!-- bot: Process for MeSpace Process Table -->

> **ตารางของระบบอัตโนมัติ (bot)** — ไม่ใช่ข้อมูลธุรกิจ

| คุณสมบัติ | ค่า |
|---|---|
| ชนิด | bot |
| ที่มาข้อมูล | `native` |
| source_path | `/ProcessStateTables/70999aca-5a1f-4dfc-907b417bc046f574/e8dd4cb2-0865-4a3e-8843784baf6492ad/State Table` |
| จำนวนคอลัมน์ | 12 |
| เห็นใน UI | `NEVER` |

## คอลัมน์ทั้งหมด

| # | ชื่อคอลัมน์ | ประเภท | คำอธิบาย | สูตร / ค่าเริ่มต้น | Key |
|---:|---|---|---|---|:---:|
| 1 | `Instance Id` | Text | คอลัมน์ข้อความ — **Key ของแถว** | — | ✅ |
| 2 | `ID_ปริ๊นใบวางบิล` | Text | คอลัมน์ข้อความ | — |  |
| 3 | `ชื่องาน` | Text | คอลัมน์ข้อความ — ตรวจความถูกต้องตามเงื่อนไข | — |  |
| 4 | `StartDate` | Date | คอลัมน์วันที่ | — |  |
| 5 | `EndDate` | Date | คอลัมน์วันที่ | — |  |
| 6 | `ราคารวม` | Price | คอลัมน์ราคา | — |  |
| 7 | `Export to xlsx` | Yes/No | คอลัมน์ใช่/ไม่ใช่ | — |  |
| 8 | `Export to xlsx To Athens` | Yes/No | คอลัมน์ใช่/ไม่ใช่ | — |  |
| 9 | `ปริ๊นใบวางบิลแยกตามชื่องาน` | Yes/No | คอลัมน์ใช่/ไม่ใช่ | — |  |
| 10 | `วันที่ออกเอกสาร` | Date | คอลัมน์วันที่ | — |  |
| 11 | `ผลลัพท์` | List | คอลัมน์รายการอ้างอิง | — |  |
| 12 | `Clear` | Ref | คอลัมน์อ้างอิงตารางอื่น — อ้างอิง → `Clear Output 9` (คอลัมน์เป้าหมาย: InstanceId) | — |  |

<!-- col: Process for MeSpace Process Table :: Instance Id -->
<!-- col: Process for MeSpace Process Table :: ID_ปริ๊นใบวางบิล -->
<!-- col: Process for MeSpace Process Table :: ชื่องาน -->
<!-- col: Process for MeSpace Process Table :: StartDate -->
<!-- col: Process for MeSpace Process Table :: EndDate -->
<!-- col: Process for MeSpace Process Table :: ราคารวม -->
<!-- col: Process for MeSpace Process Table :: Export to xlsx -->
<!-- col: Process for MeSpace Process Table :: Export to xlsx To Athens -->
<!-- col: Process for MeSpace Process Table :: ปริ๊นใบวางบิลแยกตามชื่องาน -->
<!-- col: Process for MeSpace Process Table :: วันที่ออกเอกสาร -->
<!-- col: Process for MeSpace Process Table :: ผลลัพท์ -->
<!-- col: Process for MeSpace Process Table :: Clear -->
