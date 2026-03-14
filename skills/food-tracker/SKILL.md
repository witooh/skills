---
name: food-tracker
description: >-
  Track daily phosphorus (ฟอสฟอรัส) and potassium (โพแทสเซียม) intake from food
  for kidney disease management. Use this skill whenever the user mentions food
  they ate, wants to log meals, check daily/monthly intake, or asks for nutrient
  reports. Trigger on: "กินข้าว", "กิน...มื้อเช้า/เที่ยง/เย็น", "บันทึกอาหาร",
  "สรุปวันนี้", "สรุปเดือน", "รายงานอาหาร", "ฟอสฟอรัส", "โพแทสเซียม",
  "log food", "food tracker", "what did I eat", any Thai or English food name
  followed by a meal context, or when the user sends a photo/image of food.
  Also trigger when the user asks which foods contributed most to their mineral
  intake.
metadata:
  author: witooh
  version: "1.0"
---

# Food Tracker

ติดตามฟอสฟอรัสและโพแทสเซียมจากอาหาร สำหรับผู้ที่ต้องควบคุมแร่ธาตุ (เช่น ผู้ป่วยโรคไต)

ใช้ Python + SQLite (built-in, ไม่ต้องติดตั้งอะไรเพิ่ม)

## Prerequisites

Initialize the database once before first use:

```bash
python <skill-dir>/scripts/db.py --init
```

The database will be created at `<skill-dir>/data/food_tracker.db`.

## Workflow A: Log Food

When the user mentions food they ate (e.g. "กินข้าวมันไก่ มื้อเที่ยง") or sends a food photo:

### Step 1 - Parse input

**If the user sends an image/photo:**
1. Analyze the image to identify all food items visible in the photo
2. Estimate the serving size of each item from visual cues (plate size, portion)
3. List what you see and confirm with the user before proceeding, e.g.:
   "จากรูปเห็น: ข้าวสวย 1 จาน, แกงเขียวหวานไก่ 1 ชาม, ไข่เจียว 1 ชิ้น — ถูกต้องไหมครับ?"
4. Once confirmed (or corrected), continue to Step 2 with the identified food names

**If the user sends text:**

Extract from the user's message:
- **Food name(s)** — there may be multiple items
- **Meal period** — เช้า / กลางวัน / เย็น / ก่อนนอน
- **Meal time** — if user specifies a time, use it. Otherwise use current time (Asia/Bangkok, UTC+7)
- **Serving size** — if mentioned (e.g. "2 ถ้วย", "1 จาน")

### Step 2 - Look up nutrients

For each food item, use WebSearch:

```
Search: "{food_name} phosphorus potassium mg per serving nutrition facts"
Also try: "{food_name} ฟอสฟอรัส โพแทสเซียม ต่อหน่วย"
```

Extract phosphorus_mg and potassium_mg per serving. Prefer Thai food databases or credible sources (USDA, Thai nutrition databases).

If WebSearch returns no usable data, read `references/nutrients.md` for common Thai food values. If still not found, estimate using AI knowledge and mark `source` as `ai_estimate`.

### Step 3 - Check for duplicates

Before inserting, check if similar food was logged before:

```bash
python <skill-dir>/scripts/db.py --search "food_name"
```

If a match is found with different nutrient values, inform the user but still proceed with the new entry.

### Step 4 - Store the entry

```bash
python <skill-dir>/scripts/db.py --log \
  --food "ข้าวมันไก่" \
  --meal-time "2026-03-05T12:00" \
  --meal-period "กลางวัน" \
  --phosphorus 250 \
  --potassium 300 \
  --serving "1 จาน" \
  --source web
```

### Step 5 - Show running total

```bash
python <skill-dir>/scripts/db.py --report daily
```

### Step 6 - Reply in Thai

Confirm what was logged and show today's running totals using the daily report format below.

## Workflow B: Reports

### Daily Report

```bash
python <skill-dir>/scripts/db.py --report daily --date 2026-03-05
```

Format output as:

```
## รายงานประจำวัน - {date}

| # | อาหาร | มื้อ | ฟอสฟอรัส | โพแทสเซียม | ปริมาณ |
|---|-------|------|----------|-----------|--------|
| 1 | ข้าวสวย | เช้า | 68 mg | 55 mg | 1 ถ้วย |

### สรุปรวม
| แร่ธาตุ | รับไปแล้ว | เกณฑ์/วัน | สถานะ |
|---------|----------|----------|-------|
| ฟอสฟอรัส | 310 mg | 1,000 mg | 31% ✅ |
| โพแทสเซียม | 737 mg | 3,000 mg | 25% ✅ |
```

### Monthly Report

```bash
python <skill-dir>/scripts/db.py --report monthly --month 2026-03
```

Format output as:

```
## รายงานประจำเดือน - {month}

### ภาพรวม
| แร่ธาตุ | รวมทั้งเดือน | เฉลี่ย/วัน | วันที่บันทึก |
|---------|------------|----------|------------|
| ฟอสฟอรัส | 8,432 mg | 843 mg | 10 วัน |
| โพแทสเซียม | 19,540 mg | 1,954 mg | 10 วัน |

### อาหารที่เป็นแหล่งฟอสฟอรัสสูงสุด
| อันดับ | อาหาร | รวม | ทานกี่ครั้ง | เฉลี่ย/ครั้ง |
|-------|-------|-----|----------|------------|
| 1 | นมวัว | 1,220 mg | 5 ครั้ง | 244 mg |

### อาหารที่เป็นแหล่งโพแทสเซียมสูงสุด
(same format)

### วันที่กินเกินเกณฑ์ต่อวัน
| วันที่ | ฟอสฟอรัส | สถานะ | โพแทสเซียม | สถานะ |
|-------|----------|-------|-----------|-------|
| 6 มี.ค. | 1,050 mg | 🔴 เกิน | 2,200 mg | ✅ |

(ถ้าไม่มีวันที่เกินเกณฑ์ แสดง "ไม่มีวันที่เกินเกณฑ์ในเดือนนี้ ✅")

### เมนูที่ควรหลีกเลี่ยง
อาหารที่ค่าต่อครั้งสูงกว่า 20% ของเกณฑ์ต่อวัน (P >200mg หรือ K >600mg):
| อาหาร | ค่าเฉลี่ย/ครั้ง | ทานกี่ครั้ง | รวมทั้งเดือน | ควรเลี่ยงเพราะ |
|-------|---------------|----------|------------|--------------|
| ไก่ทอด Bonchon | P: 300 mg | 3 ครั้ง | 900 mg | ฟอสฟอรัสสูง |
```

The monthly report includes frequency count (ทานกี่ครั้ง) so it answers "สรุปเดือน", "เมนูไหนทำให้ฟอสฟอรัสเยอะ", and "เมนูไหนควรเลี่ยง" questions. The `exceeded_days` and `foods_to_avoid` fields in the JSON output provide this data.

### Status Indicators

- ✅ = < 70% of daily limit
- ⚠️ = 70-90% of daily limit
- 🔴 = > 90% of daily limit

## Script Reference

All commands output JSON to stdout. Errors go to stderr with exit code 1.

| Command | Description |
|---------|-------------|
| `--init` | Initialize/migrate database |
| `--log --food NAME --meal-time DT --phosphorus N --potassium N [--serving S] [--meal-period P] [--source web\|ai_estimate]` | Insert food log |
| `--search QUERY` | Find similar food names (FTS5 + LIKE) |
| `--report daily [--date YYYY-MM-DD]` | Daily summary (default: today) |
| `--report monthly [--month YYYY-MM]` | Monthly summary (default: this month) |
| `--list [--date YYYY-MM-DD]` | List raw entries for a date |
| `--delete ID` | Delete entry by ID |

## Nutrient Thresholds (CKD Reference)

| Mineral | Daily Limit |
|---------|------------|
| Phosphorus (ฟอสฟอรัส) | 800-1,000 mg |
| Potassium (โพแทสเซียม) | 2,000-3,000 mg |

These are general reference values. Always defer to the user's doctor.

## Important Notes

- All timestamps displayed as Asia/Bangkok (UTC+7)
- Nutrient values from web search are preferred over AI estimates
- When searching for duplicates, check both exact and similar names because Thai food names can vary (e.g. "ข้าวผัดกะเพรา" vs "ข้าวกะเพรา")
- This skill does NOT provide medical advice — data is for personal tracking only
- Always add the disclaimer in reports: "ข้อมูลนี้เป็นเพียงการติดตามส่วนตัว ไม่ใช่คำแนะนำทางการแพทย์"
