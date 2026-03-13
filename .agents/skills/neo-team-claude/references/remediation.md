# Remediation Loop

When verification agents (Code Reviewer, Security, QA) return blocking findings, the pipeline doesn't stop — it loops back for remediation. The goal is to resolve issues automatically without requiring the user to intervene, while capping iterations to prevent infinite loops.

## How it works

```
Verification agent(s) return findings
    │
    ├── All Approved / no blocking findings → Proceed to Summary
    │
    └── Has blocking findings → Remediation cycle:
            1. Collect all blocking findings into a single prioritized list
            2. Delegate to Developer (or DevOps for CI/CD) to fix
               (Developer runs self-review as part of their fix)
            3. Re-run ONLY the agents that returned blocking findings
            4. If still blocked → try one more cycle (max 2 total)
            5. If blocked after 2 cycles → stop pipeline, escalate to user
```

## What counts as "blocking"

| Agent         | Blocking Condition           | Non-Blocking          |
| ------------- | ---------------------------- | --------------------- |
| Code Reviewer | Blocker or Critical severity | Warning, Info         |
| Security      | Critical or High severity    | Medium, Low           |
| QA            | Sign-Off = "Blocked"         | Sign-Off = "Approved" |

## Handling non-blocking findings (Warning / Info / Medium / Low)

After remediation completes (or if there were no blocking findings), check if there are non-blocking findings. If yes, present them to the user and ask:

```
## Non-Blocking Findings

The following warnings/suggestions were found. They won't break anything now,
but may be worth addressing:

- [Warning] [file:line] description
- [Info] [file:line] description

Would you like me to fix these too, or skip for now?
```

Let the user decide — don't fix automatically (wastes time if user doesn't care) and don't silently ignore (user may want to know).

## Remediation rules

- **Only re-run failing agents** — if Code Reviewer approved but Security blocked, only re-run Security after the fix
- **Pass specific findings** — give Developer the exact findings list with file:line references, not a vague "fix the issues"
- **Developer owns quality** — Developer applies self-review during their fix, same as initial implementation
- **Max 2 remediation cycles** — if the issue can't be resolved in 2 passes, it likely needs human judgment (architectural disagreement, ambiguous requirements, complex trade-off)
- **Report all cycles in Summary** — show which findings were found, which were fixed, and which remain unresolved

## Escalation to user

After 2 failed remediation cycles, stop and present:

```
## Remediation Failed — Needs Your Input

**Unresolved Findings:**
- [list of remaining Blocker/Critical/Blocked items with details]

**What was attempted:**
- Cycle 1: Developer fixed X, Y — but Z remains
- Cycle 2: Developer attempted Z — but [reason it failed]

**Recommendation:** [suggested path forward]
```
