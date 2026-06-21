#!/usr/bin/env python3
"""Deterministic lead -> property matcher. No LLM. Same input -> same output.

Usage:
    python match.py <leads.json> <properties.json> <out matches.json> [match-config.json]

Rule per lead: keep a property if transaction_type matches AND
price <= budget * (1 + budget_tolerance).
Rank kept properties by same-city first,
then cheapest, with a stable tie-break on property id. Take top_n.
"""
import json
import sys


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def match_lead(lead, properties, tolerance, top_n):
    budget = lead.get("budget")
    ttype = lead.get("transaction_type")
    pref_city = lead.get("preferred_city")

    eligible = []
    if budget is not None and ttype is not None:
        ceiling = budget * (1 + tolerance)
        for p in properties:
            if p.get("transaction_type") != ttype:
                continue
            if p.get("price") is None or p["price"] > ceiling:
                continue
            eligible.append(p)

    # rank: same city first (0 before 1), then cheapest, then id (stable)
    def sort_key(p):
        same_city = 0 if pref_city and p.get("city") == pref_city else 1
        return (same_city, p.get("price", 0), p["id"])

    eligible.sort(key=sort_key)

    candidates = []
    for p in eligible[:top_n]:
        same = pref_city and p.get("city") == pref_city
        reason = "price {} <= budget {} x {}; {}".format(
            p.get("price"), budget, 1 + tolerance,
            "same city {}".format(pref_city) if same else "different city {}".format(p.get("city")),
        )
        candidates.append({
            "property_id": p["id"],
            "price": p.get("price"),
            "city": p.get("city"),
            "reason": reason,
        })

    return {
        "phone": lead.get("phone"),
        "eligible_count": len(eligible),
        "candidates": candidates,
    }


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)
    leads = load(sys.argv[1])
    properties = load(sys.argv[2])
    out_path = sys.argv[3]
    cfg = load(sys.argv[4]) if len(sys.argv) > 4 else {"budget_tolerance": 0.15, "top_n": 3}

    tolerance = cfg.get("budget_tolerance", 0.15)
    top_n = cfg.get("top_n", 3)

    results = [match_lead(l, properties, tolerance, top_n) for l in leads]

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    matched = sum(1 for r in results if r["candidates"])
    print("leads: {} | with matches: {} | no match: {}".format(
        len(results), matched, len(results) - matched))


if __name__ == "__main__":
    main()
