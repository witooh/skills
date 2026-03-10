---
name: loop
description: Iteratively improve any output until measurable criteria are met. Use when the user wants to refine existing work against specific standards. Triggers on phrases like "improve this", "make it better", "iterate", "loop", "refine", "keep improving", "not good enough yet", or when the user provides criteria and wants repeated improvement until they're satisfied.
metadata:
  version: "1.2"
---

# Loop

Iteratively improve any output until all criteria are met — with scored evaluation at every step so "better" is never subjective.

## Quick Start

1. Receive input (existing work or raw request)
2. Establish 2-3 ranked, measurable criteria
3. Score baseline (Iteration 0), then iteratively improve — one focused goal per iteration
4. Each iteration: improve → score → compare → decide (continue/stop)
5. Deliver final output with full iteration history

## Tools

| Tool | Purpose |
|------|---------|
| `ask_user` | Ask the user ONE question at a time when establishing criteria or confirming direction. Prefer providing `choices` for faster UX. |

## Core Rules

1. **Never improve without criteria.** If none exist, establish them first.
2. **Always score before AND after.** Every iteration has a scorecard.
3. **One focused goal per iteration.** Closely related changes may go together, but they must serve a single improvement goal. Multiple unrelated changes make attribution impossible.
4. **Target the largest gap first.** Never polish a met criterion while others are unmet.
5. **Detect regressions.** If a previously-met criterion drops, revert or fix before continuing.
6. **Stop when appropriate.** All criteria met, 3 stalled iterations, 10 total iterations (soft max), or user says stop.
7. **Always use `ask_user` for questions.** Never embed questions in plain text output. Prefer providing `choices` when the answer space is predictable.

## Workflow

The improvement loop involves these steps, executed in strict order. For detailed scoring rubric, scorecard formats, priority rules, and completion conditions: see [references/EVALUATION-GUIDE.md](references/EVALUATION-GUIDE.md)

1. **Receive** — Accept the input (existing work or raw request)
2. **Establish Criteria** — Extract or ask for measurable evaluation criteria
3. **Capture Baseline** — Produce first output, score it (Iteration 0)
4. **Improve** — Make one focused change targeting the largest gap
5. **Evaluate** — Score the new output, compare to previous iteration
6. **Decide** — Continue, stop, or adjust criteria
7. **Deliver** — Present final output with full iteration history

### Step 1 — Receive

Accept the input. It can be:

- **Existing work** — User provides something they want improved. Ask for criteria (Step 2).
- **Raw request** — User describes what they want. Produce the first version, then ask for criteria.

Acknowledge what was received. Do NOT start improving yet.

### Step 2 — Establish Criteria

Confirm or ask for 2-3 ranked, specific, observable criteria. Force-rank if more than 3.

### Step 3 — Capture Baseline

Produce the first output (or use existing work as-is), score it against all criteria, and present to the user with key gaps identified.

### Step 4 — Improve

Make **one focused change** targeting the largest gap. Explain what you're changing and why before making the change.

### Step 5 — Evaluate

Score the new output against ALL criteria, compare to previous iteration, and check for regressions.

### Step 6 — Decide

Continue if gaps remain, stop if all criteria met, 3 stalled iterations, 10 total iterations, or user says stop.

### Step 7 — Deliver

Present the final output with a summary:

```
## Final Output

[The improved result]

---

### Iteration History

| Iteration | Change | Total Score | Delta |
|---|---|---|---|
| 0 (Baseline) | — | X / Y | — |
| 1 | [Change description] | X / Y | +W |
| 2 | [Change description] | X / Y | +W |

**Final Score: X / Y**
**Criteria met:** [List]
**Criteria not met (if any):** [List with reason]
```

## Handling Edge Cases

**User changes criteria mid-loop:** Accept the change. Re-score the current output against the new criteria and continue from Step 4.

**User provides feedback instead of letting the loop run:** Treat feedback as a new criterion or a signal to re-prioritize. Adjust and continue.

**Output is already perfect (all criteria met at baseline):** Declare success immediately. Suggest the user raise the bar if they want further improvement.

**Criteria conflict with each other:** Flag the conflict: *"Criterion A and B seem to pull in opposite directions. Which should win when they conflict?"*

## What This Skill Does NOT Do

- Does not discover goals or explore intent — it requires clear input and criteria
- Does not guess what "better" means — requires explicit criteria
- Does not make unlimited iterations — has clear stopping conditions
- Does not trade met criteria for unmet ones without user approval
