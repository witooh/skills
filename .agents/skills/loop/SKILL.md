---
name: loop
description: Iteratively improve any output until measurable criteria are met. Use after brainstorm to take an improved prompt and develop it through scored iterations, or use standalone when the user wants to refine existing work against specific standards. Triggers on phrases like "improve this", "make it better", "iterate", "loop", "refine", "keep improving", "not good enough yet", or when the user provides criteria and wants repeated improvement until they're satisfied.
metadata:
  version: "1.1"
---

# Loop

Iteratively improve any output until all criteria are met — with scored evaluation at every step so "better" is never subjective.

## Quick Start

1. Receive input (brainstorm output, existing work, or raw request)
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

For detailed scoring rubric, evaluation patterns, and anti-patterns: see [references/EVALUATION-GUIDE.md](references/EVALUATION-GUIDE.md)

## Workflow

The improvement loop involves these steps, executed in strict order:

1. **Receive** — Accept the input (brainstorm output, existing work, or raw request)
2. **Establish Criteria** — Extract or ask for measurable evaluation criteria
3. **Capture Baseline** — Produce first output, score it (Iteration 0)
4. **Improve** — Make one focused change targeting the largest gap
5. **Evaluate** — Score the new output, compare to previous iteration
6. **Decide** — Continue, stop, or adjust criteria
7. **Deliver** — Present final output with full iteration history

### Step 1 — Receive

Accept the input. It can be:

- **Brainstorm output** — Contains an Improved Prompt + Discovery Summary with Criteria. Extract the criteria and prompt directly.
- **Existing work** — User provides something they want improved. Ask for criteria (Step 2).
- **Raw request** — User describes what they want. Produce the first version, then ask for criteria.

Acknowledge what was received. Do NOT start improving yet.

### Step 2 — Establish Criteria

**If criteria came from brainstorm:** Confirm them with the user: *"I'll evaluate against these criteria in priority order: 1) ... 2) ... 3) ... Does this look right?"*

**If no criteria exist:** Ask ONE question at a time:

- What are the top 2-3 things that matter most in the result?
- What would make you reject the result?
- Any decided trade-offs?

Force-rank if more than 3. Make each criterion specific and observable.

### Step 3 — Capture Baseline

Produce the first output (or use the existing work as-is) and score it:

```
## Iteration 0 — Baseline

| Criterion | Score (0-2) | Evidence |
|---|---|---|
| [Criterion 1] | X | [What was observed] |
| [Criterion 2] | X | [What was observed] |

**Total: X / Y**
**Key gaps:** [Most impactful unmet criteria]
```

Present the baseline to the user. Ask: *"Here's where we stand. The biggest gap is [X]. I'll focus on that first. Sound good?"*

### Step 4 — Improve

Make **one focused change** targeting the criterion with:
1. Score 0 (not met at all) — highest priority
2. Highest user-ranked criterion that is not yet 2
3. Easiest path from 1 → 2 — if priorities are equal

Explain what you're changing and why before making the change.

### Step 5 — Evaluate

Score the new output against ALL criteria and compare:

```
## Iteration N

**Change:** [What was changed and why]

| Criterion | Previous | Current | Delta |
|---|---|---|---|
| [Criterion 1] | 1 | 2 | +1 |
| [Criterion 2] | 0 | 1 | +1 |

**Total: X / Y (was: Z / Y, delta: +W)**
**Remaining gaps:** [What's still unmet]
```

**Regression check:** If any criterion dropped, revert or fix before continuing.

### Step 6 — Decide

| Condition | Action |
|---|---|
| All criteria scored 2 | Go to Step 7 — Deliver |
| Gaps remain | Go to Step 4 — Improve next gap |
| 3 consecutive iterations with zero delta | Stop. Ask user to adjust criteria or accept |
| 10 total iterations reached | Stop. Present best result and ask user whether to continue or accept |
| User says "good enough" or "stop" | Go to Step 7 — Deliver |
| A criterion is proven impossible | Flag it. Ask user to remove or relax |

**Scorecard display:** For iterations 1-5, show the full scorecard. From iteration 6 onward, show only changed criteria and the total score to reduce noise.

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

- Does not brainstorm or discover goals — use the `brainstorm` skill for that
- Does not guess what "better" means — requires explicit criteria
- Does not make unlimited iterations — has clear stopping conditions
- Does not trade met criteria for unmet ones without user approval
