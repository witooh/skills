# Test Plan: Sentiment Voter Skill

## Executive Summary

**Feature:** Sentiment Voter Skill - Multi-LLM sentiment analysis with voting and caching for stock/ETF/crypto articles.

**Testing Objectives:**
- Verify multi-LLM voting mechanism works correctly
- Validate cache system with TTL functionality
- Ensure CLI interface handles all input methods
- Verify error handling and edge cases
- Test integration with news skills (coindesk-news, massive-news)

**Key Risks:**
- LLM API failures affecting voting reliability
- Cache corruption or TTL issues
- Parallel execution race conditions
- Integration failures with external news sources

**Timeline:** 2-3 hours

---

## Test Scope

### In Scope:

**Core Features:**
- Multi-LLM sentiment voting (3 models)
- Sentiment classification (bullish/bearish/neutral)
- Confidence scoring algorithm
- File-based caching with TTL
- Cache management (clear_cache.py)

**CLI Interface:**
- Article input via --article flag
- File input via --file flag
- Stdin input (pipe)
- Custom models configuration
- Cache TTL configuration
- Symbol specification
- Verbose output mode

**Integration:**
- opencode run command execution
- coindesk-news skill integration
- massive-news skill integration

### Out of Scope:
- News fetching functionality (tested separately)
- LLM model performance/accuracy
- Network connectivity issues
- File system permissions (assumed valid)

---

## Test Strategy

### Test Types:

1. **Functional Testing** - Core voting logic, sentiment aggregation
2. **Integration Testing** - LLM calls, news skill integration
3. **Regression Testing** - Cache functionality, CLI stability
4. **Error Handling** - Invalid inputs, API failures, timeouts
5. **Performance Testing** - Parallel execution, cache retrieval speed

### Test Approach:

- **Black box testing** - Test as end user would use
- **Positive testing** - Valid inputs and normal flows
- **Negative testing** - Invalid inputs and error conditions
- **Boundary testing** - TTL limits, article size limits
- **Parallel testing** - Concurrent LLM calls

---

## Test Environment

### Requirements:

- **OS:** macOS / Linux / Windows (cross-platform)
- **Python:** 3.8+
- **CLI Tools:** opencode (for LLM calls)
- **Network:** Internet connection (for LLM API)
- **Disk Space:** ~100MB for cache directory

### Test Data:

**Sample Articles:**
- Crypto article (BTC/ETH news)
- Stock article (AAPL/TSLA news)
- Neutral article (market overview)
- Edge case: Very long article (>8000 chars)
- Edge case: Short article (<100 chars)
- Edge case: Non-English article
- Edge case: Article with special characters

**Test Symbols:**
- BTC, ETH, SOL (crypto)
- AAPL, TSLA, NVDA (stocks)
- SPY, VOO (ETFs)

---

## Entry Criteria

- [ ] Skill directory structure complete
- [ ] All scripts executable and syntax-valid
- [ ] Python 3.8+ installed
- [ ] opencode CLI installed and configured
- [ ] Test data prepared
- [ ] Cache directory writable

---

## Exit Criteria

- [ ] All P0 test cases executed
- [ ] 90%+ test case pass rate
- [ ] No critical bugs open
- [ ] All high-severity bugs documented with workarounds
- [ ] Cache functionality verified
- [ ] Integration with news skills tested

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| LLM API rate limiting | Medium | High | Implement retry logic, test with delays |
| Cache corruption on disk full | Low | Medium | Handle disk full errors gracefully |
| Parallel execution deadlock | Low | High | Set reasonable timeouts, add watchdog |
| opencode CLI not installed | Medium | High | Check prerequisites in setup |
| Network timeout during LLM call | Medium | Medium | Implement timeout handling |

---

## Test Deliverables

1. Test plan document (this file)
2. Manual test cases (test-cases.md)
3. Test execution report
4. Bug reports (if any)
5. Test summary report

---

## Regression Suite

### Smoke Tests (15 min):
- TC-SMOKE-001: Basic sentiment analysis with valid article
- TC-SMOKE-002: Cache hit functionality
- TC-SMOKE-003: Clear cache command

### Full Regression (60 min):
- All functional test cases
- All integration test cases
- All error handling test cases
- Cache boundary tests

---

## Test Schedule

| Phase | Duration | Activities |
|-------|----------|------------|
| Setup | 15 min | Environment prep, test data creation |
| Functional | 45 min | Core voting logic tests |
| Integration | 30 min | LLM calls, news skill integration |
| Error Handling | 30 min | Invalid inputs, failures |
| Cache | 30 min | TTL, clearing, corruption |
| Regression | 30 min | Full suite execution |
| Reporting | 15 min | Results compilation |

**Total Estimated Time:** ~3 hours

---

## Success Criteria

**PASS:**
- All P0 tests pass (100%)
- 90%+ of all tests pass
- Sentiment voting works with all 3 models
- Cache correctly stores and retrieves results
- CLI handles all input methods correctly
- No data loss or corruption

**CONDITIONAL PASS:**
- P1 failures with documented workarounds
- Known limitations documented
- Non-critical UI issues

**FAIL:**
- Any P0 test fails
- Critical bug in voting logic
- Cache corruption causing data loss
- Integration completely broken

---

*Created: 2024-02-01*
*Tester: QA Team*
*Status: Draft*
