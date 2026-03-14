# Workflow Pipeline Definitions

Each workflow lists the pipeline steps with explicit context-passing notes. Follow the order strictly — parallel steps are marked.

## New Feature

```
Complex task (Brainstorm + BA + Architect + Plan):
1. /brainstorm         → invoke brainstorm skill to explore the idea and clarify direction with the user
2. business-analyst    → structure requirements and acceptance criteria
   Context: Brainstorm output (key decisions, constraints, scope)
3. architect           → design endpoint/module contract and data flow
   Context: BA's user stories + acceptance criteria + business rules
4. /plan               → synthesize Architect's design into an implementation plan, present to user for confirmation
   Include: component breakdown, file changes, API contracts, implementation order
   Wait for user approval before proceeding
5. developer           → implement code and unit tests
   Context: Architect's design + confirmed plan + BA's acceptance criteria
   [If multiple independent components: spawn parallel developer agents]
6. REVIEW LOOP         → run the review-fix loop (see Review Loop section)
   Input: Developer's changed files + project conventions
7. [If task adds/changes API endpoints: delegate to `api-doc-gen` skill to update docs/api-doc.md]

Simple task (skip Brainstorm + BA):
1. architect           → clarify requirements AND design contract in one step
2. developer           → implement code and unit tests
   Context: Architect's design + acceptance criteria
   [If multiple independent components: spawn parallel developer agents]
3. REVIEW LOOP         → run the review-fix loop (see Review Loop section)
   Input: Developer's changed files + project conventions
4. [If task adds/changes API endpoints: delegate to `api-doc-gen` skill to update docs/api-doc.md]
```

## Bug Fix

```
Complex bug (multi-file, ambiguous root cause, multiple fix strategies):
1. system-analyzer     → diagnose root cause
2. /plan               → synthesize root cause into a fix plan, present to user for confirmation
   Include: root cause summary, affected files/lines, proposed fix approach, risk assessment
   Wait for user approval before proceeding — bugs can have multiple valid fixes with different trade-offs
3. developer           → implement fix and unit/regression tests
   Context: System Analyzer's root cause + confirmed fix plan
   [If multiple independent fixes: spawn parallel developer agents]
4. REVIEW LOOP         → run the review-fix loop (see Review Loop section)
   Input: Developer's changed files + project conventions + System Analyzer's root cause (for QA regression test design)
5. [If fix changes API endpoints: delegate to `api-doc-gen` skill to update docs/api-doc.md]

Simple bug (single file, obvious root cause, straightforward fix):
1. system-analyzer     → diagnose root cause
2. developer           → implement fix and unit/regression tests
   Context: System Analyzer's root cause + affected files/lines
3. REVIEW LOOP         → run the review-fix loop (see Review Loop section)
   Input: Developer's changed files + project conventions + System Analyzer's root cause (for QA regression test design)
4. [If fix changes API endpoints: delegate to `api-doc-gen` skill to update docs/api-doc.md]
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
2. architect (opus)    → design target structure
   Context: System Analyzer's dependency map + current structure analysis
3. /plan               → present refactoring plan to user for confirmation
   Include: affected modules, target structure, migration steps, risk areas
   Wait for user approval before proceeding
4. developer           → implement refactoring
   Context: Architect's target structure + confirmed plan
   [If multiple independent modules: spawn parallel developer agents]
5. REVIEW LOOP         → run the review-fix loop (see Review Loop section)
   Input: Developer's changed files + project conventions
6. [If refactoring changes API contracts: delegate to `api-doc-gen` skill to update docs/api-doc.md]

Simple (single module, extract function, simplify logic):
1. system-analyzer     → analyze current code + identify dependencies
2. architect           → design target structure
   Context: System Analyzer's analysis
3. developer           → implement refactoring
   Context: Architect's target structure
4. REVIEW LOOP         → run the review-fix loop (see Review Loop section)
   Input: Developer's changed files + project conventions
5. [If refactoring changes API contracts: delegate to `api-doc-gen` skill to update docs/api-doc.md]
```

## Requirement Clarification

```
1. business-analyst    → clarify and structure requirements
2. architect           → validate technical feasibility
   Context: BA's structured requirements
```

## Review Loop

Review-fix loop used as a sub-workflow embedded in other pipelines (e.g., New Feature, Bug Fix).

```
Review Loop:

┌─→ 1. code-reviewer + security + qa → review conventions, security, and test coverage (ALL PARALLEL)
│      To all: Developer's changed files + project conventions
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
