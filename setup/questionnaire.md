# Onboarding Questionnaire: Property Matching

Read this file when the user types "setup". Ask all questions in one pass. Collect answers,
then apply them across the workspace and verify no placeholders remain.

---

### Q1: Which realtor should this run for?
- The realtor's `user_id` (UUID). All leads and properties are scoped to this id.
- Type: free text (UUID)
- Fills: `{{REALTOR_USER_ID}}` everywhere it appears in `stages/`
- Default: none (required)

### Q2: How far over budget is still a match?
- A property is kept if its price is at most this fraction over the lead's budget.
- Type: number (fraction)
- Writes: `budget_tolerance` in `shared/match-config.json`
- Default: `0.15` (15 percent)

### Q3: How many matches per lead?
- Maximum suggested properties returned for each lead.
- Type: number
- Writes: `top_n` in `shared/match-config.json`
- Default: `3`

---

## After Onboarding

1. Replace `{{REALTOR_USER_ID}}` in every `stages/*/CONTEXT.md` with the Q1 answer.
2. Write Q2 and Q3 into `shared/match-config.json`.
3. Search the workspace for `{{` and confirm no placeholders remain.
4. Tell the user: "Setup done. Start with `stages/01-collect/CONTEXT.md` to pull leads and properties."
