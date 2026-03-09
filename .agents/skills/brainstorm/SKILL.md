---
name: brainstorm
description: Improve any user prompt through structured discovery before answering. Use when the user wants to brainstorm, refine an idea, improve a prompt, explore a new domain, plan a project, or when the request is broad/vague and would benefit from clarification. Triggers on phrases like "brainstorm", "help me think through", "improve this prompt", "I have an idea", "let's explore", "I want to build", "I'm thinking about", or any open-ended request where jumping straight to an answer would produce generic results.
metadata:
  version: "1.1"
---

# Brainstorm

Transform vague ideas into precise, actionable prompts through structured questioning — especially for users who lack domain expertise.

## Quick Start

1. User provides a vague idea or open-ended request
2. Agent walks through 7 phases: Receive → Goal → Direction → Reference → Context → Criteria → Synthesize
3. Each phase uses `ask_user` to ask ONE question at a time (prefer multiple choice)
4. Output: a self-contained **Improved Prompt** + Discovery Summary
5. Optionally hand off to the **loop** skill for iterative refinement

## Tools

| Tool | Purpose |
|------|---------|
| `ask_user` | Ask the user ONE question at a time during discovery phases. Prefer providing `choices` for faster UX. |
| `web_search` | Find references when the user has none (Phase 4 — Reference). |

## Core Rules

1. **NEVER answer before questioning is complete.** The urge to help immediately produces generic output.
2. **Ask ONE question at a time using `ask_user`.** Multiple questions get shallow answers. Always use the `ask_user` tool — never embed questions in plain text output.
3. **Prefer multiple choice when possible.** Pass a `choices` array to `ask_user`. Choices are easier to answer than open-ended questions, reduce cognitive load, and reveal preferences faster. Only use open-ended when the answer truly cannot be predicted.
4. **Use the user's language.** Do not introduce jargon they did not use.
5. **Ask about life, not about the domain.** Constraints, risks, and deal-breakers require zero domain knowledge but eliminate wrong paths decisively.
6. **Search for references when the user has none.** AI has vast knowledge but needs a direction signal to know which subset to surface.
7. **Track what's established.** Never re-ask something already answered.
8. **Respect the user's time.** Budget roughly 2-3 questions per phase. If a phase gets repeated "I don't know" or "doesn't matter" responses, move on after 2 attempts.

## Workflow

Improving a prompt involves these phases, executed in strict order:

1. **Receive** — Accept the user's initial prompt without judgment
2. **Goal** — Establish a clear, measurable end-state
3. **Direction** — Eliminate unsuitable paths via constraints, risks, deal-breakers
4. **Reference** — Ground the work in existing knowledge or AI-discovered sources
5. **Context** — Surface real-world constraints (time, money, skills, environment)
6. **Criteria** — Define what "better" means before any iteration
7. **Synthesize** — Produce the improved prompt

For detailed questioning patterns, techniques, and anti-patterns per phase: see [references/QUESTIONING-GUIDE.md](references/QUESTIONING-GUIDE.md)

### Phase 1 — Receive

Read the user's initial prompt. Acknowledge what they want to achieve. Do NOT start solving.

Say something like: *"I understand you want to [restate]. Before I help, I need to ask a few questions to make sure the result fits your specific situation. Let's start with your goal."*

### Phase 2 — Goal

Ask questions until the goal can be stated in one sentence with at least one measurable indicator.

- What is the single most important outcome?
- How would you know this succeeded?
- What does "done" look like?

Summarize the goal and confirm before moving on.

### Phase 3 — Direction

Eliminate wrong paths by asking about constraints, NOT about domain specifics:

- What must absolutely NOT happen?
- What level of risk are you comfortable with?
- Have you tried anything before that didn't work?

Each answer rules out branches. After gathering constraints, **propose 2-3 viable approaches** with trade-offs. Lead with your recommended option and explain why. Let the user react — their reaction narrows direction further than any question could.

Summarize which direction was chosen and why.

### Phase 4 — Reference

Ask if the user has examples, articles, templates, or prior work.

**If user has none:** Use `web_search` to find 2-3 high-quality references that fit the goal + constraints. Present them briefly and ask which feels closest. The reaction provides further direction.

**If user has references:** Ask what specifically they like about them — this reveals hidden preferences.

### Phase 5 — Context

Surface practical constraints that change feasibility:

- Time available (per week, total timeline)
- Budget or resource limits
- Existing skills and tools
- Who else is involved

If context contradicts the goal, flag it gently and ask whether to adjust.

### Phase 6 — Criteria

Define evaluation criteria BEFORE producing output:

- Top 2-3 things that matter most in the result
- What would make them reject the result
- Any decided trade-offs (speed vs. quality, simple vs. comprehensive)

Force-rank if more than 3 criteria. Make each criterion specific and measurable.

### Phase 7 — Synthesize

After all phases are complete, produce the **Improved Prompt**:

1. **Draft the full prompt** incorporating all discovered information.
2. **Present it to the user** and ask: *"Does this capture what you need? Anything to adjust?"*
3. **Iterate if needed.** Fix issues based on feedback until the user confirms.

Use this structure for the final output:

```
## Improved Prompt

[The refined, specific prompt incorporating all discovered information]

---

### Discovery Summary

**Goal:** [One sentence with measurable indicator]
**Direction:** [Chosen approach and key constraints that shaped it]
**Reference:** [Sources that grounded the direction]
**Context:** [Practical constraints: time, budget, skills, environment]
**Criteria:** [Ranked evaluation criteria]
```

The improved prompt must:
- Be self-contained (usable without the discovery summary)
- Include all critical constraints and context inline
- Be specific enough that any AI would produce a targeted, non-generic answer
- Reflect the user's vocabulary and intent, not impose new framing

## Next Step — Loop Skill

After delivering the improved prompt, suggest the **loop** skill if the user wants to iteratively develop the output:

*"The improved prompt is ready. If you'd like me to develop it through scored iterations until it meets your criteria, say `/loop`."*

The loop skill accepts the Improved Prompt + Discovery Summary directly and uses the criteria from Phase 6 as its evaluation rubric.

## Handling Edge Cases

**User wants to skip phases:** Respect their pace but note what's missing: *"We can move on — just know that without [X], the result might be more generic than it could be."*

**User says "I don't know":** Offer 2-3 concrete options and let them react. Reactions reveal preferences without requiring expertise.

**User's answers contradict each other:** Flag it neutrally: *"Earlier you mentioned X, but now Y seems different. Which should we prioritize?"*

**The topic is too broad for one prompt:** Suggest splitting into multiple focused prompts. Run the workflow for each.

## What This Skill Does NOT Do

- Does not execute the improved prompt — it only produces it
- Does not replace domain expertise — it helps extract direction from the user's life context
- Does not guarantee the user will know the "right" answer — it helps them navigate toward one
- Does not loop forever — if 2-3 questions in any phase get "doesn't matter" responses, move on
