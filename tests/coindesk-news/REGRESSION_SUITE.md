# Regression Test Suite: coindesk-news Skill

## Overview
Regression test suite สำหรับ coindesk-news skill เน้นที่ critical paths และ common use cases ที่ต้องทำงานได้เสมอ

**Execution Time:** ~10-15 minutes  
**Frequency:** ก่อน release, หลังแก้ไขโค้ด, หรือเมื่อ API มีปัญหา

---

## Critical Path Tests (P0)

ต้องผ่านทั้งหมดก่อน release ได้รับอนุมัติ

### Suite A: fetch_news.py - Core Functionality

**Test A1: Basic Fetch**
```bash
python skills/coindesk-news/scripts/fetch_news.py --limit 5
```
✅ **Pass Criteria:**
- Exit code 0
- 5 articles displayed
- No error messages

**Test A2: Category Filter**
```bash
python skills/coindesk-news/scripts/fetch_news.py --categories BTC --limit 3
```
✅ **Pass Criteria:**
- Exit code 0
- All articles tagged with BTC
- No unrelated articles

**Test A3: JSON Output**
```bash
python skills/coindesk-news/scripts/fetch_news.py --format json --limit 3 | python -m json.tool > /dev/null && echo "PASS" || echo "FAIL"
```
✅ **Pass Criteria:**
- Valid JSON output
- Can be parsed by json.tool

**Test A4: Markdown Output**
```bash
python skills/coindesk-news/scripts/fetch_news.py --format markdown --limit 3 | grep -q "# CoinDesk Crypto News" && echo "PASS" || echo "FAIL"
```
✅ **Pass Criteria:**
- Contains markdown header
- Properly formatted

---

### Suite B: list_sources.py - Core Functionality

**Test B1: Basic List**
```bash
python skills/coindesk-news/scripts/list_sources.py | head -5
```
✅ **Pass Criteria:**
- Table format displayed
- CoinDesk appears (score 71)
- Multiple sources listed

**Test B2: JSON Format**
```bash
python skills/coindesk-news/scripts/list_sources.py --format json | python -m json.tool > /dev/null && echo "PASS" || echo "FAIL"
```
✅ **Pass Criteria:**
- Valid JSON
- Contains source data

---

### Suite C: list_categories.py - Core Functionality

**Test C1: Basic List**
```bash
python skills/coindesk-news/scripts/list_categories.py | head -5
```
✅ **Pass Criteria:**
- Categories displayed
- Alphabetical sorting
- Common categories present

**Test C2: Filter Function**
```bash
python skills/coindesk-news/scripts/list_categories.py --filter BTC
```
✅ **Pass Criteria:**
- Shows BTC category
- Filter works correctly

---

## Smoke Tests (Quick Verification)

รันเพื่อตรวจสอบว่าระบบทำงานได้ใน 2-3 นาที

```bash
#!/bin/bash
# smoke_test.sh - Run all smoke tests

echo "=== Smoke Test: coindesk-news Skill ==="
echo

FAILED=0

echo "Test 1: fetch_news basic..."
python skills/coindesk-news/scripts/fetch_news.py --limit 3 > /dev/null 2>&1
if [ $? -eq 0 ]; then echo "✅ PASS"; else echo "❌ FAIL"; FAILED=$((FAILED+1)); fi

echo "Test 2: fetch_news categories..."
python skills/coindesk-news/scripts/fetch_news.py --categories BTC --limit 2 > /dev/null 2>&1
if [ $? -eq 0 ]; then echo "✅ PASS"; else echo "❌ FAIL"; FAILED=$((FAILED+1)); fi

echo "Test 3: list_sources..."
python skills/coindesk-news/scripts/list_sources.py > /dev/null 2>&1
if [ $? -eq 0 ]; then echo "✅ PASS"; else echo "❌ FAIL"; FAILED=$((FAILED+1)); fi

echo "Test 4: list_categories..."
python skills/coindesk-news/scripts/list_categories.py > /dev/null 2>&1
if [ $? -eq 0 ]; then echo "✅ PASS"; else echo "❌ FAIL"; FAILED=$((FAILED+1)); fi

echo "Test 5: list_categories filter..."
python skills/coindesk-news/scripts/list_categories.py --filter BTC > /dev/null 2>&1
if [ $? -eq 0 ]; then echo "✅ PASS"; else echo "❌ FAIL"; FAILED=$((FAILED+1)); fi

echo
echo "=== Results ==="
echo "Failed: $FAILED"
exit $FAILED
```

---

## Full Regression Suite

ชุดทดสอบครอบคลุมสำหรับ regression testing

### Phase 1: fetch_news.py (5-7 นาที)

| # | Test Case | Command | Expected |
|---|-----------|---------|----------|
| 1 | Default params | `--limit 10` | 10 articles, summary format |
| 2 | Limit boundary | `--limit 1` | 1 article |
| 3 | Limit max | `--limit 50` | 50 articles (or max available) |
| 4 | Single category | `--categories BTC --limit 5` | BTC articles only |
| 5 | Multi categories | `--categories BTC,ETH --limit 5` | BTC or ETH articles |
| 6 | Invalid category | `--categories XYZ999` | "No articles found" |
| 7 | Positive sentiment | `--sentiment POSITIVE --limit 5` | All [POSITIVE] |
| 8 | Negative sentiment | `--sentiment NEGATIVE --limit 5` | All [NEGATIVE] |
| 9 | Neutral sentiment | `--sentiment NEUTRAL --limit 5` | All [NEUTRAL] |
| 10 | JSON format | `--format json --limit 3` | Valid JSON |
| 11 | Markdown format | `--format markdown --limit 3` | Markdown content |
| 12 | Summary format | `--format summary --limit 3` | Table-like summary |
| 13 | Source filter | `--sources 5 --limit 3` | CoinDesk articles only |
| 14 | Combined filters | `--categories BTC --sentiment NEGATIVE --limit 3` | Filtered results |
| 15 | Empty results | `--categories NONEXISTENT` | "No articles found" |

### Phase 2: list_sources.py (2-3 นาที)

| # | Test Case | Command | Expected |
|---|-----------|---------|----------|
| 1 | Table format | (default) | Formatted table |
| 2 | JSON format | `--format json` | Valid JSON array |
| 3 | Sorting | (default) | Sorted by score descending |
| 4 | Data completeness | `--format json` | All fields present |

### Phase 3: list_categories.py (2-3 นาที)

| # | Test Case | Command | Expected |
|---|-----------|---------|----------|
| 1 | All categories | (default) | All categories listed |
| 2 | Filter BTC | `--filter BTC` | BTC category |
| 3 | Filter ETH | `--filter ETH` | ETH category |
| 4 | Filter SOL | `--filter SOL` | SOL category |
| 5 | Case insensitive | `--filter btc` | BTC category (lowercase) |
| 6 | No matches | `--filter XYZ999` | "No categories found" |
| 7 | JSON format | `--format json` | Valid JSON |
| 8 | Filter + JSON | `--format json --filter BTC` | Filtered JSON |

---

## Automated Test Script

สร้างไฟล์ `run_regression_tests.sh`:

```bash
#!/bin/bash

# Regression Test Suite for coindesk-news Skill
# Usage: ./run_regression_tests.sh

SKILL_DIR="skills/coindesk-news/scripts"
FAILED=0
PASSED=0

echo "=========================================="
echo "Regression Test Suite: coindesk-news"
echo "Date: $(date)"
echo "=========================================="
echo

run_test() {
    local test_name="$1"
    local command="$2"
    local expected="$3"
    
    echo -n "Testing: $test_name... "
    
    result=$(eval "$command" 2>&1)
    exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        if echo "$result" | grep -q "$expected"; then
            echo "✅ PASS"
            PASSED=$((PASSED+1))
        else
            echo "❌ FAIL (output mismatch)"
            FAILED=$((FAILED+1))
        fi
    else
        echo "❌ FAIL (exit code $exit_code)"
        FAILED=$((FAILED+1))
    fi
}

# Test fetch_news.py
run_test "fetch_news default" \
    "python $SKILL_DIR/fetch_news.py --limit 3" \
    "Source:"

run_test "fetch_news BTC filter" \
    "python $SKILL_DIR/fetch_news.py --categories BTC --limit 2" \
    "BTC"

run_test "fetch_news JSON" \
    "python $SKILL_DIR/fetch_news.py --format json --limit 2" \
    '"Data":'

run_test "fetch_news markdown" \
    "python $SKILL_DIR/fetch_news.py --format markdown --limit 2" \
    "# CoinDesk Crypto News"

run_test "fetch_news sentiment" \
    "python $SKILL_DIR/fetch_news.py --sentiment POSITIVE --limit 2" \
    "[POSITIVE]"

# Test list_sources.py
run_test "list_sources table" \
    "python $SKILL_DIR/list_sources.py" \
    "CoinDesk"

run_test "list_sources JSON" \
    "python $SKILL_DIR/list_sources.py --format json" \
    '"NAME":'

# Test list_categories.py
run_test "list_categories table" \
    "python $SKILL_DIR/list_categories.py" \
    "BTC"

run_test "list_categories filter" \
    "python $SKILL_DIR/list_categories.py --filter ETH" \
    "ETH"

run_test "list_categories JSON" \
    "python $SKILL_DIR/list_categories.py --format json" \
    '"NAME":'

# Summary
echo
echo "=========================================="
echo "Test Results"
echo "=========================================="
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo "Total:  $((PASSED+FAILED))"
echo "=========================================="

if [ $FAILED -eq 0 ]; then
    echo "✅ All tests passed!"
    exit 0
else
    echo "❌ Some tests failed!"
    exit 1
fi
```

---

## Test Execution Checklist

ก่อนรัน regression suite:

- [ ] Python 3.8+ ติดตั้งและใช้งานได้
- [ ] Internet connection ใช้งานได้
- [ ] CoinDesk API accessible (ลอง curl ดู)
- [ ] Scripts มี permission execute
- [ ] ไม่มีการแก้ไขโค้ดที่ยังไม่เสร็จ

หลังรัน regression suite:

- [ ] All P0 tests pass
- [ ] 90%+ ของทั้งหมด pass
- [ ] ไม่มี critical bugs
- [ ] Error handling ทำงานถูกต้อง
- [ ] Documentation ตรงกับ implementation

---

## Bug Report Template

หากพบ bug ระหว่าง regression testing:

```markdown
# BUG: [Brief Description]

**Severity:** Critical / High / Medium / Low
**Script:** fetch_news.py / list_sources.py / list_categories.py
**Found During:** Regression Test Suite

## Steps to Reproduce

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Expected Behavior

[What should happen]

## Actual Behavior

[What actually happens]

## Command Executed

```bash
[command that triggers the bug]
```

## Output

```
[actual output]
```

## Environment

- OS: [macOS/Linux/Windows]
- Python: [version]
- Date: [when found]

## Impact

[How this affects users]
```

---

## History

| Date | Version | Tests Run | Pass Rate | Notes |
|------|---------|-----------|-----------|-------|
| 2026-02-01 | 1.0.0 | Initial | ⬜ | First regression suite |

---

**Related Documents:**
- [TEST_PLAN.md](TEST_PLAN.md) - Main test plan
- [TEST_CASES_FETCH_NEWS.md](TEST_CASES_FETCH_NEWS.md) - Detailed fetch_news tests
- [TEST_CASES_LIST_SOURCES.md](TEST_CASES_LIST_SOURCES.md) - Detailed list_sources tests
- [TEST_CASES_LIST_CATEGORIES.md](TEST_CASES_LIST_CATEGORIES.md) - Detailed list_categories tests
