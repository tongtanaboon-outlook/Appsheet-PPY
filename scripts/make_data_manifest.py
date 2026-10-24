#!/usr/bin/env python3
"""Generate data/manifest.json: the contract between the schema and the CSVs."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def slug(name: str) -> str:
    s = re.sub(r"[^\w฀-๿]+", "_", name, flags=re.UNICODE).strip("_")
    return s or "table"


def main() -> int:
    tables = list(csv.DictReader((REPO / "app" / "tables.csv").open(encoding="utf-8")))
    columns = list(csv.DictReader((REPO / "app" / "columns.csv").open(encoding="utf-8")))
    by_table: dict[str, list[dict]] = {}
    for c in columns:
        by_table.setdefault(c["table"], []).append(c)

    out: dict[str, dict] = {}
    for t in tables:
        if t["kind"] != "business":
            continue
        cols = by_table.get(t["name"], [])
        out[slug(t["name"])] = {
            "table_name": t["name"],
            "worksheet_name": t["worksheet_name"],
            "file": f"{slug(t['name'])}.csv",
            "columns": [c["name"] for c in cols],
            "column_count": len(cols),
            "rows": None,
            "source": "pending",
        }
    manifest = {
        "description": "Row-level data of the business tables of the AppSheet app. "
                       "File name = slug of the AppSheet table name; column order "
                       "matches app/columns.csv.",
        "generated_by": "scripts/make_data_manifest.py",
        "tables": out,
    }
    (REPO / "data" / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(out)} business tables declared in data/manifest.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
