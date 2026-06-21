# RealEstateICM — סוכן ICM להתאמת נכסים

אתה סוכן ICM. תיקייה זו היא המוח שלך.

## חוקי יסוד
1. קרא תמיד `CONTEXT.md` כדי לנווט בין השלבים.
2. כשמבקשים שלב — קרא `stages/0X-NAME/CONTEXT.md` (collect → match → assign).
3. Layer 3 = `shared/`, `references/` — קרא רק מה שרשום ב-Inputs של השלב.
4. Layer 4 = `output/` של השלב הקודם.
5. לעולם אל תערוך `shared/match-config.json` או `scripts/`.
6. כתוב תוצרים ל-`output/` בלבד — דווח, והמתן לאישור אנושי לפני השלב הבא.
7. **נתונים טריים + חוכמת ריצות קודמות.** לפני תחילת collect — בדוק אם `01-collect/output/_run.json` קיים. אם כן, הצג למשתמש: ⏱️זמן הריצה הקודמת, 📊מספר לידים, 🏠מספר נכסים. תן בחירה: להמשיך עם קיים / לסרוק מחדש. אם המשתמש בוחר בסריקה חדשה — מחק את קבצי output הישנים, שלוף חי מ-MCP, כתוב חותמת זמן חדשה. לעולם אל תסתמך על `output/` מריצה קודמת בלי לשאול. אם `_run.json` לא קיים — פשוט שלוף חדש.

---

## Folder Map

```
RealEstateICM/
├── AGENTS.md          (you are here)
├── CONTEXT.md         (start here for task routing)
├── setup/             (onboarding questionnaire)
├── shared/            (match-config.json)
├── scripts/           (match.py - deterministic matcher)
├── deploy/            (profile-root router source)
└── stages/
    ├── 01-collect/    (pull leads + properties from prod MCP)
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
| Collect | `stages/01-collect/CONTEXT.md` (has embedded MCP docs) | stages 02-03, scripts/ |
| Match | `stages/02-match/CONTEXT.md`, `scripts/match.py`, `shared/match-config.json` | stages 01/03 |
| Assign | `stages/03-assign/CONTEXT.md` | scripts/, stages 01-02 |

## Stage Handoffs

Each stage writes to its own `output/` folder. The next stage reads from there. Edit an output file and the next stage picks up your edits.
