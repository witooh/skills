# Test Cases: list_sources.py

## Overview
Script สำหรับแสดงรายการ news sources ที่ใช้ใน CoinDesk Data API

---

## TC-SOURCES-001: Basic List - Default Table Format

**Priority:** P0 (Critical)  
**Type:** Functional  
**Estimated Time:** 30 seconds

### Objective
Verify script displays sources in table format by default

### Preconditions
- Python 3.8+ installed
- Internet connection available

### Test Steps

1. Execute command:
   ```bash
   python skills/coindesk-news/scripts/list_sources.py
   ```

**Expected Results:**
- Table format with columns: ID, Name, Score, Status
- Header row with column names
- Separator line
- Multiple source rows (should have many sources)
- Sources sorted by BENCHMARK_SCORE (highest first)

**Example Output:**
```
ID     Name                      Score  Status    
--------------------------------------------------
5      CoinDesk                  71     ACTIVE    
55     Blockworks                59     ACTIVE    
44     Decrypt                   57     ACTIVE    
```

### Verification
- Column headers aligned
- Data properly formatted in columns
- Score column shows numeric values
- Status shows "ACTIVE" or other status

---

## TC-SOURCES-002: JSON Format Output

**Priority:** P1 (High)  
**Type:** Functional

### Test Steps

1. Execute with JSON format:
   ```bash
   python skills/coindesk-news/scripts/list_sources.py --format json
   ```

**Expected Results:**
- Valid JSON array of source objects
- Each source contains:
  - ID (integer)
  - NAME (string)
  - SOURCE_KEY (string)
  - IMAGE_URL (string)
  - URL (string)
  - LANG (string)
  - SOURCE_TYPE (string)
  - BENCHMARK_SCORE (integer)
  - STATUS (string)
  - Additional metadata fields

**Verification:**
```bash
python skills/coindesk-news/scripts/list_sources.py --format json | python -m json.tool > /dev/null && echo "Valid JSON"
```

---

## TC-SOURCES-003: Sorting Order

**Priority:** P2 (Medium)  
**Type:** Functional

### Test Steps

1. Execute and check sorting:
   ```bash
   python skills/coindesk-news/scripts/list_sources.py
   ```

**Expected:**
- Sources sorted by BENCHMARK_SCORE descending (highest to lowest)
- CoinDesk (score 71) should be first
- Sources with score 0 should be at the end

---

## TC-SOURCES-004: Source Data Completeness

**Priority:** P1 (High)  
**Type:** Functional

### Test Steps

1. Check JSON output for required fields:
   ```bash
   python skills/coindesk-news/scripts/list_sources.py --format json | head -50
   ```

**Verify Each Source Has:**
- TYPE: "120"
- ID: Numeric identifier
- SOURCE_KEY: Short identifier (e.g., "coindesk", "blockworks")
- NAME: Display name
- IMAGE_URL: URL to source logo
- URL: Website URL
- LANG: Language code
- SOURCE_TYPE: "RSS" or other
- BENCHMARK_SCORE: Quality score
- STATUS: "ACTIVE" or other

---

## TC-SOURCES-005: Empty Results Handling

**Priority:** P2 (Medium)  
**Type:** Edge Case

### Test Steps

Note: This requires API to return empty data or mocking

**Expected:**
- Message: "No sources found."
- No crash or error
- Graceful handling

---

## TC-SOURCES-006: Error Handling - API Failure

**Priority:** P1 (High)  
**Type:** Error Handling

### Test Steps

1. If API is unavailable, execute:
   ```bash
   python skills/coindesk-news/scripts/list_sources.py
   ```

**Expected:**
- Error message displayed: "Error: <description>"
- Script exits gracefully
- No Python traceback shown to user

---

## TC-SOURCES-007: Error Handling - Network Timeout

**Priority:** P1 (High)  
**Type:** Error Handling

### Test Steps

**Expected:**
- Timeout after 30 seconds (as defined in code)
- Error message displayed
- Graceful exit
- No hanging

---

## TC-SOURCES-008: Help Documentation

**Priority:** P2 (Medium)  
**Type:** Documentation

### Test Steps

1. Display help:
   ```bash
   python skills/coindesk-news/scripts/list_sources.py --help
   ```

**Expected:**
- Shows usage information
- Lists --format option with choices
- Description of script purpose

---

## TC-SOURCES-009: Unicode/Source Names

**Priority:** P2 (Medium)  
**Type:** Functional / Internationalization

### Test Steps

1. Execute and check source names:
   ```bash
   python skills/coindesk-news/scripts/list_sources.py
   ```

**Verification:**
- Source names display correctly
- Special characters handled properly
- Long names truncated appropriately (24 chars max for table)

---

## TC-SOURCES-010: Score Range Validation

**Priority:** P2 (Medium)  
**Type:** Functional

### Test Steps

1. Execute and analyze scores:
   ```bash
   python skills/coindesk-news/scripts/list_sources.py --format json
   ```

**Expected:**
- Scores are numeric values
- Range appears to be 0-100
- Highest score sources are well-known (CoinDesk, etc.)
- Score 0 sources still show as ACTIVE

---

## Test Execution Log

| Test ID | Status | Notes | Date |
|---------|--------|-------|------|
| TC-SOURCES-001 | ⬜ | | |
| TC-SOURCES-002 | ⬜ | | |
| TC-SOURCES-003 | ⬜ | | |
| TC-SOURCES-004 | ⬜ | | |
| TC-SOURCES-005 | ⬜ | | |
| TC-SOURCES-006 | ⬜ | | |
| TC-SOURCES-007 | ⬜ | | |
| TC-SOURCES-008 | ⬜ | | |
| TC-SOURCES-009 | ⬜ | | |
| TC-SOURCES-010 | ⬜ | | |

---

**Next:** [TEST_CASES_LIST_CATEGORIES.md](TEST_CASES_LIST_CATEGORIES.md)
