---
name: dca-analyst
description: Analyze DCA and Enhanced DCA (eDCA) portfolios using agent-first data collection (Playwright browsing + news skills) to gather technical analysis (daily/weekly), news context, and market data. Supports standard DCA, Value Averaging, RSI-adjusted DCA, and volatility-based strategies. Use when users ask to analyze DCA, evaluate an eDCA plan, review portfolio performance, or compare DCA strategies. Trigger phrases include "DCA", "eDCA", "ถัวเฉลี่ย", "ถัวเฉลี่ยต้นทุน", "value averaging", "DCA ขั้นเทพ", "วิเคราะห์พอร์ต", "DCA analysis", "enhanced DCA", "adaptive DCA".
metadata:
  version: 1.0
---

# DCA Analyst (Pro Edition)

Analyze standard and Enhanced DCA (eDCA) portfolios using agent-driven data collection and advanced strategy modeling. Supports adaptive strategies that adjust investment amounts based on market conditions. This skill is informational only and does not provide investment advice.

## Required Inputs (from user)

Provide as much of the following as possible; if data is missing, proceed with explicit assumptions.

### Basic Portfolio Data

- Portfolio holdings: symbol, asset type (stock/ETF/crypto), current units, avg cost, currency
- DCA plan: base amount per interval, frequency (weekly/monthly), start date, target horizon
- Allocation targets (optional): percentage per asset
- Fees/constraints (optional): transaction fees, exchange limits, tax assumptions
- Preferred sources (optional): specific sites, regions, or news sources

### eDCA Strategy Selection (optional)

- **Strategy type**: `standard`, `value_averaging`, `rsi_adjusted`, `volatility_based`, `momentum_based`
- **Adjustment parameters**: multiplier range (e.g., 0.5x to 2.0x), thresholds
- **Risk settings**: max position size, stop conditions

**Example (Standard DCA):**

```json
{
  "base_currency": "USD",
  "dca_plan": { "amount": 500, "frequency": "monthly", "start": "2023-01-01" },
  "holdings": [
    { "symbol": "AAPL", "type": "stock", "units": 10, "avg_cost": 175.2 },
    { "symbol": "QQQ", "type": "etf", "units": 4, "avg_cost": 380.0 }
  ]
}
```

**Example (Enhanced DCA - RSI Strategy):**

```json
{
  "base_currency": "USD",
  "dca_plan": {
    "base_amount": 500,
    "frequency": "monthly",
    "strategy": "rsi_adjusted",
    "adjustment_rules": {
      "multiplier_min": 0.5,
      "multiplier_max": 2.0,
      "rsi_oversold": 30,
      "rsi_overbought": 70
    }
  },
  "holdings": [{ "symbol": "QQQ", "type": "etf", "units": 5, "avg_cost": 375.0 }]
}
```

## Enhanced DCA (eDCA) Strategies

Choose a strategy based on user's sophistication and data availability. All strategies are informational models only.

### 1. Standard DCA

**Description**: Fixed amount invested at regular intervals regardless of price.
**Use when**: User wants simplicity, beginner-friendly approach.
**Formula**: `investment = base_amount` (constant)

### 2. Value Averaging (VA)

**Description**: Adjust investment to maintain a target portfolio value trajectory.
**Use when**: User wants to "buy low, sell high" automatically within accumulation phase.
**Formula**:

```
target_value = base_amount × period_number
gap = target_value - current_value
investment = base_amount + gap
```

**Constraints**: Set min/max investment limits to avoid extreme contributions.

### 3. RSI-Adjusted DCA

**Description**: Increase investment when RSI indicates oversold conditions, decrease when overbought.
**Use when**: Technical indicators available, user wants mean-reversion approach.
**Formula**:

```
if RSI < 30: multiplier = max_multiplier (e.g., 2.0x)
if RSI > 70: multiplier = min_multiplier (e.g., 0.5x)
if 30 <= RSI <= 70: multiplier = linear interpolation
investment = base_amount × multiplier
```

### 4. Volatility-Based DCA

**Description**: Increase investment during high volatility (potential opportunities), decrease during low volatility.
**Use when**: Market volatility data available, user wants risk-adjusted approach.
**Formula**:

```
volatility_z = (current_volatility - avg_volatility) / std_volatility
multiplier = base_multiplier + (volatility_z × sensitivity)
investment = base_amount × clamp(multiplier, min, max)
```

### 5. Momentum-Based DCA (Trend Following)

**Description**: Increase investment during uptrends, decrease during downtrends (contrarian to mean reversion).
**Use when**: User believes in trend continuation, has moving average data.
**Formula**:

```
if price > MA(50): multiplier increases (up to max)
if price < MA(50): multiplier decreases (down to min)
investment = base_amount × multiplier
```

## Core Workflow (Agent-First)

### Phase 1: Strategy Setup

1. **Identify strategy type**
   - Parse user input for strategy selection.
   - Default to `standard` if not specified.
   - Validate adjustment parameters (min/max multipliers, thresholds).

2. **Validate inputs**
   - Normalize symbols and currencies.
   - If units or avg cost are missing, mark those metrics as unavailable.
   - Load `references/dca-metrics.md` and `references/edca-strategies.md`.

### Phase 2: Data Collection

3. **Market data (prices + history)**
   - Use `stock-market` skill to fetch current prices and historical data.
   - Capture timestamps and quote currency.
   - For eDCA: fetch minimum 50 days of history for RSI/MA calculations.

4. **Technical analysis (daily + weekly)**
   - Use `/playwright` skill to open technical analysis pages.
   - **For ETFs on investing.com**:
     - Navigate to `https://www.investing.com/etfs/{identifier}`
     - Click on "Technical" tab or scroll to Technical Analysis section
     - **MUST CAPTURE** (in order of priority):
       1. **Technical Summary**: Daily and Weekly signals (Strong Sell/Sell/Neutral/Buy/Strong Buy)
       2. **Technical Indicators** section - capture ALL of:
          - RSI(14) value and signal (e.g., "42.211 - Sell")
          - MACD(12,26) value and signal (e.g., "-0.37 - Sell")
          - STOCH(9,6) value and signal
          - ADX(14) value and signal
          - CCI(14) value and signal
          - Williams %R value and signal
          - ATR(14) value (for volatility calculation)
       3. **Moving Averages** section:
          - Summary signal (Strong Sell/Sell/Neutral/Buy/Strong Buy)
          - Individual MA values: MA5, MA10, MA20, MA50, MA100, MA200
          - Count of Buy vs Sell signals
       4. **Pivot Points** (optional but useful):
          - Classic Pivot Point (P)
          - Support levels (S1, S2, S3)
          - Resistance levels (R1, R2, R3)
   - **For Stocks**: Use investing.com Stocks Technical Summary or individual stock pages with same data points.
   - **Save method**: Take screenshot OR copy-paste the Technical Analysis table content
   - **Fallback**: If investing.com page not found, try TradingView (tradingview.com/symbols/EXCHANGE-TICKER) for individual indicators.

5. **News context**
   - Use `massive-news` for stocks/ETFs.
   - Use `coindesk-news` for crypto.
   - Run `sentiment-voter` for consensus sentiment on key articles.

### Phase 3: Analysis & Modeling

6. **Calculate eDCA multipliers**
   - For RSI strategy: compute current RSI, determine multiplier.
   - For volatility strategy: calculate rolling volatility, determine multiplier.
   - For value averaging: compute target trajectory, determine gap.
   - Apply min/max constraints to all multipliers.

7. **Project scenarios**
   - Model 3 scenarios: Bull (prices +20%), Base (current trend), Bear (prices -20%).
   - Show how eDCA vs Standard DCA performs in each scenario.
   - Calculate "Enhanced Value" = potential units gained vs standard approach.

8. **DCA metrics**
   - Compute standard metrics (total invested, current value, P/L).
   - Compute eDCA metrics (projected optimal investment, cost basis improvement).
   - Use formulas in `references/dca-metrics.md`.

### Phase 4: Synthesis

9. **Generate report**
   - **Read previous reports** from `./report/` (1-3 most recent) for learning context
   - Compare current recommendations with past ones
   - Note if market conditions are similar to previous periods
   - Provide structured summary with strategy details.
   - Include scenario analysis and sensitivity testing.
   - Keep language descriptive and avoid investment advice.
   - **Add Learning Metadata section** at end for future agent learning
   - **Save report** to `./report/` with filename format: `YYYY-MM-DD-HH:MM:SS.md` (local time)

## Output Format (Markdown)

### Language

**Primary Language**: Thai (ภาษาไทย)

- All reports should be generated in Thai for user comprehension
- Technical terms may remain in English with Thai explanations
- Numerical data: Use comma (,) for thousands, period (.) for decimals (Thai format)

### Report Structure - Executive Summary First

All reports MUST start with **Executive Summary (สรุปผลการวิเคราะห์)** at the top:

```
# รายงานวิเคราะห์ DCA - [ชื่อ Portfolio]

**วันที่รายงาน**: 2026-02-02 20:53:58 (เวลาไทย)
**ไฟล์**: ./report/2026-02-02-20:53:58.md

---

## 🎯 สรุปผลการวิเคราะห์ (Executive Summary)

### 📊 ภาพรวมพอร์ต
- มูลค่าพอร์ตปัจจุบัน: $X,XXX (+XX%)
- กำไร/ขาดทุน: +$XXX (ไม่รวมการขาย)
- จำนวนสินทรัพย์: X ตัว

### 💰 แผน DCA เดือนนี้
**งบประมาณ**: 30,000 บาท (อัตราแลกเปลี่ยน: 34.XX บาท/ดอลลาร์)

| สินทรัพย์ | สัญญาณ | Multiplier | จำนวนเงิน | คำแนะนำ |
|---------|--------|-----------|----------|---------|
| SMH | ซื้อแรง (Strong Buy) | 1.2x | $XXX (~XX,XXX บาท) | เพิ่มการลงทุน |
| QQQM | ซื้อ (Buy) | 1.4x | $XXX (~XX,XXX บาท) | โอกาสดี RSI ต่ำ |

### ⚡ การกระทำที่แนะนำ (Action Items)
1. **ด่วน**: ซื้อ QQQM 1.4x (RSI 42 ใกล้ oversold)
2. **ติดตาม**: SMH ใกล้จุดสูงสุด 52 สัปดาห์ - ระวังจุดกลับตัว
3. **ระวัง**: พอร์ตกระจุกตัวเทคโนโลยี 89% - พิจารณากระจายความเสี่ยง

### 📈 สรุป Technical Signals
- **SMH**: Daily/Weekly/Monthly = Strong Buy ✅
- **QQQM**: Daily = Neutral ⚪ | Weekly/Monthly = Strong Buy ✅

### ⚠️ จุดเสี่ยงที่ต้องระวัง
- ความเสี่ยงขาลงสูง: พอร์ตรวมเทคโนโลยี
- QQQM กำลังปรับตัวลง - โอกาสเข้าซื้อ
- SMH ใกล้จุดสูงสุด - ระวังการย่อตัว

---

## 📋 รายละเอียดการวิเคราะห์ (Full Analysis)
[รายละเอียดเต็มตามหัวข้อด้านล่าง...]
```

### Standard DCA Report

```
## ภาพรวมพอร์ต (Portfolio Summary)
- สกุลเงิน: ...
- แผน DCA: ...
- สินทรัพย์: ...

## วิเคราะห์ทางเทคนิค (Technical Analysis)
- แหล่งข้อมูล: ...
- รายวัน: ...
- รายสัปดาห์: ...

## สรุปข่าวสาร (News Summary)
- หุ้น/ETF: ...
- คริปโต: ...
- ความรู้สึกตลาด: ...

## สถิติ DCA (DCA Metrics)
| สัญลักษณ์ | ราคาเฉลี่ย | เงินลงทุนรวม | มูลค่าปัจจุบัน | กำไร/ขาดทุน | บันทึก |
|----------|------------|-------------|---------------|------------|--------|

## ข้อสมมติและช่องโหว่ข้อมูล
- ...

## แหล่งข้อมูล
- URLs, timestamps, screenshots
```

### Enhanced DCA (eDCA) Report

```
## ภาพรวมพอร์ต (Portfolio Summary)
- สกุลเงิน: ...
- กลยุทธ์: [standard/value_averaging/rsi_adjusted/volatility_based/momentum]
- จำนวนพื้นฐาน: ...
- ช่วงปรับตัว: 0.5x - 2.0x

## บริบทตลาดและตัวชี้วัด (Market Context & Indicators)
- RSI ปัจจุบัน: ...
- ความผันผวน (30 วัน): ...
- แนวโน้ม: ...
- สรุปทางเทคนิค: ...

## eDCA Analysis
| Metric | Current | Standard DCA | eDCA Recommendation |
|--------|---------|--------------|---------------------|
| Multiplier | 1.0x | 1.0x (fixed) | 1.5x (RSI=25) |
| Suggested Investment | $500 | $500 | $750 |
| Projected Avg Cost | $175 | $180 | $168 |
| Units This Period | 2.86 | 2.78 | 4.46 |

## Scenario Analysis (90-day projection)
| Scenario | Price Change | Std DCA Value | eDCA Value | Advantage |
|----------|--------------|---------------|------------|-----------|
| Bull | +20% | $1,200 | $1,350 | +$150 (+12.5%) |
| Base | 0% | $1,000 | $1,080 | +$80 (+8%) |
| Bear | -20% | $800 | $920 | +$120 (+15%) |

## Risk Metrics
- Max Drawdown (historical): ...
- Volatility-adjusted return: ...
- Value at Risk (95%): ...

## News & Sentiment
- Key developments: ...
- Consensus sentiment: ...
- Impact on strategy: ...

## Strategy Notes
- Why this multiplier was chosen: ...
- Alternative scenarios: ...
- Risk warnings: ...

## Sources & Assumptions
- Data sources: ...
- Calculation assumptions: ...
- Confidence level: ...
```

## Report Storage

All DCA analysis reports must be saved to disk for future reference.

### Directory Structure

- **Location**: `./report/`
- **Create if missing**: Automatically create the directory if it doesn't exist

### Filename Format

Use local time format: `YYYY-MM-DD-HH:MM:SS.md`

**Examples**:

- `./report/2026-01-25-18:00:00.md`
- `./report/2026-02-02-14:30:00.md`

**Time Format Rules**:

- Use **local time** (not UTC)
- 24-hour format
- Zero-padded: `18:00:00` (not `6:0:0`)
- Include seconds for uniqueness

### How to Determine Local Time

1. Check user's timezone from context or system settings
2. Default to Asia/Bangkok (UTC+7) if not specified
3. Use current timestamp when report is generated

### File Format

- **Format**: Markdown (`.md`)
- **Encoding**: UTF-8
- **Language**: Thai (ภาษาไทย)
- **Content**: Full report with Executive Summary at top, followed by detailed analysis

### Workflow

1. Gather data (prices, technical indicators, exchange rate)
2. Calculate eDCA multipliers based on technical signals
3. **Generate report in Thai** with Executive Summary first
4. **Include Action Items** with clear recommendations
5. Save to `./report/` with filename format: `{YYYY-MM-DD-HH:MM:SS}.md`
6. Confirm file saved successfully
7. Include saved path in final response to user

### Required Data Collection Checklist

Before generating report, ensure you have:

- [ ] Current prices for all holdings
- [ ] THB/USD exchange rate from Kasikornbank
- [ ] Technical indicators (RSI, MACD, ATR) from investing.com
- [ ] Daily and Weekly technical summary signals
- [ ] Moving averages (at least MA20, MA50, MA200)
- [ ] Recent news context (optional but recommended)
- [ ] Calculated eDCA multipliers for each holding
- [ ] **Previous reports from `./report/`** (for learning context - read 1-3 most recent)

## Tools to Use

- **/playwright**: browse technical analysis pages and capture daily/weekly sections with indicators (RSI, MACD, MA)
- **stock-market**: fetch current and historical prices (min 50 days for eDCA calculations)
- **massive-news**: stock/ETF news
- **coindesk-news**: crypto news
- **sentiment-voter**: multi-LLM sentiment consensus for news context

## Data Sources & URL Patterns

### Investing.com ETF Technical Analysis

For ETFs, use these URL patterns to access technical analysis data:

**Main ETF Page** (includes Technical Analysis tab):

- Pattern: `https://www.investing.com/etfs/{etf-identifier}`
- Examples:
  - QQQM: `https://www.investing.com/etfs/qqqm`
  - SMH: `https://www.investing.com/etfs/holdrs-merrill-lynch-semiconductor` (legacy URL)
  - SPY: `https://www.investing.com/etfs/spdr-s-p-500`

**Note**: Some ETFs use legacy ticker identifiers. If the direct ticker URL fails, try:

1. Search on investing.com for the ETF name
2. Use the legacy identifier from search results
3. For SMH specifically, use `holdrs-merrill-lynch-semiconductor` instead of `smh`

**Technical Data Available**:

- Timeframes: 1 Min, 5 Min, 15 Min, 30 Min, Hourly, Daily, Weekly, Monthly
- **Technical Summary**: Strong Sell / Sell / Neutral / Buy / Strong Buy
- **Technical Indicators** (capture ALL these values):
  - RSI(14) - Critical for RSI-adjusted DCA strategy
  - MACD(12,26) - Trend direction and momentum
  - STOCH(9,6) - Stochastic oscillator
  - STOCHRSI(14) - Stochastic RSI
  - ADX(14) - Trend strength
  - CCI(14) - Commodity Channel Index
  - Williams %R - Overbought/oversold indicator
  - ATR(14) - Average True Range (volatility measure)
  - ROC - Rate of Change
  - Ultimate Oscillator
  - Bull/Bear Power(13)
- **Moving Averages**:
  - MA5, MA10, MA20, MA50, MA100, MA200 (Simple & Exponential)
  - Summary: count of Buy vs Sell signals
- **Pivot Points**: Classic, Fibonacci, Camarilla, Woodie's, DeMark's (S1, S2, S3, P, R1, R2, R3)

**How to Extract Data**:

1. Navigate to the ETF main page using `/playwright`
2. Scroll to "Technical Analysis" section or click Technical tab
3. **Expand/capture the Technical Indicators table** - this contains individual indicator values
4. **Expand/capture the Moving Averages table** - shows all MA values
5. **Record these specific values** (copy-paste or screenshot):
   - RSI(14) exact value (e.g., 42.211)
   - MACD exact value (e.g., -0.370)
   - ATR(14) for volatility calculation
   - Daily and Weekly summary signals

**How to Use Technical Data for eDCA**:

- **RSI-Adjusted Strategy**: Use RSI(14) value directly
  - RSI < 30: multiplier = 2.0x (oversold, buy aggressively)
  - RSI 30-50: multiplier = 1.5x (tending toward oversold)
  - RSI 50-70: multiplier = 1.0x (neutral zone)
  - RSI > 70: multiplier = 0.5x (overbought, buy conservatively)
- **Volatility-Based Strategy**: Use ATR(14) value
  - High ATR = high volatility = increase investment (opportunity)
  - Low ATR = low volatility = standard investment
- **Momentum Strategy**: Use MACD and Moving Averages
  - MACD > 0 + price > MA50 = uptrend = increase investment
  - MACD < 0 + price < MA50 = downtrend = decrease investment
- **Multi-Factor**: Combine RSI (60% weight) + MACD (40% weight) for hybrid multiplier

### Thai Baht Exchange Rate (THB/USD)

For Thai investors, use Kasikornbank (KBank) for accurate exchange rates:

**Kasikornbank Foreign Exchange Rates**:

- URL: `https://www.kasikornbank.com/en/rate/pages/foreign-exchange.aspx`
- Use `/playwright` to navigate and capture:
  - USD/THB buying rate (TT)
  - USD/THB selling rate (TT)
  - Telegraphic Transfer (TT) rates for investment calculations
- **Note**: Bank rates are more reliable than crypto/USDT rates for THB conversions
- Update rate for each report generation (rates change daily)

**Alternative Banks**:

- Bangkok Bank: `https://www.bangkokbank.com/en/personal/other-services/foreign-exchange-rates`
- SCB: `https://www.scb.co.th/en/personal-banking/foreign-exchange-rates.html`

### Alternative Technical Analysis Sources

- **TradingView**: `https://www.tradingview.com/symbols/{EXCHANGE}-{TICKER}/`
- **TipRanks**: `https://www.tipranks.com/etf/{ticker}`
- **Yahoo Finance**: `https://finance.yahoo.com/quote/{TICKER}/technical` (limited indicators)

## Learning & Feedback Loop (Continuous Improvement)

The agent can learn from historical reports stored in `./report/` to improve future eDCA analysis accuracy.

### How to Use Past Reports for Learning

When generating a new report, agent SHOULD:

1. Check `./report/` directory for previous reports
2. Read 1-3 most recent reports to understand:
   - Previous recommendations and multipliers used
   - Market conditions from prior periods
   - Accuracy of past predictions
   - Portfolio changes over time

### What to Track in Reports for Learning

Each report should include a **Learning Metadata** section at the end:

```markdown
## Learning Metadata (สำหรับ Agent เรียนรู้)

### การตัดสินใจครั้งนี้ (This Report Decisions)

| สินทรัพย์ | RSI   | MACD   | Multiplier | จำนวนเงิน | เหตุผลหลัก           |
| --------- | ----- | ------ | ---------- | --------- | -------------------- |
| SMH       | 58.25 | +12.45 | 1.2x       | $340      | ใกล้จุดสูงสุด, ระวัง |
| QQQM      | 42.21 | -0.37  | 1.4x       | $614      | RSI ใกล้ oversold    |

### สภาวะตลาด (Market Conditions)

- VIX: 18.81 (สูงกว่าปกติ)
- แนวโน้ม sector: Tech แข็งแกร่ง
- ข่าวสำคัญ: NVDA Groq deal, AI demand growth

### ความมั่นใจ (Confidence Level)

- SMH: 75% (ติดตามระดับราคาใกล้สูงสุด)
- QQQM: 85% (RSI ต่ำ แนวโน้มชัดเจน)

### บทเรียนจากรายงานก่อน (Lessons from Previous Reports)

- [รายงานครั้งก่อน] แนะนำ: ...
- ผลที่เกิดขึ้น: ...
- ปรับปรุงครั้งนี้: ...
```

### Learning Triggers (เมื่อไหร่ควรเรียนรู้)

**Review Previous Reports When:**

1. **New analysis requested** - Always check past 1-3 reports
2. **Same asset showing similar RSI levels** - Compare with previous recommendations
3. **Market conditions changed significantly** - Learn what worked in similar conditions
4. **User asks for strategy review** - Analyze accuracy of past predictions

**Specific Learning Opportunities:**

- RSI < 30 (oversold) → Check if previous oversold signals were profitable
- RSI > 70 (overbought) → Check if reducing investment at highs was correct
- High volatility periods → Learn which multipliers work best
- Sector rotation → Understand correlation patterns

### Continuous Improvement Process

```
1. READ previous reports from ./report/
2. COMPARE current market conditions with historical patterns
3. IDENTIFY what worked/didn't work in past recommendations
4. ADJUST multipliers based on historical accuracy
5. DOCUMENT rationale for future learning
6. GENERATE new report with improved recommendations
```

### Feedback Loop Questions (Ask When Analyzing)

**Before Making Recommendation:**

- "What did I recommend last time RSI was around [current value]?"
- "How did that recommendation perform?"
- "Should I adjust the multiplier based on past results?"

**After Market Movement (Next Report):**

- "Did the previous multiplier recommendation work well?"
- "Should I increase/decrease confidence in RSI signals?"
- "What market factor did I miss last time?"

### Report Naming for Easy Retrieval

**Current format**: `YYYY-MM-DD-HH:MM:SS.md`
**Alternative with context**: `YYYY-MM-DD-{strategy}-{market-condition}.md`

Example:

- `2026-02-02-rsi-adjusted-bull.md`
- `2026-02-02-volatility-based-correction.md`

### Meta-Learning (Learning About Learning)

Track these metrics over time:

- **Recommendation accuracy rate**: % of profitable recommendations
- **Multiplier effectiveness**: Which multiplier ranges work best per asset
- **Indicator reliability**: Which technical indicators predict best for each asset
- **Market regime performance**: How does eDCA perform in bull/bear/sideways markets

### Example Learning Scenario

**Scenario**: User asks for QQQM analysis, current RSI = 42

**Agent Learning Process**:

1. Check `./report/` for past QQQM recommendations
2. Find report from 2026-01-15: QQQM RSI = 40, recommended 1.5x
3. Find report from 2026-01-25: QQQM RSI = 45, recommended 1.3x
4. Check current prices vs those reports
5. Learn: "RSI 40-45 range with 1.3-1.5x worked well"
6. Apply: Recommend 1.4x for current RSI 42 (interpolated)

## Analysis Frequency (ความถี่ในการวิเคราะห์)

### ความถี่ที่แนะนำ (Recommended Frequency)

| ระดับ               | ความถี่       | เหมาะกับ                 | ใช้เมื่อ                   |
| ------------------- | ------------- | ------------------------ | -------------------------- |
| **🔴 สูงสุด**       | รายวัน        | Day traders, ระยะสั้นมาก | ตลาดผันผวนรุนแรง           |
| **🟠 สูง**          | รายสัปดาห์    | Active investors         | DCA รายสัปดาห์, ตลาดผันผวน |
| **🟡 ปานกลาง**      | ราย 2 สัปดาห์ | Most investors           | ค่าเริ่มต้นที่ดี           |
| **🟢 มาตรฐาน**      | รายเดือน      | Long-term investors      | DCA รายเดือน (แนะนำ)       |
| **🔵 ต่ำ**          | ราย 2-3 เดือน | Passive investors        | ตลาดทรงตัว                 |
| **⚪ ตามเหตุการณ์** | Ad-hoc        | ทุกคน                    | เหตุการณ์สำคัญ             |

### แนะนำสำหรับผู้ใช้ทั่วไป: **รายเดือน (Monthly)** 🟢

**เหตุผล**:

- DCA ส่วนใหญ่เป็นรายเดือน (สอดคล้องกับเงินเดือน)
- Technical indicators รายวันมี noise มาก (สัญญาณ false สูง)
- รายสัปดาห์อาจบ่อยเกินไป - เปลืองเวลาและค่าธรรมเนียม
- รายเดือนให้ภาพรวมที่ชัดเจนพอสำหรับการตัดสินใจ

**กำหนดเวลา**: วันที่ 1-5 ของเดือน (หลังเงินเดือนออก)

### Trigger Events (เหตุการณ์ที่ควรวิเคราะห์ทันที)

วิเคราะห์เพิ่มเติมเมื่อเกิดเหตุการณ์เหล่านี้:

#### 🚨 **เหตุการณ์สำคัญ (Analyze Immediately)**

- VIX พุ่งสูงกว่า 30 (ความผันผวนสูง)
- ข่าวใหญ่ sector (เช่น NVDA earnings, Fed meeting)
- ตลาดลงมากกว่า 5% ในวันเดียว
- RSI < 25 หรือ RSI > 75 (extreme levels)
- Portfolio ลงมากกว่า 10% จากจุดสูงสุด

#### ⚠️ **เหตุการณ์ปานกลาง (Analyze within 1-3 days)**

- Earnings season สำคัญ
- Economic data releases (CPI, GDP, unemployment)
- Sector rotation ชัดเจน
- Breakout/breakdown ทางเทคนิค

#### ℹ️ **เหตุการณ์ทั่วไป (Include in next scheduled analysis)**

- ข่าวทั่วไป
- การปรับลด/ขึ้นอัตราดอกเบี้ยที่คาดการณ์แล้ว
- รายงานทั่วไป

### บัญชีผู้ใช้ตามสไตล์ (User Profiles)

**1. 👨‍💼 นักลงทุนผู้รอบรอบ (Conservative)**

- ความถี่: ราย 2 เดือน
- Focus: Long-term trend (Weekly/Monthly)
- ซื้อเมื่อ: RSI < 40, แนวโน้มแข็งแกร่ง

**2. 🎯 นักลงทุนสมดุล (Balanced) - Recommended**

- ความถี่: รายเดือน
- Focus: Daily + Weekly สมดุล
- ซื้อเมื่อ: RSI 35-45 (near oversold)

**3. ⚡ นักลงทุนกระตือรือร้น (Aggressive)**

- ความถี่: ราย 2 สัปดาห์
- Focus: Daily signals + short-term opportunities
- ซื้อเมื่อ: ใช้ทุกโอกาสที่ RSI < 50

**4. 🎮 Active Trader**

- ความถี่: รายสัปดาห์
- Focus: All timeframes + volatility
- ซื้อเมื่อ: ใช้ทุก technical signal

### การปรับความถี่ตามสภาวะตลาด

```
สภาวะตลาด          ความถี่ที่แนะนำ      เหตุผล
-----------------  ------------------  ---------------------------
Bull Market        ราย 2 เดือน         ไม่ต้องวิเคราะห์บ่อย
Sideways/Volatile  ราย 2-3 สัปดาห์     โอกาสเข้าซื้อบ่อย
Bear Market        รายสัปดาห์          ติดตามจุดตกต่ำ
Crash/Correction   รายวัน/สัปดาห์      จับจังหวะ dip
New Holdings       ราย 2 สัปดาห์       ติดตาม entry ใหม่
Stable Portfolio   รายเดือน            ค่าเริ่มต้นที่ดี
```

### ตัวอย่างกำหนดการ (Sample Schedule)

**สำหรับ DCA รายเดือน 30,000 บาท**:

```
วันที่ 1-5 ของเดือน: วิเคราะห์และสร้างรายงาน
วันที่ 5-10: ดำเนินการซื้อตามแผน
วันที่ 15: ตรวจสอบราคา (quick check ไม่ต้องสร้างรายงาน)
วันที่ 25: วางแผนเดือนถัดไป (เบื้องต้น)
```

### คำถามช่วยตัดสินใจ (Decision Framework)

**ถามตัวเองก่อนวิเคราะห์**:

1. มีเงินสำหรับ DCA ในงวดนี้หรือยัง?
2. มีเหตุการณ์สำคัญที่เปลี่ยนแปลงตลาดหรือไม่?
3. ครั้งก่อนวิเคราะห์เมื่อไหร่? (น้อยกว่า 2 สัปดาห์ อาจไม่จำเป็น)
4. Technical indicators เปลี่ยนแปลงมากกว่า 10% หรือไม่?
5. มีข่าวสำคัญรออยู่ใน 1 สัปดาห์นี้หรือไม่?

**ถ้าตอบ "ใช่" อย่างน้อย 2 ข้อ → วิเคราะห์ได้**

### หยุดวิเคราะห์บ่อยเกินไป (Over-analysis Warning)

⚠️ **Warning Signs**:

- วิเคราะห์บ่อยกว่าซื้อ (วิเคราะห์รายสัปดาห์ แต่ซื้อรายเดือน)
- เปลี่ยนแผนบ่อยจากการวิเคราะห์ใหม่
- Analysis paralysis (ไม่ตัดสินใจเพราะวิเคราะห์มากเกิน)

✅ **แก้ไข**:

- กำหนดวันวิเคราะห์ล่วงหน้า
- ใช้ DCA mechanical มากกว่า timing
- วิเคราะห์เพื่อยืนยัน ไม่ใช่หาจุดที่ดีที่สุด (perfect entry)

## References

- `references/dca-metrics.md`: Standard DCA calculation formulas
- `references/edca-strategies.md`: Enhanced DCA strategy details and formulas
- `references/risk-metrics.md`: Advanced risk calculations (VaR, drawdown)
- `references/example-report.md`: Sample Thai DCA report with full structure (Executive Summary, Technical Analysis, Learning Metadata)
- `./report/*.md`: Historical reports for learning (previous analyses)

## Notes

- **Informational only**: This skill provides analysis, not investment advice.
- **Quote sources**: Always cite URLs, timestamps, and indicator values.
- **eDCA assumptions**: When technical indicators are unavailable, fall back to standard DCA with a note.
- **Risk disclosure**: Include warnings about strategy limitations and market unpredictability.
- **Backtest disclaimer**: Scenario projections are hypothetical, not guarantees.
