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
            2. Send findings to Developer via write_agent (preserves implementation context)
               — if Developer was not spawned with mode: "background", spawn new agent
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

## Multi-turn remediation with write_agent (Copilot CLI v1.0.5+)

When the orchestrator spawns the Developer agent with `mode: "background"`, the agent stays alive after its initial implementation. This enables multi-turn remediation — sending findings back to the SAME agent instead of spawning a new one.

### How to use

1. **Initial spawn:** Launch Developer with `mode: "background"` in the `task` tool call:
   ```
   task(
     description: "Developer implements feature",
     agent_type: "general-purpose",
     model: "claude-sonnet-4.6",
     mode: "background",
     prompt: "..."
   )
   // Returns agent_id
   ```

2. **Read result:** Use `read_agent(agent_id)` to get the Developer's implementation output.

3. **Send remediation findings:** If verification agents find blocking issues, use `write_agent` to send them back:
   ```
   write_agent(
     agent_id: "<developer_agent_id>",
     message: """
   ## Remediation Required — Cycle 1

   The following blocking findings were found by verification agents.
   Fix these issues in the code you just implemented.

   ### Blocking Findings
   - [Blocker] src/handler.go:42 — Missing error check on db.Query result
   - [Critical] src/service.go:15 — SQL injection via string concatenation

   Fix each finding, run self-review, then report what you changed.
   """
   )
   ```

4. **Read remediation result:** Use `read_agent(agent_id)` again to get the fix.

5. **Re-verify:** Re-run only the failing verification agents.

### Benefits over spawning new agents

- **Context preserved** — Developer retains full understanding of the codebase, the original implementation, and WHY certain decisions were made
- **Faster** — no need to re-read project files, CLAUDE.md, or re-understand the architecture
- **More accurate fixes** — Developer knows exactly which code they wrote, making targeted fixes easier

### Fallback

If the Developer agent has already completed (not in background mode), fall back to the original behavior: spawn a new Developer agent with the findings and relevant context from the original implementation.

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
