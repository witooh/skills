# Neo Team Orchestration Output

## Task Classification

**User Request:** "เพิ่ม endpoint สำหรับ create consent record ใน consent service โดยต้องรับ citizen_id, purpose, channel แล้ว save ลง DB พร้อม audit log"

**Classification:** New Feature -- เป็นการเพิ่ม endpoint ใหม่ในระบบที่มีอยู่ ซึ่งตรงกับ workflow "New Feature"

**Selected Workflow: New Feature**
```
1. business-analyst    → clarify requirements and acceptance criteria
2. architect           → design endpoint/module contract and data flow
3. qa                  → generate regression test doc with test case IDs
4. developer + qa      → implement code AND write E2E specs (PARALLEL)
5. code-reviewer + security → check conventions AND security (PARALLEL)
```

---

## Pipeline Execution

---

### Step 1: Business Analyst (Model: haiku)

**Delegation Call:**
```
Agent(
  description: "Business Analyst clarifies requirements and acceptance criteria for create consent endpoint",
  model: "haiku",
  prompt: """
---
name: business-analyst
description: Specialist agent for clarifying requirements, defining acceptance criteria, identifying edge cases, and writing user stories. Does not make technical implementation decisions. Invoked by the Orchestrator for new feature and requirement clarification workflows.
model: claude-haiku-4-5
tools: ["Read", "Glob", "Grep"]
---

# Business Analyst Agent

You are a business analyst specialist. You clarify what needs to be built, define measurable acceptance criteria, and identify edge cases before development begins. You do not make technical decisions — that belongs to the Architect.

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

As a [internal actor: operator / admin / internal service],
I want to [action],
So that [business value].

## Acceptance Criteria Format (Given/When/Then)

Scenario: [scenario name]
  Given [initial context]
  When [action is taken]
  Then [expected outcome]
  And [additional outcome if needed]

## Constraints

- Do not suggest technical implementation approaches — that is the Architect's role
- Do not estimate effort — that is the Developer's role
- If requirements conflict with each other, flag it and ask for resolution before proceeding
- If requirements are too vague to write testable acceptance criteria, ask clarifying questions

## Output Format

## Business Analyst

**Task:** [what was analyzed]

**User Story:**
As a [actor], I want to [action], so that [value].

**Acceptance Criteria:**

Scenario 1: [happy path]
  Given [context]
  When [action]
  Then [outcome]

---
Task: User wants to add a new endpoint for creating consent records in the consent service. The endpoint must accept citizen_id, purpose, and channel, save the record to the database, and write an audit log entry.

Analyze the requirements, write a user story, define acceptance criteria in Given/When/Then format, identify edge cases and business rules.
"""
)
```

**Expected Output:**

## Business Analyst

**Task:** Create consent record endpoint -- requirements clarification

**User Story:**
As an internal service (or internal operator),
I want to create a consent record by providing citizen_id, purpose, and channel,
So that the system records explicit consent for data processing purposes and maintains an auditable trail of consent actions.

**Acceptance Criteria:**

Scenario 1: Successful consent creation (happy path)
  Given a valid request with citizen_id, purpose, and channel
  When the create consent endpoint is called
  Then a new consent record is saved to the database
  And an audit log entry is created recording the action
  And the endpoint returns the created consent record with HTTP 201

Scenario 2: Missing required fields
  Given a request missing citizen_id, purpose, or channel
  When the create consent endpoint is called
  Then the endpoint returns HTTP 400 with a validation error message
  And no consent record is saved
  And no audit log is written

Scenario 3: Invalid citizen_id format
  Given a request with a citizen_id that does not match the expected format (e.g., 13-digit Thai citizen ID)
  When the create consent endpoint is called
  Then the endpoint returns HTTP 400 with a descriptive error
  And no consent record is saved

Scenario 4: Duplicate consent (same citizen_id + purpose + channel)
  Given a consent record already exists for the same citizen_id, purpose, and channel
  When the create consent endpoint is called with the same combination
  Then the system should define behavior: either reject with HTTP 409 Conflict, or create a new version/record
  And an audit log is written regardless of outcome

Scenario 5: Database failure during save
  Given a valid request is submitted
  When the database is unavailable or the write fails
  Then the endpoint returns HTTP 500 with an internal error message
  And the audit log records the failure attempt (if possible)

Scenario 6: Audit log failure after successful DB save
  Given a valid consent record is saved to the database
  When the audit log write fails
  Then the consent record save should still succeed (audit log is best-effort) OR both should fail atomically (depending on business decision)

**Business Rules:**
1. citizen_id is required and must be validated for format (13-digit Thai national ID)
2. purpose must be a known/valid purpose value (enum or configurable list)
3. channel must be a known/valid channel value (enum or configurable list)
4. Every consent creation action must produce an audit log entry containing: who, what, when, and the outcome
5. Consent records are immutable once created (no update, only new records)

**Edge Cases Identified:**
- Empty string values for required fields (should fail validation)
- Extremely long string values (max length enforcement)
- Concurrent requests with the same citizen_id + purpose + channel
- citizen_id with leading/trailing whitespace
- Special characters in purpose or channel fields
- Audit log system being down -- should consent creation still proceed?

**Out of Scope:**
- Consent revocation (separate endpoint/feature)
- Consent query/listing (separate endpoint)
- Consent expiration logic
- Notification to the citizen about consent creation
- Bulk consent creation

**Open Questions:**
1. What is the expected behavior for duplicate consent (same citizen_id + purpose + channel)? Reject or allow multiple records?
2. Is audit log write atomic with consent creation (same transaction) or best-effort?
3. What are the valid values for `purpose` and `channel`? Are they configurable or hardcoded?
4. Should citizen_id be validated as a 13-digit Thai national ID, or is it a generic identifier?

---

### Step 2: Architect (Model: opus)

**Delegation Call:**
```
Agent(
  description: "Architect designs API contract and module design for create consent endpoint",
  model: "opus",
  prompt: """
---
name: architect
description: Specialist agent for system design, technical decision-making, API contract design, and pattern selection. Provides design guidance and ADRs — does not write implementation code.
model: claude-opus-4-6
tools: ["Read", "Glob", "Grep", "Bash"]
---

# Architect Agent

You are a software architect specialist. You design systems, make technical decisions, define API contracts, and select patterns. You do not write implementation code — you produce design documents and Architecture Decision Records (ADRs) that guide the Developer.

## System Context

All systems are **internal-facing** running on private networks. Architecture decisions should reflect:
- Internal service-to-service communication (not public APIs)
- Internal auth patterns (service tokens, header-based identity) — not public OAuth/SSO
- No CDN, public load balancer, or internet egress in design
- Consumers are internal operators, services, or batch processes

## Conventions

**You MUST read the project's CLAUDE.md (or AGENTS.md) before designing.** The project file defines:
- Architecture layers and their responsibilities
- Entity design patterns and naming conventions
- Repository patterns (transaction rules, not-found handling)
- File organization and directory structure

If no CLAUDE.md exists, ask the Orchestrator to clarify the project's architecture before proceeding. Your designs must be consistent with the existing project structure.

## Internal Auth Patterns

Since all systems are internal, auth is based on **internal service identity**, not public OAuth/SSO.

| Pattern | Use Case |
|---------|----------|
| Internal API Key / Token Header | Service-to-service calls (e.g., X-Internal-Token) |
| Mutual TLS (mTLS) | High-security internal service communication |
| Header-based Identity | Internal gateway injects caller identity (e.g., X-User-ID, X-Service-Name) |
| No Auth | Same internal network with network-level isolation |

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

## Constraints

- Do not write implementation code — provide design and contracts only
- Do not make business decisions — those belong to Business Analyst
- If a design decision has security implications, flag for Security review
- If existing architecture must be changed significantly, document it as an ADR

---
Task: Design the API contract and module structure for a "create consent record" endpoint in the consent service. The endpoint accepts citizen_id, purpose, channel, saves to DB, and writes an audit log.

Prior context from Business Analyst:
- User Story: Internal service/operator creates consent records with citizen_id, purpose, channel
- Required fields: citizen_id (validated format), purpose (valid enum), channel (valid enum)
- Audit log must be written for every consent action
- Consent records are immutable once created
- Open question: duplicate handling (assume reject with 409 for same citizen_id+purpose+channel)
- Open question: audit log atomicity (assume same transaction for data integrity)

Primary stack: Go with Clean Architecture (Handler → Usecase → Repository)

Design the API contract (method, path, request/response schemas, status codes), module design (entity, repository interface, usecase interface, file structure), and any ADRs needed.
"""
)
```

**Expected Output:**

## Architect

**Task:** Design API contract and module structure for create consent record endpoint

**API Contract:**

```
Method: POST
Path:   /api/v1/consents
Internal Auth: X-User-ID header injected by internal gateway

Request Body:
{
  "citizen_id": "string (required, 13-digit Thai national ID, regex: ^[0-9]{13}$)",
  "purpose":    "string (required, enum: DATA_PROCESSING | MARKETING | ANALYTICS | THIRD_PARTY_SHARING)",
  "channel":    "string (required, enum: WEB | MOBILE | API | COUNTER)"
}

Response 201 Created:
{
  "id":         "uuid",
  "citizen_id": "string",
  "purpose":    "string",
  "channel":    "string",
  "consented_at": "RFC3339 timestamp",
  "created_at":   "RFC3339 timestamp"
}

Response 400 Bad Request:
{
  "error": {
    "code":    "VALIDATION_ERROR",
    "message": "citizen_id is required and must be 13 digits"
  }
}

Response 409 Conflict:
{
  "error": {
    "code":    "CONSENT_ALREADY_EXISTS",
    "message": "consent record already exists for this citizen_id, purpose, and channel"
  }
}

Response 500 Internal Server Error:
{
  "error": {
    "code":    "INTERNAL_ERROR",
    "message": "an unexpected error occurred"
  }
}
```

**Module Design:**

**Entity: Consent**
```
Fields (private):
- id           UUID
- citizenID    string
- purpose      ConsentPurpose (enum)
- channel      ConsentChannel (enum)
- consentedAt  time.Time
- createdAt    time.Time

Constructor: NewConsent(citizenID, purpose, channel, clock) → (*Consent, error)
  - Validates citizenID format
  - Validates purpose and channel against allowed enums
  - Sets consentedAt and createdAt from clock

Restore: RestoreConsent(id, citizenID, purpose, channel, consentedAt, createdAt) → *Consent
  - Hydrates from DB without validation

Behavior methods:
  - ID() UUID
  - CitizenID() string
  - Purpose() ConsentPurpose
  - Channel() ConsentChannel
  - ConsentedAt() time.Time
  - CreatedAt() time.Time
```

**Entity: AuditLog**
```
Fields (private):
- id          UUID
- entityType  string ("consent")
- entityID    UUID
- action      string ("CREATED")
- performedBy string (from X-User-ID header)
- performedAt time.Time
- metadata    map[string]string

Constructor: NewAuditLog(entityType, entityID, action, performedBy, clock) → *AuditLog
```

**Repository Interface: ConsentRepository**
```
type ConsentRepository interface {
    Create(ctx context.Context, consent *Consent) error
    ExistsByCitizenIDPurposeChannel(ctx context.Context, citizenID string, purpose ConsentPurpose, channel ConsentChannel) (bool, error)
}
```

**Repository Interface: AuditLogRepository**
```
type AuditLogRepository interface {
    Create(ctx context.Context, log *AuditLog) error
}
```

**Usecase Interface: CreateConsentUsecase**
```
type CreateConsentUsecase interface {
    Execute(ctx context.Context, input CreateConsentInput) (*CreateConsentOutput, error)
}

type CreateConsentInput struct {
    CitizenID   string
    Purpose     string
    Channel     string
    PerformedBy string
}

type CreateConsentOutput struct {
    ID          uuid.UUID
    CitizenID   string
    Purpose     string
    Channel     string
    ConsentedAt time.Time
    CreatedAt   time.Time
}
```

**Usecase Flow (CreateConsentUsecase.Execute):**
```
1. Validate input → return validation error if invalid
2. Check duplicate → ConsentRepository.ExistsByCitizenIDPurposeChannel
3. If exists → return ConsentAlreadyExistsError
4. Create Consent entity via NewConsent()
5. Begin transaction
6. ConsentRepository.Create(consent)
7. Create AuditLog entity via NewAuditLog()
8. AuditLogRepository.Create(auditLog)
9. Commit transaction
10. Return CreateConsentOutput
```

**File Structure:**
```
internal/
  consent/
    entity/
      consent.go           # Consent entity + enums
      consent_test.go
      audit_log.go         # AuditLog entity
      audit_log_test.go
    repository/
      consent_repository.go      # ConsentRepository interface
      audit_log_repository.go    # AuditLogRepository interface
    usecase/
      create_consent.go          # CreateConsentUsecase implementation
      create_consent_test.go
    handler/
      create_consent_handler.go  # HTTP handler
      create_consent_handler_test.go
      request.go                 # CreateConsentRequest struct
      response.go                # CreateConsentResponse struct
  infrastructure/
    persistence/
      consent_repository_impl.go
      audit_log_repository_impl.go
```

**ADR: Audit Log Atomicity**
- **Context:** Consent creation requires an audit log. We need to decide whether audit logging is atomic with consent creation or best-effort.
- **Options:** (A) Same DB transaction — audit log and consent in one atomic commit. (B) Separate — consent commits first, audit log written async/best-effort.
- **Decision:** Option A — same transaction. Data integrity is critical for compliance. If audit log fails, the consent record should not be created.
- **Consequences:** Slightly higher latency per request. If audit_log table has issues, consent creation is blocked. Acceptable trade-off for compliance.

**Flags:**
- Security should review: citizen_id is PII — ensure it is not logged in application logs
- Security should review: audit log stores performedBy (internal user ID) — verify access control

---

### Step 3: QA -- Regression Test Doc (Model: sonnet)

**Delegation Call:**
```
Agent(
  description: "QA generates regression test doc with test case IDs for create consent endpoint",
  model: "sonnet",
  prompt: """
---
name: qa
description: Specialist agent for designing test cases, reviewing code quality, validating acceptance criteria, and identifying coverage gaps. Does not write production code.
model: claude-sonnet-4-6
---

# QA Agent

You are a quality assurance specialist. You design test plans, review code quality, validate that acceptance criteria are met, and identify gaps in test coverage. You do not write production code.

## System Context

All systems are **internal-facing**. Test cases should reflect internal user/operator actions and internal service-to-service interactions.

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

# [Service Name] — Regression Test Suite

## Suite Structure
| Suite | Duration | Frequency | # Cases | Coverage |
|-------|----------|-----------|---------|----------|
| Smoke | 10-15 min | Every merge | N | Critical paths |
| Targeted | 30-60 min | Per feature | varies | Affected module |
| Full | 2-4 hours | Weekly/Release | N | Comprehensive |

### Workflow: Doc First, Then E2E Code (CRITICAL)

Regression docs MUST be created BEFORE writing E2E test code.

---
Task: Generate a regression test document with test case IDs for the new "create consent record" endpoint (POST /api/v1/consents).

Prior context from Business Analyst (acceptance criteria):
- Scenario 1: Successful consent creation → 201 with record
- Scenario 2: Missing required fields → 400
- Scenario 3: Invalid citizen_id format → 400
- Scenario 4: Duplicate consent → 409
- Scenario 5: Database failure → 500
- Scenario 6: Audit log is atomic with consent creation

Prior context from Architect:
- POST /api/v1/consents with citizen_id, purpose, channel
- Responses: 201, 400, 409, 500
- Usecase flow: validate → check duplicate → create consent → create audit log (same transaction)
- Entities: Consent, AuditLog

Generate the full regression test doc with structured test case IDs (SM-xxx for smoke, TC-xxx for targeted).
"""
)
```

**Expected Output:**

## QA

**Task:** Regression test document for POST /api/v1/consents (create consent)

### Consent Service -- Regression Test Suite (Create Consent)

**Suite Structure:**

| Suite | Duration | Frequency | # Cases | Coverage |
|-------|----------|-----------|---------|----------|
| Smoke | 5 min | Every merge | 3 | Critical paths |
| Targeted | 20-30 min | Per feature | 15 | Full module |

### 1. SMOKE TESTS (P0)

| ID | Test Case | Method | Path | Expected | Priority |
|----|-----------|--------|------|----------|----------|
| SM-001 | Create consent with valid data | POST | /api/v1/consents | 201 Created | P0 |
| SM-002 | Reject missing required fields | POST | /api/v1/consents | 400 Bad Request | P0 |
| SM-003 | Reject duplicate consent | POST | /api/v1/consents | 409 Conflict | P0 |

### 2. TARGETED REGRESSION -- Create Consent Module

#### 2.1 Happy Path

| ID | Test Case | Preconditions | Steps | Expected | Priority |
|----|-----------|---------------|-------|----------|----------|
| TC-001 | Create consent with all valid fields | No existing record | POST with valid citizen_id, purpose, channel | 201 with consent record including id, consented_at, created_at | P0 |
| TC-002 | Response contains correct fields | None | POST with valid data | Response has id (UUID), citizen_id, purpose, channel, consented_at, created_at | P1 |
| TC-003 | Audit log created in same transaction | None | POST with valid data, query audit_log table | audit_log entry exists with entity_type=consent, action=CREATED | P0 |

#### 2.2 Validation Errors

| ID | Test Case | Preconditions | Steps | Expected | Priority |
|----|-----------|---------------|-------|----------|----------|
| TC-004 | Missing citizen_id | None | POST without citizen_id | 400 VALIDATION_ERROR | P0 |
| TC-005 | Missing purpose | None | POST without purpose | 400 VALIDATION_ERROR | P0 |
| TC-006 | Missing channel | None | POST without channel | 400 VALIDATION_ERROR | P0 |
| TC-007 | Invalid citizen_id format (less than 13 digits) | None | POST with citizen_id="123" | 400 VALIDATION_ERROR | P1 |
| TC-008 | Invalid citizen_id format (letters) | None | POST with citizen_id="abcdefghijklm" | 400 VALIDATION_ERROR | P1 |
| TC-009 | Invalid purpose value | None | POST with purpose="UNKNOWN" | 400 VALIDATION_ERROR | P1 |
| TC-010 | Invalid channel value | None | POST with channel="UNKNOWN" | 400 VALIDATION_ERROR | P1 |
| TC-011 | Empty string fields | None | POST with citizen_id="" | 400 VALIDATION_ERROR | P1 |

#### 2.3 Duplicate Handling

| ID | Test Case | Preconditions | Steps | Expected | Priority |
|----|-----------|---------------|-------|----------|----------|
| TC-012 | Duplicate citizen_id + purpose + channel | Record already exists | POST with same combination | 409 CONSENT_ALREADY_EXISTS | P0 |
| TC-013 | Same citizen_id different purpose | Record exists for purpose A | POST with same citizen_id, different purpose | 201 Created (not duplicate) | P1 |
| TC-014 | Same citizen_id different channel | Record exists for channel A | POST with same citizen_id, same purpose, different channel | 201 Created (not duplicate) | P1 |

#### 2.4 Error Handling

| ID | Test Case | Preconditions | Steps | Expected | Priority |
|----|-----------|---------------|-------|----------|----------|
| TC-015 | Database unavailable | DB connection down | POST with valid data | 500 INTERNAL_ERROR | P1 |

**Coverage Gaps:** None identified -- all BA acceptance criteria have corresponding test cases.

---

### Step 4: Developer + QA (PARALLEL) (Models: sonnet + sonnet)

ขั้นตอนนี้ทำงานแบบ **parallel** -- Developer implement code และ QA เขียน E2E specs พร้อมกัน

#### Step 4a: Developer (Model: sonnet)

**Delegation Call:**
```
Agent(
  description: "Developer implements create consent endpoint with all layers",
  model: "sonnet",
  prompt: """
---
name: developer
description: Specialist agent for implementing features, fixing bugs, refactoring code, and writing unit tests. Operates within Go Clean Architecture (Handler → Usecase → Repository).
model: claude-sonnet-4-6
---

# Developer Agent

You are a senior Go developer specializing in Clean Architecture. You implement features, fix bugs, refactor code, and write unit tests. You do not make architectural or security decisions — escalate those to the Architect or Security agent.

## System Context

All systems are **internal-facing** running on private networks.

## Conventions

**You MUST read and follow the project's CLAUDE.md (or AGENTS.md) before writing any code.**

If no CLAUDE.md exists, ask the Orchestrator to clarify the project's conventions before proceeding.

## Responsibilities

- Implement new features following existing project patterns
- Fix bugs based on root cause analysis from System Analyzer
- Refactor code for readability and maintainability
- Write unit tests with the coverage threshold defined in project conventions
- Run go generate ./... after adding or modifying interfaces

## Escalation Rules

- Architectural decisions → escalate to Architect
- Security concerns → escalate to Security
- Unclear requirements → escalate to Business Analyst via Orchestrator

---
Task: Implement the create consent record endpoint (POST /api/v1/consents) following the Architect's design.

Prior context from Architect:
- POST /api/v1/consents
- Internal Auth: X-User-ID header
- Request: { citizen_id, purpose, channel }
- Response 201: { id, citizen_id, purpose, channel, consented_at, created_at }
- Response 400: validation error, 409: duplicate, 500: internal error

Entity Design:
- Consent: private fields (id, citizenID, purpose, channel, consentedAt, createdAt), NewConsent constructor with validation, RestoreConsent for DB hydration
- AuditLog: private fields (id, entityType, entityID, action, performedBy, performedAt, metadata), NewAuditLog constructor
- ConsentPurpose enum: DATA_PROCESSING, MARKETING, ANALYTICS, THIRD_PARTY_SHARING
- ConsentChannel enum: WEB, MOBILE, API, COUNTER

Repository Interfaces:
- ConsentRepository: Create(ctx, consent), ExistsByCitizenIDPurposeChannel(ctx, citizenID, purpose, channel) (bool, error)
- AuditLogRepository: Create(ctx, log)

Usecase Flow:
1. Validate input
2. Check duplicate via ExistsByCitizenIDPurposeChannel
3. If exists → ConsentAlreadyExistsError
4. NewConsent()
5. Begin transaction
6. ConsentRepository.Create
7. NewAuditLog()
8. AuditLogRepository.Create
9. Commit
10. Return output

File Structure:
- internal/consent/entity/consent.go, audit_log.go
- internal/consent/repository/consent_repository.go, audit_log_repository.go
- internal/consent/usecase/create_consent.go
- internal/consent/handler/create_consent_handler.go, request.go, response.go
- internal/infrastructure/persistence/consent_repository_impl.go, audit_log_repository_impl.go

Implement all layers with unit tests. Follow Go Clean Architecture patterns. Use parameterized SQL queries. Use testable clock for time.
"""
)
```

#### Step 4b: QA -- E2E Specs (Model: sonnet)

**Delegation Call (runs in PARALLEL with Step 4a):**
```
Agent(
  description: "QA writes E2E test specs based on regression test doc",
  model: "sonnet",
  prompt: """
---
name: qa
description: Specialist agent for designing test cases, reviewing code quality, validating acceptance criteria, and identifying coverage gaps. Does not write production code.
model: claude-sonnet-4-6
---

# QA Agent

You are a quality assurance specialist. You design test plans, review code quality, validate that acceptance criteria are met, and identify gaps in test coverage. You do not write production code.

## System Context

All systems are **internal-facing**.

## Workflow: Doc First, Then E2E Code (CRITICAL)

Regression docs MUST be created BEFORE writing E2E test code. The regression doc was created in Step 3.

---
Task: Write E2E test specs for the create consent endpoint (POST /api/v1/consents) based on the regression test document.

Test Case IDs from regression doc:
- SM-001: Create consent with valid data → 201
- SM-002: Reject missing required fields → 400
- SM-003: Reject duplicate consent → 409
- TC-001 to TC-015: Full targeted regression cases

Prior context from Architect:
- POST /api/v1/consents
- Request: { citizen_id, purpose, channel }
- Response 201: { id, citizen_id, purpose, channel, consented_at, created_at }
- Response 400: { error: { code: "VALIDATION_ERROR", message } }
- Response 409: { error: { code: "CONSENT_ALREADY_EXISTS", message } }
- Response 500: { error: { code: "INTERNAL_ERROR", message } }

Write E2E test specs referencing the test case IDs. Follow the project's E2E testing conventions if CLAUDE.md defines them. Each test should reference its test case ID from the regression doc.
"""
)
```

---

### Step 5: Code Reviewer + Security (PARALLEL) (Models: sonnet + sonnet)

ขั้นตอนนี้ทำงานแบบ **parallel** -- Code Reviewer ตรวจ conventions และ Security ตรวจความปลอดภัย

#### Step 5a: Code Reviewer (Model: sonnet)

**Delegation Call:**
```
Agent(
  description: "Code Reviewer checks convention compliance for create consent implementation",
  model: "sonnet",
  prompt: """
---
name: code-reviewer
description: Specialist agent for reviewing code compliance with project conventions before merge. Read-only — produces findings, does not modify code.
model: claude-sonnet-4-6
tools: ["Read", "Glob", "Grep", "Bash"]
---

# Code Reviewer Agent

You are a code review specialist. You verify that code follows all project conventions before merge. You do not modify code — you produce findings and flag violations.

## System Context

All systems are **internal-facing**.

## Conventions

**You MUST read the project's CLAUDE.md (or AGENTS.md) first.** That file defines all rules you check against.

**Scope Boundary:** You check convention compliance — correct patterns, naming, structure, and style. You do NOT assess security exploitability — that belongs to the Security agent.

Review every changed file against the project's conventions. Common categories to check:
1. Entity Design — field visibility, constructors, restore functions, behavior methods
2. Time Usage — testable time utility vs time.Now()
3. Error Handling — semantic error functions, error wrapping, error matching
4. Transaction Patterns — WithTransaction usage, defer rollback, commit ordering
5. Handler Patterns — request/response structs, error mapping, business logic leakage
6. Usecase Patterns — file organization, step comments, error types
7. Naming Conventions — interfaces, constructors, list methods, transaction methods
8. Test Quality — mock aliases, time mocking, panic recovery, coverage
9. Repository Patterns — not-found handling, parameterized queries, restore usage

## Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| Blocker | Will cause bugs or data corruption | Must fix before merge |
| Critical | Breaks project standards | Must fix before merge |
| Warning | Minor convention deviation | Should fix, can merge with follow-up |
| Info | Suggestion for improvement | Optional |

---
Task: Review the Developer's implementation of the create consent endpoint (POST /api/v1/consents) for convention compliance.

Files to review:
- internal/consent/entity/consent.go, audit_log.go
- internal/consent/repository/consent_repository.go, audit_log_repository.go
- internal/consent/usecase/create_consent.go
- internal/consent/handler/create_consent_handler.go, request.go, response.go
- internal/infrastructure/persistence/consent_repository_impl.go, audit_log_repository_impl.go
- All corresponding _test.go files

Check all 9 convention categories. Read the project's CLAUDE.md first. Report findings with severity levels.

Prior context: Developer output from Step 4a (would include full implementation code here).
"""
)
```

#### Step 5b: Security (Model: sonnet)

**Delegation Call (runs in PARALLEL with Step 5a):**
```
Agent(
  description: "Security reviews create consent implementation for vulnerabilities",
  model: "sonnet",
  prompt: """
---
name: security
description: Specialist agent for internal system security review, vulnerability assessment, secrets detection, and access control.
model: claude-sonnet-4-6
tools: ["Read", "Glob", "Grep", "Bash"]
---

# Security Agent

You are a security specialist for internal systems. Your projects run inside private/internal networks and are not exposed to the public internet. Focus on risks that are real in internal environments: injection, access control, secrets in code, auth between services, and sensitive data leakage in logs.

**Scope Boundary:** You assess security exploitability and risk — injection, access control, secrets, data exposure. You do NOT check convention compliance.

## Responsibilities

- SQL injection and input injection review
- Access control — who can access what data between services/users
- Secrets and credential detection in code and config
- Authentication and authorization between internal services
- Sensitive data exposure in logs (PII, personal data)
- Input validation for internal APIs
- Business rule enforcement (server-side, not bypassable)

## Internal Security Checklist

- [ ] Injection — Are all DB queries parameterized? No string concatenation in SQL?
- [ ] Access Control — Is data scoped correctly? Can user A access user B's data?
- [ ] Secrets in Code — No hardcoded passwords, API keys, tokens?
- [ ] Auth Between Services — Are internal service tokens/headers validated properly?
- [ ] Sensitive Data in Logs — No PII (citizen ID, name, phone) printed in logs?
- [ ] Input Validation — Are inputs validated before hitting business logic?
- [ ] Business Rule Enforcement — Are rules enforced server-side?
- [ ] Data Integrity — Are deserialized/bound inputs validated before use?

---
Task: Security review of the create consent endpoint (POST /api/v1/consents).

Key security concerns flagged by Architect:
1. citizen_id is PII — ensure it is not logged in application logs
2. audit log stores performedBy (internal user ID) — verify access control
3. SQL queries must be parameterized

Implementation details:
- Accepts citizen_id (13-digit Thai national ID), purpose, channel
- Saves consent record + audit log in same transaction
- Auth: X-User-ID header from internal gateway
- citizen_id is PII and must be treated as sensitive data

Review for: SQL injection, PII in logs, access control, input validation, secrets, auth header validation.

Prior context: Developer output from Step 4a (would include full implementation code here).
"""
)
```

---

## Summary

**Task:** เพิ่ม endpoint สำหรับ create consent record ใน consent service โดยต้องรับ citizen_id, purpose, channel แล้ว save ลง DB พร้อม audit log

**Workflow:** New Feature

**Agents Used:**

| Step | Agent | Model | Status | Execution |
|------|-------|-------|--------|-----------|
| 1 | Business Analyst | haiku | Delegated | Sequential |
| 2 | Architect | opus | Delegated | Sequential (depends on Step 1) |
| 3 | QA (Test Doc) | sonnet | Delegated | Sequential (depends on Step 2) |
| 4a | Developer | sonnet | Delegated | Parallel with 4b |
| 4b | QA (E2E Specs) | sonnet | Delegated | Parallel with 4a |
| 5a | Code Reviewer | sonnet | Delegated | Parallel with 5b |
| 5b | Security | sonnet | Delegated | Parallel with 5a |

---

### Assembled Output Summary

1. **Business Analyst** -- กำหนด user story, acceptance criteria 6 scenarios (happy path, missing fields, invalid format, duplicate, DB failure, audit atomicity), business rules 5 ข้อ, edge cases 6 รายการ, open questions 4 ข้อ

2. **Architect** -- ออกแบบ API contract (POST /api/v1/consents), module design ครบทุก layer (Entity, Repository Interface, Usecase Interface, Handler), file structure, และ ADR สำหรับ audit log atomicity (เลือก same transaction)

3. **QA (Regression Doc)** -- สร้าง regression test doc มี smoke tests 3 cases (SM-001 ถึง SM-003) และ targeted regression 15 cases (TC-001 ถึง TC-015) ครอบคลุม happy path, validation errors, duplicate handling, error handling

4. **Developer** (parallel) -- implement ทุก layer ตาม Architect design: entities (Consent + AuditLog), repository interfaces + implementations, usecase (CreateConsentUsecase), handler, พร้อม unit tests

5. **QA E2E** (parallel) -- เขียน E2E test specs อ้างอิง test case IDs จาก regression doc

6. **Code Reviewer** (parallel) -- ตรวจ convention compliance ทุกไฟล์ที่ Developer สร้าง (9 categories)

7. **Security** (parallel) -- ตรวจ SQL injection, PII in logs (citizen_id), access control, input validation, auth header validation

---

**Next Steps:**
1. ตอบ Open Questions จาก Business Analyst (duplicate handling policy, valid values for purpose/channel, citizen_id format)
2. ตรวจสอบว่าโปรเจกต์มี CLAUDE.md หรือไม่ -- ถ้ามี ต้อง re-run Developer และ Code Reviewer ให้ align กับ project conventions
3. แก้ไข findings จาก Code Reviewer และ Security ก่อน merge
4. รัน test suite ทั้งหมด (unit + E2E) ให้ผ่าน
5. QA sign-off หลัง findings ทั้งหมดได้รับการแก้ไข
