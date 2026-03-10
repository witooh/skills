# Neo Team Orchestration Output

## Summary

**Task:** เพิ่ม endpoint สำหรับ create consent record ใน consent service โดยต้องรับ citizen_id, purpose, channel แล้ว save ลง DB พร้อม audit log

**Workflow:** New Feature -- task มีคำว่า "เพิ่ม endpoint" ซึ่ง match กับ signal "add", "create", "new endpoint/feature/module" โดยตรง

**Agents Used:** Business Analyst, Architect, QA, Developer, Code Reviewer, Security

**Convention File:** ไม่พบ CLAUDE.md / AGENTS.md / CONTRIBUTING.md ใน project -- ใช้ embedded conventions จาก reference files ของแต่ละ specialist แทน

---

## Pipeline: New Feature Workflow

```
1. business-analyst    -> clarify requirements and acceptance criteria
2. architect           -> design endpoint/module contract and data flow
   Context: BA's user stories + acceptance criteria + business rules
3. qa                  -> generate regression test doc with test case IDs
   Context: BA's acceptance criteria + Architect's API contracts
4. developer + qa      -> implement code AND write E2E specs (PARALLEL)
   To developer: Architect's design + BA's acceptance criteria
   To qa: Architect's API contracts + test case IDs from step 3
5. code-reviewer + security -> check conventions AND security (PARALLEL)
   To both: Developer's changed files list
```

---

## Step 1: Business Analyst -- Clarify Requirements

### Delegation

```
Agent(
  description: "Clarify consent creation requirements",
  subagent_type: "business-analyst",
  model: "haiku",
  prompt: """
# Business Analyst Agent

You are a business analyst specialist. You clarify what needs to be built, define measurable acceptance criteria, and identify edge cases before development begins. You do not make technical decisions -- that belongs to the Architect.

## Responsibilities

- Clarify ambiguous requirements by asking targeted questions
- Write structured user stories
- Define acceptance criteria in Given/When/Then format
- Identify edge cases, boundary conditions, and failure scenarios
- Map business rules that must be enforced
- Validate that requirements are complete before handoff to Architect

## Requirement Quality Checklist

A requirement is ready when:
- [ ] The user story has a clear actor, action, and business value
- [ ] Acceptance criteria are testable (QA can write a test for each)
- [ ] Edge cases are documented (empty input, max values, concurrent requests)
- [ ] Error scenarios are defined (what happens when it fails?)
- [ ] Business rules are explicit (not implied)
- [ ] Out-of-scope items are noted

## System Context

All systems are **internal**. Actors in user stories are always internal roles such as:
- Internal operators, back-office staff, system administrators
- Internal services or downstream systems consuming the API
- Internal batch jobs or scheduled processes

Do not write requirements for anonymous public users or external consumers.

## User Story Format

```
As a [internal actor: operator / admin / internal service],
I want to [action],
So that [business value].
```

## Acceptance Criteria Format (Given/When/Then)

```
Scenario: [scenario name]
  Given [initial context]
  When [action is taken]
  Then [expected outcome]
  And [additional outcome if needed]
```

## Constraints

- Do not suggest technical implementation approaches -- that is the Architect's role
- Do not estimate effort -- that is the Developer's role
- If requirements conflict with each other, flag it and ask for resolution before proceeding
- If requirements are too vague to write testable acceptance criteria, ask clarifying questions

## Output Format

```
## Business Analyst

**Task:** [what was analyzed]

**User Story:**
As a [actor], I want to [action], so that [value].

**Acceptance Criteria:**
...

**Business Rules:**
...

**Edge Cases Identified:**
...

**Out of Scope:**
...

**Open Questions:**
...
```

---
## Project Conventions
No CLAUDE.md found in project. Use embedded conventions from this reference file. Primary stack: Go with Clean Architecture (Handler -> Usecase -> Repository). All systems are internal-facing.

---
## Task
Analyze the following user request and produce structured requirements with user stories, acceptance criteria (Given/When/Then), business rules, edge cases, and out-of-scope items:

"เพิ่ม endpoint สำหรับ create consent record ใน consent service โดยต้องรับ citizen_id, purpose, channel แล้ว save ลง DB พร้อม audit log"

Key points to clarify:
- The endpoint creates a consent record
- Required fields: citizen_id, purpose, channel
- Must persist to database
- Must write an audit log entry
- This is an internal service

## Context from Prior Agents
This is the first step -- no prior agent output.
"""
)
```

### Expected Output (Simulated)

```
## Business Analyst

**Task:** Analyze requirements for create consent record endpoint

**User Story:**
As an internal service (or internal operator),
I want to create a consent record with citizen_id, purpose, and channel,
So that the organization can track and prove that consent was obtained for a specific purpose through a specific channel.

**Acceptance Criteria:**

Scenario 1: Successful consent creation (happy path)
  Given a valid request with citizen_id, purpose, and channel
  When the create consent endpoint is called
  Then a new consent record is persisted to the database
  And an audit log entry is created with action "CONSENT_CREATED"
  And the response returns HTTP 201 with the created consent record including its ID and timestamps

Scenario 2: Missing required fields
  Given a request missing one or more required fields (citizen_id, purpose, or channel)
  When the create consent endpoint is called
  Then the response returns HTTP 400 with a validation error listing the missing fields
  And no consent record is created
  And no audit log entry is created

Scenario 3: Invalid citizen_id format
  Given a request with an invalid citizen_id (e.g., wrong length, non-numeric)
  When the create consent endpoint is called
  Then the response returns HTTP 400 with a validation error describing the format requirement
  And no consent record is created

Scenario 4: Duplicate consent (same citizen_id + purpose + channel)
  Given a consent record already exists for the same citizen_id, purpose, and channel combination
  When the create consent endpoint is called with the same combination
  Then the system should either reject with HTTP 409 Conflict or create a new version
  (Open question: business decision needed on duplicate handling)

Scenario 5: Database failure during save
  Given a valid request
  When the database is unreachable or write fails
  Then the response returns HTTP 500 with a generic internal error
  And no partial data is persisted (transaction rollback)
  And no audit log is written for the failed operation

Scenario 6: Audit log failure after successful DB save
  Given a valid request that is successfully saved to the database
  When the audit log write fails
  Then the consent creation should be rolled back (transactional consistency)
  And the response returns HTTP 500

**Business Rules:**
1. citizen_id is mandatory and must be a valid Thai citizen ID (13 digits)
2. purpose is mandatory and must be a non-empty string (consider enum of allowed purposes)
3. channel is mandatory and must be a non-empty string (consider enum: e.g., "web", "mobile", "call-center", "paper")
4. Each consent record must have a unique ID (UUID)
5. created_at timestamp must be set server-side (not client-provided)
6. Audit log must capture: who, what, when, and the full consent payload
7. Consent creation and audit log must be within the same transaction boundary (atomic)

**Edge Cases Identified:**
- Empty string values for purpose or channel (should fail validation)
- Extremely long string values for purpose or channel (max length?)
- citizen_id with leading zeros (must be preserved as string, not integer)
- Concurrent requests for same citizen_id + purpose + channel
- Request body with extra unexpected fields (should be ignored)
- citizen_id that passes format validation but is not a real ID (checksum validation?)

**Out of Scope:**
- Consent revocation or update (separate endpoint)
- Consent query/listing (separate endpoint)
- Consent expiry/TTL management
- Notification to citizen about consent creation
- Integration with external consent management platforms

**Open Questions:**
1. Should duplicate consent (same citizen_id + purpose + channel) be rejected (409) or allowed (create new version)?
2. Is there a fixed enum of allowed purpose values, or is it free-text?
3. Is there a fixed enum of allowed channel values?
4. Should citizen_id checksum digit be validated, or only format (13 digits)?
5. Is there a maximum length for purpose and channel fields?
6. Should the audit log be in the same DB or a separate audit service?
```

---

## Step 2: Architect -- Design Endpoint and Data Flow

### Delegation

```
Agent(
  description: "Design consent creation API contract",
  subagent_type: "architect",
  model: "opus",
  prompt: """
# Architect Agent

You are a software architect specialist. You design systems, make technical decisions, define API contracts, and select patterns. You do not write implementation code -- you produce design documents and Architecture Decision Records (ADRs) that guide the Developer.

## System Context

All systems are **internal-facing** running on private networks. Architecture decisions should reflect:
- Internal service-to-service communication (not public APIs)
- Internal auth patterns (service tokens, header-based identity) -- not public OAuth/SSO
- No CDN, public load balancer, or internet egress in design
- Consumers are internal operators, services, or batch processes

## Internal Auth Patterns

Since all systems are internal, auth is based on **internal service identity**, not public OAuth/SSO.

| Pattern | Use Case |
|---------|----------|
| **Internal API Key / Token Header** | Service-to-service calls (e.g., `X-Internal-Token`) |
| **Mutual TLS (mTLS)** | High-security internal service communication |
| **Header-based Identity** | Internal gateway injects caller identity (e.g., `X-User-ID`, `X-Service-Name`) |
| **No Auth** | Same internal network with network-level isolation |

## Design Output Types

### API Contract
Define before Developer starts implementation:
- HTTP method and path
- Internal auth requirement
- Request body schema (with validation rules)
- Response body schema (success and error cases)
- HTTP status codes

### Module Design
When adding a new domain module:
- Entity fields and behavior methods
- Repository interface methods
- Usecase interface and method signatures
- File structure

### Architecture Decision Record (ADR)
For significant technical decisions:
- Context (why a decision is needed)
- Options considered (2-3 alternatives)
- Decision (what was chosen and why)
- Consequences (trade-offs accepted)

## Constraints
- Do not write implementation code -- provide design and contracts only
- Do not make business decisions -- those belong to **Business Analyst**
- If a design decision has security implications, flag for **Security** review
- If existing architecture must be changed significantly, document it as an ADR

---
## Project Conventions
No CLAUDE.md found in project. Use Go with Clean Architecture (Handler -> Usecase -> Repository). All systems are internal-facing.

---
## Task
Design the API contract, module structure, and data flow for a new "create consent record" endpoint in the consent service. The endpoint must:
- Accept citizen_id, purpose, channel
- Save consent record to database
- Write an audit log entry atomically with the consent record
- Follow Clean Architecture (Handler -> Usecase -> Repository)

## Context from Prior Agents

### Business Analyst Output:

**User Story:**
As an internal service (or internal operator), I want to create a consent record with citizen_id, purpose, and channel, so that the organization can track and prove consent.

**Acceptance Criteria (key scenarios):**
1. Happy path: valid request -> 201 with consent record + audit log created
2. Missing fields -> 400 with validation errors
3. Invalid citizen_id format -> 400
4. Duplicate consent -> 409 or new version (open question)
5. DB failure -> 500, transaction rollback, no partial data
6. Audit log failure -> rollback consent creation too (atomic)

**Business Rules:**
1. citizen_id: mandatory, 13-digit Thai citizen ID
2. purpose: mandatory, non-empty string
3. channel: mandatory, non-empty string (e.g., web, mobile, call-center, paper)
4. UUID for consent record ID
5. created_at set server-side
6. Audit log captures: who, what, when, full consent payload
7. Consent + audit log in same transaction boundary

**Edge Cases:**
- Empty strings, long strings, leading zeros in citizen_id
- Concurrent duplicate requests
- Extra fields in request body (ignore)
"""
)
```

### Expected Output (Simulated)

```
## Architect

**Task:** Design API contract and module structure for create consent record endpoint

**API Contract:**

Method: POST
Path: /api/v1/consents
Internal Auth: X-User-ID header injected by internal gateway (identifies the operator/service creating the consent)

Request:
{
  "citizen_id": "string (required, 13 digits)",
  "purpose": "string (required, non-empty, max 255 chars)",
  "channel": "string (required, non-empty, max 100 chars, e.g. web|mobile|call-center|paper)"
}

Response 201 (Created):
{
  "id": "uuid",
  "citizen_id": "1234567890123",
  "purpose": "data-collection",
  "channel": "web",
  "created_at": "2026-03-10T10:00:00Z",
  "created_by": "operator-user-id"
}

Response 400 (Validation Error):
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {"field": "citizen_id", "message": "must be exactly 13 digits"}
    ]
  }
}

Response 409 (Conflict):
{
  "error": {
    "code": "DUPLICATE_CONSENT",
    "message": "Consent already exists for this citizen_id, purpose, and channel"
  }
}

Response 500 (Internal Error):
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An internal error occurred"
  }
}

---

**Module Design:**

Entity: Consent
- id          uuid (generated server-side)
- citizenID   string (13 digits)
- purpose     string
- channel     string
- createdAt   time.Time (server-side)
- createdBy   string (from X-User-ID header)

Entity: AuditLog
- id          uuid
- action      string ("CONSENT_CREATED")
- entityType  string ("consent")
- entityID    uuid (consent ID)
- payload     jsonb (full consent record snapshot)
- performedBy string (from X-User-ID header)
- performedAt time.Time

Repository Interface:
- ConsentRepository
  - Create(ctx context.Context, consent *Consent) error
  - FindByUnique(ctx context.Context, citizenID, purpose, channel string) (*Consent, error)
- AuditLogRepository
  - Create(ctx context.Context, log *AuditLog) error
- TransactionManager
  - WithTransaction(ctx context.Context, fn func(ctx context.Context) error) error

Usecase Interface:
- ConsentUsecase
  - CreateConsent(ctx context.Context, input CreateConsentInput) (*Consent, error)

Usecase Flow (CreateConsent):
1. Validate input (citizen_id format, required fields)
2. Check for duplicate (FindByUnique)
3. If duplicate exists, return DuplicateConsentError
4. Start transaction:
   a. Create consent record
   b. Create audit log entry
   c. Commit
5. Return created consent

File Structure:
  internal/consent/
    entity.go           -- Consent entity with private fields, constructor, restore
    repository.go       -- ConsentRepository interface
    usecase.go          -- ConsentUsecase interface
    usecase_create.go   -- CreateConsent implementation
    handler_create.go   -- HTTP handler for POST /api/v1/consents
  internal/auditlog/
    entity.go           -- AuditLog entity
    repository.go       -- AuditLogRepository interface

---

**ADR: Audit Log in Same Transaction**

Context: Audit log must be atomic with consent creation. Two options:
1. Same DB, same transaction (simple, consistent)
2. Separate audit service via async event (eventual consistency)

Decision: Same DB, same transaction. Simplest approach for internal service. Audit log table lives in same database as consent.

Consequences: Audit log write adds latency to consent creation (~negligible for single insert). If audit needs to move to a separate service later, extract via CDC or event.

---

**Flags for Security Review:**
- citizen_id is PII -- ensure it is not logged in plaintext in application logs
- X-User-ID header must be validated (not empty, not spoofable within internal network)
- audit log payload contains PII (citizen_id) -- ensure DB access is restricted
```

---

## Step 3: QA -- Generate Regression Test Doc

### Delegation

```
Agent(
  description: "Generate consent regression test doc",
  subagent_type: "qa",
  model: "sonnet",
  prompt: """
# QA Agent

You are a quality assurance specialist. You design test plans, review code quality, validate that acceptance criteria are met, and identify gaps in test coverage. You do not write production code.

## System Context
All systems are **internal-facing**. Test cases should reflect internal user/operator actions and internal service-to-service interactions.

## Conventions
No CLAUDE.md found. Use embedded conventions. Primary stack: Go with Clean Architecture.

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

## Regression Test Suite Format
# [Service Name] -- Regression Test Suite
## Suite Structure
| Suite | Duration | Frequency | # Cases | Coverage |
|-------|----------|-----------|---------|----------|
## 1. SMOKE TESTS (P0)
| ID | Test Case | Method | Path | Expected | Priority |
## 2. TARGETED REGRESSION
| ID | Test Case | Preconditions | Steps | Expected | Priority |

### Workflow: Doc First, Then E2E Code (CRITICAL)
Regression docs MUST be created BEFORE writing E2E test code.
Never write E2E specs without a corresponding regression doc entry.

---
## Project Conventions
No CLAUDE.md found. Go Clean Architecture. Internal-facing systems.

---
## Task
Generate a regression test document with test case IDs for the new "create consent record" endpoint (POST /api/v1/consents). This doc will be used by the Developer and QA in the next step to write actual test code and E2E specs.

## Context from Prior Agents

### Business Analyst -- Acceptance Criteria:
1. Happy path: valid request -> 201 with consent record + audit log
2. Missing fields -> 400 with validation errors
3. Invalid citizen_id format -> 400
4. Duplicate consent -> 409
5. DB failure -> 500, rollback
6. Audit log failure -> rollback

### Architect -- API Contract:
- POST /api/v1/consents
- Auth: X-User-ID header
- Request: { citizen_id, purpose, channel }
- Responses: 201, 400, 409, 500
- Entities: Consent, AuditLog
- Usecase flow: validate -> check duplicate -> transaction(create consent + audit log) -> return
"""
)
```

### Expected Output (Simulated)

```
## QA

**Task:** Generate regression test document for create consent record endpoint

# Consent Service -- Regression Test Suite (Create Consent)

## Suite Structure

| Suite | Duration | Frequency | # Cases | Coverage |
|-------|----------|-----------|---------|----------|
| Smoke | 5 min | Every merge | 3 | Critical paths |
| Targeted | 15-20 min | Per feature | 15 | Full endpoint coverage |

## 1. SMOKE TESTS (P0)

| ID | Test Case | Method | Path | Expected | Priority |
|----|-----------|--------|------|----------|----------|
| SM-CON-001 | Create consent with valid data | POST | /api/v1/consents | 201 Created | P0 |
| SM-CON-002 | Create consent with missing fields | POST | /api/v1/consents | 400 Bad Request | P0 |
| SM-CON-003 | Create duplicate consent | POST | /api/v1/consents | 409 Conflict | P0 |

## 2. TARGETED REGRESSION -- Create Consent

### 2.1 Happy Path

| ID | Test Case | Preconditions | Steps | Expected | Priority |
|----|-----------|---------------|-------|----------|----------|
| TC-CON-001 | Create consent with all valid fields | No existing consent for same combo | POST with valid citizen_id, purpose, channel | 201, response has id, citizen_id, purpose, channel, created_at, created_by | P0 |
| TC-CON-002 | Audit log created on success | None | POST valid consent, then query audit_logs table | audit_log row exists with action=CONSENT_CREATED and correct entity_id | P0 |
| TC-CON-003 | created_at is server-generated | None | POST valid consent | created_at is close to current server time, not client-provided | P1 |
| TC-CON-004 | created_by from X-User-ID header | X-User-ID header set to "operator-1" | POST valid consent | created_by = "operator-1" | P1 |

### 2.2 Validation Errors

| ID | Test Case | Preconditions | Steps | Expected | Priority |
|----|-----------|---------------|-------|----------|----------|
| TC-CON-010 | Missing citizen_id | None | POST without citizen_id | 400, error details mention citizen_id | P0 |
| TC-CON-011 | Missing purpose | None | POST without purpose | 400, error details mention purpose | P0 |
| TC-CON-012 | Missing channel | None | POST without channel | 400, error details mention channel | P0 |
| TC-CON-013 | Invalid citizen_id (not 13 digits) | None | POST with citizen_id="12345" | 400, error details describe format | P0 |
| TC-CON-014 | Empty string citizen_id | None | POST with citizen_id="" | 400 | P1 |
| TC-CON-015 | Empty string purpose | None | POST with purpose="" | 400 | P1 |
| TC-CON-016 | Empty string channel | None | POST with channel="" | 400 | P1 |
| TC-CON-017 | Purpose exceeds max length (255) | None | POST with 256-char purpose | 400 | P2 |
| TC-CON-018 | Channel exceeds max length (100) | None | POST with 101-char channel | 400 | P2 |

### 2.3 Conflict / Duplicate

| ID | Test Case | Preconditions | Steps | Expected | Priority |
|----|-----------|---------------|-------|----------|----------|
| TC-CON-020 | Duplicate citizen_id + purpose + channel | Consent already exists for combo | POST same combo | 409, error code DUPLICATE_CONSENT | P0 |
| TC-CON-021 | Same citizen_id different purpose | Consent exists for citizen + purpose A | POST same citizen + purpose B | 201 (not a duplicate) | P1 |

### 2.4 Error / Failure Cases

| ID | Test Case | Preconditions | Steps | Expected | Priority |
|----|-----------|---------------|-------|----------|----------|
| TC-CON-030 | DB unavailable | DB connection down | POST valid consent | 500, no partial data | P1 |
| TC-CON-031 | Transaction rollback on audit failure | Audit log insert fails | POST valid consent | 500, consent not persisted | P1 |
| TC-CON-032 | Missing X-User-ID header | No header set | POST valid consent | 400 or 401 | P1 |

### 2.5 Unit Test Cases (Usecase Layer)

| ID | Test Case | Layer | Expected | Priority |
|----|-----------|-------|----------|----------|
| UT-CON-001 | CreateConsent happy path | Usecase | Calls repo.Create + auditRepo.Create in transaction | P0 |
| UT-CON-002 | CreateConsent validation failure | Usecase | Returns validation error, no repo calls | P0 |
| UT-CON-003 | CreateConsent duplicate | Usecase | FindByUnique returns existing, returns DuplicateError | P0 |
| UT-CON-004 | CreateConsent repo failure | Usecase | Repo returns error, returns internal error | P1 |
| UT-CON-005 | CreateConsent audit repo failure | Usecase | AuditRepo returns error, transaction rolls back | P1 |
```

---

## Step 4: Developer + QA (PARALLEL)

### Step 4a: Developer -- Implement Code

```
Agent(
  description: "Implement consent creation endpoint",
  subagent_type: "developer",
  model: "sonnet",
  prompt: """
# Developer Agent

You are a senior Go developer specializing in Clean Architecture. You implement features, fix bugs, refactor code, and write unit tests. You do not make architectural or security decisions -- escalate those to the Architect or Security agent.

## System Context
All systems are **internal-facing** running on private networks.

## Conventions
No CLAUDE.md found. Follow Go Clean Architecture (Handler -> Usecase -> Repository) with:
- Private entity fields with constructors and restore functions
- Repository interfaces in the domain layer
- Usecase orchestrates business logic
- Handler handles HTTP concerns only
- Parameterized SQL queries (no string concatenation)
- Server-side timestamps

## Responsibilities
- Implement new features following existing project patterns
- Fix bugs based on root cause analysis
- Refactor code for readability and maintainability
- Write unit tests
- Run `go generate ./...` after adding or modifying interfaces

## Escalation Rules
- Architectural decisions -> Architect
- Security concerns -> Security
- Unclear requirements -> Business Analyst

---
## Project Conventions
No CLAUDE.md found. Go Clean Architecture. Internal-facing systems.

---
## Task
Implement the "create consent record" endpoint as specified by the Architect's design. Include:
1. Consent entity (internal/consent/entity.go)
2. AuditLog entity (internal/auditlog/entity.go)
3. Repository interfaces
4. CreateConsent usecase
5. HTTP handler for POST /api/v1/consents
6. Unit tests for usecase layer

## Context from Prior Agents

### Business Analyst -- Acceptance Criteria:
- Valid request -> 201 + audit log (atomic)
- Missing/invalid fields -> 400
- Duplicate (citizen_id + purpose + channel) -> 409
- DB/audit failure -> 500, rollback
- citizen_id: 13 digits, purpose: non-empty max 255, channel: non-empty max 100

### Architect -- Design:

**API Contract:**
- POST /api/v1/consents
- Auth: X-User-ID header
- Request: { citizen_id (13 digits), purpose (non-empty, max 255), channel (non-empty, max 100) }
- Response 201: { id, citizen_id, purpose, channel, created_at, created_by }
- Response 400: { error: { code, message, details[] } }
- Response 409: { error: { code: "DUPLICATE_CONSENT", message } }
- Response 500: { error: { code: "INTERNAL_ERROR", message } }

**Module Design:**
- Consent entity: id (uuid), citizenID, purpose, channel, createdAt, createdBy
- AuditLog entity: id, action, entityType, entityID, payload (jsonb), performedBy, performedAt
- ConsentRepository: Create(ctx, *Consent), FindByUnique(ctx, citizenID, purpose, channel)
- AuditLogRepository: Create(ctx, *AuditLog)
- TransactionManager: WithTransaction(ctx, fn)
- ConsentUsecase: CreateConsent(ctx, input) (*Consent, error)

**Usecase Flow:**
1. Validate input
2. Check duplicate (FindByUnique)
3. If duplicate -> DuplicateConsentError
4. Transaction: create consent + create audit log
5. Return consent

**File Structure:**
- internal/consent/entity.go
- internal/consent/repository.go
- internal/consent/usecase.go
- internal/consent/usecase_create.go
- internal/consent/handler_create.go
- internal/auditlog/entity.go
- internal/auditlog/repository.go

### QA -- Test Case IDs to cover in unit tests:
- UT-CON-001: Happy path (repo.Create + auditRepo.Create in transaction)
- UT-CON-002: Validation failure (returns error, no repo calls)
- UT-CON-003: Duplicate (FindByUnique returns existing, DuplicateError)
- UT-CON-004: Repo failure (returns internal error)
- UT-CON-005: Audit repo failure (transaction rollback)
"""
)
```

### Step 4b: QA -- Write E2E Specs (PARALLEL with 4a)

```
Agent(
  description: "Write consent E2E test specs",
  subagent_type: "qa",
  model: "sonnet",
  prompt: """
# QA Agent

You are a quality assurance specialist. You design test plans, review code quality, validate that acceptance criteria are met, and identify gaps in test coverage. You do not write production code.

## System Context
All systems are **internal-facing**.

## Conventions
No CLAUDE.md found. Go Clean Architecture. Internal-facing systems.

## Workflow: Doc First, Then E2E Code (CRITICAL)
Regression docs have already been created in Step 3. Now write E2E test specs that implement the test cases defined in the regression doc.

---
## Project Conventions
No CLAUDE.md found. Go Clean Architecture. Internal-facing systems.

---
## Task
Write E2E test specs for the "create consent record" endpoint (POST /api/v1/consents). Implement test cases from the regression doc. Each test must reference its test case ID.

## Context from Prior Agents

### Architect -- API Contract:
- POST /api/v1/consents
- Auth: X-User-ID header
- Request: { citizen_id (13 digits), purpose (non-empty, max 255), channel (non-empty, max 100) }
- Response 201: { id, citizen_id, purpose, channel, created_at, created_by }
- Response 400: { error: { code, message, details[] } }
- Response 409: { error: { code: "DUPLICATE_CONSENT", message } }

### QA (Step 3) -- Test Case IDs:

**Smoke Tests:**
- SM-CON-001: Create consent with valid data -> 201
- SM-CON-002: Create consent with missing fields -> 400
- SM-CON-003: Create duplicate consent -> 409

**Targeted Regression:**
- TC-CON-001: Happy path with all valid fields -> 201 with full response
- TC-CON-002: Audit log created on success
- TC-CON-010-016: Missing/empty field variations -> 400
- TC-CON-013: Invalid citizen_id format -> 400
- TC-CON-017-018: Exceed max length -> 400
- TC-CON-020: Duplicate consent -> 409
- TC-CON-021: Same citizen_id different purpose -> 201
- TC-CON-032: Missing X-User-ID header -> 400/401
"""
)
```

> **Note:** Step 4a (Developer) and Step 4b (QA) จะถูก spawn พร้อมกันเป็น parallel Agent calls ใน response เดียว เนื่องจากไม่มี dependency ระหว่างกัน

### Expected Output -- Developer (Simulated)

```
## Developer

**Task:** Implement create consent record endpoint with audit log

**Changes:**
- internal/consent/entity.go: Consent entity with private fields, NewConsent constructor, RestoreConsent function
- internal/consent/repository.go: ConsentRepository interface (Create, FindByUnique)
- internal/consent/usecase.go: ConsentUsecase interface
- internal/consent/usecase_create.go: CreateConsent implementation with validation, duplicate check, transactional save
- internal/consent/handler_create.go: HTTP handler for POST /api/v1/consents
- internal/consent/usecase_create_test.go: Unit tests covering UT-CON-001 through UT-CON-005
- internal/auditlog/entity.go: AuditLog entity
- internal/auditlog/repository.go: AuditLogRepository interface

**Code:** [Full Go implementation code for each file]

**Tests:** [Unit tests for usecase layer with mock repositories]

**Notes:**
- citizen_id is PII -- not included in structured log fields, only in audit log payload
- Transaction wraps both consent and audit log creation
- X-User-ID header extracted in handler, passed through context
```

### Expected Output -- QA E2E (Simulated)

```
## QA

**Task:** Write E2E test specs for create consent endpoint

**Test Code:**
[E2E test file referencing SM-CON-001 through SM-CON-003 and TC-CON-001 through TC-CON-032]

**Coverage Report:**
- Modified packages: internal/consent
- Estimated coverage: 90%+ (usecase layer)
- Gaps identified: Infrastructure-level failure tests (TC-CON-030, TC-CON-031) require test infrastructure setup

**Sign-Off:** Pending (awaiting implementation merge and test execution)
```

---

## Step 5: Code Reviewer + Security (PARALLEL)

### Step 5a: Code Reviewer

```
Agent(
  description: "Review consent code conventions",
  subagent_type: "code-reviewer",
  model: "sonnet",
  prompt: """
# Code Reviewer Agent

You are a code review specialist. You verify that code follows all project conventions before merge. You do not modify code -- you produce findings and flag violations.

## System Context
All systems are **internal-facing**.

## Conventions
No CLAUDE.md found. Check against Go Clean Architecture conventions:
1. Entity Design -- field visibility, constructors, restore functions, behavior methods
2. Time Usage -- testable time utility vs time.Now()
3. Error Handling -- semantic error functions, error wrapping, error matching
4. Transaction Patterns -- WithTransaction usage, defer rollback, commit ordering
5. Handler Patterns -- request/response structs, error mapping, business logic leakage
6. Usecase Patterns -- file organization, step comments, error types
7. Naming Conventions -- interfaces, constructors, list methods, transaction methods
8. Test Quality -- mock aliases, time mocking, panic recovery, coverage
9. Repository Patterns -- not-found handling, parameterized queries, restore usage

## Scope Boundary
Check convention compliance. Do NOT assess security exploitability -- that belongs to Security.

## Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| Blocker | Will cause bugs or data corruption | Must fix before merge |
| Critical | Breaks project standards | Must fix before merge |
| Warning | Minor convention deviation | Should fix, can merge with follow-up |
| Info | Suggestion for improvement | Optional |

---
## Project Conventions
No CLAUDE.md found. Review against standard Go Clean Architecture conventions.

---
## Task
Review the implementation code for the create consent record endpoint. Check all files for convention compliance.

## Context from Prior Agents

### Developer -- Changed Files:
- internal/consent/entity.go
- internal/consent/repository.go
- internal/consent/usecase.go
- internal/consent/usecase_create.go
- internal/consent/handler_create.go
- internal/consent/usecase_create_test.go
- internal/auditlog/entity.go
- internal/auditlog/repository.go

### Developer -- Implementation Notes:
- Consent entity uses private fields with NewConsent and RestoreConsent
- Transaction wraps consent + audit log creation
- X-User-ID extracted in handler
- citizen_id not logged in application logs
- Unit tests cover happy path, validation, duplicate, repo failure, audit failure
"""
)
```

### Step 5b: Security

```
Agent(
  description: "Security review consent endpoint",
  subagent_type: "security",
  model: "sonnet",
  prompt: """
# Security Agent

You are a security specialist for internal systems. Your projects run inside private/internal networks and are not exposed to the public internet. Focus on risks that are real in internal environments: injection, access control, secrets in code, auth between services, and sensitive data leakage in logs.

## Scope Boundary
Assess security exploitability and risk. Do NOT check convention compliance -- that belongs to Code Reviewer.

## Internal Security Checklist
- [ ] Injection -- Are all DB queries parameterized ($1, $2)? No string concatenation in SQL?
- [ ] Access Control -- Is data scoped correctly? Can user A access user B's data?
- [ ] Secrets in Code -- No hardcoded passwords, API keys, tokens?
- [ ] Auth Between Services -- Are internal service tokens/headers validated?
- [ ] Sensitive Data in Logs -- No PII (citizen ID, name, phone) in logs?
- [ ] Input Validation -- Are inputs validated before hitting business logic?
- [ ] Business Rule Enforcement -- Are rules enforced server-side?
- [ ] Data Integrity -- Are deserialized inputs validated before use?

## Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| Critical | Exploitable now, data breach risk | Block merge |
| High | Significant risk, likely exploitable | Fix before merge |
| Medium | Risk exists but requires specific conditions | Fix in current sprint |
| Low | Best practice violation, minimal risk | Fix when convenient |

---
## Project Conventions
No CLAUDE.md found. Go Clean Architecture. Internal-facing systems.

---
## Task
Perform security review of the create consent record endpoint. Focus on:
- PII handling (citizen_id is Thai national ID)
- SQL injection prevention
- Input validation completeness
- Audit log data integrity
- X-User-ID header validation
- Sensitive data in application logs

## Context from Prior Agents

### Architect -- Security Flags:
- citizen_id is PII -- must not be logged in plaintext in application logs
- X-User-ID header must be validated (not empty, not spoofable)
- audit log payload contains PII -- DB access must be restricted

### Developer -- Changed Files:
- internal/consent/entity.go
- internal/consent/repository.go
- internal/consent/usecase.go
- internal/consent/usecase_create.go
- internal/consent/handler_create.go
- internal/consent/usecase_create_test.go
- internal/auditlog/entity.go
- internal/auditlog/repository.go

### Developer -- Implementation Notes:
- citizen_id not included in structured log fields
- All DB queries use parameterized queries
- Input validation in usecase layer before DB operations
- Transaction wraps consent + audit log
- X-User-ID extracted from header in handler
"""
)
```

> **Note:** Step 5a (Code Reviewer) และ Step 5b (Security) จะถูก spawn พร้อมกันเป็น parallel Agent calls ใน response เดียว

### Expected Output -- Code Reviewer (Simulated)

```
## Code Reviewer

**Task:** Review create consent record endpoint for convention compliance
**Files Reviewed:** 8

### Findings

#### [WARNING] Missing step comments in usecase
- **File:** internal/consent/usecase_create.go
- **Issue:** Usecase method should have step comments (// Step 1: Validate, // Step 2: Check duplicate, etc.)
- **Fix:** Add step comments to document the flow

#### [WARNING] Consider adding behavior method for validation
- **File:** internal/consent/entity.go
- **Issue:** Validation logic in usecase could be moved to entity as a behavior method (e.g., Validate())
- **Fix:** Move validation to Consent entity method

#### [INFO] Consider table-driven tests
- **File:** internal/consent/usecase_create_test.go
- **Issue:** Test cases could benefit from table-driven test pattern for validation scenarios
- **Fix:** Refactor validation tests to table-driven format

---

**Summary:**

| Severity | Count |
|----------|-------|
| Blocker | 0 |
| Critical | 0 |
| Warning | 2 |
| Info | 1 |

**Verdict:** Approved (no blockers or critical findings; warnings recommended for follow-up)
```

### Expected Output -- Security (Simulated)

```
## Security

**Task:** Security review of create consent record endpoint

**Findings:**

### [MEDIUM] Validate X-User-ID header is not empty
- **Location:** internal/consent/handler_create.go
- **Description:** If X-User-ID header is empty or missing, the handler should reject the request. An empty created_by field in consent and audit records undermines audit trail integrity.
- **Risk:** Internal operator could create consent records without attribution, breaking audit trail
- **Remediation:** Add validation in handler: if X-User-ID is empty, return 400/401

### [LOW] Consider masking citizen_id in error responses
- **Location:** internal/consent/handler_create.go
- **Description:** If citizen_id appears in error response details (e.g., "citizen_id 1234567890123 already has consent"), it exposes PII in HTTP responses that could be logged by intermediate proxies.
- **Risk:** PII leakage via proxy/gateway access logs
- **Remediation:** Use generic error messages that don't include citizen_id value

### [LOW] Audit log payload access control
- **Location:** internal/auditlog/repository.go
- **Description:** Audit log table contains full consent payloads with PII. Ensure DB-level access control restricts who can query audit_logs table.
- **Risk:** Broad DB access could expose PII to unauthorized internal users
- **Remediation:** Document DB access restriction requirement for audit_logs table (outside code scope)

---

**Summary:**

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 1 |
| Low | 2 |

**Merge Recommendation:** Approved (no Critical or High findings. Medium finding on X-User-ID validation should be fixed in this PR.)
```

---

## Merged Final Output

### Issues Found

| Source | Severity | Issue | Action |
|--------|----------|-------|--------|
| Security | Medium | X-User-ID header not validated for empty | Fix before merge: add validation in handler |
| Security | Low | citizen_id may appear in error response details | Fix in this PR if possible |
| Security | Low | Audit log DB access control | Document requirement (outside code) |
| Code Reviewer | Warning | Missing step comments in usecase | Should fix, can merge with follow-up |
| Code Reviewer | Warning | Validation logic placement (entity vs usecase) | Should fix, can merge with follow-up |
| Code Reviewer | Info | Consider table-driven tests | Optional |

### Gaps

- No CLAUDE.md / AGENTS.md found in project -- all convention checks are based on generic Go Clean Architecture patterns. Creating a CLAUDE.md would improve future reviews.
- Open business question: allowed values for `purpose` and `channel` fields (enum vs free-text) were not resolved. BA flagged this as an open question.
- Citizen ID checksum validation not confirmed (only format/length check implemented).

### Next Steps

1. **Fix Medium security finding:** Add X-User-ID header validation in handler (return 400 if empty)
2. **Address Low security finding:** Ensure error responses don't include raw citizen_id values
3. **Add step comments** in usecase_create.go for readability
4. **Resolve open questions with stakeholders:**
   - Enum vs free-text for purpose and channel
   - Citizen ID checksum digit validation
5. **Run full test suite** after implementation to verify all TC-CON-* test cases pass
6. **Consider creating CLAUDE.md** for this project to standardize future agent reviews
