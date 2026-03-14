---
name: api-doc-gen
description: >
  Generate and validate API documentation from source code. Scans handler/router
  files to produce a standardized Markdown API doc (docs/api-doc.md) — or validates
  an existing doc against the current codebase. Use this skill whenever the user
  wants to generate API docs, update API documentation, check if API docs are
  out of date, create endpoint documentation from code, or says things like
  "gen api doc", "สร้าง api doc", "อัปเดต api doc", "เช็ค api doc ตรงกับ code ไหม",
  "document these endpoints", "api doc outdated". Also trigger when neo-team
  delegates API documentation tasks to this skill.
compatibility:
  environment: claude-code
  tools:
    - Read
    - Glob
    - Grep
    - Bash
    - Edit
    - Write
---

# API Doc Generator

Generate or validate API documentation by scanning source code. Currently optimized for Go (with Fiber, Echo, Chi, Gin support). The output follows a standardized Markdown template so all API docs look consistent across services.

## Modes

| Mode | When to use | What it does |
|------|-------------|--------------|
| **Generate** | No `docs/api-doc.md` exists, or user wants to regenerate from scratch | Scan code → produce full API doc |
| **Update** | `docs/api-doc.md` exists, code has changed | Scan code → diff against existing doc → update only changed parts |
| **Validate** | User wants to check consistency | Compare existing doc vs code → report discrepancies without modifying |

Detect the mode automatically:
1. If `docs/api-doc.md` doesn't exist → **Generate**
2. If user says "validate", "check", "เช็ค" → **Validate**
3. Otherwise → **Update**

The user can override by specifying the mode explicitly.

## Workflow

### Step 0: Read Project Context

Read `CLAUDE.md` (or `AGENTS.md`, `CONTRIBUTING.md`) to understand:
- Project name and purpose (for the doc header)
- Framework used (Fiber, Echo, Chi, Gin)
- Project structure conventions
- API versioning pattern (e.g., `/api/v1/`)

If no convention file exists, infer from the code structure.

### Step 1: Discover Routes

Scan the codebase for route registration patterns. Read [`references/go-scan-patterns.md`](references/go-scan-patterns.md) for framework-specific patterns.

**What to find:**
- All registered routes (method + path)
- The handler function each route maps to
- Route groups and prefixes
- Middleware applied (auth, validation)

**Where to look (in order):**
1. Router setup file — often `cmd/api/main.go`, `internal/router.go`, or `routes.go`
2. Route group files — `internal/<domain>/routes.go`
3. Handler files — `internal/<domain>/handler/*.go`

### Step 2: Extract Endpoint Details

For each discovered route, trace from handler → usecase → repository to extract:

1. **Request shape** — handler's request struct (path params, query params, request body)
2. **Response shape** — handler's response struct (success and error cases)
3. **Business rules** — validation in usecase layer, error conditions
4. **Error responses** — mapped HTTP status codes from error handling

**Where to find these:**
- Request/Response structs: `handler/request.go`, `handler/response.go`, or inline in handler files
- Domain entities: `entity.go` in the domain package
- Error mapping: handler's error-to-status-code logic
- Validation rules: request struct tags (`validate:"required"`), usecase validation

### Step 3: Generate or Validate

Read [`references/api-doc-template.md`](references/api-doc-template.md) for the exact output format.

#### Generate / Update Mode

Produce `docs/api-doc.md` following the template exactly:
- Document header with service name, version, base URL
- Table of contents with anchor links
- Each endpoint in template format (method, path, auth, params, request/response, errors)
- Common error responses section at the end

For **Update** mode: read the existing doc first, identify which endpoints changed or are new, and update only those sections. Preserve any manually-added notes or descriptions that aren't auto-generated.

#### Validate Mode

Compare existing `docs/api-doc.md` against discovered routes and produce a report:

```
## API Doc Validation Report

**Status:** [In Sync / Out of Sync]
**Checked:** [timestamp]

### Missing from Doc (endpoints in code but not documented)
- POST /api/v1/consents — handler: CreateConsent (internal/consent/handler/consent_handler.go:45)

### Missing from Code (documented but no matching route)
- DELETE /api/v1/consents/:id — documented but no route registration found

### Field Mismatches
- GET /api/v1/consents/:citizen_id
  - Response field `revoked_at` exists in code but not in doc
  - Doc shows `status` as String, code uses custom type `ConsentStatus`

### Summary
| Category | Count |
|----------|-------|
| Endpoints in code | X |
| Endpoints in doc | Y |
| Missing from doc | Z |
| Missing from code | W |
| Field mismatches | N |
```

### Step 4: Verify

After generating or updating:
1. Check that Table of Contents links match actual heading anchors
2. Verify all field tables use `M`/`O` for Mandatory column
3. Count endpoints in doc matches endpoints discovered in code
4. Report what was done

## Expanding to Other Languages

This skill currently focuses on Go. The scanning logic is in `references/go-scan-patterns.md`. To add a new language:
1. Create `references/<language>-scan-patterns.md` with framework-specific route/handler patterns
2. Update Step 0 to detect the language from project files (`go.mod` → Go, `package.json` → Node.js, etc.)
3. The template and output format remain the same regardless of language

## Output

After completion, report:

```
## API Doc Generator

**Mode:** [Generate / Update / Validate]
**File:** docs/api-doc.md
**Endpoints:** [N endpoints documented]

**Changes:**
- [list of endpoints added/updated/removed]

**Warnings:** [any issues found — missing structs, unresolvable types, etc.]
```
