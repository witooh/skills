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
  version: "2.0"
---

# State DB

Centralized state management for Claude Code skills via Supabase REST API.

## Setup

All operations use these shell variables. Define them before executing any command:

```bash
SB_URL="$STATE_DB_SUPABASE_URL/rest/v1/skill_state"
SB_AUTH=(-H "apikey: $STATE_DB_SUPABASE_ANON_KEY" -H "Authorization: Bearer $STATE_DB_SUPABASE_ANON_KEY")
SB_JSON=(-H "Content-Type: application/json")
SB_RETURN=(-H "Prefer: return=representation")
```

## Table Schema

Table: `skill_state`

| Column | Type | Note |
|--------|------|------|
| id | BIGSERIAL | PRIMARY KEY |
| skill_name | TEXT | e.g. 'food-tracker', 'dca' |
| key1 | TEXT | primary sub-key, e.g. 'entry', 'config' |
| key2 | TEXT | nullable, second-level key |
| key3 | TEXT | nullable, third-level key |
| key4 | TEXT | nullable, fourth-level key |
| key5 | TEXT | nullable, fifth-level key |
| data | JSONB | schemaless payload |
| created_at | TIMESTAMPTZ | DEFAULT NOW() |
| updated_at | TIMESTAMPTZ | DEFAULT NOW(), auto-updated via trigger |

Index: `idx_skill_state_keys` on `(skill_name, key1, key2, key3, key4, key5)`. PostgreSQL leftmost prefix matching means queries on `(skill_name)`, `(skill_name, key1)`, `(skill_name, key1, key2)`, etc. all use this single index efficiently.

---

## Operations

### INSERT

```bash
curl -s -X POST "$SB_URL" "${SB_AUTH[@]}" "${SB_JSON[@]}" "${SB_RETURN[@]}" \
  -d '{
    "skill_name": "food-tracker",
    "key1": "entry",
    "data": {"meal": "lunch", "items": ["rice", "chicken"], "phosphorus_mg": 250}
  }'
```

Multi-key insert:

```bash
curl -s -X POST "$SB_URL" "${SB_AUTH[@]}" "${SB_JSON[@]}" "${SB_RETURN[@]}" \
  -d '{
    "skill_name": "expense-tracker",
    "key1": "entry",
    "key2": "food",
    "key3": "2026-03",
    "data": {"amount": 250, "description": "lunch"}
  }'
```

### QUERY

Base form: `curl -s "$SB_URL?<filters>" "${SB_AUTH[@]}"`

**Common filter patterns:**

| Filter | Query string example |
|--------|---------------------|
| By skill_name | `?skill_name=eq.food-tracker&order=created_at.desc` |
| By skill_name + key1 | `?skill_name=eq.food-tracker&key1=eq.entry&order=created_at.desc` |
| By skill_name + key1 + key2 | `?skill_name=eq.expense-tracker&key1=eq.entry&key2=eq.food` |
| By 3 keys | `?skill_name=eq.project&key1=eq.task&key2=eq.backend&key3=eq.sprint-12` |
| Null key check | `?skill_name=eq.my-skill&key2=is.null` |
| Date range | `?skill_name=eq.food-tracker&created_at=gte.2026-03-01T00:00:00Z&created_at=lt.2026-03-15T00:00:00Z` |
| Select columns | `?skill_name=eq.dca&select=id,data,created_at` |
| Pagination | `?skill_name=eq.food-tracker&order=created_at.desc&limit=10&offset=0` |

Example:

```bash
curl -s "$SB_URL?skill_name=eq.food-tracker&key1=eq.entry&order=created_at.desc&limit=10" \
  "${SB_AUTH[@]}"
```

### JSONB Filters

Supabase uses PostgREST `data->>field` syntax for JSONB filtering. Append these to query strings:

| Filter type | Query string example |
|-------------|---------------------|
| Top-level field | `&data->>asset=eq.BTC` |
| String match | `&data->>meal=eq.lunch` |
| Numeric comparison | `&data->>phosphorus_mg=gt.200` |
| Combined with date | `&data->>asset=eq.BTC&created_at=gte.2026-03-01T00:00:00Z` |

Example:

```bash
curl -s "$SB_URL?skill_name=eq.dca&data->>asset=eq.BTC&order=created_at.desc" \
  "${SB_AUTH[@]}"
```

### UPDATE

```bash
curl -s -X PATCH "$SB_URL?id=eq.42" "${SB_AUTH[@]}" "${SB_JSON[@]}" "${SB_RETURN[@]}" \
  -d '{
    "data": {"meal": "lunch", "items": ["rice", "chicken", "egg"], "phosphorus_mg": 350}
  }'
```

### DELETE

```bash
curl -s -X DELETE "$SB_URL?id=eq.42" "${SB_AUTH[@]}" "${SB_RETURN[@]}"
```

Delete by skill_name + key1:

```bash
curl -s -X DELETE "$SB_URL?skill_name=eq.dca&key1=eq.config" "${SB_AUTH[@]}" "${SB_RETURN[@]}"
```

Delete by multi-key:

```bash
curl -s -X DELETE "$SB_URL?skill_name=eq.expense-tracker&key1=eq.entry&key2=eq.food&key3=eq.2026-03" \
  "${SB_AUTH[@]}" "${SB_RETURN[@]}"
```

---

## Key Design Guidelines

1. **One skill_name per skill** — never write to another skill's namespace.
2. **Use key1 as the record type** — equivalent to a "table name" within your skill (e.g. `entry`, `config`, `portfolio`).
3. **Use key2-key5 for natural hierarchy** — if your data has inherent groupings (category, date-period, entity-id), promote them to key columns rather than filtering on JSONB fields. This makes queries faster and more readable.
4. **Leave unused keys as null** — most skills will only need key1 or key1+key2. Do not fill keys just to fill them.
5. **Put dates inside `data`** — `created_at` is the DB insert time. If your skill cares about a logical date (e.g. "the date the user ate lunch"), store it as a field in `data` so you can filter with `data->>date=eq.2026-03-14`.
6. **Keep data flat when possible** — `{"asset": "BTC", "amount": 100}` is easier to query than `{"details": {"asset": "BTC", "amount": 100}}` because PostgREST JSONB filtering works best on top-level fields.
7. **Use `limit=1` for singleton reads** — when fetching config or the latest entry, always add `&limit=1` to avoid pulling unnecessary rows.
8. **Sort by `created_at.desc` for latest-first** — default ordering for most queries.

---

## Integration Guide for Skills

This section is written for skills (and the agents executing them) that need persistent state.

### Step 1: Reference This Skill

Add this line at the top of your skill's SKILL.md where state management is needed:

```
For state management, read and follow the protocol in skills/state-db/SKILL.md
```

### Step 2: Design Your State

Plan how your skill organizes records using `skill_name` and `key1`-`key5` — a six-level namespace:

- **`skill_name`** — your skill's unique identifier. One skill = one skill_name.
- **`key1`** (required by convention) — record type / "table" within your skill (e.g. `entry`, `config`, `portfolio`).
- **`key2`-`key5`** (optional) — additional hierarchy levels. Each skill decides what these mean.
- **`data`** — the actual payload. Schemaless JSONB.

### Step 3: Document Your State Schema

In your SKILL.md, document the keys and data shapes your skill uses:

```markdown
## State Schema (via state-db)

skill_name: `my-skill`

| key1 | key2 | key3 | purpose | data fields |
|------|------|------|---------|-------------|
| entry | (null) | (null) | individual records | `{date, amount, category}` |
| entry | food | (null) | food-specific records | `{date, amount, item}` |
| config | (null) | (null) | user preferences | `{currency, timezone}` |
| summary | 2026-03 | (null) | monthly rollup | `{total, breakdown}` |
```

### Key Naming Conventions

Each skill documents what key1-key5 means in its own SKILL.md. Common patterns:

| Level | Common usage |
|-------|-------------|
| key1 | Record type: `entry`, `config`, `summary`, `portfolio`, `transaction` |
| key2 | Category or entity: `food`, `transport`, `BTC`, `daily`, `monthly` |
| key3 | Time period or sub-category: `2026-03`, `sprint-12` |
| key4-key5 | Rarely needed. Reserved for deeply hierarchical data. |

Rule of thumb: if you're putting a value in `data` purely to filter on it, consider promoting it to a key column instead.

---

## State Design Patterns

### Pattern 1: Append-Only Log

For skills that record events over time (meals, transactions, logs). Each action creates a new row — never update, just insert.

```
skill_name: "food-tracker"
key1: "entry"
```

```bash
# Log a meal
curl -s -X POST "$SB_URL" "${SB_AUTH[@]}" "${SB_JSON[@]}" "${SB_RETURN[@]}" \
  -d '{
    "skill_name": "food-tracker",
    "key1": "entry",
    "data": {"date": "2026-03-14", "meal": "lunch", "items": ["rice", "chicken"], "phosphorus_mg": 250, "potassium_mg": 400}
  }'

# Query today's entries
curl -s "$SB_URL?skill_name=eq.food-tracker&key1=eq.entry&data->>date=eq.2026-03-14&order=created_at.asc" \
  "${SB_AUTH[@]}"
```

### Pattern 2: Singleton Config

For skills that store one config record. Query first, then INSERT or UPDATE by id. Safe for single-agent use.

```
skill_name: "my-skill"
key1: "config"
```

```bash
# Read existing config
EXISTING=$(curl -s "$SB_URL?skill_name=eq.my-skill&key1=eq.config&limit=1" "${SB_AUTH[@]}")

# If empty [] -> INSERT new config
curl -s -X POST "$SB_URL" "${SB_AUTH[@]}" "${SB_JSON[@]}" "${SB_RETURN[@]}" \
  -d '{
    "skill_name": "my-skill",
    "key1": "config",
    "data": {"currency": "THB", "timezone": "Asia/Bangkok"}
  }'

# If exists -> UPDATE by id (extract id from EXISTING with jq)
ID=$(echo "$EXISTING" | jq -r '.[0].id')
curl -s -X PATCH "$SB_URL?id=eq.$ID" "${SB_AUTH[@]}" "${SB_JSON[@]}" "${SB_RETURN[@]}" \
  -d '{"data": {"currency": "USD", "timezone": "Asia/Bangkok"}}'
```

### Pattern 3: Keyed Entities

For skills that manage distinct entities. Use `key1` for entity type and `key2` for specific entity — avoids JSONB filtering for the most common queries.

```
skill_name: "dca"
key1: "portfolio"   key2: (null)    -> each row = one asset
key1: "transaction" key2: "BTC"     -> buy/sell events for BTC
key1: "transaction" key2: "ETH"     -> buy/sell events for ETH
key1: "config"      key2: (null)    -> single row for settings
```

```bash
# Add an asset to portfolio
curl -s -X POST "$SB_URL" "${SB_AUTH[@]}" "${SB_JSON[@]}" "${SB_RETURN[@]}" \
  -d '{
    "skill_name": "dca",
    "key1": "portfolio",
    "data": {"asset": "BTC", "total_invested": 50000, "total_units": 0.85}
  }'

# Find specific asset
curl -s "$SB_URL?skill_name=eq.dca&key1=eq.portfolio&data->>asset=eq.BTC&limit=1" \
  "${SB_AUTH[@]}"

# List all BTC transactions (key2 filters by asset — uses index, no JSONB scan)
curl -s "$SB_URL?skill_name=eq.dca&key1=eq.transaction&key2=eq.BTC&order=created_at.desc" \
  "${SB_AUTH[@]}"
```

### Pattern 4: Time-Series with Aggregation

For skills that need both raw data and periodic summaries. Use `key1` for record type, `key2` for aggregation level, and optionally `key3` for specific period.

```
skill_name: "expense-tracker"
key1: "entry"    key2: (null)      -> individual expenses
key1: "summary"  key2: "daily"     -> one row per day with totals
key1: "summary"  key2: "monthly"   -> one row per month
key1: "summary"  key2: "monthly"   key3: "2026-03" -> specific month
```

```bash
# Insert daily summary
curl -s -X POST "$SB_URL" "${SB_AUTH[@]}" "${SB_JSON[@]}" "${SB_RETURN[@]}" \
  -d '{
    "skill_name": "expense-tracker",
    "key1": "summary",
    "key2": "daily",
    "data": {"date": "2026-03-14", "total": 1250, "count": 5, "categories": {"food": 800, "transport": 450}}
  }'

# Query all monthly summaries
curl -s "$SB_URL?skill_name=eq.expense-tracker&key1=eq.summary&key2=eq.monthly&order=created_at.desc" \
  "${SB_AUTH[@]}"

# Query specific month summary
curl -s "$SB_URL?skill_name=eq.expense-tracker&key1=eq.summary&key2=eq.monthly&key3=eq.2026-03&limit=1" \
  "${SB_AUTH[@]}"
```

---

## Response Format & Error Handling

All Supabase REST responses return JSON arrays. A successful INSERT/UPDATE with `Prefer: return=representation` returns the created/updated rows. An empty result returns `[]`.

Non-2xx responses return:

```json
{"code": "PGRST...", "message": "...", "details": "...", "hint": "..."}
```

Error-checked curl pattern:

```bash
RESULT=$(curl -s -w "\n%{http_code}" -X POST "$SB_URL" "${SB_AUTH[@]}" "${SB_JSON[@]}" "${SB_RETURN[@]}" \
  -d '{"skill_name": "test", "data": {}}')
HTTP_CODE=$(echo "$RESULT" | tail -1)
BODY=$(echo "$RESULT" | sed '$d')
```

---

## Migration from v1 (key) to v2 (key1-key5)

The `key` column was renamed to `key1` in v2. If your skill referenced `key` in queries:

- Change all `key=eq.xxx` to `key1=eq.xxx` in PostgREST queries
- Change all `"key": "xxx"` to `"key1": "xxx"` in INSERT/PATCH payloads
- No data migration needed — existing rows retain their values in the renamed column

SQL applied to Supabase:

```sql
ALTER TABLE skill_state RENAME COLUMN key TO key1;
ALTER TABLE skill_state ADD COLUMN key2 TEXT;
ALTER TABLE skill_state ADD COLUMN key3 TEXT;
ALTER TABLE skill_state ADD COLUMN key4 TEXT;
ALTER TABLE skill_state ADD COLUMN key5 TEXT;
CREATE INDEX idx_skill_state_keys
  ON skill_state (skill_name, key1, key2, key3, key4, key5);
```
