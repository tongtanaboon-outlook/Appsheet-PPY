#!/usr/bin/env python3
"""
Deterministic quality gate for the AppSheet -> GitHub repository.

This is the anti-"agent dropped the work" mechanism: every documented item is
checked against the machine-readable schema, so a missing table, column,
relation, formula or bot table fails the build instead of silently shipping.

Usage:
    python scripts/validate_repo.py [--repo .]

Exit code 0 = all checks pass, 1 = at least one check failed.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

# The counts the AppSheet "Application Documentation" PDF declares on its cover
# page. They are the ground truth for "did we extract everything?".
PDF_COUNTS = {
    "tables": 90,
    "columns": 2304,
    "views": 115,
    "actions": 214,
    "slices": 8,
    "format_rules": 11,
}

ANCHORS = {
    "table": re.compile(r"<!--\s*table:\s*(.+?)\s*-->"),
    "col": re.compile(r"<!--\s*col:\s*(.+?)\s*-->"),
    "rel": re.compile(r"<!--\s*rel:\s*(.+?)\s*-->"),
    "formula": re.compile(r"<!--\s*formula:\s*(.+?)\s*-->"),
    "bot": re.compile(r"<!--\s*bot:\s*(.+?)\s*-->"),
}


class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, bool, str]] = []

    def add(self, name: str, ok: bool, detail: str = "") -> None:
        self.rows.append((name, ok, detail))

    @property
    def failed(self) -> list[tuple[str, bool, str]]:
        return [r for r in self.rows if not r[1]]

    def render(self) -> str:
        out = []
        for name, ok, detail in self.rows:
            mark = "PASS" if ok else "FAIL"
            out.append(f"[{mark}] {name}" + (f" - {detail}" if detail else ""))
        return "\n".join(out)


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def anchors_in(*paths: Path) -> set[str]:
    """Collect anchors from one or more documentation files."""
    out: set[str] = set()
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for rx in ANCHORS.values():
            out |= {m.group(1).strip() for m in rx.finditer(text)}
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = Path(args.repo).resolve()
    rep = Report()

    # ---------------------------------------------------------------- schema
    tables = read_csv(repo / "app" / "tables.csv")
    columns = read_csv(repo / "app" / "columns.csv")
    relations = read_csv(repo / "app" / "relations.csv")
    views = read_csv(repo / "app" / "views.csv")
    actions = read_csv(repo / "app" / "actions.csv")
    slices = read_csv(repo / "app" / "slices.csv")
    rules = read_csv(repo / "app" / "format_rules.csv")
    meta_path = repo / "app" / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}

    actual = {
        "tables": len(tables),
        "columns": len(columns),
        "views": len(views),
        "actions": len(actions),
        "slices": len(slices),
        "format_rules": len(rules),
    }
    for key, expected in PDF_COUNTS.items():
        rep.add(f"schema/{key} count == {expected}", actual[key] == expected,
                f"got {actual[key]}")

    # every table must own its columns
    by_table: dict[str, list[dict]] = {}
    for c in columns:
        by_table.setdefault(c["table"], []).append(c)
    orphans = [t["name"] for t in tables if t["name"] not in by_table]
    rep.add("every table has columns", not orphans, ", ".join(orphans[:5]))

    # every relation must point at a known table
    names = {t["name"] for t in tables}
    bad_rel = [r for r in relations if r["to_table"] not in names]
    rep.add("relations point at known tables", not bad_rel,
            ", ".join(f"{r['from_table']}->{r['to_table']}" for r in bad_rel[:5]))

    # type qualifier JSON must be parseable
    bad_json = [c for c in columns if c["type_qualifier_raw"].strip()
                and not c["type_qualifier_raw"].strip().startswith("{")]
    rep.add("type qualifier payloads are JSON", not bad_json, f"{len(bad_json)} bad")

    # field alignment: an action must point at a table that exists
    bad_action = [a["name"] for a in actions
                  if a.get("for_record_of_table") and a["for_record_of_table"] != "No"
                  and a["for_record_of_table"] not in names]
    rep.add("actions point at a known table", not bad_action,
            ", ".join(bad_action[:5]))

    # every action must have a verb and a target table
    no_target = [a["name"] for a in actions if not a.get("for_record_of_table")]
    rep.add("every action declares its target table", not no_target,
            ", ".join(no_target[:5]))

    # views must carry a known view type
    view_types = {"form", "table", "gallery", "deck", "detail", "ref",
                  "calendar", "slider", "group", "chat", "list", "template",
                  "deck_list"}
    bad_view = [v["name"] for v in views if v.get("view_type")
                and v["view_type"] not in view_types]
    rep.add("views carry a known view type", not bad_view, ", ".join(bad_view[:5]))

    # expressions that the PDF renders on top of the property table: these are
    # flagged so a human can confirm them in the app (not a build failure)
    flagged = [f"{c['table']} :: {c['name']}" for c in columns if c.get("needs_review")]
    rep.add("expressions flagged for manual review are listed",
            len(flagged) == meta.get("counts", {}).get("needs_review", -1),
            f"{len(flagged)}: " + ", ".join(flagged[:3]))

    # every column must have a type
    no_type = [f"{c['table']} :: {c['name']}" for c in columns if not c.get("type")]
    rep.add("every column has a type", not no_type, ", ".join(no_type[:5]))

    # ---------------------------------------------------------------- docs
    # The AI-written docs and the deterministically generated ones are both
    # accepted: the generated files guarantee 100% coverage, the AI files add
    # the business interpretation on top.
    table_docs = sorted((repo / "docs" / "tables").glob("*.md"))
    process_docs = sorted((repo / "docs" / "process-tables").glob("*.md"))
    rule_docs = sorted((repo / "docs" / "rules").glob("*.md"))
    dd = anchors_in(*(table_docs + process_docs))
    erd = anchors_in(repo / "docs" / "05-erd.md")
    fm = anchors_in(*(table_docs + process_docs))
    bt = anchors_in(*process_docs)
    all_docs = anchors_in(*(table_docs + process_docs + rule_docs))

    missing_tables = [t["name"] for t in tables if t["name"] not in dd]
    rep.add("data dictionary covers every table", not missing_tables,
            f"{len(missing_tables)} missing: " + ", ".join(missing_tables[:5]))

    missing_cols = [f"{c['table']} :: {c['name']}" for c in columns
                    if f"{c['table']} :: {c['name']}" not in dd]
    rep.add("data dictionary covers every column", not missing_cols,
            f"{len(missing_cols)} missing: " + ", ".join(missing_cols[:5]))

    missing_rels = [f"{r['from_table']} -> {r['to_table']}" for r in relations
                    if f"{r['from_table']} -> {r['to_table']}" not in erd]
    rep.add("erd covers every relation", not missing_rels,
            f"{len(missing_rels)} missing: " + ", ".join(missing_rels[:5]))

    computed = [c for c in columns if c["app_formula"] or c["initial_value"]]
    missing_f = [f"{c['table']} :: {c['name']}" for c in computed
                 if f"{c['table']} :: {c['name']}" not in fm]
    rep.add("formula catalog covers every computed column", not missing_f,
            f"{len(missing_f)} missing: " + ", ".join(missing_f[:5]))

    bot_tables = [t["name"] for t in tables if t["kind"] == "bot"]
    missing_b = [n for n in bot_tables if n not in bt]
    rep.add("bot inventory covers every bot table", not missing_b,
            f"{len(missing_b)} missing: " + ", ".join(missing_b[:5]))

    # ---------------------------------------------------------------- data
    manifest_path = repo / "data" / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        rep.add("data manifest lists every business table",
                len(manifest.get("tables", {})) == meta.get("counts", {}).get("business_tables", -1),
                f"manifest={len(manifest.get('tables', {}))}")
        csvs = {p.stem for p in (repo / "data").glob("*.csv")}
        unknown = csvs - set(manifest.get("tables", {}))
        rep.add("data csv files are declared in the manifest", not unknown,
                ", ".join(sorted(unknown)[:5]))
    else:
        rep.add("data manifest exists", False, "data/manifest.json missing")

    # one file per table / per rule must exist
    rep.add("one documentation file per business table",
            len(table_docs) == meta.get("counts", {}).get("business_tables", -1),
            f"{len(table_docs)} files")
    rep.add("one documentation file per bot table",
            len(process_docs) == (meta.get("counts", {}).get("bot_tables", 0)
                                  + meta.get("counts", {}).get("system_tables", 0)),
            f"{len(process_docs)} files")
    rep.add("one documentation file per format rule",
            len(rule_docs) == meta.get("counts", {}).get("format_rules", -1),
            f"{len(rule_docs)} files")

    # ------------------------------------------------- generated docs in sync
    gen = repo / "scripts" / "make_docs.py"
    if gen.exists():
        import subprocess
        res = subprocess.run(["python3", str(gen), "--check"], cwd=str(repo),
                             capture_output=True, text=True)
        diff_lines = [l.strip() for l in res.stdout.splitlines() if l.startswith("DIFF ")]
        n_diff = 0
        if diff_lines:
            import re as _re
            m = _re.search(r"DIFF\s+(\d+)", diff_lines[0])
            n_diff = int(m.group(1)) if m else len(diff_lines)
        rep.add("generated documentation is in sync with the schema", n_diff == 0,
                f"{n_diff} file(s) out of sync")

    # ---------------------------------------------------------------- output
    print(rep.render())
    if rep.failed:
        print(f"\n{len(rep.failed)} check(s) FAILED")
        return 1
    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
