# Neo Team Orchestration Output

## User Request

> "review code ใน internal/domain/consent/ ก่อน merge เข้า main ดูทั้ง convention, security, และ test coverage"

---

## Step 0: Task Classification

**Task Type:** Code Review

User ขอให้ review code ใน `internal/domain/consent/` ก่อน merge เข้า main โดยครอบคลุม convention, security, และ test coverage ตรงกับ workflow **Code Review** พอดี

**Selected Workflow: Code Review**

```
1. code-reviewer       → check convention compliance
2. developer + security + qa → review correctness, security, coverage (PARALLEL)
```

**Agents Used:** Code Reviewer (sonnet), Developer (sonnet), Security (sonnet), QA (sonnet)

---

## Step 1: Code Reviewer — Check Convention Compliance

### Delegation

ก่อนอื่น orchestrator ต้อง read reference file ของ code-reviewer แล้วส่งเข้า Agent tool

```
# Orchestrator reads reference file first
Read("references/code-reviewer.md")

# Then delegates
Agent(
  description: "Code Reviewer checks convention compliance for internal/domain/consent/",
  model: "sonnet",
  prompt: """
[Full content of references/code-reviewer.md]

---
Task: Review all code in `internal/domain/consent/` for convention compliance before merge to main.

Instructions:
1. Read the project's CLAUDE.md first to understand project conventions
2. Scan all files in internal/domain/consent/ (entities, usecases, repositories, handlers)
3. Check against all convention categories: entity design, time usage, error handling,
   transaction patterns, handler patterns, usecase patterns, naming conventions,
   test quality, repository patterns
4. Report findings with severity levels (Blocker / Critical / Warning / Info)
5. Produce verdict: Approved or Changes Required
"""
)
```

### Simulated Output from Code Reviewer

```
## Code Reviewer

**Task:** Convention compliance review for internal/domain/consent/
**Files Reviewed:** 12

### Findings

#### [CRITICAL] Entity uses public fields instead of private with getters
- **File:** internal/domain/consent/entity/consent.go:15-22
- **Issue:** Struct fields `UserID`, `Purpose`, `Status` are exported directly.
  Convention requires private fields with getter methods and constructor/restore functions.
- **Fix:** Make fields unexported, add NewConsent() constructor, RestoreConsent() function,
  and getter methods.

#### [CRITICAL] Direct time.Now() usage in usecase
- **File:** internal/domain/consent/usecase/grant_consent.go:45
- **Issue:** Uses `time.Now()` directly instead of the project's clock utility.
  This makes time-dependent logic untestable.
- **Fix:** Inject clock dependency via constructor, use `clock.Now()` instead.

#### [WARNING] Missing step comments in usecase
- **File:** internal/domain/consent/usecase/grant_consent.go:30-60
- **Issue:** Usecase method lacks numbered step comments (// Step 1: ..., // Step 2: ...).
- **Fix:** Add step comments per usecase convention.

#### [WARNING] Import order not following convention
- **File:** internal/domain/consent/handler/consent_handler.go:3-12
- **Issue:** Third-party imports mixed with standard library imports.
  Convention: stdlib → third-party → internal (separated by blank lines).
- **Fix:** Re-order imports into three groups.

#### [INFO] Mock alias naming
- **File:** internal/domain/consent/usecase/grant_consent_test.go:10
- **Issue:** Mock import uses `mockRepo` alias. Convention prefers `consentRepoMock`.
- **Fix:** Rename import alias to match convention pattern.

---

**Summary:**
| Severity | Count |
|----------|-------|
| Blocker  | 0     |
| Critical | 2     |
| Warning  | 2     |
| Info     | 1     |

**Verdict:** Changes Required (reason: 2 Critical findings — public entity fields, direct time.Now())
```

---

## Step 2: Developer + Security + QA — PARALLEL

Step 2 ทำงาน 3 agent พร้อมกัน เพราะไม่มี dependency ระหว่างกัน Orchestrator ส่ง Agent() call ทั้ง 3 ตัวในคราวเดียว พร้อมส่ง output จาก Code Reviewer เป็น context ให้ทุกตัว

### 2A: Developer — Review Correctness

```
# Orchestrator reads reference file first
Read("references/developer.md")

# Then delegates
Agent(
  description: "Developer reviews code correctness in internal/domain/consent/",
  model: "sonnet",
  prompt: """
[Full content of references/developer.md]

---
Task: Review code correctness in `internal/domain/consent/` before merge to main.
This is a review-only task — do not implement changes, only report findings.

Prior context from Code Reviewer:
- CRITICAL: Entity uses public fields (consent.go:15-22)
- CRITICAL: Direct time.Now() usage (grant_consent.go:45)
- WARNING: Missing step comments, import order
- INFO: Mock alias naming

Instructions:
1. Read the project's CLAUDE.md first
2. Review all implementation files for correctness:
   - Entity logic (consent.go) — constructors, state transitions, validation
   - Usecase logic (grant_consent.go, revoke_consent.go) — business flow, error handling
   - Repository implementation — query correctness, transaction usage
   - Handler — request binding, response mapping, error mapping
3. Check that business logic is in the correct layer (not leaking to handler/repo)
4. Verify error handling patterns are correct
5. Report any correctness issues found
"""
)
```

#### Simulated Output from Developer

```
## Developer

**Task:** Code correctness review for internal/domain/consent/

**Changes:** (review-only, no changes made)

**Findings:**
- internal/domain/consent/usecase/grant_consent.go:52 — Error from repository is returned
  unwrapped. Should use `apperror.Wrap(err, "grant consent failed")` per convention.
- internal/domain/consent/usecase/revoke_consent.go:38 — Missing nil check on fetched entity
  before calling method. If consent not found, this will panic.
- internal/domain/consent/repository/consent_repo.go:67 — Transaction commit is called before
  all operations complete. The audit log insert at line 70 runs outside the transaction.
- internal/domain/consent/handler/consent_handler.go:28 — Handler contains business validation
  logic (checking consent expiry). This should be in the usecase or entity layer.

**Notes:**
- The transaction ordering issue (repo:67) is a potential data integrity bug —
  QA and Security should be aware.
- The nil pointer risk (revoke usecase:38) should have a test case for "consent not found".
```

### 2B: Security — Security Review

```
# Orchestrator reads reference file first
Read("references/security.md")

# Then delegates
Agent(
  description: "Security reviews internal/domain/consent/ for vulnerabilities",
  model: "sonnet",
  prompt: """
[Full content of references/security.md]

---
Task: Security review of `internal/domain/consent/` before merge to main.

Prior context from Code Reviewer:
- CRITICAL: Entity uses public fields (consent.go:15-22)
- CRITICAL: Direct time.Now() usage (grant_consent.go:45)

Instructions:
1. Scan all files in internal/domain/consent/ using the Internal Security Checklist
2. Check for: SQL injection, access control, secrets in code, auth between services,
   sensitive data in logs, input validation, business rule enforcement, data integrity
3. Pay special attention to consent data — it may contain PII references
4. Report findings with severity levels (Critical / High / Medium / Low)
5. Provide merge recommendation
"""
)
```

#### Simulated Output from Security (contains HIGH finding — PII in logs)

```
## Security

**Task:** Security review of internal/domain/consent/

**Findings:**

### [HIGH] PII Leaked in Log Statements
- **Location:** internal/domain/consent/usecase/grant_consent.go:48
- **Description:** Log statement includes user's CitizenID and FullName in plain text:
  `logger.Info("granting consent", "citizenID", req.CitizenID, "name", req.FullName)`
  This exposes PII in application logs accessible to operations staff.
- **Risk:** Internal operators with log access can view personal data without
  authorization. Violates data minimization principle for consent processing.
- **Remediation:** Remove PII fields from log statements. Use only non-identifying
  references: `logger.Info("granting consent", "userID", req.UserID, "consentType", req.Purpose)`

### [MEDIUM] Missing Input Validation on Consent Purpose
- **Location:** internal/domain/consent/handler/consent_handler.go:22
- **Description:** The `Purpose` field from request body is passed directly to the usecase
  without validation against an allowed list. An internal user could submit arbitrary
  purpose strings.
- **Risk:** Could lead to inconsistent consent records or bypass consent type restrictions
  enforced elsewhere.
- **Remediation:** Validate Purpose against an enum/allowed list at the handler or entity level.

### [LOW] Access Control — No Ownership Check on Revoke
- **Location:** internal/domain/consent/usecase/revoke_consent.go:25
- **Description:** Revoke endpoint does not verify that the requesting user owns the
  consent record. Any authenticated internal user could revoke another user's consent.
- **Risk:** Low in internal context but could cause data integrity issues if
  misused by operators.
- **Remediation:** Add ownership validation — compare requesting user ID with
  consent's owner ID before allowing revoke.

---

**Summary:**
| Severity | Count |
|----------|-------|
| Critical | 0     |
| High     | 1     |
| Medium   | 1     |
| Low      | 1     |

**Merge Recommendation:** Blocked (reason: 1 High finding — PII in logs must be fixed before merge)
```

### 2C: QA — Test Coverage Review

```
# Orchestrator reads reference file first
Read("references/qa.md")

# Then delegates
Agent(
  description: "QA reviews test coverage for internal/domain/consent/",
  model: "sonnet",
  prompt: """
[Full content of references/qa.md]

---
Task: Review test coverage for `internal/domain/consent/` before merge to main.

Prior context from Code Reviewer:
- CRITICAL: Entity uses public fields (consent.go:15-22)
- CRITICAL: Direct time.Now() usage — makes time-dependent tests unreliable
- INFO: Mock alias naming inconsistency

Prior context from Developer:
- Missing nil check on fetched entity in revoke_consent.go:38 (panic risk)
- Transaction commit ordering issue in consent_repo.go:67

Instructions:
1. Read the project's CLAUDE.md first to understand test conventions
2. Review all test files in internal/domain/consent/
3. Check coverage against the Test Coverage Checklist:
   - Happy path, not found, validation error, infra error, panic recovery, edge cases
4. Identify gaps — especially for the nil pointer risk and transaction issue flagged by Developer
5. Provide coverage estimate and sign-off decision
"""
)
```

#### Simulated Output from QA

```
## QA

**Task:** Test coverage review for internal/domain/consent/

**Test Plan:**
| # | Test Case | Type | Expected Result | Status |
|---|-----------|------|-----------------|--------|
| 1 | Grant consent — happy path | Unit | Consent created, status=active | Pass |
| 2 | Grant consent — duplicate | Unit | Return error (already exists) | Pass |
| 3 | Grant consent — invalid purpose | Unit | Return validation error | Missing |
| 4 | Grant consent — DB failure | Unit | Return infrastructure error | Pass |
| 5 | Revoke consent — happy path | Unit | Status changed to revoked | Pass |
| 6 | Revoke consent — not found | Unit | Return not-found error | Missing |
| 7 | Revoke consent — already revoked | Unit | Return conflict error | Missing |
| 8 | Handler — panic recovery | Unit | Returns 500, no crash | Missing |
| 9 | Repository — transaction rollback on failure | Unit | Rollback called, no partial commit | Missing |
| 10 | Entity — time-dependent consent expiry | Unit | Correct expiry check with mocked time | Missing |

**Coverage Report:**
- Modified packages: consent/entity, consent/usecase, consent/repository, consent/handler
- Estimated coverage: ~45% (usecase has tests, entity/handler/repo mostly untested)
- Gaps identified:
  - No test for "consent not found" in revoke flow (risk: nil pointer panic per Developer finding)
  - No test for transaction rollback behavior
  - No panic recovery test in handler
  - No time-mocked tests (blocked by direct time.Now() usage per Code Reviewer finding)
  - No test for invalid consent purpose (security-relevant per Security finding)

**Acceptance Criteria Validation:**
- Grant consent flow: Partial (happy path only)
- Revoke consent flow: Partial (happy path only)
- Error handling: Not Tested
- Consent expiry logic: Not Tested

**Sign-Off:** Blocked (reason: Coverage ~45%, missing critical test cases for not-found, transaction, and panic recovery paths. 6 of 10 required test cases are missing.)
```

---

## Handling Security HIGH Finding: PII in Logs

### Analysis of Skill's Guidance

Skill file ไม่ได้มี explicit step สำหรับ "หลังจากพบ Security HIGH finding ให้ทำอะไรต่อ" โดยเฉพาะ สิ่งที่ skill กำหนดไว้มีเพียง:

1. **Security reference file** บอกว่า: "Do not approve merge if Critical or High findings are unresolved" — คือ block merge
2. **Agent Failure Handling** table — จัดการกรณี agent failure แต่ไม่ใช่กรณี finding ที่ต้อง remediate
3. **Delegation Rules** บอกว่า: "Never let Developer make security decisions alone — route to Security"
4. **Workflow definition** — Code Review workflow มีแค่ 2 steps จบ ไม่มี step 3 สำหรับ remediation

### Gap ที่พบ

**Skill ไม่มี remediation loop** — เมื่อ Security พบ High finding ที่ block merge, skill ไม่ได้บอกว่า orchestrator ควร:
- (a) Delegate ให้ Developer แก้ไขแล้ววน review อีกรอบ?
- (b) แค่รายงาน finding แล้วจบ pipeline ให้ user ไปจัดการเอง?
- (c) เปิด workflow ใหม่ (เช่น Bug Fix หรือ Security Audit) สำหรับ remediation?

### สิ่งที่ Orchestrator จะทำ (ad-hoc decision)

เนื่องจาก skill ไม่มี explicit guidance สำหรับ remediation loop ใน Code Review workflow, orchestrator จะ:

1. **รายงาน finding ทั้งหมดตามที่ pipeline กำหนด** (workflow จบที่ step 2)
2. **ระบุใน Summary ว่า merge ถูก block** พร้อมเหตุผล
3. **แนะนำ Next Steps** ให้ user — ซึ่งอาจเป็นการ run pipeline ใหม่หลัง fix
4. **Flag gap นี้** เพื่อให้ improve skill ในอนาคต

> **Note for skill improvement:** Code Review workflow ควรมี optional step 3 แบบ conditional:
> "If Security or Code Reviewer blocks merge → delegate to Developer to fix → re-run blocking agents to verify"
> เพื่อให้ pipeline สามารถ loop จนผ่านได้โดยไม่ต้องให้ user เริ่มใหม่

---

## Summary

**Task:** Review code in `internal/domain/consent/` before merge to main — convention, security, and test coverage

**Workflow:** Code Review

**Agents Used:** Code Reviewer (sonnet), Developer (sonnet), Security (sonnet), QA (sonnet)

---

### Code Reviewer — Convention Compliance

| Severity | Count |
|----------|-------|
| Blocker  | 0     |
| Critical | 2     |
| Warning  | 2     |
| Info     | 1     |

**Key Findings:**
- [CRITICAL] Entity uses public fields — must use private fields + getters + constructor/restore
- [CRITICAL] Direct `time.Now()` — must use clock utility for testability
- [WARNING] Missing step comments in usecase
- [WARNING] Import ordering

**Verdict:** Changes Required

### Developer — Correctness Review

**Key Findings:**
- Unwrapped error in grant_consent usecase
- Nil pointer risk in revoke_consent (missing not-found check)
- Transaction commit ordering bug — audit log runs outside transaction
- Business logic leaking into handler layer

### Security — Security Review

| Severity | Count |
|----------|-------|
| Critical | 0     |
| High     | 1     |
| Medium   | 1     |
| Low      | 1     |

**Key Findings:**
- [HIGH] PII (CitizenID, FullName) leaked in log statements — must remove before merge
- [MEDIUM] No input validation on consent Purpose field
- [LOW] No ownership check on revoke endpoint

**Merge Recommendation:** Blocked

### QA — Test Coverage Review

| Metric | Value |
|--------|-------|
| Estimated Coverage | ~45% |
| Test Cases Required | 10 |
| Test Cases Passing | 4 |
| Test Cases Missing | 6 |

**Key Gaps:**
- No test for "consent not found" path (nil pointer panic risk)
- No transaction rollback test
- No panic recovery test in handler
- No time-mocked tests (blocked by `time.Now()` usage)
- No validation error test

**Sign-Off:** Blocked

---

### Overall Merge Decision

> **BLOCKED** — Merge ไม่สามารถทำได้จนกว่าจะแก้ไข issues ต่อไปนี้

**Must fix before merge:**

| # | Source | Severity | Issue |
|---|--------|----------|-------|
| 1 | Code Reviewer | Critical | Entity public fields — refactor to private + getters |
| 2 | Code Reviewer | Critical | Direct time.Now() — replace with clock utility |
| 3 | Security | High | PII in logs — remove CitizenID/FullName from log statements |
| 4 | Developer | High | Transaction commit ordering — move commit after audit log |
| 5 | Developer | High | Nil pointer risk — add not-found check in revoke usecase |
| 6 | QA | Blocker | Test coverage ~45% — add 6 missing test cases |

**Should fix (can merge with follow-up):**

| # | Source | Severity | Issue |
|---|--------|----------|-------|
| 7 | Security | Medium | Input validation on Purpose field |
| 8 | Code Reviewer | Warning | Missing step comments in usecase |
| 9 | Code Reviewer | Warning | Import ordering |
| 10 | Security | Low | Ownership check on revoke |

---

### Next Steps

1. **Developer** แก้ไข 6 must-fix items (entity refactor, clock, PII logs, transaction, nil check, tests)
2. **Re-run Code Review workflow** หลังแก้ไขเสร็จ เพื่อ verify ว่าผ่านทุก agent
3. **QA** เขียน test cases ที่ขาดหาย (6 cases) ให้ coverage ขึ้นถึง threshold
4. **Security** verify ว่า PII ถูกลบออกจาก logs แล้ว

---

### Skill Gap Identified

**Remediation Loop Missing:** Code Review workflow ไม่มี mechanism สำหรับ auto-remediation เมื่อพบ blocking findings ปัจจุบัน pipeline จบที่ step 2 แล้วรายงานผล — user ต้อง manually trigger review อีกรอบหลัง fix

**Recommendation for skill improvement:** เพิ่ม conditional step 3:
```
3. IF any agent blocks merge:
   → developer    → implement fixes for all blocking findings
   → re-run blocking agents (code-reviewer / security / qa) to verify
   → repeat until all agents approve or max 2 iterations
```
