---
name: nadlanai-platform-apis
description: Use when working on NadlanAI workflows — editing n8n workflows, calling Evolution API, querying Supabase, tracing Dify calls in Langfuse, or running closed-loop tests to verify end-to-end behavior across the WhatsApp bot stack.
---

# NadlanAI Platform APIs

## Overview

All services run on `nadlanai.org` subdomains. This skill covers credentials, key endpoints, and how to run a closed-loop test (trigger → verify n8n execution → verify Supabase state → trace Dify in Langfuse).

---

## 1. n8n

**URL:** `https://n8n.nadlanai.org`  
**API key:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxZWIyNjYyMy1mMTQwLTRhYzItOTQ5YS04OTU0MmRlMDE0ZGIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiNTU0OTNlNjMtMjg2Ny00YmE3LWJmYzMtZmI1MTBjYzlhNDIzIiwiaWF0IjoxNzgwNDk3NDk1fQ.aeZlOcjzjTsCMmrHnGs-mIXocr0h-EoxufVwyQLbq3s` (issued 2026-06-03). Generate at Settings > API. **If you get 401, key expired — ask user to paste a new one.**

Key workflow IDs:
| Workflow | ID |
|---|---|
| Main WhatsApp → Dify | `5DNOUbaTDxT6jDNb` |
| Catalog sender (standalone) | `Ac8TNRdLy7UO6qzJ` |
| Dify Lookup (conv_id bridge) | `W9DBUW4XKelkmGXN` |

**Read workflow:**
```bash
curl https://n8n.nadlanai.org/api/v1/workflows/5DNOUbaTDxT6jDNb \
  -H "X-N8N-API-KEY: <key>"
```

**Update workflow** (PUT — only these top-level keys are accepted: `name`, `nodes`, `connections`, `settings`, `staticData`):
```bash
curl -X PUT https://n8n.nadlanai.org/api/v1/workflows/5DNOUbaTDxT6jDNb \
  -H "X-N8N-API-KEY: <key>" \
  -H "Content-Type: application/json" \
  -d @payload.json
```

**Check latest execution:**
```bash
curl "https://n8n.nadlanai.org/api/v1/executions?workflowId=5DNOUbaTDxT6jDNb&limit=1" \
  -H "X-N8N-API-KEY: <key>"
```

Webhook path (no auth): `POST https://n8n.nadlanai.org/webhook/whatsapp-webhook`

---

## 2. Evolution API (WhatsApp gateway)

**URL:** `https://evolution-api.nadlanai.org`  
**Instance:** `NadlanAI Bot`  
**API key:** `aqo5YT24Stg5swTmAAk2PLQO5hFtZt3L`  
**Business owner JID:** `972555046885@s.whatsapp.net`

Key endpoints:

| Action | Method & Path |
|---|---|
| Send text | `POST /message/sendText/NadlanAI%20Bot` |
| Send product card | `POST /message/sendProduct/NadlanAI%20Bot` |
| Get WA catalog | `POST /business/getCatalog/NadlanAI%20Bot` |
| Get media as base64 | `POST /chat/getBase64FromMediaMessage/NadlanAI%20Bot` |
| Send typing indicator | `POST /chat/sendPresence/NadlanAI%20Bot` |

**Send text:**
```bash
curl -X POST https://evolution-api.nadlanai.org/message/sendText/NadlanAI%20Bot \
  -H "apikey: aqo5YT24Stg5swTmAAk2PLQO5hFtZt3L" \
  -H "Content-Type: application/json" \
  -d '{"number":"972535313995@s.whatsapp.net","text":"test"}'
```

**Get catalog:**
```bash
curl -X POST https://evolution-api.nadlanai.org/business/getCatalog/NadlanAI%20Bot \
  -H "apikey: aqo5YT24Stg5swTmAAk2PLQO5hFtZt3L" \
  -H "Content-Type: application/json" \
  -d '{"number":"972555046885"}'
```

Response structure: `{ catalog: [ { id, retailerId, name, ... } ] }` — `retailerId` maps to Supabase `properties.id`.

---

## 3. Supabase (database + storage)

**URL:** `https://supabase.nadlanai.org`  
**Token (anon):** `eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzdXBhYmFzZSIsImlhdCI6MTc3ODY5MDM0MCwiZXhwIjo0OTM0MzYzOTQwLCJyb2xlIjoiYW5vbiJ9.mzf3HnKlYcMQ0PdKUeHVZEOXv9rFTSOe5Q3xMQdtQUc`

**Query a lead:**
```bash
curl "https://supabase.nadlanai.org/rest/v1/leads?phone=eq.972535313995&select=*" \
  -H "apikey: <token>" -H "Authorization: Bearer <token>"
```

**Query properties:**
```bash
curl "https://supabase.nadlanai.org/rest/v1/properties?id=in.(1,2,3)&select=id,wa_id,title,price,property_images(s3_key,is_primary)" \
  -H "apikey: <token>"
```

**Call RPC:**
```bash
curl -X POST "https://supabase.nadlanai.org/rest/v1/rpc/save_conversation" \
  -H "apikey: <token>" -H "Content-Type: application/json" \
  -d '{"p_phone":"972535313995@s.whatsapp.net","p_app_id":"app-DJJFl9lDbTNHXnZqJYjma5rT","p_conversation_id":""}'
```

Key RPCs: `insert_seen_msg`, `upsert_buffer`, `claim_batch(p_phone, p_app_id, p_my_ts)`, `save_conversation(p_phone, p_app_id, p_conversation_id)`

**`whatsapp_conversations` table:** keyed on `(phone, app_id)`. `app_id` = Dify API key (`app-DJJFl9lDbTNHXnZqJYjma5rT`). Multiple chatflows can share the table without collision.

**Storage URL pattern:**
```
https://supabase.nadlanai.org/storage/v1/object/public/properties/<s3_key>
```

---

## 4. Dify (LLM agent)

**URL:** `https://dify.nadlanai.org`  
**App token:** `app-DJJFl9lDbTNHXnZqJYjma5rT`

**Send message:**
```bash
curl -X POST https://dify.nadlanai.org/v1/chat-messages \
  -H "Authorization: Bearer app-DJJFl9lDbTNHXnZqJYjma5rT" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": {"phone":"972535313995","full_name":"טסט"},
    "query": "שלום",
    "conversation_id": "",
    "response_mode": "blocking",
    "user": "972535313995"
  }'
```

Response fields: `answer` (text), `conversation_id` (save for next turn).

**Reset conversation** (force fresh Dify session for a phone):
```bash
curl -X POST "https://supabase.nadlanai.org/rest/v1/rpc/save_conversation" \
  -H "apikey: <token>" -H "Content-Type: application/json" \
  -d '{"p_phone":"972535313995@s.whatsapp.net","p_app_id":"app-DJJFl9lDbTNHXnZqJYjma5rT","p_conversation_id":""}'
```

**Dify Lookup — get conv_id for a phone:**
```bash
curl -X POST "https://n8n.nadlanai.org/webhook/dify-lookup" \
  -H "Content-Type: application/json" \
  -d '{"phone":"972535313995","app_id":"app-DJJFl9lDbTNHXnZqJYjma5rT"}'
```
Returns: `{ phone, remoteJid, app_id, conversation_id, full_name, found_conversation, found_lead }`

---

## 5. Langfuse (observability)

**URL:** `https://langfuse.nadlanai.org`  
**Public key:** `pk-lf-e462c29e-3422-470c-baf4-8746101c5abe`  
**Secret key:** `sk-lf-4fb54da5-ff59-422f-9cd5-0e015c1060f4`  
**Auth:** HTTP Basic — public key as username, secret key as password.

**Get recent traces:**
```bash
curl -u "pk-lf-e462c29e-3422-470c-baf4-8746101c5abe:sk-lf-4fb54da5-ff59-422f-9cd5-0e015c1060f4" \
  "https://langfuse.nadlanai.org/api/public/traces?limit=5"
```

**Filter by user (phone number):**
```bash
curl -u "pk-lf-...:sk-lf-..." \
  "https://langfuse.nadlanai.org/api/public/traces?userId=972535313995&limit=5"
```

Use Langfuse UI for full trace details including tool calls, prompts, and errors.

---

## 6. MCP / dify-tools (Dify agent tools)

**URL:** `https://dify-tools.nadlanai.org/mcp`  
**Protocol:** JSON-RPC 2.0 (streamable-http)  
**Purpose:** Tools exposed to Dify chatflow agents (lead management, property search)

Two-step flow: init → get session ID → call tool.

**Step 1 — init:**
```bash
curl -X POST https://dify-tools.nadlanai.org/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
# Save the mcp-session-id response header
```

**Step 2 — call tool:**
```bash
curl -X POST https://dify-tools.nadlanai.org/mcp \
  -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: <session-id>" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"register_new_lead","arguments":{"phone":"972535313995","full_name":"טסט"}}}'
```

Key tools: `register_new_lead(phone, full_name)`, `update_lead_properties_to_offer(phone, property_ids[])`

---

## 7. MCP / NadlanAi-Service (property management)

**URL:** `https://mcp.nadlanai.org/mcp`  
**Protocol:** JSON-RPC 2.0 (streamable-http)  
**Purpose:** Full property & lead management API — used by the hub admin UI and agents to create/update listings, upload images, manage leads.

Same two-step init flow as section 6 — the `mcp-session-id` header comes back in the **response headers** of the init call.

**Step 1 — init (save header):**
```bash
curl -X POST https://mcp.nadlanai.org/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -D /tmp/mcp_headers.txt \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' \
  > /dev/null
SESSION=$(grep -i "mcp-session-id" /tmp/mcp_headers.txt | awk '{print $2}' | tr -d '\r\n')
```

**Step 2 — list tools:**
```bash
curl -s -X POST https://mcp.nadlanai.org/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SESSION" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
```

**Step 3 — call tool:**
```bash
curl -X POST https://mcp.nadlanai.org/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SESSION" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"add_new_property_listing","arguments":{...}}}'
```

**Key tools:**

| Tool | Purpose |
|---|---|
| `add_new_property_listing` | Create new property. Required: `title, transaction_type, city, address, property_type, rooms, area_sqm, price, property_condition` |
| `upload_image_to_property` | Upload image (base64 or URL) to a property. Required: `property_id, image_type, image_source`. Optional: `label, is_primary` |
| `get_property_full_details` | Get full property by ID |
| `search_real_estate_properties` | Search by city, type, price, rooms |
| `search_real_estate_properties_by_admin` | Same + `edit_mode_url` flag for hub links |
| `register_new_lead` | Create/update lead |
| `update_lead_properties_to_offer` | Set property IDs for a lead |
| `create_post` | Create draft social post linked to a property |
| `upload_image_to_post` | Attach image to a post |
| `publish_post_to_facebook` | Publish post to Facebook |

**`add_new_property_listing` full schema:**
```json
{
  "title": "string",
  "transaction_type": "sale | rent",
  "city": "string",
  "address": "string",
  "property_type": "string",
  "rooms": "number",
  "area_sqm": "number",
  "price": "number",
  "property_condition": "string",
  "neighborhood": "string | null",
  "floor": "string | null",
  "parking": false,
  "elevator": false,
  "balcony": false
}
```

**Common mistake:** The init call must go to a **separate** request — you cannot reuse a session across multiple Node.js/fetch calls without passing the header. In the browser (hub), use a small `mcpClient` wrapper that initializes once and reuses the session.

---

## Closed-Loop Test Procedure

Run this sequence to verify a full flow works end-to-end:

### Step 1 — Trigger
```bash
# Simulate flat-format webhook (Evolution Bot format)
curl -X POST https://n8n.nadlanai.org/webhook/whatsapp-webhook \
  -H "Content-Type: application/json" \
  -d '{
    "chatInput": "שלום",
    "keyId": "TEST-MSG-001",
    "remoteJid": "972535313995@s.whatsapp.net",
    "pushName": "טסט",
    "fromMe": false,
    "instanceName": "NadlanAI Bot"
  }'
```

### Step 2 — Check n8n execution
Open `https://n8n.nadlanai.org/workflow/5DNOUbaTDxT6jDNb` > Executions tab.  
Or via API:
```bash
curl "https://n8n.nadlanai.org/api/v1/executions?workflowId=5DNOUbaTDxT6jDNb&limit=3" \
  -H "X-N8N-API-KEY: <key>"
```
Look for: `status: success`, all nodes green. Red node = check its output for error.

### Step 3 — Verify Supabase
```bash
# Check lead was seen / buffer updated
curl "https://supabase.nadlanai.org/rest/v1/leads?phone=eq.972535313995&select=phone,stage,properties_to_offer,conversation_id" \
  -H "apikey: <token>"
```

### Step 4 — Trace Dify in Langfuse (if Dify call failed or answer is wrong)
```bash
curl -u "pk-lf-e462c29e-3422-470c-baf4-8746101c5abe:sk-lf-4fb54da5-ff59-422f-9cd5-0e015c1060f4" \
  "https://langfuse.nadlanai.org/api/public/traces?userId=972535313995@s.whatsapp.net&limit=3"
```
Open the trace URL from the response in the Langfuse UI to see the full LLM call, tool calls, and errors.

### Step 5 — Check WhatsApp (manual)
Open the phone / WhatsApp Business account and confirm the message arrived.

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| n8n API returns 401 | Key expired — generate new at Settings > API |
| n8n PUT rejected `additionalProperties` | Strip all fields except `name, nodes, connections, settings, staticData` |
| Evolution returns "no available server" | Hardcode URL to `evolution-api.nadlanai.org`, don't use `body.serverUrl` from webhook |
| Supabase returns empty array | Check filter — phone must match exactly (e.g. `972535313995` not `972535313995@s.whatsapp.net`) |
| Langfuse traces empty | Filter by `userId` = full remoteJid (`972535313995@s.whatsapp.net`) |
| MCP call fails with 400 | Missing `Mcp-Session-Id` header — must initialize first and pass the header |
