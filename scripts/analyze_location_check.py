#!/usr/bin/env python3
"""
Measure the real distance distribution before enforcing the 20 m rule.

Why this exists
---------------
Enforcing "LatLong_Actual vs จุดส่งสินค้าปลายทาง <= 20 m" will block real
deliveries if the GPS at the drop point is noisy, or if the join points at the
wrong drop point of a multi-stop shipment. This script answers three
questions on the *actual* data before you turn the block on:

  1. What share of rows even has LatLong_Actual? (blank -> no check, no block)
  2. How far apart are the two points, really? (distribution + how many rows
     would be blocked at 20 / 30 / 50 / 100 m)
  3. Does the join key point at the right drop point? (compare the drop name
     coming through MATCH_KEY vs the drop name on the scan row)

Usage
-----
    python3 scripts/analyze_location_check.py --data data
    python3 scripts/analyze_location_check.py --data data --out report.json

Expects the exported CSVs from data/ (see data/README.md):
    <ตารางงานประจำวัน>.csv
    <SCGนครหลวงJWDภูมิภาค>.csv
Column names are matched loosely so a renamed column still resolves.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

DAILY_TABLE = "ตารางงานประจำวัน"
SCAN_TABLE = "SCGนครหลวงJWDภูมิภาค"

THRESHOLDS = [20, 30, 50, 100, 200]
EARTH_R = 6_371_000.0


# ---------------------------------------------------------------- helpers

def load_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def find_csv(data_dir: Path, table: str) -> Path | None:
    """Find the CSV of a table by slug or by exact name."""
    for p in sorted(data_dir.glob("*.csv")):
        if p.stem == table:
            return p
    slug = "".join(c if c.isalnum() else "_" for c in table)
    for p in sorted(data_dir.glob("*.csv")):
        if p.stem == slug or slug in p.stem:
            return p
    return None


def col(row: dict, *candidates: str) -> str:
    """Fetch a column value, tolerating whitespace/case differences."""
    keys = {k.strip().lower(): k for k in row}
    for c in candidates:
        v = keys.get(c.strip().lower())
        if v is not None:
            return (row[v] or "").strip()
    return ""


def parse_latlong(value: str) -> tuple[float, float] | None:
    """Accept (lat, long), lat,long and plain text."""
    s = (value or "").strip().strip("()").replace(";", ",")
    if not s:
        return None
    parts = [p.strip() for p in s.split(",") if p.strip()]
    if len(parts) < 2:
        return None
    try:
        lat, lon = float(parts[0]), float(parts[1])
    except ValueError:
        return None
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        return None
    if lat == 0 and lon == 0:
        return None
    return lat, lon


def haversine_m(a: tuple[float, float], b: tuple[float, float]) -> float:
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = (math.sin(dlat / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2)
    return 2 * EARTH_R * math.asin(min(1.0, math.sqrt(h)))


def percentile(values: list[float], q: float) -> float:
    if not values:
        return float("nan")
    s = sorted(values)
    k = (len(s) - 1) * q
    f, c = math.floor(k), math.ceil(k)
    return s[f] if f == c else s[f] * (c - k) + s[c] * (k - f)


# ---------------------------------------------------------------- analysis

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(REPO / "data"))
    ap.add_argument("--out")
    ap.add_argument("--join-key", default="SM_Link_SCG",
                    help="คอลัมน์ในชีต SCG ที่ชี้กลับไปแถวของชีตงานประจำวัน "
                         "(ค่าเริ่มต้น = SM_Link_SCG ซึ่งเป็น Ref ตัวเดียวกับที่แอปใช้)")
    args = ap.parse_args()
    data_dir = Path(args.data)

    daily_path = find_csv(data_dir, DAILY_TABLE)
    scan_path = find_csv(data_dir, SCAN_TABLE)
    if not daily_path or not scan_path:
        print("ไม่พบไฟล์ CSV ของตารางที่ต้องการ", file=sys.stderr)
        print(f"  ต้องมี: {DAILY_TABLE}.csv และ {SCAN_TABLE}.csv ใน {data_dir}",
              file=sys.stderr)
        print("  ดูวิธี export ได้ที่ data/README.md", file=sys.stderr)
        return 2

    daily = load_csv(daily_path)
    scan = load_csv(scan_path)
    print(f"อ่านแล้ว: {daily_path.name} ({len(daily)} แถว) · {scan_path.name} ({len(scan)} แถว)")
    print()

    # --- index the daily table the same way the app does ------------------
    # The SCG sheet pulls from ตารางงานประจำวัน through the Ref column
    # SM_Link_SCG (its value is the daily table key ID_งานประจำวัน).
    # That is the join we must measure - not MATCH_KEY, which is a different
    # mechanism inside the app.
    by_ref: dict[str, dict] = {}
    by_invoice_first: dict[str, dict] = {}
    for row in daily:
        key = col(row, "ID_งานประจำวัน")
        if key and key not in by_ref:
            by_ref[key] = row
        inv = col(row, "Invoice No")
        if inv and inv not in by_invoice_first:
            by_invoice_first[inv] = row

    stats = Counter()
    dist_match: list[float] = []
    dist_invoice: list[float] = []
    wrong_drop_name = 0
    compared_names = 0
    worst: list[tuple[float, str, str]] = []

    for row in scan:
        stats["scan_rows"] += 1
        ref_key = col(row, args.join_key)
        actual = parse_latlong(col(row, "จุดส่งสินค้าปลายทาง"))
        if actual is None:
            stats["scan_without_point"] += 1
            continue
        if not ref_key:
            stats["scan_without_match_key"] += 1
            continue

        d_row = by_ref.get(ref_key)
        if d_row is None:
            stats["match_key_not_found"] += 1
            continue
        stats["matched"] += 1

        ref = parse_latlong(col(d_row, "LatLong_Actual"))
        if ref is None:
            stats["daily_without_latlong_actual"] += 1
            continue
        stats["comparable"] += 1

        dist = haversine_m(actual, ref)
        dist_match.append(dist)

        # does MATCH_KEY point at the same drop as the scan row?
        scan_drop = col(row, "ชื่อปลายทาง")
        daily_drop = col(d_row, "ชื่อปลายทาง")
        if scan_drop and daily_drop:
            compared_names += 1
            if scan_drop.strip() != daily_drop.strip():
                wrong_drop_name += 1

        # same comparison but with the "first row of the invoice" join
        inv = col(row, "Invoice No")
        if inv and inv in by_invoice_first:
            d2 = by_invoice_first[inv]
            ref2 = parse_latlong(col(d2, "LatLong_Actual"))
            if ref2:
                dist_invoice.append(haversine_m(actual, ref2))

        worst.append((dist, col(row, "Invoice No"), col(row, "ชื่อปลายทาง")))

    worst.sort(reverse=True)

    # ------------------------------------------------------------- report
    print("=" * 66)
    print("ผลการวิเคราะห์ระยะทาง (LatLong_Actual vs จุดส่งสินค้าปลายทาง)")
    print("=" * 66)
    print(f"วิธีจับคู่: {args.join_key} (ค่าในคอลัมน์นี้ต้อง = ID_งานประจำวัน ของชีตงานประจำวัน)")
    print(f"แถวในชีตสแกน              : {stats['scan_rows']:,}")
    print(f"  ไม่มีพิกัดจุดส่งสินค้าปลายทาง: {stats['scan_without_point']:,}")
    print(f"  ไม่มี {args.join_key:20s}: {stats['scan_without_match_key']:,}")
    print(f"  จับคู่ {args.join_key} ไม่เจอแถว: {stats['match_key_not_found']:,}")
    print(f"  จับคู่ได้                 : {stats['matched']:,}")
    print(f"  แต่แถวนั้นไม่มี LatLong_Actual: {stats['daily_without_latlong_actual']:,}")
    print(f"  **เทียบได้จริง**          : {stats['comparable']:,}")
    print()

    if dist_match:
        n = len(dist_match)
        print(f"ระยะทาง (เมตร) — n = {n:,}")
        print(f"  มัธยฐาน        : {percentile(dist_match, .5):8.1f} m")
        print(f"  p75             : {percentile(dist_match, .75):8.1f} m")
        print(f"  p90             : {percentile(dist_match, .90):8.1f} m")
        print(f"  p95             : {percentile(dist_match, .95):8.1f} m")
        print(f"  p99             : {percentile(dist_match, .99):8.1f} m")
        print(f"  สูงสุด          : {max(dist_match):8.1f} m")
        print()
        print("  จะถูกบล็อกที่เกณฑ์    จำนวนแถว        สัดส่วน")
        for t in THRESHOLDS:
            c = sum(1 for d in dist_match if d > t)
            print(f"    > {t:>3} ม.        {c:>8,}        {c/n*100:6.2f}%")
    else:
        print("!! ยังไม่มีแถวไหนเทียบได้เลย — ตรวจ MATCH_KEY / LatLong_Actual ก่อน")

    print()
    if compared_names:
        print(f"ตรวจชื่อจุดส่ง: เทียบ {compared_names:,} แถว · ไม่ตรงกัน {wrong_drop_name:,} แถว"
              f" ({wrong_drop_name/compared_names*100:.2f}%)")
        if wrong_drop_name:
            print("  → MATCH_KEY ชี้จุดส่งคนละจุดกับแถวสแกนในบางส่วน "
                  "= ต้องตรวจวิธีจับคู่ก่อนบังคับ")
    else:
        print("ตรวจชื่อจุดส่ง: เทียบไม่ได้ (ไม่มีชื่อปลายทางในข้อมูล)")

    if dist_invoice:
        print()
        print(f"เทียบกับการจับคู่แบบ 'แถวแรกของ Invoice' (วิธีเดิม): "
              f"p50 = {percentile(dist_invoice, .5):.1f} m · "
              f"p95 = {percentile(dist_invoice, .95):.1f} m")

    if worst:
        print()
        print("ตัวอย่างที่ห่างที่สุด 5 แถว (ตรวจด้วยตาตา):")
        for d, inv, drop in worst[:5]:
            print(f"  {d:9.1f} m | Invoice {inv or '-'} | {drop or '-'}")

    report = {
        "scan_rows": stats["scan_rows"],
        "comparable": stats["comparable"],
        "matched": stats["matched"],
        "match_key_not_found": stats["match_key_not_found"],
        "daily_without_latlong_actual": stats["daily_without_latlong_actual"],
        "scan_without_match_key": stats["scan_without_match_key"],
        "drop_name_mismatch": wrong_drop_name,
        "drop_name_compared": compared_names,
        "distance_m": {
            "p50": percentile(dist_match, .5) if dist_match else None,
            "p90": percentile(dist_match, .90) if dist_match else None,
            "p95": percentile(dist_match, .95) if dist_match else None,
            "p99": percentile(dist_match, .99) if dist_match else None,
            "max": max(dist_match) if dist_match else None,
        },
        "would_block": {
            str(t): sum(1 for d in dist_match if d > t) for t in THRESHOLDS
        } if dist_match else {},
        "worst": [{"distance_m": round(d, 1), "invoice": inv, "drop": drop}
                  for d, inv, drop in worst[:20]],
    }
    if args.out:
        Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=2),
                                  encoding="utf-8")
        print(f"\nบันทึกรายงานเป็น {args.out}")

    print()
    print("คำแนะนำ: เลือกเกณฑ์จากตัวเลขข้างบน — ถ้าที่เกณฑ์ 20 ม. แถวที่จะโดนบล็อกมากกว่า ~2% "
          "ของแถวที่เทียบได้ แปลว่าเกณฑ์นี้เข้มเกินหรือ GPS ที่จุดส่งไม่แม่นยำ")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
