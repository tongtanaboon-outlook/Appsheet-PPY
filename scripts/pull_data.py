#!/usr/bin/env python3
"""
Pull the actual row data of the app's business tables.

Three ingestion paths, in order of preference:

1. Google Sheets (recommended, fastest, complete)
      The 29 business tables are Google-Sheet backed ("Data Source = google").
      One spreadsheet holds them as worksheets. Export with a service account:
        python scripts/pull_google_sheets.py --spreadsheet-id <ID> --out data/

2. AppSheet REST API (no Google credentials needed)
      Uses the AppSheet API key + app id from the app URL:
        https://appsheet.app/<APP_ID>?appServiceId=<API_KEY>
        python scripts/pull_appsheet_data.py --app-id <ID> --api-key <KEY>

3. Manual export (no credentials at all)
      In the app: Data -> ... -> Export -> CSV, once per table, then drop the
      files into data/ using the file names listed in data/manifest.json.

Everything lands in data/<table-slug>.csv with the column names of
app/columns.csv, so scripts/validate_repo.py can check the result.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def slug(name: str) -> str:
    s = re.sub(r"[^\w฀-๿]+", "_", name, flags=re.UNICODE).strip("_")
    return s or "table"


def load_schema():
    meta = json.loads((REPO / "app" / "meta.json").read_text(encoding="utf-8"))
    tables = list(csv.DictReader((REPO / "app" / "tables.csv").open(encoding="utf-8")))
    columns = list(csv.DictReader((REPO / "app" / "columns.csv").open(encoding="utf-8")))
    return meta, tables, columns


# --------------------------------------------------------------------------
# 1) Google Sheets
# --------------------------------------------------------------------------

def pull_google_sheets(spreadsheet_id: str, out_dir: Path, sheets_title: str | None) -> int:
    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
    except ImportError:
        print("pip install google-api-python-client google-auth", file=sys.stderr)
        return 2

    key_file = REPO / "config.local.json"
    if not key_file.exists():
        print(f"missing {key_file} (see data/README.md)", file=sys.stderr)
        return 2
    cfg = json.loads(key_file.read_text(encoding="utf-8"))
    creds = Credentials.from_service_account_info(cfg, scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
    svc = build("sheets", "v4", credentials=creds)

    _, tables, columns = load_schema()
    by_table: dict[str, list[dict]] = {}
    for c in columns:
        by_table.setdefault(c["table"], []).append(c)

    written = 0
    for t in tables:
        if t["kind"] != "business":
            continue
        title = t["worksheet_name"] or t["name"]
        if sheets_title and title != sheets_title:
            continue
        try:
            values = svc.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id, range=f"'{title}'").execute().get("values", [])
        except urllib.error.HTTPError as exc:
            print(f"  ! {title}: {exc}", file=sys.stderr)
            continue
        if not values:
            print(f"  - {title}: empty")
            continue
        header = values[0]
        rows = values[1:]
        cols = by_table.get(t["name"], [])
        target = out_dir / f"{slug(t['name'])}.csv"
        out_dir.mkdir(parents=True, exist_ok=True)
        with target.open("w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(header)
            w.writerows(rows)
        print(f"  + {title}: {len(rows)} rows -> {target.name}")
        written += 1
    return 0 if written else 1


# --------------------------------------------------------------------------
# 2) AppSheet REST API
# --------------------------------------------------------------------------

APPSHEET_API = "https://api.appsheet.com/v2/apps/{app_id}/tables/{table}/rows"


def appsheet_request(app_id: str, api_key: str, table: str) -> list[dict]:
    url = APPSHEET_API.format(app_id=app_id, table=urllib.parse.quote(table))
    req = urllib.request.Request(url + "?key=" + urllib.parse.quote(api_key))
    with urllib.request.urlopen(req, timeout=60) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    return payload.get("rows", [])


def pull_appsheet(app_id: str, api_key: str, out_dir: Path) -> int:
    _, tables, columns = load_schema()
    by_table: dict[str, list[dict]] = {}
    for c in columns:
        by_table.setdefault(c["table"], []).append(c)
    out_dir.mkdir(parents=True, exist_ok=True)
    ok = 0
    for t in tables:
        if t["kind"] != "business":
            continue
        try:
            rows = appsheet_request(app_id, api_key, t["name"])
        except urllib.error.HTTPError as exc:
            print(f"  ! {t['name']}: HTTP {exc.code}", file=sys.stderr)
            continue
        except Exception as exc:                      # noqa: BLE001
            print(f"  ! {t['name']}: {exc}", file=sys.stderr)
            continue
        if not rows:
            print(f"  - {t['name']}: 0 rows")
            continue
        cols = [c["name"] for c in by_table.get(t["name"], [])]
        target = out_dir / f"{slug(t['name'])}.csv"
        with target.open("w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(cols)
            for row in rows:
                w.writerow([row.get(c, "") for c in cols])
        print(f"  + {t['name']}: {len(rows)} rows -> {target.name}")
        ok += 1
        time.sleep(0.3)                              # be gentle with the API
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mode", choices=["sheets", "appsheet"], default="sheets")
    ap.add_argument("--spreadsheet-id")
    ap.add_argument("--app-id")
    ap.add_argument("--api-key")
    ap.add_argument("--out", default=str(REPO / "data"))
    args = ap.parse_args()
    out_dir = Path(args.out)

    if args.mode == "sheets":
        if not args.spreadsheet_id:
            ap.error("--spreadsheet-id is required")
        return pull_google_sheets(args.spreadsheet_id, out_dir, None)
    if not args.app_id or not args.api_key:
        ap.error("--app-id and --api-key are required")
    return pull_appsheet(args.app_id, args.api_key, out_dir)


if __name__ == "__main__":
    raise SystemExit(main())
