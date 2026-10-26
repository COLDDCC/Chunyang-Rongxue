#!/usr/bin/env python3
"""Check that Markdown table total rows equal the sum of the rows above them.

Standard library only. For every table (including tables inside blockquotes), a row
whose first cell contains a total label (合计 / 总计 / 小计 / Total / Subtotal / Sum)
is compared, column by column, with the rows above it since the previous total.
Cells may hold a number or a range such as "3,000–8,000", optionally with currency
symbols, "约", "≈", "US$", "¥", "万" or Markdown emphasis. A column is checked only
when every summed cell and the total cell parse as numbers; otherwise it is skipped.
Totals must match exactly (to the precision shown) unless marked approximate with
"≈" or "约"; an approximate total may differ by half of its rounding unit
(≈15,600 accepts 15,550–15,650).

Exit codes: 0 = no mismatches, 1 = mismatch found, 2 = unreadable file / usage.
This catches arithmetic drift between copies of a figure; it cannot tell whether
the underlying figures are true.
"""
import argparse
import re
import sys
from pathlib import Path

TOTAL = re.compile(r"(合计|总计|小计|共计|\btotal\b|\bsubtotal\b|\bsum\b)", re.I)
NUMBER = r"\d[\d,]*(?:\.\d+)?"
VALUE = re.compile(rf"^({NUMBER})(?:\s*(?:–|—|-|~|～|至|to)\s*({NUMBER}))?$")
NOISE = re.compile(r"(\*\*|__|`|US\$|S\$|HK\$|NT\$|RMB|USD|CNY|[$¥￥€£฿≈约~]|万|元|美元|天|晚|年)", re.I)
SEPARATOR = re.compile(r"^:?-{2,}:?$")
APPROX = re.compile(r"[≈约]")


def rounding_unit(cell):
    """Smallest unit the written total was rounded to."""
    text = NOISE.sub("", cell).strip().replace(",", "")
    numbers = re.findall(r"\d+(?:\.\d+)?", text)
    units = []
    for n in numbers:
        if "." in n:
            units.append(10 ** -len(n.split(".")[1]))
        else:
            zeros = len(n) - len(n.rstrip("0"))
            units.append(10 ** min(zeros, max(len(n) - 2, 0)))
    return min(units) if units else 1


def parse_value(cell):
    """Return (low, high, decimals) for a numeric cell, or None."""
    text = NOISE.sub("", cell).strip()
    match = VALUE.match(text)
    if not match:
        return None
    low = match.group(1).replace(",", "")
    high = (match.group(2) or match.group(1)).replace(",", "")
    decimals = max(len(x.split(".")[1]) if "." in x else 0 for x in (low, high))
    return float(low), float(high), decimals


def split_row(line):
    line = re.sub(r"^\s*(>\s*)+", "", line).strip()
    if not (line.startswith("|") and line.endswith("|")):
        return None
    return [c.strip() for c in line[1:-1].split("|")]


def tables(text):
    """Yield (start_line, rows) for each Markdown table."""
    current, start = [], 0
    for number, line in enumerate(text.splitlines(), 1):
        row = split_row(line)
        if row is None:
            if current:
                yield start, current
            current = []
            continue
        if not current:
            start = number
        if all(SEPARATOR.match(c) for c in row if c):
            continue
        current.append((number, row))
    if current:
        yield start, current


def check_table(rows, rel_tol):
    problems = []
    header, body = rows[0][1], rows[1:]
    block = []
    for line, row in body:
        if row and TOTAL.search(NOISE.sub("", row[0])):
            for col in range(1, len(row)):
                total = parse_value(row[col]) if row[col] else None
                if total is None or not block:
                    continue
                parts = [parse_value(r[col]) if col < len(r) else None for _, r in block]
                if any(p is None for p in parts):
                    continue
                low, high = sum(p[0] for p in parts), sum(p[1] for p in parts)
                step = 10 ** -max([total[2]] + [p[2] for p in parts])
                allowed = rounding_unit(row[col]) / 2 if APPROX.search(row[col]) else step / 2
                for got, want in ((total[0], low), (total[1], high)):
                    if abs(got - want) > max(allowed + 1e-9, abs(want) * rel_tol):
                        name = header[col] if col < len(header) and header[col] else f"column {col + 1}"
                        problems.append(f"line {line}: '{row[0]}' / {name}: total {row[col]} but rows sum to "
                                        + (f"{low:g}" if low == high else f"{low:g}–{high:g}"))
                        break
            block = []
        else:
            block.append((line, row))
    return problems


def check(text, rel_tol=0.0):
    problems, checked = [], 0
    for _, rows in tables(text):
        if len(rows) > 1 and any(r and TOTAL.search(NOISE.sub("", r[0])) for _, r in rows[1:]):
            checked += 1
            problems += check_table(rows, rel_tol)
    return checked, problems


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("files", nargs="+")
    parser.add_argument("--rel-tol", type=float, default=0.0,
                        help="extra relative tolerance, e.g. 0.01 for 1%% (default 0)")
    args = parser.parse_args(argv)
    failed = False
    for name in args.files:
        try:
            text = Path(name).read_text(encoding="utf-8")
        except OSError as exc:
            print(f"Cannot read {name}: {exc}", file=sys.stderr)
            return 2
        checked, problems = check(text, args.rel_tol)
        print(f"{name}: {checked} table(s) with totals checked, {len(problems)} mismatch(es)")
        for problem in problems:
            print("  - " + problem)
        failed = failed or bool(problems)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
