#!/usr/bin/env python3
"""
Build the GitHub-ready schema layer from the extracted AppSheet structure.

Input : schema_raw.json (output of extract_appsheet.py)
Output: app/*.json|csv  - machine readable schema
        docs/_generated/* - generated tables used by the docs pipeline
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path

APP_NAME = "เผ่าปัญญาทรานสปอร์ต"
APP_ID = "เผ่าปั ญญาทรานสปอร์ต-915154893"
APP_VERSION = "1.004638"
PDF_GENERATED = "2026-09-15T02:56:32+07:00"

BOT_MARKERS = ("process for ", " output", "step output")
BOT_TABLES = {
    "Process for ปริ๊นใบวางบิล Process Table",
    "Process for ปริ๊นใบวางบิล_คลังSCGJWDวังน้อย Process Table",
    "Process for ปริ๊นใบวางบิล_เบทาโกร+เหมาตู้ Process Table",
    "Process for ปริ๊นใบวางบิล_โอนคลัง กระสอบ2(บางบัวทอง)",
    "Process for ปริ๊นใบวางบิล_โอนคลัง บุญถาวร เกษตร_นวมิ นทร์ - 1 Process Table",
    "Process for ปริ๊นใบวางบิล_โอนคลัง เอเธน Process Table",
    "Process for ปริ๊นใบวางบิล_รับเอกสาร (งานพี่เหน่ง) Process Table",
    "Process for ปริ๊นใบวางบิล_รับเอกสาร (งานพี่เหน่ง) สตีเบล",
    "Process for ปริ๊นใบวางบิล_ไอโรบอท Process Table",
    "Process for ปริ๊นใบวางบิลเอเทน - 1 Process Table",
    "Process for ปริ๊นใบวางบิลโอนคลัง มโนยนต์ (นวนคร)",
    "Process for สรุปจำนวนจุดที่ส่งงานSCGวังน้อย Process Table",
    "Process for สรุปส่วนต่าง - 1 Process Table",
    "Process for ทำเบิกค่ายกขึ้นชั้น Process Table",
    "Process for ทำเบิกส่วนต่างScgวังน้อย - 1 Process Table",
    "Process for ได้เพิ่ม25%ของค่าเที่ยว Process Table",
    "Process for ได้เพิ่ม200_ไม่มีสินค้าคืน_ร้านปิ ด_ไม่มีในจุดส่ง",
    "Process for เพิ่มรูปรับคืน - 1 Process Table",
    "Process for ใบป่ ะหน้า - 1 Process Table",
    "Process for โอนคลัง (GQ) จีคิว Process Table",
    "Process for ฺBot_4ตัว_จัดเรียงเส้นทาง Process Table",
    "Process for Bot_รับสินค้าคืน - 1 Process Table",
    "Process for Bot_เบิกค่าขนส่งตามระยะทาง - 1 Process Table",
    "Process for Telegram_แจ้งปั ญหา - 1 Process Table",
    "Process for MeSpace Process Table",
    "Process for New bot - 1 Process Table",
    "Process for AppSheet_KM - 1 Process Table",
    "Process for Update ScanStatus เมื่อสแกน Invoice - 1 Process Table",
    "Process for ปริ๊นใบวางบิล_LINEMAN (6W) (SCG Express)",
    "Process for ปริ๊นใบวางบิล_Thai paper (SCG Express) - 1",
}


def classify(table: dict) -> str:
    """business | bot | system."""
    name = table["name"]
    low = name.lower()
    if table.get("source_path", "").startswith("/ProcessStateTables/"):
        return "bot"
    if name in BOT_TABLES or any(m in low for m in BOT_MARKERS):
        return "bot"
    if name == "_Per User Settings":
        return "system"
    if table.get("data_source") in ("google", "google_tables"):
        return "business"
    return "bot"


def slug(name: str) -> str:
    s = re.sub(r"[^\w฀-๿]+", "_", name, flags=re.UNICODE).strip("_")
    return s or "table"


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main() -> int:
    src = Path(sys.argv[1])
    out = Path(sys.argv[2])
    data = json.loads(src.read_text(encoding="utf-8"))

    tables = data["tables"]
    columns = data["columns"]
    kind_by_table = {t["name"]: classify(t) for t in tables}

    # ---------------- tables ----------------
    table_rows = []
    for t in tables:
        kind = kind_by_table[t["name"]]
        cols = [c for c in columns if c["table"] == t["name"]]
        table_rows.append(OrderedDict([
            ("name", t["name"]),
            ("kind", kind),
            ("slug", slug(t["name"])),
            ("visible", t["visible"]),
            ("shared", t["shared"]),
            ("data_source", t["data_source"]),
            ("worksheet_name", t["worksheet_name"]),
            ("source_path", t["source_path"]),
            ("data_locale", t["data_locale"]),
            ("updates_allowed", t["updates_allowed"]),
            ("update_mode_expression", t["update_mode_expression"]),
            ("security_filter", t["security_filter"]),
            ("column_count", len(cols)),
            ("formula_column_count", sum(1 for c in cols if c["app_formula"])),
            ("computed_column_count", sum(1 for c in cols
                                          if c["app_formula"] or c["initial_value"])),
            ("ref_column_count", sum(1 for c in cols if c["type"] == "Ref")),
        ]))
    write_csv(out / "app" / "tables.csv", table_rows)

    # ---------------- columns ----------------
    col_rows = []
    for c in columns:
        tq = c["type_qualifier"] or {}
        ref_to = tq.get("ReferencedTableName", "") or ""
        col_rows.append(OrderedDict([
            ("table", c["table"]),
            ("table_kind", kind_by_table.get(c["table"], "")),
            ("index", c["index"]),
            ("name", c["name"]),
            ("type", c["type"]),
            ("description", c.get("description", "")),
            ("app_formula", c["app_formula"]),
            ("initial_value", c["initial_value"]),
            ("reset_on_edit", c["reset_on_edit"]),
            ("key", c["key"]),
            ("part_of_key", c["part_of_key"]),
            ("hidden", c["hidden"]),
            ("read_only", c["read_only"]),
            ("searchable", c["searchable"]),
            ("scannable", c["scannable"]),
            ("sensitive_data", c["sensitive_data"]),
            ("ref_table", ref_to),
            ("ref_key_column", tq.get("ReferencedKeyColumn", "") or ""),
            ("valid_if", tq.get("Valid_If", "") or ""),
            ("required_if", tq.get("Required_If", "") or ""),
            ("editable_if", tq.get("Editable_If", "") or ""),
            ("show_if", tq.get("Show_If", "") or ""),
            ("error_message_if_invalid", tq.get("Error_Message_If_Invalid", "") or ""),
            ("suggested_values", tq.get("Suggested_Values", "") or ""),
            ("enum_values", tq.get("EnumValues", "") or ""),
            ("type_qualifier_raw", c["type_qualifier_raw"]),
        ]))
    write_csv(out / "app" / "columns.csv", col_rows)

    # ---------------- computed columns ----------------
    computed = [r for r in col_rows if r["app_formula"] or r["initial_value"]]
    write_csv(out / "app" / "computed_columns.csv", computed)

    # ---------------- relations ----------------
    rel_rows = []
    for r in col_rows:
        if r["type"] == "Ref" and r["ref_table"]:
            rel_rows.append(OrderedDict([
                ("from_table", r["table"]),
                ("from_kind", r["table_kind"]),
                ("from_column", r["name"]),
                ("to_table", r["ref_table"]),
                ("to_kind", kind_by_table.get(r["ref_table"], "")),
                ("to_key_column", r["ref_key_column"]),
                ("direction", "many-to-one"),
            ]))
    write_csv(out / "app" / "relations.csv", rel_rows)

    # ---------------- views / actions / slices / rules ----------------
    def flat(rows, drop=()):
        out_rows = []
        for row in rows:
            o = OrderedDict()
            for k, v in row.items():
                if k in drop:
                    continue
                if isinstance(v, (dict, list)):
                    v = json.dumps(v, ensure_ascii=False)
                o[k] = v
            out_rows.append(o)
        return out_rows

    write_csv(out / "app" / "views.csv", flat(data["views"]))
    write_csv(out / "app" / "actions.csv", flat(data["actions"]))
    write_csv(out / "app" / "slices.csv", flat(data["slices"]))
    write_csv(out / "app" / "format_rules.csv", flat(data["format_rules"]))

    # ---------------- table groups ----------------
    groups = OrderedDict()
    for kind in ("business", "bot", "system"):
        groups[kind] = [t["name"] for t in tables if kind_by_table[t["name"]] == kind]
    (out / "app" / "table_groups.json").write_text(
        json.dumps(groups, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---------------- meta ----------------
    meta = OrderedDict([
        ("app_name", APP_NAME),
        ("app_id", APP_ID),
        ("app_version", APP_VERSION),
        ("app_folder", f"/appsheet/data/{APP_ID}"),
        ("function", "Other"),
        ("runnable", True),
        ("deployable", False),
        ("personal_use_only", False),
        ("documentation_generated_at", PDF_GENERATED),
        ("source_document", "Application Documentation.PDF"),
        ("counts", OrderedDict([
            ("tables", len(tables)),
            ("business_tables", len(groups["business"])),
            ("bot_tables", len(groups["bot"])),
            ("system_tables", len(groups["system"])),
            ("columns", len(columns)),
            ("computed_columns", len(computed)),
            ("relations", len(rel_rows)),
            ("views", len(data["views"])),
            ("actions", len(data["actions"])),
            ("slices", len(data["slices"])),
            ("format_rules", len(data["format_rules"])),
        ])),
    ])
    (out / "app" / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---------------- full tables.json ----------------
    full = OrderedDict()
    for t in tables:
        cols = [c for c in columns if c["table"] == t["name"]]
        full[t["name"]] = OrderedDict([
            ("kind", kind_by_table[t["name"]]),
            ("table", t),
            ("columns", cols),
        ])
    (out / "app" / "tables.json").write_text(
        json.dumps(full, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(meta["counts"], indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
