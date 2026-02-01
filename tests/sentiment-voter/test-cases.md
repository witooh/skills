# Test Cases: Sentiment Voter Skill

## Smoke Tests

### TC-SMOKE-001: Basic Sentiment Analysis
**Priority:** P0 (Critical)  
**Type:** Functional  
**Estimated Time:** 3 minutes

#### Objective
Verify basic sentiment analysis works with a valid article

#### Preconditions
- Python 3.8+ installed
- opencode CLI configured
- sentiment_voter.py executable

#### Test Steps
1. Run basic sentiment analysis command:
   ```bash
   cd /Users/witooharianto/dev/witooh/skills/skills/sentiment-voter
   python3 scripts/sentiment_voter.py -a "Bitcoin price surges to new all-time high as institutional investors continue buying. Market sentiment extremely positive with analysts predicting further gains." -s BTC
   ```
   **Expected:** JSON output with sentiment field (bullish/bearish/neutral), confidence score (0-100), timestamp, and cached=false

2. Verify output contains all required fields:
   **Expected:** 
   - symbol: "BTC"
   - sentiment: one of ["bullish", "bearish", "neutral"]
   - confidence: numeric value between 0-100
   - timestamp: valid datetime string
   - cached: boolean false (first run)

#### Post-conditions
- Result cached in ~/.cache/sentiment-voter/

---

### TC-SMOKE-002: Cache Hit Functionality
**Priority:** P0 (Critical)  
**Type:** Functional  
**Estimated Time:** 2 minutes

#### Objective
Verify cache correctly retrieves previously analyzed results

#### Preconditions
- TC-SMOKE-001 completed (result cached)

#### Test Steps
1. Run same analysis again with same article:
   ```bash
   python3 scripts/sentiment_voter.py -a "Bitcoin price surges to new all-time high as institutional investors continue buying. Market sentiment extremely positive with analysts predicting further gains." -s BTC
   ```
   **Expected:** Same sentiment result with cached=true

2. Verify timestamp is identical to first run:
   **Expected:** cached=true, timestamp unchanged from first execution

#### Post-conditions
- Cache file exists and is valid
- No LLM calls made (retrieved from cache)

---

### TC-SMOKE-003: Clear Cache Command
**Priority:** P0 (Critical)  
**Type:** Functional  
**Estimated Time:** 2 minutes

#### Objective
Verify cache clearing functionality works

#### Preconditions
- Cache directory has at least one cached result

#### Test Steps
1. Clear all cache:
   ```bash
   python3 scripts/clear_cache.py --all
   ```
   **Expected:** Output shows "Removed N cache entries" where N >= 1

2. Verify cache directory is empty:
   ```bash
   ls ~/.cache/sentiment-voter/
   ```
   **Expected:** No .json files present (or directory doesn't exist)

#### Post-conditions
- Cache directory empty or removed
- Subsequent analysis calls LLMs (cached=false)

---

## Functional Tests

### TC-FUNC-001: Article Input via --article Flag
**Priority:** P1 (High)  
**Type:** Functional  
**Estimated Time:** 2 minutes

#### Objective
Verify article input via command line flag

#### Test Steps
1. Provide article directly:
   ```bash
   python3 scripts/sentiment_voter.py --article "Tesla reports record deliveries in Q4, beating analyst expectations. Stock rises 5% in after-hours trading." --symbol TSLA
   ```
   **Expected:** Valid JSON output with symbol="TSLA"

2. Use short flag:
   ```bash
   python3 scripts/sentiment_voter.py -a "Market volatility continues as inflation data surprises investors." -s SPY
   ```
   **Expected:** Valid JSON output with symbol="SPY"

---

### TC-FUNC-002: Article Input via --file Flag
**Priority:** P1 (High)  
**Type:** Functional  
**Estimated Time:** 3 minutes

#### Objective
Verify article input from file

#### Preconditions
- Test file exists: /tmp/test_article.txt with content

#### Test Steps
1. Create test file:
   ```bash
   echo "Ethereum network upgrade completed successfully, gas fees drop 30%. Developers celebrate improved scalability." > /tmp/test_article.txt
   ```

2. Analyze from file:
   ```bash
   python3 scripts/sentiment_voter.py --file /tmp/test_article.txt --symbol ETH
   ```
   **Expected:** Valid JSON output analyzing the file content

3. Use short flag:
   ```bash
   python3 scripts/sentiment_voter.py -f /tmp/test_article.txt -s ETH
   ```
   **Expected:** Same result as step 2

#### Post-conditions
- Test file can be deleted

---

### TC-FUNC-003: Stdin Input (Pipe)
**Priority:** P1 (High)  
**Type:** Functional  
**Estimated Time:** 2 minutes

#### Objective
Verify article input via stdin/pipe

#### Test Steps
1. Pipe article to script:
   ```bash
   echo "Solana blockchain experiences temporary outage, developers working on fix. Price drops 8% in hours." | python3 scripts/sentiment_voter.py -s SOL
   ```
   **Expected:** Valid JSON output analyzing piped content

2. Pipe from file:
   ```bash
   cat /tmp/test_article.txt | python3 scripts/sentiment_voter.py -s ETH
   ```
   **Expected:** Valid JSON output

---

### TC-FUNC-004: Custom Models Configuration
**Priority:** P1 (High)  
**Type:** Functional  
**Estimated Time:** 5 minutes

#### Objective
Verify custom models can be specified

#### Test Steps
1. Use custom model set:
   ```bash
   python3 scripts/sentiment_voter.py -a "NVIDIA announces new AI chips, revenue forecast beats expectations." -s NVDA -m "opencode/glm-4.7-free,opencode/kimi-k2.5-free,opencode/big-pickle"
   ```
   **Expected:** Valid JSON output, verbose mode should show all 3 custom models voting

2. Verify with verbose flag:
   ```bash
   python3 scripts/sentiment_voter.py -a "Test article content here." -s TEST -m "opencode/glm-4.7-free,opencode/kimi-k2.5-free,opencode/big-pickle" -v
   ```
   **Expected:** Output includes votes array with 3 custom model names

---

### TC-FUNC-005: Custom Cache TTL
**Priority:** P1 (High)  
**Type:** Functional  
**Estimated Time:** 5 minutes

#### Objective
Verify custom TTL configuration

#### Test Steps
1. Set short TTL (1 second):
   ```bash
   python3 scripts/sentiment_voter.py -a "Test article for TTL." -s TTL --ttl 1
   ```
   **Expected:** Analysis completes, result cached

2. Wait 2 seconds, run again:
   ```bash
   sleep 2 && python3 scripts/sentiment_voter.py -a "Test article for TTL." -s TTL --ttl 1
   ```
   **Expected:** cached=false (cache expired)

3. Set long TTL (1 hour = 3600 seconds):
   ```bash
   python3 scripts/sentiment_voter.py -a "Long TTL test." -s LONG --ttl 3600
   ```
   **Expected:** Result cached with 1-hour expiration

---

### TC-FUNC-006: Verbose Output Mode
**Priority:** P2 (Medium)  
**Type:** Functional  
**Estimated Time:** 2 minutes

#### Objective
Verify verbose mode shows detailed voting breakdown

#### Test Steps
1. Run with verbose flag:
   ```bash
   python3 scripts/sentiment_voter.py -a "Apple unveils new iPhone with revolutionary features. Pre-orders exceed expectations." -s AAPL -v
   ```
   **Expected:** JSON output includes votes array with:
   - model names
   - individual sentiments
   - individual confidence scores
   - reasoning for each vote

2. Verify votes array has 3 entries:
   **Expected:** votes.length === 3

---

### TC-FUNC-007: No Cache Mode
**Priority:** P1 (High)  
**Type:** Functional  
**Estimated Time:** 2 minutes

#### Objective
Verify --no-cache flag disables caching

#### Test Steps
1. Run without cache:
   ```bash
   python3 scripts/sentiment_voter.py -a "Test article." -s NOCACHE --no-cache
   ```
   **Expected:** Valid result, no cache file created

2. Run again with same article:
   ```bash
   python3 scripts/sentiment_voter.py -a "Test article." -s NOCACHE --no-cache
   ```
   **Expected:** cached=false (not retrieved from cache)

---

## Integration Tests

### TC-INT-001: Multi-LLM Voting Consensus
**Priority:** P0 (Critical)  
**Type:** Integration  
**Estimated Time:** 3 minutes

#### Objective
Verify 3 LLMs vote and consensus is calculated correctly

#### Test Steps
1. Run analysis with verbose mode:
   ```bash
   python3 scripts/sentiment_voter.py -a "Strong bullish sentiment across all markets. Major indices hit record highs. Institutional buying continues." -s SPY -v
   ```
   **Expected:** 
   - All 3 models return votes
   - Final sentiment based on majority
   - Confidence calculated from votes

2. Verify aggregation logic:
   - If 2+ models agree → that sentiment wins
   - If tie → higher confidence wins
   - Unanimous → full confidence
   - Majority → 80% confidence
   - Split → 50% confidence

---

### TC-INT-002: LLM Response Parsing
**Priority:** P1 (High)  
**Type:** Integration  
**Estimated Time:** 3 minutes

#### Objective
Verify LLM responses are parsed correctly

#### Test Steps
1. Test valid JSON response:
   **Expected:** Parser extracts sentiment, confidence, reasoning correctly

2. Test malformed JSON (fallback):
   **Expected:** Fallback parser detects keywords (bullish/bearish/neutral) from text

3. Test invalid sentiment value:
   **Expected:** Invalid values default to "neutral"

4. Test out-of-range confidence:
   **Expected:** Clamped to 0-100 range

---

### TC-INT-003: Integration with coindesk-news
**Priority:** P1 (High)  
**Type:** Integration  
**Estimated Time:** 5 minutes

#### Objective
Verify integration with coindesk-news skill

#### Preconditions
- coindesk-news skill installed and working

#### Test Steps
1. Get news and analyze:
   ```bash
   news=$(opencode run "use coindesk-news skill to get latest BTC article")
   python3 scripts/sentiment_voter.py -a "$news" -s BTC -v
   ```
   **Expected:** Valid sentiment analysis of fetched news

2. Verify no errors in pipeline:
   **Expected:** Exit code 0, valid JSON output

---

### TC-INT-004: Integration with massive-news
**Priority:** P1 (High)  
**Type:** Integration  
**Estimated Time:** 5 minutes

#### Objective
Verify integration with massive-news skill

#### Preconditions
- massive-news skill installed and working

#### Test Steps
1. Get stock news and analyze:
   ```bash
   news=$(opencode run "use massive-news skill to get latest AAPL article")
   python3 scripts/sentiment_voter.py -a "$news" -s AAPL -v
   ```
   **Expected:** Valid sentiment analysis of fetched news

2. Test ETF:
   ```bash
   news=$(opencode run "use massive-news skill to get latest SPY news")
   python3 scripts/sentiment_voter.py -a "$news" -s SPY
   ```
   **Expected:** Valid sentiment analysis

---

## Error Handling Tests

### TC-ERR-001: Missing Article Input
**Priority:** P1 (High)  
**Type:** Error Handling  
**Estimated Time:** 1 minute

#### Objective
Verify error when no article provided

#### Test Steps
1. Run without article:
   ```bash
   python3 scripts/sentiment_voter.py -s BTC
   ```
   **Expected:** Error message "Error: No article content provided", exit code 1

2. Run with empty stdin:
   ```bash
   echo "" | python3 scripts/sentiment_voter.py -s BTC
   ```
   **Expected:** Same error message

---

### TC-ERR-002: Invalid Number of Models
**Priority:** P2 (Medium)  
**Type:** Error Handling  
**Estimated Time:** 1 minute

#### Test Steps
1. Use 2 models:
   ```bash
   python3 scripts/sentiment_voter.py -a "Test." -s TEST -m "model1,model2"
   ```
   **Expected:** Error "Error: Exactly 3 models required"

2. Use 4 models:
   ```bash
   python3 scripts/sentiment_voter.py -a "Test." -s TEST -m "m1,m2,m3,m4"
   ```
   **Expected:** Error "Error: Exactly 3 models required"

3. Use 1 model:
   ```bash
   python3 scripts/sentiment_voter.py -a "Test." -s TEST -m "model1"
   ```
   **Expected:** Error "Error: Exactly 3 models required"

---

### TC-ERR-003: Non-existent File
**Priority:** P2 (Medium)  
**Type:** Error Handling  
**Estimated Time:** 1 minute

#### Test Steps
1. Reference non-existent file:
   ```bash
   python3 scripts/sentiment_voter.py -f /nonexistent/file.txt -s TEST
   ```
   **Expected:** File not found error, graceful exit

---

### TC-ERR-004: LLM Call Timeout
**Priority:** P1 (High)  
**Type:** Error Handling  
**Estimated Time:** 3 minutes

#### Objective
Verify timeout handling when LLM call takes too long

#### Preconditions
- Can simulate slow network or use invalid model

#### Test Steps
1. Use invalid model to simulate failure:
   ```bash
   python3 scripts/sentiment_voter.py -a "Test article." -s TEST -m "invalid-model-1,invalid-model-2,invalid-model-3" --verbose
   ```
   **Expected:** 
   - Error logged for each failed model
   - Fallback vote added (neutral, confidence=20)
   - Analysis completes with remaining votes

---

### TC-ERR-005: Cache Corruption Handling
**Priority:** P2 (Medium)  
**Type:** Error Handling  
**Estimated Time:** 3 minutes

#### Objective
Verify handling of corrupted cache files

#### Test Steps
1. Create corrupted cache file:
   ```bash
   mkdir -p ~/.cache/sentiment-voter
   echo "invalid json" > ~/.cache/sentiment-voter/corrupted.json
   ```

2. Trigger cache read:
   ```bash
   python3 scripts/sentiment_voter.py -a "Test." -s CORRUPT
   ```
   **Expected:** Corrupted file deleted, new analysis performed

---

## Cache Management Tests

### TC-CACHE-001: Clear Expired Entries
**Priority:** P1 (High)  
**Type:** Functional  
**Estimated Time:** 3 minutes

#### Objective
Verify clear_cache.py removes expired entries only

#### Test Steps
1. Create entries with different ages:
   - Entry A: Just created (not expired)
   - Entry B: Created 5 hours ago (expired with default 4hr TTL)

2. Clear expired:
   ```bash
   python3 scripts/clear_cache.py
   ```
   **Expected:** Only Entry B removed

---

### TC-CACHE-002: Clear Specific Symbol
**Priority:** P2 (Medium)  
**Type:** Functional  
**Estimated Time:** 2 minutes

#### Objective
Verify --symbol flag clears specific symbol only

#### Test Steps
1. Have cached entries for BTC, ETH, SOL

2. Clear only BTC:
   ```bash
   python3 scripts/clear_cache.py --symbol BTC
   ```
   **Expected:** Only BTC entries removed, ETH and SOL remain

---

### TC-CACHE-003: Cache Directory Creation
**Priority:** P2 (Medium)  
**Type:** Functional  
**Estimated Time:** 1 minute

#### Objective
Verify cache directory auto-created if not exists

#### Test Steps
1. Remove cache directory:
   ```bash
   rm -rf ~/.cache/sentiment-voter
   ```

2. Run analysis:
   ```bash
   python3 scripts/sentiment_voter.py -a "Test." -s TEST
   ```
   **Expected:** Directory created automatically, cache file saved

---

## Edge Case Tests

### TC-EDGE-001: Very Long Article (>8000 chars)
**Priority:** P2 (Medium)  
**Type:** Edge Case  
**Estimated Time:** 2 minutes

#### Objective
Verify articles >8000 chars are truncated correctly

#### Test Steps
1. Create long article:
   ```bash
   python3 -c "print('Bitcoin news ' * 1000)" > /tmp/long_article.txt
   wc -c /tmp/long_article.txt  # Should be >8000
   ```

2. Analyze:
   ```bash
   python3 scripts/sentiment_voter.py -f /tmp/long_article.txt -s BTC -v
   ```
   **Expected:** Analysis completes (truncated to 8000 chars), valid result

---

### TC-EDGE-002: Very Short Article (<100 chars)
**Priority:** P2 (Medium)  
**Type:** Edge Case  
**Estimated Time:** 1 minute

#### Test Steps
1. Analyze short text:
   ```bash
   python3 scripts/sentiment_voter.py -a "BTC up." -s BTC
   ```
   **Expected:** Valid analysis despite minimal context

---

### TC-EDGE-003: Special Characters in Article
**Priority:** P2 (Medium)  
**Type:** Edge Case  
**Estimated Time:** 2 minutes

#### Test Steps
1. Test with special chars:
   ```bash
   python3 scripts/sentiment_voter.py -a "Bitcoin's price: $50,000! 🚀 <script>alert('test')</script>" -s BTC
   ```
   **Expected:** Handles special chars gracefully, no crashes

---

### TC-EDGE-004: Unicode/Non-English Content
**Priority:** P3 (Low)  
**Type:** Edge Case  
**Estimated Time:** 2 minutes

#### Test Steps
1. Test with Thai:
   ```bash
   python3 scripts/sentiment_voter.py -a "ราคาบิทคอยน์พุ่งสูงเป็นประวัติการณ์ นักลงทุนสถาบันซื้อต่อเนื่อง" -s BTC
   ```
   **Expected:** Analysis completes (may be less accurate but no crash)

2. Test with Chinese:
   ```bash
   python3 scripts/sentiment_voter.py -a "比特币价格创新高，机构投资者持续买入" -s BTC
   ```
   **Expected:** Analysis completes

---

### TC-EDGE-005: Empty Symbol
**Priority:** P2 (Medium)  
**Type:** Edge Case  
**Estimated Time:** 1 minute

#### Test Steps
1. Run without symbol (uses default "asset"):
   ```bash
   python3 scripts/sentiment_voter.py -a "Market analysis."
   ```
   **Expected:** symbol="asset" in output

---

## Performance Tests

### TC-PERF-001: Parallel LLM Execution
**Priority:** P1 (High)  
**Type:** Performance  
**Estimated Time:** 3 minutes

#### Objective
Verify 3 LLMs are called in parallel (not sequentially)

#### Test Steps
1. Run with timing:
   ```bash
   time python3 scripts/sentiment_voter.py -a "Test article for performance measurement." -s PERF -v
   ```
   **Expected:** Total time < (sum of individual LLM calls), indicating parallel execution

---

### TC-PERF-002: Cache Retrieval Speed
**Priority:** P2 (Medium)  
**Type:** Performance  
**Estimated Time:** 2 minutes

#### Test Steps
1. First call (no cache):
   ```bash
   time python3 scripts/sentiment_voter.py -a "Cache speed test." -s SPEED
   ```
   Note the time (includes 3 LLM calls)

2. Second call (cache hit):
   ```bash
   time python3 scripts/sentiment_voter.py -a "Cache speed test." -s SPEED
   ```
   **Expected:** Significantly faster (< 1 second vs. 10-30 seconds)

---

## Regression Tests

### TC-REG-001: Full Regression Suite
**Priority:** P0 (Critical)  
**Type:** Regression  
**Estimated Time:** 30 minutes

#### Objective
Run complete test suite to verify no regressions

#### Test List
- [ ] TC-SMOKE-001: Basic sentiment analysis
- [ ] TC-SMOKE-002: Cache hit
- [ ] TC-SMOKE-003: Clear cache
- [ ] TC-FUNC-001 to TC-FUNC-007: All functional tests
- [ ] TC-INT-001 to TC-INT-004: All integration tests
- [ ] TC-ERR-001 to TC-ERR-003: Critical error handling
- [ ] TC-CACHE-001 to TC-CACHE-002: Cache management

#### Pass Criteria
- 90%+ tests pass
- No P0 tests fail
- All critical paths work

---

## Appendix: Test Data

### Sample Articles

**Bullish Article:**
```
Bitcoin price surges to new all-time high as institutional investors continue buying. 
Market sentiment extremely positive with analysts predicting further gains. 
Major companies announce Bitcoin treasury additions.
```

**Bearish Article:**
```
Cryptocurrency markets crash as regulatory crackdown intensifies. 
Major exchange faces liquidity crisis, withdrawals halted. 
Investor confidence at all-time low, panic selling continues.
```

**Neutral Article:**
```
Stock market closes mixed as investors await Fed decision. 
Tech sector shows gains while energy stocks decline. 
Trading volume remains average with no major movements.
```

---

*Test Cases Version: 1.0*  
*Created: 2024-02-01*  
*Total Test Cases: 35*  
*Estimated Total Time: ~3 hours*