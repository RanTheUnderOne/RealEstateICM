# Match

Run the deterministic matcher over the collected leads and properties. No LLM.

## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|--------------|---------------|-----|
| Collect | `../01-collect/output/leads.json` | Full file | who to match |
| Collect | `../01-collect/output/properties.json` | Full file | the inventory |
| Config | `../../shared/match-config.json` | Full file | budget tolerance, top N |
| Script | `../../scripts/match.py` | Full file | the match logic |

## Process

1. Run: `python ../../scripts/match.py ../01-collect/output/leads.json ../01-collect/output/properties.json output/matches.json ../../shared/match-config.json`
2. Read `output/matches.json` and present each lead's candidates with their reason.

## Checkpoints

| After Step | Agent Presents | Human Decides |
|------------|---------------|---------------|
| 2 | Per-lead top matches with keep/rank reason, plus any lead with zero matches | Approve, edit, or drop matches before assign |

## Audit

| Check | Pass Condition |
|-------|---------------|
| Hard filter honored | Every candidate has matching transaction_type and price within tolerance |
| No-match visible | Leads with `eligible_count` 0 are shown, not hidden |
| Reproducible | Re-running on the same inputs yields an identical `matches.json` |

## Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Matches | `output/matches.json` | `[{phone, eligible_count, candidates:[{property_id, price, city, reason}]}]` |
