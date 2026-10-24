# Format Rule: เตือนตรวจสอบ RW

<!-- rule: เตือนตรวจสอบ RW -->

| คุณสมบัติ | ค่า |
|---|---|
| ใช้กับข้อมูล | `SCGนครหลวงJWDภูมิภาค` |
| คอลัมน์/แอ็กชันที่กระทบ | `Shipment No` |
| เงื่อนไข | `=IN([Invoice No],ข้อมูลงานRW[เลขที่เอกสาร])` |
| ลำดับกติกา | 1 |
| ปิดใช้งาน | `No` |
| แสดงใน UI | `ALWAYS` |

## รูปแบบที่ใช้

```json
"{\"textColor\": \"red\", \"highlightColor\": \"red\", \"textSize\": 1.3, \"underline\": false, \"strikethrough\": false, \"bold\": true, \"italic\": false, \"uppercase\": false, \"icon\": null, \"imageSize\": null}"
```
