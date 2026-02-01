# Test Cases: fetch_news.py

## Overview
Script สำหรับดึงข่าว cryptocurrency จาก CoinDesk Data API รองรับ filtering และ multiple output formats

---

## TC-FETCH-001: Basic Fetch - Default Parameters

**Priority:** P0 (Critical)  
**Type:** Functional  
**Estimated Time:** 30 seconds

### Objective
Verify script works with no parameters (default behavior)

### Preconditions
- Python 3.8+ installed
- Internet connection available
- CoinDesk API accessible

### Test Steps

1. Execute command:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py
   ```

**Expected Results:**
- Script executes without errors
- Output displays 10 news articles (default limit)
- Each article shows:
  - Numbered list (1., 2., etc.)
  - Sentiment label in brackets [POSITIVE/NEGATIVE/NEUTRAL]
  - Title
  - Source name
  - Published date (YYYY-MM-DD HH:MM format)
  - Categories
  - URL

### Post-conditions
- Exit code 0
- No error messages in stderr

---

## TC-FETCH-002: Limit Parameter - Valid Values

**Priority:** P0 (Critical)  
**Type:** Functional

### Test Steps

1. Test with limit=1:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --limit 1
   ```
   **Expected:** Displays exactly 1 article

2. Test with limit=5:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --limit 5
   ```
   **Expected:** Displays exactly 5 articles

3. Test with limit=50 (max):
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --limit 50
   ```
   **Expected:** Displays 50 articles (or all available if less)

4. Test with limit=100 (exceeds max):
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --limit 100
   ```
   **Expected:** Displays 50 articles (limit capped at 50)

### Pass Criteria
- Article count matches limit or max available
- No errors or crashes

---

## TC-FETCH-003: Limit Parameter - Boundary Values

**Priority:** P1 (High)  
**Type:** Functional / Edge Case

### Test Steps

1. Test with limit=0:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --limit 0
   ```
   **Expected:** "No articles found." or 0 articles

2. Test with negative value:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --limit -1
   ```
   **Expected:** Error message or defaults to reasonable value

3. Test with non-numeric value:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --limit abc
   ```
   **Expected:** argparse error "invalid int value"

---

## TC-FETCH-004: Categories Filter - Single Category

**Priority:** P0 (Critical)  
**Type:** Functional

### Test Steps

1. Filter by BTC:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --categories BTC --limit 5
   ```
   **Expected:** Articles related to Bitcoin only

2. Filter by ETH:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --categories ETH --limit 5
   ```
   **Expected:** Articles related to Ethereum only

3. Filter by non-existent category:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --categories XYZ123 --limit 5
   ```
   **Expected:** "No articles found." or empty list

### Verification
- Check categories column includes filtered category
- Articles are relevant to the category

---

## TC-FETCH-005: Categories Filter - Multiple Categories

**Priority:** P1 (High)  
**Type:** Functional

### Test Steps

1. Filter by multiple categories:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --categories BTC,ETH --limit 10
   ```
   **Expected:** Articles related to BTC OR ETH

2. Filter by three categories:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --categories BTC,ETH,SOL --limit 10
   ```
   **Expected:** Articles related to any of the specified categories

3. Test with spaces (should handle gracefully):
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --categories "BTC, ETH" --limit 5
   ```
   **Expected:** Should work or handle gracefully

---

## TC-FETCH-006: Sentiment Filter

**Priority:** P1 (High)  
**Type:** Functional

### Test Steps

1. Filter by POSITIVE sentiment:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --sentiment POSITIVE --limit 10
   ```
   **Expected:** All articles show [POSITIVE] sentiment

2. Filter by NEGATIVE sentiment:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --sentiment NEGATIVE --limit 10
   ```
   **Expected:** All articles show [NEGATIVE] sentiment

3. Filter by NEUTRAL sentiment:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --sentiment NEUTRAL --limit 10
   ```
   **Expected:** All articles show [NEUTRAL] sentiment

4. Invalid sentiment value:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --sentiment UNKNOWN
   ```
   **Expected:** argparse error with valid choices

---

## TC-FETCH-007: Output Format - Summary (Default)

**Priority:** P0 (Critical)  
**Type:** UI/Functional

### Test Steps

1. Explicit summary format:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --format summary --limit 3
   ```

**Expected Output Format:**
```
1. [NEGATIVE] Article Title Here
   Source: CoinDesk | 2026-02-01 18:10
   Categories: BTC, MARKET
   URL: https://example.com/article

2. [POSITIVE] Another Article Title
   ...
```

**Verification:**
- Numbered list format
- Sentiment in square brackets
- Source name and timestamp
- Categories as comma-separated
- URL at the end
- Empty line between articles

---

## TC-FETCH-008: Output Format - JSON

**Priority:** P1 (High)  
**Type:** Functional

### Test Steps

1. JSON output:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --format json --limit 2
   ```

**Expected Results:**
- Valid JSON structure
- Contains "Data" array with articles
- Each article has fields: ID, TITLE, BODY, URL, PUBLISHED_ON, SENTIMENT, etc.
- JSON is properly indented
- No syntax errors when parsed

**Verification:**
```bash
python skills/coindesk-news/scripts/fetch_news.py --format json --limit 2 | python -m json.tool > /dev/null && echo "Valid JSON"
```

---

## TC-FETCH-009: Output Format - Markdown

**Priority:** P1 (High)  
**Type:** UI/Functional

### Test Steps

1. Markdown output:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --format markdown --limit 2
   ```

**Expected Output Format:**
```markdown
# CoinDesk Crypto News

## [+] Article Title
**Source:** CoinDesk | **Published:** 2026-02-01 18:10
**Categories:** BTC, MARKET

Article body preview (first 500 chars)...

[Read more](https://example.com/article)

---
```

**Verification:**
- H1 title "# CoinDesk Crypto News"
- H2 headers with sentiment emoji
- Bold formatting for metadata
- Body text truncated at 500 chars with "..."
- Clickable links in markdown format
- Separator lines (---)

---

## TC-FETCH-010: Sources Filter

**Priority:** P2 (Medium)  
**Type:** Functional

### Test Steps

1. Filter by source ID:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --sources 5 --limit 5
   ```
   **Expected:** Articles only from source ID 5 (CoinDesk)

2. Multiple source IDs:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --sources 5,55 --limit 10
   ```
   **Expected:** Articles from sources 5 or 55

3. Invalid source ID:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --sources 99999 --limit 5
   ```
   **Expected:** "No articles found." or empty list

---

## TC-FETCH-011: Language Parameter

**Priority:** P2 (Medium)  
**Type:** Functional

### Test Steps

1. Default language (EN):
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --limit 3
   ```
   **Expected:** English articles

2. Explicit EN:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --lang EN --limit 3
   ```
   **Expected:** Same as default

3. Other language (if supported):
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --lang TH --limit 3
   ```
   **Expected:** Depends on API support

---

## TC-FETCH-012: Combined Parameters

**Priority:** P1 (High)  
**Type:** Functional

### Test Steps

1. Categories + Sentiment:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --categories BTC --sentiment POSITIVE --limit 5
   ```
   **Expected:** BTC articles with POSITIVE sentiment only

2. Categories + Format:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --categories ETH --format markdown --limit 3
   ```
   **Expected:** ETH articles in markdown format

3. Limit + Categories + Sources:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --limit 5 --categories BTC --sources 5
   ```
   **Expected:** 5 BTC articles from CoinDesk source only

4. All parameters:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --limit 10 --categories BTC,ETH --sentiment NEGATIVE --format json --lang EN
   ```
   **Expected:** JSON output of 10 NEGATIVE BTC/ETH articles in English

---

## TC-FETCH-013: Error Handling - Network Timeout

**Priority:** P1 (High)  
**Type:** Error Handling / Integration

### Preconditions
- Network connection available

### Test Steps

1. Test with network timeout (simulated or actual slow connection):
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --limit 5
   ```
   (May need to use tools to simulate slow network)

**Expected:**
- Script handles timeout gracefully
- Error message in stderr
- Exit code non-zero
- No crash or hang

---

## TC-FETCH-014: Error Handling - API Unavailable

**Priority:** P1 (High)  
**Type:** Error Handling / Integration

### Test Steps

1. If API is down or returns error:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py
   ```

**Expected:**
- Error message displayed: "Error: <description>"
- Exit code 1
- Graceful failure (no Python traceback to user)

---

## TC-FETCH-015: Error Handling - Invalid JSON Response

**Priority:** P2 (Medium)  
**Type:** Error Handling

### Test Steps

Note: This may require mocking or happens if API returns non-JSON

**Expected:**
- Error: "JSON parse error: ..."
- Graceful handling
- Exit code 1

---

## TC-FETCH-016: Help Documentation

**Priority:** P2 (Medium)  
**Type:** Documentation

### Test Steps

1. Display help:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --help
   ```

**Expected:**
- Shows usage information
- Lists all available options
- Shows examples
- Properly formatted

---

## TC-FETCH-017: Empty Results Handling

**Priority:** P1 (High)  
**Type:** Functional / Edge Case

### Test Steps

1. Query that returns no results:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --categories NONEXISTENT123
   ```

**Expected:**
- Message: "No articles found."
- Exit code 0 (not an error, just no data)
- No crash

---

## TC-FETCH-018: Unicode/Encoding Support

**Priority:** P2 (Medium)  
**Type:** Functional / Internationalization

### Test Steps

1. Articles with special characters should display correctly:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --limit 20
   ```

**Verification:**
- Unicode characters display correctly
- No encoding errors
- Emojis (if present) render properly
- Non-ASCII characters in titles/body handled

---

## TC-FETCH-019: Timestamp Formatting

**Priority:** P2 (Medium)  
**Type:** Functional

### Test Steps

1. Check timestamp format:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --limit 5
   ```

**Expected Format:**
- Format: YYYY-MM-DD HH:MM
- Example: "2026-02-01 18:10"
- All dates in consistent format
- No "N/A" unless timestamp is missing/invalid

---

## TC-FETCH-020: Article Data Completeness

**Priority:** P1 (High)  
**Type:** Functional

### Test Steps

1. Fetch articles and verify fields:
   ```bash
   python skills/coindesk-news/scripts/fetch_news.py --format json --limit 10
   ```

**Verify Each Article Has:**
- ID (numeric)
- TITLE (string)
- BODY (string, may be long)
- URL (valid URL format)
- PUBLISHED_ON (timestamp)
- AUTHORS (string or null)
- SENTIMENT (POSITIVE/NEGATIVE/NEUTRAL)
- SOURCE_DATA (object with NAME, ID)
- CATEGORY_DATA (array of category objects)

---

## Test Execution Log

| Test ID | Status | Notes | Date |
|---------|--------|-------|------|
| TC-FETCH-001 | ⬜ | | |
| TC-FETCH-002 | ⬜ | | |
| TC-FETCH-003 | ⬜ | | |
| TC-FETCH-004 | ⬜ | | |
| TC-FETCH-005 | ⬜ | | |
| TC-FETCH-006 | ⬜ | | |
| TC-FETCH-007 | ⬜ | | |
| TC-FETCH-008 | ⬜ | | |
| TC-FETCH-009 | ⬜ | | |
| TC-FETCH-010 | ⬜ | | |
| TC-FETCH-011 | ⬜ | | |
| TC-FETCH-012 | ⬜ | | |
| TC-FETCH-013 | ⬜ | | |
| TC-FETCH-014 | ⬜ | | |
| TC-FETCH-015 | ⬜ | | |
| TC-FETCH-016 | ⬜ | | |
| TC-FETCH-017 | ⬜ | | |
| TC-FETCH-018 | ⬜ | | |
| TC-FETCH-019 | ⬜ | | |
| TC-FETCH-020 | ⬜ | | |

---

**Next:** [TEST_CASES_LIST_SOURCES.md](TEST_CASES_LIST_SOURCES.md)
