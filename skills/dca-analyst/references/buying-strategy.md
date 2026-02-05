# Buying Strategy & Price Levels Reference

Reference guide for calculating recommended buy price levels and execution strategies for DCA/eDCA plans.

## Recommended Buy Levels

### Price Level Calculation Methods

#### 1. Pivot Points Method (Recommended)

Use Pivot Points as the primary method for determining buy price levels.

**Classic Pivot Points Formula**:

```
Pivot (P) = (High + Low + Close) / 3
Support 1 (S1) = (2 × P) - High
Support 2 (S2) = P - (High - Low)
Support 3 (S3) = Low - 2 × (High - P)
Resistance 1 (R1) = (2 × P) - Low
Resistance 2 (R2) = P + (High - Low)
Resistance 3 (R3) = High + 2 × (P - Low)
```

**Usage**:

- **Buy Now (Level 1)**: Current price or near S1 when RSI signal is Buy
- **Add More (Level 2)**: When price drops to S2
- **Heavy Buy (Level 3)**: When price drops to S3 (excellent opportunity)
- **Stop Loss**: Approximately 3-5% below S3

#### 2. Fibonacci Retracement Method

**Key Levels**:

```
0% = Recent Swing High
23.6% = Minor pullback
38.2% = Normal pullback (S1 equivalent)
50.0% = Moderate correction (S2 equivalent)
61.8% = Deep correction (S3 equivalent, golden ratio)
78.6% = Major correction
100% = Full retracement
```

**Formula**:

```
Fib_Level = High - ((High - Low) × Fib_Percentage)

Example: High = $100, Low = $80
S1 (38.2%) = $100 - (($100-$80) × 0.382) = $92.36
S2 (50.0%) = $100 - (($100-$80) × 0.500) = $90.00
S3 (61.8%) = $100 - (($100-$80) × 0.618) = $87.64
```

#### 3. Moving Average Support Method

**Key MA Levels**:

```
MA20 = Short-term support (Level 1)
MA50 = Medium-term support (Level 2)
MA200 = Long-term support (Level 3)
```

**Condition Check**:

```
if price > MA20 > MA50 > MA200:
    # Uptrend - buy pullback to MA20
    Level_1 = MA20
    Level_2 = MA50
    Level_3 = MA200
elif price < MA20:
    # Potential correction - wait for MA support
    Level_1 = MA50
    Level_2 = MA200
    Level_3 = MA200 × 0.95  # 5% below MA200
```

#### 4. ATR-Based Levels (Volatility-Adjusted)

**Formula**:

```
ATR = Average True Range (14 periods)

Level_1 = Current_Price - (0.5 × ATR)
Level_2 = Current_Price - (1.0 × ATR)
Level_3 = Current_Price - (1.5 × ATR)
Stop_Loss = Current_Price - (2.0 × ATR)
```

**Example**:

```
Current Price = $100, ATR(14) = $5

Level_1 = $100 - ($5 × 0.5) = $97.50
Level_2 = $100 - ($5 × 1.0) = $95.00
Level_3 = $100 - ($5 × 1.5) = $92.50
Stop_Loss = $100 - ($5 × 2.0) = $90.00
```

### Hybrid Method (Combining Multiple Methods)

**Confluence Zones**:

```
# Find zones where multiple methods overlap
overlap_confidence = 0
if Pivot_S1 within 2% of Fib_38.2:
    overlap_confidence += 1
if Pivot_S1 within 2% of MA50:
    overlap_confidence += 1
if Fib_38.2 within 2% of MA50:
    overlap_confidence += 1

# If overlap >= 2 => Strong support zone
```

**Best Practice**:

1. Calculate Pivot Points (primary)
2. Check Fibonacci levels (confirmation)
3. Review MA levels (trend context)
4. Adjust with ATR (volatility adjustment)
5. Select zones with high confluence

---

## Buying Strategies

### 1. Tiered Entry Strategy

**Concept**: Divide investment budget into portions and buy at predetermined price levels.

**Standard Distribution**:

```
Total Budget: 100%

at Current Price: 40% (buy immediately based on RSI signal)
at S1: +30% (add when first support is reached)
at S2: +20% (add when second support is reached)
at S3: +10% (add when third support is reached - heavy averaging)
```

**Conservative Distribution**:

```
at Current Price: 25%
at S1: +25%
at S2: +25%
at S3: +25%
```

**Aggressive Distribution**:

```
at Current Price: 50%
at S1: +30%
at S2: +20%
at S3: 0% (budget exhausted earlier)
```

### 2. RSI-Tiered Strategy

**Adjust Distribution Based on RSI**:

```
if RSI < 30 (oversold):
    at Current: 60% (buy heavily immediately)
    at S1: +25%
    at S2: +15%
    multiplier_boost = 1.5x

elif RSI 30-50 (near oversold):
    at Current: 40%
    at S1: +30%
    at S2: +20%
    at S3: +10%
    multiplier_boost = 1.2x

elif RSI 50-70 (neutral):
    at Current: 30%
    at S1: +30%
    at S2: +25%
    at S3: +15%
    multiplier_boost = 1.0x

elif RSI > 70 (overbought):
    at Current: 0% (wait for pullback)
    at S1: +40%
    at S2: +35%
    at S3: +25%
    multiplier_boost = 0.5x
```

### 3. Volatility-Adjusted Strategy

**Adjust Buying Based on ATR**:

```
ATR_percentile = rank(current_ATR, historical_ATR_90d)

if ATR_percentile > 80 (high vol):
    # Spread entries wider
    Level_1 = Current - (1.0 × ATR)
    Level_2 = Current - (2.0 × ATR)
    Level_3 = Current - (3.0 × ATR)
    Buy smaller amounts: 30% / 30% / 25% / 15%

elif ATR_percentile < 20 (low vol):
    # Tighter entries
    Level_1 = Current - (0.3 × ATR)
    Level_2 = Current - (0.6 × ATR)
    Level_3 = Current - (0.9 × ATR)
    Buy larger amounts: 50% / 30% / 20%

else (normal vol):
    # Standard entries
    Level_1 = Current - (0.5 × ATR)
    Level_2 = Current - (1.0 × ATR)
    Level_3 = Current - (1.5 × ATR)
    Buy standard: 40% / 30% / 20% / 10%
```

### 4. Time-Based Strategy (for Long-term DCA)

**Weekly/Monthly Integration**:

```
# For monthly DCA
Week 1: Deploy 40% at market
Week 2: Set limit orders at S1 (30%)
Week 3: Adjust S2 order if S1 not filled
Week 4: Final sweep - buy remaining at market

Order expiry: End of DCA period
```

### 5. Momentum Filter Strategy

**Add Trend Conditions**:

```
# Only buy dips in uptrend
if MA50 > MA200 (uptrend):
    enable_all_buy_levels = True
    multiplier = calculated_multiplier

elif MA50 < MA200 (downtrend):
    # More cautious
    enable_level_1 = False  # Don't buy at current
    enable_level_2 = True   # Wait for S1
    enable_level_3 = True   # S2, S3 if it falls further
    multiplier = min(calculated_multiplier, 1.0)  # Cap at 1x

elif abs(MA50 - MA200) < 1% (consolidation):
    # Neutral, standard approach
    enable_all_buy_levels = True
    multiplier = 1.0
```

---

## Order Types & Execution

### Order Type Selection

| Level         | Order Type | Time in Force | Notes                     |
| ------------- | ---------- | ------------- | ------------------------- |
| Current Price | Market     | IOC           | Buy immediately on signal |
| S1            | Limit      | GTC           | Wait for price to drop    |
| S2            | Limit      | GTC           | Wait for deeper drop      |
| S3            | Limit      | GTC/GTD       | May set expiry date       |
| Stop Loss     | Stop-Limit | GTC           | Loss protection           |

### Execution Workflow

```
1. Technical Analysis:
   - Fetch RSI, MACD, MA, Pivot Points
   - Calculate eDCA multiplier

2. Determine Price Levels:
   - Calculate S1, S2, S3 from Pivot Points
   - Check confluence with Fib/MA

3. Budget Allocation:
   - Based on selected strategy (Tiered/RSI-based/Vol-based)
   - Adjust with multiplier

4. Create Buy Orders:
   - Market order: XX% of budget
   - Limit orders: at S1, S2, S3

5. Set Stop Loss:
   - Approximately 3-5% below S3
   - Or use ATR-based stop

6. Monitor and Adjust:
   - Review every 1-2 weeks
   - Cancel expired orders
   - Adjust levels if market changes
```

---

## Risk Management

### Position Sizing

```
max_position_single_asset = 25% of portfolio
max_buy_per_dca_period = 2.5x base_amount
```

### Stop Loss Calculation

**Method 1: Below S3**:

```
stop_loss = S3 × 0.95  # 5% below S3
```

**Method 2: ATR-based**:

```
stop_loss = entry_price - (2.0 × ATR)
```

**Method 3: Percentage-based**:

```
stop_loss = average_cost × 0.90  # 10% below avg cost
```

### Circuit Breakers

```
# Auto-stop buying when:
if portfolio_drawdown > 20%:
    pause_new_buys = True

if RSI < 15 (extreme oversold):
    require_manual_confirmation = True

if single_day_drop > 10%:
    use_min_multiplier = True
    wait_24h_before_buy = True
```

---

## Example Calculations

### Example 1: QQQM with RSI 42

**Given Data**:

```
Current Price: $210.50
RSI(14): 42 (near oversold)
ATR(14): $4.25
MA50: $215.00
MA200: $195.00

Pivot Points (Daily):
- P: $212.00
- S1: $208.50
- S2: $205.00
- S3: $201.50
```

**Calculation**:

```
Step 1: eDCA Multiplier
RSI = 42, threshold: oversold=30, neutral=50
multiplier = 1.0 + ((50-42)/20) × (2.0-1.0) = 1.4x

Step 2: Buy Levels
Level 1: $210.50 (current)
Level 2: $208.50 (S1)
Level 3: $205.00 (S2)
Stop Loss: $201.50 × 0.95 = $191.43

Step 3: Budget Allocation (base $500, mult 1.4x = $700)
at Current: 40% = $280
at S1: +30% = $210
at S2: +20% = $140
Reserve: +10% = $70
```

**Execution Plan**:

```
1. Market Order: Buy $280 immediately @ ~$210.50
2. Limit Order: $210 @ $208.50 (GTC)
3. Limit Order: $140 @ $205.00 (GTC)
4. Stop Loss: Set at $191.43
5. Reserve: $70 for S3 if price drops significantly
```

### Example 2: SMH with RSI 65 (Near Overbought)

**Given Data**:

```
Current Price: $285.00
RSI(14): 65 (near overbought)
ATR(14): $7.50
52-week high: $290.00

Pivot Points:
- P: $282.00
- S1: $275.00
- S2: $268.00
- S3: $261.00
```

**Calculation**:

```
Step 1: eDCA Multiplier
RSI = 65, near overbought
multiplier = 1.0 - ((65-50)/20) × (1.0-0.5) = 0.625x ≈ 0.7x

Step 2: Strategy Adjustment
Price near 52-week high → Be cautious
Don't buy at current price, wait for pullback

Step 3: Budget Allocation (base $500, mult 0.7x = $350)
at Current: 0% = $0 (wait for pullback)
at S1: +50% = $175
at S2: +35% = $122.50
at S3: +15% = $52.50
```

**Execution Plan**:

```
1. NO Market Order (RSI too high)
2. Limit Order: $175 @ $275.00
3. Limit Order: $122.50 @ $268.00
4. Limit Order: $52.50 @ $261.00
5. Stop Loss: Set at $248.00 (5% below S3)
```

---

## Data Requirements Checklist

To calculate buy price levels and strategies, the following data is required:

- [ ] Current Price
- [ ] RSI(14) - for multiplier calculation
- [ ] ATR(14) - for volatility adjustment
- [ ] Pivot Points (P, S1, S2, S3, R1, R2, R3)
- [ ] Moving Averages (MA20, MA50, MA200)
- [ ] 52-week High/Low
- [ ] DCA budget per period
- [ ] Exchange rate (THB/USD) for Thai investors

---

## References

- `dca-metrics.md`: DCA calculation formulas
- `edca-strategies.md`: Strategy multiplier calculations
- `risk-metrics.md`: Advanced risk calculations
