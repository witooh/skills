# Workflow Pipeline Definitions

Each workflow lists the pipeline steps with explicit context-passing notes. Follow the order strictly — parallel steps are marked.

## New Feature

```
Simple task (merged BA+Architect):
1. architect           → clarify requirements AND design contract in one step
2. developer + qa      → implement code AND write test specs (PARALLEL)
   To developer: Architect's design + acceptance criteria
                [If task adds/changes API endpoints: also update docs/api-doc.md using api-doc-template.md]
   To qa: Architect's API contracts + acceptance criteria
3. code-reviewer + security → check conventions AND security (PARALLEL)
   To both: Developer's changed files list
4. [REMEDIATION if step 3 has Blocker/Critical findings]

Complex task (separate BA+Architect):
1. business-analyst    → clarify requirements and acceptance criteria
2. architect           → design endpoint/module contract and data flow
   Context: BA's user stories + acceptance criteria + business rules
3. developer + qa      → implement code AND write test specs (PARALLEL)
   To developer: Architect's design + BA's acceptance criteria
                [If task adds/changes API endpoints: also update docs/api-doc.md using api-doc-template.md]
   To qa: Architect's API contracts + BA's acceptance criteria
4. code-reviewer + security → check conventions AND security (PARALLEL)
   To both: Developer's changed files list
5. [REMEDIATION if step 4 has Blocker/Critical findings]
```

## Bug Fix

```
1. system-analyzer     → diagnose root cause
2. developer + qa + code-reviewer + security → implement fix AND write regression test AND check conventions AND security (4-WAY PARALLEL)
   To developer: System Analyzer's root cause + affected files/lines
                [If fix changes API request/response shape: also update docs/api-doc.md using api-doc-template.md]
   To qa: Developer's task description + original bug description + System Analyzer's findings
   To code-reviewer: affected files from System Analyzer
   To security: affected files from System Analyzer
3. [REMEDIATION if step 2 has Blocker/Critical findings]
```

## Incident Investigation

```
1. incident-investigator → gather evidence from live systems (kubectl logs, psql queries, argocd status, docker inspect) and trace root cause back to code
2. Route based on Root Cause Type:
   ├── Code Bug → developer + qa (PARALLEL)
   │   To developer: Incident Investigator's root cause + evidence chain + affected files/lines
   │                 [If fix changes API: also update docs/api-doc.md using api-doc-template.md]
   │   To qa: Incident Investigator's findings + bug description for regression test
   ├── Infrastructure Problem → devops
   │   To devops: Incident Investigator's infra findings + ArgoCD/K8s evidence
   ├── Configuration Error → devops + security (PARALLEL)
   │   To devops: config drift details + recommended fix
   │   To security: credential/secret-related findings if any
   └── Data Issue → developer (manual fix may need user approval)
       To developer: Incident Investigator's data anomaly details + affected records
3. code-reviewer + security + qa → verify fix, security, and test coverage (ALL PARALLEL)
   To all: changed files from step 2
4. [REMEDIATION if step 3 has Blocker/Critical findings]
```

## Security Audit

```
1. security + system-analyzer  → review code and behavior (PARALLEL)
2. developer           → implement fixes
   Context: Security findings + System Analyzer's analysis
3. qa + security + code-reviewer → verify fixes, re-check security, AND check conventions (ALL PARALLEL)
   Context: Security's original findings + Developer's changes
4. [REMEDIATION if step 3 has Critical/High or QA Blocked]
```

## Performance Issue

```
1. system-analyzer     → identify bottlenecks
2. architect           → propose solution design
   Context: System Analyzer's bottleneck analysis
3. developer + qa      → implement optimization AND write perf tests (PARALLEL)
   Context: Architect's solution design
4. code-reviewer + security → check conventions AND security (PARALLEL)
   Context: Developer's changed files
5. [REMEDIATION if step 4 has Blocker/Critical or QA Blocked]
```

## Code Review

```
1. code-reviewer + developer + security + qa → review conventions, correctness, security, coverage (ALL PARALLEL)
   To all: files under review + project conventions
2. [REMEDIATION if step 1 has Blocker/Critical findings]
```

## CI/CD Change

```
1. architect           → validate design and impact
2. devops              → implement Docker/pipeline changes
   Context: Architect's design review
3. security + code-reviewer + qa → verify no new attack surface, check conventions, AND verify changes (ALL PARALLEL)
   Context: DevOps's changed files
4. [REMEDIATION if step 3 has Critical/High findings — DevOps fixes, not Developer]
```

## Requirement Clarification

```
1. business-analyst    → clarify and structure requirements
2. architect           → validate technical feasibility
   Context: BA's structured requirements
```

## Refactoring

```
1. architect           → review current design, propose target structure
2. developer + qa      → implement refactoring AND verify no regression (PARALLEL)
   Context: Architect's target structure
   [If refactoring changes API contracts (path, method, request/response shape): Developer also updates docs/api-doc.md using api-doc-template.md]
3. code-reviewer + security → check compliance AND security (PARALLEL)
   Context: Developer's changed files
4. [REMEDIATION if step 3 has Blocker/Critical or QA Blocked]
```

## Database Migration

```
1. architect           → design schema changes
2. developer           → create migration files (up + down)
   Context: Architect's schema design
3. qa + code-reviewer + security → verify migration, check conventions, AND security (ALL PARALLEL)
   Context: Developer's migration files
4. [REMEDIATION if step 3 has Blocker/Critical or QA Blocked]
```

## Documentation Sync

```
1. developer           → identify code changes that affect docs
2. architect           → update docs/solution-design.md
                         If updating API docs (e.g. docs/api-doc.md), read references/api-doc-template.md first
   Context: Developer's findings
3. qa + code-reviewer + security → verify docs match implementation, check conventions, AND security (ALL PARALLEL)
   Context: Architect's updated docs
4. [REMEDIATION if step 3 has Blocker/Critical or QA Blocked]
```

When generating or updating API documentation, the Architect (or Developer) must read [`api-doc-template.md`](api-doc-template.md) and follow its structure exactly — endpoint layout, field table columns, Business Logic section, and Error Responses format. This ensures all API docs across services look consistent.

## Pre-Merge Review

```
1. code-reviewer + security + qa → check conventions, security, coverage (ALL PARALLEL)
   To all: files under review + project conventions
2. [REMEDIATION if any agent has Blocker/Critical/Blocked findings]
```
