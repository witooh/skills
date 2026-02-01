# Regression Test Suite: fetch_news.py

## Overview

Regression test suite for `fetch_news.py` skill. Organized by execution time and risk coverage:
- **Smoke Tests:** 5 min - Critical path only
- **Full Regression:** 15-20 min - All critical + high priority
- **Quick Sanity:** 2 min - After hotfixes

---

## Setup

Before running any regression suite:

```bash
# Verify prerequisites
python3 --version           # Python 3.9+
pip list | grep massive    # Verify massive package
echo $MASSIVE_API_KEY       # Verify API key is set

# If needed, install dependencies
pip install massive
export MASSIVE_API_KEY="your-api-key"
```

---

## Smoke Test Suite (5 minutes)

**Purpose:** Quick validation that core functionality works  
**Frequency:** Before each release, after hotfixes  
**Pass Rate Required:** 100% (all tests must pass)  
**Stop-on-Failure:** YES (fail fast)

### ST-001: Basic Fetch Default Parameters

```bash
python skills/massive-news/scripts/fetch_news.py AAPL
```

**Pass Criteria:**
- Displays 10 articles (default limit)
- Exit code 0
- No errors in stderr
- Output contains article titles, dates, URLs

---

### ST-002: JSON Output Valid

```bash
python skills/massive-news/scripts/fetch_news.py AAPL --limit 2 --json | python -m json.tool > /dev/null
```

**Pass Criteria:**
- JSON parses without errors
- Exit code 0
- Contains "count" and "results" fields

---

### ST-003: Limit Parameter Works

```bash
python skills/massive-news/scripts/fetch_news.py TSLA --limit 5 | grep -c "^##" | grep -q 5 || echo "Limit test: passed"
```

**Pass Criteria:**
- Returns exactly 5 articles
- Exit code 0

---

### ST-004: Date Range Filter Works

```bash
python skills/massive-news/scripts/fetch_news.py MSFT --from 2024-01-01 --to 2024-01-31 --limit 3
```

**Pass Criteria:**
- Returns articles within date range
- Exit code 0
- No errors

---

### ST-005: Help Text Works

```bash
python skills/massive-news/scripts/fetch_news.py --help | grep -q "Massive API\|ticker\|--limit"
```

**Pass Criteria:**
- Help displays without errors
- Contains relevant documentation
- Exit code 0

---

## Full Regression Suite (15-20 minutes)

**Purpose:** Comprehensive validation of all major features  
**Frequency:** Before release, weekly during development  
**Pass Rate Required:** 90%+ (minor failures acceptable with justification)  
**Stop-on-Failure:** NO (run all tests, report summary)

### Critical Path Tests (P0)

Execute in order. Stop if any fails.

| Test | Command | Expected |
|------|---------|----------|
| **FRG-001** | `python skills/massive-news/scripts/fetch_news.py AAPL` | 10 articles, exit 0 |
| **FRG-002** | `python skills/massive-news/scripts/fetch_news.py AAPL --limit 1` | 1 article, exit 0 |
| **FRG-003** | `python skills/massive-news/scripts/fetch_news.py AAPL --limit 1000` | Up to 1000 articles, exit 0 |
| **FRG-004** | `python skills/massive-news/scripts/fetch_news.py AAPL --limit 5 --json \| python -m json.tool > /dev/null` | Valid JSON, exit 0 |

---

### High Priority Tests (P1)

| Test | Command | Expected |
|------|---------|----------|
| **FRG-005** | `python skills/massive-news/scripts/fetch_news.py aapl --limit 3` | Same as AAPL (case insensitive) |
| **FRG-006** | `python skills/massive-news/scripts/fetch_news.py TSLA --from 2024-01-01 --limit 5` | Articles from 2024-01-01 onward |
| **FRG-007** | `python skills/massive-news/scripts/fetch_news.py GOOGL --from 2024-01-01 --to 2024-01-31 --limit 5` | Articles in Jan 2024 range |
| **FRG-008** | `python skills/massive-news/scripts/fetch_news.py MSFT --order asc --limit 3` | Articles in ascending order |
| **FRG-009** | `python skills/massive-news/scripts/fetch_news.py MSFT --order desc --limit 3` | Articles in descending order |
| **FRG-010** | `python skills/massive-news/scripts/fetch_news.py NVDA --limit 3 --json \| python -c "import json, sys; data=json.load(sys.stdin); assert len(data['results'])==3"` | Exactly 3 results in JSON |

---

### Medium Priority Tests (P2)

| Test | Command | Expected |
|------|---------|----------|
| **FRG-011** | `python skills/massive-news/scripts/fetch_news.py AAPL --limit 0 2>&1` | Error or 0 articles |
| **FRG-012** | `python skills/massive-news/scripts/fetch_news.py AAPL --limit -1 2>&1` | Error or defaults to 1 |
| **FRG-013** | `python skills/massive-news/scripts/fetch_news.py FAKEMN --limit 3 2>&1` | "No articles found" or error |
| **FRG-014** | `python skills/massive-news/scripts/fetch_news.py AAPL --from invalid-date 2>&1` | Error: invalid date format |
| **FRG-015** | `unset MASSIVE_API_KEY; python skills/massive-news/scripts/fetch_news.py AAPL 2>&1; echo $?` | Error message, exit 1 |
| **FRG-016** | `python skills/massive-news/scripts/fetch_news.py AAPL --help \| grep -q "ticker"` | Help contains "ticker" |

---

## Regression Execution Checklist

### Pre-Test (5 min setup)

- [ ] Python 3.9+ verified
- [ ] `massive` package installed
- [ ] `MASSIVE_API_KEY` set and valid
- [ ] Internet connection available
- [ ] Massive API responding (test: `python skills/massive-news/scripts/fetch_news.py AAPL --limit 1`)

### Smoke Tests (5 min)

- [ ] ST-001: Basic fetch passes
- [ ] ST-002: JSON valid
- [ ] ST-003: Limit works
- [ ] ST-004: Date filter works
- [ ] ST-005: Help works

**Go/No-Go Decision:** All smoke tests must pass to proceed

### Full Regression (15-20 min)

**P0 Critical Tests:**
- [ ] FRG-001: Basic fetch
- [ ] FRG-002: Limit=1
- [ ] FRG-003: Limit=1000
- [ ] FRG-004: JSON output

**P1 High Priority Tests:**
- [ ] FRG-005: Case insensitive
- [ ] FRG-006: From date filter
- [ ] FRG-007: Date range
- [ ] FRG-008: Sort asc
- [ ] FRG-009: Sort desc
- [ ] FRG-010: JSON count

**P2 Medium Priority Tests:**
- [ ] FRG-011: Limit=0
- [ ] FRG-012: Limit=-1
- [ ] FRG-013: Unknown ticker
- [ ] FRG-014: Invalid date
- [ ] FRG-015: Missing API key
- [ ] FRG-016: Help text

### Results Summary

| Priority | Total | Passed | Failed | Skip | Status |
|----------|-------|--------|--------|------|--------|
| P0 | 4 | __ | __ | __ | 🔴 |
| P1 | 6 | __ | __ | __ | 🔴 |
| P2 | 6 | __ | __ | __ | 🔴 |
| **TOTAL** | **16** | **__** | **__** | **__** | 🔴 |

---

## Quick Sanity Suite (2 minutes)

For hotfixes and patch releases.

```bash
# Run all 5 smoke tests
echo "=== SMOKE TEST SUITE ===" && \
echo "ST-001: Basic fetch" && \
python skills/massive-news/scripts/fetch_news.py AAPL >/dev/null 2>&1 && echo "✓ PASS" || echo "✗ FAIL" && \

echo "ST-002: JSON format" && \
python skills/massive-news/scripts/fetch_news.py AAPL --limit 2 --json 2>/dev/null | python -m json.tool >/dev/null 2>&1 && echo "✓ PASS" || echo "✗ FAIL" && \

echo "ST-003: Limit parameter" && \
python skills/massive-news/scripts/fetch_news.py TSLA --limit 5 >/dev/null 2>&1 && echo "✓ PASS" || echo "✗ FAIL" && \

echo "ST-004: Date range" && \
python skills/massive-news/scripts/fetch_news.py MSFT --from 2024-01-01 --to 2024-01-31 >/dev/null 2>&1 && echo "✓ PASS" || echo "✗ FAIL" && \

echo "ST-005: Help text" && \
python skills/massive-news/scripts/fetch_news.py --help | grep -q ticker && echo "✓ PASS" || echo "✗ FAIL"
```

---

## Test Execution Script

Save as `run_regression.sh`:

```bash
#!/bin/bash
set -e

echo "=========================================="
echo "Massive News Regression Test Suite"
echo "=========================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."
python3 --version || exit 1
pip list | grep massive || { echo "Installing massive..."; pip install massive; }
[[ -n "$MASSIVE_API_KEY" ]] || { echo "Error: MASSIVE_API_KEY not set"; exit 1; }

SCRIPT="python skills/massive-news/scripts/fetch_news.py"
PASS=0
FAIL=0

# Smoke Tests
echo ""
echo "--- SMOKE TESTS (5 min) ---"

echo -n "ST-001: Basic fetch... "
$SCRIPT AAPL > /dev/null 2>&1 && echo "✓ PASS" && ((PASS++)) || echo "✗ FAIL" && ((FAIL++))

echo -n "ST-002: JSON format... "
$SCRIPT AAPL --limit 2 --json 2>/dev/null | python -m json.tool > /dev/null 2>&1 && echo "✓ PASS" && ((PASS++)) || echo "✗ FAIL" && ((FAIL++))

echo -n "ST-003: Limit parameter... "
$SCRIPT TSLA --limit 5 > /dev/null 2>&1 && echo "✓ PASS" && ((PASS++)) || echo "✗ FAIL" && ((FAIL++))

echo -n "ST-004: Date range... "
$SCRIPT MSFT --from 2024-01-01 --to 2024-01-31 > /dev/null 2>&1 && echo "✓ PASS" && ((PASS++)) || echo "✗ FAIL" && ((FAIL++))

echo -n "ST-005: Help text... "
$SCRIPT --help | grep -q ticker && echo "✓ PASS" && ((PASS++)) || echo "✗ FAIL" && ((FAIL++))

# Summary
echo ""
echo "=========================================="
echo "Results: $PASS Passed, $FAIL Failed"
echo "=========================================="

[[ $FAIL -eq 0 ]] && exit 0 || exit 1
```

Usage:
```bash
chmod +x run_regression.sh
./run_regression.sh
```

---

## Pass/Fail Criteria

### Smoke Test Suite

| Criterion | Requirement |
|-----------|-------------|
| **All Tests Must Pass** | 5/5 (100%) |
| **Exit Code** | 0 for success, 1+ for failure |
| **Blocking** | Yes - release blocked if any fail |

### Full Regression Suite

| Priority | Pass Rate | Blocking |
|----------|-----------|----------|
| **P0 (Critical)** | 100% (4/4) | YES - fail release |
| **P1 (High)** | 90% (≥5/6) | NO - allow with notes |
| **P2 (Medium)** | 80% (≥5/6) | NO - allow with notes |

### Overall Decision

| Scenario | Decision | Action |
|----------|----------|--------|
| Smoke 5/5, Reg P0 4/4, P1 6/6, P2 6/6 | ✅ PASS | Release approved |
| Smoke 5/5, Reg P0 4/4, P1 5/6, P2 5/6 | ⚠️ CONDITIONAL | Release with known issues |
| Smoke 5/5, Reg P0 3/4 | ❌ FAIL | Block release, fix P0 bugs |
| Smoke <5 | ❌ FAIL | Block release, fix immediately |

---

## Defect Severity Matrix

When failures occur, categorize by severity:

| Severity | Examples | Action |
|----------|----------|--------|
| **Critical (P0)** | No articles returned, JSON broken, API key error | Block release, fix immediately |
| **High (P1)** | Date filter not working, limit not respected | Document workaround, fix in patch |
| **Medium (P2)** | Edge case behavior, error messages | Document, fix in minor release |
| **Low** | Cosmetic, formatting | Document, backlog |

---

## Regression Report Template

### Massive News Regression Test Report

**Date:** [Date]  
**Build:** [Version]  
**Tester:** [Name]  
**Environment:** [OS, Python version, massive package version]

#### Test Results Summary

| Suite | Total | Passed | Failed | Pass Rate | Status |
|-------|-------|--------|--------|-----------|--------|
| Smoke | 5 | __ | __ | __% | 🔴 |
| Full Reg (P0) | 4 | __ | __ | __% | 🔴 |
| Full Reg (P1) | 6 | __ | __ | __% | 🔴 |
| Full Reg (P2) | 6 | __ | __ | __% | 🔴 |
| **OVERALL** | **21** | **__** | **__** | **__% ** | 🔴 |

#### Failures

| Test ID | Issue | Severity | Reproduction | Status |
|---------|-------|----------|--------------|--------|
| FRG-NNN | Description | P0/P1/P2 | Steps to reproduce | Open |

#### Sign-Off

- [ ] All P0 tests pass
- [ ] No critical bugs found
- [ ] Ready for release

**QA Sign-Off:** ____________  
**Date:** ____________

---

**Related:** [TEST_PLAN.md](TEST_PLAN.md) | [TEST_CASES_FETCH_NEWS.md](TEST_CASES_FETCH_NEWS.md)
