#!/usr/bin/env python3
"""Build a human-readable match report: which lead fits which property.

Usage:
    python report.py <leads.json> <properties.json> <matches.json> <out report.md>
"""
import json
import sys
from datetime import date


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def main():
    leads = {l["phone"]: l for l in load(sys.argv[1])}
    props = {p["id"]: p for p in load(sys.argv[2])}
    matches = load(sys.argv[3])
    out = sys.argv[4]

    lines = ["# Property Match Report", "", "Date: {}".format(date.today().isoformat()), ""]

    for m in matches:
        lead = leads.get(m["phone"], {})
        name = lead.get("full_name") or m["phone"]
        crit = "{}, {}, budget {}".format(
            lead.get("transaction_type"), lead.get("preferred_city"), lead.get("budget"))
        lines.append("## {}  ({})".format(name, crit))

        if not m["candidates"]:
            lines.append("No matching properties.")
            lines.append("")
            continue

        for i, c in enumerate(m["candidates"], 1):
            p = props.get(c["property_id"], {})
            same = "same city" if p.get("city") == lead.get("preferred_city") else "different city"
            lines.append("{}. Property #{} - {} - {} - {:,} NIS  ({})".format(
                i, c["property_id"], p.get("title", "?"), p.get("city", "?"),
                c.get("price") or 0, same))
        lines.append("")

    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("wrote", out)


if __name__ == "__main__":
    main()
