# Property Matching

Matches a realtor's leads to their property inventory in three stages, with human approval before any live write.

## Task Routing

| Task Type | Go To | Description |
|-----------|-------|-------------|
| Collect | `stages/01-collect/CONTEXT.md` | Pull leads and properties from prod via MCP |
| Match | `stages/02-match/CONTEXT.md` | Run the deterministic matcher and review results |
| Assign | `stages/03-assign/CONTEXT.md` | Write approved matches back to prod via MCP |

## Shared Resources

| Resource | Location | Contains |
|----------|----------|----------|
| Match config | `shared/match-config.json` | Tunable constants: budget tolerance, top N |
| Matcher script | `scripts/match.py` | Deterministic match logic (no LLM) |
| Platform skill | `skills/nadlanai-platform-apis/SKILL.md` | MCP endpoints, tool usage, closed-loop test |
