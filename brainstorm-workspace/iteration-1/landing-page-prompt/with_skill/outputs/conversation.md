# Brainstorm Skill — Simulated Conversation

**User Prompt:** "ช่วยคิด prompt สำหรับสร้าง landing page ให้หน่อย จะใช้ Claude สร้าง"

---

## Phase 1 — Receive

**SKILL:**

เข้าใจแล้วครับ คุณต้องการสร้าง prompt ที่ดีสำหรับให้ Claude ช่วยสร้าง landing page ก่อนที่ผมจะช่วยเขียน prompt ผมขอถามคำถามสักหน่อยเพื่อให้ผลลัพธ์ตรงกับสิ่งที่คุณต้องการจริง ๆ ครับ เริ่มจากเป้าหมายก่อนนะครับ

---

## Phase 2 — Goal

### Question 2.1

**SKILL** `[ask_user]`:

Landing page นี้ต้องการให้คนที่เข้ามาดูทำอะไรมากที่สุด?

**Choices:**
- A) สมัครใช้งานหรือ sign up ทดลองใช้
- B) ติดต่อขอ demo / นัดโทรคุย
- C) ซื้อสินค้าหรือบริการเลย
- D) อื่น ๆ (โปรดระบุ)

**USER:** A ครับ อยากให้คนสมัครทดลองใช้ฟรีก่อน

---

### Question 2.2

**SKILL** `[ask_user]`:

แล้วอะไรคือตัวชี้วัดว่า landing page นี้ "สำเร็จ" สำหรับคุณ?

**Choices:**
- A) จำนวนคนสมัครต่อเดือน (มีตัวเลขในใจไหม?)
- B) อัตราการ convert จากคนเข้าชมเป็นคนสมัคร
- C) ยังไม่มีตัวเลขในใจ แค่ต้องการ landing page ที่ดูน่าเชื่อถือก่อน

**USER:** C ครับ ตอนนี้เพิ่งเริ่ม แค่อยากได้ landing page ที่ดูน่าเชื่อถือ professional แล้วมีปุ่มให้สมัครทดลองใช้ได้

---

### Question 2.3

**SKILL** `[ask_user]`:

สินค้าหรือบริการที่จะขายผ่าน landing page นี้คืออะไรครับ?

**USER:** เป็นระบบ POS สำหรับร้านอาหาร ครับ เป็น SaaS product กลุ่มเป้าหมายคือร้านอาหารเล็ก ๆ ในไทย

---

**SKILL (Phase 2 Summary):**

สรุป Phase 2: เป้าหมายคือ **สร้าง landing page สำหรับระบบ POS ร้านอาหาร (SaaS) ที่ดูน่าเชื่อถือ professional เพื่อให้ร้านอาหารเล็ก ๆ ในไทยสมัครทดลองใช้ฟรี** ถูกต้องไหมครับ?

**USER:** ถูกต้องครับ

---

## Phase 3 — Direction

### Question 3.1

**SKILL** `[ask_user]`:

มีอะไรที่ต้อง "ไม่ใช่แบบนี้เด็ดขาด" ไหมครับ? เช่น สิ่งที่ไม่อยากให้ landing page มี หรือให้ความรู้สึก

**Choices:**
- A) ไม่อยากดูเหมือนของถูก / ไม่น่าเชื่อถือ
- B) ไม่อยากยาวเกินไป คนไม่อ่าน
- C) ไม่อยากใช้ภาษาทางการเกินไป
- D) ไม่อยากมีข้อมูลเยอะจนสับสน
- E) มีอย่างอื่น (โปรดระบุ)

**USER:** A กับ B ครับ ไม่อยากดูเหมือนของถูก ต้องดูเป็นมืออาชีพ แล้วก็ไม่อยากยาวเกินไป กระชับ ได้ใจความ

---

### Question 3.2

**SKILL** `[ask_user]`:

ภาษาหลักบน landing page จะเป็นภาษาอะไร?

**Choices:**
- A) ภาษาไทยอย่างเดียว
- B) ภาษาอังกฤษอย่างเดียว
- C) สองภาษา (ไทย + อังกฤษ)

**USER:** A ครับ ภาษาไทยอย่างเดียว เพราะกลุ่มเป้าหมายเป็นร้านอาหารเล็ก ๆ ในไทย

---

### Question 3.3 — Propose Approaches

**SKILL** `[ask_user]`:

จากข้อมูลที่ได้มา ผมเห็นแนวทางที่เป็นไปได้ 3 แบบสำหรับ prompt ครับ:

- **A) Single Page — Modern SaaS Style (แนะนำ)**
  หน้าเดียวยาวแบบ scroll ลงมา มี hero section, features, pricing, CTA — เป็นมาตรฐาน SaaS landing page ที่ลูกค้าคุ้นเคย ทำเร็ว ดูน่าเชื่อถือ
  *ข้อดี:* ทำเร็ว ง่าย ถ้าเนื้อหาดีจะ convert ดี
  *ข้อเสีย:* ถ้าอยากเพิ่มเนื้อหาทีหลังต้อง refactor

- **B) Multi-section Landing + Subpages**
  มี landing page หลัก + หน้ารายละเอียด features, pricing แยก
  *ข้อดี:* ขยายเนื้อหาได้ง่ายในอนาคต
  *ข้อเสีย:* ใช้เวลาสร้างนานกว่า ซับซ้อนกว่า

- **C) Minimal One-Screen**
  แค่จอเดียว มี headline + value proposition + ปุ่ม CTA — เน้น "coming soon" feel
  *ข้อดี:* ทำเสร็จภายใน 1-2 ชม.
  *ข้อเสีย:* ขาดรายละเอียดที่ช่วยสร้างความเชื่อมั่น

ผมแนะนำ A ครับ เพราะคุณต้องการดูเป็นมืออาชีพ + กระชับ + มีจุดให้สมัคร — แนว modern SaaS landing page ตอบโจทย์ทุกข้อ จะเลือกแบบไหนครับ?

**USER:** A ครับ เห็นด้วย ไปแนว modern SaaS landing page เลย

---

**SKILL (Phase 3 Summary):**

สรุป Phase 3: ทิศทางคือ **Single page modern SaaS style landing page ภาษาไทย ดีไซน์เป็นมืออาชีพ กระชับ ไม่ยาวเกิน** มี sections มาตรฐาน SaaS ครับ ไปต่อเรื่อง reference เลยนะครับ

---

## Phase 4 — Reference

### Question 4.1

**SKILL** `[ask_user]`:

มี landing page ของ product อื่นที่คุณชอบ style หรือ layout ของเขาไหมครับ? หรือเคยเห็นเว็บไหนที่รู้สึกว่า "อยากได้แบบนี้"?

**Choices:**
- A) มี ขอยกตัวอย่าง
- B) ไม่มีเลย ช่วยหาให้หน่อย

**USER:** A ครับ ผมชอบ landing page ของ Square for Restaurants กับ Loyverse POS ครับ ดูสะอาด สีไม่ฉูดฉาด มี screenshot ของตัว product ชัดเจน

---

### Question 4.2

**SKILL** `[ask_user]`:

จากที่ชอบ Square กับ Loyverse — ถ้าต้องเลือกสิ่งที่ชอบมากที่สุดจากเว็บเหล่านั้น จะเป็นอะไรครับ?

**Choices:**
- A) โทนสีสะอาด มินิมอล
- B) มี screenshot / mockup ของ product ให้เห็นชัด
- C) Layout ที่อ่านง่าย ไม่รกตา
- D) ชอบหมดเลย

**USER:** D ครับ ชอบหมดเลย ทั้งโทนสีสะอาด มี product screenshot ชัด ๆ แล้วก็ layout ไม่รก อ่านง่าย

---

**SKILL (Phase 4 Summary):**

สรุป Phase 4: Reference คือ **Square for Restaurants และ Loyverse POS** — ชอบโทนสีมินิมอล สะอาด, มี product screenshot ให้เห็นชัด, layout อ่านง่ายไม่รก ครับ ไปต่อเรื่อง context ที่เกี่ยวกับตัวคุณเลยนะครับ

---

## Phase 5 — Context

### Question 5.1

**SKILL** `[ask_user]`:

คุณจะสร้าง landing page นี้ด้วยเทคโนโลยีอะไรครับ?

**Choices:**
- A) React / Next.js
- B) HTML/CSS ธรรมดา
- C) ใช้ website builder เช่น Webflow, Wix
- D) อื่น ๆ (โปรดระบุ)

**USER:** A ครับ ใช้ Next.js ครับ ผมเขียน React/Next.js ได้

---

### Question 5.2

**SKILL** `[ask_user]`:

มีเวลาสำหรับทำ landing page นี้ประมาณเท่าไหร่ครับ?

**Choices:**
- A) 1-3 วัน
- B) 1 สัปดาห์
- C) 2 สัปดาห์
- D) ไม่เร่ง ค่อย ๆ ทำ

**USER:** C ครับ 2 สัปดาห์ แต่ผมต้องทำอย่างอื่นด้วย landing page คงใช้เวลาได้ประมาณ 3-4 วันจริง ๆ

---

### Question 5.3

**SKILL** `[ask_user]`:

ทำคนเดียวหรือมีทีม? แล้วมี designer แยกไหม?

**Choices:**
- A) ทำคนเดียว ไม่มี designer
- B) ทำคนเดียว แต่มี design เตรียมไว้แล้ว
- C) มีทีม มี designer

**USER:** A ครับ ทำคนเดียว ไม่มี designer ก็เลยอยากให้ prompt ออกมาดี ๆ จะได้ให้ Claude สร้าง code ที่ดูดีเลย

---

**SKILL (Phase 5 Summary):**

สรุป Phase 5: **ใช้ Next.js, มีเวลาจริง ๆ ประมาณ 3-4 วัน, ทำคนเดียวไม่มี designer** ต้องพึ่ง prompt ที่ดีเพื่อให้ Claude สร้าง code ที่ดูดีได้เลย ครับ ไปต่อเรื่องเกณฑ์ตัดสินว่า prompt ดีหรือไม่ดีนะครับ

---

## Phase 6 — Criteria

### Question 6.1

**SKILL** `[ask_user]`:

ถ้า prompt ที่ได้ออกมาดี คุณจะรู้ได้ยังไงว่า "ใช่เลย"? เลือกสิ่งที่สำคัญที่สุด 2-3 อย่างครับ

**Choices:**
- A) Claude ให้ code ที่ run ได้เลย ไม่ต้องแก้เยอะ
- B) หน้าตาดูเป็นมืออาชีพ ไม่ต้องปรับ design เยอะ
- C) มีครบทุก section ที่ landing page ควรมี
- D) code สะอาด อ่านง่าย แก้ไขต่อได้
- E) responsive ทำงานได้ดีทั้ง desktop และมือถือ

**USER:** B กับ D กับ E ครับ อยากให้ดูเป็นมืออาชีพ code สะอาด แล้วก็ responsive

---

### Question 6.2

**SKILL** `[ask_user]`:

จาก 3 ข้อนั้น ถ้าต้องเลือกอันเดียวที่สำคัญสุด จะเป็นอันไหนครับ?

**Choices:**
- A) หน้าตาดูเป็นมืออาชีพ
- B) code สะอาด อ่านง่าย
- C) responsive ทำงานได้ดีทุกหน้าจอ

**USER:** A ครับ หน้าตาสำคัญสุด เพราะลูกค้าเห็นหน้าตาก่อน

---

**SKILL (Phase 6 Summary):**

สรุป Phase 6: เกณฑ์ตัดสิน prompt (เรียงตามความสำคัญ):
1. **หน้าตาดูเป็นมืออาชีพ** — สำคัญสุด ลูกค้าเห็นก่อน
2. **code สะอาด อ่านง่าย แก้ไขต่อได้**
3. **responsive ทำงานดีทั้ง desktop และมือถือ**

พร้อมสร้าง prompt แล้วครับ ไป Phase 7 เลยนะครับ

---

## Phase 7 — Synthesize

**SKILL:**

จากทุกอย่างที่คุยกันมา ผมสร้าง Improved Prompt ได้แล้วครับ:

---

## Improved Prompt

สร้าง landing page สำหรับระบบ POS ร้านอาหาร (SaaS) ด้วย Next.js โดยมีรายละเอียดดังนี้:

**Product:**
- ระบบ POS สำหรับร้านอาหาร แบบ SaaS (ใช้งานผ่าน browser)
- กลุ่มเป้าหมาย: ร้านอาหารเล็ก ๆ ในประเทศไทย
- เป้าหมายหลัก: ให้ผู้ใช้สมัครทดลองใช้ฟรี

**Design Direction:**
- สไตล์ modern SaaS landing page คล้ายแนว Square for Restaurants และ Loyverse POS
- โทนสีสะอาด มินิมอล ไม่ฉูดฉาด — ดูน่าเชื่อถือ เป็นมืออาชีพ
- มีพื้นที่สำหรับ product screenshot/mockup ให้เห็นหน้าตาระบบชัดเจน
- Layout เรียบง่าย อ่านง่าย ไม่รกตา
- Responsive — ทำงานได้ดีทั้ง desktop และมือถือ

**Page Structure (single page, scroll down):**
1. **Hero Section** — headline ที่บอกว่าระบบ POS นี้ช่วยอะไรร้านอาหาร, sub-headline สั้น ๆ, ปุ่ม CTA "ทดลองใช้ฟรี", และ product screenshot/mockup
2. **Features Section** — 3-4 จุดเด่นหลักของระบบ (เช่น จัดการออเดอร์ง่าย, ดูยอดขาย real-time, ใช้ได้ทุกอุปกรณ์, ตั้งค่าเร็ว) พร้อม icon
3. **Social Proof Section** — พื้นที่สำหรับ testimonial หรือ logo ร้านค้าที่ใช้ (ใส่ placeholder ไว้ก่อนได้)
4. **Pricing Section** — แสดงแพ็กเกจแบบเรียบง่าย (ใส่ข้อมูลตัวอย่างได้)
5. **CTA Section** — ย้ำ call-to-action ก่อนจบหน้า ปุ่ม "เริ่มใช้ฟรีวันนี้"
6. **Footer** — ข้อมูลติดต่อ, links

**Technical Requirements:**
- ใช้ Next.js (App Router)
- เขียน code ให้สะอาด อ่านง่าย มี component structure ที่ดี สามารถแก้ไขต่อได้
- ใช้ Tailwind CSS สำหรับ styling
- ใช้ภาษาไทยทั้งหมดสำหรับเนื้อหาบนหน้าเว็บ
- ใส่ placeholder content ที่สมจริง (ชื่อ product, features, pricing ตัวอย่าง) เพื่อให้เห็นภาพจริง
- ไม่ต้องทำ backend หรือ form submission จริง — แค่ UI

**Constraints:**
- หน้าเดียว scroll ลงมา ไม่ต้องมีหลายหน้า
- กระชับ ไม่ยาวเกินไป — เน้นคุณภาพเนื้อหามากกว่าปริมาณ
- ไม่ใช้สีฉูดฉาด ไม่ใช้ animation มากเกินไป

---

### Discovery Summary

**Goal:** สร้าง landing page สำหรับระบบ POS ร้านอาหาร (SaaS) ที่ดูน่าเชื่อถือ เป็นมืออาชีพ เพื่อให้ร้านอาหารเล็ก ๆ ในไทยสมัครทดลองใช้ฟรี

**Direction:** Single page modern SaaS style, ภาษาไทย, ดูเป็นมืออาชีพ กระชับไม่ยาวเกิน ไม่ดูเหมือนของถูก

**Reference:** Square for Restaurants และ Loyverse POS — ชอบโทนสีมินิมอล สะอาด, product screenshot ชัด, layout อ่านง่าย

**Context:** ใช้ Next.js, ทำคนเดียวไม่มี designer, มีเวลาจริง 3-4 วัน, ต้องการ code ที่ Claude สร้างแล้วใช้ได้เลย

**Criteria:** 1) หน้าตาดูเป็นมืออาชีพ (สำคัญสุด) 2) code สะอาดแก้ไขต่อได้ 3) responsive ทำงานดีทุกหน้าจอ

---

**SKILL** `[ask_user]`:

นี่คือ prompt ที่ปรับปรุงแล้วครับ ครอบคลุมสิ่งที่คุณต้องการไหม? มีอะไรอยากปรับไหมครับ?

**USER:** ดีมากครับ ครบแล้ว แต่ขอเพิ่มอีกอย่าง — อยากให้มี dark mode support ด้วยได้ไหม?

---

### Iteration

**SKILL:**

เพิ่มให้แล้วครับ ใน Technical Requirements เพิ่ม:
- **รองรับ dark mode** — ใช้ Tailwind CSS dark mode class strategy, ให้มี toggle สลับ light/dark ได้

**SKILL** `[ask_user]`:

เพิ่ม dark mode support เรียบร้อยครับ โอเคไหมครับ?

**USER:** โอเคครับ สมบูรณ์แล้ว

---

## Final Improved Prompt (After Iteration)

สร้าง landing page สำหรับระบบ POS ร้านอาหาร (SaaS) ด้วย Next.js โดยมีรายละเอียดดังนี้:

**Product:**
- ระบบ POS สำหรับร้านอาหาร แบบ SaaS (ใช้งานผ่าน browser)
- กลุ่มเป้าหมาย: ร้านอาหารเล็ก ๆ ในประเทศไทย
- เป้าหมายหลัก: ให้ผู้ใช้สมัครทดลองใช้ฟรี

**Design Direction:**
- สไตล์ modern SaaS landing page คล้ายแนว Square for Restaurants และ Loyverse POS
- โทนสีสะอาด มินิมอล ไม่ฉูดฉาด — ดูน่าเชื่อถือ เป็นมืออาชีพ
- มีพื้นที่สำหรับ product screenshot/mockup ให้เห็นหน้าตาระบบชัดเจน
- Layout เรียบง่าย อ่านง่าย ไม่รกตา
- Responsive — ทำงานได้ดีทั้ง desktop และมือถือ
- รองรับ dark mode — มี toggle สลับ light/dark ได้

**Page Structure (single page, scroll down):**
1. **Hero Section** — headline ที่บอกว่าระบบ POS นี้ช่วยอะไรร้านอาหาร, sub-headline สั้น ๆ, ปุ่ม CTA "ทดลองใช้ฟรี", และ product screenshot/mockup
2. **Features Section** — 3-4 จุดเด่นหลักของระบบ (เช่น จัดการออเดอร์ง่าย, ดูยอดขาย real-time, ใช้ได้ทุกอุปกรณ์, ตั้งค่าเร็ว) พร้อม icon
3. **Social Proof Section** — พื้นที่สำหรับ testimonial หรือ logo ร้านค้าที่ใช้ (ใส่ placeholder ไว้ก่อนได้)
4. **Pricing Section** — แสดงแพ็กเกจแบบเรียบง่าย (ใส่ข้อมูลตัวอย่างได้)
5. **CTA Section** — ย้ำ call-to-action ก่อนจบหน้า ปุ่ม "เริ่มใช้ฟรีวันนี้"
6. **Footer** — ข้อมูลติดต่อ, links

**Technical Requirements:**
- ใช้ Next.js (App Router)
- เขียน code ให้สะอาด อ่านง่าย มี component structure ที่ดี สามารถแก้ไขต่อได้
- ใช้ Tailwind CSS สำหรับ styling
- รองรับ dark mode — ใช้ Tailwind CSS dark mode class strategy, มี toggle สลับ light/dark
- ใช้ภาษาไทยทั้งหมดสำหรับเนื้อหาบนหน้าเว็บ
- ใส่ placeholder content ที่สมจริง (ชื่อ product, features, pricing ตัวอย่าง) เพื่อให้เห็นภาพจริง
- ไม่ต้องทำ backend หรือ form submission จริง — แค่ UI

**Constraints:**
- หน้าเดียว scroll ลงมา ไม่ต้องมีหลายหน้า
- กระชับ ไม่ยาวเกินไป — เน้นคุณภาพเนื้อหามากกว่าปริมาณ
- ไม่ใช้สีฉูดฉาด ไม่ใช้ animation มากเกินไป

---

### Discovery Summary

**Goal:** สร้าง landing page สำหรับระบบ POS ร้านอาหาร (SaaS) ที่ดูน่าเชื่อถือ เป็นมืออาชีพ เพื่อให้ร้านอาหารเล็ก ๆ ในไทยสมัครทดลองใช้ฟรี

**Direction:** Single page modern SaaS style, ภาษาไทย, ดูเป็นมืออาชีพ กระชับไม่ยาวเกิน, รองรับ dark mode

**Reference:** Square for Restaurants และ Loyverse POS — ชอบโทนสีมินิมอล สะอาด, product screenshot ชัด, layout อ่านง่าย

**Context:** ใช้ Next.js + Tailwind CSS, ทำคนเดียวไม่มี designer, มีเวลาจริง 3-4 วัน, ต้องการ code ที่ Claude สร้างแล้วใช้ได้เลย

**Criteria:** 1) หน้าตาดูเป็นมืออาชีพ (สำคัญสุด) 2) code สะอาดแก้ไขต่อได้ 3) responsive ทำงานดีทุกหน้าจอ

---

## Next Step

**SKILL** `[ask_user]`:

ต้องการทำอะไรต่อครับ?

**Choices:**
- A) Create a Plan — ให้ช่วยวางแผนขั้นตอนการทำ
- B) Done — จบแค่นี้ เอา prompt ไปใช้เลย

**USER:** B ครับ เอา prompt ไปใช้เลย ขอบคุณครับ

---

**SKILL:**

เรียบร้อยครับ เอา prompt ไปใช้กับ Claude ได้เลย ขอให้ได้ landing page ที่ถูกใจนะครับ!
