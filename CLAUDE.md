# Property Matching

Scans a realtor's leads and suggests matching properties from that realtor's inventory, with a human checkpoint before anything is written back to the live system.

## Folder Map

```
property-matching/
├── CLAUDE.md          (you are here)
├── CONTEXT.md         (start here for task routing)
├── setup/             (onboarding questionnaire)
├── skills/            (bundled: nadlanai-platform-apis)
├── shared/            (match-config.json)
├── scripts/           (match.py - deterministic matcher)
├── tests/             (golden test: fixtures + expected output)
└── stages/
    ├── 01-collect/    (pull leads + properties from prod)
    ├── 02-match/      (run deterministic match.py)
    └── 03-assign/     (deliver match report to realtor — no DB writes)
```

## Triggers

| Keyword | Action |
|---------|--------|
| `setup` | Run onboarding questionnaire |
| `status` | Show pipeline completion for all stages |

## Routing

| Task | Go To |
|------|-------|
| Pull leads and properties | `stages/01-collect/CONTEXT.md` |
| Compute matches | `stages/02-match/CONTEXT.md` |
| Deliver report to realtor | `stages/03-assign/CONTEXT.md` |

## What to Load

| Task | Load These | Do NOT Load |
|------|-----------|-------------|
| Collect | `stages/01-collect/CONTEXT.md`, skill sections 6-7 | stages 02-03, scripts/ |
| Match | `stages/02-match/CONTEXT.md`, `scripts/match.py`, `shared/match-config.json` | the skill, stages 01/03 |
| Assign | `stages/03-assign/CONTEXT.md`, skill sections 6-7 | scripts/, stages 01-02 |

## Stage Handoffs

Each stage writes to its own `output/` folder. The next stage reads from there. Edit an output file and the next stage picks up your edits.
