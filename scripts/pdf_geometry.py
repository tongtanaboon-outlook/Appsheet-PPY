#!/usr/bin/env python3
"""Extract geometry-aware lines from a pdftotext -bbox-layout XML dump.

Produces a JSONL cache: one record per rendered line with xMin/xMax/yMin/yMax/text.
Rationale: AppSheet's "Application Documentation" PDF is an HTML 2-column table
(label | value). Long values wrap across lines and the wrap point is ambiguous in
plain text extraction; x-coordinates let us rebuild the cell and reason about it.
"""
import json, re, sys, html
import xml.etree.ElementTree as ET

NS = "{http://www.w3.org/1999/xhtml}"


def bbox_to_jsonl(bbox_xml: str, out_jsonl: str) -> int:
    n = 0
    with open(bbox_xml, "r", encoding="utf-8") as fh, open(out_jsonl, "w", encoding="utf-8") as out:
        page_no = 0
        for event, elem in ET.iterparse(fh, events=("end",)):
            if elem.tag == NS + "page":
                page_no += 1
                lines = []
                for line in elem.iter(NS + "line"):
                    words = [(w.get("xMin"), w.get("xMax"), w.text or "") for w in line.iter(NS + "word")]
                    if not words:
                        continue
                    text = " ".join(html.unescape(w[2]) for w in words)
                    lines.append({
                        "xMin": round(float(line.get("xMin")), 2),
                        "xMax": round(float(line.get("xMax")), 2),
                        "yMin": round(float(line.get("yMin")), 2),
                        "yMax": round(float(line.get("yMax")), 2),
                        "t": text,
                    })
                lines.sort(key=lambda r: (r["yMin"], r["xMin"]))
                out.write(json.dumps({"page": page_no, "lines": lines}, ensure_ascii=False) + "\n")
                n += 1
                elem.clear()
    return n


if __name__ == "__main__":
    pages = bbox_to_jsonl(sys.argv[1], sys.argv[2])
    print(f"pages written: {pages}")
