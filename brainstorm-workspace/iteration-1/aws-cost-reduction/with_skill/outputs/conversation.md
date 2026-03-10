# Brainstorm Skill — Simulated Conversation
## Topic: AWS Cost Reduction

**User Profile:** Thai DevOps/backend engineer, team of 5, startup, 3-4 EC2 (t3.large), 1 RDS PostgreSQL, S3 buckets, services run 24/7, traffic mainly business hours, monthly cost ~50,000 THB

---

## Phase 1 — Receive

**SKILL:**

เข้าใจครับ คุณต้องการหาวิธีลดค่าใช้จ่าย AWS ของทีม ที่ตอนนี้อยู่ที่เดือนละประมาณ 5 หมื่นบาท โดยใช้ EC2 กับ RDS เป็นหลัก

ก่อนที่ผมจะเสนอวิธีลดค่าใช้จ่ายเลย ขอถามคำถามสักหน่อยเพื่อให้แนวทางที่ได้ตรงกับสถานการณ์จริงของทีมคุณมากที่สุดนะครับ เริ่มจากเป้าหมายกันก่อน

---

## Phase 2 — Goal

### Question 2.1

**SKILL** *(ask_user with choices):*

อยากลดค่าใช้จ่ายลงประมาณเท่าไหร่ครับ?

- A) ลดได้ 10-20% ก็พอ (ประหยัดเดือนละ 5,000-10,000 บาท)
- B) ลดให้ได้ 30-50% (ประหยัดเดือนละ 15,000-25,000 บาท)
- C) ลดให้มากที่สุดเท่าที่จะทำได้ ไม่มีเป้าขั้นต่ำ

**USER:**

B ครับ อยากลดให้ได้สัก 30-40% ถ้าทำได้ก็ดีมาก เดือนละ 5 หมื่นมันเยอะเกินไปสำหรับ startup ขนาดเรา

### Question 2.2

**SKILL** *(ask_user with choices):*

ช่วงเวลาที่ต้องการเห็นผลคือเมื่อไหร่ครับ?

- A) ภายใน 1-2 สัปดาห์ (ต้องเร็ว)
- B) ภายใน 1 เดือน (ค่อย ๆ ทำ)
- C) ภายใน 3 เดือน (วางแผนระยะยาวได้)

**USER:**

B ครับ ภายในเดือนนี้ได้ก็ดี แต่ไม่ต้องรีบจนเสี่ยงว่าระบบจะพัง

### Goal Summary

**SKILL:**

สรุปเป้าหมาย: ลดค่าใช้จ่าย AWS ลง 30-40% (จาก ~50,000 บาท เหลือ ~30,000-35,000 บาท/เดือน) ภายใน 1 เดือน โดยไม่กระทบความเสถียรของระบบ ถูกต้องมั้ยครับ?

**USER:**

ถูกต้องครับ

---

## Phase 3 — Direction

### Question 3.1

**SKILL** *(ask_user with choices):*

มีอะไรที่ห้ามเกิดขึ้นเด็ดขาดมั้ยครับ? เลือกได้มากกว่า 1 ข้อ

- A) ห้าม downtime ระหว่างเปลี่ยนแปลง — ระบบต้อง online ตลอด
- B) ห้ามเปลี่ยน architecture ใหญ่ ๆ เช่น ย้ายจาก EC2 ไป container/serverless
- C) ห้ามเปลี่ยน database engine — ต้องอยู่กับ PostgreSQL
- D) ไม่มีข้อห้ามพิเศษ ขอแค่ไม่กระทบ user

**USER:**

A กับ C ครับ ระบบต้อง online ตลอด แล้วก็ไม่อยากเปลี่ยน database engine เพราะ code ผูกกับ PostgreSQL เยอะมาก ส่วน architecture ถ้ามันคุ้มจริง ก็เปลี่ยนได้นะ แต่ต้องทำ incremental

### Question 3.2

**SKILL** *(ask_user with choices):*

เคยลองลดค่าใช้จ่าย AWS มาก่อนมั้ยครับ?

- A) ยังไม่เคยทำอะไรเลย ใช้ on-demand ปกติมาตลอด
- B) เคยลอง resize instance บ้าง
- C) เคยซื้อ Reserved Instances หรือ Savings Plans แล้ว
- D) เคยลองหลายอย่างแล้ว แต่ยังรู้สึกว่าแพง

**USER:**

A ครับ ยังไม่เคยทำอะไรเลย ตอนเริ่มก็กดสร้าง instance ตาม tutorial แล้วก็ใช้มาเรื่อย ๆ ไม่เคย optimize

### Question 3.3 — Proposed Approaches

**SKILL:**

จากข้อมูลที่ได้ ผมเห็นแนวทาง 3 ทางครับ:

- **A) Right-sizing + Savings Plans (แนะนำ)** — วิเคราะห์ว่า instance ที่ใช้ใหญ่เกินจริงมั้ย แล้วซื้อ Savings Plans เพื่อลดค่า compute ทันที ได้ผลเร็ว ลดได้ 30-40% ไม่ต้องเปลี่ยน architecture ความเสี่ยงต่ำ
- **B) Scheduling + Spot Instances** — เปิด-ปิด instance ตาม business hours สำหรับ non-production + ใช้ Spot สำหรับ workload ที่ทนได้ ลดได้เยอะ แต่ต้อง setup scheduler และรับมือ Spot interruption
- **C) Re-architecture ไป Containerized/Serverless** — ย้ายไป ECS/Fargate หรือ Lambda ลดได้มากสุดระยะยาว แต่ใช้เวลา 2-3 เดือน ใช้แรงเยอะ

ผมแนะนำ A เพราะได้ผลเร็ว ตรงกับ timeline 1 เดือน และไม่ต้อง downtime แต่สามารถทำ B ควบคู่ได้สำหรับ non-prod environment ครับ คิดยังไงครับ?

**USER:**

ชอบ A ครับ แล้วก็อยากทำ B ด้วยสำหรับ dev/staging ที่ไม่จำเป็นต้องเปิดตลอด ส่วน C ไว้ค่อยทำทีหลัง

### Direction Summary

**SKILL:**

สรุป Direction:
- แนวทางหลัก: Right-sizing + Savings Plans
- เสริมด้วย: Scheduling สำหรับ non-production environment
- ข้อห้าม: ห้าม downtime, ห้ามเปลี่ยน database engine
- Re-architecture ไว้เป็น phase ถัดไป
- ยังไม่เคย optimize มาก่อน (มี low-hanging fruit เยอะ)

ไปต่อ Phase ถัดไปนะครับ

---

## Phase 4 — Reference

### Question 4.1

**SKILL** *(ask_user with choices):*

มีบทความหรือ reference เกี่ยวกับการลดค่า AWS ที่เคยอ่านมาบ้างมั้ยครับ?

- A) ไม่มีเลย ไม่เคยอ่านเรื่องนี้จริงจัง
- B) มีบ้าง เคยเห็นตาม blog/YouTube
- C) มี reference ชัดเจน อยากทำตาม

**USER:**

A ครับ ไม่เคยอ่านเรื่อง cost optimization จริงจังเลย แค่รู้ว่า Reserved Instances ถูกกว่า on-demand

### Reference Search

**SKILL:**

เนื่องจากยังไม่มี reference ผมค้นหาให้ครับ *(web_search: "AWS cost optimization EC2 RDS best practices 2025-2026")*

จากที่ค้นมา มี reference 3 ตัวที่ตรงกับสถานการณ์ของคุณ:

1. **AWS Cost Optimization Pillar — Well-Architected Framework** — เป็น official guide จาก AWS เอง ครอบคลุม right-sizing, pricing models, scheduling
2. **"How we cut our AWS bill by 40%"** (blog จาก startup ขนาดใกล้เคียง) — เล่าการใช้ Compute Savings Plans + Instance Scheduler แล้วลดได้ 40%
3. **AWS Trusted Advisor + Cost Explorer guide** — วิธีใช้ tool ที่ AWS ให้ฟรีเพื่อหา waste

มีตัวไหนที่รู้สึกว่าใกล้เคียงกับที่อยากทำมั้ยครับ?

**USER:**

ข้อ 2 น่าสนใจมากครับ startup คล้าย ๆ กัน แล้วลดได้ 40% ตรงเป้าเลย ข้อ 3 ก็ดี เพราะน่าจะเริ่มจากดู tool ของ AWS ก่อน

### Reference Summary

**SKILL:**

สรุป Reference:
- Reference หลัก: กรณีศึกษา startup ที่ลดค่า AWS 40% ด้วย Savings Plans + Scheduling
- Reference เสริม: AWS Trusted Advisor + Cost Explorer เป็นจุดเริ่มต้นวิเคราะห์ waste
- ทั้ง 2 ตัวสอดคล้องกับแนวทาง Right-sizing + Savings Plans ที่เลือกไว้

ต่อไปจะถามเรื่อง context จริง ๆ ของทีมครับ

---

## Phase 5 — Context

### Question 5.1

**SKILL** *(ask_user with choices):*

EC2 instance 3-4 ตัวที่ใช้อยู่ แบ่งเป็นอะไรบ้างครับ?

- A) Production ทั้งหมด
- B) Production 2 ตัว + Staging/Dev 1-2 ตัว
- C) Production 1 ตัว + Staging 1 ตัว + Dev 1-2 ตัว
- D) แบ่งแบบอื่น (ช่วยอธิบาย)

**USER:**

B ครับ Production 2 ตัว (app server + background worker) แล้วก็ Staging 1 ตัว กับ Dev 1 ตัว รวม 4 ตัว ทุกตัวเป็น t3.large

### Question 5.2

**SKILL** *(ask_user with choices):*

RDS PostgreSQL ตัวที่ใช้ spec ประมาณไหนครับ?

- A) db.t3.medium หรือเล็กกว่า
- B) db.t3.large
- C) db.r5 หรือ db.r6g series
- D) ไม่แน่ใจ ต้องไปเช็ค

**USER:**

B ครับ db.t3.large มี 1 ตัวสำหรับ production แล้วก็มี dev อีก 1 ตัวเป็น db.t3.medium

### Question 5.3

**SKILL** *(ask_user):*

traffic ที่บอกว่าหนักแค่ช่วง business hours — ช่วงกลางคืนกับวันหยุดมี traffic ประมาณเท่าไหร่ครับ เทียบกับ peak?

**USER:**

กลางคืนแทบไม่มี traffic เลยครับ อาจจะ 5% ของ peak มีแค่ cron job บางตัวที่ทำตอนตี 2-3 กับ health check ส่วนวันเสาร์-อาทิตย์ก็น้อยมาก ประมาณ 10-15% ของวันธรรมดา

### Question 5.4

**SKILL** *(ask_user with choices):*

ในทีม 5 คน ใครเป็นคนดูแล AWS ครับ?

- A) มีคนดูแลโดยเฉพาะ 1 คน (DevOps)
- B) ผม (คนถาม) ดูแลเอง เป็นงานข้างเคียง
- C) หลายคนช่วยกันดู ไม่มีเจ้าภาพชัดเจน

**USER:**

B ครับ ผมดูแลเองเป็นหลัก แต่งาน main คือ backend dev ดู infra เป็นงานรอง ใช้เวลาประมาณ 20-30% ของเวลาทำงาน

### Context Summary

**SKILL:**

สรุป Context:
- EC2: 4 ตัว (Prod 2 + Staging 1 + Dev 1) ทั้งหมด t3.large
- RDS: 2 ตัว (Prod db.t3.large + Dev db.t3.medium)
- Traffic: กลางคืน ~5% ของ peak, วันหยุด ~10-15%
- Staging/Dev ไม่ต้องเปิด 24/7
- คนดูแล AWS: 1 คน (backend dev ดูเป็นงานรอง) — ต้องเป็นวิธีที่ไม่ซับซ้อนเกินไป
- มี S3 buckets ด้วย (ยังไม่ได้ลงรายละเอียด)

ต่อไปจะถามเรื่อง criteria สำหรับตัดสินผลลัพธ์ครับ

---

## Phase 6 — Criteria

### Question 6.1

**SKILL** *(ask_user with choices):*

ถ้าต้องเลือก 3 อย่างที่สำคัญที่สุดในการลดค่า AWS คุณจัด priority ยังไงครับ?

- A) ประหยัดมากที่สุด > ทำง่ายไม่ซับซ้อน > ไม่กระทบ performance
- B) ไม่กระทบ performance > ทำง่ายไม่ซับซ้อน > ประหยัดมากที่สุด
- C) ทำง่ายไม่ซับซ้อน > ไม่กระทบ performance > ประหยัดมากที่สุด

**USER:**

C ครับ ทำง่ายสำคัญสุด เพราะผมดูแลคนเดียว ถ้าซับซ้อนเกินก็ไม่มีเวลาดูแลระยะยาว ถัดมาคือ performance ต้องไม่กระทบ user แล้วค่อยดูว่าประหยัดได้เท่าไหร่

### Question 6.2

**SKILL** *(ask_user):*

"ทำง่ายไม่ซับซ้อน" สำหรับคุณหมายความว่ายังไงครับ? เช่น setup เสร็จใน 1 วัน? ไม่ต้องเขียน script? ดูแลรักษาน้อย?

**USER:**

หมายถึงแต่ละ step ทำได้ใน 1-2 วัน ไม่ต้องเขียน custom tool ใหม่ทั้งชิ้น ใช้ feature ที่ AWS มีอยู่แล้ว แล้วก็ต้อง reversible ได้ ถ้ามีปัญหาก็ rollback กลับได้

### Question 6.3

**SKILL** *(ask_user with choices):*

ผลลัพธ์แบบไหนที่จะทำให้คุณรู้สึกว่า "ไม่คุ้มที่จะทำ"?

- A) ใช้เวลาเยอะแต่ลดได้แค่หลักร้อยบาท
- B) ต้อง lock-in commitment นาน ๆ (เช่น 3 ปี) ที่ยกเลิกไม่ได้
- C) ต้อง downtime ระหว่างเปลี่ยน
- D) ทุกข้อข้างบน

**USER:**

D ครับ ทุกข้อเลย โดยเฉพาะ B กับ C startup อาจจะ pivot ได้ทุกเมื่อ ถ้า lock 3 ปีแล้ว business เปลี่ยนก็เสียเปล่า

### Criteria Summary

**SKILL:**

สรุป Criteria (เรียงตาม priority):
1. **ความง่ายในการทำ** — แต่ละ step ทำได้ใน 1-2 วัน ใช้ feature ที่ AWS มีอยู่แล้ว reversible ได้
2. **ไม่กระทบ performance** — user experience ต้องเหมือนเดิมหรือดีขึ้น zero downtime
3. **ประหยัดจริง** — ลดได้ 30-40% (~15,000-20,000 บาท/เดือน) แต่ไม่ lock-in ระยะยาวเกินไป (1 ปีรับได้ แต่ 3 ปีไม่รับ)

เกณฑ์ disqualify: ใช้เวลาเยอะแต่ลดได้นิดเดียว, lock-in 3 ปี, ต้อง downtime

ครบทุก phase แล้วครับ ไปสร้าง Improved Prompt กันเลย

---

## Phase 7 — Synthesize

**SKILL:**

## Improved Prompt

ช่วยวางแผนลดค่าใช้จ่าย AWS สำหรับ startup ทีม 5 คน ที่ปัจจุบันจ่ายเดือนละ ~50,000 บาท โดยต้องการลดลง 30-40% (เหลือ ~30,000-35,000 บาท/เดือน) ภายใน 1 เดือน

**Infrastructure ปัจจุบัน:**
- EC2: 4x t3.large (Production app server 1, Production worker 1, Staging 1, Dev 1) ทั้งหมดเป็น on-demand เปิด 24/7
- RDS PostgreSQL: 2 ตัว (Production db.t3.large + Dev db.t3.medium) ทั้งหมด on-demand
- S3: มี buckets อยู่บ้าง (ไม่ใช่ค่าใช้จ่ายหลัก)
- Traffic pattern: heavy เฉพาะ business hours (จ-ศ เวลาทำการ), กลางคืน ~5% ของ peak, วันหยุด ~10-15%

**แนวทางที่ต้องการ:**
1. **Right-sizing** — วิเคราะห์ว่า t3.large จำเป็นจริงหรือไม่สำหรับแต่ละ instance โดยเฉพาะ Staging/Dev ที่อาจลดเป็น t3.medium หรือ t3.small ได้
2. **Compute Savings Plans (1 ปี, No Upfront หรือ Partial Upfront)** — สำหรับ Production EC2 + RDS ที่ต้องเปิดตลอด ห้ามทำ 3-year commitment เพราะ startup อาจ pivot
3. **Instance Scheduling** — ปิด Staging + Dev instances นอก business hours และวันหยุด (ลด ~65% ของเวลาที่เปิดเปล่า ๆ)
4. **RDS optimization** — พิจารณา Reserved Instances 1 ปีสำหรับ production RDS และปิด Dev RDS นอกเวลาทำงาน

**ข้อห้ามและข้อจำกัด:**
- ห้าม downtime ระหว่างเปลี่ยนแปลง ต้อง zero-downtime migration
- ห้ามเปลี่ยน database engine (ต้องเป็น PostgreSQL)
- ดูแลโดย backend dev คนเดียวที่ทำ infra เป็นงานรอง — แต่ละ step ต้องทำได้ใน 1-2 วัน
- ทุกการเปลี่ยนแปลงต้อง reversible ได้
- ใช้ feature/tool ที่ AWS มีอยู่แล้ว (Cost Explorer, Trusted Advisor, Instance Scheduler) ไม่ต้องสร้าง custom tool ใหม่

**Output ที่ต้องการ:**
- แผนทำเป็น step-by-step เรียงตามลำดับ impact สูง + ทำง่าย ก่อน
- แต่ละ step ระบุ: สิ่งที่ต้องทำ, estimated saving (บาท/เดือน), เวลาที่ใช้, ความเสี่ยง, วิธี rollback
- สรุปรวม estimated total saving เทียบกับเป้า 30-40%

---

### Discovery Summary

**Goal:** ลดค่าใช้จ่าย AWS ลง 30-40% (จาก ~50,000 บาท เหลือ ~30,000-35,000 บาท/เดือน) ภายใน 1 เดือน โดยไม่กระทบ performance

**Direction:** Right-sizing + Compute Savings Plans (1 ปี) เป็นแนวทางหลัก เสริมด้วย Instance Scheduling สำหรับ non-production environments ยังไม่เคย optimize มาก่อน (มี low-hanging fruit เยอะ)

**Reference:** กรณีศึกษา startup ที่ลดค่า AWS 40% ด้วย Savings Plans + Scheduling / AWS Trusted Advisor + Cost Explorer เป็นจุดเริ่มต้น

**Context:** ทีม 5 คน, ดูแล AWS คนเดียว (backend dev ที่ทำ infra เป็นงานรอง), 4 EC2 + 2 RDS ทั้งหมด on-demand, traffic หนักเฉพาะ business hours, Staging/Dev เปิด 24/7 โดยไม่จำเป็น

**Criteria:**
1. ความง่ายในการทำ (แต่ละ step ทำได้ใน 1-2 วัน, reversible, ใช้ AWS native tools)
2. ไม่กระทบ performance (zero downtime, user experience ไม่เปลี่ยน)
3. ประหยัดจริง (ลด 30-40% โดยไม่ lock-in เกิน 1 ปี)

---

**SKILL:**

นี่คือ Improved Prompt ที่สรุปจากทุก phase ครับ มี่อะไรอยากปรับเปลี่ยนมั้ยครับ?

**USER:**

ดีมากครับ ครอบคลุมหมดเลย แค่เพิ่มนิดนึงว่าอยากให้เทียบ Savings Plans กับ Reserved Instances ด้วยว่าอันไหนเหมาะกว่า เพราะยังไม่แน่ใจว่าต่างกันยังไง

**SKILL:**

เพิ่มให้แล้วครับ ในส่วน Savings Plans จะเพิ่มให้เปรียบเทียบ Compute Savings Plans vs. EC2 Reserved Instances ว่าอันไหนเหมาะกว่าสำหรับ startup ที่อาจ pivot พร้อมอธิบายข้อดีข้อเสียของแต่ละแบบ

*(Updated in the prompt above — item 2 now reads: "Compute Savings Plans (1 ปี, No Upfront หรือ Partial Upfront) — เปรียบเทียบกับ EC2 Reserved Instances ว่าแบบไหนเหมาะกับ startup ที่อาจ pivot มากกว่า")*

**USER:**

เพอร์เฟกต์ครับ ใช้ได้เลย

---

## Next Step

**SKILL** *(ask_user with choices):*

ต้องการทำอะไรต่อครับ?

- A) **Create a Plan** — ให้สร้างแผนปฏิบัติการ step-by-step จาก Improved Prompt นี้
- B) **Done** — เอา Improved Prompt ไปใช้เอง ไม่ต้องทำอะไรเพิ่ม

**USER:**

A ครับ อยากได้แผนเลย

**SKILL:**

รับทราบครับ ส่งต่อให้ Plan subagent ดำเนินการสร้างแผนปฏิบัติจาก Improved Prompt และ Discovery Summary ที่สรุปไว้ครับ

*(Delegates to Agent tool with subagent_type: "Plan", passing full Improved Prompt + Discovery Summary)*

---

## Observations on Skill Execution

| Phase | Questions Asked | Technique Used | Notes |
|-------|----------------|----------------|-------|
| Receive (Phase 1) | 0 | Acknowledge + restate | Did not jump to solutions |
| Goal (Phase 2) | 2 | Multiple choice for both | Measurable target established (30-40%, 1 month) |
| Direction (Phase 3) | 2 + 1 proposal | Constraint elimination, then 3 proposed approaches | User selected recommended approach + supplement |
| Reference (Phase 4) | 1 + web_search | Multiple choice then AI search | User had no references; AI provided 3 relevant ones |
| Context (Phase 5) | 4 | Mix of multiple choice and open-ended | Revealed critical facts: all on-demand, Staging/Dev run 24/7 unnecessarily, 1 person manages infra |
| Criteria (Phase 6) | 3 | Force-ranked priorities, then drilled into "easy" | Key insight: reversibility and simplicity matter more than max savings |
| Synthesize (Phase 7) | 1 iteration | Draft + feedback + adjust | User requested one addition (SP vs RI comparison) |

**Total questions asked:** 13 (across phases 2-7)
**Key discovery moments:**
- Staging/Dev running 24/7 unnecessarily — immediate savings opportunity
- All instances are on-demand with zero prior optimization — lots of low-hanging fruit
- One person manages infra part-time — simplicity is the top priority
- Startup may pivot — no 3-year commitments
- Night/weekend traffic is negligible — scheduling is highly effective
