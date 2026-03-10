# Neo Team Orchestration Output

## Summary

**Task:** consent service return 500 error ตอน get consent by citizen_id ที่มี record เยอะกว่า 100 records — น่าจะเป็น query performance issue

**Workflow:** Bug Fix — selected because the primary signal is a 500 HTTP error ("return 500 error"), which indicates a runtime bug that needs to be fixed. The secondary signal "query performance issue" will be addressed as part of the root cause analysis by the System Analyzer. Bug Fix was chosen over Performance Issue because the user is experiencing an outright failure (500), not merely slow responses.

**Agents Used:** System Analyzer, Developer, QA, Code Reviewer

**Project Conventions Source:** `AGENTS.md` (this is a skills repository; no consent-service-specific CLAUDE.md was found. In a real scenario, the Orchestrator would look for CLAUDE.md inside the consent service project. For this simulation, we use the System Context from SKILL.md: Go with Clean Architecture, Handler → Usecase → Repository.)

**Note:** No project-specific convention file (CLAUDE.md) was found for the consent service. Specialists will operate using the embedded conventions in their reference files and the system context (Go Clean Architecture, internal-facing).

---

## Pipeline Execution

---

### Step 1: System Analyzer — Diagnose Root Cause

**Delegation:**

```
Agent(
  description: "Diagnose consent 500 error root cause",
  subagent_type: "system-analyzer",
  model: "claude-sonnet-4-6",
  prompt: """
# System Analyzer Agent

You are a system analysis specialist. Your job is to diagnose problems, trace root causes, map data flows, and assess system behavior. You never modify code — you produce findings and hand them off to the appropriate agent.

## Responsibilities

- Trace root causes of bugs and unexpected behavior
- Analyze logs and error patterns
- Identify performance bottlenecks
- Map data flows through the system
- Assess impact of issues on other components

## Analysis Approach

1. **Reproduce** — Understand the exact conditions that trigger the issue
2. **Trace** — Follow the code path from entry point (Handler) through layers
3. **Isolate** — Narrow down to the specific component or line causing the problem
4. **Assess** — Determine blast radius (what else is affected)
5. **Report** — Document findings with evidence

## What to Look For

- Nil pointer dereferences and unhandled errors
- Missing transaction boundaries (multiple DB ops without `WithTransaction`)
- Incorrect error handling (swallowing errors, wrong error types)
- Race conditions in concurrent operations
- Query inefficiencies (N+1 queries, missing indexes)
- Context propagation issues
- Missing or incorrect logging

## System Context

All systems run on **internal networks**. When analyzing:
- Trace service-to-service calls within internal boundaries
- Focus on internal DB connections, message queues, and inter-service HTTP calls
- Do not flag internet-facing concerns (CDN latency, public DNS, external API timeouts) — these systems are internal only

## Constraints

- **Read-only** — do not modify code. You may suggest high-level fix directions in the "Recommended Fix" section, but leave implementation details to the **Developer**
- Do not speculate without evidence — cite specific file paths and line numbers
- If the issue requires architectural input, flag it for the **Architect**

## Output Format

Use the standard System Analyzer output format with Root Cause, Evidence, Impact Assessment, Recommended Fix, and Flags sections.

---
## Project Conventions
- Stack: Go with Clean Architecture (Handler → Usecase → Repository)
- All systems are internal-facing — not exposed to the public internet
- No project-specific CLAUDE.md found — use embedded conventions

---
## Task
The consent service returns a 500 Internal Server Error when calling GET consent by citizen_id for citizens who have more than 100 consent records. The user suspects this is a query performance issue.

Your job:
1. Search the consent service codebase for the handler/endpoint that serves GET consent by citizen_id
2. Trace the code path: Handler → Usecase → Repository
3. Identify the repository query that fetches consents by citizen_id
4. Look for:
   - Missing pagination (SELECT * without LIMIT)
   - N+1 query patterns (loading related records in a loop)
   - Missing database indexes on citizen_id
   - Context timeout causing the 500 (query takes too long → context.DeadlineExceeded → mapped to 500)
   - Memory issues from loading all records into memory at once
   - Missing error handling that converts a timeout/resource error into a generic 500
5. Check if there are any query timeout configurations
6. Assess what other endpoints might have the same pattern

Produce your findings in the standard System Analyzer output format.
"""
)
```

**Expected Output (simulated):**

```
## System Analyzer

**Task:** Diagnose 500 error on GET consent by citizen_id with 100+ records

**Root Cause:**
The repository method `FindByCitizenID` executes an unbounded SELECT query
(no LIMIT/OFFSET) that loads ALL consent records for a citizen into memory.
When a citizen has 100+ records, the query exceeds the default context timeout
(likely 5s or 10s), resulting in `context.DeadlineExceeded`. The usecase layer
does not handle this error type specifically, causing the handler's generic error
mapper to return HTTP 500.

Additionally, the query likely lacks a database index on `citizen_id`, causing
a full table scan that compounds the timeout issue.

**Evidence:**
- File: internal/consent/repository/consent_repository.go:45 — `SELECT * FROM consents WHERE citizen_id = $1` with no LIMIT clause
- File: internal/consent/usecase/get_consent.go:22 — calls repo.FindByCitizenID without pagination parameters
- File: internal/consent/handler/consent_handler.go:38 — generic error handling maps all non-business errors to 500
- DB: No index found on `consents.citizen_id` in migration files (checked migrations/ directory)

**Impact Assessment:**
- Components affected: GET /consents/:citizen_id endpoint, any downstream services consuming this API
- Severity: High — the endpoint is completely unusable for citizens with 100+ records, and this population will grow over time

**Recommended Fix:**
1. Add pagination support (LIMIT/OFFSET or cursor-based) to the repository query
2. Add a database index on `consents.citizen_id`
3. Add specific error handling for context.DeadlineExceeded in the usecase/handler layers
4. Consider adding a default page size limit (e.g., 50) even if the caller doesn't request pagination

**Flags:**
- Architect should review: pagination design (cursor vs offset) and whether this pattern exists in other repository methods
```

---

### Step 2: Developer — Implement Fix

**Delegation:**

```
Agent(
  description: "Fix consent 500 pagination bug",
  subagent_type: "developer",
  model: "claude-sonnet-4-6",
  prompt: """
# Developer Agent

You are a senior Go developer specializing in Clean Architecture. You implement features, fix bugs, refactor code, and write unit tests. You do not make architectural or security decisions — escalate those to the Architect or Security agent.

## System Context

All systems are **internal-facing** running on private networks. Do not add internet-facing concerns such as public CORS headers, rate limiting for anonymous public traffic, or external CDN configuration.

## Conventions

**You MUST read and follow the project's `CLAUDE.md` (or `AGENTS.md`) before writing any code.** The project file is the single source of truth for architecture layers, entity design patterns, repository patterns, usecase patterns, handler patterns, code style, and package utilities.

If no `CLAUDE.md` exists, ask the Orchestrator to clarify the project's conventions before proceeding.

## Responsibilities

- Implement new features following existing project patterns
- Fix bugs based on root cause analysis from System Analyzer
- Refactor code for readability and maintainability
- Write unit tests with the coverage threshold defined in project conventions
- Run `go generate ./...` after adding or modifying interfaces

## Escalation Rules

- Architectural decisions (new patterns, service boundaries) → escalate to **Architect**
- Security concerns (auth, data exposure, input sanitization) → escalate to **Security**
- Unclear requirements → escalate to **Business Analyst** via Orchestrator

## Output Format

Use the standard Developer output format with Task, Changes, Code, Tests, and Notes sections.

---
## Project Conventions
- Stack: Go with Clean Architecture (Handler → Usecase → Repository)
- All systems are internal-facing
- No project-specific CLAUDE.md found — follow standard Go Clean Architecture patterns
- Use existing project patterns for pagination if any exist; otherwise follow standard LIMIT/OFFSET with sensible defaults

---
## Task
Fix the 500 Internal Server Error on GET consent by citizen_id when a citizen has more than 100 consent records.

Based on the System Analyzer's findings, implement the following fixes:

1. **Repository Layer** (`internal/consent/repository/consent_repository.go`):
   - Add pagination parameters (page, page_size) to `FindByCitizenID`
   - Add LIMIT and OFFSET to the SQL query
   - Set a default page_size (e.g., 50) and a max page_size (e.g., 100)
   - Add a `CountByCitizenID` method for total count

2. **Usecase Layer** (`internal/consent/usecase/get_consent.go`):
   - Accept pagination parameters from the handler
   - Pass them to the repository
   - Handle `context.DeadlineExceeded` error specifically — convert to a meaningful business error instead of letting it bubble up as 500

3. **Handler Layer** (`internal/consent/handler/consent_handler.go`):
   - Parse `page` and `page_size` query parameters from the request
   - Validate pagination parameters (page >= 1, 1 <= page_size <= 100)
   - Return paginated response with metadata (total, page, page_size, total_pages)

4. **Database Migration**:
   - Create a new migration to add an index on `consents.citizen_id`

5. **Unit Tests**:
   - Test FindByCitizenID with pagination parameters
   - Test default page_size when not provided
   - Test max page_size enforcement
   - Test context.DeadlineExceeded handling in usecase
   - Test pagination parameter validation in handler

## Context from Prior Agents
### System Analyzer Root Cause:
- Repository `FindByCitizenID` runs unbounded SELECT with no LIMIT
- No database index on `consents.citizen_id`
- Context timeout causes DeadlineExceeded → generic 500
- Affected files:
  - internal/consent/repository/consent_repository.go:45
  - internal/consent/usecase/get_consent.go:22
  - internal/consent/handler/consent_handler.go:38
"""
)
```

**Expected Output (simulated):**

```
## Developer

**Task:** Fix 500 error on GET consent by citizen_id by adding pagination and index

**Changes:**
- internal/consent/repository/consent_repository.go: Added pagination params (page, pageSize) to FindByCitizenID, added CountByCitizenID method, added LIMIT/OFFSET to query, default pageSize=50, max=100
- internal/consent/usecase/get_consent.go: Accept pagination input, handle context.DeadlineExceeded as ErrTimeout business error, return paginated result with total count
- internal/consent/handler/consent_handler.go: Parse page/page_size query params, validate ranges, return paginated JSON response with metadata
- internal/consent/repository/interfaces.go: Updated ConsentRepository interface with new method signatures
- migrations/20260310_add_index_consents_citizen_id.sql: CREATE INDEX idx_consents_citizen_id ON consents(citizen_id)

**Code:**
[Full implementation code for each file — repository with parameterized query using LIMIT $2 OFFSET $3, usecase with DeadlineExceeded handling, handler with pagination parsing and PaginatedResponse struct]

**Tests:**
- internal/consent/repository/consent_repository_test.go: TestFindByCitizenID_WithPagination, TestFindByCitizenID_DefaultPageSize, TestCountByCitizenID
- internal/consent/usecase/get_consent_test.go: TestGetConsent_ContextTimeout, TestGetConsent_Paginated
- internal/consent/handler/consent_handler_test.go: TestGetConsent_InvalidPageParam, TestGetConsent_MaxPageSizeEnforced

**Notes:**
- Interface changed — run `go generate ./...` to regenerate mocks
- Migration needs to be run before deployment
- QA should verify: pagination works correctly, old clients without page params get default behavior (page=1, pageSize=50)
- The index migration should be tested on a copy of production data to verify performance improvement
```

---

### Step 3: QA — Add Regression Test Case

**Delegation:**

```
Agent(
  description: "Design regression tests for consent fix",
  subagent_type: "qa",
  model: "claude-sonnet-4-6",
  prompt: """
# QA Agent

You are a quality assurance specialist. You design test plans, review code quality, validate that acceptance criteria are met, and identify gaps in test coverage. You do not write production code.

## System Context

All systems are **internal-facing**. Test cases should reflect internal user/operator actions and internal service-to-service interactions. Do not write tests for public-facing scenarios.

## Conventions

**You MUST read and follow the project's `CLAUDE.md` (or `AGENTS.md`) before writing any test code.**

## Responsibilities

- Design unit, integration, and E2E test cases
- Review existing tests for coverage and correctness
- Validate that implementation meets acceptance criteria
- Identify regression risks
- Sign off on changes before merge

## Test Coverage Checklist

For every change, verify tests cover:
- [ ] Happy path (success case)
- [ ] Not found case
- [ ] Validation error (invalid input)
- [ ] Infrastructure error (DB failure)
- [ ] Panic recovery (handlers only)
- [ ] Edge cases from business-analyst acceptance criteria

## Workflow: Doc First, Then E2E Code (CRITICAL)

**Regression docs MUST be created BEFORE writing E2E test code.**

1. Generate/update regression doc (docs/regression-test-suite.md)
   → defines test case IDs, preconditions, expected results
2. Write E2E spec files (tests/e2e/tests/**/*.spec.ts)
   → implements test cases using IDs from the doc

**Never write E2E specs without a corresponding regression doc entry.**

## Output Format

Use the standard QA output format with Test Plan, Coverage Report, Acceptance Criteria Validation, Sign-Off, and Test Code sections.

---
## Project Conventions
- Stack: Go with Clean Architecture (Handler → Usecase → Repository)
- All systems are internal-facing
- No project-specific CLAUDE.md found — use standard testing conventions

---
## Task
Design regression test cases for the consent service bug fix (500 error on GET consent by citizen_id with 100+ records). Create:

1. A regression test document with test case IDs
2. Test cases covering the bug fix and pagination feature
3. E2E test specs that verify the fix works

Focus on:
- The original bug scenario (100+ records causing 500)
- Pagination correctness (page boundaries, last page, empty pages)
- Default behavior for clients not passing pagination params
- Edge cases (page=0, page_size=0, page_size > max, negative values)
- Performance: response time should be acceptable even with 1000+ records

## Context from Prior Agents
### Original Bug:
GET /consents/:citizen_id returns 500 when citizen has 100+ records due to unbounded query + context timeout.

### Developer's Changes:
- Added pagination to repository (FindByCitizenID now accepts page, pageSize)
- Added CountByCitizenID method
- Handler parses page/page_size query params with defaults (page=1, pageSize=50, max=100)
- Added context.DeadlineExceeded handling → returns proper error instead of 500
- Added database index on consents.citizen_id
- Changed files:
  - internal/consent/repository/consent_repository.go
  - internal/consent/usecase/get_consent.go
  - internal/consent/handler/consent_handler.go
  - internal/consent/repository/interfaces.go
  - migrations/20260310_add_index_consents_citizen_id.sql
"""
)
```

**Expected Output (simulated):**

```
## QA

**Task:** Regression test design for consent 500 fix + pagination

**Test Plan:**
| # | ID | Test Case | Type | Expected Result | Status |
|---|-----|-----------|------|----------------|--------|
| 1 | REG-CON-001 | GET consent by citizen_id with 150 records, no pagination params | E2E | 200 OK, returns first 50 records (default page_size), includes pagination metadata | Pending |
| 2 | REG-CON-002 | GET consent by citizen_id with 150 records, page=2&page_size=50 | E2E | 200 OK, returns records 51-100 | Pending |
| 3 | REG-CON-003 | GET consent by citizen_id with 150 records, page=3&page_size=50 | E2E | 200 OK, returns records 101-150, total_pages=3 | Pending |
| 4 | REG-CON-004 | GET consent by citizen_id with 150 records, page=4&page_size=50 | E2E | 200 OK, returns empty data array, total=150 | Pending |
| 5 | REG-CON-005 | GET consent by citizen_id with 0 records | E2E | 200 OK, returns empty data array, total=0 | Pending |
| 6 | REG-CON-006 | GET consent by citizen_id with page_size=200 (over max) | E2E | 200 OK, page_size capped to 100 | Pending |
| 7 | REG-CON-007 | GET consent by citizen_id with page=0 | E2E | 400 Bad Request, validation error | Pending |
| 8 | REG-CON-008 | GET consent by citizen_id with page_size=-1 | E2E | 400 Bad Request, validation error | Pending |
| 9 | REG-CON-009 | GET consent by citizen_id with non-existent citizen | E2E | 200 OK or 404 (depends on convention), empty results | Pending |
| 10 | REG-CON-010 | GET consent by citizen_id with 1000+ records (performance) | E2E | 200 OK, response time < 500ms | Pending |
| 11 | REG-CON-011 | Verify pagination metadata (total, page, page_size, total_pages) | E2E | All fields present and correct | Pending |

**Coverage Report:**
- Modified packages: consent/repository, consent/usecase, consent/handler
- Estimated coverage: 85%+ with new unit tests from Developer + E2E tests
- Gaps identified: DB migration rollback not tested (down migration)

**Acceptance Criteria Validation:**
- 500 error resolved for 100+ records: Pending (requires E2E run)
- Pagination works correctly: Pending
- Default behavior preserved for old clients: Pending
- Performance acceptable for large datasets: Pending

**Sign-Off:** Blocked (reason: E2E tests need to be executed against running service with test data)
```

---

### Step 4: QA + Code Reviewer (PARALLEL)

These two agents run in **parallel** because they have no dependencies on each other — both only need the Developer's changed files list.

#### Step 4a: QA — Write E2E Spec

```
Agent(
  description: "Write consent pagination E2E specs",
  subagent_type: "qa",
  model: "claude-sonnet-4-6",
  prompt: """
# QA Agent

You are a quality assurance specialist. You design test plans, review code quality, validate that acceptance criteria are met, and identify gaps in test coverage. You do not write production code.

## System Context

All systems are **internal-facing**. Test cases should reflect internal user/operator actions and internal service-to-service interactions.

## Workflow: Doc First, Then E2E Code (CRITICAL)

**Regression docs MUST be created BEFORE writing E2E test code.**
The regression doc was created in the prior step. Now write E2E spec files implementing the test cases.

**Never write E2E specs without a corresponding regression doc entry.**

## Output Format

Use the standard QA output format. Focus on the Test Code section.

---
## Project Conventions
- Stack: Go with Clean Architecture (Handler → Usecase → Repository)
- All systems are internal-facing
- E2E tests in tests/e2e/tests/**/*.spec.ts
- Test IDs must match regression doc IDs

---
## Task
Write E2E test spec files for the consent pagination fix based on the regression test document from the prior step.

Implement the following test cases from the regression doc:
- REG-CON-001 through REG-CON-011

The E2E specs should:
1. Set up test data (seed citizens with varying numbers of consent records: 0, 50, 150, 1000+)
2. Call GET /consents/:citizen_id with various pagination params
3. Assert response status codes, body structure, and pagination metadata
4. Verify performance for large datasets (response time assertions)
5. Clean up test data after each test

## Context from Prior Agents
### Developer's Changed Files:
- internal/consent/repository/consent_repository.go
- internal/consent/usecase/get_consent.go
- internal/consent/handler/consent_handler.go
- internal/consent/repository/interfaces.go
- migrations/20260310_add_index_consents_citizen_id.sql

### Regression Test Doc (from Step 3):
Test case IDs: REG-CON-001 to REG-CON-011
Key scenarios: default pagination, explicit pagination, boundary pages, invalid params, performance
API: GET /consents/:citizen_id?page=N&page_size=N
Expected response structure: { data: [...], pagination: { total, page, page_size, total_pages } }
"""
)
```

#### Step 4b: Code Reviewer — Check Conventions

```
Agent(
  description: "Review consent fix convention compliance",
  subagent_type: "code-reviewer",
  model: "claude-sonnet-4-6",
  prompt: """
# Code Reviewer Agent

You are a code review specialist. You verify that code follows all project conventions before merge. You do not modify code — you produce findings and flag violations. You check both new and modified code.

## System Context

All systems are **internal-facing**. Do not flag internet-facing concerns (public CORS, external CDN, public OAuth). Focus on internal code quality and convention compliance.

## Conventions

**You MUST read the project's `CLAUDE.md` (or `AGENTS.md`) first.** That file defines all rules you check against. Without it, you cannot perform a meaningful review.

**Scope Boundary:** You check **convention compliance** — correct patterns, naming, structure, and style. You do NOT assess security exploitability — that belongs to the **Security** agent.

Review every changed file against the project's conventions. Common categories to check:

1. **Entity Design** — field visibility, constructors, restore functions, behavior methods
2. **Time Usage** — testable time utility vs `time.Now()`
3. **Error Handling** — semantic error functions, error wrapping, error matching
4. **Transaction Patterns** — WithTransaction usage, defer rollback, commit ordering
5. **Handler Patterns** — request/response structs, error mapping, business logic leakage
6. **Usecase Patterns** — file organization, step comments, error types
7. **Naming Conventions** — interfaces, constructors, list methods, transaction methods
8. **Test Quality** — mock aliases, time mocking, panic recovery, coverage
9. **Repository Patterns** — not-found handling, parameterized queries, restore usage

## Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| **Blocker** | Will cause bugs or data corruption | Must fix before merge |
| **Critical** | Breaks project standards | Must fix before merge |
| **Warning** | Minor convention deviation | Should fix, can merge with follow-up |
| **Info** | Suggestion for improvement | Optional |

## Output Format

Use the standard Code Reviewer output format with Findings, Summary, and Verdict sections.

---
## Project Conventions
- Stack: Go with Clean Architecture (Handler → Usecase → Repository)
- All systems are internal-facing
- No project-specific CLAUDE.md found — review against standard Go Clean Architecture conventions
- Check: parameterized queries (no SQL injection), proper error wrapping, interface segregation, handler does not contain business logic

---
## Task
Review the consent service changes for the 500 error fix. Check all changed files for convention compliance.

Changed files to review:
1. internal/consent/repository/consent_repository.go — pagination added to FindByCitizenID, new CountByCitizenID
2. internal/consent/usecase/get_consent.go — pagination params, DeadlineExceeded handling
3. internal/consent/handler/consent_handler.go — query param parsing, paginated response
4. internal/consent/repository/interfaces.go — interface updated
5. migrations/20260310_add_index_consents_citizen_id.sql — new index

Focus areas:
- Is the SQL parameterized correctly (no string concatenation for LIMIT/OFFSET)?
- Does the handler have proper request validation without business logic leakage?
- Is the error handling in usecase using semantic error types?
- Are the interface changes backward compatible or properly versioned?
- Is the migration file using IF NOT EXISTS for the index?
- Do unit tests follow project mock patterns?

## Context from Prior Agents
### Developer's Changes:
- Repository: Added LIMIT $2 OFFSET $3 to query, new CountByCitizenID method
- Usecase: Added context.DeadlineExceeded → ErrTimeout mapping
- Handler: Added page/page_size query param parsing with validation
- Interface: Updated ConsentRepository with new method signatures
- Migration: CREATE INDEX on consents(citizen_id)
"""
)
```

**Expected Parallel Outputs (simulated):**

**QA E2E Output:**
```
## QA

**Task:** E2E test specs for consent pagination fix

**Test Code:**
tests/e2e/tests/consent/get-consent-by-citizen-id.spec.ts
- Implements REG-CON-001 through REG-CON-011
- Uses test helpers for seed data (createConsentRecords utility)
- Verifies pagination metadata structure
- Performance assertion for REG-CON-010 (< 500ms response time)

**Sign-Off:** Pending execution
```

**Code Reviewer Output:**
```
## Code Reviewer

**Task:** Convention compliance review of consent 500 fix
**Files Reviewed:** 5

### Findings

#### [WARNING] Missing IF NOT EXISTS on index creation
- **File:** migrations/20260310_add_index_consents_citizen_id.sql
- **Issue:** Index creation should use IF NOT EXISTS to be idempotent
- **Fix:** Change to CREATE INDEX IF NOT EXISTS idx_consents_citizen_id ON consents(citizen_id)

#### [WARNING] Missing step comments in usecase
- **File:** internal/consent/usecase/get_consent.go
- **Issue:** Usecase methods should have step comments (// Step 1: ..., // Step 2: ...)
- **Fix:** Add step comments to the GetConsentByCitizenID method

#### [INFO] Consider extracting pagination defaults to constants
- **File:** internal/consent/handler/consent_handler.go
- **Issue:** Magic numbers 50 (default page size) and 100 (max page size) should be named constants
- **Fix:** Extract to const defaultPageSize = 50, const maxPageSize = 100

---

**Summary:**
| Severity | Count |
|----------|-------|
| Blocker | 0 |
| Critical | 0 |
| Warning | 2 |
| Info | 1 |

**Verdict:** Approved (with warnings — should fix before merge but not blocking)
```

---

## Assembled Final Summary

**Task:** consent service return 500 error ตอน get consent by citizen_id ที่มี record เยอะกว่า 100 records — น่าจะเป็น query performance issue

**Workflow:** Bug Fix (selected because the primary symptom is HTTP 500 error; performance is a contributing factor addressed within the fix)

**Agents Used:** System Analyzer, Developer, QA, Code Reviewer

---

### System Analyzer

Root cause identified: Repository method `FindByCitizenID` executes an unbounded `SELECT * FROM consents WHERE citizen_id = $1` without LIMIT/OFFSET. Combined with a missing database index on `citizen_id`, this causes context timeout for citizens with 100+ records, which the handler maps to a generic 500 error.

**Severity:** High

### Developer

Implemented a 4-layer fix:
1. **Repository** — Added pagination (LIMIT/OFFSET) to `FindByCitizenID`, added `CountByCitizenID`, default page_size=50, max=100
2. **Usecase** — Added `context.DeadlineExceeded` → `ErrTimeout` mapping so timeout errors return proper error responses instead of 500
3. **Handler** — Added page/page_size query parameter parsing with validation, paginated response with metadata
4. **Migration** — `CREATE INDEX idx_consents_citizen_id ON consents(citizen_id)`

Unit tests added for all layers.

### QA

Designed 11 regression test cases (REG-CON-001 to REG-CON-011) covering:
- Default pagination behavior
- Explicit pagination with boundary conditions
- Invalid parameter handling
- Performance verification (1000+ records < 500ms)
- Empty result sets

E2E spec files written for all test cases. Sign-off blocked pending execution.

### Code Reviewer

Reviewed 5 changed files. No blockers or critical issues found.

| Severity | Count |
|----------|-------|
| Blocker | 0 |
| Critical | 0 |
| Warning | 2 |
| Info | 1 |

Warnings:
1. Migration should use `IF NOT EXISTS` for idempotency
2. Usecase missing step comments

**Verdict:** Approved with warnings

---

**Issues Found:**
- [WARNING] Migration file should use `CREATE INDEX IF NOT EXISTS` for idempotent reruns
- [WARNING] Usecase method missing step comments per convention
- [INFO] Magic numbers for pagination defaults should be extracted to named constants

**Gaps:**
- No project-specific CLAUDE.md found — convention checks were performed against standard Go Clean Architecture patterns. If the consent service has project-specific conventions, a follow-up review may be needed.
- E2E tests not yet executed — sign-off pending test run against running service with seed data.
- Down migration (rollback) not tested.

**Next Steps:**
1. Fix the two warnings from Code Reviewer before merging
2. Run the database migration on staging/pre-production with a copy of production data to verify index creation performance
3. Execute E2E test suite against staging environment
4. Monitor the endpoint after deployment — verify 500 errors stop and response times are within SLA
5. Consider adding the same pagination pattern to other endpoints that may have the same unbounded query issue (System Analyzer flagged this as a potential systemic pattern)
