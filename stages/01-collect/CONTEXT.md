# Collect

Pull the realtor's open leads and full property inventory **fresh from prod via MCP** into local files. Every run pulls live — never reuse a previous run's data.

## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|--------------|---------------|-----|
| User | (conversation) | `{{REALTOR_USER_ID}}` | tenant scope for every call |
| Skill | `../../skills/nadlanai-platform-apis/SKILL.md` | sections 6-7 (MCP) | how to call the read tools |

## Process

> **MANDATORY each run. Do not skip, do not reuse old files.**

1. **Wipe stale output first.** Delete any previous artifacts so nothing carries over:
   ```sh
   rm -f output/leads.json output/properties.json output/_run.json
   ```
2. Initialize an MCP session (init → capture `Mcp-Session-Id`).
3. Call `list_leads(user_id={{REALTOR_USER_ID}})`. Keep: phone, full_name, transaction_type, budget, preferred_city, status, properties_to_offer.
4. Call `search_real_estate_properties(user_id={{REALTOR_USER_ID}})`. Keep: id, title, transaction_type, city, price.
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
