# Workflow Pipeline Definitions

Each workflow lists the pipeline steps with explicit context-passing notes. Follow the order strictly — parallel steps are marked.

**Doc First principle:** Every workflow with code changes includes a **QA Test Spec** step before Developer. QA generates a test case document following the [`test-case-document.md`](test-case-document.md) template (GIVEN/WHEN/THEN format with test steps, expected results, test data, and preconditions). Developer uses this document to implement and write tests. For complex tasks, Developer uses TDD mode (Red-Green-Refactor per test case). For simple tasks, Developer implements normally and uses the spec as reference.

**Execution Report:** During the Review Loop, after QA runs E2E tests, QA generates an execution report following the [`test-execution-report.md`](test-execution-report.md) template — mapping each test case to its actual result, status, and defect references.

## New Feature

```
Complex task (Brainstorm + BA + Architect + Plan):
1. /brainstorm         → invoke brainstorm skill to explore the idea and clarify direction with the user
2. business-analyst    → structure requirements, generate AC document (acceptance-criteria.md template)
   Context: Brainstorm output (key decisions, constraints, scope)
   IF BA returns Open Questions:
      a. Orchestrator asks user for clarification (relay BA's questions)
      b. Orchestrator re-delegates to BA with user's answers
      c. Repeat until BA has no Open Questions
   Output: AC document written to project docs folder (no Open Questions remaining)
3. architect           → design endpoint/module contract and data flow
   Context: BA's user stories + acceptance criteria + business rules
4. /plan               → synthesize Architect's design into an implementation plan, present to user for confirmation
   Include: component breakdown, file changes, API contracts, implementation order
   Wait for user approval before proceeding
5. TEST CASE REVIEW LOOP → QA generates test cases, BA reviews for AC coverage (see Test Case Review Loop section)
   Context to QA: Architect's API contracts + BA's AC document (BOTH required — hard gate)
   Context to BA (reviewer): AC document + QA's test cases
6. developer           → implement code and unit tests (TDD mode)
   Context: Architect's design + confirmed plan + BA's acceptance criteria + QA's test case document (BA-approved)
   [If multiple independent components: spawn parallel developer agents]
7. REVIEW LOOP         → run the review-fix loop (see Review Loop section)
   Input: Developer's changed files + project conventions
8. [If task adds/changes API endpoints: delegate to `api-doc-gen` skill to update docs/api-doc.md]

Simple task (BA first → Architect):
1. business-analyst    → clarify requirements, generate AC document (acceptance-criteria.md template)
   Context: User's request
   IF BA returns Open Questions:
      a. Orchestrator asks user for clarification (relay BA's questions)
      b. Orchestrator re-delegates to BA with user's answers
      c. Repeat until BA has no Open Questions
   Output: AC document written to project docs folder (no Open Questions remaining)
2. architect           → design contract and module structure, ensuring design covers every AC-ID
   Context: BA's AC document + user stories + business rules
3. TEST CASE REVIEW LOOP → QA generates test cases, BA reviews for AC coverage (see Test Case Review Loop section)
   Context to QA: Architect's API contracts + BA's AC document (BOTH required — hard gate)
   Context to BA (reviewer): AC document + QA's test cases
4. developer           → implement code and unit tests
   Context: Architect's design + BA's AC document + QA's test case document (BA-approved)
   [If multiple independent components: spawn parallel developer agents]
5. REVIEW LOOP         → run the review-fix loop (see Review Loop section)
   Input: Developer's changed files + project conventions
6. [If task adds/changes API endpoints: delegate to `api-doc-gen` skill to update docs/api-doc.md]
```

## Bug Fix

```
Complex bug (multi-file, ambiguous root cause, multiple fix strategies):
1. system-analyzer     → diagnose root cause
2. /plan               → synthesize root cause into a fix plan, present to user for confirmation
   Include: root cause summary, affected files/lines, proposed fix approach, risk assessment
   Wait for user approval before proceeding — bugs can have multiple valid fixes with different trade-offs
3. qa (test spec)      → generate test case document (test-case-document.md template)
   Context: System Analyzer's root cause + confirmed fix plan
   Mode: Test case document only — no test code, no review. Focus on regression test cases.
4. developer           → implement fix and unit/regression tests (TDD mode)
   Context: System Analyzer's root cause + confirmed fix plan + QA's test case document
   [If multiple independent fixes: spawn parallel developer agents]
5. REVIEW LOOP         → run the review-fix loop (see Review Loop section)
   Input: Developer's changed files + project conventions + System Analyzer's root cause (for QA regression test design)
6. [If fix changes API endpoints: delegate to `api-doc-gen` skill to update docs/api-doc.md]

Simple bug (single file, obvious root cause, straightforward fix):
1. system-analyzer     → diagnose root cause
2. qa (test spec)      → generate test case document (test-case-document.md template)
   Context: System Analyzer's root cause + affected files/lines
   Mode: Test case document only — no test code, no review. Focus on regression test cases.
3. developer           → implement fix and unit/regression tests
   Context: System Analyzer's root cause + affected files/lines + QA's test case document
4. REVIEW LOOP         → run the review-fix loop (see Review Loop section)
   Input: Developer's changed files + project conventions + System Analyzer's root cause (for QA regression test design)
5. [If fix changes API endpoints: delegate to `api-doc-gen` skill to update docs/api-doc.md]
```

## PR Review

Review-only workflow for external PRs — no code changes, no review loop. The goal is to provide structured feedback.
Typically invoked through the gitlab skill (or gh CLI), which provides the diff as input context.

```
Input: PR/MR diff + changed files (provided by the caller — e.g., gitlab skill, gh CLI)

1. code-reviewer + security + qa → review conventions, security, and test coverage (ALL PARALLEL)
   To all: PR diff + changed files + project conventions
2. Assemble review summary → return to caller
```

## Refactoring

```
Complex (cross-module, extract service, merge duplicates):
1. system-analyzer     → analyze current structure, dependencies, coupling risks
2. architect           → design target structure
   Context: System Analyzer's dependency map + current structure analysis
3. /plan               → present refactoring plan to user for confirmation
   Include: affected modules, target structure, migration steps, risk areas
   Wait for user approval before proceeding
4. qa (test spec)      → generate test case document (test-case-document.md template)
   Context: Architect's target structure + System Analyzer's dependency map
   Mode: Test case document only — no test code, no review. Focus on behavior preservation tests.
5. developer           → implement refactoring (TDD mode)
   Context: Architect's target structure + confirmed plan + QA's test case document
   [If multiple independent modules: spawn parallel developer agents]
6. REVIEW LOOP         → run the review-fix loop (see Review Loop section)
   Input: Developer's changed files + project conventions
7. [If refactoring changes API contracts: delegate to `api-doc-gen` skill to update docs/api-doc.md]

Simple (single module, extract function, simplify logic):
1. system-analyzer     → analyze current code + identify dependencies
2. architect           → design target structure
   Context: System Analyzer's analysis
3. qa (test spec)      → generate test case document (test-case-document.md template)
   Context: Architect's target structure + System Analyzer's analysis
   Mode: Test case document only — no test code, no review. Focus on behavior preservation tests.
4. developer           → implement refactoring
   Context: Architect's target structure + QA's test case document
5. REVIEW LOOP         → run the review-fix loop (see Review Loop section)
   Input: Developer's changed files + project conventions
6. [If refactoring changes API contracts: delegate to `api-doc-gen` skill to update docs/api-doc.md]
```

## Requirement Clarification

```
1. business-analyst    → clarify and structure requirements
   IF BA returns Open Questions:
      a. Orchestrator asks user for clarification (relay BA's questions)
      b. Orchestrator re-delegates to BA with user's answers
      c. Repeat until BA has no Open Questions
   Output: Structured requirements with all ambiguities resolved
2. architect           → validate technical feasibility
   Context: BA's structured requirements (fully clarified)
```

## Test Case Review Loop

Quality gate for test case documents — ensures test cases fully cover acceptance criteria before Developer starts implementation. This loop catches vague assertions, missing business scenarios, and duplicate test cases early, when they're cheap to fix.

```
Test Case Review Loop:

┌─→ 1. qa (test spec) → generate test case document (test-case-document.md template)
│      Context: Architect's API contracts + BA's AC document (BOTH required — hard gate)
│      Mode: Test case document only — no test code, no review
│      Every test case MUST include "Traces To: AC-XXX" field
│
│   2. business-analyst (review) → review test cases against AC document
│      Check:
│      - Every AC-ID has at least one test case covering it
│      - Test cases use specific HTTP status codes from API contract (not >= 400)
│      - Error test cases assert error body structure (error.code + error.message)
│      - Business rules from AC are fully tested
│      - No duplicate/overlapping test cases
│      Output: Coverage assessment with Approved / Revise verdict
│
│   3. Evaluate:
│      ├── BA approves → DONE (proceed to Developer)
│      └── BA has findings:
│            a. Pass BA's findings to QA
│            b. QA regenerates/fixes test cases based on feedback
└────── c. Loop back to step 2 (BA re-reviews)

Max 3 review cycles. If still unresolved → deliver to user with gaps noted.
```

**Important:** The Test Case Review Loop replaces the old standalone `qa (test spec)` step in all workflows. Wherever you see `TEST CASE REVIEW LOOP` in a workflow, run this sub-workflow.

---

## Review Loop

Review-fix loop used as a sub-workflow embedded in other pipelines (e.g., New Feature, Bug Fix).

```
Review Loop:

┌─→ 1. code-reviewer + security + qa → review conventions, security, and test coverage (ALL PARALLEL)
│      To all: Developer's changed files + project conventions
│      QA additionally: run E2E tests → generate execution report (test-execution-report.md template)
│
│   2. Evaluate results:
│      ├── ALL three agents approve → DONE (proceed to next workflow step or Summary)
│      └── ANY agent has blocking findings:
│            a. Collect all blocking feedback into a single prioritized list
│            b. Delegate to Developer to fix (pass specific file:line references)
│            c. Developer completes fixes
└────── d. Loop back to step 1 (re-run ALL three agents)

Max 3 review cycles. If still unresolved → escalate to user:

## Review Loop Failed — Needs Your Input

**Unresolved Findings:**
- [list of remaining Blocker/Critical/Blocked items with details]

**What was attempted:**
- Cycle 1: Developer fixed X, Y — but Z remains
- Cycle 2: Developer attempted Z — but [reason it failed]

**Recommendation:** [suggested path forward]

Blocking definitions:
- Code Reviewer: Blocker or Critical severity
- Security: Critical or High severity
- QA: Sign-Off = "Blocked"

Non-blocking findings (Warning/Info/Medium/Low): present to user after the loop completes and ask whether to fix or skip.
```
