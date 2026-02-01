# Test Cases: list_categories.py

## Overview
Script สำหรับแสดงรายการ news categories ที่ใช้ใน CoinDesk Data API พร้อม filter option

---

## TC-CATEGORIES-001: Basic List - Default Table Format

**Priority:** P0 (Critical)  
**Type:** Functional  
**Estimated Time:** 30 seconds

### Objective
Verify script displays categories in table format by default

### Preconditions
- Python 3.8+ installed
- Internet connection available

### Test Steps

1. Execute command:
   ```bash
   python skills/coindesk-news/scripts/list_categories.py
   ```

**Expected Results:**
- Table format with columns: ID, Name, Status
- Header row with column names
- Separator line
- Many category rows (100+ categories expected)
- Categories sorted alphabetically by name

**Example Output:**
```
ID     Name                           Status    
--------------------------------------------------
1      1INCH                          ACTIVE    
2      AAVE                           ACTIVE    
3      ADA                            ACTIVE    
14     BTC                            ACTIVE    
24     ETH                            ACTIVE    
```

### Verification
- Categories sorted alphabetically
- ID is numeric
- Name is uppercase ticker or topic
- Status shows "ACTIVE"

---

## TC-CATEGORIES-002: JSON Format Output

**Priority:** P1 (High)  
**Type:** Functional

### Test Steps

1. Execute with JSON format:
   ```bash
   python skills/coindesk-news/scripts/list_categories.py --format json
   ```

**Expected Results:**
- Valid JSON array of category objects
- Each category contains:
  - TYPE: "122"
  - ID (integer)
  - NAME (string, uppercase)
  - FILTER (object with INCLUDED_WORDS, INCLUDED_PHRASES)
  - STATUS (string)
  - CREATED_ON (timestamp)
  - UPDATED_ON (timestamp)

**Verification:**
```bash
python skills/coindesk-news/scripts/list_categories.py --format json | python -m json.tool > /dev/null && echo "Valid JSON"
```

---

## TC-CATEGORIES-003: Filter by Name - Single Match

**Priority:** P1 (High)  
**Type:** Functional

### Test Steps

1. Filter for BTC:
   ```bash
   python skills/coindesk-news/scripts/list_categories.py --filter BTC
   ```
   **Expected:** Shows BTC category only

2. Filter for ETH:
   ```bash
   python skills/coindesk-news/scripts/list_categories.py --filter ETH
   ```
   **Expected:** Shows ETH category only

3. Filter for SOL:
   ```bash
   python skills/coindesk-news/scripts/list_categories.py --filter SOL
   ```
   **Expected:** Shows SOL category only

### Verification
- Only matching categories displayed
- Case insensitive (BTC, btc, Btc all work)
- Partial matches work ("BT" matches "BTC")

---

## TC-CATEGORIES-004: Filter by Name - Multiple Matches

**Priority:** P2 (Medium)  
**Type:** Functional

### Test Steps

1. Filter with partial match:
   ```bash
   python skills/coindesk-news/scripts/list_categories.py --filter COIN
   ```
   **Expected:** Shows categories containing "COIN"

2. Filter for MARKET:
   ```bash
   python skills/coindesk-news/scripts/list_categories.py --filter MARKET
   ```
   **Expected:** Shows MARKET and related categories

---

## TC-CATEGORIES-005: Filter with No Matches

**Priority:** P2 (Medium)  
**Type:** Edge Case

### Test Steps

1. Filter with non-existent term:
   ```bash
   python skills/coindesk-news/scripts/list_categories.py --filter XYZ123NONEXISTENT
   ```

**Expected:**
- Message: "No categories found."
- Table headers still shown (or just the message)
- No error

---

## TC-CATEGORIES-006: Filter Case Insensitivity

**Priority:** P2 (Medium)  
**Type:** Functional

### Test Steps

1. Uppercase filter:
   ```bash
   python skills/coindesk-news/scripts/list_categories.py --filter BTC
   ```

2. Lowercase filter:
   ```bash
   python skills/coindesk-news/scripts/list_categories.py --filter btc
   ```

3. Mixed case:
   ```bash
   python skills/coindesk-news/scripts/list_categories.py --filter BtC
   ```

**Expected:**
- All three commands return same result
- Filtering is case-insensitive

---

## TC-CATEGORIES-007: JSON Format with Filter

**Priority:** P1 (High)  
**Type:** Functional

### Test Steps

1. JSON with filter:
   ```bash
   python skills/coindesk-news/scripts/list_categories.py --format json --filter BTC
   ```

**Expected:**
- JSON output
- Only filtered categories in array
- Valid JSON structure

---

## TC-CATEGORIES-008: Category Data Structure

**Priority:** P1 (High)  
**Type:** Functional

### Test Steps

1. Check category data:
   ```bash
   python skills/coindesk-news/scripts/list_categories.py --format json | head -100
   ```

**Verify Category Fields:**
- TYPE: Always "122"
- ID: Unique numeric identifier
- NAME: Category name (e.g., "BTC", "ETH", "MARKET")
- FILTER: Object containing:
  - INCLUDED_WORDS: Array of keywords
  - INCLUDED_PHRASES: Array of phrases (optional)
- STATUS: "ACTIVE" or other
- CREATED_ON: Unix timestamp
- UPDATED_ON: Unix timestamp or null

---

## TC-CATEGORIES-009: Common Cryptocurrency Categories

**Priority:** P2 (Medium)  
**Type:** Functional

### Test Steps

Verify these common categories exist:

```bash
# Check major cryptos
python skills/coindesk-news/scripts/list_categories.py --filter BTC
python skills/coindesk-news/scripts/list_categories.py --filter ETH
python skills/coindesk-news/scripts/list_categories.py --filter SOL
python skills/coindesk-news/scripts/list_categories.py --filter XRP
python skills/coindesk-news/scripts/list_categories.py --filter ADA
python skills/coindesk-news/scripts/list_categories.py --filter DOT
python skills/coindesk-news/scripts/list_categories.py --filter AVAX
```

**Expected:**
- All major cryptocurrencies have categories
- Each returns exactly 1 match

---

## TC-CATEGORIES-010: Topic Categories

**Priority:** P2 (Medium)  
**Type:** Functional

### Test Steps

Check topic-based categories:

```bash
python skills/coindesk-news/scripts/list_categories.py --filter MARKET
python skills/coindesk-news/scripts/list_categories.py --filter DEFI
python skills/coindesk-news/scripts/list_categories.py --filter NFT
python skills/coindesk-news/scripts/list_categories.py --filter REGULATION
python skills/coindesk-news/scripts/list_categories.py --filter BUSINESS
```

**Expected:**
- Topic categories exist
- Can be filtered successfully

---

## TC-CATEGORIES-011: Error Handling - API Failure

**Priority:** P1 (High)  
**Type:** Error Handling

### Test Steps

1. If API is unavailable:
   ```bash
   python skills/coindesk-news/scripts/list_categories.py
   ```

**Expected:**
- Error message: "Error: <description>"
- Graceful exit
- No traceback

---

## TC-CATEGORIES-012: Help Documentation

**Priority:** P2 (Medium)  
**Type:** Documentation

### Test Steps

1. Display help:
   ```bash
   python skills/coindesk-news/scripts/list_categories.py --help
   ```

**Expected:**
- Usage information
- --format option with choices
- --filter option description

---

## TC-CATEGORIES-013: Large Category List

**Priority:** P2 (Medium)  
**Type:** Performance / Functional

### Test Steps

1. List all categories:
   ```bash
   python skills/coindesk-news/scripts/list_categories.py | wc -l
   ```

**Expected:**
- Should handle 100+ categories
- No performance issues
- Output displays quickly (< 5 seconds)

---

## TC-CATEGORIES-014: Category Filter Logic

**Priority:** P2 (Medium)  
**Type:** Functional

### Test Steps

1. Examine FILTER field:
   ```bash
   python skills/coindesk-news/scripts/list_categories.py --format json --filter BTC | python -m json.tool
   ```

**Expected:**
- BTC category has filter with "BTC" in INCLUDED_WORDS
- May have "Bitcoin", "bitcoin" as additional words
- Shows how articles are categorized

---

## Test Execution Log

| Test ID | Status | Notes | Date |
|---------|--------|-------|------|
| TC-CATEGORIES-001 | ⬜ | | |
| TC-CATEGORIES-002 | ⬜ | | |
| TC-CATEGORIES-003 | ⬜ | | |
| TC-CATEGORIES-004 | ⬜ | | |
| TC-CATEGORIES-005 | ⬜ | | |
| TC-CATEGORIES-006 | ⬜ | | |
| TC-CATEGORIES-007 | ⬜ | | |
| TC-CATEGORIES-008 | ⬜ | | |
| TC-CATEGORIES-009 | ⬜ | | |
| TC-CATEGORIES-010 | ⬜ | | |
| TC-CATEGORIES-011 | ⬜ | | |
| TC-CATEGORIES-012 | ⬜ | | |
| TC-CATEGORIES-013 | ⬜ | | |
| TC-CATEGORIES-014 | ⬜ | | |

---

**Next:** [REGRESSION_SUITE.md](REGRESSION_SUITE.md)
