# Test Plan: stock-market Skill v1.0

## Executive Summary

**Product:** stock-market skill - CLI tool for fetching real-time stock and ETF prices  
**Version:** 1.0  
**API:** Yahoo Finance (unofficial)  
**Test Duration:** 2-3 hours  
**Tester:** QA Engineer  

### Testing Objectives

- Verify all 5 CLI tools function correctly (get_price, get_multiple_prices, search_symbol, get_market_summary, get_historical)
- Validate data accuracy from Yahoo Finance API
- Test error handling for invalid inputs and API failures
- Ensure support for US stocks, Thai SET, ETFs, and Crypto
- Verify CLI argument parsing and JSON parameter handling
- Test rate limiting and API reliability

### Key Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Yahoo Finance API changes/blocks | High | Critical | Monitor API, document workarounds |
| Rate limiting (2,000 req/hr) | Medium | Medium | Implement delays, cache responses |
| Thai SET data availability | Medium | High | Test with multiple .BK symbols |
| Network connectivity issues | Low | Medium | Test error messages |

---

## Test Scope

### In Scope

✅ **Functional Testing:**
- All 5 CLI tools (get_price, get_multiple_prices, search_symbol, get_market_summary, get_historical)
- JSON parameter parsing and validation
- CLI argument handling (--help, --list, tool names)
- Error handling and error message clarity

✅ **Market Coverage:**
- US Stocks (NYSE, NASDAQ): AAPL, MSFT, TSLA, JPM
- Thai SET: PTT.BK, AOT.BK, SCB.BK, KBANK.BK
- ETFs: SPY, QQQ, VTI
- Crypto: BTC-USD, ETH-USD
- Market Indices: ^GSPC, ^IXIC, ^SET.BK

✅ **Data Validation:**
- Price data format and accuracy
- Percentage calculations (change, change_percent)
- Currency handling (USD, THB)
- Timestamp formatting (ISO 8601)
- Volume and market cap formatting

✅ **Error Scenarios:**
- Invalid symbols (non-existent tickers)
- Malformed JSON parameters
- Missing required parameters
- API timeout/network errors
- Empty search results
- Rate limit exceeded

### Out of Scope

❌ Load testing beyond Yahoo Finance limits  
❌ Official Yahoo Finance API (using unofficial endpoint)  
❌ Real-time WebSocket data (using polling)  
❌ Authentication/authorization (no API key required)  
❌ Data persistence or caching  
❌ UI/Visual testing (CLI only)

---

## Test Strategy

### Test Types

1. **Functional Testing** - Verify each tool works as specified
2. **Integration Testing** - Test with live Yahoo Finance API
3. **Error Handling** - Validate graceful failure scenarios
4. **Compatibility Testing** - Test across different market types
5. **Regression Testing** - Ensure existing functionality after changes

### Test Approach

- **Black box testing** - Test from user perspective via CLI
- **Positive testing** - Valid inputs produce correct outputs
- **Negative testing** - Invalid inputs handled gracefully
- **Boundary testing** - Edge cases (empty arrays, special characters)
- **Exploratory testing** - Ad-hoc testing for unexpected issues

### Test Environments

- **OS:** macOS, Linux, Windows (via WSL)
- **Runtime:** Bun v1.0+
- **Network:** Stable internet connection required
- **Shell:** bash, zsh, PowerShell

---

## Test Environment Setup

### Prerequisites

```bash
# 1. Install Bun runtime
curl -fsSL https://bun.sh/install | bash

# 2. Navigate to skill directory
cd skills/stock-market

# 3. Install dependencies
bun install

# 4. Verify installation
bun run ./scripts/cli.ts --help
```

### Test Data

**Valid Symbols:**
- US: `AAPL`, `MSFT`, `GOOGL`, `TSLA`, `JPM`, `DIS`
- Thai: `PTT.BK`, `AOT.BK`, `SCB.BK`, `KBANK.BK`, `CPALL.BK`
- ETF: `SPY`, `QQQ`, `VTI`, `VOO`, `ARKK`
- Crypto: `BTC-USD`, `ETH-USD`, `SOL-USD`
- Indices: `^GSPC`, `^IXIC`, `^DJI`

**Invalid Symbols:**
- Non-existent: `INVALID123`, `FAKESTOCK`
- Malformed: `AAPL.BK` (wrong suffix), `PTT` (missing .BK)
- Special chars: `A@PL`, `MS;FT`

---

## Entry Criteria

- [ ] Bun runtime installed (v1.0+)
- [ ] Dependencies installed (bun install completed)
- [ ] Internet connection available
- [ ] Test environment configured
- [ ] Test data prepared

## Exit Criteria

- [ ] All P0 (Critical) test cases executed and passed
- [ ] 90%+ P1 (High) test cases passed
- [ ] All error handling scenarios tested
- [ ] No critical bugs open
- [ ] Test report documented

---

## Test Cases

### P0 - Critical Priority

#### TC-001: Get Price - Valid US Stock
**Priority:** P0 | **Type:** Functional | **Est. Time:** 2 min

**Objective:** Verify get_price returns correct data for US stock

**Preconditions:**
- Skill installed and dependencies ready
- Internet connection available

**Test Steps:**
1. Execute: `bun run ./scripts/cli.ts get_price '{"symbol": "AAPL"}'`
2. **Expected:** JSON response with success=true
3. Verify response contains: symbol, name, price, currency, change, change_percent, market_time, volume
4. Verify symbol is uppercase "AAPL"
5. Verify currency is "USD"
6. Verify price is a positive number
7. Verify timestamp is ISO 8601 format

**Test Data:**
- Input: `{"symbol": "AAPL"}`
- Expected: Apple Inc. price data

**Post-conditions:**
- None

---

#### TC-002: Get Price - Valid Thai SET Stock
**Priority:** P0 | **Type:** Functional | **Est. Time:** 2 min

**Objective:** Verify get_price works with Thai .BK suffix

**Test Steps:**
1. Execute: `bun run ./scripts/cli.ts get_price '{"symbol": "PTT.BK"}'`
2. **Expected:** JSON response with success=true
3. Verify name contains Thai company name (e.g., "ปตท")
4. Verify currency is "THB"
5. Verify all required fields present

**Test Data:**
- Input: `{"symbol": "PTT.BK"}`
- Expected: PTT Public Company data

---

#### TC-003: Get Price - Invalid Symbol
**Priority:** P0 | **Type:** Error Handling | **Est. Time:** 2 min

**Objective:** Verify graceful handling of non-existent symbol

**Test Steps:**
1. Execute: `bun run ./scripts/cli.ts get_price '{"symbol": "INVALID123"}'`
2. **Expected:** JSON response with success=false
3. Verify error message contains "Symbol not found" or similar
4. Verify timestamp is present
5. Verify exit code is non-zero (CLI fails gracefully)

**Test Data:**
- Input: `{"symbol": "INVALID123"}`
- Expected: Error response

---

#### TC-004: Search Symbol - Valid Query
**Priority:** P0 | **Type:** Functional | **Est. Time:** 2 min

**Objective:** Verify search returns relevant results

**Test Steps:**
1. Execute: `bun run ./scripts/cli.ts search_symbol '{"query": "Apple"}'`
2. **Expected:** JSON response with success=true
3. Verify data array contains at least 1 result
4. Verify first result has symbol "AAPL" or contains "Apple"
5. Verify each result has: symbol, name, exchange, type

**Test Data:**
- Input: `{"query": "Apple"}`
- Expected: Array with AAPL and related symbols

---

#### TC-005: CLI Help Display
**Priority:** P0 | **Type:** Functional | **Est. Time:** 1 min

**Objective:** Verify --help shows usage information

**Test Steps:**
1. Execute: `bun run ./scripts/cli.ts --help`
2. **Expected:** Help text displayed
3. Verify all 5 tools are listed
4. Verify usage examples shown
5. Verify exit code is 0

---

#### TC-006: CLI Tool List
**Priority:** P0 | **Type:** Functional | **Est. Time:** 1 min

**Objective:** Verify --list returns available tools

**Test Steps:**
1. Execute: `bun run ./scripts/cli.ts --list`
2. **Expected:** JSON array of tool names
3. Verify array contains: get_price, get_multiple_prices, search_symbol, get_market_summary, get_historical

---

#### TC-007: Get Multiple Prices - Valid Symbols
**Priority:** P0 | **Type:** Functional | **Est. Time:** 3 min

**Objective:** Verify batch price fetching works

**Test Steps:**
1. Execute: `bun run ./scripts/cli.ts get_multiple_prices '{"symbols": ["AAPL", "MSFT", "GOOGL"]}'`
2. **Expected:** JSON response with success=true
3. Verify data array has 3 results
4. Verify each result has symbol and price data
5. Verify AAPL, MSFT, GOOGL all present

**Test Data:**
- Input: `{"symbols": ["AAPL", "MSFT", "GOOGL"]}`

---

### P1 - High Priority

#### TC-008: Get Historical - Default Period
**Priority:** P1 | **Type:** Functional | **Est. Time:** 3 min

**Objective:** Verify historical data fetching

**Test Steps:**
1. Execute: `bun run ./scripts/cli.ts get_historical '{"symbol": "AAPL"}'`
2. **Expected:** JSON response with success=true
3. Verify data array has ~20-30 entries (1 month daily)
4. Verify each entry has: date, open, high, low, close, volume
5. Verify dates are in YYYY-MM-DD format

---

#### TC-009: Get Market Summary
**Priority:** P1 | **Type:** Functional | **Est. Time:** 3 min

**Objective:** Verify market indices summary

**Test Steps:**
1. Execute: `bun run ./scripts/cli.ts get_market_summary`
2. **Expected:** JSON response with success=true
3. Verify data array has 6 indices
4. Verify contains: S&P 500, NASDAQ, Dow Jones, SET Index
5. Verify each has name and price data

---

#### TC-010: ETF Price Fetch
**Priority:** P1 | **Type:** Functional | **Est. Time:** 2 min

**Objective:** Verify ETF symbols work correctly

**Test Steps:**
1. Execute: `bun run ./scripts/cli.ts get_price '{"symbol": "SPY"}'`
2. **Expected:** SPY (S&P 500 ETF) data returned
3. Verify name contains "S&P 500"
4. Test with QQQ, VTI as well

---

#### TC-011: Crypto Price Fetch
**Priority:** P1 | **Type:** Functional | **Est. Time:** 2 min

**Objective:** Verify crypto symbols work

**Test Steps:**
1. Execute: `bun run ./scripts/cli.ts get_price '{"symbol": "BTC-USD"}'`
2. **Expected:** Bitcoin price data returned
3. Verify symbol is "BTC-USD"
4. Test with ETH-USD

---

#### TC-012: Malformed JSON Parameter
**Priority:** P1 | **Type:** Error Handling | **Est. Time:** 1 min

**Objective:** Verify CLI handles invalid JSON

**Test Steps:**
1. Execute: `bun run ./scripts/cli.ts get_price '{invalid json}'`
2. **Expected:** Error message about invalid JSON
3. Verify exit code is non-zero

---

#### TC-013: Missing Required Parameter
**Priority:** P1 | **Type:** Error Handling | **Est. Time:** 1 min

**Objective:** Verify error when symbol is missing

**Test Steps:**
1. Execute: `bun run ./scripts/cli.ts get_price '{}'`
2. **Expected:** Error or undefined behavior handled gracefully
3. Verify meaningful error message

---

#### TC-014: Empty Symbol Array
**Priority:** P1 | **Type:** Error Handling | **Est. Time:** 1 min

**Objective:** Verify get_multiple_prices handles empty array

**Test Steps:**
1. Execute: `bun run ./scripts/cli.ts get_multiple_prices '{"symbols": []}'`
2. **Expected:** Error response
3. Verify error message mentions "non-empty array"

---

#### TC-015: Case Insensitivity
**Priority:** P1 | **Type:** Functional | **Est. Time:** 2 min

**Objective:** Verify symbol case handling

**Test Steps:**
1. Execute: `bun run ./scripts/cli.ts get_price '{"symbol": "aapl"}'`
2. **Expected:** Same result as "AAPL"
3. Verify returned symbol is uppercase

---

### P2 - Medium Priority

#### TC-016: Search - No Results
**Priority:** P2 | **Type:** Error Handling | **Est. Time:** 2 min

**Objective:** Verify search handles no matches

**Test Steps:**
1. Execute: `bun run ./scripts/cli.ts search_symbol '{"query": "xyznonexistent"}'`
2. **Expected:** success=true, empty data array
3. Verify no error, just empty results

---

#### TC-017: Historical - Custom Period
**Priority:** P2 | **Type:** Functional | **Est. Time:** 3 min

**Objective:** Verify custom period parameter

**Test Steps:**
1. Execute: `bun run ./scripts/cli.ts get_historical '{"symbol": "AAPL", "period": "5d"}'`
2. **Expected:** 5 days of data
3. Test with period: 1mo, 3mo, 1y

---

#### TC-018: Historical - Custom Interval
**Priority:** P2 | **Type:** Functional | **Est. Time:** 3 min

**Objective:** Verify custom interval parameter

**Test Steps:**
1. Execute: `bun run ./scripts/cli.ts get_historical '{"symbol": "AAPL", "interval": "1h"}'`
2. **Expected:** Hourly data
3. Verify more entries than daily interval

---

#### TC-019: Thai Stock Without .BK
**Priority:** P2 | **Type:** Error Handling | **Est. Time:** 2 min

**Objective:** Verify behavior without suffix

**Test Steps:**
1. Execute: `bun run ./scripts/cli.ts get_price '{"symbol": "PTT"}'`
2. **Expected:** Error or different stock (not PTT Thai)
3. Document expected behavior

---

#### TC-020: Unknown Tool Name
**Priority:** P2 | **Type:** Error Handling | **Est. Time:** 1 min

**Objective:** Verify error for invalid tool

**Test Steps:**
1. Execute: `bun run ./scripts/cli.ts invalid_tool '{}'``
2. **Expected:** Error message with available tools list
3. Verify exit code non-zero

---

#### TC-021: Special Characters in Symbol
**Priority:** P2 | **Type:** Error Handling | **Est. Time:** 2 min

**Objective:** Test input validation

**Test Steps:**
1. Execute: `bun run ./scripts/cli.ts get_price '{"symbol": "A@PL"}'`
2. **Expected:** Error or sanitized handling
3. Test with: spaces, semicolons, quotes

---

#### TC-022: Market Index Symbols
**Priority:** P2 | **Type:** Functional | **Est. Time:** 2 min

**Objective:** Verify index symbols work

**Test Steps:**
1. Execute: `bun run ./scripts/cli.ts get_price '{"symbol": "^GSPC"}'`
2. **Expected:** S&P 500 index data
3. Test ^IXIC (NASDAQ), ^DJI (Dow Jones)

---

#### TC-023: Data Format Validation
**Priority:** P2 | **Type:** Functional | **Est. Time:** 3 min

**Objective:** Verify data types and formats

**Test Steps:**
1. Get price for AAPL
2. Verify price is number (not string)
3. Verify volume is integer
4. Verify change_percent has 2 decimal places
5. Verify market_cap format (e.g., "2.89T")
6. Verify market_time is ISO 8601

---

### P3 - Low Priority

#### TC-024: Long Symbol Arrays
**Priority:** P3 | **Type:** Performance | **Est. Time:** 5 min

**Objective:** Test performance with many symbols

**Test Steps:**
1. Execute: `bun run ./scripts/cli.ts get_multiple_prices '{"symbols": ["AAPL","MSFT","GOOGL","AMZN","TSLA","META","NVDA","NFLX"]}'`
2. **Expected:** All 8 results returned
3. Measure response time (should be <10s)

---

#### TC-025: Rapid Successive Calls
**Priority:** P3 | **Type:** Performance | **Est. Time:** 5 min

**Objective:** Test rate limit handling

**Test Steps:**
1. Execute 10 get_price calls rapidly
2. **Expected:** All succeed (under rate limit)
3. Monitor for 429 errors

---

#### TC-026: No Arguments
**Priority:** P3 | **Type:** Error Handling | **Est. Time:** 1 min

**Objective:** Verify behavior with no args

**Test Steps:**
1. Execute: `bun run ./scripts/cli.ts`
2. **Expected:** Help text displayed (same as --help)

---

#### TC-027: Unicode Search Query
**Priority:** P3 | **Type:** Functional | **Est. Time:** 2 min

**Objective:** Test non-ASCII search

**Test Steps:**
1. Execute: `bun run ./scripts/cli.ts search_symbol '{"query": "ปตท"}'`
2. **Expected:** Results with PTT.BK
3. Test with other Thai company names

---

## Regression Test Suite

### Smoke Tests (Run First - 10 min)

1. **SM-001:** Get AAPL price
2. **SM-002:** Get PTT.BK price  
3. **SM-003:** Search for "Microsoft"
4. **SM-004:** Get market summary
5. **SM-005:** --help works

### Critical Path (P0 Tests)

Run all P0 test cases (TC-001 through TC-007)

### Full Regression (Release)

Run all P0 + P1 test cases

---

## Test Execution Tracking

### Test Run Template

```markdown
# Test Run: stock-market v1.0

**Date:** 2024-XX-XX  
**Build:** v1.0  
**Tester:** [Name]  
**Environment:** macOS + Bun 1.0+

## Summary
- Total Test Cases: 27
- Executed: 27
- Passed: 25
- Failed: 1
- Blocked: 1
- Pass Rate: 92.6%

## Results by Priority
| Priority | Total | Pass | Fail | Blocked |
|----------|-------|------|------|---------|
| P0       | 7     | 7    | 0    | 0       |
| P1       | 11    | 10   | 1    | 0       |
| P2       | 8     | 7    | 0    | 1       |
| P3       | 1     | 1    | 0    | 0       |

## Critical Issues
- TC-XXX: [Description]
  - Bug: BUG-XXX
  - Status: [Open/Fixed]

## Notes
- [Any observations]
```

---

## Bug Report Template

```markdown
# BUG-XXX: [Title]

**Severity:** Critical/High/Medium/Low  
**Priority:** P0/P1/P2/P3  
**Component:** [Tool name]

## Environment
- OS: [e.g., macOS 14]
- Bun: [e.g., 1.0.0]
- Date: [YYYY-MM-DD]

## Description
[Clear description]

## Steps to Reproduce
1. [Step]
2. [Step]
3. [Step]

## Expected
[What should happen]

## Actual
[What actually happens]

## Evidence
```bash
[Command output]
```

## Impact
- [Who affected]
- [Workaround if any]
```

---

## Sign-Off Criteria

**Ready for Release:**
- [ ] All P0 tests passed
- [ ] 90%+ P1 tests passed  
- [ ] No critical bugs open
- [ ] Documentation updated
- [ ] Performance acceptable (<10s per request)

**Approved By:**
- QA Engineer: _________________ Date: _______
- Product Owner: ______________ Date: _______

---

## Appendix: Quick Command Reference

```bash
# Install
cd skills/stock-market && bun install

# P0 Smoke Tests
bun run ./scripts/cli.ts --help
bun run ./scripts/cli.ts --list
bun run ./scripts/cli.ts get_price '{"symbol": "AAPL"}'
bun run ./scripts/cli.ts get_price '{"symbol": "PTT.BK"}'
bun run ./scripts/cli.ts search_symbol '{"query": "Microsoft"}'
bun run ./scripts/cli.ts get_multiple_prices '{"symbols": ["AAPL","MSFT"]}'
bun run ./scripts/cli.ts get_market_summary

# Error Tests
bun run ./scripts/cli.ts get_price '{"symbol": "INVALID"}'
bun run ./scripts/cli.ts get_price '{invalid json}'
bun run ./scripts/cli.ts unknown_tool

# All Tools
bun run ./scripts/cli.ts get_historical '{"symbol": "AAPL", "period": "5d"}'
```
