#!/usr/bin/env python3
"""
Deterministic extractor for AppSheet "Application Documentation" PDF dumps.

Input : pdftotext default-mode text dump (DOM reading order) of the PDF.
Output: structured schema (JSON + CSV) for every table, column, view, slice,
        format rule and action in the app.

Design notes
------------
The PDF is Chrome-rendered HTML: every property is a 2-column table row
(label | value). Long values wrap, and because the label cell is vertically
centred, the label text is painted *in the middle* of its own value. The
plain-text dump therefore interleaves labels and value fragments.

We recover structure with three deterministic signals instead of guessing:
  1. The AppSheet field label vocabulary (one label per row of the PDF)
  2. Value shape: JSON (starts with '{'), formula (starts with '='), bare token
  3. Balance checks: JSON braces + formula parens/brackets must close

No LLM, no fuzzy guessing. Every extracted value is reproducible by re-running
this script; `scripts/validate_schema.py` proves coverage against the PDF's
own headline counts.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

# --------------------------------------------------------------------------
# Field vocabularies (taken from the AppSheet documentation layout itself)
# --------------------------------------------------------------------------

TABLE_FIELDS = [
    "Table name", "Visible?", "Shared?", "Data locale", "Schema",
    "Are updates allowed?", "Expression for update mode", "Security filter",
    "Source Path", "Worksheet Name/Qualifier", "Data Source",
    "Store for image and file capture", "Column Order List",
    "Partitioned across many files/sources?",
    "Partitioned across many worksheets?",
]

COLUMN_FIELDS = [
    "Column name", "Visible?", "Description", "Type", "Type Qualifier", "App formula",
    "Read-Only", "Hidden", "Label", "Formula version", "Reset on edit?",
    "Initial value", "System Defined?", "Key", "Part of Key?",
    "Fixed definition?", "Editable Initial Value?", "Virtual?", "LocaleName",
    "Searchable", "Scannable", "NFC Scannable", "Sensitive data",
]

SLICE_FIELDS = [
    "Slice Name", "Slice Columns", "Row filter condition", "Update mode",
    "Source Table", "Visible?", "Slice Actions",
]

VIEW_FIELDS = [
    "View name", "Created by", "View type", "ActionType", "Position",
    "View configuration", "Visible?", "Icon", "Menu order",
]

ACTION_FIELDS = [
    "Action name", "Bulk action?", "Modifies data?", "Needs confirmation?",
    "Prominence", "Action order", "With these properties", "Do this",
    "Attach to column", "Set this column", "To this value",
    "Only if this condition is true", "Disable automatic updates?",
    "Display name", "Action icon", "For a record of this table",
    "Does this action apply to the whole table?", "Visible?",
]

RULE_FIELDS = [
    "Rule name", "Format these columns and actions", "For this data",
    "If this condition is true", "Rule order",
    "Is this format rule disabled?", "Like this", "Visible?",
]

APP_FIELDS = [
    "Short Name", "Version", "Default app folder", "Function", "Runnable?",
    "Deployable?", "Personal use only?",
]

ALL_FIELDS = set(TABLE_FIELDS + COLUMN_FIELDS + SLICE_FIELDS + VIEW_FIELDS +
                 ACTION_FIELDS + RULE_FIELDS + APP_FIELDS)

# Labels the PDF renders across two physical lines.
TWO_LINE_LABELS = {
    ("Expression for update", "mode"): "Expression for update mode",
    ("Store for image and file", "capture"): "Store for image and file capture",
    ("Partitioned across many", "files/sources?"): "Partitioned across many files/sources?",
    ("Partitioned across many", "worksheets?"): "Partitioned across many worksheets?",
    ("Editable Initial", "Value?"): "Editable Initial Value?",
    ("Only if this condition is", "true"): "Only if this condition is true",
    ("Disable automatic", "updates?"): "Disable automatic updates?",
    ("Format these columns and", "actions"): "Format these columns and actions",
    ("Does this action apply to", "the whole table?"): "Does this action apply to the whole table?",
}

HEADING_KEYWORDS = ["Table name", "View name", "Action name", "Rule name",
                    "Slice Name", "Schema Name"]

# Characters that carry meaning (latin letters, digits, Thai). A block made
# only of icons / symbols (FontAwesome private-use area, emoji) is decoration
# painted next to a heading and must never be treated as a value.
MEANINGFUL = re.compile(r"[A-Za-z0-9\u0E00-\u0E7F]")


# A few long labels are painted on the same line as their value.
SAME_LINE_LABELS = ["Worksheet Name/Qualifier"]


def split_inline_label(line: str, label: str) -> tuple[str, list[str]]:
    """Split 'Label value NextLabel' painted on one physical line."""
    rest = line.strip()[len(label):].strip()
    best = None
    for lab in sorted(ALL_FIELDS, key=len, reverse=True):
        idx = rest.rfind(" " + lab)
        if idx > 0 and (best is None or idx > best[0]):
            best = (idx, lab)
    if best:
        idx, lab = best
        return rest[:idx].strip(), [lab]
    return rest, []


def split_leading_labels(block: list[str]) -> tuple[list[str], list[str]]:
    """Split 'Label' + value packed into a single block."""
    for lab in SAME_LINE_LABELS:
        if len(block) >= 2 and block[0].strip().startswith(lab + " "):
            value, extra = split_inline_label(block[0], lab)
            return [lab], ([value] if value else []) + extra + block[1:]
    if len(block) >= 2 and block[0].strip() in ALL_FIELDS:
        return [block[0].strip()], block[1:]
    return [], block


def split_trailing_labels(block: list[str]) -> tuple[list[str], list[str]]:
    """Split value + 'Label' packed into a single block.

    The PDF sometimes paints a label directly after the last line of the
    previous value, without a blank line in between.
    """
    n = len(block)
    if n >= 3 and (block[-2].strip(), block[-1].strip()) in TWO_LINE_LABELS:
        return block[:-2], [TWO_LINE_LABELS[(block[-2].strip(), block[-1].strip())]]
    if n >= 2 and block[-1].strip() in ALL_FIELDS:
        return block[:-1], [block[-1].strip()]
    return block, []


def segment_block(block: list[str]) -> list[tuple[str, object]]:
    """Split a physical block into label / suffix / value segments.

    The PDF packs several logical rows into one physical block, e.g.
        ['Worksheet Name/Qualifier <value>', 'Data Source',
         'Store for image and file', 'capture']
    returns [('L', label), ('V', [line]), ('L', label), ...]
    """
    segs: list[tuple[str, object]] = []
    i = 0
    n = len(block)
    while i < n:
        line = block[i].strip()
        matched = False
        for lab in SAME_LINE_LABELS:
            if line.startswith(lab + " "):
                value, extra = split_inline_label(line, lab)
                segs.append(("L", lab))
                if value:
                    segs.append(("V", [value]))
                for e in extra:
                    segs.append(("L", e))
                i += 1
                matched = True
                break
        if matched:
            continue
        if i + 1 < n and (line, block[i + 1].strip()) in TWO_LINE_LABELS:
            segs.append(("L", TWO_LINE_LABELS[(line, block[i + 1].strip())]))
            i += 2
            continue
        if line in ALL_FIELDS:
            segs.append(("L", line))
            i += 1
            continue
        if line in LABEL_PREFIXES:
            segs.append(("L", LABEL_PREFIXES[line]))
            i += 1
            continue
        if line in LABEL_SUFFIXES:
            segs.append(("S", line))
            i += 1
            continue
        segs.append(("V", [line]))
        i += 1
    return segs


def is_decoration(block: list[str]) -> bool:
    return bool(block) and all(not MEANINGFUL.search(line) for line in block)

# AppSheet column type tokens (used to split a packed bare value block that
# holds both a long description and the type name).
KNOWN_TYPE_TOKENS = {
    "Text", "LongText", "Number", "Decimal", "Price", "Percent", "Duration",
    "Date", "DateTime", "Time", "LatLong", "Geolocation", "Email", "Phone",
    "URL", "Url", "Image", "Signature", "Yes/No", "Single select",
    "Multiple select", "Enum", "EnumList", "Ref", "RefList", "List", "Slice",
    "SliceList", "ChangeCounter", "Name", "Show", "Number of this row",
    "ID of this row", "Attachment",
}

HEADING_PATTERNS = [
    ("table", re.compile(r"^Table name (?P<rest>.*)$")),
    ("schema", re.compile(r"^Schema Name (?P<rest>.*)$")),
    ("column", re.compile(r"^Column (?P<idx>\d+):(?P<rest>.*)$")),
    ("slice", re.compile(r"^Slice Name (?P<rest>.*)$")),
    ("view", re.compile(r"^View name (?P<rest>.*)$")),
    ("action", re.compile(r"^Action name (?P<rest>.*)$")),
    ("rule", re.compile(r"^Rule name (?P<rest>.*)$")),
]

FIELD_ORDER = {
    "app": APP_FIELDS, "table": TABLE_FIELDS, "column": COLUMN_FIELDS,
    "slice": SLICE_FIELDS, "view": VIEW_FIELDS, "action": ACTION_FIELDS,
    "rule": RULE_FIELDS,
}


# --------------------------------------------------------------------------
# Low level helpers
# --------------------------------------------------------------------------

def read_blocks(path: Path) -> list[list[str]]:
    """Split the raw text dump into blocks (maximal runs of non-empty lines)."""
    raw = path.read_text(encoding="utf-8").replace("\f", "\n")
    blocks: list[list[str]] = []
    cur: list[str] = []
    for line in raw.split("\n"):
        s = line.rstrip()
        if not s.strip():
            if cur:
                blocks.append(cur)
                cur = []
        else:
            cur.append(s)
    if cur:
        blocks.append(cur)
    return blocks


# A label may be painted on two lines with a value in between; the first half
# still has to be recognised as a label.
LABEL_PREFIXES = {
    "Expression for update": "Expression for update mode",
    "Store for image and file": "Store for image and file capture",
    "Partitioned across many": "Partitioned across many files/sources?",
    "Editable Initial": "Editable Initial Value?",
    "Only if this condition is": "Only if this condition is true",
    "Disable automatic": "Disable automatic updates?",
    "Format these columns and": "Format these columns and actions",
    "Does this action apply to": "Does this action apply to the whole table?",
}
LABEL_SUFFIXES = {
    "mode", "capture", "files/sources?", "worksheets?", "Value?", "true",
    "updates?", "actions", "the whole table?",
}


def label_block_labels(block: list[str]) -> list[str]:
    """Labels contained in a block (0, 1 or several).

    A block is normally one label. It can also be a two-line label such as
    'Format these columns and' + 'actions', or two independent labels that the
    PDF painted on consecutive lines ('View name' + 'Created by').
    """
    if not block:
        return []
    if len(block) == 1:
        t = block[0].strip()
        if t in ALL_FIELDS:
            return [t]
        if t in LABEL_PREFIXES:
            return [LABEL_PREFIXES[t]]
        return []
    if len(block) == 2:
        merged = TWO_LINE_LABELS.get((block[0].strip(), block[1].strip()))
        if merged:
            return [merged]
    if all(x.strip() in ALL_FIELDS for x in block):
        return [x.strip() for x in block]
    return []


def is_label_block(block: list[str]) -> str | None:
    labs = label_block_labels(block)
    return labs[0] if labs else None


def match_heading(block: list[str]) -> tuple[str, dict, list[str]] | None:
    """Return (kind, fields, trailing_labels) if the block is a record heading.

    The PDF paints the heading line and the field label on consecutive lines,
    so the heading block usually ends with the bare label again (sometimes
    split over two physical lines). Those labels belong to the record and
    must be replayed, otherwise labels and values end up off by one.

    A section banner ("Format Rules", "Views", ...) can be merged into the same
    block, so every line of the block is scanned, not just the first.
    """
    for start in range(len(block)):
        found = _match_heading_line(block, start)
        if found is not None:
            kind, fields, trailing = found
            return kind, fields, trailing
    return None


def _match_heading_line(block: list[str], start: int) -> tuple[str, dict, list[str]] | None:
    first = block[start].strip()
    for kind, rx in HEADING_PATTERNS:
        m = rx.match(first)
        if not m:
            continue
        rest = m.group("rest").strip()
        tail_lines = [x.strip() for x in block[start + 1:]]
        trailing: list[str] = []
        while tail_lines:
            if tail_lines[-1] in ALL_FIELDS or tail_lines[-1] in HEADING_KEYWORDS:
                trailing.insert(0, tail_lines.pop())
            elif len(tail_lines) >= 2 and (tail_lines[-2], tail_lines[-1]) in TWO_LINE_LABELS:
                last = tail_lines.pop()
                prev = tail_lines.pop()
                trailing.insert(0, TWO_LINE_LABELS[(prev, last)])
            else:
                break
        tail = " ".join(tail_lines).strip()
        name = (rest + (" " + tail if tail else "")).strip()
        if kind == "column":
            return "column", {"index": int(m.group("idx")), "name": name}, trailing
        return kind, {"name": name}, trailing
    return None


def _scan_balance(text: str, openers: str, closers: str):
    depth = 0
    in_str = False
    esc = False
    for ch in text:
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch in openers:
            depth += 1
        elif ch in closers:
            depth -= 1
    return depth, in_str


def json_balanced(text: str) -> bool:
    depth, in_str = _scan_balance(text, "{", "}")
    return depth == 0 and not in_str


def formula_balanced(text: str) -> bool:
    depth, in_str = _scan_balance(text, "([", ")]")
    return depth == 0 and not in_str


def shape_of(frag: str) -> str:
    s = frag.strip()
    if s.startswith("{"):
        return "json"
    if s.startswith("="):
        return "formula"
    return "bare"


# A fragment that continues a previous expression starts with a comparison
# operator or a boolean keyword. A fragment starting with '=' is always a NEW
# formula, never a continuation.
CONTINUATION_TOKENS = re.compile(
    r"^(<=|>=|<>|[<>]|\bAND\b|\bOR\b|\bNOT\b|\bIF\b|\bSWITCH\b|\bELSE\b|\bTHEN\b)"
)

TRAILING_OPERATORS = (",", "(", "[", "+", "-", "*", "/", "&", "|", "<", ">",
                       "<=", ">=", "<>", "=")


def value_complete(frags: list[str], next_line: str | None) -> bool:
    if not frags:
        return True
    shape = shape_of(frags[0])
    if shape == "json":
        return json_balanced("".join(frags))
    if shape == "formula":
        text = " ".join(frags)
        if not formula_balanced(text):
            return False
        if text.rstrip().endswith(TRAILING_OPERATORS):
            return False
        if next_line is not None and CONTINUATION_TOKENS.match(next_line.strip()):
            return False
        return True
    if next_line is None:
        return True
    nxt = next_line.strip()
    return not (nxt.startswith("{") or nxt.startswith("="))


def join_value(frags: list[str], shape: str) -> str:
    if shape == "json":
        return "".join(f.strip() for f in frags)
    return " ".join(f.strip() for f in frags)


# --------------------------------------------------------------------------
# Record parsing
# --------------------------------------------------------------------------

class Record:
    """One table / column / view / action / slice / rule from the PDF.

    The PDF paints label cells and value cells independently (labels are
    vertically centred, values are top-aligned), so the text dump emits labels
    and values out of order. We therefore collect the two streams separately
    and zip them 1:1 - the field order inside a record is fixed by AppSheet.
    """

    def __init__(self, kind: str, heading: dict, owner: str | None = None):
        self.kind = kind
        self.heading = heading
        self.owner = owner
        self.fields: "OrderedDict[str, object]" = OrderedDict()
        self._pending_labels: list[str] = []
        self._orphan: str | None = None
        self._pending: list[str] = []
        self._shape: str | None = None
        self._seen_first_value = False

    # -- labels -------------------------------------------------------------
    def merge_suffix(self, suffix: str) -> bool:
        """Complete a two-line label whose second half was painted separately."""
        for i in range(len(self._pending_labels) - 1, -1, -1):
            lab = self._pending_labels[i]
            if (lab, suffix) in TWO_LINE_LABELS:
                self._pending_labels[i] = TWO_LINE_LABELS[(lab, suffix)]
                return True
        return False

    def add_label(self, label: str) -> None:
        """Register a field label.

        Labels are painted independently of their values, so a label can show
        up *before* its value, *after* a previous value, or even in the middle
        of a wrapped value. Values are therefore matched by label NAME, not by
        position.

        A label also terminates the value that precedes it - unless that value
        is a JSON/formula that is still unbalanced, in which case the label
        was painted *inside* the value cell and the value continues after it.
        """
        if self._pending:
            if self._shape in ("json", "formula") and not self._balanced():
                pass                      # injected label - value continues
            else:
                self._emit()
        if self._orphan is not None:
            self._assign(label, self._orphan)
            self._orphan = None
            return
        if label in self.fields:
            return
        self._pending_labels.append(label)

    def _balanced(self) -> bool:
        text = join_value(self._pending, self._shape or "bare")
        if self._shape == "json":
            return json_balanced(text)
        if self._shape == "formula":
            return formula_balanced(text)
        return True

    def flush(self) -> None:
        """Finish a record: emit whatever value is still open."""
        if self._pending:
            self._emit()

    # -- values -------------------------------------------------------------
    def _assign(self, label: str, value: str) -> None:
        if label in self.fields:
            cur = self.fields[label]
            if isinstance(cur, list):
                cur.append(value)
            else:
                self.fields[label] = [cur, value]
        else:
            self.fields[label] = value

    def _emit(self, as_single: bool = False) -> None:
        if not self._pending:
            return
        shape = self._shape or shape_of(self._pending[0])
        frags = list(self._pending)
        self._pending = []
        self._shape = None
        self._seen_first_value = True
        if shape == "bare" and not as_single and len(frags) <= len(self._pending_labels):
            # several short values packed into one block: 1:1 with the labels
            for frag in frags:
                self._emit_one(join_value([frag], "bare"))
            return
        self._emit_one(join_value(frags, shape))

    def _emit_one(self, value: str) -> None:
        if self._pending_labels:
            self._assign(self._pending_labels.pop(0), value)
        else:
            # the owning label has not been painted yet (wrapped value) ->
            # the next label that appears claims it
            self._orphan = value

    def add_fragments(self, frags: list[str], next_line: str | None) -> None:
        for idx, frag in enumerate(frags):
            if not self._pending:
                self._shape = shape_of(frag)
                self._pending = [frag]
            elif self._shape == "bare" and shape_of(frag) in ("json", "formula"):
                # a complete bare token followed by a brand-new value shape
                self._emit()
                self._shape = shape_of(frag)
                self._pending = [frag]
            elif (self._shape == "bare" and len(self._pending) >= 1
                  and len(self._pending) >= 1 and len(frags) > 1
                  and re.fullmatch(r"[A-Z][A-Z0-9_]*", self._pending[0].strip())):
                # a short enum value followed by the next field's value
                self._emit()
                self._shape = "bare"
                self._pending = [frag]
            elif (self._shape == "bare" and len(self._pending) >= 1
                  and frag.strip() in KNOWN_TYPE_TOKENS
                  and "Type" in self._pending_labels
                  and self._pending_labels.index("Type") >= 1):
                # a packed block: long description + type token
                self._emit(as_single=True)
                self._shape = "bare"
                self._pending = [frag]
            else:
                self._pending.append(frag)
            # a json/formula value ends as soon as it is balanced - unless the
            # next fragment continues the expression
            if self._shape in ("json", "formula"):
                text = join_value(self._pending, self._shape)
                nxt = frags[idx + 1] if idx + 1 < len(frags) else next_line
                if self._shape == "json":
                    done = json_balanced(text)
                else:
                    # a formula that ends with an operator ("... * 1000" split
                    # across a line break) is not finished yet
                    done = (formula_balanced(text)
                            and not text.rstrip().endswith(TRAILING_OPERATORS))
                    if done and nxt is not None \
                            and CONTINUATION_TOKENS.match(nxt.strip()):
                        done = False
                if done:
                    self._emit()

    def split_leading_name(self, heading_name: str, frags: list[str]) -> list[str]:
        """Split a value block whose first line is the record's own name.

        A few records paint the heading, then two labels, then the values:
            'Rule name <x>' | 'Rule name' | 'Format these columns and actions'
            <x> | Invoice No | ScanStatus | ...
        The first value is always the record's own name, so cut there.
        """
        if self._seen_first_value or self._pending or not frags:
            return frags
        if frags[0].strip() != heading_name:
            return frags
        self._seen_first_value = True
        if self._pending_labels:
            self._assign(self._pending_labels.pop(0), heading_name)
        else:
            self._orphan = heading_name
        return frags[1:]


def parse_document(blocks: list[list[str]]) -> dict:
    records: list[Record] = []
    cur: Record | None = None
    cur_table: str | None = None
    skip_next_value = False
    canonical: dict[str, str] = {}
    prev_was_heading = False
    i = 0
    n = len(blocks)
    while i < n:
        block = blocks[i]
        labels = label_block_labels(block)
        heading = match_heading(block)

        # A heading whose name was painted on its own line (emoji views) shows
        # up as a bare keyword block that is *not* preceded by another heading.
        if heading is None and len(block) == 1 and block[0].strip() in HEADING_KEYWORDS \
                and i + 2 < n:
            nxt = blocks[i + 1]
            nxt2 = blocks[i + 2]
            # a split heading repeats its name (either as the next block or
            # right after the repeated field label)
            repeats = (len(nxt) == 1 and len(nxt2) == 1 and nxt[0].strip() == nxt2[0].strip()) or \
                      (len(nxt) == 1 and len(nxt2) >= 1
                       and block[0].strip() in label_block_labels(nxt2))
            if repeats and len(nxt) == 1 and not label_block_labels(nxt):
                kind = {"Table name": "table", "View name": "view",
                        "Action name": "action", "Rule name": "rule",
                        "Slice Name": "slice"}.get(block[0].strip())
                if kind is None:
                    kind = "schema"
                if kind == "schema":
                    nm = nxt[0].strip()
                    cur_table = nm[:-len("_Schema")] if nm.endswith("_Schema") else nm
                    cur = None
                    skip_next_value = True
                    prev_was_heading = True
                    i += 2
                    continue
                if cur is not None:
                    cur.flush()
                cur = Record(kind, {"name": nxt[0].strip()}, owner=cur_table)
                records.append(cur)
                prev_was_heading = True
                i += 2
                continue

        if heading is not None:
            kind, fields, trailing = heading
            if kind == "table":
                nm = fields.get("name", "")
                canonical[re.sub(r"\s+", "", nm)] = nm
            # Edge case: the PDF paints the values of the *previous* record
            # after this record's heading (labels are vertically centred).
            if (cur is not None and cur._pending_labels and i + 2 < n):
                nxt, nxt2 = blocks[i + 1], blocks[i + 2]
                labs2 = label_block_labels(nxt2)
                if (not label_block_labels(nxt)
                        and match_heading(nxt) is None
                        and labs2 and labs2[0].endswith("name")):
                    cur.add_fragments(nxt, None)
                    i += 1
            if kind == "schema":
                name = fields.get("name", "")
                base = name[:-len("_Schema")] if name.endswith("_Schema") else name
                cur_table = canonical.get(re.sub(r"\s+", "", base), base)
                cur = None
                skip_next_value = True   # the schema's own "Visible?" row
                i += 1
                continue
            if cur is not None:
                cur.flush()
            cur = Record(kind, fields, owner=cur_table)
            for lab in trailing:
                cur.add_label(lab)
            records.append(cur)
            prev_was_heading = True
            i += 1
            continue

        if labels:
            if cur is not None:
                for lab in labels:
                    cur.add_label(lab)
            skip_next_value = False
            i += 1
            continue
        elif (len(block) == 1 and block[0].strip() in LABEL_SUFFIXES
              and cur is not None and cur.merge_suffix(block[0].strip())):
            # the second half of a two-line label -> merge it into the label
            skip_next_value = False
            i += 1
            continue
        elif (len(block) == 1 and block[0].strip() in LABEL_SUFFIXES
              and cur is not None):
            # looks like a label suffix but no label is waiting for it.
            # Only boolean literals can be real values ('true' as a condition);
            # the other suffixes are leftovers of an already merged label.
            if block[0].strip().lower() not in ("true", "false"):
                prev_was_heading = False
                i += 1
                continue

        # value block
        if (is_decoration(block) and cur is not None
                and not cur._pending_labels and not cur._pending):
            # a decorative glyph painted next to a heading (icon of the view)
            # - but never a real value such as the "Action icon" field
            prev_was_heading = False
            i += 1
            continue
        if is_decoration(block) and cur is None:
            prev_was_heading = False
            i += 1
            continue
        if skip_next_value:
            skip_next_value = False
            i += 1
            continue
        if cur is None:
            i += 1
            continue

        # The heading of a record repeats its own name as the first value.
        segs = segment_block(block)
        # merge consecutive value segments back into one run
        merged: list[tuple[str, object]] = []
        for kind, payload in segs:
            if kind == "V" and merged and merged[-1][0] == "V":
                merged[-1][1].extend(payload)          # type: ignore[union-attr]
            else:
                merged.append((kind, payload))
        for kind, payload in merged:
            if kind == "L":
                cur.add_label(str(payload))
            elif kind == "S":
                if not cur.merge_suffix(str(payload)):
                    # not a label suffix after all -> it may be a plain value
                    # (only boolean literals qualify)
                    if str(payload).strip().lower() in ("true", "false"):
                        cur.add_fragments([str(payload)], None)
            else:
                frags = list(payload)                 # type: ignore[arg-type]
                if cur._pending_labels and cur._pending_labels[0].endswith("name"):
                    frags = cur.split_leading_name(cur.heading.get("name", ""), frags)
                    if not frags:
                        continue
                cur.add_fragments(frags, None)
        prev_was_heading = False
        i += 1

    return {"records": records, "current_table": cur_table}


# --------------------------------------------------------------------------
# Post-processing
# --------------------------------------------------------------------------

def try_json(value: str):
    v = value.strip()
    if not v.startswith("{"):
        return None
    try:
        return json.loads(v)
    except Exception:
        return None


def _scalar(v):
    if isinstance(v, list):
        return "\n".join(str(x) for x in v)
    return v if v is not None else ""


def build_output(parsed: dict) -> dict:
    tables, columns, views, actions, slices, rules = [], [], [], [], [], []
    recs = parsed["records"]

    for r in [x for x in recs if x.kind == "table"]:
        f = dict(r.fields)
        # Repair: a wrapped 'Source Path' value can have its second half
        # painted before the 'Source Path' label, which leaves the remainder in
        # the 'Data Source' slot. A data source is never a path, so the
        # remainder belongs to the source path.
        ds = str(f.get("Data Source", ""))
        if ds and "/" in ds and ds not in ("google_tables",):
            f["Source Path"] = str(f.get("Source Path", "")) + ds
            f["Data Source"] = "native"
        tables.append({
            "name": r.heading.get("name") or _scalar(f.get("Table name", "")),
            "visible": _scalar(f.get("Visible?", "")),
            "shared": _scalar(f.get("Shared?", "")),
            "data_locale": _scalar(f.get("Data locale", "")),
            "schema": _scalar(f.get("Schema", "")),
            "updates_allowed": _scalar(f.get("Are updates allowed?", "")),
            "update_mode_expression": _scalar(f.get("Expression for update mode", "")),
            "security_filter": _scalar(f.get("Security filter", "")),
            "source_path": _scalar(f.get("Source Path", "")),
            "worksheet_name": _scalar(f.get("Worksheet Name/Qualifier", "")),
            "data_source": _scalar(f.get("Data Source", "")),
            "file_capture": _scalar(f.get("Store for image and file capture", "")),
            "column_order_list": _scalar(f.get("Column Order List", "")),
            "partitioned_files": _scalar(f.get("Partitioned across many files/sources?", "")),
            "partitioned_worksheets": _scalar(f.get("Partitioned across many worksheets?", "")),
        })

    # attach columns to their owning table (the schema heading owns them)
    table_names = [t["name"] for t in tables]
    name_set = set(table_names)
    by_nospace = {re.sub(r"\s+", "", n): n for n in table_names}

    for r in [x for x in recs if x.kind == "column"]:
        f = r.fields
        tq_raw = _scalar(f.get("Type Qualifier", ""))
        tq = try_json(tq_raw)
        if tq:
            for key in ("ReferencedTableName", "ReferencedRootTableName"):
                val = tq.get(key)
                if isinstance(val, str) and val and val not in name_set:
                    fixed = by_nospace.get(re.sub(r"\s+", "", val))
                    if fixed:
                        tq[key] = fixed
        columns.append({
            "table": r.owner or "",
            "index": r.heading.get("index"),
            "name": r.heading.get("name") or _scalar(f.get("Column name", "")),
            "visible": _scalar(f.get("Visible?", "")),
            "type": _scalar(f.get("Type", "")),
            "type_qualifier_raw": "" if tq is not None else tq_raw,
            "type_qualifier": tq if tq is not None else {},
            "app_formula": _scalar(f.get("App formula", "")),
            "read_only": _scalar(f.get("Read-Only", "")),
            "hidden": _scalar(f.get("Hidden", "")),
            "label": _scalar(f.get("Label", "")),
            "formula_version": _scalar(f.get("Formula version", "")),
            "reset_on_edit": _scalar(f.get("Reset on edit?", "")),
            "initial_value": _scalar(f.get("Initial value", "")),
            "system_defined": _scalar(f.get("System Defined?", "")),
            "key": _scalar(f.get("Key", "")),
            "part_of_key": _scalar(f.get("Part of Key?", "")),
            "fixed_definition": _scalar(f.get("Fixed definition?", "")),
            "editable_initial_value": _scalar(f.get("Editable Initial Value?", "")),
            "virtual": _scalar(f.get("Virtual?", "")),
            "locale_name": _scalar(f.get("LocaleName", "")),
            "searchable": _scalar(f.get("Searchable", "")),
            "scannable": _scalar(f.get("Scannable", "")),
            "nfc_scannable": _scalar(f.get("NFC Scannable", "")),
            "sensitive_data": _scalar(f.get("Sensitive data", "")),
        })

    for r in [x for x in recs if x.kind == "view"]:
        f = r.fields
        views.append({
            "name": r.heading.get("name") or _scalar(f.get("View name", "")),
            "created_by": _scalar(f.get("Created by", "")),
            "view_type": _scalar(f.get("View type", "")),
            "action_type": _scalar(f.get("ActionType", "")),
            "position": _scalar(f.get("Position", "")),
            "visible": _scalar(f.get("Visible?", "")),
            "icon": _scalar(f.get("Icon", "")),
            "menu_order": _scalar(f.get("Menu order", "")),
            "configuration_raw": _scalar(f.get("View configuration", "")),
            "configuration": try_json(_scalar(f.get("View configuration", ""))) or {},
        })

    for r in [x for x in recs if x.kind == "action"]:
        f = r.fields
        props = try_json(_scalar(f.get("With these properties", "")))
        actions.append({
            "name": r.heading.get("name") or _scalar(f.get("Action name", "")),
            "bulk_action": _scalar(f.get("Bulk action?", "")),
            "modifies_data": _scalar(f.get("Modifies data?", "")),
            "needs_confirmation": _scalar(f.get("Needs confirmation?", "")),
            "prominence": _scalar(f.get("Prominence", "")),
            "action_order": _scalar(f.get("Action order", "")),
            "do_this": _scalar(f.get("Do this", "")),
            "attach_to_column": _scalar(f.get("Attach to column", "")),
            "set_this_column": _scalar(f.get("Set this column", "")),
            "to_this_value": _scalar(f.get("To this value", "")),
            "condition": _scalar(f.get("Only if this condition is true", "")),
            "disable_automatic_updates": _scalar(f.get("Disable automatic updates?", "")),
            "action_icon": _scalar(f.get("Action icon", "")),
            "for_record_of_table": _scalar(f.get("For a record of this table", "")),
            "applies_to_whole_table": _scalar(f.get("Does this action apply to the whole table?", "")),
            "visible": _scalar(f.get("Visible?", "")),
            "properties_raw": _scalar(f.get("With these properties", "")),
            "properties": props if props is not None else {},
        })

    for r in [x for x in recs if x.kind == "slice"]:
        f = r.fields
        slices.append({
            "name": r.heading.get("name") or _scalar(f.get("Slice Name", "")),
            "source_table": _scalar(f.get("Source Table", "")),
            "row_filter_condition": _scalar(f.get("Row filter condition", "")),
            "update_mode": _scalar(f.get("Update mode", "")),
            "visible": _scalar(f.get("Visible?", "")),
            "columns_raw": _scalar(f.get("Slice Columns", "")),
            "actions_raw": _scalar(f.get("Slice Actions", "")),
        })

    for r in [x for x in recs if x.kind == "rule"]:
        f = r.fields
        rules.append({
            "name": r.heading.get("name") or _scalar(f.get("Rule name", "")),
            "for_data": _scalar(f.get("For this data", "")),
            "condition": _scalar(f.get("If this condition is true", "")),
            "rule_order": _scalar(f.get("Rule order", "")),
            "disabled": _scalar(f.get("Is this format rule disabled?", "")),
            "like_this_raw": _scalar(f.get("Like this", "")),
            "like_this": try_json(_scalar(f.get("Like this", ""))) or {},
            "columns_and_actions_raw": _scalar(f.get("Format these columns and actions", "")),
            "visible": _scalar(f.get("Visible?", "")),
        })

    return {"tables": tables, "columns": columns, "views": views,
            "actions": actions, "slices": slices, "format_rules": rules}


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: extract_appsheet.py <raw-text-dump> <out-dir>")
        return 2
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)

    blocks = read_blocks(src)
    parsed = parse_document(blocks)
    data = build_output(parsed)

    (out / "schema_raw.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def write_csv(name: str, rows: list[dict]) -> None:
        if not rows:
            return
        with (out / name).open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)

    for name, rows in [("tables.csv", data["tables"]), ("columns.csv", data["columns"]),
                       ("views.csv", data["views"]), ("actions.csv", data["actions"]),
                       ("slices.csv", data["slices"]),
                       ("format_rules.csv", data["format_rules"])]:
        write_csv(name, rows)

    print(json.dumps({k: len(v) for k, v in data.items()}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
