# Old Skill Simulation — Side Project Idea

**User Prompt:** "อยากทำ side project แต่ยังไม่รู้จะทำอะไรดี ช่วยคิดหน่อย"

**Simulated User Persona:** Thai software developer, interested in tech, free time on weekends, knows Go and TypeScript, budget-conscious.

---

## Phase 1 — Receive

**SKILL:**

เข้าใจครับ คุณอยากทำ side project แต่ยังไม่แน่ใจว่าจะทำอะไรดี ก่อนที่ผมจะช่วยเสนอไอเดีย ผมขอถามคำถามสักหน่อยเพื่อให้ผลลัพธ์ตรงกับสถานการณ์ของคุณจริง ๆ ครับ เริ่มจากเป้าหมายกันก่อนเลย

---

## Phase 2 — Goal

### Question 2.1

**SKILL** `[ask_user with choices]`:

> สำหรับ side project นี้ อะไรคือสิ่งที่สำคัญที่สุดที่คุณอยากได้จากมัน?
>
> A) สร้างรายได้เสริม
> B) เรียนรู้เทคโนโลยีใหม่ ๆ
> C) สร้าง portfolio ไว้สมัครงาน
> D) แก้ปัญหาบางอย่างที่ตัวเองเจอในชีวิตจริง

**USER:**

> B ครับ อยากเรียนรู้เทคโนโลยีใหม่ ๆ แต่ถ้าได้รายได้เสริมด้วยก็ดี

### Question 2.2

**SKILL** `[ask_user with choices]`:

> ดีครับ เรียนรู้เทคโนโลยีใหม่เป็นหลัก รายได้เสริมเป็นโบนัส — แล้วคุณจะรู้ได้ยังไงว่า side project นี้ "สำเร็จ" แล้ว?
>
> A) deploy ขึ้น production ได้ มีคนใช้จริงอย่างน้อย 10 คน
> B) เรียนรู้จนเขียน blog หรือพูดแชร์ให้คนอื่นได้
> C) ทำเสร็จจน push ขึ้น GitHub เป็น public repo ได้
> D) อื่น ๆ (ระบุเอง)

**USER:**

> A ครับ อยาก deploy ขึ้น production จริง ๆ ให้มีคนใช้ได้

### Phase 2 Summary

**SKILL:**

สรุป Goal: **ทำ side project เพื่อเรียนรู้เทคโนโลยีใหม่ โดย deploy ขึ้น production จริง มีคนใช้อย่างน้อย 10 คน** ถ้าสร้างรายได้เสริมได้ด้วยจะดีมาก

ถูกต้องไหมครับ?

**USER:**

> ถูกต้องครับ

---

## Phase 3 — Direction

### Question 3.1

**SKILL** `[ask_user with choices]`:

> ดีครับ ต่อไปผมจะถามเกี่ยวกับข้อจำกัดและสิ่งที่ไม่อยากเจอ เพื่อตัดทางที่ไม่เหมาะออกไป
>
> มีอะไรที่ "ไม่อยากทำเด็ดขาด" ไหมครับ?
>
> A) ไม่อยากทำอะไรที่ต้องลงทุนเงินเยอะ (เช่น ซื้อ hardware, จ่าย API แพง ๆ)
> B) ไม่อยากทำอะไรที่ต้องหาลูกค้า/ทำ marketing
> C) ไม่อยากทำอะไรที่ต้องดูแลรักษา (maintain) ตลอดเวลา
> D) ไม่มีข้อจำกัดอะไรเป็นพิเศษ

**USER:**

> A ครับ ไม่อยากลงทุนเงินเยอะ ค่า server ถ้าได้ free tier หรือถูก ๆ จะดีมาก

### Question 3.2

**SKILL** `[ask_user with choices]`:

> เข้าใจครับ ต้องงบต่ำ — แล้วระดับความเสี่ยงที่รับได้ล่ะครับ?
>
> A) เล่นปลอดภัย — ใช้เทคโนโลยีที่มี community ใหญ่ มี tutorial เยอะ
> B) กลาง ๆ — ลองของใหม่ได้ แต่ไม่อยากเจอ bug ที่ไม่มีใครเคยเจอ
> C) ชอบเสี่ยง — อยากลองของ cutting-edge ถึงจะ documentation น้อยก็โอเค

**USER:**

> B ครับ กลาง ๆ ลองของใหม่ได้ แต่ไม่อยากติดปัญหาแล้วหา solution ไม่เจอ

### Question 3.3

**SKILL** `[ask_user with choices]`:

> เคยลองทำ side project มาก่อนไหมครับ? ถ้าเคย เกิดอะไรขึ้น?
>
> A) เคย แต่ทำไม่เสร็จเพราะ scope ใหญ่เกินไป
> B) เคย แต่ทำไม่เสร็จเพราะหมดแรงจูงใจ
> C) เคย และทำเสร็จ
> D) ไม่เคยทำเลย

**USER:**

> A ครับ เคยลองแต่ scope ใหญ่เกินไป ทำ ๆ ไปก็เลิกกลางทาง

### Proposing Approaches

**SKILL:**

จากข้อมูลที่ได้ — ต้องการเรียนรู้เทคโนโลยีใหม่ งบต่ำ ความเสี่ยงปานกลาง และเคยเจอปัญหา scope ใหญ่เกินไป — ผมเห็นทางเลือกหลัก ๆ 3 แบบครับ:

> **A) CLI tool หรือ API service ขนาดเล็ก** — ทำ tool ที่แก้ปัญหาเฉพาะทางสักอย่าง เช่น notification service, URL shortener, file converter ข้อดี: scope เล็ก ทำเสร็จเร็ว deploy ง่ายบน free tier ข้อเสีย: อาจหาคนใช้ยากถ้าปัญหาไม่แรงพอ
>
> **B) Web app ที่แก้ปัญหาตัวเอง** — ทำ app ที่คุณเองใช้ได้ เช่น expense tracker, habit tracker, bookmark manager ข้อดี: มี user คนแรกคือตัวเอง มีแรงจูงใจเพราะใช้เอง ข้อเสีย: ถ้าทำ UI เยอะ scope อาจบานได้
>
> **C) Open-source contribution / micro-SaaS** — เริ่มจาก contribute ให้ project ที่สนใจ แล้วแตก feature ออกมาเป็น service เล็ก ๆ ข้อดี: ได้ community support, ได้เรียนรู้จาก codebase คนอื่น ข้อเสีย: ต้องใช้เวลาเรียนรู้ codebase เดิมก่อน
>
> **ผมแนะนำ A ครับ** เพราะ scope เล็ก ลด risk ที่จะทำไม่เสร็จ deploy ได้ฟรีบน Railway/Fly.io/Cloudflare Workers และเรียนรู้เทคโนโลยีใหม่ได้ชัดเจน

**USER:**

> A ดีครับ ชอบไอเดีย CLI tool / API service เล็ก ๆ สนใจทั้ง API service ที่คนอื่นเรียกใช้ได้

### Phase 3 Summary

**SKILL:**

สรุป Direction: **ทำ API service ขนาดเล็กที่แก้ปัญหาเฉพาะทาง** งบต่ำ (free tier), ความเสี่ยงปานกลาง (ลองของใหม่ได้แต่ต้องมี community), scope ต้องเล็กเพื่อไม่ให้ซ้ำรอยเดิม

---

## Phase 4 — Reference

### Question 4.1

**SKILL** `[ask_user with choices]`:

> มี API service หรือ tool ที่เคยเห็นแล้วรู้สึกว่า "อันนี้เจ๋งดี อยากทำแบบนี้" ไหมครับ?
>
> A) มี (ระบุได้เลย)
> B) ไม่มี ช่วยหาให้หน่อย

**USER:**

> B ครับ ไม่มีเลย ช่วยหาให้หน่อย

### Web Search (simulated)

**SKILL** `[web_search]`:

*ค้นหา: "small API side project ideas for developers 2025-2026", "micro-SaaS API projects Go TypeScript"*

ผมหา reference มาให้ 3 อันครับ:

> 1. **Dub.co** — Open-source link management API (ทำ URL shortener + analytics) ใช้ TypeScript, deploy บน Vercel — เป็นตัวอย่างที่ดีของ API service เล็ก ๆ ที่โตได้
> 2. **Novu** — Open-source notification infrastructure API — แสดงให้เห็นว่า notification service เป็น use case ที่มีคนต้องการ
> 3. **Unkey** — Open-source API key management service ใช้ Go + TypeScript, deploy ง่าย — เป็นตัวอย่าง developer tool ที่ scope เล็ก

มีอันไหนที่รู้สึกว่าใกล้เคียงกับที่อยากทำไหมครับ?

### Question 4.2

**SKILL** `[ask_user with choices]`:

> จาก 3 ตัวอย่างนี้ อันไหนรู้สึก "ใช่" มากที่สุด?
>
> A) Dub.co — ชอบเรื่อง link management / URL shortener
> B) Novu — ชอบเรื่อง notification service
> C) Unkey — ชอบเรื่อง API key management / developer tool
> D) ไม่ชอบเลย แต่ได้ไอเดียอื่น

**USER:**

> C ครับ ชอบ Unkey ที่เป็น developer tool ชอบ idea ที่ทำ tool ให้ developer ใช้

### Phase 4 Summary

**SKILL:**

สรุป Reference: **Unkey (open-source API key management)** เป็น direction ที่ชอบ — developer tool / API service ที่ developer คนอื่นเอาไปใช้ได้ scope ชัดเจน

---

## Phase 5 — Context

### Question 5.1

**SKILL** `[ask_user with choices]`:

> ดีครับ มาดูสถานการณ์จริงของคุณบ้าง — ในหนึ่งสัปดาห์ คุณมีเวลาจริง ๆ สำหรับ side project ประมาณกี่ชั่วโมง?
>
> A) 2-4 ชั่วโมง/สัปดาห์ (วันเสาร์หรืออาทิตย์วันใดวันหนึ่ง)
> B) 5-8 ชั่วโมง/สัปดาห์ (เสาร์อาทิตย์วันละครึ่งวัน)
> C) 8-15 ชั่วโมง/สัปดาห์ (เสาร์อาทิตย์เต็มวัน)
> D) มากกว่า 15 ชั่วโมง/สัปดาห์

**USER:**

> B ครับ ประมาณ 5-8 ชั่วโมง เสาร์อาทิตย์วันละ 3-4 ชั่วโมง

### Question 5.2

**SKILL** `[ask_user with choices]`:

> เทคโนโลยีที่ถนัดตอนนี้คืออะไรบ้างครับ? และอยากลองอะไรใหม่?
>
> A) ถนัด Go — อยากลอง TypeScript/frontend ใหม่ ๆ
> B) ถนัด TypeScript — อยากลอง Go หรือ Rust
> C) ถนัดทั้ง Go และ TypeScript — อยากลอง infrastructure/DevOps ใหม่ ๆ (เช่น Kubernetes, Terraform)
> D) ถนัดทั้ง Go และ TypeScript — อยากลอง AI/ML integration

**USER:**

> D ครับ ถนัดทั้ง Go และ TypeScript แล้วอยากลองเอา AI/ML มา integrate ด้วย

### Question 5.3

**SKILL** `[ask_user with choices]`:

> งบสำหรับ infrastructure ต่อเดือนยอมจ่ายได้เท่าไหร่ครับ?
>
> A) 0 บาท — free tier เท่านั้น
> B) ไม่เกิน 200 บาท/เดือน (~$5-6)
> C) ไม่เกิน 700 บาท/เดือน (~$20)
> D) ไม่เกิน 1,500 บาท/เดือน (~$40-50)

**USER:**

> B ครับ ไม่เกิน 200 บาท ถ้าได้ free ยิ่งดี

### Phase 5 Summary

**SKILL:**

สรุป Context:
- **เวลา:** 5-8 ชั่วโมง/สัปดาห์ (สุดสัปดาห์)
- **ทักษะ:** ถนัด Go + TypeScript, อยากเรียน AI/ML integration
- **งบ:** ไม่เกิน ~200 บาท/เดือน (ถ้า free ยิ่งดี)
- **ทำคนเดียว**

เรื่อง AI/ML integration น่าสนใจครับ — แต่ค่า API ของ LLM (เช่น OpenAI, Anthropic) อาจเป็นต้นทุนหลัก ต้องเลือก use case ที่ token usage ไม่เยอะมากนะครับ เพื่อให้อยู่ในงบ

---

## Phase 6 — Criteria

### Question 6.1

**SKILL** `[ask_user with choices]`:

> เกือบครบแล้วครับ — ถ้าทำ side project เสร็จแล้ว อะไรที่จะทำให้คุณรู้สึกว่า "นี่แหละ ตรงกับที่ต้องการเลย"?
>
> A) เรียนรู้ได้เยอะ — ได้ลอง tech ใหม่จริง ๆ
> B) มีคนใช้จริง — ไม่ใช่แค่ทำเสร็จแล้ววางไว้
> C) code สวย — architecture ดี เอาไปโชว์ใน portfolio ได้
> D) ทำเสร็จเร็ว — ไม่ลากยาวข้ามเดือน

**USER:**

> A กับ B ครับ อยากเรียนรู้ได้เยอะ และมีคนใช้จริงด้วย

### Question 6.2

**SKILL** `[ask_user with choices]`:

> ถ้าต้องเลือกอันเดียว ระหว่าง "เรียนรู้ได้เยอะ" กับ "มีคนใช้จริง" อันไหนสำคัญกว่าครับ?
>
> A) เรียนรู้ได้เยอะ — ถ้าไม่มีคนใช้ก็ไม่เป็นไร ขอให้ได้ลอง tech ใหม่
> B) มีคนใช้จริง — ถ้าไม่ได้เรียน tech ใหม่มากก็โอเค ขอให้มี impact

**USER:**

> A ครับ เรียนรู้สำคัญกว่า

### Question 6.3

**SKILL** `[ask_user with choices]`:

> สุดท้ายครับ — อะไรที่จะทำให้คุณ "ไม่พอใจ" กับ project นี้?
>
> A) ทำเสร็จแต่ไม่ได้เรียนรู้อะไรใหม่เลย
> B) ทำไม่เสร็จ — ลากยาวเกิน 2-3 เดือนแล้วเลิก
> C) ทำเสร็จแต่ code ยุ่งเหยิงจน deploy ไม่ได้
> D) ทำเสร็จแต่ไม่มีใครสนใจเลย

**USER:**

> B ครับ กลัวทำไม่เสร็จมากที่สุด ไม่อยากซ้ำรอยเดิม

### Phase 6 Summary

**SKILL:**

สรุป Criteria (เรียงตามลำดับความสำคัญ):
1. **เรียนรู้เทคโนโลยีใหม่ได้จริง** — ต้องได้ลอง AI/ML integration ในบริบทจริง
2. **ทำเสร็จได้ภายใน 2-3 เดือน** — scope ต้องเล็กพอที่ 5-8 ชม./สัปดาห์จะ deliver ได้
3. **มีคนใช้จริง** — deploy ขึ้น production มีคนใช้อย่างน้อย 10 คน

---

## Phase 7 — Synthesize

**SKILL:**

จากทุก phase ที่คุยกันมา ผมสรุปเป็น Improved Prompt ให้ครับ:

---

## Improved Prompt

ช่วยเสนอไอเดีย side project สำหรับ developer ที่มีเงื่อนไขดังนี้:

**เป้าหมายหลัก:** เรียนรู้การ integrate AI/ML เข้ากับ production service จริง โดย deploy ให้มีคนใช้อย่างน้อย 10 คน ถ้าสร้างรายได้เสริมได้ด้วยจะเป็นโบนัส

**ประเภทโปรเจค:** API service / developer tool ขนาดเล็ก ที่ developer คนอื่นเอาไปใช้ได้ (แนว Unkey — API key management เป็นตัวอย่าง direction ที่ชอบ)

**ข้อจำกัด:**
- งบไม่เกิน 200 บาท/เดือน (free tier preferred) — ค่า LLM API ต้องคุมให้ต่ำ
- เวลา 5-8 ชั่วโมง/สัปดาห์ (สุดสัปดาห์เท่านั้น)
- ทำคนเดียว
- Scope ต้องเล็กพอที่จะเสร็จใน 2-3 เดือน (เคยเจอปัญหา scope ใหญ่เกินแล้วเลิกกลางทาง)

**Tech stack:** Go และ TypeScript (ถนัดแล้ว), ต้องการลอง AI/ML integration เป็นหลัก เทคโนโลยีที่เลือกต้องมี community พอสมควร ไม่ใช่ cutting-edge จนหา solution ไม่ได้

**เกณฑ์ตัดสินไอเดีย (เรียงตามลำดับ):**
1. ได้เรียนรู้ AI/ML integration ในบริบทจริง
2. ทำเสร็จได้ใน 2-3 เดือนด้วยเวลาที่มี
3. มีคนใช้จริงได้อย่างน้อย 10 คน

เสนอมา 3 ไอเดีย พร้อมอธิบายว่าแต่ละอันตอบเกณฑ์ข้างบนยังไง และแนะนำ tech stack ที่เหมาะสม

---

### Discovery Summary

**Goal:** เรียนรู้เทคโนโลยี AI/ML integration ผ่าน side project ที่ deploy ขึ้น production จริง มีคนใช้อย่างน้อย 10 คน
**Direction:** API service / developer tool ขนาดเล็ก แบบ Unkey-style, ความเสี่ยงปานกลาง, scope จำกัด
**Reference:** Unkey (open-source API key management) เป็น style ที่ชอบ — developer tool ที่มี API ให้คนอื่นเรียกใช้
**Context:** 5-8 ชม./สัปดาห์, ถนัด Go + TypeScript, งบ ~200 บาท/เดือน, ทำคนเดียว, เคย fail จาก scope ใหญ่
**Criteria:** 1) เรียนรู้ AI/ML จริง 2) เสร็จใน 2-3 เดือน 3) มีคนใช้จริง 10+ คน

---

**SKILL** `[ask_user]`:

> นี่คือ Improved Prompt ที่สรุปจากทุกอย่างที่คุยกันมาครับ ครอบคลุมสิ่งที่คุณต้องการไหม? มีอะไรอยากปรับไหม?

**USER:**

> ดีครับ ครบแล้ว ไม่ต้องปรับอะไร

---

## Next Step

**SKILL** `[ask_user with choices]`:

> ต้องการทำอะไรต่อครับ?
>
> A) Create a Plan — ให้ผมช่วยสร้าง implementation plan
> B) Done — จบแค่นี้

**USER:**

> B ครับ Done

**SKILL:**

เรียบร้อยครับ! เอา Improved Prompt ด้านบนไปใช้ถาม AI ตัวไหนก็ได้ จะได้ผลลัพธ์ที่ตรงกับสถานการณ์ของคุณมากกว่าถามแบบกว้าง ๆ ครับ ขอให้สนุกกับ side project!

---

## Simulation Metadata

| Field | Value |
|---|---|
| Skill version | 1.2 (old) |
| Total phases executed | 7/7 |
| Total questions asked | 13 (Goal: 2, Direction: 3 + approach proposal, Reference: 2, Context: 3, Criteria: 3) |
| Tools used (simulated) | ask_user (13x), web_search (1x) |
| Estimated real-time | ~10-15 minutes of user interaction |
| Phase skipped | None |
| Contradictions flagged | 1 (AI/ML cost vs budget constraint — flagged in Context summary) |
| "I don't know" responses | 0 |
| User iterations on final prompt | 0 (accepted first draft) |
