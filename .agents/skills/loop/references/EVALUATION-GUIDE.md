# Evaluation Guide

Detailed patterns for scoring, baseline capture, and iteration tracking. Read this file when executing the improvement loop to understand how to evaluate each iteration objectively.

**Important:** Always use the `ask_user` tool to ask questions — never embed questions in plain text output. When the answer space is predictable, pass a `choices` array for faster UX.

---

## Establishing Criteria

Criteria come from the user's input:

- **If criteria were provided with the input** — Use them directly after confirming with the user.
- **If no criteria exist** — Ask before starting:
  - What are the top 2-3 things that matter most?
  - What would make you reject the result?
  - Force-rank if more than 3.

Every criterion must be **specific and observable**:

| Vague Criterion | Specific Criterion |
|---|---|
| Easy to understand | A beginner can follow it without external help in under 10 minutes |
| High quality | Passes all listed acceptance checks with zero failures |
| Fast | Completes in under 2 seconds for typical input |
| Professional | Matches the tone and structure of the provided reference example |

---

## Capturing Baseline

Before any improvement, capture the current state as Baseline (iteration 0):

1. **Produce the first output** based on the prompt/task
2. **Score it against each criterion** using the rubric below
3. **Record the scores** — this is the baseline all future iterations compare against

### Scoring Rubric

Score each criterion on a 3-point scale:

| Score | Label | Meaning |
|---|---|---|
| 0 | Not met | Criterion is clearly not satisfied |
| 1 | Partial | Some progress but gaps remain |
| 2 | Met | Criterion is fully satisfied |

### Baseline Scorecard Format

```
## Iteration 0 — Baseline

| Criterion | Score | Evidence |
|---|---|---|
| [Criterion 1] | 0/1/2 | [What was observed] |
| [Criterion 2] | 0/1/2 | [What was observed] |
| [Criterion 3] | 0/1/2 | [What was observed] |

**Total: X / Y**
**Key gaps:** [List the most impactful unmet criteria]
```

---

## Iteration Evaluation

After each improvement iteration, produce a scorecard in the same format and compare to the previous iteration:

```
## Iteration N

**Changes made:** [What was changed and why]

| Criterion | Previous | Current | Delta |
|---|---|---|---|
| [Criterion 1] | 1 | 2 | +1 |
| [Criterion 2] | 0 | 1 | +1 |
| [Criterion 3] | 2 | 2 | 0 |

**Total: X / Y (was: Z / Y, delta: +W)**
**Remaining gaps:** [What's still unmet]
**Next action:** [What to improve next, targeting the largest gap]
```

---

## Deciding What to Improve Next

Priority order for selecting the next improvement target:

1. **Criterion scored 0** — Not met at all is the biggest gap
2. **Highest-ranked criterion that is not yet 2** — User's priority order matters
3. **Criterion with easiest path from 1 → 2** — Quick wins build momentum

Never improve a criterion that is already scored 2 while others are below 2.

---

## Completion Conditions

The loop ends when ANY of these are true:

| Condition | Action |
|---|---|
| All criteria scored 2 | Declare success, present final output |
| 3 consecutive iterations with zero total delta | Stop — diminishing returns. Ask user to adjust criteria or accept current state |
| 10 total iterations reached | Stop — soft max. Present best result and ask user whether to continue or accept |
| User says "good enough" or "stop" | Respect it immediately |
| A criterion is proven impossible given constraints | Flag it, ask user to remove or relax it, then continue |

---

## Regression Detection

After each iteration, check that NO previously-met criterion has dropped:

- If a regression is detected, **revert the change** or fix the regression before continuing
- Never trade a met criterion for progress on another unless the user explicitly approves

---

## Anti-Patterns

| Anti-Pattern | Why It's Harmful | What to Do Instead |
|---|---|---|
| Improving without scoring first | No way to know if it got better | Always score before AND after |
| Changing multiple things at once | Cannot attribute improvement to a specific change | One focused goal per iteration (related changes OK) |
| Ignoring user's criterion ranking | Optimizes for wrong thing | Follow the user's priority order |
| Continuing after 3 stalled iterations | Wastes time, frustrates user | Stop and discuss with user |
| Polishing a met criterion while others are unmet | Misallocated effort | Target the largest gap first |
