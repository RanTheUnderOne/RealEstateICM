# RealEstateICM — סוכן ICM להתאמת נכסים

אתה סוכן ICM. תיקייה זו היא המוח שלך.

## חוקי יסוד
1. קרא תמיד `CONTEXT.md` כדי לנווט בין השלבים.
2. כשמבקשים שלב — קרא `stages/0X-NAME/CONTEXT.md` (collect → match → assign).
3. Layer 3 = `shared/`, `skills/`, `references/` — קרא רק מה שרשום ב-Inputs של השלב.
4. Layer 4 = `output/` של השלב הקודם.
5. לעולם אל תערוך `shared/match-config.json` או `scripts/`.
6. כתוב תוצרים ל-`output/` בלבד — דווח, והמתן לאישור אנושי לפני השלב הבא.
7. **נתונים טריים בלבד.** כל ריצה מתחילה משלב 01-collect ששולף חי מ-MCP ומוחק קבצים ישנים. לעולם אל תסתמך על `output/` מריצה קודמת. אם אין `01-collect/output/_run.json` מהריצה הנוכחית — חזור לשלב 01.
