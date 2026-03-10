# Brainstorm Skill Simulation: Landing Page Prompt

**User Prompt:** "ช่วยคิด prompt สำหรับสร้าง landing page ให้หน่อย จะใช้ Claude สร้าง"
**Date:** 2026-03-10

---

## Triage Decision (Internal)

**Analysis of user request:**
- User explicitly says "ช่วยคิด prompt" -- wants to create a prompt
- Mentions using Claude to generate the output -- the prompt is for another AI
- Signal matches: "ช่วยคิด prompt" is a direct match for Prompt Mode

**Mode Selected: Prompt Mode**
**Rationale:** User explicitly wants to craft a prompt for Claude to generate a landing page. This is a prompt improvement request, not open-ended brainstorming or a focused technical problem. Full discovery flow (5-7 questions) applies.

---

## Phase 1 -- Receive

**SKILL:**

ได้เลยครับ ผมจะช่วยสร้าง prompt สำหรับทำ landing page ให้ดีที่สุด ขอถามอีกสักสองสามข้อเพื่อให้ prompt ตรงกับสิ่งที่ต้องการจริงๆ นะครับ

---

## Phase 2 -- Goal (1 question)

**SKILL asks via `AskUserQuestion`:**

> Landing page นี้ต้องทำอะไรให้สำเร็จเป็นหลัก?
>
> **Options:**
> A) ให้คนสมัครใช้งาน (sign-up / waitlist)
> B) ให้คนซื้อสินค้าหรือบริการ
> C) ให้คนติดต่อเข้ามา (lead generation)
> D) อย่างอื่น (ระบุได้เลย)

**USER:**

> A ครับ อยากให้คนสมัคร waitlist ก่อน เพราะตัว product ยังไม่เสร็จ เป็น SaaS ระบบ POS สำหรับร้านอาหาร

**SKILL (internal):** Goal established -- "ให้เจ้าของร้านอาหารสมัคร waitlist สำหรับ SaaS POS system" Measurable indicator: waitlist sign-up conversion. Moving to Direction phase.

---

## Phase 3 -- Direction (2 questions + proposal)

### Question 1 -- Constraints / Deal-breakers

**SKILL asks via `AskUserQuestion`:**

> มีอะไรที่ landing page นี้ห้ามเป็นเด็ดขาดไหมครับ? เช่น ไม่อยากได้แบบที่ดูเหมือนเว็บขายตรง หรือไม่อยากมีข้อมูลมากเกินไป

**USER:**

> ไม่อยากให้ดูเหมือนเว็บขายของถูกๆ ครับ อยากให้ดู modern และ clean ไม่ต้องยาวมาก ไม่อยากให้มี pop-up รบกวน target เป็นร้านอาหารเล็กๆ ในไทย เจ้าของร้านอาจจะไม่ค่อย tech-savvy

### Question 2 -- Approach Proposal

**SKILL asks via `AskUserQuestion`:**

> จากที่บอกมา ผมเห็นทางเลือกหลักๆ 3 แบบ:
>
> **Options:**
> A) **Single-page hero + benefits + CTA** -- หน้าเดียวสั้นกระชับ เน้น hero section สวยๆ ตามด้วย 3-4 benefits แล้วจบด้วย waitlist form เหมาะกับ target ที่ไม่ค่อยอ่านเยอะ (แนะนำ)
> B) **Multi-section storytelling** -- เล่าปัญหาของเจ้าของร้าน แล้วค่อยนำเสนอ solution มี social proof, pricing preview ยาวกว่าแต่ persuasive กว่า
> C) **Minimal teaser** -- แค่ logo, tagline สั้นๆ กับ email form สร้างไว แต่ conversion อาจต่ำเพราะข้อมูลน้อย
>
> ผมแนะนำ A เพราะ target เป็นเจ้าของร้านที่ยุ่งและไม่ค่อยอยากอ่านเยอะ แต่ยังได้ข้อมูลพอให้ตัดสินใจ -- ชอบแบบไหนครับ?

**USER:**

> A ครับ ชอบแบบสั้นกระชับ แต่อยากมี section เล็กๆ สัก 1-2 อันที่บอก pain point ของเจ้าของร้านด้วย ให้รู้สึกว่าเข้าใจปัญหาเขา

**SKILL (internal):** Direction locked -- single-page with hero, pain points, benefits, CTA. Constraints: modern/clean, no pop-ups, not too long, Thai small restaurant owners (not tech-savvy). User wants pain point acknowledgment. Moving to Reference phase (relevant since this is a design/style request).

---

## Phase 4 -- Reference (1 question)

**SKILL asks via `AskUserQuestion`:**

> มีเว็บ landing page หรือ SaaS ไหนที่ชอบ style ของเขาไหมครับ? จะได้ใส่เป็น reference ใน prompt ด้วย
>
> **Options:**
> A) มี -- บอกได้เลย
> B) ไม่มี -- ช่วยหาให้

**USER:**

> ชอบ style ของ Notion กับ Linear ครับ clean ดี typography สวย

**SKILL (internal):** References established -- Notion-style and Linear-style aesthetics (clean layout, strong typography, generous whitespace). No need to WebSearch. Moving to Context phase.

---

## Phase 5 -- Context (1 question)

**SKILL asks via `AskUserQuestion`:**

> เรื่อง tech stack กับ timeline -- ถูกต้องไหมครับ?
>
> **Options:**
> A) ใช้ React/Next.js, ต้องเสร็จใน 1-2 สัปดาห์
> B) ใช้ React/Next.js แต่ยังไม่มี deadline
> C) ยังไม่แน่ใจ tech stack
> D) อย่างอื่น (ระบุได้)

**USER:**

> A ครับ ใช้ Next.js อยู่แล้ว ต้อง launch ใน 2 สัปดาห์ ทำคนเดียว

**SKILL (internal):** Context locked -- Next.js, solo developer, 2-week deadline. This means the prompt should produce code-ready output, not just a design mockup. The tight timeline means Claude should generate actual components. Moving to Criteria phase.

---

## Phase 6 -- Criteria (1 question)

**SKILL asks via `AskUserQuestion`:**

> ถ้าต้องจัดลำดับความสำคัญ 3 อย่างนี้ -- เรียงจากสำคัญสุดไปน้อยสุดจะเป็นยังไงครับ?
>
> **Options:**
> A) Design สวย > Conversion สูง > Code quality ดี
> B) Conversion สูง > Design สวย > Code quality ดี
> C) Code quality ดี > Design สวย > Conversion สูง
> D) เรียงแบบอื่น (ระบุได้)

**USER:**

> B ครับ Conversion สำคัญสุด แล้วก็ design สวยรองลงมา code quality ไว้ refactor ทีหลังได้

**SKILL (internal):** Criteria ranked: 1. Conversion rate 2. Visual design (modern/clean) 3. Code quality (acceptable, not priority). All phases complete. Moving to Synthesize.

---

## Phase 7 -- Synthesize

**SKILL:**

ได้ครบแล้วครับ นี่คือ prompt ที่ refined แล้ว:

---

## Improved Prompt

```
สร้าง landing page สำหรับ SaaS ระบบ POS ร้านอาหาร ด้วย Next.js (App Router) + Tailwind CSS

## บริบท
- Product: ระบบ POS สำหรับร้านอาหารขนาดเล็กในไทย (ยังอยู่ในช่วง pre-launch, เปิดรับ waitlist)
- Target audience: เจ้าของร้านอาหารเล็กๆ ในไทย อายุ 30-55 ปี ไม่ค่อย tech-savvy
- ชื่อ product: [ใส่ชื่อ]
- Tagline: [ใส่ tagline]

## โครงสร้างหน้า (single-page, scroll)

### 1. Hero Section
- Headline ภาษาไทยที่สื่อ value proposition หลัก -- เน้นความง่ายในการจัดการร้าน
- Sub-headline 1 บรรทัด ขยายความ
- CTA button "สมัคร Waitlist" ที่โดดเด่น
- ภาพ mockup ของระบบ (ใช้ placeholder image พร้อม comment บอกขนาด)

### 2. Pain Points Section
- หัวข้อที่ทำให้เจ้าของร้านรู้สึกว่า "นี่คือปัญหาของเรา"
- แสดง 3 pain points หลักเป็น card:
  1. จดออเดอร์ผิด / ตกหล่น
  2. สรุปยอดขายปลายวันวุ่นวาย
  3. ไม่รู้ว่าเมนูไหนขายดี เมนูไหนควรเลิก
- ใช้ icon + ข้อความสั้น ไม่เกิน 2 บรรทัดต่อ card

### 3. Benefits / Solution Section
- แสดง 3-4 benefits ที่ตอบ pain points ด้านบน
- แต่ละ benefit มี icon, หัวข้อสั้น, คำอธิบาย 1 บรรทัด
- เน้นภาษาง่ายๆ ที่เจ้าของร้านเข้าใจ ไม่ใช้ศัพท์ tech

### 4. CTA / Waitlist Section
- Form มีแค่ 2 fields: ชื่อร้าน + เบอร์โทร (หรือ LINE ID)
- ข้อความสั้นบอกว่าสมัครแล้วได้อะไร (เช่น "ทดลองใช้ฟรี 3 เดือนแรก")
- CTA button ชัดเจน
- ไม่มี pop-up ใดๆ ทั้งสิ้น

### 5. Footer
- ชื่อบริษัท, ช่องทางติดต่อ, link โซเชียล
- Minimal -- ไม่ต้องมีลิงก์เยอะ

## Design Requirements
- Style: Modern, clean คล้าย Notion / Linear -- generous whitespace, typography ชัดเจน
- Font: ใช้ Google Fonts ที่รองรับภาษาไทย (เช่น Noto Sans Thai + Inter)
- Color palette: สร้าง palette ที่ดู professional ไม่ฉูดฉาด โทนสีหลัก 1 สี + neutral
- Fully responsive (mobile-first เพราะ target มักใช้มือถือ)
- Smooth scroll behavior

## Technical Requirements
- Next.js 14+ App Router
- Tailwind CSS
- TypeScript
- Component structure แยกเป็น section components
- Waitlist form ใช้ Server Action หรือ API route (เก็บลง database -- ใส่ TODO comment ตรง DB logic)
- SEO: meta tags ภาษาไทย, Open Graph tags
- ทำ placeholder สำหรับรูปภาพทั้งหมด พร้อม comment บอกว่าควรใช้รูปแบบไหน

## สิ่งที่ไม่ต้องมี
- ไม่มี pop-up, modal, หรือ overlay ใดๆ
- ไม่มี animation ซับซ้อน (แค่ subtle fade-in ได้)
- ไม่มี pricing section (ยังไม่พร้อมประกาศราคา)
- ไม่ต้อง integrate analytics ตอนนี้

## สิ่งที่ต้อง output
- ไฟล์ page.tsx หลัก
- Component files แยกตาม section
- globals.css (ถ้าต้อง customize เพิ่มจาก Tailwind)
- tailwind.config.ts (ถ้าต้อง extend theme)
```

---

### Discovery Summary

| Dimension | Detail |
|-----------|--------|
| **Goal** | Drive waitlist sign-ups for a pre-launch restaurant POS SaaS targeting small Thai restaurants |
| **Direction** | Single-page hero + pain points + benefits + CTA; short and scannable for non-tech-savvy audience |
| **Reference** | Notion / Linear aesthetic -- clean, generous whitespace, strong typography |
| **Context** | Solo developer, Next.js stack, 2-week launch deadline |
| **Criteria** | 1. Conversion rate 2. Visual design (modern/clean) 3. Code quality (acceptable) |

---

ครบแล้วครับ prompt นี้น่าจะให้ Claude สร้าง landing page ที่ตรงกับที่ต้องการได้เลย มีอะไรอยากปรับไหมครับ?

---

## User Response to Final Output

**USER:**

> ดีมากครับ ชอบเลย แค่อยากเพิ่ม section สั้นๆ เรื่อง "ทำไมต้องเรา" สัก 2-3 bullet ได้ไหม

---

## Iteration

**SKILL:**

ได้เลยครับ เพิ่มให้แล้ว:

*(Added between Benefits and CTA sections in the prompt):*

```
### 3.5. Why Us Section (สั้นๆ)
- 2-3 bullet points เช่น:
  - "ออกแบบมาเพื่อร้านอาหารเล็กโดยเฉพาะ ไม่มี feature เกินจำเป็น"
  - "ใช้ได้เลยไม่ต้องติดตั้งเครื่อง -- แค่มีมือถือหรือ tablet"
  - "ทีมพัฒนาคนไทย support ภาษาไทย"
- Layout: simple list หรือ minimal cards
```

ตอนนี้ prompt พร้อมใช้แล้วครับ อยากให้ทำอะไรต่อไหม?

> **Options:**
> A) สร้าง implementation plan
> B) ลงลึกเรื่องอื่นเพิ่ม
> C) เอา prompt นี้ไปใช้ได้เลย

**USER:**

> C ครับ ขอบคุณมากครับ

---

## End of Simulation

---

## Observation Table

| Metric | Value |
|--------|-------|
| **Mode Selected** | Prompt Mode |
| **Triage Accuracy** | Correct -- user explicitly said "ช่วยคิด prompt" which is a direct Prompt Mode signal |
| **Total Questions Asked** | 6 (Goal: 1, Direction: 2, Reference: 1, Context: 1, Criteria: 1) |
| **Questions with Multiple Choice** | 6/6 (100%) |
| **Phases Executed** | All 7 (Receive, Goal, Direction, Reference, Context, Criteria, Synthesize) |
| **Reference Phase** | Included (appropriate -- design/style request for a landing page) |
| **Time-to-Value** | 6 questions before final output -- within the 5-7 range specified for Prompt Mode |
| **Iteration Rounds** | 1 (user requested minor addition, handled cleanly) |
| **Output Format** | Improved Prompt + Discovery Summary -- matches Prompt Mode spec |
| **Prompt Self-Contained** | Yes -- all constraints, design refs, tech stack, exclusions baked into the prompt |
| **Language Mirroring** | Skill used Thai throughout, matched user's casual tone, avoided jargon |
| **Information Reuse** | Good -- no questions re-asked what user already provided (e.g., POS, restaurant, Thai market extracted from answers, not re-asked) |

### Strengths Observed

| Strength | Evidence |
|----------|----------|
| Triage was instant and correct | "ช่วยคิด prompt" mapped directly to Prompt Mode without ambiguity |
| Multiple choice reduced friction | Every question offered options, user could answer in 1-2 words each time |
| Pain point section was user-driven | User asked for it in Direction phase, skill incorporated it naturally |
| Prompt output is production-ready | Includes file structure, tech constraints, anti-requirements, and placeholder guidance |
| Appropriate phase inclusion | Reference phase was included because this is a design request (per QUESTIONING-GUIDE.md) |

### Potential Improvements

| Area | Observation |
|------|-------------|
| Context question was leading | The skill guessed "React/Next.js, 1-2 weeks" as option A -- this happened to be correct but could bias the user. An open-ended "What's your tech stack and timeline?" might be more neutral |
| Product name not collected | The prompt has `[ใส่ชื่อ]` placeholder -- could have asked during discovery |
| No WebSearch used | Could have searched for competitor POS landing pages as additional reference, though user already had clear style preferences so this was arguably correct to skip |
