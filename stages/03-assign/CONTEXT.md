# Report

Deliver match results to the realtor as a formatted report. No DB writes.

## Inputs

| Source | File/Location | Why |
|--------|--------------|-----|
| Match report | `../02-match/output/match-report.md` | human-readable results |
| Matches | `../02-match/output/matches.json` | structured data for summary stats |
| Leads | `../01-collect/output/leads.json` | lead count |

## Process

1. Read `match-report.md`.
2. Prepend a summary header:
   - Total leads scanned
   - Leads with at least one match
   - Leads with no match
3. Write final report to `output/final-report.md`.
4. Present the report to the user (paste inline).

## Output

| Artifact | Location | Format |
|----------|----------|--------|
| Final report | `output/final-report.md` | Markdown, ready to send/paste |

## Notes

- No DB writes in this stage.
- Report is the deliverable. User decides what to do next (send via WhatsApp, email, paste to CRM).
- If user wants to write `properties_to_offer` back to DB later, that is a separate stage-04 decision.
