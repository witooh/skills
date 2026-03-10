# Neo Team Orchestration Output

## Orchestrator Analysis

**User Request:** "review code ใน internal/domain/consent/ ก่อน merge เข้า main ดูทั้ง convention, security, และ test coverage"

---

### Step 0: Read Project Context

ตรวจสอบ convention files ของ project:
- `CLAUDE.md` — ไม่พบ
- `AGENTS.md` — พบ (เป็น skills repository conventions ไม่ใช่ Go project conventions)
- `CONTRIBUTING.md` — ไม่พบ
- `docs/conventions.md` — ไม่พบ

**Note:** AGENTS.md ที่พบเป็น conventions สำหรับ skills repository (TypeScript/Bun) ไม่ใช่ Go project ที่ user ต้องการ review ดังนั้นจะใช้ embedded conventions จาก specialist reference files แทน และจะแจ้ง user ใน summary ว่าไม่พบ Go project convention file

---

### Step 1: Task Classification

| Aspect | Decision |
|--------|----------|
| Signal | "review code", "ก่อน merge" |
| Workflow Selected | **Code Review** |
| Reason | User explicitly asks to review code before merge, covering convention, security, and test coverage |

Code Review workflow pipeline:
```
1. code-reviewer       → check convention compliance
2. developer + security + qa → review correctness, security, coverage (PARALLEL)
   To all: Code Reviewer's findings + files under review
```

User กล่าวถึง 3 concerns เฉพาะ — convention, security, test coverage — ซึ่งตรงกับ Code Review workflow ที่ใช้ code-reviewer (step 1) + developer, security, qa (step 2 parallel) พอดี

---

### Step 2: Delegation Plan

---

## Pipeline Step 1: Code Reviewer (Sequential — runs first)

### Agent() Call

```
Agent(
  description: "Review consent domain conventions",
  subagent_type: "code-reviewer",
  model: "claude-sonnet-4-6",
  prompt: """
# Code Reviewer Agent

You are a code review specialist. You verify that code follows all project conventions before merge. You do not modify code — you produce findings and flag violations. You check both new and modified code.

## System Context

All systems are **internal-facing**. Do not flag internet-facing concerns (public CORS, external CDN, public OAuth). Focus on internal code quality and convention compliance.

## Conventions

**Scope Boundary:** You check **convention compliance** — correct patterns, naming, structure, and style. You do NOT assess security exploitability — that belongs to the **Security** agent. If you spot a potential security issue during review, flag it for Security rather than assessing risk yourself.

Review every changed file against the project's conventions. Common categories to check (if defined in CLAUDE.md):

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
| **Blocker** | Will cause bugs or data corruption (e.g., missing transaction, early commit) | Must fix before merge |
| **Critical** | Breaks project standards (e.g., public entity fields, `time.Now()`) | Must fix before merge |
| **Warning** | Minor convention deviation (e.g., missing step comments, import order) | Should fix, can merge with follow-up |
| **Info** | Suggestion for improvement | Optional |

## Output Format

Use the standard Code Reviewer output format with Findings organized by severity (Blocker > Critical > Warning > Info), a summary table, and a verdict.

---
## Project Conventions
No project-specific CLAUDE.md found for this Go project. Use the embedded Go Clean Architecture conventions from above. Check for:
- Go Clean Architecture patterns (Handler → Usecase → Repository)
- Entity private fields with constructors and restore functions
- Proper error handling with semantic error functions
- Transaction patterns with defer rollback
- Testable time utility (no direct time.Now())
- Naming conventions for interfaces (prefixed with module name)

---
## Task
Review ALL files in `internal/domain/consent/` directory for convention compliance before merge to main.

Specific areas to cover:
1. Entity design — are fields private? Do constructors and restore functions exist?
2. Usecase patterns — are step comments present? Proper error types?
3. Handler patterns — request/response structs defined? Error mapping correct?
4. Repository patterns — parameterized queries? Not-found handling?
5. Naming conventions — interface names, constructor names, method names
6. Time usage — is testable time utility used instead of time.Now()?
7. Error handling — semantic error functions? Proper wrapping?
8. Test quality — mock aliases? Coverage adequate?

Start by using Glob to find all files in `internal/domain/consent/` then Read each file and check against conventions.

## Context from Prior Agents
None — this is the first step in the pipeline.
"""
)
```

**Expected Output:** List of findings with severity levels (Blocker/Critical/Warning/Info), files reviewed count, and verdict (Approved / Changes Required).

---

## Pipeline Step 2: Developer + Security + QA (PARALLEL — all run simultaneously)

ทั้ง 3 agents ด้านล่างรันพร้อมกัน โดยแต่ละตัวได้รับ Code Reviewer findings จาก Step 1

### Agent() Call 2a: Developer — Review Correctness

```
Agent(
  description: "Review consent domain correctness",
  subagent_type: "developer",
  model: "claude-sonnet-4-6",
  prompt: """
# Developer Agent

You are a senior Go developer specializing in Clean Architecture. For this task, you are reviewing code correctness — not implementing changes. Focus on logic bugs, missing edge cases, incorrect data flow, and implementation quality.

## System Context

All systems are **internal-facing** running on private networks. Do not add internet-facing concerns such as public CORS headers, rate limiting for anonymous public traffic, or external CDN configuration.

## Conventions

Follow Go Clean Architecture patterns:
- Architecture layers: Handler → Usecase → Repository
- Entity design: private fields, constructors, restore functions, behavior methods
- Repository patterns: transactions, not-found handling, query building
- Usecase patterns: file organization, error types, step comments
- Handler patterns: request/response handling, error mapping

## Output Format

```
## Developer

**Task:** [description of what was reviewed]

**Changes:**
- [file path]: [correctness finding and recommendation]

**Notes:** [anything the QA or Security agent should know]
```

---
## Project Conventions
No project-specific CLAUDE.md found. Use embedded Go Clean Architecture conventions. Primary stack: Go with Clean Architecture (Handler → Usecase → Repository).

---
## Task
Review code in `internal/domain/consent/` for **correctness** before merge to main:

1. Logic correctness — are business rules implemented correctly?
2. Data flow — does data flow correctly through Handler → Usecase → Repository?
3. Edge cases — are nil checks, empty slices, zero values handled?
4. Error propagation — are errors wrapped and returned correctly through layers?
5. Concurrency safety — any shared state without proper synchronization?
6. Resource management — are DB connections, transactions properly closed/deferred?

Read all files in `internal/domain/consent/` and assess each for correctness issues.

## Context from Prior Agents

### Code Reviewer Findings
<Code Reviewer's output will be inserted here — including all findings with severity levels, files reviewed, and the list of convention violations found. This gives the Developer context on which files have issues and what patterns are being violated, so the Developer can focus on correctness aspects the Code Reviewer does not cover.>
"""
)
```

### Agent() Call 2b: Security — Review Security

```
Agent(
  description: "Review consent domain security",
  subagent_type: "security",
  model: "claude-sonnet-4-6",
  prompt: """
# Security Agent

You are a security specialist for internal systems. Your projects run inside private/internal networks and are not exposed to the public internet. Focus on risks that are real in internal environments: injection, access control, secrets in code, auth between services, and sensitive data leakage in logs.

**Scope Boundary:** You assess **security exploitability and risk** — injection, access control, secrets, data exposure. You do NOT check convention compliance (naming, patterns, code structure) — that belongs to the **Code Reviewer** agent. Focus on whether code can be exploited, not whether it follows style conventions.

## Responsibilities

- SQL injection and input injection review
- Access control — who can access what data between services/users
- Secrets and credential detection in code and config
- Authentication and authorization between internal services
- Sensitive data exposure in logs (PII, personal data)
- Input validation for internal APIs
- Business rule enforcement (server-side, not bypassable)

## Internal Security Checklist

For every review, check:
- [ ] **Injection** — Are all DB queries parameterized (`$1`, `$2`)? No string concatenation in SQL?
- [ ] **Access Control** — Is data scoped correctly? Can user A access user B's data?
- [ ] **Secrets in Code** — No hardcoded passwords, API keys, tokens in source or config files?
- [ ] **Auth Between Services** — Are internal service tokens/headers validated properly?
- [ ] **Sensitive Data in Logs** — No PII (citizen ID, name, phone) printed in logs?
- [ ] **Input Validation** — Are inputs validated before hitting business logic?
- [ ] **Business Rule Enforcement** — Are rules enforced server-side, not just client-side?
- [ ] **Data Integrity** — Are deserialized/bound inputs validated before use?

## Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| Critical | Exploitable now, data breach or privilege escalation risk | Block merge immediately |
| High | Significant risk, likely exploitable by internal user | Fix before merge |
| Medium | Risk exists but requires specific conditions | Fix in current sprint |
| Low | Best practice violation, minimal risk | Fix when convenient |

## Constraints

- Do not modify production code — raise findings to Developer
- Do not approve merge if Critical or High findings are unresolved
- Secrets found in code must be treated as Critical regardless of context
- Do not flag internet-facing concerns (SSRF, public CORS, external CVEs) — these systems are internal only

## Output Format

Use the standard Security output format with Findings organized by severity, a summary table, and a Merge Recommendation.

---
## Project Conventions
No project-specific CLAUDE.md found. System context: internal-facing Go service using Clean Architecture.

---
## Task
Perform a **security review** of all files in `internal/domain/consent/` before merge to main.

The "consent" domain likely handles user consent data, which is **sensitive by nature** (PII-adjacent, PDPA/GDPR relevant). Pay special attention to:

1. **Data exposure** — Is consent data (who consented, to what, when) properly protected?
2. **Access control** — Can one user/service view or modify another's consent records?
3. **Injection** — Are all queries parameterized? No string concatenation in SQL?
4. **Input validation** — Are consent payloads validated before processing?
5. **Logging** — Is PII (user IDs, consent details) being logged?
6. **Secrets** — Any hardcoded credentials or tokens?
7. **Authorization** — Are consent modification endpoints properly authorized?
8. **Data integrity** — Can consent records be tampered with or replayed?

Read all files in `internal/domain/consent/` and check each against the Internal Security Checklist.

## Context from Prior Agents

### Code Reviewer Findings
<Code Reviewer's output will be inserted here — specifically any findings flagged for Security review, the list of all files reviewed, and any potential security-adjacent issues the Code Reviewer identified but deferred to Security for assessment.>
"""
)
```

### Agent() Call 2c: QA — Review Test Coverage

```
Agent(
  description: "Review consent domain test coverage",
  subagent_type: "qa",
  model: "claude-sonnet-4-6",
  prompt: """
# QA Agent

You are a quality assurance specialist. You design test plans, review code quality, validate that acceptance criteria are met, and identify gaps in test coverage. You do not write production code.

## System Context

All systems are **internal-facing**. Test cases should reflect internal user/operator actions and internal service-to-service interactions. Do not write tests for public-facing scenarios (anonymous public traffic, external API consumers, CDN behavior).

## Conventions

Follow Go testing patterns:
- Testing standards: assertion library, test structure, grouping
- Mock setup patterns: interface mocking, DB mocking, mock import aliases
- Time mocking approach
- Coverage requirements
- Test file placement and naming (*_test.go in same package)

## Test Coverage Checklist

For every change, verify tests cover:
- [ ] Happy path (success case)
- [ ] Not found case
- [ ] Validation error (invalid input)
- [ ] Infrastructure error (DB failure)
- [ ] Panic recovery (handlers only)
- [ ] Edge cases from business acceptance criteria

## Sign-Off Criteria

A change is ready for merge when:
1. All test cases pass
2. Coverage meets project threshold on modified packages
3. No regression in existing tests
4. All acceptance criteria from BA are validated

## Output Format

Use the standard QA output format with Test Plan table, Coverage Report, Acceptance Criteria Validation, and Sign-Off verdict.

---
## Project Conventions
No project-specific CLAUDE.md found. Use embedded Go testing conventions. Expected patterns: table-driven tests, testify assertions, mock interfaces.

---
## Task
Review **test coverage** for all code in `internal/domain/consent/` before merge to main.

Specific areas to assess:

1. **Test file existence** — Does every .go file have a corresponding _test.go?
2. **Coverage analysis** — Run `go test -cover ./internal/domain/consent/...` and report coverage percentage
3. **Test case completeness** — For each usecase/handler/repository:
   - Happy path tested?
   - Error paths tested (not found, validation error, DB error)?
   - Edge cases tested (empty input, nil values, boundary conditions)?
4. **Mock quality** — Are mocks properly set up? Using interface-based mocking?
5. **Test isolation** — Are tests independent? No shared mutable state between tests?
6. **Missing test scenarios** — Identify specific untested paths and recommend test cases

For the consent domain specifically:
- Are consent creation/update/revocation flows all tested?
- Are authorization checks tested (user can only manage own consent)?
- Are concurrent consent modifications tested?

Read all files in `internal/domain/consent/` (both source and test files). Run coverage tools if available.

## Context from Prior Agents

### Code Reviewer Findings
<Code Reviewer's output will be inserted here — specifically findings related to test quality (mock aliases, time mocking, panic recovery, coverage gaps) and the full list of files under review so QA knows which files need test coverage.>
"""
)
```

---

## Step 3: Merge Parallel Outputs

เมื่อ Step 2 agents ทั้ง 3 ตัวเสร็จ Orchestrator จะ:

1. **รวม findings** จากทุก agent — deduplicate กรณีที่ Code Reviewer กับ Security flag issue เดียวกัน
2. **จัดลำดับ findings** — Blocker/Critical ก่อน, แล้ว High, Medium, Warning, Low, Info
3. **Resolve conflicts** — ถ้า Security กับ Code Reviewer ขัดแย้งกัน: Security ชนะเรื่อง security issues, Code Reviewer ชนะเรื่อง convention issues
4. **รวม action items** เป็น list เดียวสำหรับ Developer

---

## Step 4: Assemble Final Summary

```
## Summary

**Task:** Review code in internal/domain/consent/ before merge to main — convention, security, and test coverage
**Workflow:** Code Review (matched signals: "review", "ก่อน merge" → Code Review workflow)
**Agents Used:** Code Reviewer, Developer, Security, QA

---

### 1. Code Reviewer — Convention Compliance

<Code Reviewer's full output here>
- Findings organized by severity
- Files reviewed count
- Verdict: Approved / Changes Required

---

### 2. Developer — Correctness Review

<Developer's full output here>
- Logic correctness findings
- Data flow issues
- Edge case gaps

---

### 3. Security — Security Review

<Security's full output here>
- Security findings by severity (Critical/High/Medium/Low)
- Consent-specific security concerns (PII, access control, data integrity)
- Merge Recommendation: Approved / Blocked

---

### 4. QA — Test Coverage Review

<QA's full output here>
- Test plan table
- Coverage percentage per package
- Missing test scenarios
- Sign-Off: Approved / Blocked

---

**Issues Found:**
- [Consolidated list of all Blocker/Critical findings from Code Reviewer]
- [Consolidated list of all Critical/High findings from Security]
- [Consolidated list of all blocking issues from QA]

**Gaps:**
- No project-specific CLAUDE.md found — convention checks used embedded Go Clean Architecture conventions rather than project-specific rules. Recommend creating a CLAUDE.md for this project.

**Next Steps:**
1. Fix all Blocker/Critical findings from Code Reviewer before merge
2. Fix all Critical/High findings from Security before merge
3. Add missing test cases identified by QA to meet coverage threshold
4. Re-run pipeline after fixes to verify resolution
5. Consider creating a project CLAUDE.md to codify conventions for future reviews
```

---

## Execution Summary

### Pipeline Visualization

```
                    ┌─────────────────────┐
                    │   Step 0: Read       │
                    │   Project Context    │
                    │   (AGENTS.md found,  │
                    │    no Go CLAUDE.md)  │
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │   Step 1: Classify   │
                    │   → Code Review      │
                    │     Workflow          │
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │  Step 1 (Pipeline):  │
                    │  Code Reviewer       │
                    │  (sonnet, sequential)│
                    └─────────┬───────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
    ┌─────────▼─────┐ ┌──────▼──────┐ ┌──────▼──────┐
    │ Step 2a:      │ │ Step 2b:    │ │ Step 2c:    │
    │ Developer     │ │ Security    │ │ QA          │
    │ (sonnet)      │ │ (sonnet)    │ │ (sonnet)    │
    │ correctness   │ │ security    │ │ test cover  │
    └───────┬───────┘ └──────┬──────┘ └──────┬──────┘
            │                │               │
            └───────────────┬┘───────────────┘
                            │  PARALLEL
                    ┌───────▼─────────┐
                    │  Step 3: Merge   │
                    │  Parallel Outputs│
                    └───────┬─────────┘
                            │
                    ┌───────▼─────────┐
                    │  Step 4: Final   │
                    │  Summary Output  │
                    └─────────────────┘
```

### Agent Delegation Summary

| Step | Agent | subagent_type | Model | Mode | Input |
|------|-------|---------------|-------|------|-------|
| 1 | Code Reviewer | code-reviewer | claude-sonnet-4-6 | Sequential | Files in internal/domain/consent/ |
| 2a | Developer | developer | claude-sonnet-4-6 | Parallel | Code Reviewer findings + consent files |
| 2b | Security | security | claude-sonnet-4-6 | Parallel | Code Reviewer findings + consent files |
| 2c | QA | qa | claude-sonnet-4-6 | Parallel | Code Reviewer findings + consent files |

### Context Passing Map

| From | To | What Gets Passed |
|------|----|-----------------|
| Code Reviewer | Developer | All findings + severity + files reviewed list |
| Code Reviewer | Security | Security-flagged findings + files reviewed list |
| Code Reviewer | QA | Test quality findings + files reviewed list |

### Total Agent Calls: 4

| Metric | Value |
|--------|-------|
| Sequential steps | 2 (Step 1, then Step 2) |
| Parallel agents in Step 2 | 3 (Developer, Security, QA) |
| Total Agent() invocations | 4 |
| Estimated wall-clock steps | 2 rounds (sequential + parallel batch) |

### Key Decisions

1. **Workflow Selection:** Code Review — user explicitly said "review code" and "ก่อน merge"
2. **No project CLAUDE.md:** Proceed with embedded conventions from reference files; flag as gap in summary
3. **Consent domain = sensitive data:** Instructed Security agent to pay special attention to PII, access control, and data integrity given the consent context
4. **Developer in review mode:** Developer agent tasked with correctness review (not implementation) since this is a review workflow

### Compliance with Delegation Rules

| Rule | Status |
|------|--------|
| Never skip relevant specialist | All 4 specialists included per workflow |
| Never implement code yourself | Orchestrator delegates only, no code written |
| Never let Developer make security decisions alone | Security agent runs in parallel |
| Always read reference file before composing prompt | All 4 reference files read before delegation |
| Always include project conventions | Included in every prompt (noted absence of Go CLAUDE.md) |
