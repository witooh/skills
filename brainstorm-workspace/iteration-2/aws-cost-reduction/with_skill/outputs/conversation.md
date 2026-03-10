# Brainstorm Skill Simulation: AWS Cost Reduction

## User Prompt

> "brainstorm วิธีลดค่าใช้จ่าย AWS ของทีม ตอนนี้เดือนละประมาณ 5 หมื่นบาท ใช้ EC2 กับ RDS เป็นหลัก"

---

## Triage Decision (Internal)

**Analysis of user prompt:**

- Contains specific numbers: ~50,000 THB/month
- Contains specific tech stack: EC2, RDS
- Contains specific problem: reduce AWS costs
- Signal phrase: "brainstorm วิธี..." (brainstorm ways to...)
- User already provided current situation with concrete details

**Mode Selected: Focused Mode**

**Rationale:** The prompt already contains specifics (numbers, tech stack, current situation). The user says "brainstorm วิธี..." which is a Focused Mode signal. They don't need open-ended exploration or a prompt — they want actionable strategies for a well-defined problem.

**Flow:** Targeted discovery (2-4 questions) — only ask about genuine unknowns, skip what's already stated.

---

## Conversation

---

### Phase 1 — Acknowledge Context

**SKILL:**

เข้าใจแล้วครับ ผมสรุปสิ่งที่รู้จาก prompt ก่อนนะ:

- **Monthly AWS spend:** ~50,000 THB/month
- **Primary services:** EC2 and RDS
- **Goal:** Reduce monthly cost

ก่อนจะให้ recommendations ขอถามเพิ่มอีก 2 เรื่องเพื่อให้คำแนะนำตรงจุดมากขึ้นครับ

---

### Phase 2 — Fill Gaps

**SKILL asks Question 1:**

> **AskUserQuestion**
>
> "ตอนนี้ EC2 instances ใช้ pattern ยังไงครับ?"
>
> **Options:**
> - A) Run 24/7 แต่ traffic จริงๆ แค่ช่วง business hours
> - B) Run 24/7 มี traffic ตลอด
> - C) มี auto-scaling อยู่แล้ว ปรับตาม load
> - D) ไม่แน่ใจ ยังไม่เคยดู usage pattern

---

**USER (simulated):**

> A ครับ — Run 24/7 แต่ traffic จริงๆ แค่ช่วง business hours ประมาณ 9-18 น. วันจันทร์-ศุกร์ ใช้ EC2 อยู่ 3-4 ตัว เป็น t3.large ทั้งหมด แล้วก็มี RDS PostgreSQL 1 ตัว กับ S3 buckets อีกหน่อย

---

**SKILL (internal note):** ได้ข้อมูลเพิ่มเยอะมาก — EC2 3-4 instances (t3.large), RDS PostgreSQL 1 instance, S3, traffic เฉพาะ business hours weekdays เท่านั้น นี่เป็น key insight เพราะ run 24/7 แต่ใช้จริงแค่ ~45 ชั่วโมง/สัปดาห์ จาก 168 ชั่วโมง (~27% utilization by hours)

---

**SKILL asks Question 2:**

> **AskUserQuestion**
>
> "สิ่งที่สำคัญที่สุดในการลดค่าใช้จ่ายรอบนี้คืออะไรครับ?"
>
> **Options:**
> - A) ลดให้ได้เยอะที่สุด ยอมเปลี่ยน architecture ได้
> - B) ลดพอประมาณ แต่ต้องไม่เพิ่ม complexity ให้ทีม
> - C) ลดแบบ quick win ก่อน ไม่ต้องเปลี่ยนอะไรมาก
> - D) ลดแบบยั่งยืน ค่อยๆ ทำ ไม่รีบ

---

**USER (simulated):**

> C ครับ — อยากได้ quick win ก่อน ทีมมี 5 คน เป็น startup อยู่ ไม่มีเวลา re-architect อะไรใหญ่ๆ ตอนนี้ ถ้าลดได้สัก 30-40% ก็ดีมากแล้ว

---

**SKILL (internal note):** เข้าใจครบแล้ว — startup, team 5 คน, ต้องการ quick wins, target ลด 30-40% (~15,000-20,000 THB/month), ไม่มีเวลา re-architect สิ่งที่รู้ตอนนี้เพียงพอจะทำ recommendations ได้เลย ไม่ต้องถามเพิ่ม

**Phase transition:** มีข้อมูลครบ — รู้ usage pattern (business hours only), priority (quick wins), constraints (small team, no re-architecture), target (30-40% reduction) ไปต่อ Phase 3 Strategize ได้เลย

---

### Phase 3 — Strategize

**SKILL:**

จากข้อมูลทั้งหมด นี่คือแผนลดค่าใช้จ่าย AWS แบบ quick win เรียงจาก impact สูง + effort ต่ำ ก่อนครับ:

---

## AWS Cost Reduction Strategies

### Current Situation Summary

| Item | Detail |
|------|--------|
| Monthly spend | ~50,000 THB |
| EC2 | 3-4x t3.large (24/7) |
| RDS | 1x PostgreSQL (24/7) |
| S3 | Small usage |
| Traffic pattern | Business hours only (Mon-Fri, 9-18) |
| Team | 5 people, startup |
| Target | 30-40% reduction (~15,000-20,000 THB/month) |

---

### Quick Wins (Start Here)

#### 1. EC2 Scheduling — Stop/Start Non-Production Hours

| Aspect | Detail |
|--------|--------|
| What | Use AWS Instance Scheduler or a simple Lambda + EventBridge to stop EC2 instances outside business hours |
| Impact | Save ~65-70% on EC2 costs (run ~50 hrs/week instead of 168) |
| Effort | 2-4 hours setup |
| Estimated saving | 15,000-20,000 THB/month (EC2 portion alone) |
| Risk | Must ensure no scheduled jobs run at night; need graceful shutdown handling |
| How | Create EventBridge rules: start at 08:30 Mon-Fri, stop at 18:30 Mon-Fri |

This single change alone could hit your 30-40% target.

#### 2. RDS Scheduling or Downsize

| Aspect | Detail |
|--------|--------|
| What | Option A: Stop RDS outside business hours (if dev/staging). Option B: Consider Aurora Serverless v2 for auto-pause |
| Impact | Save 50-65% on RDS if schedulable |
| Effort | 2-3 hours |
| Estimated saving | 3,000-8,000 THB/month |
| Risk | RDS stop/start takes 5-10 min; connections will drop. Only do this if acceptable for your workflow. Production DB that has nightly batch jobs should NOT be stopped |
| How | If RDS is production and must stay 24/7, instead consider Reserved Instance (see #4) |

#### 3. Right-size EC2 Instances

| Aspect | Detail |
|--------|--------|
| What | Check CloudWatch CPU/Memory metrics. If average CPU < 20%, downgrade from t3.large to t3.medium or t3.small |
| Impact | 50% cost reduction per downsized instance (t3.large -> t3.medium) |
| Effort | 1-2 hours to check metrics, 30 min per instance to resize |
| Estimated saving | 2,000-5,000 THB/month |
| Risk | Low — t3 instances can burst if needed; monitor for 1 week after change |
| How | AWS Console -> CloudWatch -> EC2 metrics -> check avg CPU over last 2 weeks |

---

### Medium-Term Improvements (Next Month)

#### 4. Reserved Instances or Savings Plans

| Aspect | Detail |
|--------|--------|
| What | Commit to 1-year Reserved Instances (no upfront) for instances that must run 24/7 (e.g., production RDS) |
| Impact | 30-40% discount vs on-demand |
| Effort | 1 hour to purchase |
| Estimated saving | 3,000-5,000 THB/month on always-on resources |
| Risk | Locked in for 1 year; choose "no upfront" to minimize commitment risk for a startup |
| How | AWS Console -> Cost Explorer -> Reserved Instance recommendations |

#### 5. S3 Lifecycle Policies

| Aspect | Detail |
|--------|--------|
| What | Move old objects to S3 Infrequent Access or Glacier after 30/90 days |
| Impact | 40-80% reduction on storage costs for old data |
| Effort | 30 min |
| Estimated saving | Likely small (500-1,500 THB/month) unless you have a lot of data |
| Risk | None for data you don't access frequently; retrieval from Glacier takes time |

#### 6. Review and Delete Unused Resources

| Aspect | Detail |
|--------|--------|
| What | Check for unattached EBS volumes, old snapshots, unused Elastic IPs, idle load balancers |
| Impact | Varies — often 5-10% of bill is zombie resources |
| Effort | 1-2 hours audit |
| Estimated saving | 1,000-3,000 THB/month |
| Risk | None if you verify before deleting |
| How | AWS Trusted Advisor (free tier) or Cost Explorer -> cost by resource |

---

### Action Plan

**Start here this week:**

| Priority | Action | Expected saving | Time needed |
|----------|--------|----------------|-------------|
| 1 | Set up EC2 scheduling (stop nights + weekends) | 15,000-20,000 THB/month | 2-4 hours |
| 2 | Right-size EC2 (check CloudWatch, downgrade if over-provisioned) | 2,000-5,000 THB/month | 2-3 hours |
| 3 | Audit zombie resources (EBS, snapshots, EIPs) | 1,000-3,000 THB/month | 1-2 hours |

**Combined estimated savings from quick wins: 18,000-28,000 THB/month (36-56%)**

This should exceed your 30-40% target with just the quick wins. Reserved Instances and S3 lifecycle can be done next month for additional savings.

---

### Phase 4 — Refine

**SKILL:**

นี่คือ recommendations เรียงจาก quick win ไปถึง medium-term ครับ โดย strategy #1 (EC2 scheduling) อย่างเดียวน่าจะลดได้ใกล้ target แล้ว

มีอะไรอยากปรับหรือถามเพิ่มไหมครับ?

> **AskUserQuestion**
>
> "อยากให้ช่วยอะไรต่อครับ?"
>
> **Options:**
> - A) ช่วยทำ implementation plan แบบ step-by-step สำหรับ EC2 scheduling
> - B) อยากดู strategy เพิ่มเรื่อง container/serverless migration
> - C) ครบแล้ว เอาไปทำได้เลย
> - D) อยากปรับ/ถามเพิ่มเรื่องอื่น

---

**USER (simulated):**

> A ครับ — ช่วยทำ step-by-step สำหรับ EC2 scheduling หน่อย อยากได้แบบทำตามได้เลย

---

**SKILL:**

เข้าใจครับ จะส่งต่อให้ Plan agent ทำ implementation plan แบบ step-by-step สำหรับ EC2 scheduling ให้นะครับ

> **Agent** (subagent_type: "Plan")
>
> Context: User wants a step-by-step implementation plan for EC2 Instance Scheduling using EventBridge + Lambda to stop/start 3-4 t3.large instances. Schedule: Start at 08:30 Mon-Fri, Stop at 18:30 Mon-Fri. Startup environment, team of 5, needs to be simple and followable.

*(Handoff to Plan subagent — end of brainstorm workflow)*

---

## End of Simulation

---

## Observation Table

| Metric | Value |
|--------|-------|
| Mode selected | Focused |
| Triage reasoning | Prompt contained specifics (numbers, tech stack, current situation) + "brainstorm วิธี" signal |
| Total questions asked | 2 |
| Question 1 topic | Usage pattern (EC2 traffic hours) |
| Question 2 topic | Priority/constraints (quick win vs re-architecture) |
| Questions skipped | 0 redundant questions — everything in the prompt was acknowledged, not re-asked |
| Phases executed | Phase 1 (Acknowledge) -> Phase 2 (Fill Gaps, 2 questions) -> Phase 3 (Strategize) -> Phase 4 (Refine + next step) |
| Output format | Actionable strategies with priorities and estimated impact (correct for Focused mode) |
| Time-to-value | 2 questions before receiving full recommendations |
| User turns before output | 3 (initial prompt + 2 answers) |
| Recommendations given | 6 strategies (3 quick wins + 3 medium-term) |
| Estimated total savings | 18,000-28,000 THB/month from quick wins alone (36-56%) |
| Target met? | Yes — exceeds the 30-40% target |
| Next step offered | 4 options via AskUserQuestion (plan, go deeper, done, adjust) |
| Handoff triggered | Yes — to Plan subagent for EC2 scheduling implementation |

### Key Observations on Skill Behavior

| Observation | Detail |
|-------------|--------|
| Triage accuracy | Correctly identified Focused mode from signals ("brainstorm วิธี" + specific numbers/tech) |
| Context acknowledgment | Phase 1 explicitly listed known facts, avoiding re-asking |
| Question efficiency | Only 2 questions, both targeting genuine unknowns that would change recommendations |
| Multiple choice usage | Both questions used options array — faster UX, lower cognitive load |
| Information extraction | Got rich additional context from answers (instance count, types, team size, PostgreSQL, S3) |
| Output structure | Matched Focused mode spec: prioritized list, quick wins first, each with impact/effort/risk |
| Actionability | Every recommendation includes specific "How" steps, not just theory |
| Clear "start here" | Explicit action plan table with priority order |
| Next steps | Offered continuation options including Plan subagent handoff |
| Language mirroring | Used user's level of technical language, didn't over-explain AWS concepts to an engineer |
