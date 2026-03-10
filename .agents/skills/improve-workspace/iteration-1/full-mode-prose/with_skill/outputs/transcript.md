# Improve Skill — Transcript

## Mode Selection

**User request:** "ช่วย improve README นี้หน่อย มันยาวเกิน อ่านไม่รู้เรื่อง แล้วก็ structure ไม่ดี"

**Analysis:** The user mentions multiple dimensions — length (conciseness), readability (clarity), and structure. This involves competing tradeoffs and multiple quality dimensions.

**Decision: Full Mode** — Multiple criteria (clarity, conciseness, structure) need to be balanced. Quick Mode is insufficient.

---

## Step 1 — Receive

Received: `README.md` for "My Project" — a web application with Go backend, React frontend, PostgreSQL database, and Redis caching.

**Observations on input:**
- 111 lines
- Vague project name and description ("a project that does stuff")
- Installation section is rambling, self-contradictory (install PostgreSQL / actually don't)
- Environment variables lack structure and grouping
- API endpoints are a flat, undifferentiated list
- No quick-start or TL;DR
- Team section is low-value for a README
- Overall tone is informal and stream-of-consciousness

---

## Step 2 — Establish Criteria

**What I would ask the user:**
> "You mentioned three things: too long, hard to understand, and bad structure. I'd suggest these as our ranked criteria:
>
> 1. **Clarity** — A new team member can understand what the project does and how to get started in under 2 minutes of reading
> 2. **Structure** — Information is logically grouped with clear hierarchy; a reader can jump to any section without reading top-to-bottom
> 3. **Conciseness** — Under 80 lines with no redundant or self-contradictory content
>
> Does this ranking match your priorities? Anything to add or change?"

**Assumed user response:** "Yes, that looks good. Go ahead."

### Final Criteria (Ranked)

| Rank | Criterion | Observable Target |
|---|---|---|
| 1 | Clarity | A new team member understands project purpose and can start in under 2 min |
| 2 | Structure | Logical grouping, clear hierarchy, scannable sections with jump-to navigation |
| 3 | Conciseness | Under 80 lines, no redundant or contradictory content |

---

## Step 3 — Capture Baseline (Iteration 0)

Scoring the original README against established criteria.

### Iteration 0 — Baseline

| Criterion | Score | Evidence |
|---|---|---|
| Clarity | 0 / 2 | Project description is "does stuff". Installation rambles and contradicts itself. No clear purpose statement. Reader cannot determine what this project is for. |
| Structure | 1 / 2 | Has section headings (About, Install, Run, etc.) which is basic structure. But sections aren't logically grouped — env vars are separate from installation, API is a flat list, no table of contents. |
| Conciseness | 0 / 2 | 111 lines. Installation section is stream-of-consciousness. Env vars repeat "for sending emails" four times. API is a flat dump of every endpoint with no grouping. Team section adds no operational value. |

**Total: 1 / 6**
**Key gaps:** Clarity (0) and Conciseness (0) are the biggest problems. Structure is partially there but needs significant improvement.

---

## Step 4 — Iteration 1

**Target: Clarity (score 0 — largest gap, highest-ranked criterion)**

**What I'm changing and why:**
The biggest clarity problem is that the reader has no idea what this project IS. The title is "My Project", the description says "does stuff", and the About section buries the tech stack in a run-on sentence. I will:
- Write a clear, specific project description
- Add a concise tech stack overview
- Rewrite the installation section to remove contradictions and present steps clearly

### Iteration 1 — Scorecard

**Changes made:** Rewrote project description to be specific, added structured tech stack, rewrote installation as clear numbered steps without contradictions.

| Criterion | Previous | Current | Delta |
|---|---|---|---|
| Clarity | 0 | 2 | +2 |
| Structure | 1 | 1 | 0 |
| Conciseness | 0 | 0 | 0 |

**Total: 3 / 6 (was: 1 / 6, delta: +2)**

**What I would ask the user:**
> "Clarity is now addressed — the project purpose and setup are clear. Structure and conciseness are still gaps. Does this score look right to you?"

**Assumed user response:** "Looks right. Keep going."

**Remaining gaps:** Structure (1) and Conciseness (0)
**Next action:** Target Conciseness (score 0, second-largest gap)

---

## Step 5 — Iteration 2

**Target: Conciseness (score 0 — largest remaining gap)**

**What I'm changing and why:**
The README is bloated. Specific cuts:
- Remove Team section (belongs in CONTRIBUTING.md or org chart, not README)
- Group env vars into a table, remove repetitive descriptions
- Group API endpoints by resource in collapsed/summary tables instead of flat list
- Trim redundant wording throughout

### Iteration 2 — Scorecard

**Changes made:** Removed Team section, converted env vars to a grouped table, grouped API endpoints by resource, trimmed redundant text throughout.

| Criterion | Previous | Current | Delta |
|---|---|---|---|
| Clarity | 2 | 2 | 0 |
| Structure | 1 | 1 | 0 |
| Conciseness | 0 | 2 | +2 |

**Total: 5 / 6 (was: 3 / 6, delta: +2)**

**What I would ask the user:**
> "Conciseness is now addressed — we're well under 80 lines with no redundancy. Clarity remains solid. Structure is the last gap. Does this score look right?"

**Assumed user response:** "Yes, structure still needs work."

**Remaining gaps:** Structure (1)
**Next action:** Target Structure (score 1, the only remaining gap)

---

## Step 6 — Iteration 3

**Target: Structure (score 1 — only remaining gap)**

**What I'm changing and why:**
The document needs a logical hierarchy that lets readers jump to what they need. I will:
- Reorder sections in the reader's natural flow: What is it → Prerequisites → Quick Start → Config → API → Testing → Deployment → Contributing
- Use consistent heading levels
- Make sections self-contained so readers can skip sections

### Iteration 3 — Scorecard

**Changes made:** Reordered sections to match reader flow (what → setup → use → develop → deploy). Made sections self-contained. Used consistent heading hierarchy.

| Criterion | Previous | Current | Delta |
|---|---|---|---|
| Clarity | 2 | 2 | 0 |
| Structure | 1 | 2 | +1 |
| Conciseness | 2 | 2 | 0 |

**Total: 6 / 6 (was: 5 / 6, delta: +1)**

**What I would ask the user:**
> "All three criteria are now met. Here's the final scorecard — does this match your assessment?"

**Assumed user response:** "Looks great!"

**No regressions detected.** All criteria met.

---

## Step 7 — Deliver

### Completion Condition Met

All criteria scored 2/2. Loop complete after 3 iterations.

### Iteration History

| Iteration | Change | Total Score | Delta |
|---|---|---|---|
| 0 (Baseline) | -- | 1 / 6 | -- |
| 1 | Rewrote project description, tech stack, and installation for clarity | 3 / 6 | +2 |
| 2 | Removed bloat, grouped env vars and API endpoints, trimmed redundancy | 5 / 6 | +2 |
| 3 | Reordered sections to logical flow, consistent hierarchy | 6 / 6 | +1 |

**Final Score: 6 / 6**
**Criteria met:** Clarity, Structure, Conciseness
**Criteria not met:** None

### Final Output

See `improved.md` for the complete improved README.
