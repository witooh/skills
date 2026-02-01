# Test Plan: Massive News Skill

## Executive Summary

**Product:** massive-news Skill  
**Version:** 1.0.0  
**Test Date:** 2026-02-01  
**Tester:** QA Team  

Massive News Skill เป็น Python-based CLI tool สำหรับดึงข่าว stock/ETF จาก Massive API โดยใช้ official Python client (`massive` package) ประกอบด้วย 1 script:
- `fetch_news.py` - ดึงข่าว stock/ETF พร้อม date filtering, sentiment analysis, และ multiple output formats

## Test Scope

### In Scope
- การทำงานของ `fetch_news.py` ในสภาวะปกติ
- Parameter validation (ticker, limit, from/to dates, order)
- Output formatting (markdown, json)
- Date format validation
- Error handling (missing API key, invalid inputs, API failures)
- Limit boundary testing (1-1000 range)

### Out of Scope
- Performance testing under extreme load
- API rate limiting behavior (depends on Massive API plan)
- Real-time data accuracy verification
- Cross-platform testing (Linux/Windows specific)

## Test Strategy

### Test Types
1. **Functional Testing** - Verify core functionality works as expected
2. **Integration Testing** - API connectivity and data parsing
3. **Error Handling** - Missing API key, network errors, invalid inputs
4. **Parameter Validation** - Date formats, limit bounds, ticker case handling

### Test Approach
- Manual execution with various parameter combinations
- Boundary value analysis for limit parameters (0, 1, 1000, 1001)
- Date format validation (valid/invalid YYYY-MM-DD)
- Error injection for API key and network failures

## Test Environment

**Operating System:** macOS / Linux / Windows  
**Python Version:** 3.9+  
**Dependencies:** `massive` Python package (`pip install massive`)  
**API Key:** `MASSIVE_API_KEY` environment variable required  
**Network:** Internet connection required

## Entry Criteria

- [ ] Script is executable (`chmod +x`)
- [ ] Python 3.9+ installed
- [ ] `massive` package installed (`pip install massive`)
- [ ] `MASSIVE_API_KEY` environment variable set
- [ ] Internet connection available
- [ ] Massive API accessible (api.massive.com)

## Exit Criteria

- [ ] All P0 (Critical) test cases pass
- [ ] 90%+ P1 (High) test cases pass
- [ ] No critical bugs open
- [ ] Error handling works correctly
- [ ] API key validation works
- [ ] Documentation accurate

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Massive API unavailable/down | Low | High | Test with mock data / skip API tests |
| Invalid/expired API key | Medium | High | Verify API key before testing |
| API rate limiting | Medium | Medium | Add delays between requests |
| Network timeout variations | High | Low | Set explicit timeout expectations |
| No news for specific ticker | Medium | Low | Use popular tickers (AAPL, TSLA) |

## Test Deliverables

- [x] Test Plan Document (this file)
- [ ] Test Cases (TEST_CASES_FETCH_NEWS.md)
- [ ] Test Execution Report
- [ ] Bug Reports (if found)
- [ ] Regression Test Suite

## Test Schedule

| Phase | Duration | Activities |
|-------|----------|------------|
| Preparation | 15 min | Setup environment, verify API key |
| Functional Testing | 1 hour | Execute test cases |
| Error Handling Testing | 30 min | Test error scenarios |
| Regression Testing | 20 min | Run critical path tests |
| Reporting | 15 min | Document results |

---

## Quick Reference - Test Commands

```bash
# Prerequisites
pip install massive
export MASSIVE_API_KEY="your-api-key"

# Basic usage
python skills/massive-news/scripts/fetch_news.py AAPL

# With limit
python skills/massive-news/scripts/fetch_news.py TSLA --limit 5
python skills/massive-news/scripts/fetch_news.py GOOGL -n 20

# Date filtering
python skills/massive-news/scripts/fetch_news.py MSFT --from 2024-01-01
python skills/massive-news/scripts/fetch_news.py NVDA --from 2024-01-01 --to 2024-01-31

# Sort order
python skills/massive-news/scripts/fetch_news.py AAPL --order asc
python skills/massive-news/scripts/fetch_news.py AAPL --order desc

# JSON output
python skills/massive-news/scripts/fetch_news.py AAPL --json --limit 3

# Combined parameters
python skills/massive-news/scripts/fetch_news.py TSLA --limit 10 --from 2024-01-01 --order asc --json
```

---

**Next:** See [TEST_CASES_FETCH_NEWS.md](TEST_CASES_FETCH_NEWS.md) for detailed test cases.
