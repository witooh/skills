# Test Cases: fetch_news.py

## Overview
Script สำหรับดึงข่าว stock/ETF จาก Massive API โดยใช้ official Python client รองรับ date filtering, sentiment analysis, และ multiple output formats

---

## TC-MN-001: Basic Fetch - Valid Ticker (AAPL)

**Priority:** P0 (Critical)  
**Type:** Functional  
**Estimated Time:** 30 seconds

### Objective
Verify script works with valid ticker symbol using default parameters

### Preconditions
- Python 3.9+ installed
- `massive` package installed (`pip install massive`)
- `MASSIVE_API_KEY` environment variable set
- Internet connection available
- Massive API accessible

### Test Steps

1. Execute command with valid ticker:
   ```bash
   python skills/massive-news/scripts/fetch_news.py AAPL
   ```

**Expected Results:**
- Script executes without errors
- Output displays 10 news articles (default limit)
- Each article shows:
  - H2 heading with title and sentiment (if available)
  - Author and publication timestamp
  - Ticker symbols
  - Description text
  - Read more link
  - Separator (---)
- Exit code 0
- No error messages in stderr

### Post-conditions
- Script completes successfully
- Output is human-readable markdown format

---

## TC-MN-002: Limit Parameter Validation (1, 10, 1000)

**Priority:** P0 (Critical)  
**Type:** Functional / Parameter Validation

### Objective
Verify limit parameter correctly restricts article count

### Test Steps

1. Test with limit=1:
   ```bash
   python skills/massive-news/scripts/fetch_news.py AAPL --limit 1
   ```
   **Expected:** Displays exactly 1 article

2. Test with limit=10 (default):
   ```bash
   python skills/massive-news/scripts/fetch_news.py AAPL --limit 10
   ```
   **Expected:** Displays 10 articles (or fewer if unavailable)

3. Test with limit=1000 (max):
   ```bash
   python skills/massive-news/scripts/fetch_news.py AAPL --limit 1000
   ```
   **Expected:** Displays up to 1000 articles (or all available if less)

4. Test with short flag -n:
   ```bash
   python skills/massive-news/scripts/fetch_news.py TSLA -n 5
   ```
   **Expected:** Displays exactly 5 articles

### Pass Criteria
- Article count matches requested limit (or available if fewer)
- No errors or crashes
- Script handles all boundary values within 1-1000 range

---

## TC-MN-003: JSON Output Format

**Priority:** P0 (Critical)  
**Type:** Functional / Output Format

### Objective
Verify JSON output format is valid and complete

### Test Steps

1. JSON output with small limit:
   ```bash
   python skills/massive-news/scripts/fetch_news.py AAPL --limit 2 --json
   ```

**Expected Results:**
- Valid JSON structure with proper formatting
- Top-level object contains:
  - `count`: number of articles returned
  - `results`: array of article objects
- Each article object contains:
  - `id`: unique identifier
  - `title`: string
  - `author`: string or null
  - `published_utc`: ISO timestamp
  - `description`: string
  - `article_url`: valid URL
  - `image_url`: URL or null
  - `amp_url`: URL or null
  - `tickers`: array of ticker symbols
  - `keywords`: array of strings or null
  - `publisher`: object with name, homepage_url, logo_url
  - `insights`: array of objects with ticker, sentiment, sentiment_reasoning

**Verification:**
```bash
python skills/massive-news/scripts/fetch_news.py AAPL --limit 2 --json | python -m json.tool > /dev/null && echo "Valid JSON"
```

### Pass Criteria
- JSON parses without errors
- All required fields present
- No trailing commas or syntax errors

---

## TC-MN-004: Date Range Filtering (--from, --to)

**Priority:** P1 (High)  
**Type:** Functional / Parameter Validation

### Objective
Verify date range filtering returns articles within specified date range

### Test Steps

1. Fetch from specific date:
   ```bash
   python skills/massive-news/scripts/fetch_news.py AAPL --from 2024-01-01 --limit 5
   ```
   **Expected:** All articles published on or after 2024-01-01

2. Fetch within date range:
   ```bash
   python skills/massive-news/scripts/fetch_news.py TSLA --from 2024-01-01 --to 2024-01-31 --limit 10
   ```
   **Expected:** All articles between 2024-01-01 and 2024-01-31 (inclusive)

3. Recent articles only:
   ```bash
   python skills/massive-news/scripts/fetch_news.py GOOGL --from 2025-01-01 --limit 5
   ```
   **Expected:** Only recent articles from January 2025 onward

### Verification
- Check `published_utc` field for each article
- All dates >= from_date and <= to_date
- Format preserved as YYYY-MM-DD HH:MM:SS or ISO 8601

### Pass Criteria
- Date filtering works correctly
- Articles within specified range only
- No articles outside date range

---

## TC-MN-005: Sort Order (--order asc/desc)

**Priority:** P1 (High)  
**Type:** Functional / Parameter Validation

### Objective
Verify sort order parameter controls article chronology

### Test Steps

1. Descending order (newest first):
   ```bash
   python skills/massive-news/scripts/fetch_news.py AAPL --order desc --limit 3 --json
   ```
   **Expected:** Articles sorted newest to oldest

2. Ascending order (oldest first):
   ```bash
   python skills/massive-news/scripts/fetch_news.py AAPL --order asc --limit 3 --json
   ```
   **Expected:** Articles sorted oldest to newest

### Verification
```bash
# Extract timestamps and verify order
python skills/massive-news/scripts/fetch_news.py AAPL --order desc --limit 5 --json | \
  python -c "import json, sys; data = json.load(sys.stdin); \
  dates = [a['published_utc'] for a in data['results']]; \
  print('Descending' if dates == sorted(dates, reverse=True) else 'Wrong order')"
```

### Pass Criteria
- desc order: timestamps in descending order (newest first)
- asc order: timestamps in ascending order (oldest first)

---

## TC-MN-006: Ticker Case Insensitivity (aapl vs AAPL)

**Priority:** P1 (High)  
**Type:** Functional / Parameter Validation

### Objective
Verify script handles ticker symbols in any case (uppercase/lowercase)

### Test Steps

1. Lowercase ticker:
   ```bash
   python skills/massive-news/scripts/fetch_news.py aapl --limit 5
   ```
   **Expected:** Returns AAPL news (converted to uppercase internally)

2. Uppercase ticker:
   ```bash
   python skills/massive-news/scripts/fetch_news.py AAPL --limit 5
   ```
   **Expected:** Same results as lowercase

3. Mixed case ticker:
   ```bash
   python skills/massive-news/scripts/fetch_news.py AaPl --limit 5
   ```
   **Expected:** Same results as other cases

### Verification
- All three commands return identical results
- Output header shows ticker in uppercase
- No "ticker not found" errors

### Pass Criteria
- Case-insensitive ticker handling works
- Output consistent regardless of input case

---

## TC-MN-007: Combined Parameters

**Priority:** P1 (High)  
**Type:** Functional / Integration

### Objective
Verify script works correctly with multiple parameters combined

### Test Steps

1. Limit + date range:
   ```bash
   python skills/massive-news/scripts/fetch_news.py TSLA --limit 10 --from 2024-01-01 --to 2024-01-31
   ```
   **Expected:** Max 10 articles from January 2024

2. Date range + sort order:
   ```bash
   python skills/massive-news/scripts/fetch_news.py GOOGL --from 2024-06-01 --to 2024-06-30 --order asc --limit 5
   ```
   **Expected:** 5 articles from June 2024, oldest first

3. All parameters + JSON:
   ```bash
   python skills/massive-news/scripts/fetch_news.py MSFT --limit 20 --from 2024-01-01 --to 2024-12-31 --order desc --json
   ```
   **Expected:** Valid JSON with up to 20 articles from 2024, newest first

### Pass Criteria
- All parameters work together correctly
- Results filtered and sorted as expected
- Output format respected

---

## TC-MN-008: Invalid Date Format

**Priority:** P2 (Medium)  
**Type:** Error Handling / Parameter Validation

### Objective
Verify script rejects invalid date formats with clear error message

### Test Steps

1. Invalid format (MM-DD-YYYY):
   ```bash
   python skills/massive-news/scripts/fetch_news.py AAPL --from 01-01-2024
   ```
   **Expected:** Error message mentioning YYYY-MM-DD format

2. Invalid format (no dashes):
   ```bash
   python skills/massive-news/scripts/fetch_news.py AAPL --from 20240101
   ```
   **Expected:** Error message with correct format

3. Invalid date values:
   ```bash
   python skills/massive-news/scripts/fetch_news.py AAPL --from 2024-13-01
   ```
   **Expected:** Error message (month 13 invalid)

4. Invalid day:
   ```bash
   python skills/massive-news/scripts/fetch_news.py AAPL --from 2024-02-30
   ```
   **Expected:** Error message (Feb 30 invalid)

### Pass Criteria
- Proper error messages displayed
- Exit code 1 (error)
- Clear instruction on correct format
- No script crash or traceback

---

## TC-MN-009: Limit Boundary Values (0, -1, 1001)

**Priority:** P2 (Medium)  
**Type:** Error Handling / Edge Case

### Objective
Verify script handles limit boundary values correctly

### Test Steps

1. Zero limit:
   ```bash
   python skills/massive-news/scripts/fetch_news.py AAPL --limit 0
   ```
   **Expected:** Either error or "No articles found" with exit code 0

2. Negative limit:
   ```bash
   python skills/massive-news/scripts/fetch_news.py AAPL --limit -1
   ```
   **Expected:** Clamped to 1 or error message

3. Over max (1001):
   ```bash
   python skills/massive-news/scripts/fetch_news.py AAPL --limit 1001
   ```
   **Expected:** Clamped to 1000 (internal max)

4. Non-numeric limit:
   ```bash
   python skills/massive-news/scripts/fetch_news.py AAPL --limit abc
   ```
   **Expected:** argparse error "invalid int value"

### Pass Criteria
- Boundary values handled gracefully
- No unexpected crashes
- Clear error messages for non-numeric values

---

## TC-MN-010: Unknown Ticker Symbol

**Priority:** P2 (Medium)  
**Type:** Error Handling / Edge Case

### Objective
Verify script handles invalid/unknown ticker symbols

### Test Steps

1. Non-existent ticker:
   ```bash
   python skills/massive-news/scripts/fetch_news.py FAKEMN --limit 5
   ```
   **Expected:** Error or "No articles found"

2. Invalid format ticker:
   ```bash
   python skills/massive-news/scripts/fetch_news.py 12345 --limit 5
   ```
   **Expected:** Error or "No articles found"

3. Very long ticker string:
   ```bash
   python skills/massive-news/scripts/fetch_news.py AAAAAAAAAAAAAAAAAAAAA --limit 5
   ```
   **Expected:** Error or "No articles found"

### Pass Criteria
- No script crash
- Clear message if ticker not found
- Exit code 0 (not an error state)

---

## TC-MN-011: Missing API Key Error

**Priority:** P2 (Medium)  
**Type:** Error Handling / Integration

### Objective
Verify script handles missing MASSIVE_API_KEY environment variable

### Test Steps

1. Unset API key and run script:
   ```bash
   unset MASSIVE_API_KEY
   python skills/massive-news/scripts/fetch_news.py AAPL --limit 1
   ```
   **Expected:** Error message mentioning missing API key

2. Restore API key:
   ```bash
   export MASSIVE_API_KEY="your-key"
   python skills/massive-news/scripts/fetch_news.py AAPL --limit 1
   ```
   **Expected:** Script works normally

### Pass Criteria
- Clear error message when API key missing
- Exit code 1
- No Python traceback displayed to user
- Helpful message suggesting to set environment variable

---

## TC-MN-012: Network Error Handling

**Priority:** P2 (Medium)  
**Type:** Error Handling / Integration

### Objective
Verify script handles network errors gracefully

### Test Steps

1. Simulate network unavailability (if possible):
   - Disconnect internet or use network throttling tool
   ```bash
   python skills/massive-news/scripts/fetch_news.py AAPL --limit 5
   ```
   **Expected:** Error message mentioning network issue

2. With internet restored:
   ```bash
   python skills/massive-news/scripts/fetch_news.py AAPL --limit 5
   ```
   **Expected:** Script works normally

### Pass Criteria
- Graceful error handling for network issues
- Exit code 1 on network error
- No raw exception tracebacks
- Helpful error message

---

## TC-MN-013: Help Documentation

**Priority:** P2 (Medium)  
**Type:** Documentation / Usability

### Objective
Verify help text and usage information is complete and accurate

### Test Steps

1. Display help:
   ```bash
   python skills/massive-news/scripts/fetch_news.py --help
   ```

**Expected Output Contains:**
- Description of script purpose
- List of all available arguments:
  - `ticker` (required, positional)
  - `--limit` / `-n` (optional, default 10)
  - `--from` (optional, date format)
  - `--to` (optional, date format)
  - `--order` (optional, choices: asc/desc)
  - `--json` (optional flag)
- Examples of usage
- Proper formatting

### Pass Criteria
- Help text accurate and complete
- Exit code 0
- All parameters documented with defaults

---

## TC-MN-014: Empty Results Handling

**Priority:** P1 (High)  
**Type:** Edge Case / Functional

### Objective
Verify script handles queries with no results gracefully

### Test Steps

1. Date range with no articles:
   ```bash
   python skills/massive-news/scripts/fetch_news.py AAPL --from 2000-01-01 --to 2000-01-02
   ```
   **Expected:** "No articles found" or empty list

2. Future date range (likely no results):
   ```bash
   python skills/massive-news/scripts/fetch_news.py AAPL --from 2030-01-01 --to 2030-01-31
   ```
   **Expected:** "No articles found" or empty list

### Verification
- Message clearly states no results
- Exit code 0 (not an error)
- No crash or unexpected behavior

### Pass Criteria
- Graceful empty result handling
- Clear user feedback
- JSON output shows count: 0

---

## TC-MN-015: Unicode/Special Character Support

**Priority:** P2 (Medium)  
**Type:** Internationalization / Functional

### Objective
Verify script handles articles with unicode and special characters

### Test Steps

1. Fetch articles that may contain unicode:
   ```bash
   python skills/massive-news/scripts/fetch_news.py AAPL --limit 20
   ```

**Verification:**
- Unicode characters display correctly
- No encoding errors in output
- Emojis (if present) render properly
- Special characters in URLs preserved
- Non-ASCII characters in titles/descriptions handled

### Pass Criteria
- No encoding errors
- Unicode content displays properly
- No mojibake (garbled text)

---

## TC-MN-016: Timestamp Formatting

**Priority:** P2 (Medium)  
**Type:** Functional / Data Integrity

### Objective
Verify published timestamps are formatted consistently

### Test Steps

1. Check timestamp format in markdown output:
   ```bash
   python skills/massive-news/scripts/fetch_news.py AAPL --limit 5
   ```

**Expected Format:**
- Should include date and time
- Consistent across all articles
- Readable format (e.g., 2024-01-15 14:30:00)

2. Check JSON timestamp format:
   ```bash
   python skills/massive-news/scripts/fetch_news.py AAPL --limit 3 --json
   ```

**Expected:**
- ISO 8601 format or consistent datetime string
- All articles have valid timestamps

### Pass Criteria
- Timestamps formatted consistently
- No "N/A" unless genuinely missing
- Timestamps are parseable

---

## TC-MN-017: Article Data Completeness

**Priority:** P1 (High)  
**Type:** Data Integrity / Functional

### Objective
Verify JSON output contains all expected article fields

### Test Steps

1. Fetch and verify article structure:
   ```bash
   python skills/massive-news/scripts/fetch_news.py AAPL --limit 10 --json
   ```

**Verify Each Article Has:**
- `id`: numeric or string identifier
- `title`: non-empty string
- `author`: string (may be null)
- `published_utc`: timestamp
- `description`: string (may be null)
- `article_url`: valid URL format
- `image_url`: URL or null
- `amp_url`: URL or null
- `tickers`: array of strings
- `keywords`: array of strings or null
- `publisher`: object with name, homepage_url, logo_url
- `insights`: array of sentiment objects (if available)

### Pass Criteria
- All expected fields present
- Data types correct
- No missing critical fields

---

## TC-MN-018: Stdout vs Stderr

**Priority:** P2 (Medium)  
**Type:** Functional / Integration

### Objective
Verify output goes to correct stream

### Test Steps

1. Capture stdout and stderr separately:
   ```bash
   python skills/massive-news/scripts/fetch_news.py AAPL --limit 2 2>stderr.txt 1>stdout.txt
   ```

**Expected:**
- Article data in stdout (stdout.txt)
- No errors in stderr (stderr.txt should be empty)
- Exit code 0

2. Test error case:
   ```bash
   python skills/massive-news/scripts/fetch_news.py --invalid-arg 2>stderr.txt 1>stdout.txt; echo $?
   ```

**Expected:**
- Error message in stderr
- stdout empty
- Exit code 2 (argparse error)

### Pass Criteria
- Normal output on stdout
- Errors on stderr only
- Exit codes correct (0 for success, 1-2 for errors)

---

## TC-MN-019: Performance - Large Limit

**Priority:** P2 (Medium)  
**Type:** Performance / Functional

### Objective
Verify script handles large result sets efficiently

### Test Steps

1. Request maximum articles:
   ```bash
   time python skills/massive-news/scripts/fetch_news.py AAPL --limit 1000 --json > /dev/null
   ```

**Expected:**
- Completes within reasonable time (< 30 seconds)
- Valid JSON output
- No memory errors
- Exit code 0

### Pass Criteria
- Handles large result sets
- Completes in acceptable time
- No out-of-memory errors

---

## TC-MN-020: Ticket Symbols with Hyphens/Dots

**Priority:** P2 (Medium)  
**Type:** Parameter Validation / Edge Case

### Objective
Verify script handles special characters in ticker symbols

### Test Steps

1. ETF with dot (e.g., BRK.B):
   ```bash
   python skills/massive-news/scripts/fetch_news.py BRK.B --limit 5
   ```
   **Expected:** Returns news for Berkshire Hathaway B shares

2. Ticker variations:
   ```bash
   python skills/massive-news/scripts/fetch_news.py BF.A --limit 5
   ```
   **Expected:** Returns relevant news

### Pass Criteria
- Special characters in ticker handled correctly
- Correct results returned
- No parsing errors

---

## Test Execution Log

| Test ID | Status | Notes | Date |
|---------|--------|-------|------|
| TC-MN-001 | ⬜ | | |
| TC-MN-002 | ⬜ | | |
| TC-MN-003 | ⬜ | | |
| TC-MN-004 | ⬜ | | |
| TC-MN-005 | ⬜ | | |
| TC-MN-006 | ⬜ | | |
| TC-MN-007 | ⬜ | | |
| TC-MN-008 | ⬜ | | |
| TC-MN-009 | ⬜ | | |
| TC-MN-010 | ⬜ | | |
| TC-MN-011 | ⬜ | | |
| TC-MN-012 | ⬜ | | |
| TC-MN-013 | ⬜ | | |
| TC-MN-014 | ⬜ | | |
| TC-MN-015 | ⬜ | | |
| TC-MN-016 | ⬜ | | |
| TC-MN-017 | ⬜ | | |
| TC-MN-018 | ⬜ | | |
| TC-MN-019 | ⬜ | | |
| TC-MN-020 | ⬜ | | |

---

**Next:** [REGRESSION_SUITE.md](REGRESSION_SUITE.md)
