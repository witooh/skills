---
name: state-db
description: >-
  Centralized state management layer for all Claude Code skills using Supabase.
  Provides persistent read/write access to a shared database via REST API.
  Use this skill whenever another skill needs to persist data, retrieve stored
  state, or manage records across sessions. Trigger on: "save state", "load state",
  "persist data", "skill state", "state-db", "read from db", "write to db",
  "supabase", "skill_state", or when any skill needs to store or retrieve
  persistent data. Also use when building or modifying skills that require
  cross-session memory or shared data storage.
metadata:
  author: witooh
  version: "1.0"
---

# State DB

Centralized state management for Claude Code skills via Supabase REST API.

## Environment Variables

Read credentials from shell environment:

```bash
URL="$STATE_DB_SUPABASE_URL"
KEY="$STATE_DB_SUPABASE_ANON_KEY"
```

All curl commands below use these variables. Ensure they are set before executing.

## Table Schema

Table: `skill_state`

| Column | Type | Note |
|--------|------|------|
| id | BIGSERIAL | PRIMARY KEY |
| skill_name | TEXT | e.g. 'food-tracking', 'dca' |
| key | TEXT | optional sub-type, e.g. 'entry', 'config' |
| data | JSONB | schemaless payload |
| created_at | TIMESTAMPTZ | DEFAULT NOW() |
| updated_at | TIMESTAMPTZ | DEFAULT NOW(), auto-updated via trigger |

---

## Operations

### INSERT

```bash
curl -s -X POST "$STATE_DB_SUPABASE_URL/rest/v1/skill_state" \
  -H "apikey: $STATE_DB_SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $STATE_DB_SUPABASE_ANON_KEY" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{
    "skill_name": "food-tracking",
    "key": "entry",
    "data": {"meal": "lunch", "items": ["rice", "chicken"], "phosphorus_mg": 250}
  }'
```

### QUERY

**By skill_name:**

```bash
curl -s "$STATE_DB_SUPABASE_URL/rest/v1/skill_state?skill_name=eq.food-tracking&order=created_at.desc" \
  -H "apikey: $STATE_DB_SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $STATE_DB_SUPABASE_ANON_KEY"
```

**By skill_name + key:**

```bash
curl -s "$STATE_DB_SUPABASE_URL/rest/v1/skill_state?skill_name=eq.food-tracking&key=eq.entry&order=created_at.desc" \
  -H "apikey: $STATE_DB_SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $STATE_DB_SUPABASE_ANON_KEY"
```

**By date range:**

```bash
curl -s "$STATE_DB_SUPABASE_URL/rest/v1/skill_state?skill_name=eq.food-tracking&created_at=gte.2026-03-01T00:00:00Z&created_at=lt.2026-03-15T00:00:00Z&order=created_at.desc" \
  -H "apikey: $STATE_DB_SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $STATE_DB_SUPABASE_ANON_KEY"
```

**Select specific columns:**

```bash
curl -s "$STATE_DB_SUPABASE_URL/rest/v1/skill_state?skill_name=eq.dca&select=id,data,created_at" \
  -H "apikey: $STATE_DB_SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $STATE_DB_SUPABASE_ANON_KEY"
```

**Limit and pagination:**

```bash
curl -s "$STATE_DB_SUPABASE_URL/rest/v1/skill_state?skill_name=eq.food-tracking&order=created_at.desc&limit=10&offset=0" \
  -H "apikey: $STATE_DB_SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $STATE_DB_SUPABASE_ANON_KEY"
```

### UPDATE

Update by id:

```bash
curl -s -X PATCH "$STATE_DB_SUPABASE_URL/rest/v1/skill_state?id=eq.42" \
  -H "apikey: $STATE_DB_SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $STATE_DB_SUPABASE_ANON_KEY" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{
    "data": {"meal": "lunch", "items": ["rice", "chicken", "egg"], "phosphorus_mg": 350}
  }'
```

### DELETE

Delete by id:

```bash
curl -s -X DELETE "$STATE_DB_SUPABASE_URL/rest/v1/skill_state?id=eq.42" \
  -H "apikey: $STATE_DB_SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $STATE_DB_SUPABASE_ANON_KEY"
```

Delete by skill_name + key:

```bash
curl -s -X DELETE "$STATE_DB_SUPABASE_URL/rest/v1/skill_state?skill_name=eq.dca&key=eq.config" \
  -H "apikey: $STATE_DB_SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $STATE_DB_SUPABASE_ANON_KEY"
```

---

## JSONB Queries

Supabase uses PostgREST operators for JSONB filtering.

**Filter by top-level JSONB field:**

```bash
curl -s "$STATE_DB_SUPABASE_URL/rest/v1/skill_state?skill_name=eq.dca&data->>asset=eq.BTC&order=created_at.desc" \
  -H "apikey: $STATE_DB_SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $STATE_DB_SUPABASE_ANON_KEY"
```

**Filter by nested JSONB field:**

```bash
curl -s "$STATE_DB_SUPABASE_URL/rest/v1/skill_state?skill_name=eq.food-tracking&data->>meal=eq.lunch&order=created_at.desc" \
  -H "apikey: $STATE_DB_SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $STATE_DB_SUPABASE_ANON_KEY"
```

**Numeric comparison inside JSONB (cast to int):**

```bash
curl -s "$STATE_DB_SUPABASE_URL/rest/v1/skill_state?skill_name=eq.food-tracking&data->>phosphorus_mg=gt.200&order=created_at.desc" \
  -H "apikey: $STATE_DB_SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $STATE_DB_SUPABASE_ANON_KEY"
```

**Combine JSONB filter with date range:**

```bash
curl -s "$STATE_DB_SUPABASE_URL/rest/v1/skill_state?skill_name=eq.dca&data->>asset=eq.BTC&created_at=gte.2026-03-01T00:00:00Z&order=created_at.desc" \
  -H "apikey: $STATE_DB_SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $STATE_DB_SUPABASE_ANON_KEY"
```

---

## Integration Guide for Skills

This section is written for skills (and the agents executing them) that need persistent state. Read this section to understand how to design and use state-db from your skill.

### Step 1: Reference This Skill

Add this line at the top of your skill's SKILL.md where state management is needed:

```
For state management, read and follow the protocol in skills/state-db/SKILL.md
```

This tells the executing agent to read state-db's SKILL.md and use the curl patterns defined above.

### Step 2: Design Your State

Before writing any data, plan how your skill will organize its records using `skill_name` and `key`. Think of it like a two-level namespace:

- **`skill_name`** — your skill's unique identifier. One skill = one skill_name. This isolates your data from all other skills.
- **`key`** — sub-categories within your skill. Each key represents a different type of record your skill manages.
- **`data`** — the actual payload. Schemaless JSONB, so you define whatever fields make sense for each key.

Design your keys by listing out what types of data your skill needs to persist, then assign each type a key name.

### Step 3: Document Your State Schema

In your SKILL.md, document the keys and data shapes your skill uses. This serves as a contract so any agent executing your skill knows what to read and write.

Use this format:

```markdown
## State Schema (via state-db)

skill_name: `my-skill`

| key | purpose | data fields |
|-----|---------|-------------|
| entry | individual records | `{date, amount, category}` |
| config | user preferences | `{currency, timezone, default_category}` |
| summary | daily/monthly rollups | `{period, total, breakdown}` |
```

---

## State Design Patterns

### Pattern 1: Append-Only Log

For skills that record events over time (meals, transactions, logs). Each action creates a new row — never update, just insert.

```
skill_name: "food-tracking"
key: "entry"
```

```bash
# Log a meal
curl -s -X POST "$STATE_DB_SUPABASE_URL/rest/v1/skill_state" \
  -H "apikey: $STATE_DB_SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $STATE_DB_SUPABASE_ANON_KEY" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{
    "skill_name": "food-tracking",
    "key": "entry",
    "data": {"date": "2026-03-14", "meal": "lunch", "items": ["rice", "chicken"], "phosphorus_mg": 250, "potassium_mg": 400}
  }'

# Query today's entries
curl -s "$STATE_DB_SUPABASE_URL/rest/v1/skill_state?skill_name=eq.food-tracking&key=eq.entry&data->>date=eq.2026-03-14&order=created_at.asc" \
  -H "apikey: $STATE_DB_SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $STATE_DB_SUPABASE_ANON_KEY"
```

### Pattern 2: Singleton Config

For skills that store one config record per user. Use UPSERT-like behavior: query first, then INSERT or UPDATE.

```
skill_name: "my-skill"
key: "config"
```

```bash
# Check if config exists
EXISTING=$(curl -s "$STATE_DB_SUPABASE_URL/rest/v1/skill_state?skill_name=eq.my-skill&key=eq.config&limit=1" \
  -H "apikey: $STATE_DB_SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $STATE_DB_SUPABASE_ANON_KEY")

# If empty [], INSERT. If exists, UPDATE by id.
```

### Pattern 3: Keyed Entities

For skills that manage distinct entities (e.g. portfolio assets, project configs). Use `key` to distinguish entity type, and a field inside `data` as the logical identifier.

```
skill_name: "dca"
key: "portfolio"      -> each row = one asset
key: "transaction"    -> each row = one buy/sell event
key: "config"         -> single row for settings
```

```bash
# Add an asset to portfolio
curl -s -X POST "$STATE_DB_SUPABASE_URL/rest/v1/skill_state" \
  -H "apikey: $STATE_DB_SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $STATE_DB_SUPABASE_ANON_KEY" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{
    "skill_name": "dca",
    "key": "portfolio",
    "data": {"asset": "BTC", "total_invested": 50000, "total_units": 0.85}
  }'

# Find specific asset
curl -s "$STATE_DB_SUPABASE_URL/rest/v1/skill_state?skill_name=eq.dca&key=eq.portfolio&data->>asset=eq.BTC&limit=1" \
  -H "apikey: $STATE_DB_SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $STATE_DB_SUPABASE_ANON_KEY"

# List all transactions for BTC
curl -s "$STATE_DB_SUPABASE_URL/rest/v1/skill_state?skill_name=eq.dca&key=eq.transaction&data->>asset=eq.BTC&order=created_at.desc" \
  -H "apikey: $STATE_DB_SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $STATE_DB_SUPABASE_ANON_KEY"
```

### Pattern 4: Time-Series with Aggregation

For skills that need both raw data and periodic summaries. Use separate keys for raw entries and rollups.

```
skill_name: "expense-tracker"
key: "entry"          -> individual expenses
key: "daily-summary"  -> one row per day with totals
key: "monthly-summary" -> one row per month
```

```bash
# Insert daily summary (create or update for the day)
curl -s -X POST "$STATE_DB_SUPABASE_URL/rest/v1/skill_state" \
  -H "apikey: $STATE_DB_SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $STATE_DB_SUPABASE_ANON_KEY" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{
    "skill_name": "expense-tracker",
    "key": "daily-summary",
    "data": {"date": "2026-03-14", "total": 1250, "count": 5, "categories": {"food": 800, "transport": 450}}
  }'
```

---

## Key Design Guidelines

1. **One skill_name per skill** — never write to another skill's namespace.
2. **Use key to separate concerns** — think of keys as "tables" within your skill. If you find yourself filtering `data` fields to distinguish record types, that should be a separate key instead.
3. **Put dates inside `data`** — `created_at` is the DB insert time. If your skill cares about a logical date (e.g. "the date the user ate lunch"), store it as a field in `data` so you can filter with `data->>date=eq.2026-03-14`.
4. **Keep data flat when possible** — `{"asset": "BTC", "amount": 100}` is easier to query than `{"details": {"asset": "BTC", "amount": 100}}` because PostgREST JSONB filtering works best on top-level fields.
5. **Use `limit=1` for singleton reads** — when fetching config or the latest entry, always add `&limit=1` to avoid pulling unnecessary rows.
6. **Sort by `created_at.desc` for latest-first** — default ordering for most queries.

---

## Response Format

All Supabase REST responses return JSON arrays. A successful INSERT/UPDATE with `Prefer: return=representation` returns the created/updated rows. An empty result returns `[]`.

## Error Handling

Check HTTP status code. Non-2xx responses return:

```json
{"code": "PGRST...", "message": "...", "details": "...", "hint": "..."}
```

Parse with `jq` for scripting:

```bash
RESULT=$(curl -s -w "\n%{http_code}" -X POST "$STATE_DB_SUPABASE_URL/rest/v1/skill_state" \
  -H "apikey: $STATE_DB_SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $STATE_DB_SUPABASE_ANON_KEY" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{"skill_name": "test", "data": {}}')
HTTP_CODE=$(echo "$RESULT" | tail -1)
BODY=$(echo "$RESULT" | sed '$d')
```
