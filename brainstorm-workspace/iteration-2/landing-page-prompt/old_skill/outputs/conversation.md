# Old Skill Simulation: Landing Page Prompt Brainstorm

**Skill Version:** 1.2 (snapshot)
**User Prompt:** "ช่วยคิด prompt สำหรับสร้าง landing page ให้หน่อย จะใช้ Claude สร้าง"
**Simulated User Profile:** SaaS product for restaurant POS system, targeting small restaurants in Thailand, wants modern/clean design, knows React/Next.js, launch in 2 weeks

---

## Phase 1 — Receive

**SKILL:**

เข้าใจครับ คุณต้องการ prompt ที่ดีสำหรับให้ Claude ช่วยสร้าง landing page ก่อนที่ผมจะช่วยเขียน prompt ให้ ผมขอถามคำถามสักหน่อยเพื่อให้ prompt ที่ได้ตรงกับสถานการณ์ของคุณจริงๆ ไม่ใช่ได้ผลลัพธ์กว้างๆ ทั่วไป มาเริ่มจากเป้าหมายของคุณกันก่อนครับ

---

## Phase 2 — Goal

### Question 2.1

**SKILL (ask_user with choices):**

Landing page นี้ สิ่งที่สำคัญที่สุดที่คุณต้องการคืออะไร?

| Choice | Description |
|--------|-------------|
| A | Get users to sign up / register |
| B | Explain the product so people understand what it does |
| C | Build credibility and trust before launch |
| D | Other (please specify) |

**USER:**

A ครับ ต้องการให้คนสมัครใช้งาน เพราะกำลังจะ launch ระบบ POS สำหรับร้านอาหาร

### Question 2.2

**SKILL (ask_user with choices):**

เข้าใจครับ เป็นระบบ POS สำหรับร้านอาหาร แล้วคุณจะรู้ได้ยังไงว่า landing page นี้สำเร็จ?

| Choice | Description |
|--------|-------------|
| A | Number of signups (e.g., 100 signups in first month) |
| B | Conversion rate from visitor to signup |
| C | Number of demo requests / contact form submissions |
| D | Other metric |

**USER:**

A ครับ ต้องการอย่างน้อย 100 signups ในเดือนแรก เพราะจะใช้เป็น early adopter

### Question 2.3

**SKILL (ask_user):**

กลุ่มเป้าหมายที่จะ sign up คือใครครับ?

| Choice | Description |
|--------|-------------|
| A | Small restaurant owners (1-5 branches) |
| B | Medium restaurant chains (5-20 branches) |
| C | Food trucks / street food vendors |
| D | All types of food businesses |

**USER:**

A ครับ ร้านอาหารขนาดเล็กในไทย 1-5 สาขา เจ้าของร้านเป็นคนตัดสินใจเอง

**SKILL (Phase 2 Summary):**

สรุป Phase Goal:
- **เป้าหมาย:** สร้าง landing page สำหรับระบบ POS ร้านอาหาร เพื่อให้ได้ signups อย่างน้อย 100 ราย ในเดือนแรก
- **กลุ่มเป้าหมาย:** เจ้าของร้านอาหารขนาดเล็กในไทย (1-5 สาขา)
- **Measurable indicator:** 100 signups ภายใน 1 เดือนแรกหลัง launch

ถูกต้องไหมครับ?

**USER:**

ถูกต้องครับ

---

## Phase 3 — Direction

### Question 3.1

**SKILL (ask_user with choices):**

มีอะไรที่ landing page นี้ **ต้องไม่ทำ** หรือ **ต้องหลีกเลี่ยง** ไหมครับ?

| Choice | Description |
|--------|-------------|
| A | Must NOT look too technical / complicated — target users are not tech-savvy |
| B | Must NOT require credit card for signup |
| C | Must NOT be too long — users won't scroll much |
| D | All of the above |
| E | Other |

**USER:**

D ครับ ทั้งหมดเลย เจ้าของร้านอาหารส่วนใหญ่ไม่ได้เก่งเทค ต้องดูง่ายๆ ไม่ต้องใส่บัตรเครดิต แล้วก็ไม่ยาวเกินไป

### Question 3.2

**SKILL (ask_user with choices):**

เคยลองทำ landing page มาก่อนไหมครับ? มีอะไรที่ไม่ work?

| Choice | Description |
|--------|-------------|
| A | Never made one before — this is the first time |
| B | Made one before but conversion was low |
| C | Made one before but it took too long to build |
| D | Other |

**USER:**

A ครับ ครั้งแรกเลย

### Question 3.3 — Proposing Approaches

**SKILL (ask_user with choices):**

จากข้อมูลที่ได้ ผมเห็นทาง 3 ทางครับ:

| Choice | Approach | Trade-off |
|--------|----------|-----------|
| A (Recommended) | Single-page with hero + features + social proof + CTA — focused, fast to build, mobile-first | Covers essentials but no deep product demo |
| B | Multi-section long-form with detailed product walkthrough + comparison table + FAQ | More complete info but longer build time and users may not scroll |
| C | Minimal teaser page with waitlist signup + countdown timer | Fastest to build but relies on hype, less info for decision-making |

ผมแนะนำ A ครับ เพราะกลุ่มเป้าหมายไม่ได้อยากอ่านเยอะ ต้องการเห็นชัดเจนว่ามันคืออะไร แล้วก็สมัครได้เลย อันไหนตรงกับที่คุณคิดครับ?

**USER:**

A ครับ ตรงเลย ต้องการแบบกระชับ ดูดี สมัครง่าย

**SKILL (Phase 3 Summary):**

สรุป Phase Direction:
- **Deal-breakers:** ห้ามดูซับซ้อน, ไม่ต้องใส่บัตรเครดิต, ไม่ยาวเกินไป
- **Approach:** Single-page, hero + features + social proof + CTA, mobile-first
- **Ruled out:** Long-form walkthrough (ไม่ตรงกับ user ที่ไม่ scroll), Teaser page (ข้อมูลน้อยเกินไปสำหรับการตัดสินใจ)

---

## Phase 4 — Reference

### Question 4.1

**SKILL (ask_user with choices):**

คุณมีตัวอย่าง landing page ที่ชอบ หรือ website ที่รู้สึกว่า "แบบนี้แหละ" ไหมครับ?

| Choice | Description |
|--------|-------------|
| A | Yes, I have examples I like |
| B | No, but I know the style I want |
| C | No idea — please find some for me |

**USER:**

B ครับ ไม่มีตัวอย่างตรงๆ แต่ชอบสไตล์ modern, clean, minimal สีไม่ฉูดฉาด

### Question 4.2

**SKILL (ask_user with choices):**

สไตล์ modern/clean/minimal ที่ว่า ใกล้เคียงกับแนวไหนมากกว่าครับ?

| Choice | Description |
|--------|-------------|
| A | Apple-style — lots of white space, large typography, premium feel |
| B | Stripe-style — gradient accents, clean layout, developer-friendly |
| C | Notion-style — simple illustrations, friendly, approachable |
| D | Linear-style — dark theme, sleek, modern SaaS |

**USER:**

C ครับ แนว Notion ดี ดูเป็นมิตร เข้าใจง่าย เหมาะกับกลุ่มเป้าหมาย

**SKILL:**

ผมจะ search หาตัวอย่างที่ใกล้เคียงให้ครับ

*(web_search: "SaaS landing page Notion style friendly minimal restaurant POS")*

ผมเจอตัวอย่างที่น่าสนใจ:

1. **Square for Restaurants** (squareup.com) — clean, simple messaging, focused on small business owners
2. **Toast POS** (toasttab.com) — friendly tone, clear feature sections, strong social proof
3. **Loyverse POS** (loyverse.com) — minimal design, free tier emphasis, easy signup flow

มีอันไหนที่รู้สึกว่าใกล้เคียงไหมครับ?

**USER:**

Square ดีครับ ชอบที่มันดูง่ายและ messaging ชัดเจน แต่อยากให้ดู Thai-friendly กว่านี้

**SKILL (Phase 4 Summary):**

สรุป Phase Reference:
- **Design style:** Notion-like — friendly, approachable, simple illustrations
- **Reference point:** Square for Restaurants (messaging clarity, simplicity)
- **Adaptation:** Thai-friendly tone and design

---

## Phase 5 — Context

### Question 5.1

**SKILL (ask_user with choices):**

คุณมีเวลาทำ landing page นี้จริงๆ เท่าไหร่ครับ?

| Choice | Description |
|--------|-------------|
| A | A few days (this week) |
| B | 1-2 weeks |
| C | About a month |
| D | No specific deadline |

**USER:**

B ครับ ประมาณ 2 สัปดาห์ เพราะจะ launch product ด้วย

### Question 5.2

**SKILL (ask_user with choices):**

เครื่องมือที่จะใช้สร้าง landing page มีความถนัดอะไรบ้างครับ?

| Choice | Description |
|--------|-------------|
| A | No-code tools (Webflow, Wix, Squarespace) |
| B | React / Next.js |
| C | HTML/CSS/JS basics |
| D | WordPress |
| E | Other |

**USER:**

B ครับ ถนัด React/Next.js อยู่แล้ว จะ code เอง

### Question 5.3

**SKILL (ask_user with choices):**

มีใครอื่นที่ต้องเห็นด้วยกับ landing page นี้ไหมครับ? (co-founder, designer, etc.)

| Choice | Description |
|--------|-------------|
| A | Just me — I decide everything |
| B | Need approval from 1-2 people |
| C | Team decision |

**USER:**

A ครับ ตัดสินใจเองได้เลย

**SKILL (Phase 5 Summary):**

สรุป Phase Context:
- **Timeline:** 2 weeks (launching product simultaneously)
- **Tech stack:** React/Next.js, coding from scratch
- **Team:** Solo decision-maker
- **Budget implication:** No design team, relying on Claude to generate code

---

## Phase 6 — Criteria

### Question 6.1

**SKILL (ask_user with choices):**

ถ้าต้องเลือก 2 อย่างที่สำคัญที่สุดสำหรับ landing page นี้ คุณจะเลือกอะไรครับ?

| Choice | Description |
|--------|-------------|
| A | Looks professional and trustworthy |
| B | Fast to build (code-ready output from Claude) |
| C | High conversion rate (optimized for signups) |
| D | Easy to maintain and update later |
| E | Mobile-friendly / responsive |

**USER:**

B กับ C ครับ อยากให้ Claude ให้โค้ดที่ใช้ได้เลย แล้วก็ต้อง optimize ให้คน sign up เยอะ

### Question 6.2

**SKILL (ask_user):**

ระหว่าง B กับ C ถ้าต้องเลือก 1 ที่สำคัญกว่า อันไหนครับ?

| Choice | Description |
|--------|-------------|
| A | Fast to build — need working code ASAP |
| B | High conversion — even if it takes more iteration |

**USER:**

A ครับ ต้อง ship ให้ทัน ถ้าได้โค้ดที่ใช้ได้เลยจะดีมาก conversion ค่อยปรับทีหลังได้

### Question 6.3

**SKILL (ask_user):**

อะไรจะทำให้คุณ reject ผลลัพธ์ที่ได้จาก prompt นี้ครับ?

| Choice | Description |
|--------|-------------|
| A | Code doesn't work / has errors |
| B | Design looks outdated or ugly |
| C | Content/copy doesn't make sense for Thai market |
| D | Too generic — looks like any random SaaS page |

**USER:**

A กับ D ครับ ต้องใช้ได้จริง แล้วก็ต้องดูเหมือน POS สำหรับร้านอาหารไทย ไม่ใช่ template ทั่วไป

**SKILL (Phase 6 Summary):**

สรุป Phase Criteria (force-ranked):
1. **Code-ready output** — Claude produces working React/Next.js code that can be used immediately
2. **Conversion-optimized** — Clear CTA, minimal friction signup, persuasive copy
3. **Not generic** — Must feel specific to Thai restaurant POS, not a template

---

## Phase 7 — Synthesize

**SKILL:**

จากข้อมูลทั้งหมด ผมเขียน Improved Prompt ให้ครับ:

---

## Improved Prompt

สร้าง landing page สำหรับระบบ POS ร้านอาหาร (SaaS) โดยใช้ React + Next.js ให้โค้ดที่ใช้ได้เลย โดยมีรายละเอียดดังนี้:

**Product:**
- ระบบ POS สำหรับร้านอาหารขนาดเล็กในประเทศไทย (1-5 สาขา)
- กลุ่มเป้าหมายคือเจ้าของร้านที่ไม่ได้เก่งเทคโนโลยี ต้องดูง่าย เข้าใจได้ทันที

**Page Structure (single page, ไม่ยาวเกินไป):**
1. Hero section — headline ชัดเจนว่าคืออะไร + sub-headline บอก value proposition + ปุ่ม CTA "สมัครฟรี" (ไม่ต้องใส่บัตรเครดิต)
2. Features section — 3-4 features หลักๆ พร้อม simple illustrations/icons
3. Social proof section — testimonials หรือตัวเลข (เช่น "ร้านอาหารกว่า XX ร้านไว้วางใจ")
4. CTA section สุดท้าย — ย้ำ signup อีกครั้ง

**Design:**
- สไตล์ Notion-like: friendly, approachable, minimal, simple illustrations
- อ้างอิง Square for Restaurants ในเรื่อง messaging ที่ชัดเจนและ layout ที่ง่าย
- สีไม่ฉูดฉาด, white space เยอะ, typography อ่านง่าย
- Thai-friendly design — ภาษาไทยเป็นหลัก, font ที่รองรับภาษาไทยดี
- Mobile-first responsive

**Technical:**
- React + Next.js (App Router)
- Tailwind CSS สำหรับ styling
- ให้โค้ดเป็น component structure ที่ชัดเจน แยกเป็น Hero, Features, SocialProof, CTA
- ใส่ comment อธิบายส่วนที่ต้อง customize (เช่น เปลี่ยนชื่อ product, ใส่ logo)
- Signup form เก็บแค่ ชื่อ + เบอร์โทร + ชื่อร้าน (ไม่ต้องบัตรเครดิต)

**Copy/Content:**
- เขียนภาษาไทย ใช้ภาษาที่เจ้าของร้านอาหารเข้าใจ ไม่ใช้ศัพท์เทค
- Headline ต้องบอกได้ภายใน 1 ประโยคว่าระบบนี้ช่วยอะไร
- เน้น pain point ของเจ้าของร้านเล็ก: จัดการออเดอร์ยุ่งยาก, ดูยอดขายไม่ได้ real-time, ระบบเดิมแพงและซับซ้อน

**ห้าม:**
- ห้ามดูซับซ้อนหรือ technical
- ห้ามยาวเกินไป (ไม่เกิน 4-5 sections)
- ห้ามดูเหมือน template SaaS ทั่วไป — ต้องรู้สึกว่าทำมาเพื่อร้านอาหารไทยโดยเฉพาะ

---

### Discovery Summary

**Goal:** สร้าง landing page ระบบ POS ร้านอาหาร เพื่อให้ได้ signups อย่างน้อย 100 ราย ในเดือนแรก จากเจ้าของร้านอาหารขนาดเล็กในไทย

**Direction:** Single-page (hero + features + social proof + CTA), mobile-first, ไม่ซับซ้อน ไม่ต้องบัตรเครดิต ตัดทางเลือก long-form walkthrough และ teaser page ออก

**Reference:** Notion-style design (friendly, approachable), Square for Restaurants (messaging clarity), Thai-friendly adaptation

**Context:** Timeline 2 สัปดาห์, code เองด้วย React/Next.js, ตัดสินใจคนเดียว, ไม่มี designer

**Criteria:** 1) Code-ready output (working React/Next.js code) 2) Conversion-optimized (clear CTA, minimal friction) 3) Not generic (specific to Thai restaurant POS)

---

**SKILL:**

นี่คือ prompt ที่ปรับปรุงแล้วครับ ครอบคลุมทุกอย่างที่คุยกันมา — ตั้งแต่เป้าหมาย, design direction, technical stack, ไปจนถึง copy guidelines

คุณดูแล้วตรงกับที่ต้องการไหมครับ? มีอะไรอยากปรับไหม?

**USER:**

ดีมากครับ ตรงเลย แต่อยากเพิ่มเรื่อง pricing section ด้วยได้ไหม? แบบ free tier กับ paid tier ง่ายๆ

**SKILL:**

ได้ครับ ผมเพิ่ม pricing section เข้าไปใน prompt:

**(เพิ่มใน Page Structure ระหว่าง Social Proof กับ CTA สุดท้าย):**

> 4. Pricing section — แสดง 2 plans ง่ายๆ: Free (จำกัดฟีเจอร์) กับ Pro (เต็มระบบ) แบบ pricing cards เรียบๆ ราคาเป็นบาท ไม่ต้อง toggle monthly/yearly ให้ซับซ้อน

แล้วก็อัปเดต component structure เป็น: Hero, Features, SocialProof, Pricing, CTA

ตอนนี้ครบไหมครับ?

**USER:**

ครบแล้วครับ ขอบคุณมาก

---

## Next Step

**SKILL (ask_user with choices):**

ต้องการทำอะไรต่อครับ?

| Choice | Description |
|--------|-------------|
| A | Create a Plan — ให้ช่วยวางแผน implementation step-by-step |
| B | Done — จบแค่นี้ เอา prompt ไปใช้ได้เลย |

**USER:**

B ครับ เอา prompt ไปใช้เลย ขอบคุณครับ

**SKILL:**

ยินดีครับ! เอา prompt ไปใช้กับ Claude ได้เลย ขอให้ launch สำเร็จครับ

---

## Simulation Metadata

| Field | Value |
|-------|-------|
| Total questions asked | 13 |
| Phase 2 (Goal) questions | 3 |
| Phase 3 (Direction) questions | 3 (including approach proposal) |
| Phase 4 (Reference) questions | 2 + 1 web search |
| Phase 5 (Context) questions | 3 |
| Phase 6 (Criteria) questions | 3 |
| User feedback iterations in Phase 7 | 1 (added pricing section) |
| Total phases completed | 7/7 |
| Multiple choice questions | 12/13 (92%) |
| Open-ended questions | 1/13 (8%) |
| Skill rules followed | All 8 core rules observed |
| Next Step offered | Yes — user chose "Done" |
