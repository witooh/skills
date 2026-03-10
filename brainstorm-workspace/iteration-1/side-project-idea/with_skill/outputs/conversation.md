# Brainstorm Skill — Simulated Conversation

**User Prompt:** "อยากทำ side project แต่ยังไม่รู้จะทำอะไรดี ช่วยคิดหน่อย"

**Simulated User Persona:** Thai software developer, knows Go and TypeScript, free weekends, budget-conscious, interested in tech.

---

## Phase 1 — Receive

**SKILL:**

เข้าใจครับ คุณอยากทำ side project แต่ยังไม่แน่ใจว่าจะทำอะไรดี — ก่อนที่ผมจะเสนอไอเดีย ขอถามคำถามสัก 2-3 ข้อในแต่ละช่วงเพื่อให้ได้ไอเดียที่เหมาะกับคุณจริง ๆ ไม่ใช่คำตอบแบบกว้าง ๆ ที่ใครก็ตอบได้

เริ่มจากเรื่องเป้าหมายก่อนนะครับ

---

## Phase 2 — Goal

### Question 2.1

**SKILL (ask_user with choices):**

ทำ side project ครั้งนี้ สิ่งที่สำคัญที่สุดสำหรับคุณคืออะไรครับ?

| Choice | Description |
|--------|-------------|
| A | Learn a new skill or technology |
| B | Generate extra income / revenue |
| C | Build something useful for myself or people around me |
| D | Build a portfolio / career credibility |

**USER:**

A กับ C ครับ อยากได้ทั้งเรียนรู้เทคโนโลยีใหม่ ๆ แล้วก็ได้ของที่ใช้ได้จริง

---

### Question 2.2

**SKILL (ask_user, open-ended):**

ถ้าทำเสร็จแล้วจะรู้ได้ยังไงว่า "สำเร็จ" ครับ? เช่น มีคนใช้งานจริงกี่คน หรือ เรียนรู้เทคโนโลยีอะไรได้สำเร็จ หรืออะไรที่เป็นตัววัดได้

**USER:**

ถ้ามีคนใช้ได้จริงสัก 10-50 คนก็ดีใจแล้วครับ แล้วก็ได้ลองเทคโนโลยีที่ยังไม่เคยใช้จริงจัง ๆ สักตัว

---

### Phase 2 Summary

**SKILL:**

สรุป Phase นี้: เป้าหมายของคุณคือ **สร้าง side project ที่มีคนใช้งานจริงประมาณ 10-50 คน และได้เรียนรู้เทคโนโลยีใหม่อย่างน้อย 1 ตัวอย่างจริงจัง** ถูกต้องมั้ยครับ?

**USER:**

ใช่ครับ ตรงเลย

---

## Phase 3 — Direction

### Question 3.1

**SKILL (ask_user with choices):**

มีอะไรที่ "ห้ามเกิดขึ้น" กับ project นี้บ้างมั้ยครับ?

| Choice | Description |
|--------|-------------|
| A | Must not require upfront investment (money) |
| B | Must not consume too much time — cannot affect my main job |
| C | Must not be too complex to maintain alone |
| D | All of the above |

**USER:**

D ครับ ทั้งหมดเลย ไม่อยากลงทุนเยอะ ไม่อยากกระทบงานหลัก แล้วก็ต้อง maintain คนเดียวได้

---

### Question 3.2

**SKILL (ask_user with choices):**

เคยลองทำ side project มาก่อนมั้ยครับ? ถ้าเคย อะไรทำให้หยุดหรือไม่สำเร็จ?

| Choice | Description |
|--------|-------------|
| A | Never tried before |
| B | Tried but lost motivation halfway |
| C | Tried but the scope was too big |
| D | Tried but couldn't find users |

**USER:**

C ครับ เคยลองทำแอปตัวนึง แต่ scope มันบานออกไปเรื่อย ๆ จนท้อเลิก

---

### Proposed Approaches

**SKILL:**

จาก constraints ที่ได้ — ไม่ลงทุน, ไม่กระทบงานหลัก, maintain คนเดียวได้, scope ต้องเล็ก — ผมเห็นทางเลือก 3 แบบครับ:

| Approach | Description | Gain | Give Up |
|----------|-------------|------|---------|
| A (Recommended) | Developer tool / CLI tool — a small, focused utility that solves one specific pain point for developers | Small scope, you control the feature set, easy to deploy, fits Go/TS skill | Smaller user base (niche), less visible to non-dev audience |
| B | SaaS micro-app — a single-feature web app for a broader audience (e.g., a URL shortener with analytics, a bookmark manager) | Potentially more users, learn frontend + backend | More maintenance (hosting, auth, UI), scope creep risk is higher |
| C | Open-source library/package — a reusable module solving a gap you've encountered in your work | Portfolio credibility, low maintenance, zero hosting cost | Harder to get 10-50 "users" who actively rely on it, less tangible product feel |

ผมแนะนำ **A (Developer tool / CLI tool)** เพราะ scope เล็ก ควบคุมได้ ไม่ต้องทำ UI ซับซ้อน แล้ว Go เหมาะกับงาน CLI มาก ๆ

คุณสนใจทางไหนครับ?

**USER:**

A ครับ ชอบไอเดีย CLI tool เพราะตรงกับ Go ที่อยากลองทำอะไรจริงจังด้วย แต่ B ก็น่าสนใจนะ เผื่อจะรวมกันได้ เช่น CLI + web dashboard เล็ก ๆ

---

### Phase 3 Summary

**SKILL:**

สรุป Phase นี้: ทิศทางคือ **Developer-focused CLI tool เขียนด้วย Go** อาจมี web dashboard เล็ก ๆ เสริม constraints สำคัญ: scope เล็ก, ไม่ลงทุน, maintain คนเดียว, เคยมีปัญหา scope creep มาก่อนจึงต้องควบคุม scope อย่างเข้มงวด

---

## Phase 4 — Reference

### Question 4.1

**SKILL (ask_user with choices):**

มี CLI tool หรือ developer tool ตัวไหนที่คุณชอบ หรือรู้สึกว่า "อยากทำแบบนี้" บ้างมั้ยครับ?

| Choice | Description |
|--------|-------------|
| A | Yes — I have some tools in mind |
| B | Not really — help me find references |

**USER:**

A ครับ ชอบ `lazygit` กับ `fzf` ตรงที่มันทำเรื่องเดียวแต่ทำได้ดีมาก แล้วก็ `gh` (GitHub CLI) ที่มันเอา workflow จาก web มาใช้ใน terminal ได้

---

### Question 4.2

**SKILL (ask_user, open-ended):**

สิ่งที่ชอบเกี่ยวกับ tools พวกนี้ ถ้าต้องเลือกมาสัก 2 อย่าง จะเป็นอะไรครับ?

**USER:**

1. ใช้ง่าย ไม่ต้องอ่าน doc เยอะ — เปิดมาก็รู้เลยว่าต้องทำอะไร
2. ทำแค่เรื่องเดียวแต่ทำได้ครบ — ไม่พยายามเป็นทุกอย่าง

---

### Phase 4 Summary

**SKILL:**

สรุป Phase นี้: Reference tools คือ `lazygit`, `fzf`, `gh` — สิ่งที่ชอบคือ **intuitive UX (ใช้ง่ายไม่ต้องอ่าน doc เยอะ)** และ **single-purpose excellence (ทำเรื่องเดียวแต่ทำได้ดี)**

---

## Phase 5 — Context

### Question 5.1

**SKILL (ask_user with choices):**

ในหนึ่งสัปดาห์ คุณมีเวลาว่างจริง ๆ ที่จะใส่ side project ได้ประมาณเท่าไหร่ครับ?

| Choice | Description |
|--------|-------------|
| A | 2-4 hours/week (weekend only, a few hours) |
| B | 5-8 hours/week (half a day on weekend) |
| C | 8-12 hours/week (most of the weekend) |
| D | More than 12 hours/week |

**USER:**

B ครับ ประมาณ 5-8 ชม. ต่อสัปดาห์ ส่วนใหญ่วันเสาร์ครับ

---

### Question 5.2

**SKILL (ask_user with choices):**

เรื่อง tech stack — ตอนนี้ประสบการณ์คุณเป็นยังไงครับ?

| Choice | Description |
|--------|-------------|
| A | Go — experienced, use at work regularly |
| B | Go — used a bit, want to go deeper |
| C | TypeScript — experienced, use at work regularly |
| D | Both Go and TS experienced, want to try something else entirely |

**USER:**

C ครับ TypeScript ใช้ประจำที่ทำงาน ส่วน Go ใช้นิดหน่อย อยากลงลึกกว่านี้ ถือว่าเป็น "เทคโนโลยีใหม่" ที่อยากเรียนรู้

---

### Question 5.3

**SKILL (ask_user with choices):**

เรื่อง budget สำหรับ hosting / infrastructure ยอมจ่ายได้เท่าไหร่ต่อเดือนครับ?

| Choice | Description |
|--------|-------------|
| A | 0 baht — free tier only |
| B | Under 200 baht/month |
| C | 200-500 baht/month |
| D | More than 500 baht/month |

**USER:**

A ครับ ไม่อยากจ่ายเลยถ้าเป็นไปได้ free tier หรือ distribute เป็น binary ให้คนโหลดไปใช้เองก็ได้

---

### Phase 5 Summary

**SKILL:**

สรุป Phase นี้: เวลา **5-8 ชม./สัปดาห์ (วันเสาร์)**, Go เป็นเทคโนโลยีใหม่ที่อยากลงลึก (มีพื้นฐานเล็กน้อย), TypeScript เชี่ยวชาญ, **budget = 0 บาท** — distribute เป็น binary ได้ ไม่จำเป็นต้อง host

ข้อสังเกต: เนื่องจากเวลา 5-8 ชม./สัปดาห์ + เรียนรู้ Go ไปด้วย ควรตั้ง target ว่า MVP ใช้เวลาประมาณ 4-6 สัปดาห์ เพื่อไม่ให้ลากยาวจนหมดแรง — สอดคล้องกับ constraint เรื่อง scope creep ที่เคยเจอ ตกลงมั้ยครับ?

**USER:**

เห็นด้วยครับ 4-6 สัปดาห์ดี ถ้านานกว่านั้นก็น่าจะเริ่มท้อ

---

## Phase 6 — Criteria

### Question 6.1

**SKILL (ask_user with choices):**

ถ้าต้องเลือก 3 อย่างที่สำคัญที่สุดสำหรับ project นี้ คุณจะจัดอันดับยังไงครับ?

| Criteria | Description |
|----------|-------------|
| A | Simplicity — easy to use, minimal features, does one thing well |
| B | Learning value — maximizes what I learn about Go |
| C | Usefulness — actually solves a real problem people have |
| D | Polish — good UX, nice output, feels professional |

เรียงจากสำคัญที่สุดไปน้อยที่สุด 3 ตัว

**USER:**

C > A > B ครับ อยากให้มันมีประโยชน์จริง ๆ ก่อน แล้วก็ต้องใช้ง่าย ส่วนเรื่องเรียนรู้ Go มันได้มาเองอยู่แล้วจากการทำ

---

### Question 6.2

**SKILL (ask_user, open-ended):**

ถ้า project ออกมาแล้วคุณจะ "ไม่พอใจ" เพราะอะไรครับ? อะไรที่จะทำให้รู้สึกว่าเสียเวลา?

**USER:**

ถ้าทำเสร็จแล้วไม่มีใครใช้เลย หรือตัวเองก็ไม่ใช้ นั่นแหละเสียเวลา อีกอย่างคือถ้า scope มันบานจนทำไม่เสร็จเหมือนครั้งก่อน

---

### Phase 6 Summary

**SKILL:**

สรุป Phase นี้: Criteria เรียงตามลำดับ:
1. **Usefulness** — solves a real problem, has actual users (including myself)
2. **Simplicity** — does one thing well, easy to use without reading docs
3. **Learning value** — gain real Go experience (comes naturally from building)

Red flag to avoid: scope creep leading to abandonment, or building something nobody uses.

---

## Phase 7 — Synthesize

**SKILL:**

จากทุก Phase ที่คุยกันมา ผมเขียน Improved Prompt ให้ครับ:

---

## Improved Prompt

I'm a software developer experienced in TypeScript (daily at work) with basic Go knowledge. I want to build a **developer-focused CLI tool written in Go** as a side project. Here are my parameters:

**Goal:** Build a CLI tool that at least 10-50 developers (including myself) actually use, while leveling up my Go skills through real-world practice.

**Constraints:**
- Must be completable as an MVP within 4-6 weekends (5-8 hours/week, Saturdays only)
- Zero budget — no hosting costs; distribute as a compiled binary (e.g., via GitHub Releases, Homebrew tap)
- I will be the sole maintainer — scope must stay tiny and manageable by one person
- I have a history of scope creep killing past projects, so the idea MUST be laser-focused on one specific problem

**Direction:** A single-purpose CLI tool in the style of `lazygit`, `fzf`, or `gh` — intuitive enough to use without reading extensive docs, does one thing but does it thoroughly.

**What I need from you:**
1. Suggest 3-5 specific CLI tool ideas that fit ALL constraints above. For each idea, include:
   - The specific developer pain point it solves
   - Why it's achievable in 4-6 weekends with basic Go knowledge
   - Who the 10-50 target users would be (be specific — not just "developers")
   - One existing tool it's similar to (but differentiated from)
2. For each idea, rate it on: Usefulness (solves a real problem), Simplicity (small scope, one-person maintainable), Learning Value (exercises interesting Go concepts like concurrency, CLI frameworks, file I/O, etc.)
3. Recommend your top pick and explain why

**Do NOT suggest:** generic CRUD apps, todo lists, weather apps, or anything that requires a backend/database/hosting to function.

---

### Discovery Summary

**Goal:** Build a side project CLI tool that gets 10-50 real users and provides hands-on Go learning — measurable by actual adoption and personal skill growth.

**Direction:** Developer-focused CLI tool written in Go, distributed as binary. Inspired by the single-purpose excellence of lazygit/fzf/gh. Chosen over SaaS micro-app (too much maintenance) and open-source library (harder to get tangible users).

**Reference:** lazygit, fzf, gh CLI — valued for intuitive UX and single-purpose focus. The reference pattern is "take a painful workflow and make it effortless in the terminal."

**Context:** 5-8 hours/week (Saturdays only), 4-6 week MVP timeline, zero budget, sole maintainer, TypeScript expert learning Go (basic level), history of scope creep causing project abandonment.

**Criteria (ranked):**
1. Usefulness — must solve a real problem that I and others actually face
2. Simplicity — one feature done well, usable without docs
3. Learning value — exercises meaningful Go patterns (inherent in building any real tool)

---

**SKILL:**

นี่คือ Improved Prompt ที่สรุปจากทุกอย่างที่คุยกันมาครับ ครบถ้วนมั้ยครับ? มีอะไรอยากปรับมั้ย?

**USER:**

ดีมากครับ ครบหมดเลย แค่เพิ่มนิดนึงได้มั้ย — อยากให้เน้นว่าถ้าเป็นไปได้ อยากได้ tool ที่ตัวเองจะใช้ทุกวันในงานด้วย ไม่ใช่แค่ทำเพื่อคนอื่น

---

### Iteration — Incorporating Feedback

**SKILL:**

เพิ่มให้แล้วครับ ตรงส่วน "What I need from you" ข้อ 1 เพิ่มเงื่อนไข:

> **Strong preference:** The tool should solve a pain point I personally face in my daily development workflow — "scratching my own itch" ensures sustained motivation and guarantees at least one real user (me).

**USER:**

เพอร์เฟกต์ครับ ใช้ได้เลย

---

## Final Output

## Improved Prompt

I'm a software developer experienced in TypeScript (daily at work) with basic Go knowledge. I want to build a **developer-focused CLI tool written in Go** as a side project. Here are my parameters:

**Goal:** Build a CLI tool that at least 10-50 developers (including myself) actually use, while leveling up my Go skills through real-world practice.

**Constraints:**
- Must be completable as an MVP within 4-6 weekends (5-8 hours/week, Saturdays only)
- Zero budget — no hosting costs; distribute as a compiled binary (e.g., via GitHub Releases, Homebrew tap)
- I will be the sole maintainer — scope must stay tiny and manageable by one person
- I have a history of scope creep killing past projects, so the idea MUST be laser-focused on one specific problem

**Direction:** A single-purpose CLI tool in the style of `lazygit`, `fzf`, or `gh` — intuitive enough to use without reading extensive docs, does one thing but does it thoroughly.

**What I need from you:**
1. Suggest 3-5 specific CLI tool ideas that fit ALL constraints above. For each idea, include:
   - The specific developer pain point it solves
   - Why it's achievable in 4-6 weekends with basic Go knowledge
   - Who the 10-50 target users would be (be specific — not just "developers")
   - One existing tool it's similar to (but differentiated from)
   - **Strong preference:** The tool should solve a pain point I personally face in my daily development workflow — "scratching my own itch" ensures sustained motivation and guarantees at least one real user (me).
2. For each idea, rate it on: Usefulness (solves a real problem), Simplicity (small scope, one-person maintainable), Learning Value (exercises interesting Go concepts like concurrency, CLI frameworks, file I/O, etc.)
3. Recommend your top pick and explain why

**Do NOT suggest:** generic CRUD apps, todo lists, weather apps, or anything that requires a backend/database/hosting to function.

---

### Discovery Summary

**Goal:** Build a side project CLI tool that gets 10-50 real users and provides hands-on Go learning — measurable by actual adoption and personal skill growth.

**Direction:** Developer-focused CLI tool written in Go, distributed as binary. Inspired by the single-purpose excellence of lazygit/fzf/gh. Chosen over SaaS micro-app (too much maintenance) and open-source library (harder to get tangible users).

**Reference:** lazygit, fzf, gh CLI — valued for intuitive UX and single-purpose focus. The reference pattern is "take a painful workflow and make it effortless in the terminal."

**Context:** 5-8 hours/week (Saturdays only), 4-6 week MVP timeline, zero budget, sole maintainer, TypeScript expert learning Go (basic level), history of scope creep causing project abandonment.

**Criteria (ranked):**
1. Usefulness — must solve a real problem that I and others actually face (strong preference for "scratch my own itch")
2. Simplicity — one feature done well, usable without docs
3. Learning value — exercises meaningful Go patterns (inherent in building any real tool)

---

## Next Step

**SKILL (ask_user with choices):**

ต่อไปคุณอยากทำอะไรครับ?

| Choice | Description |
|--------|-------------|
| A | Create a Plan — let me build a step-by-step implementation plan for you |
| B | Done — I'll take it from here |

**USER:**

B ครับ ขอเอา prompt นี้ไปลองใช้ก่อน ขอบคุณมากครับ!

**SKILL:**

ได้เลยครับ! เอา Improved Prompt ด้านบนไปใช้กับ AI ตัวไหนก็ได้ จะได้คำตอบที่ตรงกับสถานการณ์ของคุณมากกว่าถามแบบกว้าง ๆ แน่นอนครับ ขอให้สนุกกับ side project!

---

## Observation Notes (for skill evaluation)

| Aspect | Observation |
|--------|-------------|
| Total questions asked | 11 questions across Phases 2-6 (within the 2-3 per phase budget) |
| Multiple choice usage | 8 out of 11 questions used choices — good ratio |
| Open-ended questions | 3 (Phase 2.2, 4.2, 6.2) — used appropriately where answers were unpredictable |
| Phase transitions | Each phase ended with a summary before moving on |
| Jargon avoidance | Maintained user's language level throughout; no unnecessary technical terms introduced |
| Constraint discovery | Identified: zero budget, sole maintainer, scope creep history, weekend-only time, Go as learning target |
| Direction proposal | Offered 3 approaches with trade-offs, led with recommendation — user's reaction refined direction further (CLI + possible dashboard) |
| Reference handling | User had references; follow-up extracted hidden preferences (intuitive UX, single-purpose) |
| Context-goal conflict detection | Flagged time constraint vs. ambition, proposed 4-6 week MVP timeline |
| Iteration | User requested one addition after synthesis; incorporated cleanly |
| Final prompt quality | Self-contained, specific, includes all constraints inline, actionable by any AI |
