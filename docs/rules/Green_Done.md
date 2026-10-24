# Format Rule: Green_Done

<!-- rule: Green_Done -->

| คุณสมบัติ | ค่า |
|---|---|
| ใช้กับข้อมูล | `ตารางงานประจำวัน` |
| คอลัมน์/แอ็กชันที่กระทบ | `Plan Delivery Invoice No Shipment No ชื่อ - นามสกุล ทะเบียนรถ ชื่อเจ้าของสินค้า ชื่อปลายทาง` |
| เงื่อนไข | `=[ScanStatus] = "สแกนแล้ว"` |
| ลำดับกติกา | 1 |
| ปิดใช้งาน | `No` |
| แสดงใน UI | `ALWAYS` |

## รูปแบบที่ใช้

```json
"{\"textColor\": \"green\", \"highlightColor\": \"green\", \"textSize\": 1.0, \"underline\": false, \"strikethrough\": false, \"bold\": true, \"italic\": false, \"uppercase\": false, \"icon\": \"fal fa-check-circle\", \"imageSize\": null}"
```
