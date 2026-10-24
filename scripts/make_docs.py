#!/usr/bin/env python3
"""
Build the documentation layer from the machine-readable schema.

Design goal: an AI agent should be able to open ONE file for the one table it
is working on, and get the complete picture (columns, types, formulas,
conditions, relations) without reading a 2304-row CSV.

Output layout:
    docs/00-overview.md                 โครงสร้างทั่วไปของแอป
    docs/01-main-tables.md              ตารางหลัก 29 ตาราง (สารบัญ)
    docs/02-process-output-tables.md    Process/Output 60 ตาราง (สารบัญ)
    docs/03-columns-and-formulas.md     สูตรทั้งหมด 319 คอลัมน์
    docs/04-views-actions-rules-slices.md  UX layer
    docs/05-glossary.md
    docs/tables/<table>.md              29 ไฟล์ - ตารางจริง ทีละไฟล์
    docs/process-tables/<table>.md      60 ไฟล์ - ตารางบอท ทีละไฟล์
    docs/rules/<rule>.md                11 ไฟล์ - Format rule ทีละไฟล์

    python3 scripts/make_docs.py           # สร้าง
    python3 scripts/make_docs.py --check   # ตรวจว่าเอกสารตรงกับ schema
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"

# ---------------------------------------------------------------- helpers

def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def esc(text: str) -> str:
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


def short(text: str, n: int = 90) -> str:
    t = re.sub(r"\s+", " ", (text or "").strip())
    return t if len(t) <= n else t[: n - 1] + "…"


def slug(name: str) -> str:
    s = re.sub(r"[^\w฀-๿]+", "_", name, flags=re.UNICODE).strip("_")
    return s or "item"


TYPE_THAI = {
    "Text": "ข้อความ", "LongText": "ข้อความยาว", "Number": "ตัวเลข",
    "Decimal": "ทศนิยม", "Price": "ราคา", "Percent": "เปอร์เซ็นต์",
    "Duration": "ระยะเวลา", "Date": "วันที่", "DateTime": "วันที่และเวลา",
    "Time": "เวลา", "LatLong": "พิกัด GPS", "Geolocation": "ตำแหน่ง",
    "Email": "อีเมล", "Phone": "เบอร์โทร", "Url": "ลิงก์", "Image": "รูปภาพ",
    "Signature": "ลายเซ็น", "Yes/No": "ใช่/ไม่ใช่", "Enum": "ตัวเลือกเดียว",
    "EnumList": "ตัวเลือกหลาย", "Ref": "อ้างอิงตารางอื่น",
    "List": "รายการอ้างอิง", "Slice": "รายการจาก slice",
    "Number of this row": "เลขแถว", "ID of this row": "ID แถว",
    "ChangeCounter": "ตัวนับการเปลี่ยนแปลง", "Name": "ชื่อ-นามสกุล",
    "Show": "ข้อความแสดงผล",
}


def describe(col: dict) -> str:
    """Factual Thai description derived from the schema - never invented."""
    ctype = col.get("type", "")
    label = TYPE_THAI.get(ctype, ctype or "ไม่ระบุชนิด")
    bits: list[str] = []
    if col.get("key") == "Yes":
        bits.append("**Key ของแถว**")
    if ctype == "Ref" and col.get("ref_table"):
        extra = f" (คอลัมน์เป้าหมาย: {col['ref_key_column']})" if col.get("ref_key_column") else ""
        bits.append(f"อ้างอิง → `{col['ref_table']}`{extra}")
    if col.get("app_formula"):
        bits.append("คำนวณอัตโนมัติ")
    if col.get("initial_value"):
        bits.append("มีค่าเริ่มต้นเมื่อสร้างแถว")
    if col.get("required_if"):
        bits.append("บังคับกรอกตามเงื่อนไข")
    if col.get("valid_if"):
        bits.append("ตรวจความถูกต้องตามเงื่อนไข")
    if col.get("editable_if"):
        bits.append("แก้ไขได้ตามเงื่อนไข")
    if col.get("show_if"):
        bits.append("แสดงผลตามเงื่อนไข")
    if col.get("hidden") == "Yes":
        bits.append("ซ่อนใน UI")
    if col.get("sensitive_data") == "Yes":
        bits.append("**ข้อมูลอ่อนไหว (PII)**")
    text = f"คอลัมน์{label}"
    if bits:
        text += " — " + "; ".join(bits)
    return text


def cond_lines(col: dict) -> list[str]:
    out = []
    for key, label in [("valid_if", "Valid_If"), ("required_if", "Required_If"),
                       ("editable_if", "Editable_If"), ("show_if", "Show_If"),
                       ("reset_on_edit", "Reset_If"),
                       ("error_message_if_invalid", "Error_Message_If_Invalid"),
                       ("suggested_values", "Suggested_Values")]:
        if col.get(key):
            out.append(f"- **{label}**: `{short(col[key], 400)}`")
    if col.get("enum_values"):
        out.append(f"- **ค่าที่เลือกได้**: `{short(col['enum_values'], 400)}`")
    return out


# ---------------------------------------------------------------- per table

def table_doc(t: dict, cols: list[dict], rels: list[dict], incoming: list[dict],
              kind: str) -> str:
    name = t["name"]
    is_biz = kind == "business"
    out: list[str] = []
    out.append(f"# {name}")
    out.append("")
    out.append(f"<!-- table: {name} -->")
    out.append("")
    if is_biz:
        out.append(f"> **ตารางธุรกิจ** — มีข้อมูลจริงอยู่ใน Google Sheet "
                   f"`{t.get('worksheet_name') or name}`")
    else:
        out.append(f"> **ตารางของระบบอัตโนมัติ (bot)** — ไม่ใช่ข้อมูลธุรกิจ "
                   f"ห้ามใช้นับจำนวนธุรกิจ · ดู "
                   f"[02-process-output-tables.md](../02-process-output-tables.md)")
    out.append("")

    key_cols = [c["name"] for c in cols if c.get("key") == "Yes"]
    computed = [c for c in cols if c.get("app_formula") or c.get("initial_value")]
    out.append("| คุณสมบัติ | ค่า |")
    out.append("|---|---|")
    out.append(f"| ชนิดตาราง | {'ตารางจริง (business)' if is_biz else t['kind']} |")
    out.append(f"| ที่มาข้อมูล | `{t.get('data_source') or '-'}` |")
    out.append(f"| จำนวนคอลัมน์ | {len(cols)} |")
    out.append(f"| Key | {', '.join('`'+k+'`' for k in key_cols) if key_cols else 'ไม่มี'} |")
    out.append(f"| คอลัมน์คำนวณอัตโนมัติ | {len(computed)} |")
    out.append(f"| เห็นใน UI | `{t.get('visible')}` |")
    if t.get("security_filter"):
        out.append(f"| Security filter | `{short(t['security_filter'], 200)}` |")
    if t.get("updates_allowed"):
        out.append(f"| สิทธิ์แก้ไข | `{t['updates_allowed']}` |")
    out.append("")

    out.append("## คอลัมน์ทั้งหมด")
    out.append("")
    out.append("| # | ชื่อคอลัมน์ | ประเภท | คำอธิบาย | สูตร / ค่าเริ่มต้น | Key | Ref ไปยัง |")
    out.append("|---:|---|---|---|---|:---:|---|")
    for c in cols:
        f = c.get("app_formula") or c.get("initial_value") or ""
        f = ("`" + short(f, 110) + "`") if f else "—"
        out.append(
            f"| {c['index']} | `{esc(c['name'])}` | {esc(c.get('type',''))} "
            f"| {describe(c)} | {f} "
            f"| {'✅' if c.get('key')=='Yes' else ''} "
            f"| {esc(c.get('ref_table','')) or '—'} |")
    out.append("")
    for c in cols:
        out.append(f"<!-- col: {name} :: {c['name']} -->")
    out.append("")

    if computed:
        out.append("## สูตรในตารางนี้")
        out.append("")
        for c in computed:
            out.append(f"### {c['name']}")
            out.append("")
            out.append(f"<!-- formula: {name} :: {c['name']} -->")
            out.append("")
            if c.get("app_formula"):
                out.append("**App formula**")
                out.append("")
                out.append("```")
                out.append(c["app_formula"])
                out.append("```")
                out.append("")
            if c.get("initial_value"):
                out.append("**ค่าเริ่มต้น**")
                out.append("")
                out.append("```")
                out.append(c["initial_value"])
                out.append("```")
                out.append("")
            for line in cond_lines(c):
                out.append(line)
            out.append("")

    out.append("## ความสัมพันธ์")
    out.append("")
    if rels:
        out.append("**อ้างอิงออกไป** (คอลัมน์ของตารางนี้ → ตารางอื่น)")
        out.append("")
        for r in rels:
            out.append(f"- `{r['from_column']}` → `{r['to_table']}` "
                       f"(key: `{r['to_key_column']}`)")
            out.append(f"<!-- rel: {r['from_table']} -> {r['to_table']} -->")
    else:
        out.append("- ไม่มีคอลัมน์ Ref ที่ชี้ออกไปยังตารางอื่น")
    out.append("")
    if incoming:
        out.append("**ถูกอ้างอิงจากตารางอื่น**")
        out.append("")
        for r in incoming:
            out.append(f"- `{r['from_table']}`.`{r['from_column']}` → `{name}`")
    else:
        out.append("- ไม่มีตารางอื่นอ้างอิงกลับมา")
    out.append("")
    return "\n".join(out)


def bot_doc(t: dict, cols: list[dict]) -> str:
    name = t["name"]
    out: list[str] = []
    out.append(f"# {name}")
    out.append("")
    out.append(f"<!-- table: {name} -->")
    out.append(f"<!-- bot: {name} -->")
    out.append("")
    out.append(f"> **ตารางของระบบอัตโนมัติ (bot)** — ไม่ใช่ข้อมูลธุรกิจ")
    out.append("")
    out.append("| คุณสมบัติ | ค่า |")
    out.append("|---|---|")
    out.append(f"| ชนิด | {t['kind']} |")
    out.append(f"| ที่มาข้อมูล | `{t.get('data_source') or '-'}` |")
    out.append(f"| source_path | `{short(t.get('source_path',''), 120)}` |")
    out.append(f"| จำนวนคอลัมน์ | {t['column_count']} |")
    out.append(f"| เห็นใน UI | `{t.get('visible')}` |")
    out.append("")
    out.append("## คอลัมน์ทั้งหมด")
    out.append("")
    out.append("| # | ชื่อคอลัมน์ | ประเภท | คำอธิบาย | สูตร / ค่าเริ่มต้น | Key |")
    out.append("|---:|---|---|---|---|:---:|")
    for c in cols:
        f = c.get("app_formula") or c.get("initial_value") or ""
        f = ("`" + short(f, 110) + "`") if f else "—"
        out.append(f"| {c['index']} | `{esc(c['name'])}` | {esc(c.get('type',''))} "
                   f"| {describe(c)} | {f} "
                   f"| {'✅' if c.get('key')=='Yes' else ''} |")
    out.append("")
    for c in cols:
        out.append(f"<!-- col: {name} :: {c['name']} -->")
    out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------- indexes

def main_tables_index(tables: list[dict], cols_by_table: dict) -> str:
    out = ["# 01 — ตารางหลัก (Main Tables)", "",
           "> **29 ตาราง** ที่เป็นข้อมูลธุรกิจจริง — ทั้งหมดมี `Data Source = google`",
           "> (เก็บใน Google Sheet) และ `Visible? = ALWAYS` (ผู้ใช้เห็นและใส่ข้อมูลได้)", "",
           "ทุกตารางมีไฟล์รายละเอียดใน [`tables/`](tables/) — "
           "AI ที่ทำงานเฉพาะตารางใดตารางหนึ่ง ให้เปิดแค่ไฟล์นั้น", "",
           "| # | ตาราง | คอลัมน์ | คำนวณ | Ref | Key | คำอธิบาย |", "|---:|---|---:|---:|---:|---|---|"]
    biz = [t for t in tables if t["kind"] == "business"]
    for i, t in enumerate(biz, 1):
        cols = cols_by_table.get(t["name"], [])
        key = next((c["name"] for c in cols if c.get("key") == "Yes"), "—")
        ncomp = sum(1 for c in cols if c.get("app_formula") or c.get("initial_value"))
        nref = sum(1 for c in cols if c.get("type") == "Ref")
        out.append(f"| {i} | [`{t['name']}`](tables/{slug(t['name'])}.md) "
                   f"| {t['column_count']} | {ncomp} | {nref} | `{key}` "
                   f"| ที่มา `{t.get('data_source')}` |")
    out.append("")
    return "\n".join(out)


def process_tables_index(tables: list[dict], cols_by_table: dict) -> str:
    bots = [t for t in tables if t["kind"] in ("bot", "system")]
    out = ["# 02 — Process Tables + Output Tables", "",
           "> **61 ตาราง** ที่ AppSheet สร้างให้กับระบบอัตโนมัติ — **ไม่ใช่ข้อมูลธุรกิจ**",
           "> ห้ามนับแถวจากตารางเหล่านี้ (ถูกเขียนทับและล้างอยู่ตลอด)", "",
           "## ชนิดของตารางบอท", "",
           "| ชนิด | รูปแบบชื่อ | source_path | หน้าที่ |", "|---|---|---|---|",
           "| Process Table | `Process for <บอท> Process Table` | `/ProcessStateTables/<bot>/<tbl>/State Table` | ตัวแปรที่ส่งผ่านขั้นตอนของ process |",
           "| Step Output | `<ชื่อ> Output` / `New step Output` | `/ProcessStateTables/.../StepOutput_<ชื่อ>` | ผลลัพธ์ของ step — ถูกล้างทุกครั้งที่รัน |",
           "| ระบบ | `_Per User Settings` | `_Per User Settings` | ค่าตั้งค่ารายผู้ใช้ |",
           "",
           "## ดัชนีตารางบอท", "",
           "| # | ตาราง | ชนิด | คอลัมน์ | ที่มา |", "|---:|---|---|---:|---|"]
    for i, t in enumerate(bots, 1):
        out.append(f"| {i} | [`{t['name']}`](process-tables/{slug(t['name'])}.md) "
                   f"| {t['kind']} | {t['column_count']} "
                   f"| `{short(t.get('source_path',''), 60)}` |")
    out.append("")
    return "\n".join(out)


def columns_and_formulas(tables: list[dict], cols_by_table: dict) -> str:
    out = ["# 03 — ตาราง + คอลัมน์ + สูตรในคอลัมน์", "",
           "ทุกคอลัมน์ของทุกตาราง พร้อมสูตรและเงื่อนไข — "
           "**319 คอลัมน์ที่คำนวณอัตโนมัติ** "
           f"(192 มี `App formula` · 127 มี `Initial value`)", "",
           "| ตาราง | คอลัมน์ | ชนิด | สูตร / ค่าเริ่มต้น | เงื่อนไข |",
           "|---|---|---|---|---|"]
    for t in tables:
        cols = cols_by_table.get(t["name"], [])
        comp = [c for c in cols if c.get("app_formula") or c.get("initial_value")]
        if not comp:
            continue
        for c in comp:
            f = c.get("app_formula") or c.get("initial_value") or ""
            conds = "; ".join(
                f"{k}={short(c[k], 70)}" for k in
                ("valid_if", "required_if", "editable_if", "show_if") if c.get(k))
            out.append(f"| `{t['name']}` | `{esc(c['name'])}` | {esc(c.get('type',''))} "
                       f"| `{short(f, 150)}` | {conds or '—'} |")
    out.append("")
    return "\n".join(out)


def ux_layer(views: list[dict], actions: list[dict], rules: list[dict],
             slices: list[dict], tables: list[dict]) -> str:
    by_kind = defaultdict(list)
    for a in actions:
        by_kind[a.get("do_this") or "?"].append(a)
    out = []
    out.append("# 04 - Views / Actions / Format Rules / Slices")
    out.append("")
    out.append("ชั้น UX ของแอป - กำหนดว่า *ผู้ใช้เห็นอะไร กดอะไรได้ "
               "และข้อมูลถูกเน้น/เปลี่ยนสีอย่างไร*")
    out.append("")
    out.append(f"* **Views** {len(views)} - **Actions** {len(actions)} - "
               f"**Format Rules** {len(rules)} - **Slices** {len(slices)}")
    out.append("")
    out.append("## Format Rules (" + str(len(rules)) + " รายการ)")
    out.append("")
    out.append("กติกาที่เปลี่ยนสี/ตัวหนา/ไอคอนตามเงื่อนไข - "
               "**สีและสถานะใน UI ไม่ใช่ข้อมูลดิบ**")
    out.append("")
    out.append("| # | กติกา | ใช้กับข้อมูล | เงื่อนไข | รูปแบบ |")
    out.append("|---:|---|---|---|---|")
    for i, r in enumerate(rules, 1):
        out.append(f"| {i} | [`{r['name']}`](rules/{slug(r['name'])}.md) "
                   f"| `{r.get('for_data','')}` | `{short(r.get('condition',''), 120)}` "
                   f"| `{short(r.get('like_this_raw',''), 90)}` |")
    out.append("")
    out.append("## Actions (" + str(len(actions)) + " รายการ) แยกตามชนิดคำสั่ง")
    out.append("")
    out.append("| `do_this` | จำนวน | ความหมาย |")
    out.append("|---|---:|---|")
    meaning = {
        "SET_COLUMN_VALUE": "ตั้งค่าคอลัมน์ในแถว (เช่น ปุ่มอนุมัติ)",
        "ADD_RECORD": "เพิ่มแถวใหม่", "DELETE_RECORD": "ลบแถว",
        "NAVIGATE_APP": "เปิดหน้าจอ/แอปอื่น", "EDIT_RECORD": "เปิดฟอร์มแก้ไข",
        "EXPORT_VIEW": "export CSV/XLSX", "EMAIL": "ส่งอีเมล",
        "REF_ACTION": "เปิดรายการที่อ้างอิง", "COMPOSITE": "รวมหลายคำสั่ง",
        "NAVIGATE_DIFFERENT_APP": "ข้ามไปแอปอื่น", "NAVIGATE_URL": "เปิด URL ภายนอก",
        "SMS": "ส่ง SMS", "CALL": "โทรหา", "ADD_RECORD_TO": "เพิ่มแถวลงอีกตาราง",
    }
    for k, v in sorted(by_kind.items(), key=lambda kv: -len(kv[1])):
        out.append(f"| `{k}` | {len(v)} | {meaning.get(k, '-')} |")
    out.append("")
    out.append("### Action ที่แก้ไขข้อมูล (modifies data)")
    out.append("")
    out.append("| action | ชนิด | ตารางเป้าหมาย | คอลัมน์ |")
    out.append("|---|---|---|---|")
    for a in actions:
        if a.get("modifies_data") != "Yes":
            continue
        out.append(f"| `{esc(a['name'])}` | `{a.get('do_this','')}` "
                   f"| `{a.get('for_record_of_table','')}` | `{a.get('set_this_column','')}` |")
    out.append("")
    out.append("## Views (" + str(len(views)) + " รายการ)")
    out.append("")
    out.append("| # | ชื่อ view | ชนิด | ตำแหน่ง | เมนู |")
    out.append("|---:|---|---|---|---:|")
    for i, v in enumerate(views, 1):
        out.append(f"| {i} | `{esc(v['name'])}` | {v.get('view_type','')} "
                   f"| {v.get('position','')} | {v.get('menu_order','')} |")
    out.append("")
    out.append("## Slices (" + str(len(slices)) + " รายการ)")
    out.append("")
    out.append("| # | ชื่อ slice | ตาราง | เงื่อนไขกรอง | update mode |")
    out.append("|---:|---|---|---|---|")
    for i, s in enumerate(slices, 1):
        out.append(f"| {i} | `{esc(s['name'])}` | `{s.get('source_table','')}` "
                   f"| `{short(s.get('row_filter_condition',''), 110)}` "
                   f"| `{s.get('update_mode','')}` |")
    out.append("")
    return "\n".join(out)


def rule_doc(r: dict, tables: list[dict]) -> str:
    name = r["name"]
    out = [f"# Format Rule: {name}", "", f"<!-- rule: {name} -->", "",
           "| คุณสมบัติ | ค่า |", "|---|---|",
           f"| ใช้กับข้อมูล | `{r.get('for_data','')}` |",
           f"| คอลัมน์/แอ็กชันที่กระทบ | `{esc(r.get('columns_and_actions_raw',''))}` |",
           f"| เงื่อนไข | `{esc(r.get('condition',''))}` |",
           f"| ลำดับกติกา | {r.get('rule_order','')} |",
           f"| ปิดใช้งาน | `{r.get('disabled','')}` |",
           f"| แสดงใน UI | `{r.get('visible','')}` |",
           "",
           "## รูปแบบที่ใช้", "", "```json",
           json.dumps(r.get("like_this") or {}, ensure_ascii=False, indent=2),
           "```", ""]
    return "\n".join(out)


BOT_ANALYSIS = '# โครงสร้างภายในของบอทและระบบอัตโนมัติ\n\n> ⚠️ **ข้อจำกัดที่ต้องรู้ก่อนอ่าน:** เอกสาร "Application Documentation" ของ AppSheet\n> **ไม่มีส่วนนิยามของบอท** (ไม่มี event / webhook / schedule / bot definition)\n> สิ่งที่มีคือ **ผลข้างเคียง** ของบอท ได้แก่\n> 1. **ตารางบอท** 60 ตาราง (Process Table / Step Output) — ที่บอทเขียนกลับมา\n> 2. **action** 214 รายการ — คำสั่งที่ผู้ใช้/ระบบเรียกใช้\n> 3. **slices** 8 และ **format rules** 11 — กติกาการแสดงผล\n>\n> ถ้าต้องการนิยามบอทจริง (ทริกเกอร์/เวลา/เงื่อนไข) ให้ไปที่\n> **AppSheet → Automations → Bots** แล้ว export — ดู [วิธีเติมข้อมูล](#วิธีเติมนิยามบอทจริง)\n\n---\n\n## 1. ตารางบอทมีอะไรบ้าง\n\nระบบอัตโนมัติของแอปนี้แบ่งเป็น **2 กลุ่ม**\n\n### กลุ่ม A — บอทประมวลผลใบวางบิล (โหลดมากที่สุด)\n\nชื่อเริ่มด้วย `Process for ปริ๊นใบวางบิล...` — คือบอทที่ไปดึงข้อมูลจากระบบปริ๊นของแต่ละ\nคลัง/สาขามาสร้างใบวางบิล มีหลายเวอร์ชันเพราะแต่ละคลังมีระบบปริ๊นต่างกัน\n\n| บอท | ตารางผลลัพธ์ | หมายเหตุจากหลักฐาน (source_path / action) |\n|---|---|---|\n| `Process for ปริ๊นใบวางบิล Process Table` | `ปริ๊นใบวางบิล_step Output` | บอทปริ๊นหลัก |\n| `Process for ปริ๊นใบวางบิล_โอนคลัง มโนยนต์ (นวนคร)` | `Clear Output 2` | โอนคลังมโนยนต์ (สาขานวนคร) |\n| `Process for ปริ๊นใบวางบิล_โอนคลัง กระสอบ2(บางบัวทอง)` | `Clear Output 3` | โอนคลัง กระสอบ 2 (บางบัวทอง) |\n| `Process for ปริ๊นใบวางบิล_ไอโรบอท Process Table` | `Clear Output 4` | ไอโรบอท — คลังสินค้าเอสซีจี เจดับเบิ้ลยูดี วังน้อย |\n| `Process for ปริ๊นใบวางบิล_โอนคลัง เอเธน Process Table` | `Clear Output 5` | โอนคลัง เอเธน |\n| `Process for ปริ๊นใบวางบิล_โอนคลัง บุญถาวร เกษตร_นวมิ นทร์ - 1 Process Table` | `Clear Output 14` | โอนคลัง บุญถาวรเกษตร (นวมินทร์) |\n| `Process for ปริ๊นใบวางบิล_คลังSCGJWDวังน้อย Process Table` | `Clear Output 10` | คลัง SCGJWD วังน้อย |\n| `Process for ปริ๊นใบวางบิล_รับเอกสาร (งานพี่เหน่ง) Process Table` | `Clear Output 7` | รับเอกสาร (งานพี่เหน่ง) |\n| `Process for ปริ๊นใบวางบิล_รับเอกสาร (งานพี่เหน่ง) สตีเบล` | `Clear Output 6` | รับเอกสาร สตีเบล |\n| `Process for ปริ๊นใบวางบิล_เบทาโกร+เหมาตู้ Process Table` | `Clear Output 11` | เบทาโกร + เหมาตู้ |\n| `Process for ปริ๊นใบวางบิล_LINEMAN (6W) (SCG Express)` | `Clear Output 12` | LINEMAN 6 ล้อ |\n| `Process for ปริ๊นใบวางบิล_Thai paper (SCG Express) - 1` | `Clear Output 13` | Thai paper |\n| `Process for ปริ๊นใบวางบิลเอเทน - 1 Process Table` | `Clear Output` | เอเทน |\n| `Process for โอนคลัง (GQ) จีคิว Process Table` | `Clear Output 8` | โอนคลัง จีคิว (GQ) |\n\n> ชื่อคลัง/สาขาในชื่อบอทตรงกับชื่อที่ปรากฏในคอลัมน์และค่าคงที่ของแอป\n> เช่น `คลังสินค้า เอสซีจี เจดับเบิ้ลยูดี วังน้อย` (คอลัมน์ LatLong ค่าคงที่ในตาราง `SCGนครหลวงJWDภูมิภาค`)\n\n### กลุ่ม B — บอทงานเฉพาะทาง\n\n| บอท | ตารางผลลัพธ์ | หน้าที่ที่อนุมานจากชื่อ (มีหลักฐาน = ชื่อบอท + ชื่อตารางผลลัพธ์ + action ที่ผูก) |\n|---|---|---|\n| `Process for Telegram_แจ้งปั ญหา - 1 Process Table` | `Telegram_แจ้งปั ญหา2 Output` | ส่งแจ้งปัญหาระหว่างวันผ่าน Telegram — ยืนยันได้ว่า action `Send SMS`/`EMAIL` และตาราง `แจ้งปั ญหาระหว่างวัน` มี `Ref` จากบอทนี้ |\n| `Process for Bot_รับสินค้าคืน - 1 Process Table` | `เข้ารับสินค้าคืน Output` | บอทรับสินค้าคืน — เขียนคอลัมน์ `สถานะการเข้ารับสินค้า` (มี 6 ค่า: ได้เพิ่ม 200 / ไม่มีสินค้าคืน / ได้เพิ่ม 50% / ทำเบิกค่ายกขึ้นชั้น / เบิกค่าขนส่งตามระยะทาง) |\n| `Process for Bot_เบิกค่าขนส่งตามระยะทาง - 1 Process Table` | `เบิกตามระยะทาง Output` | บอทเบิกค่าขนส่งตามระยะทาง (มีตาราง `ราคาตามระยะทาง` ในตารางจริง) |\n| `Process for ฺBot_4ตัว_จัดเรียงเส้นทาง Process Table` | `GoogleMapsRoutesAPI_Step Output` | จัดเรียงเส้นทาง 4 ตัว — มีหลักฐานจาก `GoogleMapsRoutesAPI` และคอลัมน์ `ที่อยู่ปลายทาง_LatLong_Api` ในตารางจริง |\n| `Process for ใบป่ ะหน้า - 1 Process Table` | (State Table) | สร้างใบประกาศ/ใบหน้า |\n| `Process for สรุปส่วนต่าง - 1 Process Table` | `เคลียสรุปจุดส่ง Output` | สรุปส่วนต่าง + เคลียสรุปจุดส่ง |\n| `Process for สรุปจำนวนจุดที่ส่งงานSCGวังน้อย Process Table` | (State Table) | นับจำนวนจุดที่ส่งงานของ SCG วังน้อย |\n| `Process for ทำเบิกส่วนต่างScgวังน้อย - 1 Process Table` | `ทำเบิกส่วนต่างScgวังน้อยstep Output`, `New step2 Output`, `ไม่ผ่านNew step Output` | บอทเบิกส่วนต่าง SCG วังน้อย (มี 3 step แยก: ผ่าน / ไม่ผ่าน) |\n| `Process for ทำเบิกค่ายกขึ้นชั้น Process Table` | (State Table) | เบิกค่ายกขึ้นชั้น |\n| `Process for ได้เพิ่ม25%ของค่าเที่ยว Process Table` | (State Table) | ได้เพิ่ม 25% ของค่าเที่ยว |\n| `Process for ได้เพิ่ม200_ไม่มีสินค้าคืน_ร้านปิ ด_ไม่มีในจุดส่ง Process Table` | (State Table) | ได้เพิ่ม 200 เมื่อไม่มีสินค้าคืน / ร้านปิด / ไม่มีในจุดส่งงานวันนี้ |\n| `Process for เพิ่มรูปรับคืน - 1 Process Table` | `New step Output` | เพิ่มรูปใบเสร็จ/สลิปตอนรับคืน |\n| `Process for Update ScanStatus เมื่อสแกน Invoice - 1 Process Table` | `Update Output` | อัปเดตสถานะการสแกน (`ScanStatus`) เมื่อสแกนใบวางบิล — ยืนยันได้จาก action `Update ScanStatus` |\n| `Process for New bot - 1 Process Table` | `New step Output 3` | บอทใหม่ (ยังไม่มีคำอธิบายในเอกสาร) |\n| `Process for MeSpace Process Table` | `Clear Output 9` | MeSpace — มี enum `งานMeSpace+แพ็คสินค้า` ในตาราง `ข้อมูลการวางบิล` |\n| `Process for AppSheet_KM - 1 Process Table` | `AppSheet___KM Output` | AppSheet_KM — ยังไม่มีคำอธิบายในเอกสาร |\n\n---\n\n## 2. Action catalog (214 รายการ)\n\nจัดกลุ่มตาม `do_this` (ชนิดคำสั่ง) — ทั้งหมดเป็น action ที่ผู้ใช้กด หรือระบบเรียกจากปุ่ม/สแกน\n\n| `do_this` | จำนวน | ความหมาย |\n|---|---:|---|\n| `SET_COLUMN_VALUE` | 49 | ตั้งค่าคอลัมน์ในแถวปัจจุบัน (เช่น ปุ่ม "อนุมัติ" → เซ็ต `สถานะการอนุมัติ` = "อนุมัติ") |\n| `ADD_RECORD` | 29 | เพิ่มแถวใหม่ (เช่น บันทึกงานประจำวัน, บันทึกสแกน) |\n| `DELETE_RECORD` | 29 | ลบแถว (เช่น เคลียสรุปจุดส่ง, ล้างข้อมูลเก่า) |\n| `NAVIGATE_APP` | 29 | เปิดหน้าจอ/แอปอื่น (เช่น กดเปิดแผนที่, สลับไปหน้าสรุป) |\n| `EDIT_RECORD` | 28 | เปิดฟอร์มแก้ไขแถว |\n| `EXPORT_VIEW` | 21 | export ข้อมูลเป็น CSV/XLSX — มี action ชื่อลงท้าย `csv` / `xlsx` หลายรายการ (เช่น `SCGนครหลวงJWDภูมิภาค_csv`, `PDFพนักงานcsv`) |\n| `EMAIL` | 12 | ส่งอีเมล (เช่น `Compose Email (Email พนักงาน)`, `Compose Email (Email ผู้อนุมัติ)`, `Compose Email (Scan_By)`) |\n| `REF_ACTION` | 4 | เปิดรายการที่อ้างอิง (`View Ref (...)`) |\n| `COMPOSITE` | 3 | รวมหลายคำสั่ง (เช่น `สร้างใบป่ ะหน้าทุกคน`) |\n| `NAVIGATE_DIFFERENT_APP` | 3 | ข้ามไปแอปอื่น |\n| `NAVIGATE_URL` | 3 | เปิด URL ภายนอก (Google Maps) |\n| `SMS` | 1 | ส่ง SMS (`Send SMS (เบอร์โทรศัพท์)`) |\n| `CALL` | 1 | โทรหา (`Call Phone (เบอร์โทรศัพท์)`) |\n| `ADD_RECORD_TO` | 1 | เพิ่มแถวลงอีกตาราง (`ACT_Create_SCG_Flow`) |\n\n**139 รายการเปลี่ยนแปลงข้อมูล** (`modifies_data = Yes`) — เหล่านี้คือ action ที่เขียนข้อมูลกลับเข้าตาราง\nส่วนที่เหลือเป็น action อ่านอย่างเดียว (ดูรูป, ส่งอีเมล, export)\n\n### action ที่ผูกกับคลัง/สาขาต่าง ๆ (สร้างใบประกาศ)\n\nมี action ชื่อ `สร้างใบป่ ะหน้า_<ชื่อ-นามสกุลพนักงาน>` อย่างน้อย 15 รายการ\n(เช่น `สร้างใบป่ ะหน้า_สำเริง แก้วกามเกตุ`, `สร้างใบป่ ะหน้า_กิตติพงษ์ แหลมผักแว่น`)\n→ เป็นการสร้างเอกสาร "ใบประกาศ/ใบหน้า" รายคน แยกตามผู้รับผิดชอบ\n\n---\n\n## 3. Pipeline map — ข้อมูลในตารางจริงถูกสร้างอย่างไร\n\nลำดับนี้มาจากการไล่เรียง **หลักฐานในไฟล์** (ชื่อบอท, action ที่ผูกกับตาราง, `Ref` ระหว่างตาราง,\nคอลัมน์ที่คำนวณ) ไม่ใช่จากการเดา\n\n```\n① รับงานประจำวัน\n   └─ พนักงาน/ระบบบันทึกงาน → ตารางจริง: ตารางงานประจำวัน (หนึ่งแถว = หนึ่งใบวางบิล)\n      มี: ชื่องาน, ทะเบียนรถ, จุดส่งสินค้าปลายทาง (LatLong), ราคา, สถานะ ScanStatus\n\n② สแกนหน้างาน\n   └─ action "Compose Email (Scan_By)" / ปุ่มสแกน → ตารางจริง: SCGนครหลวงJWDภูมิภาค\n      คำนวณ: ระยะขยับจากจุดเริ่มต้น_เมตร (DISTANCE), ระยะเวลาใช้งาน_นาที,\n             ความเร็วการเคลื่อนที่_เมตร_นาที, ผลการตรวจสอบงานส่ง (PASS/WARNING/FAIL),\n             เหตุผิดปกติที่ตรวจพบ\n\n③ ปริ๊นใบวางบิล  (บอท "ปริ๊นใบวางบิล" + เวอร์ชันต่อคลัง/สาขา)\n   └─ บอท 14 เวอร์ชัน → ตารางบอท (Step Output) → ตารางจริง: ข้อมูลการวางบิล, ปริ๊นใบวางบิล\n\n④ คิดราคา\n   └─ ตารางจริง: ราคาในระบบก่อนส่งสินค้า (ราคาตามระยะทาง + ราคาจุดเพิ่ม + เรทดีเซล)\n      └─ อ้างอิง: ราคาน้ำมันดีเซล, Price_Table, PriceOverride\n\n⑤ ตรวจสอบ/เบิกส่วนต่าง\n   └─ บอท "ทำเบิกส่วนต่างScgวังน้อย" (3 step: ผ่าน/ไม่ผ่าน) → ตารางจริง: ทำเบิกส่วนต่างScgวังน้อย\n   └─ บอท "รับสินค้าคืน" → ตารางจริง: รับงานคืนได้เงิน200\n\n⑥ อนุมัติ\n   └─ action "อนุมัติ" / "รอการอนุมัติ" → SET_COLUMN_VALUE ที่ `สถานะการอนุมัติ`\n      เงื่อนไข: =AND([สถานะการอนุมัติ] <> "อนุมัติ", USERROLE() = "ADMIN")\n\n⑦ สรุป\n   └─ ตารางจริง: สรุป_Shipment, สรุป_เจ้าของสินค้า (ใช้ FILTER จาก ตารางงานประจำวัน)\n   └─ action EXPORT_VIEW (xlsx/csv) → ส่งออกรายงาน\n\n⑧ แจ้งปัญหา\n   └─ บอท Telegram_แจ้งปั ญหา → ตารางจริง: แจ้งปั ญหาระหว่างวัน\n      (มี enum 11 แบบ: สินค้าชำรุด, ถังน้ำมันหนักเกิน, ร้านปิด, ที่อยู่ไม่ตรง ฯลฯ)\n```\n\n### ตารางจริง 29 ตาราง ← บอท/แหล่งที่มีหลักฐานว่าเขียนเข้า\n\n| ตารางจริง | หลักฐานว่ามีอะไรเขียนเข้า |\n|---|---|\n| `ตารางงานประจำวัน` | action `ADD_RECORD` / `EDIT_RECORD` ผูกกับตารางนี้ + `ScanStatus` ถูกอัปเดตโดยบอท "Update ScanStatus เมื่อสแกน Invoice" |\n| `SCGนครหลวงJWDภูมิภาค` | action `Add` (ADD_RECORD) ผูกกับตารางนี้ |\n| `ScanDocs` | บันทึกการสแกนรับ (Scan_Method = Barcode/Manual) — ผูกกับ `ตารางงานประจำวัน` ด้วย `Invoice_No` |\n| `ข้อมูลการวางบิล` | บอทปริ๊นใบวางบิล + การคิดราคา (มี `ราคา` ที่คำนวณจากระยะทาง/จุดเพิ่ม) |\n| `ราคาในระบบก่อนส่งสินค้า` | action ที่เซ็ตราคาก่อนส่ง (`ราคาในระบบหลังส่งสินค้า` ใน format rule) |\n| `รับงานคืนได้เงิน200` | บอท "รับสินค้าคืน" + ค่า enum `สถานะการเข้ารับสินค้า` ที่บอทเขียน |\n| `ทำเบิกส่วนต่างScgวังน้อย` | บอท "ทำเบิกส่วนต่างScgวังน้อย" (3 step) |\n| `แจ้งปั ญหาระหว่างวัน` | บอท Telegram + `Ref` จากบอท `SM_Link` / `RT_Link` |\n| `Doc_Return` | `Ref` จาก `SCGนครหลวงJWDภูมิภาค` (คอลัมน์ `ID_Doc_Return`) — เอกสารคืนสินค้าถูกสร้างจากงานสแกน |\n| `ราคาน้ำมันดีเซล`, `Price_Table`, `PriceOverride` | ตารางตั้งค่าราคา (อัปเดตโดยคน) — มีหลักฐานจาก enum/ชื่อคอลัมน์ `StartDate`/`EndDate` |\n| ตารางอื่น 20 ตาราง | ไม่ปรากฏว่ามีบอทเขียนเข้าในเอกสารนี้ — ให้ถือว่าเป็นตารางที่คนกรอก/คำนวณเอง |\n\n---\n\n## 4. Slices (8) และ Format rules (11)\n\n**Slices** คือมุมมองของตารางเดียวกันที่กรอง/เรียงข้อมูลต่างกัน\n(เช่น `รอการอนุมัติ` กรอง `=USERROLE() = "ADMIN"`)\n\n**Format rules** คือกติกาการเปลี่ยนสี/ตัวหนา/ไอคอนตามเงื่อนไข เช่น\n`อนุมัติ` → ตัวหนาสีเขียว, `รอการอนุมัติ` → สีส้ม, `ผลการตรวจสอบงานส่ง_FAIL` → สีแดง\n→ **AI ที่อ่านข้อมูลต้องรู้ว่าสี/สถานะใน UI ถูกกำหนดโดยกติกาเหล่านี้ ไม่ใช่ข้อมูลดิบ**\n\n---\n\n## 5. วิธีเติมนิยามบอทจริง\n\n1. เปิดแอป → **Automations → Bots** → ดูแต่ละบอท (ชื่อ, trigger, condition, ตารางที่เขียน)\n2. Export เป็นไฟล์ แล้ววางใน `app/automations.json` ในรูปแบบ:\n\n```json\n{\n  "bots": [\n    {\n      "name": "ปริ๊นใบวางบิล",\n      "event": "<ชนิด event>",\n      "condition": "<เงื่อนไข>",\n      "process_table": "Process for ปริ๊นใบวางบิล Process Table",\n      "writes_to": ["ข้อมูลการวางบิล"]\n    }\n  ]\n}\n```\n\n3. ผนวกเข้ากับ `app/actions.csv` เพื่อให้ AI เห็นว่า "อะไรเขียนลงตารางไหน เมื่อไร"\n\n> จนกว่าจะเติม ให้ถือว่า **ทุกข้อความในหน้านี้เป็น "หลักฐานจากชื่อและโครงสร้าง" ไม่ใช่นิยามบอท**\n> ห้ามอ้างว่าบอททำงานเวลาใดหรือทริกเกอร์อะไร เพราะเอกสารไม่มี\n\n---\n\n## 6. ดัชนีตารางบอททั้ง 61 ตาราง\n'


OVERVIEW = '# 00 — ภาพรวมแอป (Overview)\n\n## แอปนี้คืออะไร\n\n**AppSheet app ของ หจก. เผ่าปัญญา ทรานสปอร์ต** — ผู้ให้บริการขนส่งและจัดจำหน่ายโลจิสติกส์\nใช้งานจริงกับลูกค้า **SCG Express / SCGJWD (JWD)** เป็นระบบปฏิบัติการงานส่งสินค้ารายวัน\n\n| | |\n|---|---|\n| ชื่อแอป | เผ่าปั ญญาทรานสปอร์ต |\n| App ID / โฟลเดอร์ | `เผ่าปัญญาทรานสปอร์ต-915154893` |\n| เวอร์ชัน | 1.004638 |\n| เอกสารสร้างเมื่อ | 15/09/2569 02:56 (ตามเวลาไทย) |\n| Function / Runnable | Other / Yes · Deployable: No · Personal use only: No |\n| Data locale | en-GB (บางตารางเป็น th-TH) |\n\n## ขนาดของระบบ\n\n| สิ่ง | จำนวน |\n|---|---:|\n| ตารางทั้งหมด | 90 |\n| ├ ตารางธุรกิจ | 29 |\n| ├ ตารางบอท | 60 |\n| └ ตารางระบบ | 1 |\n| คอลัมน์ | 2304 |\n| คอลัมน์คำนวณอัตโนมัติ | 319 |\n| ความสัมพันธ์ Ref | 80 |\n| Views | 115 |\n| Actions | 214 |\n| Slices | 8 |\n| Format rules | 11 |\n\n## วงจรการทำงานของแอป\n\n```\n① รับงานประจำวัน\n   พนักงานได้รับงานจากลูกค้า → ระบบบันทึกลง "ตารางงานประจำวัน"\n   (หนึ่งแถว = หนึ่งใบวางบิล: ชื่องาน, ทะเบียนรถ, จุดส่ง, ราคา, ScanStatus)\n\n② สแกนหน้างาน\n   พนักงานสแกนใบวางบิลที่ปลายทาง → "SCGนครหลวงJWDภูมิภาค"\n   ระบบคำนวณอัตโนมัติ: ระยะทางที่เคลื่อนที่, เวลาใช้งาน, ความเร็ว\n   และให้คะแนน PASS / WARNING / FAIL + รายการความผิดปกติที่พบ\n\n③ ปริ๊นใบวางบิล\n   บอท 14 เวอร์ชัน (ตามคลัง/สาขา: มโนยนต์, กระสอบ2, ไอโรบอท, เอเทน, MeSpace,\n   บุญถาวรเกษตร, LINEMAN, Thai paper, เบทาโกร, สตีเบล, …)\n   → "ข้อมูลการวางบิล" + "ปริ๊นใบวางบิล"\n\n④ คิดราคา\n   ราคาตามระยะทาง + ราคาจุดเพิ่ม + เรทน้ำมันดีเซล + ราคาคงที่/ที่แทนที่ (PriceOverride)\n   → "ราคาในระบบก่อนส่งสินค้า"\n\n⑤ เบิกส่วนต่าง\n   เทียบราคาในระบบกับราคาจริงหลังส่ง → บอท "ทำเบิกส่วนต่างScgวังน้อย"\n   → "ทำเบิกส่วนต่างScgวังน้อย" (136 คอลัมน์)\n\n⑥ อนุมัติ\n   ผู้ดูแลกดปุ่ม "อนุมัติ" → SET_COLUMN_VALUE ที่ "สถานะการอนุมัติ"\n   (เงื่อนไข: ต้องเป็น ADMIN และยังไม่ได้อนุมัติ)\n\n⑦ รับสินค้าคืน\n   บอท "รับสินค้าคืน" → "รับงานคืนได้เงิน200" (สถานะ 6 แบบ: เพิ่ม 200 / เพิ่ม 50% ฯลฯ)\n\n⑧ สรุปและรายงาน\n   "สรุป_Shipment" / "สรุป_เจ้าของสินค้า" (ใช้ FILTER) → หน้าหลัก → export xlsx/csv\n\n⑨ แจ้งปัญหาระหว่างวัน\n   พนักงานแจ้งปัญหา 11 ประเภท → บอท Telegram → "แจ้งปั ญหาระหว่างวัน"\n```\n\nรายละเอียดและหลักฐานของแต่ละขั้น: [04-bots-and-automations.md](04-bots-and-automations.md)\n\n## กลุ่มตารางธุรกิจ (29 ตาราง)\n\n| กลุ่ม | ตาราง | ความสำคัญ |\n|---|---|---|\n| งานประจำวัน | `ตารางงานประจำวัน` (40) | **แกนกลางของทั้งระบบ** — ทุกอย่างอ้างอิงกลับมาที่นี่ |\n| สแกน | `SCGนครหลวงJWDภูมิภาค` (49), `ScanDocs` (18), `ส่งงานที่ยังไม่มีข้อมูลในระบบ` (15) | บันทึกหลักฐานการส่ง |\n| บิล/ราคา | `ข้อมูลการวางบิล` (45), `ปริ๊นใบวางบิล` (11), `ราคาในระบบก่อนส่งสินค้า` (15), `ราคาน้ำมันดีเซล` (4), `Price_Table` (8), `PriceOverride` (7) | วงจรราคา |\n| เบิก | `ทำเบิกส่วนต่างScgวังน้อย` (136), `สรุปเบิกส่วนต่าง` (12), `รับงานคืนได้เงิน200` (29) | เทียบราคาจริงกับราคาในระบบ |\n| คน/รถ | `ข้อมูลพนักงาน` (17), `ข้อมูลงานRT` (12), `ข้อมูลงานRW` (15), `ข้อมูลการเข้าบำรุงรักษา` (14), `ข้อมูลชื่องานต้นทางปลายทาง` (9) | มิติประกอบ |\n| เอกสาร | `Doc_Return` (7), `Image_Doc_Return` (4), `PDFพนักงาน` (11), `Announcements` (7), `Acknowledge_Logs` (11), `แจ้งปั ญหาระหว่างวัน` (29) | เอกสาร/ประกาศ/ปัญหา |\n| มุมมอง | `สรุป_Shipment` (14), `สรุป_เจ้าของสินค้า` (13), `หน้าหลัก` (4), `FILTER` (14) | dashboard + ตัวกรอง |\n\n## โมเดลความปลอดภัย\n\n| ระดับ | กลไก |\n|---|---|\n| ระดับแถว (Row Security) | `=OR(USERROLE() = "ADMIN", [Email พนักงาน] = USEREMAIL())` — พนักงานเห็นเฉพาะแถวของตัวเอง ผู้ดูแล (ADMIN) เห็นทั้งหมด |\n| ระดับคอลัมน์ | `Editable_If = =USERROLE()="ADMIN"` บนคอลัมน์ราคา/พิกัด → พนักงานแก้ไขไม่ได้ |\n| ระดับการมองเห็น | `Show_If` เช่น `=ISNOTBLANK([InvoiceNo])` → ซ่อนข้อมูลที่ยังไม่พร้อม |\n| ระดับการบังคับ | `Required_If` + `Error_Message_If_Invalid` เช่น "Invoice นี้ไม่ถูกต้อง, ไม่ใช่งานวันที่เลือก หรือสแกนรับไปแล้ว" |\n\nตารางที่มี security filter: `SCGนครหลวงJWDภูมิภาค`, `ข้อมูลการวางบิล`, `ข้อมูลการเข้าบำรุงรักษา`,\n`ตารางงานประจำวัน`, `แจ้งปั ญหาระหว่างวัน`, `รับงานคืนได้เงิน200`, `ทำเบิกส่วนต่างScgวังน้อย`\n(ดูคอลัมน์ `security_filter` ใน `app/tables.csv`)\n\n## ข้อจำกัดของชุดข้อมูลนี้\n\n1. **ไม่มีข้อมูลระดับแถว** — มีแต่โครงสร้าง ตัวเลขทางธุรกิจยังคำนวณไม่ได้\n2. **ไม่มีนิยามบอท** — AppSheet Application Documentation ไม่มีส่วน Automation/Bot\n3. **ตารางบอทเป็น state machine** — ห้ามนับแถวจากตารางบอท\n4. **มี PII** — ชื่อ-นามสกุล, เบอร์โทร, ทะเบียนรถ, GPS, ที่อยู่, ข้อมูลลูกค้า\n5. **สูตรมาจากการคัดลอกจาก PDF** — บางจุดอาจมีช่องว่าง/อักขระเพี้ยนจากต้นฉบับ\n   ถ้าจะใช้สูตรจริงให้ยืนยันใน AppSheet อีกครั้ง\n6. **ยังไม่มีข้อมูลจาก Google Sheet** — ต้อง export ตาม `data/README.md`\n\n## อ่านต่อ\n\n* โครงสร้างทุกคอลัมน์ → [01a-data-dictionary-business.md](01a-data-dictionary-business.md)\n* ตารางบอท → [01b-data-dictionary-bot.md](01b-data-dictionary-bot.md)\n* ความสัมพันธ์ → [02-erd.md](02-erd.md)\n* สูตรทั้งหมด → [03-formulas.md](03-formulas.md)\n* บอทและ pipeline → [04-bots-and-automations.md](04-bots-and-automations.md)\n* ศัพท์ → [05-glossary.md](05-glossary.md)\n* คู่มือ AI → [../AGENTS.md](../AGENTS.md)\n'


def overview_doc(meta: dict, tables: list[dict], cols: list[dict]) -> str:
    """Curated narrative overview (maintained by hand, embedded here so the
    generator can rebuild it byte-identically)."""
    return OVERVIEW


def erd_doc(tables: list[dict], relations: list[dict]) -> str:
    """ERD: mermaid diagram + every relation."""
    biz = {t["name"] for t in tables if t["kind"] == "business"}
    used: dict[str, str] = {}

    def mname(name: str) -> str:
        base = re.sub(r"[^A-Za-z0-9_]", "_", name)
        if not base or not base[0].isalpha():
            base = "T_" + base
        if base in used and used[base] != name:
            n = 2
            while f"{base}_{n}" in used:
                n += 1
            base = f"{base}_{n}"
        used[base] = name
        return base

    out = []
    out.append("# 05 - ความสัมพันธ์ของข้อมูล (ERD)")
    out.append("")
    out.append(f"ทั้งหมด {len(relations)} ความสัมพันธ์เป็นแบบ **many-to-one** "
               "(ลูกค้าหนึ่งแถวอ้างอิงแม่หนึ่งแถว) "
               "ไม่มี many-to-many โดยตรง")
    out.append("")
    out.append("## แผนภาพ (ตารางจริง)")
    out.append("")
    out.append("```mermaid")
    out.append("erDiagram")
    for t in sorted(biz):
        out.append(f"    {mname(t)} {{")
        out.append("        string _key")
        out.append("    }")
    for r in relations:
        if r["from_table"] not in biz or r["to_table"] not in biz:
            continue
        out.append(f"    {mname(r['from_table'])} }}o--|| {mname(r['to_table'])} "
                   f": \"{r['from_column']}\"")
    out.append("```")
    out.append("")
    out.append("## ตารางความสัมพันธ์ทั้งหมด")
    out.append("")
    out.append("| จากตาราง | คอลัมน์ | -> ตาราง | key ของปลายทาง | ชนิดตารางปลายทาง |")
    out.append("|---|---|---|---|---|")
    for r in relations:
        out.append(f"| `{esc(r['from_table'])}` | `{esc(r['from_column'])}` "
                   f"| `{esc(r['to_table'])}` | `{esc(r['to_key_column'])}` "
                   f"| {r.get('to_kind','')} |")
        out.append(f"<!-- rel: {r['from_table']} -> {r['to_table']} -->")
    out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    tables = read_csv(REPO / "app" / "tables.csv")
    columns = read_csv(REPO / "app" / "columns.csv")
    relations = read_csv(REPO / "app" / "relations.csv")
    views = read_csv(REPO / "app" / "views.csv")
    actions = read_csv(REPO / "app" / "actions.csv")
    slices = read_csv(REPO / "app" / "slices.csv")
    rules = read_csv(REPO / "app" / "format_rules.csv")
    meta = json.loads((REPO / "app" / "meta.json").read_text(encoding="utf-8"))

    cols_by_table: dict[str, list[dict]] = defaultdict(list)
    for c in columns:
        cols_by_table[c["table"]].append(c)
    for lst in cols_by_table.values():
        lst.sort(key=lambda c: int(c["index"] or 0))

    rels_out: dict[str, list[dict]] = defaultdict(list)
    rels_in: dict[str, list[dict]] = defaultdict(list)
    for r in relations:
        rels_out[r["from_table"]].append(r)
        rels_in[r["to_table"]].append(r)

    files: dict[Path, str] = {}

    files[DOCS / "00-overview.md"] = overview_doc(meta, tables, columns)
    files[DOCS / "01-main-tables.md"] = main_tables_index(tables, cols_by_table)
    files[DOCS / "02-process-output-tables.md"] = (
        BOT_ANALYSIS + "\n---\n\n" + process_tables_index(tables, cols_by_table))
    files[DOCS / "03-columns-and-formulas.md"] = columns_and_formulas(tables, cols_by_table)
    files[DOCS / "04-views-actions-rules-slices.md"] = ux_layer(views, actions, rules, slices, tables)
    files[DOCS / "05-erd.md"] = erd_doc(tables, relations)

    for t in tables:
        cols = cols_by_table.get(t["name"], [])
        if t["kind"] == "business":
            files[DOCS / "tables" / f"{slug(t['name'])}.md"] = table_doc(
                t, cols, rels_out.get(t["name"], []), rels_in.get(t["name"], []), "business")
        else:
            files[DOCS / "process-tables" / f"{slug(t['name'])}.md"] = bot_doc(t, cols)

    for r in rules:
        files[DOCS / "rules" / f"{slug(r['name'])}.md"] = rule_doc(r, tables)

    diffs = []
    for path, text in sorted(files.items()):
        cur = path.read_text(encoding="utf-8") if path.exists() else None
        if cur == text:
            continue
        diffs.append(path)
        if not args.check:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")

    if args.check:
        print(f"DIFF {len(diffs)} file(s)")
        for p in diffs[:10]:
            print("  ", p.relative_to(REPO))
    else:
        print(f"wrote {len(files) - len(diffs)} file(s), {len(diffs)} unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
