# Questioning Guide

Detailed patterns for each of the 5 discovery phases (Phases 2–6 of the brainstorm workflow). Phase 1 (Receive) and Phase 7 (Synthesize) are bookend phases covered in SKILL.md. Read this file when executing the brainstorm workflow to understand the intent, techniques, and examples for each phase.

**Important:** Always use the `ask_user` tool to ask questions — never embed questions in plain text output. When the answer space is predictable, pass a `choices` array for faster UX.

---

## Phase 2 — Goal

**Intent:** Establish a clear, measurable end-state so every subsequent question narrows toward it.

**Key questions to explore (pick the most relevant, ask ONE at a time):**

- What is the single most important outcome you want?
- How would you know this succeeded? What does "done" look like?
- Is there a deadline or milestone that matters?
- Who benefits from this and how?

**Prefer multiple choice when the answer space is predictable:**

- "Which matters more to you?" → A) Speed of delivery B) Quality of result C) Cost efficiency
- "What does success look like?" → A) Revenue target B) User growth C) Personal learning

**Techniques:**

- If the user gives a vague goal ("I want to make money"), ask what "enough" looks like in concrete terms.
- If the goal is a feeling ("I want to feel secure"), translate to observable indicators: "What would need to be true for you to feel secure?"
- Reflect back the goal in one sentence and confirm before moving on.

**Exit criteria:** You can state the goal in one sentence with at least one measurable indicator.

---

## Phase 3 — Direction

**Intent:** Eliminate unsuitable paths WITHOUT requiring domain knowledge from the user. Ask about life, not tech.

**Key questions to explore (pick the most relevant, ask ONE at a time):**

- What must absolutely NOT happen? (deal-breakers, hard constraints)
- What level of risk are you comfortable with? (conservative ↔ aggressive)
- Are there ethical, legal, or personal boundaries?
- Have you tried anything before that didn't work? What went wrong?

**Techniques:**

- Frame questions in everyday language: "Would you be okay losing 30% temporarily?" not "What's your max drawdown tolerance?"
- Use the user's own words — avoid introducing jargon they didn't use.
- Each constraint eliminates branches. Summarize which directions are now ruled out.

**Why this works without domain knowledge:** Constraints, deal-breakers, and risk tolerance are personal — the user is the only source of truth. AI then maps these to domain-specific paths internally.

**Exit criteria:** At least 2-3 constraints that meaningfully narrow the solution space, AND the user has selected from 2-3 proposed approaches.

**Proposing approaches:** After collecting constraints, propose 2-3 viable approaches:

- Lead with your recommended option and explain why
- Include trade-offs for each (what you gain vs. what you give up)
- Frame as multiple choice: "Given your constraints, I see these paths: A) ... B) ... C) ... I'd recommend A because [reason]. Which resonates?"
- The user's reaction to options reveals more than direct questions ever could

---

## Phase 4 — Reference

**Intent:** Ground the work in existing knowledge — either the user's sources or AI-discovered ones.

**Key questions to explore (ask ONE at a time):**

- Do you have any examples, articles, templates, or prior work related to this?
- Is there someone whose approach you admire or want to emulate?
- Have you seen a solution elsewhere that's close to what you want?

**When user has NO references:**

This is the critical case. Use the direction constraints from Phase 3 to search:

1. Summarize what you know so far (goal + constraints)
2. Use `web_search` to find 2-3 high-quality references that fit the constraints
3. Present the references briefly and ask: "Do any of these feel close to what you want?"
4. The user's reaction gives you further directional signal

**When user HAS references:**

- Confirm you can access them (URLs, files, descriptions)
- Ask what specifically they like about the reference — this reveals hidden preferences

**Exit criteria:** At least 1 reference that both parties agree is directionally relevant.

---

## Phase 5 — Context

**Intent:** Surface real-world constraints the user often forgets to mention but that change everything.

**Key questions to explore (pick the most relevant, ask ONE at a time):**

- How much time can you realistically invest in this? (per day/week, total timeline)
- What's your budget or resource limit?
- What skills or tools do you already have? What's new territory?
- Who else is involved? Do you need buy-in from anyone?
- What's your current environment? (technical stack, team size, existing systems)

**Techniques:**

- Ask about reality, not aspirations: "How many hours per week do you actually have free?" not "How much time would you ideally spend?"
- If the user says "I'm flexible" — probe one level deeper. True flexibility is rare.
- Context often contradicts earlier stated goals. If so, flag it gently: "You mentioned wanting X by Y, but with Z hours/week that might be tight. Should we adjust the goal or the timeline?"

**Exit criteria:** Enough practical constraints to distinguish between "theoretically possible" and "actually feasible for this person."

---

## Phase 6 — Criteria

**Intent:** Define what "better" means BEFORE producing output, so quality is measurable.

**Key questions to explore (ask ONE at a time):**

- If you had to pick the top 2-3 things that matter most in the result, what are they?
- What would make you say "this is exactly what I wanted"?
- What would make you reject the result?
- Is there a trade-off you've already decided on? (e.g., speed over quality, simple over comprehensive)

**Techniques:**

- Force-rank if the user gives more than 3 criteria: "If you could only optimize for one, which would it be?"
- Make criteria specific: "easy to use" → "a beginner can follow it in under 10 minutes without external help"
- Record criteria explicitly — they become the evaluation rubric for the output

**Exit criteria:** 2-3 ranked, specific criteria that can be used to evaluate the final output.

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Harmful | What to Do Instead |
|---|---|---|
| Asking multiple questions at once | Overwhelms user, gets shallow answers | Ask ONE question, wait, then follow up |
| Using open-ended when choices exist | Higher cognitive load, slower answers | Offer 2-3 concrete choices when possible |
| Introducing jargon the user didn't use | Makes non-experts feel lost | Mirror the user's vocabulary |
| Skipping to output after Phase 1 | Produces generic answers | Complete all 7 phases |
| Asking domain-specific questions to non-experts | User can't answer, feels stuck | Ask about life/constraints instead |
| Treating "I don't know" as a dead end | Misses opportunity for AI to help | Offer options or search for references |
| Repeating questions already answered | Wastes time, frustrates user | Track what's been established |

---

## Phase Transition Signals

Move to the next phase when:

- The current phase's exit criteria are met
- OR the user explicitly wants to move on (respect their pace)
- OR 2-3 questions in the current phase all get "I don't know" / "doesn't matter" responses

Before transitioning, briefly summarize what was established in the current phase.
