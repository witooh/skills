# Test Plan: CoinDesk News Skill

## Executive Summary

**Product:** coindesk-news Skill  
**Version:** 1.0.0  
**Test Date:** 2026-02-01  
**Tester:** QA Team  

CoinDesk News Skill เป็น Python-based CLI tool สำหรับดึงข่าว cryptocurrency จาก CoinDesk Data API โดยไม่ต้องใช้ API key ประกอบด้วย 3 scripts:
- `fetch_news.py` - ดึงข่าว crypto พร้อม filtering options
- `list_sources.py` - แสดงรายการ news sources
- `list_categories.py` - แสดงรายการ categories

## Test Scope

### In Scope
- การทำงานของทั้ง 3 scripts ในสภาวะปกติ
- Parameter validation และ error handling
- Output formatting (summary, markdown, json)
- API integration และ network error handling
- Unicode/encoding support

### Out of Scope
- Performance testing under extreme load
- Security penetration testing
- Cross-platform testing (Linux/Windows specific)
- API rate limiting behavior (depends on CoinDesk API)

## Test Strategy

### Test Types
1. **Functional Testing** - Verify core functionality works as expected
2. **Integration Testing** - API connectivity and data parsing
3. **Error Handling** - Network errors, invalid inputs, API failures
4. **UI/Output Testing** - Output formatting and display

### Test Approach
- Manual execution with various parameter combinations
- Boundary value analysis for limit parameters
- Equivalence partitioning for categories/sentiment filters
- Error injection for network failure scenarios

## Test Environment

**Operating System:** macOS / Linux / Windows  
**Python Version:** 3.8+  
**Network:** Internet connection required  
**Dependencies:** Python standard library only (argparse, json, urllib, datetime)

## Entry Criteria

- [x] All scripts are executable (`chmod +x`)
- [x] Python 3.8+ installed and accessible
- [x] Internet connection available
- [x] CoinDesk Data API accessible (https://data-api.coindesk.com)

## Exit Criteria

- [ ] All P0 (Critical) test cases pass
- [ ] 90%+ P1 (High) test cases pass
- [ ] No critical bugs open
- [ ] Error handling works correctly
- [ ] Documentation accurate

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| CoinDesk API unavailable/down | Medium | High | Test with mock data / skip API tests |
| API rate limiting | Medium | Medium | Add delays between requests |
| Network timeout variations | High | Low | Set explicit timeout expectations |
| Character encoding issues | Low | Medium | Test with various Unicode characters |

## Test Deliverables

- [x] Test Plan Document (this file)
- [ ] Test Cases (detailed step-by-step)
- [ ] Test Execution Report
- [ ] Bug Reports (if found)
- [ ] Regression Test Suite

## Test Schedule

| Phase | Duration | Activities |
|-------|----------|------------|
| Preparation | 30 min | Setup environment, review scripts |
| Functional Testing | 2 hours | Execute test cases for all scripts |
| Regression Testing | 30 min | Run critical path tests |
| Reporting | 30 min | Document results, create bug reports |

---

## Quick Reference - Test Commands

```bash
# Test fetch_news.py
python scripts/fetch_news.py --limit 5
python scripts/fetch_news.py --categories BTC,ETH --limit 3
python scripts/fetch_news.py --sentiment NEGATIVE
python scripts/fetch_news.py --format json --limit 2
python scripts/fetch_news.py --format markdown --limit 2

# Test list_sources.py
python scripts/list_sources.py
python scripts/list_sources.py --format json

# Test list_categories.py
python scripts/list_categories.py
python scripts/list_categories.py --filter BTC
python scripts/list_categories.py --format json --filter ETH
```

---

**Next:** See [TEST_CASES_FETCH_NEWS.md](TEST_CASES_FETCH_NEWS.md) for detailed test cases.
