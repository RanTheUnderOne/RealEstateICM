# Collect

Pull the realtor's open leads and full property inventory **fresh from prod via MCP** into local files. Every run pulls live — never reuse a previous run's data.

## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|--------------|---------------|-----|
| User | (conversation) | `{{REALTOR_USER_ID}}` | tenant scope for every call |
| Skill | `../../skills/nadlanai-platform-apis/SKILL.md` | section 7 (prod-mcp) | how to call the read tools |

## Process

> **MANDATORY each run. Check for prior run before pulling. Do not blindly reuse old files.**

0. **Check for prior run.** If `output/_run.json` exists, read it and present to user:
   ```
   נמצאה ריצה קודמת:
   ⏱️  זמן: <run_id/timestamp>
   📊 לידים: <lead_count>
   🏠 נכסים: <property_count>

   להשתמש בתוצאות הקיימות, או לסרוק מחדש?
   ```
   Wait for user decision:
   - **Existing** → jump to step 6 (keep outputs, skip pull). Same `_run.json` stays.
   - **Fresh scan** → continue to step 1.

1. **Wipe stale output.** Delete previous artifacts so nothing carries over:
   ```sh
   rm -f output/leads.json output/properties.json output/_run.json
   ```
2. Initialize an MCP session (init → capture `Mcp-Session-Id`).
3. Call `list_leads(user_id={{REALTOR_USER_ID}})`. Keep: phone, full_name, transaction_type, budget, preferred_city, status, properties_to_offer.
4. Call `search_real_estate_properties(user_id={{REALTOR_USER_ID}}, limit=100)`. Default limit is 5 — always pass `limit=100` to get full inventory. Keep: id, title, transaction_type, city, price.
5. Save both to `output/` (overwrite).
6. **Write the run stamp** `output/_run.json` so freshness is auditable:
   ```json
   { "run_id": "<utc timestamp e.g. 2026-06-21T22:15:03Z>", "source": "mcp-live", "lead_count": <n>, "property_count": <n> }
   ```

## Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Leads | `output/leads.json` | `[{phone, full_name, transaction_type, budget, preferred_city, status, properties_to_offer[]}]` |
| Properties | `output/properties.json` | `[{id, title, transaction_type, city, price}]` |
| Run stamp | `output/_run.json` | `{run_id, source, lead_count, property_count}` |

## Audit

| Check | Pass Condition |
|-------|---------------|
| Fresh pull | `output/_run.json` exists and `run_id` is the current run's timestamp |
| No carry-over | Old leads/properties were deleted in step 1 before pulling |
