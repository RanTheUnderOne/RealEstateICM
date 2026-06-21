# Collect

Pull the realtor's open leads and full property inventory **fresh from prod via MCP** into local files. Every run pulls live — never reuse a previous run's data.

## MCP Connection

| Field | Value |
|-------|-------|
| URL | `https://prod-mcp.nadlanai.org/mcp` |
| Protocol | JSON-RPC 2.0 (streamable-http) |

Two-step flow: init → get `Mcp-Session-Id` from response headers → call tools.

**Step 1 — init:**
```bash
curl -X POST https://prod-mcp.nadlanai.org/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -D /tmp/mcp_headers.txt \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"icm-collect","version":"1.0"}}}' \
  > /dev/null
SESSION=$(grep -i "mcp-session-id" /tmp/mcp_headers.txt | awk '{print $2}' | tr -d '\r\n')
```

**Step 2 — call tool:**
```bash
curl -X POST https://prod-mcp.nadlanai.org/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SESSION" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"<tool>","arguments":{...}}}'
```

## Read Tools

| Tool | Purpose | Required Param |
|------|---------|---------------|
| `list_leads` | Get all leads for a user | `user_id` |
| `get_lead_profile` | Get full lead profile | `user_id` |
| `search_real_estate_properties` | Search properties by city, type, price, rooms | `user_id` |
| `get_property_full_details` | Get full property by ID | `user_id` |

## Inputs

| Source | File/Location | Why |
|--------|--------------|-----|
| User | (conversation) `{{REALTOR_USER_ID}}` | tenant scope for every call |

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
3. Call `list_leads(user_id={{REALTOR_USER_ID}})`. Keep: phone, full_name, transaction_type, budget, preferred_city, status.
4. Call `search_real_estate_properties(user_id={{REALTOR_USER_ID}}, limit=100)`. Default limit is 5 — always pass `limit=100` to get full inventory. Keep: id, title, transaction_type, city, price.
5. Save both to `output/` (overwrite).
6. **Write the run stamp** `output/_run.json` so freshness is auditable:
   ```json
   { "run_id": "<utc timestamp e.g. 2026-06-21T22:15:03Z>", "source": "mcp-live", "lead_count": <n>, "property_count": <n> }
   ```

## Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Leads | `output/leads.json` | `[{phone, full_name, transaction_type, budget, preferred_city, status}]` |
| Properties | `output/properties.json` | `[{id, title, transaction_type, city, price}]` |
| Run stamp | `output/_run.json` | `{run_id, source, lead_count, property_count}` |

## Pitfalls

| Symptom | Cause | Fix |
|---------|-------|-----|
| `search_real_estate_properties` returns too few results | Default limit is 5 | Always pass `limit=100` |
| `list_leads` returns empty | Wrong `user_id` | Verify tenant ID exactly |
| MCP returns 400 | Missing `Mcp-Session-Id` | Must init first, save session header |
| `get_property_full_details` errors | Missing `user_id` | Always pass it |

## Audit

| Check | Pass Condition |
|-------|---------------|
| Fresh pull | `output/_run.json` exists and `run_id` is the current run's timestamp |
| No carry-over | Old leads/properties were deleted in step 1 before pulling |
