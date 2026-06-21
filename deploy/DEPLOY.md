# DEPLOY — התקנת RealEstateICM בפרופיל Hermes `icm-poc`

מדריך מלא להעלאת ה-workspace לתוך הבוט. כל פקודה מיועדת לריצה בתוך
ה-container של Hermes (shell של הסוכן). אחרי כל שלב יש בדיקת אימות —
אל תתקדם אם האימות נכשל.

## נתיבים קבועים

| מה | נתיב |
|----|------|
| שורש הפרופיל | `/home/hermeswebui/.hermes/profiles/icm-poc/` |
| תיקיית workspace | `/home/hermeswebui/.hermes/profiles/icm-poc/workspace/` |
| יעד ה-clone | `/home/hermeswebui/.hermes/profiles/icm-poc/workspace/RealEstateICM/` |
| כתובת הריפו | `https://github.com/RanTheUnderOne/RealEstateICM.git` |

---

## שלב 0 — בדיקות מקדימות (מה צריך להיות קיים)

```bash
git --version          # חייב להחזיר גרסה. אם אין git — עצור, צריך להתקין.
python3 --version      # נדרש להרצת scripts/match.py (stdlib בלבד, בלי pip)
ls -d /home/hermeswebui/.hermes/profiles/icm-poc/workspace/   # התיקייה חייבת להתקיים
```

אימות: שלוש הפקודות עברו בלי שגיאה. אם `workspace/` לא קיים:
```bash
mkdir -p /home/hermeswebui/.hermes/profiles/icm-poc/workspace/
```

---

## שלב 1 — שכפול הריפו (CREATE: תיקיית RealEstateICM)

```bash
cd /home/hermeswebui/.hermes/profiles/icm-poc/workspace/
git clone https://github.com/RanTheUnderOne/RealEstateICM.git
```

אימות:
```bash
ls -la /home/hermeswebui/.hermes/profiles/icm-poc/workspace/RealEstateICM/
# חייב להופיע: AGENTS.md  CONTEXT.md  shared/  scripts/  setup/  stages/  deploy/
```

> אם התיקייה כבר קיימת מריצה קודמת — מחק קודם: `rm -rf RealEstateICM` ואז clone מחדש.

---

## שלב 2 — הצבת ה-AGENTS.md של שורש הפרופיל (CREATE: הנתב)

זהו ה-AGENTS.md השני (הנתב). הוא יושב ליד `SOUL.md` ומפנה את הסוכן אל ה-workspace.

```bash
cp /home/hermeswebui/.hermes/profiles/icm-poc/workspace/RealEstateICM/deploy/AGENTS.profile-root.md \
   /home/hermeswebui/.hermes/profiles/icm-poc/AGENTS.md
```

אימות:
```bash
cat /home/hermeswebui/.hermes/profiles/icm-poc/AGENTS.md
# חייב להתחיל ב: "# icm-poc — נתב ICM"
ls /home/hermeswebui/.hermes/profiles/icm-poc/   # חייבים להופיע יחד: AGENTS.md ו-SOUL.md
```

---

## שלב 3 — אימות שני קבצי AGENTS.md (BUILD: מבנה שני-שכבות)

```bash
echo "=== ROUTER (שורש פרופיל) ==="
cat /home/hermeswebui/.hermes/profiles/icm-poc/AGENTS.md
echo "=== BRAIN (workspace) ==="
cat /home/hermeswebui/.hermes/profiles/icm-poc/workspace/RealEstateICM/AGENTS.md
```

אימות: הראשון = "נתב ICM" (מפנה ל-workspace/RealEstateICM). השני = "סוכן ICM
להתאמת נכסים" (6 חוקי יסוד). שניהם בעברית.

---

## שלב 4 — מבחן זהב (BUILD/TEST: ודא שהמנוע רץ ב-container)

מאמת ש-`scripts/match.py` עובד בתוך הסביבה לפני שמפעילים את ה-pipeline.

```bash
cd /home/hermeswebui/.hermes/profiles/icm-poc/workspace/RealEstateICM/
bash tests/run-golden.sh
```

אימות: הטסט מסתיים ב-PASS (התאמות תואמות ל-`tests/expected-matches.json`).
אם נכשל — בעיה בסביבת python, לא בפריסה.

---

## שלב 5 — בחירת ה-workspace ב-WebUI (פעולה אנושית)

1. פתח את WebUI של Hermes, פרופיל `icm-poc`.
2. בבורר ה-workspace בחר את התיקייה:
   `workspace/RealEstateICM`
3. מרגע הבחירה — Hermes מזריק אוטומטית את `AGENTS.md` מאותה תיקייה.

אימות: שאל את הסוכן "מה אתה?" — הוא אמור לזהות עצמו כסוכן ICM להתאמת נכסים
ולהפנות ל-CONTEXT.md.

---

## שלב 6 — הפעלת ה-pipeline (טריגרים)

| טריגר | פעולה |
|-------|-------|
| `setup` | מריץ את שאלון ההיכרות החד-פעמי (`setup/questionnaire.md`) |
| `status` | מציג השלמת שלבים לכל ה-pipeline |

זרימת השלבים (כל שלב מסתיים בנקודת אישור אנושית — אין התקדמות אוטומטית):
1. **01-collect** — משיכת לידים ונכסים מ-prod דרך MCP → `stages/01-collect/output/`
2. **02-match** — הרצת `scripts/match.py` הדטרמיניסטי → `stages/02-match/output/`
3. **03-assign** — בניית דוח התאמות למתווך (ללא כתיבה ל-DB) → `stages/03-assign/output/`

---

## Rollback (ביטול מלא)

```bash
rm -rf /home/hermeswebui/.hermes/profiles/icm-poc/workspace/RealEstateICM/
rm -f  /home/hermeswebui/.hermes/profiles/icm-poc/AGENTS.md
```

---

## תקלות נפוצות

| תסמין | סיבה | תיקון |
|-------|------|-------|
| `Gemini returned HTTP 404` בכל קריאה | מודל הסוכן מוגדר ל-Gemini במקום Deepseek | תקן provider ל-Deepseek ב-env של `hermes-agent` (Coolify) |
| הסוכן לא מזהה עצמו כ-ICM | לא נבחר ה-workspace הנכון ב-WebUI | בחר `workspace/RealEstateICM` במדויק |
| `git clone` נכשל | אין רשת יוצאת מה-container | ודא גישת אינטרנט / proxy |
| מבחן הזהב נכשל | python חסר/שגוי | ודא `python3` זמין ב-container |
