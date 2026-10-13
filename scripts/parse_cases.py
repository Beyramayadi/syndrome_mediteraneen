"""
Parse pasted Medscape "Case Challenge" listing text into structured records.
 
Handles case entries with a title, summary, and French date line.
 
Usage:
    python3 parse_cases.py
"""
 
import re
import json
from pathlib import Path
 
# French month names -> numbers, for optional date normalization
FR_MONTHS = {
    "janvier": 1, "février": 2, "fevrier": 2, "mars": 3, "avril": 4,
    "mai": 5, "juin": 6, "juillet": 7, "août": 8, "aout": 8,
    "septembre": 9, "octobre": 10, "novembre": 11, "décembre": 12, "decembre": 12,
}
 
# Matches a French date like "août 27, 2026" or "février 07, 2023",
# optionally preceded by "Case Challenge, "
DATE_RE = re.compile(
    r'(?:Case Challenge,\s*)?'
    r'([A-Za-zéû]+)\s+(\d{1,2}),\s*(\d{4})',
    re.IGNORECASE
)
 
def normalize_date(month_fr, day, year):
    month_num = FR_MONTHS.get(month_fr.lower())
    if month_num is None:
        return None
    return f"{int(year):04d}-{month_num:02d}-{int(day):02d}"
 
def split_into_blocks(raw_text):
    """
    Split raw pasted text into per-case blocks.
    A new block starts at a line beginning with '*', '[', or a capitalized
    title-like line, IF the previous block already has a date line (i.e. is complete).
    Simpler and more robust: split on the date line, since every entry ends with one.
    """
    lines = [l.strip() for l in raw_text.strip().splitlines() if l.strip()]
    blocks = []
    current = []
    for line in lines:
        current.append(line)
        if DATE_RE.search(line) and len(line) < 60:
            # treat short lines containing a date as the end of a block
            blocks.append(current)
            current = []
    if current:
        blocks.append(current)  # trailing incomplete block, if any
    return blocks
 
def parse_block(block_lines):
    record = {"title": None, "summary": None, "date_raw": None, "date_iso": None}
 
    first_line = block_lines[0]
    record["title"] = first_line.strip()
    summary_parts = []
    body_lines = block_lines[1:]
 
    # Last line is expected to hold (or contain) the date
    date_line = body_lines[-1] if body_lines else ""
    date_match = DATE_RE.search(date_line)
    if date_match:
        record["date_raw"] = date_line.strip()
        record["date_iso"] = normalize_date(*date_match.groups())
        summary_lines = body_lines[:-1]
    else:
        summary_lines = body_lines
 
    summary_parts.extend(summary_lines)
    record["summary"] = " ".join(s.strip() for s in summary_parts if s.strip())
 
    return record
 
def parse_text(raw_text):
    blocks = split_into_blocks(raw_text)
    records = []
    for block in blocks:
        if not block:
            continue
        rec = parse_block(block)
        if rec["title"]:
            records.append(rec)
    return records
 
def main():
    project_root = Path(__file__).resolve().parents[1]
    in_path = project_root / "dataset" / "raw" / "data.txt"
    out_path = project_root / "dataset" / "processed" / "parsed_cases.json"

    with open(in_path, encoding="utf-8") as f:
        raw = f.read()
 
    records = parse_text(raw)
 
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
 
    print(f"Parsed {len(records)} cases -> {out_path}")
 
if __name__ == "__main__":
    main()