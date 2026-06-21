# Collect

Pull the realtor's open leads and full property inventory from prod into local files.

## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|--------------|---------------|-----|
| User | (conversation) | `{{REALTOR_USER_ID}}` | tenant scope for every call |
| Skill | `../../skills/nadlanai-platform-apis/SKILL.md` | sections 6-7 (MCP) | how to call the read tools |

## Process

1. Initialize an MCP session (init -> capture `Mcp-Session-Id`).
2. Call `list_leads(user_id={{REALTOR_USER_ID}})`. Keep: phone, full_name, transaction_type, budget, preferred_city, status, properties_to_offer.
3. Call `search_real_estate_properties(user_id={{REALTOR_USER_ID}})`. Keep: id, title, transaction_type, city, price.
4. Save both to output/.

## Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Leads | `output/leads.json` | `[{phone, full_name, transaction_type, budget, preferred_city, status, properties_to_offer[]}]` |
| Properties | `output/properties.json` | `[{id, title, transaction_type, city, price}]` |
