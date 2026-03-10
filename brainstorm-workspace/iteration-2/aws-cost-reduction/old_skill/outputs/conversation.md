# Old Skill (v1.2) — Simulated Conversation

**User Prompt:** "brainstorm วิธีลดค่าใช้จ่าย AWS ของทีม ตอนนี้เดือนละประมาณ 5 หมื่นบาท ใช้ EC2 กับ RDS เป็นหลัก"

**Simulated User Persona:** Thai DevOps/backend engineer, team of 5, startup environment, running 3-4 EC2 instances (t3.large), one RDS PostgreSQL, some S3 buckets, services run 24/7 but traffic is mainly business hours.

---

## Phase 1 — Receive

**SKILL:**

เข้าใจครับ คุณต้องการหาวิธีลดค่าใช้จ่าย AWS ของทีม ซึ่งตอนนี้อยู่ที่ประมาณเดือนละ 50,000 บาท โดยใช้ EC2 กับ RDS เป็นหลัก

ก่อนที่ผมจะช่วยหาวิธีลดค่าใช้จ่าย ผมอยากถามคำถามสักหน่อยเพื่อให้ผลลัพธ์ตรงกับสถานการณ์จริงของทีมคุณมากที่สุด เริ่มจากเป้าหมายกันเลยนะครับ

---

## Phase 2 — Goal

### Question 2.1

**SKILL** *(via ask_user with choices):*

> สิ่งที่สำคัญที่สุดในการลดค่าใช้จ่ายครั้งนี้คืออะไรครับ?
>
> A) ลดค่าใช้จ่ายให้ได้มากที่สุด ยอมรับการเปลี่ยนแปลงระบบได้
> B) ลดค่าใช้จ่ายในระดับที่สมเหตุสมผล โดยไม่ต้องเปลี่ยนระบบมาก
> C) ลดค่าใช้จ่ายเพื่อให้อยู่ในงบประมาณที่กำหนด (มีตัวเลขเป้าหมาย)

**USER:**

> B ครับ ไม่อยากเปลี่ยนระบบเยอะ แต่อยากลดให้ได้สักประมาณ 30-40% ถ้าเป็นไปได้

### Question 2.2

**SKILL** *(via ask_user with choices):*

> ถ้าลดได้ 30-40% หมายความว่าเป้าหมายอยู่ที่ประมาณ 30,000-35,000 บาท/เดือน ใช่ไหมครับ? แล้วมี deadline ที่อยากให้ทำเสร็จไหม?
>
> A) อยากเห็นผลใน 1-2 สัปดาห์
> B) ภายใน 1 เดือน
> C) ค่อยๆ ทำ ไม่เร่ง ขอให้ได้ผลจริง

**USER:**

> B ครับ ภายในเดือนนี้ เพราะ CEO เริ่มถามแล้ว

### Phase 2 Summary

**SKILL:**

สรุป Goal: ลดค่าใช้จ่าย AWS จากเดือนละ ~50,000 บาท ลงเหลือ ~30,000-35,000 บาท (ลด 30-40%) ภายใน 1 เดือน โดยไม่ต้องเปลี่ยนสถาปัตยกรรมระบบมาก ไปต่อ Phase ถัดไปนะครับ

---

## Phase 3 — Direction

### Question 3.1

**SKILL** *(via ask_user with choices):*

> มีอะไรที่ห้ามเกิดขึ้นเด็ดขาดไหมครับ?
>
> A) ระบบ downtime ไม่ได้เลย แม้แค่นาที
> B) downtime ได้บ้างตอนดึกๆ แต่ช่วงเวลาทำงานต้องปกติ
> C) downtime ช่วงสั้นๆ ได้ ถ้าแจ้งล่วงหน้า

**USER:**

> B ครับ ช่วง business hours ห้าม down แต่ตอนตี 2-3 ทำ maintenance ได้

### Question 3.2

**SKILL** *(via ask_user with choices):*

> เคยลองลดค่าใช้จ่ายมาก่อนไหมครับ? ทำอะไรไปแล้วบ้าง?
>
> A) ยังไม่เคยทำอะไรเลย ใช้ on-demand มาตลอด
> B) เคยลอง resize instance แล้ว แต่ไม่ค่อยมีผล
> C) เคยซื้อ Reserved Instance/Savings Plan บ้างแล้ว

**USER:**

> A ครับ ยังไม่เคยทำอะไรเลย ตอนนี้ใช้ on-demand ทั้งหมด เพราะตอนแรกคิดว่าจะ scale แล้วก็ยังไม่ได้ทำ

### Question 3.3

**SKILL** *(via ask_user with choices):*

> ระดับความเสี่ยงที่ยอมรับได้ในการเปลี่ยนแปลง?
>
> A) Conservative — ทำแต่สิ่งที่มั่นใจว่าปลอดภัย 100%
> B) Moderate — ยอมรับความเสี่ยงบ้าง ถ้ามี rollback plan
> C) Aggressive — ลองได้เต็มที่ ขอให้ลดค่าใช้จ่ายมาก

**USER:**

> B ครับ moderate ได้ ขอให้มี rollback plan

### Proposed Approaches

**SKILL:**

จากข้อมูลที่ได้ — ใช้ on-demand ทั้งหมด, downtime ได้นอก business hours, ยอมรับความเสี่ยงระดับ moderate — ผมเห็นทางเลือกหลักๆ 3 แบบครับ:

> **A) Quick Wins — Right-sizing + Scheduling (แนะนำ)**
> ปรับขนาด instance ให้ตรง workload จริง + ตั้ง schedule ปิด/เปิดตาม business hours
> - ข้อดี: ทำได้เร็ว, เสี่ยงต่ำ, เห็นผลทันที
> - ข้อเสีย: อาจลดได้ไม่ถึง 40%
>
> **B) Commitment-based Savings — Reserved Instances / Savings Plans**
> ซื้อ commitment 1 ปี เพื่อรับส่วนลด
> - ข้อดี: ลดได้เยอะ (30-60%)
> - ข้อเสีย: ต้อง commit ล่วงหน้า, ถ้า workload เปลี่ยนจะเสียเงินฟรี
>
> **C) ผสม A + B — Quick wins ก่อน แล้วค่อยซื้อ commitment หลังเห็นตัวเลขจริง**
> - ข้อดี: ได้ผลทั้งระยะสั้นและระยะยาว
> - ข้อเสีย: ใช้เวลามากกว่า
>
> ผมแนะนำ A ครับ เพราะทำได้เร็วภายใน 1 เดือน และเสี่ยงต่ำ แต่ C ก็น่าสนใจถ้าอยากลดได้มากกว่า อันไหนตรงใจครับ?

**USER:**

> C ครับ เริ่มจาก quick wins ก่อน แล้วค่อยดู commitment ทีหลัง

### Phase 3 Summary

**SKILL:**

สรุป Direction: ใช้แนวทาง "Quick Wins ก่อน แล้วค่อย Commit" — เริ่มจาก right-sizing + scheduling ก่อน แล้วพิจารณา Savings Plans/Reserved Instances หลังรู้ baseline จริง ข้อจำกัดสำคัญคือ ห้าม downtime ช่วง business hours และต้องมี rollback plan

---

## Phase 4 — Reference

### Question 4.1

**SKILL** *(via ask_user with choices):*

> มีบทความ เครื่องมือ หรือตัวอย่างที่เคยดูเรื่องลดค่าใช้จ่าย AWS ไหมครับ?
>
> A) ไม่มีเลย ยังไม่ได้ศึกษา
> B) เคยอ่านบทความบ้างแต่จำไม่ได้
> C) มี มีลิงก์/เครื่องมือที่สนใจ

**USER:**

> A ครับ ยังไม่ได้ศึกษาเลย รู้แค่ว่ามี AWS Cost Explorer

### Reference Search

**SKILL:**

*(ใช้ web_search ค้นหา references)*

ผมค้นหามาให้ 3 แหล่งอ้างอิงครับ:

1. **AWS Well-Architected Cost Optimization Pillar** — best practices จาก AWS โดยตรง มีเรื่อง right-sizing, scheduling, commitment
2. **AWS Instance Scheduler** — เครื่องมือของ AWS สำหรับตั้ง schedule เปิด/ปิด EC2 และ RDS อัตโนมัติ
3. **AWS Compute Optimizer** — เครื่องมือ free ของ AWS ที่วิเคราะห์ usage แล้วแนะนำ instance type ที่เหมาะสม

### Question 4.2

**SKILL** *(via ask_user with choices):*

> จาก 3 อันนี้ อันไหนดูน่าสนใจสำหรับสถานการณ์ของทีมครับ?
>
> A) AWS Instance Scheduler — ตรงกับเรื่อง scheduling ที่เราจะทำ
> B) AWS Compute Optimizer — อยากรู้ว่า instance ปัจจุบัน oversize ไหม
> C) ทั้ง A และ B เลย ดูเหมือนใช้ได้ทั้งคู่

**USER:**

> C ครับ ทั้งสองอันเลย Compute Optimizer ไม่รู้ว่ามี จะลองเปิดดู

### Phase 4 Summary

**SKILL:**

สรุป Reference: ใช้ AWS Compute Optimizer สำหรับ right-sizing analysis และ AWS Instance Scheduler สำหรับ schedule เปิด/ปิดนอก business hours เป็น reference หลัก พร้อมอ้างอิง AWS Well-Architected Cost Optimization Pillar

---

## Phase 5 — Context

### Question 5.1

**SKILL** *(via ask_user with choices):*

> ช่วยบอกรายละเอียดของ infrastructure ตอนนี้ได้ไหมครับ? EC2 มีกี่ตัว และเป็น instance type อะไร?
>
> A) 2-3 ตัว ขนาดเล็ก (t3.small/medium)
> B) 3-4 ตัว ขนาดกลาง (t3.large หรือ m5.large)
> C) 5 ตัวขึ้นไป หลายขนาด
> D) ไม่แน่ใจ ต้องไปเช็ค

**USER:**

> B ครับ มี 3 ตัว t3.large กับอีก 1 ตัว t3.medium สำหรับ staging รวม 4 ตัว

### Question 5.2

**SKILL** *(via ask_user with choices):*

> RDS เป็น instance type อะไรครับ? แล้ว Multi-AZ ไหม?
>
> A) db.t3.medium, Single-AZ
> B) db.t3.large, Single-AZ
> C) db.r5.large หรือใหญ่กว่า, Multi-AZ
> D) ไม่แน่ใจ

**USER:**

> B ครับ db.t3.large, Single-AZ, PostgreSQL

### Question 5.3

**SKILL** *(via ask_user):*

> ในทีม 5 คน มีใครจัดการ AWS infrastructure เป็นหลักบ้างครับ? และมีประสบการณ์กับ AWS มากน้อยแค่ไหน?
>
> A) มีคนเดียวที่ดูแล (ตัวเอง) ประสบการณ์ปานกลาง
> B) มี 2-3 คนที่พอช่วยได้
> C) ทุกคนช่วยกัน แต่ไม่มีใครเชี่ยวชาญจริงจัง

**USER:**

> A ครับ ผมดูแลคนเดียว ประสบการณ์ AWS สัก 2 ปี พอรู้เรื่อง แต่ไม่ได้เชี่ยวชาญ cost optimization เฉพาะทาง

### Phase 5 Summary

**SKILL:**

สรุป Context:
- Infrastructure: EC2 x4 (3x t3.large + 1x t3.medium staging), RDS db.t3.large PostgreSQL Single-AZ, S3 buckets บางส่วน
- ทุกอย่างรัน 24/7 แต่ traffic จริงเฉพาะ business hours
- ทีม 5 คน แต่มี 1 คน (user) ดูแล infra คนเดียว ประสบการณ์ AWS 2 ปี
- Staging instance รันตลอดเวลาเช่นกัน

---

## Phase 6 — Criteria

### Question 6.1

**SKILL** *(via ask_user with choices):*

> ถ้าต้องเลือก 2-3 อย่างที่สำคัญที่สุดในแผนลดค่าใช้จ่ายนี้ อะไรสำคัญสุดครับ?
>
> A) ลดเงินได้จริง ตัวเลขต้องชัดเจน
> B) ทำได้ง่าย ไม่ซับซ้อน คนเดียวจัดการได้
> C) ไม่กระทบ performance ของระบบ production
> D) มี rollback plan ชัดเจน กลับไปสถานะเดิมได้ทันที

**USER:**

> B กับ C ครับ ทำง่ายที่สุดเพราะผมดูแลคนเดียว และห้ามกระทบ production เด็ดขาด

### Question 6.2

**SKILL** *(via ask_user with choices):*

> ถ้าต้อง force rank — ระหว่าง "ทำง่าย คนเดียวจัดการได้" กับ "ไม่กระทบ production" อันไหนสำคัญกว่ากันครับ?
>
> A) ไม่กระทบ production สำคัญกว่า — ยอมทำยากขึ้นได้
> B) ทำง่ายสำคัญกว่า — ยอมรับ risk เล็กน้อยได้

**USER:**

> A ครับ production ต้องปกติ สำคัญสุด

### Phase 6 Summary

**SKILL:**

สรุป Criteria (เรียงตามลำดับความสำคัญ):
1. **ไม่กระทบ production** — ระบบช่วง business hours ต้อง stable เหมือนเดิม
2. **ทำง่าย คนเดียวจัดการได้** — ต้องไม่ซับซ้อนจนต้องมีทีม DevOps เฉพาะทาง
3. **เห็นผลเป็นตัวเลข** — ต้องวัดได้ว่าลดลงเท่าไหร่

---

## Phase 7 — Synthesize

### Draft Improved Prompt

**SKILL:**

จากทุกอย่างที่เราคุยกันมา ผมสร้าง Improved Prompt ให้ครับ:

---

## Improved Prompt

ช่วยสร้างแผนลดค่าใช้จ่าย AWS แบบ step-by-step สำหรับ startup ทีมเล็ก (5 คน) ที่ใช้จ่ายเดือนละ ~50,000 บาท โดยมีเป้าหมายลดลงเหลือ 30,000-35,000 บาท/เดือน (ลด 30-40%) ภายใน 1 เดือน

**Infrastructure ปัจจุบัน:**
- EC2: 3x t3.large (production) + 1x t3.medium (staging) — ทั้งหมดรัน on-demand 24/7
- RDS: 1x db.t3.large PostgreSQL, Single-AZ
- S3: มีใช้บ้าง (ไม่ใช่ค่าใช้จ่ายหลัก)
- Traffic จริงเฉพาะ business hours (จันทร์-ศุกร์ 9:00-18:00) แต่ระบบรัน 24/7

**แนวทางหลัก:** เริ่มจาก quick wins (right-sizing + scheduling) ก่อน แล้วค่อยพิจารณา Savings Plans/Reserved Instances หลังจากรู้ baseline จริง

**ข้อจำกัดสำคัญ:**
- ห้าม downtime ช่วง business hours เด็ดขาด — maintenance ได้เฉพาะช่วงดึก
- DevOps 1 คนดูแลทั้งหมด (ประสบการณ์ AWS 2 ปี) — แผนต้องไม่ซับซ้อนเกินไป
- ต้องมี rollback plan ทุก step
- ไม่ต้องเปลี่ยนสถาปัตยกรรมระบบใหม่

**เครื่องมือที่จะใช้:**
- AWS Compute Optimizer สำหรับ right-sizing recommendations
- AWS Instance Scheduler สำหรับ schedule เปิด/ปิดอัตโนมัติ
- AWS Cost Explorer สำหรับ tracking ผล

**เกณฑ์ประเมินผล (เรียงตามความสำคัญ):**
1. ไม่กระทบ production — ระบบช่วง business hours ต้อง stable เหมือนเดิม
2. ทำง่าย คนเดียวจัดการได้ — ทุก step ต้องทำได้ด้วย DevOps 1 คน
3. เห็นผลเป็นตัวเลข — ต้องวัดได้ว่าลดลงกี่บาท/เดือน

ช่วยให้แผนเป็น checklist ที่ระบุ: สิ่งที่ต้องทำ, ค่าใช้จ่ายที่คาดว่าจะลดได้, ระดับความเสี่ยง, และ rollback plan ของแต่ละ step

---

### Discovery Summary

**Goal:** ลดค่าใช้จ่าย AWS จาก ~50,000 บาท/เดือน ลงเหลือ 30,000-35,000 บาท/เดือน (ลด 30-40%) ภายใน 1 เดือน โดยไม่ต้องเปลี่ยนสถาปัตยกรรมมาก

**Direction:** Quick Wins ก่อน (right-sizing + scheduling) แล้วค่อยพิจารณา commitment-based savings ทีหลัง — เลือกเพราะทำได้เร็ว เสี่ยงต่ำ เหมาะกับ DevOps 1 คน

**Reference:** AWS Compute Optimizer, AWS Instance Scheduler, AWS Well-Architected Cost Optimization Pillar

**Context:** Startup ทีม 5 คน, DevOps 1 คน (ประสบการณ์ 2 ปี), EC2 4 ตัว + RDS 1 ตัว ทั้งหมด on-demand 24/7, traffic เฉพาะ business hours

**Criteria:** (1) Production stability first (2) Simplicity — 1 person can execute (3) Measurable cost reduction

---

### Confirmation

**SKILL** *(via ask_user with choices):*

> Improved Prompt นี้ครอบคลุมสิ่งที่คุณต้องการไหมครับ? มีอะไรอยากปรับไหม?
>
> A) ดีแล้ว ไม่ต้องแก้
> B) อยากเพิ่ม/ปรับบางส่วน
> C) เปลี่ยนแนวทางเลย

**USER:**

> A ครับ ดีแล้ว ครอบคลุมดี

---

## Next Step

**SKILL** *(via ask_user with choices):*

> ต้องการทำอะไรต่อครับ?
>
> A) Create a Plan — ให้สร้างแผนปฏิบัติการ step-by-step
> B) Done — เอา Improved Prompt ไปใช้เอง

**USER:**

> B ครับ เอา prompt ไปใช้เองได้

---

## Workflow Complete

**SKILL:**

เรียบร้อยครับ! Improved Prompt พร้อมใช้งานแล้ว สามารถเอาไปใส่ใน Claude หรือ AI ตัวไหนก็ได้เพื่อให้สร้างแผนลดค่าใช้จ่าย AWS ที่ตรงกับสถานการณ์จริงของทีมคุณ ขอให้ลดค่าใช้จ่ายสำเร็จครับ!

---

## Simulation Metadata

| Field | Value |
|-------|-------|
| Skill Version | 1.2 (Old) |
| Total Phases Executed | 7/7 |
| Total Questions Asked | 12 |
| Phase 2 (Goal) Questions | 2 |
| Phase 3 (Direction) Questions | 3 + approach proposal |
| Phase 4 (Reference) Questions | 2 + web search |
| Phase 5 (Context) Questions | 3 |
| Phase 6 (Criteria) Questions | 2 |
| Phase 7 (Synthesize) Questions | 1 (confirmation) + 1 (next step) |
| Multiple Choice Used | 12/12 (100%) |
| Open-ended Questions | 0 |
| User Said "I don't know" | 0 |
| Phase Skipped | 0 |
| Approach Proposed | Yes (3 options with recommendation) |
| References Found via Search | 3 |
| Final Output Format | Improved Prompt + Discovery Summary |
