# Brainstorm: วิธีลดค่าใช้จ่าย AWS

**Context:** ค่าใช้จ่ายปัจจุบัน ~50,000 THB/เดือน, ใช้ EC2 + RDS เป็นหลัก

---

## 1. EC2 Cost Optimization

### 1.1 Right-sizing Instances
- เปิด AWS Cost Explorer แล้วดู CPU/Memory utilization ย้อนหลัง 2 สัปดาห์
- ถ้า average CPU < 20% หรือ memory < 40% แสดงว่า over-provisioned สามารถลดขนาด instance ลงได้
- ใช้ AWS Compute Optimizer ซึ่งจะแนะนำ instance type ที่เหมาะสมให้อัตโนมัติ
- ประหยัดได้ประมาณ 20-40% จากการ downsize

### 1.2 เปลี่ยนเป็น Reserved Instances หรือ Savings Plans
- ถ้ารู้ว่าจะใช้ EC2 ต่อไปอีกอย่างน้อย 1 ปี ซื้อ Reserved Instances (1-year, no upfront) ประหยัดได้ ~30-40%
- Savings Plans ยืดหยุ่นกว่า ไม่ล็อค instance type สามารถเปลี่ยน instance family ได้
- เริ่มจาก Compute Savings Plan เพราะคลุม EC2, Fargate, Lambda ทั้งหมด

### 1.3 ใช้ Spot Instances สำหรับ Workload ที่รับ Interruption ได้
- เช่น batch processing, CI/CD runners, dev/staging environments
- ประหยัดได้ 60-90% เมื่อเทียบกับ On-Demand
- ใช้ Spot Fleet หรือ Auto Scaling Group แบบ mixed instances เพื่อลดความเสี่ยง

### 1.4 ปิด Instance ที่ไม่ได้ใช้
- Dev/Staging environments ปิดนอกเวลาทำงานและวันหยุด
- ใช้ AWS Instance Scheduler หรือเขียน Lambda + EventBridge rule ง่ายๆ เพื่อ start/stop ตามเวลา
- ประหยัดได้ ~65% ถ้าเปิดแค่วันจันทร์-ศุกร์ 08:00-20:00

### 1.5 พิจารณาเปลี่ยนเป็น Graviton (ARM) Instances
- เช่น เปลี่ยนจาก m5.large เป็น m7g.large
- ราคาถูกกว่า ~20% และ performance ดีกว่า
- รองรับ Docker, Linux workloads ส่วนใหญ่ได้เลย

---

## 2. RDS Cost Optimization

### 2.1 Right-sizing RDS Instances
- ดู CloudWatch metrics: CPUUtilization, FreeableMemory, DatabaseConnections
- ถ้า CPU < 20% average ลอง downsize เช่น db.r5.xlarge -> db.r5.large
- ทดสอบ performance หลัง downsize ด้วย load test ก่อน apply กับ production

### 2.2 ใช้ Reserved Instances สำหรับ RDS
- RDS Reserved Instances ประหยัดได้ ~30-45% (1-year, no upfront)
- Database มักจะเป็น long-running workload อยู่แล้ว เหมาะกับ RI มาก

### 2.3 เปลี่ยนเป็น Aurora Serverless v2 (ถ้าเหมาะสม)
- ถ้า database มี traffic ไม่สม่ำเสมอ (เช่น กลางคืนเงียบมาก)
- Aurora Serverless v2 จะ scale down ถึง 0.5 ACU (~1 GB RAM) ช่วงไม่มี traffic
- เหมาะกับ dev/staging databases มากเป็นพิเศษ

### 2.4 ลด Storage Costs
- ตรวจสอบว่า allocated storage เยอะเกินไปหรือไม่
- ใช้ Aurora ที่ storage เป็น auto-scaling จ่ายตามใช้จริง
- ลบ manual snapshots เก่าที่ไม่จำเป็น
- ปรับ backup retention period ให้เหมาะสม (ไม่จำเป็นต้อง 35 วันเสมอไป)

### 2.5 ใช้ Read Replica อย่างมีประสิทธิภาพ
- ถ้ามี read replica ที่ไม่ค่อยมี traffic ลองรวมกลับเข้า primary
- หรือใช้ ElastiCache (Redis) แทนสำหรับ caching read-heavy queries

---

## 3. General Strategies

### 3.1 ตรวจสอบ Unused Resources
- Unattached EBS volumes (จ่ายเงินทั้งที่ไม่ได้ mount)
- Elastic IPs ที่ไม่ได้ผูกกับ instance (มีค่าใช้จ่ายตั้งแต่ Feb 2024)
- Old snapshots, unused load balancers
- ใช้ AWS Trusted Advisor หรือ Cost Explorer เพื่อหา

### 3.2 Data Transfer Optimization
- ตรวจสอบค่า data transfer ใน bill ถ้าสูงผิดปกติ อาจมี misconfiguration
- ใช้ VPC endpoints สำหรับ S3/DynamoDB แทน NAT Gateway (ประหยัดทั้ง NAT Gateway cost และ data transfer cost)
- ถ้ามี NAT Gateway ตรวจสอบว่าจำเป็นจริงหรือไม่

### 3.3 ใช้ AWS Cost Anomaly Detection
- เปิดใช้ฟรี จะแจ้งเตือนเมื่อค่าใช้จ่ายผิดปกติ
- ตั้ง budget alerts ใน AWS Budgets เพื่อ monitor รายเดือน

---

## 4. Quick Wins (ทำได้เลย ไม่ต้องเปลี่ยน Architecture)

| Action | Estimated Savings | Effort |
|---|---|---|
| Right-size EC2 instances | 20-40% on EC2 | Low |
| Schedule dev/staging stop/start | ~65% on non-prod EC2 | Low |
| Delete unused EBS volumes & snapshots | Varies | Low |
| Switch to Graviton instances | ~20% on EC2 | Medium |
| Buy 1-year Savings Plans (EC2+RDS) | 30-40% overall | Low |
| Right-size RDS instances | 20-30% on RDS | Medium |
| Remove unused Elastic IPs | Small but easy | Low |

---

## 5. Medium-term Strategies (1-3 เดือน)

| Action | Estimated Savings | Effort |
|---|---|---|
| Migrate to Aurora Serverless v2 (non-prod) | 50-70% on non-prod DB | High |
| Containerize with ECS Fargate Spot | 40-60% on compute | High |
| Implement caching layer (ElastiCache) | Reduce RDS load/size | Medium |
| Use Spot Instances for stateless workloads | 60-90% on eligible EC2 | Medium |

---

## Recommended Action Plan

**สัปดาห์ที่ 1-2: Visibility**
1. เปิด AWS Cost Explorer และ Compute Optimizer
2. วิเคราะห์ bill breakdown ว่า EC2 กี่ %, RDS กี่ %, อื่นๆ กี่ %
3. หา unused resources ด้วย Trusted Advisor

**สัปดาห์ที่ 3-4: Quick Wins**
4. Right-size instances (EC2 + RDS)
5. ตั้ง schedule ปิด dev/staging นอกเวลาทำงาน
6. ลบ unused resources

**เดือนที่ 2: Commit**
7. ซื้อ Savings Plans หรือ Reserved Instances สำหรับ production workloads
8. ทดสอบ Graviton instances

**เป้าหมายที่เป็นไปได้:** ลดจาก 50,000 THB เหลือ 25,000-35,000 THB/เดือน (ประหยัด 30-50%)
