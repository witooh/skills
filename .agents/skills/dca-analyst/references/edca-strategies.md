# Enhanced DCA (eDCA) Strategies Reference

Advanced DCA strategies that dynamically adjust investment amounts based on market conditions. Use when users want to optimize their cost basis beyond standard fixed-amount investing.

## Strategy Selection Guide

| Strategy | Best For | Data Requirements | Complexity |
|----------|----------|-------------------|------------|
| Standard DCA | Beginners, simplicity | None | Low |
| Value Averaging | Mean reversion believers | Target trajectory calc | Medium |
| RSI-Adjusted | Technical traders | RSI values (14-day) | Medium |
| Volatility-Based | Risk managers | Historical volatility (30d) | High |
| Momentum-Based | Trend followers | Moving averages (50d) | Medium |

## 1. Standard DCA (Baseline)

### Formula
```
investment_amount = base_amount
multiplier = 1.0 (constant)
```

### Characteristics
- Fixed dollar amount at fixed intervals
- No decision-making required
- Reduces timing risk through mechanical investing

## 2. Value Averaging (VA)

### Concept
Maintain a predetermined portfolio value trajectory. Buy more when under target, buy less (or sell) when over target.

### Formula
```
# Target value at period t
target_value(t) = base_amount × t

# Current portfolio value
current_value = units_held × current_price

# Value gap
gap = target_value - current_value

# Investment amount
investment = base_amount + gap

# Apply constraints
investment = clamp(investment, min_investment, max_investment)
```

### Example
```
Month 3, base $500/month:
- Target value: $500 × 3 = $1,500
- Current value: $1,200 (market dropped)
- Gap: $1,500 - $1,200 = $300
- Investment: $500 + $300 = $800 (buy more)

Month 6, base $500/month:
- Target value: $500 × 6 = $3,000
- Current value: $3,500 (market rallied)
- Gap: $3,000 - $3,500 = -$500
- Investment: $500 - $500 = $0 (skip buying)
```

### Constraints (Critical)
- **Min Investment**: 0 or positive floor (e.g., $100)
- **Max Investment**: Cap to avoid extreme contributions (e.g., 3x base)
- **No Selling in Accumulation Phase**: Set min to 0 if user doesn't want to sell

## 3. RSI-Adjusted DCA

### Concept
Increase investment when RSI indicates oversold conditions (< 30), decrease when overbought (> 70).

### Formula
```
# RSI thresholds (standard)
oversold = 30
overbought = 70
midpoint = 50

# Calculate multiplier
if RSI <= oversold:
    multiplier = max_multiplier
elif RSI >= overbought:
    multiplier = min_multiplier
else:
    # Linear interpolation between thresholds
    ratio = (midpoint - RSI) / (midpoint - oversold)
    multiplier = 1.0 + ratio × (max_multiplier - 1.0)

# Clamp to bounds
multiplier = clamp(multiplier, min_multiplier, max_multiplier)

# Final investment
investment = base_amount × multiplier
```

### Example
```
Base $500, range 0.5x - 2.0x:

RSI = 25 (oversold):
  multiplier = 2.0
  investment = $500 × 2.0 = $1,000 (buy aggressively)

RSI = 50 (neutral):
  multiplier = 1.0
  investment = $500 × 1.0 = $500 (standard amount)

RSI = 75 (overbought):
  multiplier = 0.5
  investment = $500 × 0.5 = $250 (buy conservatively)
```

### RSI Calculation (if not provided by source)
```
RSI = 100 - (100 / (1 + RS))
where:
  RS = Average Gain / Average Loss (over 14 periods)
```

### Considerations
- Use 14-day RSI as default
- Adjust thresholds for different asset classes (crypto may need wider ranges)
- Combine with trend filter: only apply if 50-day MA confirms oversold

## 4. Volatility-Based DCA

### Concept
Increase investment during high volatility periods (potential mean reversion opportunities), decrease during calm markets.

### Formula
```
# Calculate volatility metrics (30-day rolling)
current_vol = std_dev(returns_last_30d)
historical_avg_vol = avg(volatility_last_1year)
historical_std_vol = std_dev(volatility_last_1year)

# Z-score of current volatility
volatility_z = (current_vol - historical_avg_vol) / historical_std_vol

# Base multiplier adjustment
base_sensitivity = 0.3  # Adjust based on risk tolerance
multiplier = 1.0 + (volatility_z × base_sensitivity)

# Apply bounds
multiplier = clamp(multiplier, min_multiplier, max_multiplier)

# Final investment
investment = base_amount × multiplier
```

### Volatility Regime Multipliers
```
Very Low Vol (z < -1): 0.7x (market complacent)
Low Vol (z < -0.5): 0.85x
Normal Vol (-0.5 to 0.5): 1.0x
High Vol (z > 0.5): 1.3x
Very High Vol (z > 1): 1.6x (opportunity)
Extreme Vol (z > 2): 2.0x (max position)
```

### Risk Controls
- Cap max investment during extreme volatility (avoid catching falling knife)
- Require confirmation from other indicators (RSI, volume)
- Reduce position size if consecutive high-vol periods

## 5. Momentum-Based DCA

### Concept
Trend-following approach: increase investment during uptrends, decrease during downtrends. Opposite philosophy to mean reversion.

### Formula
```
# Price vs Moving Average
price_vs_ma50 = (current_price - MA50) / MA50

# Convert to multiplier
momentum_threshold = 0.05  # 5% deviation triggers adjustment

if price_vs_ma50 > momentum_threshold:
    # Uptrend - increase position
    trend_strength = min(price_vs_ma50 / 0.10, 1.0)  # Cap at 10% deviation
    multiplier = 1.0 + (trend_strength × (max_multiplier - 1.0))
elif price_vs_ma50 < -momentum_threshold:
    # Downtrend - decrease position
    trend_strength = min(abs(price_vs_ma50) / 0.10, 1.0)
    multiplier = 1.0 - (trend_strength × (1.0 - min_multiplier))
else:
    # Neutral - standard amount
    multiplier = 1.0

investment = base_amount × clamp(multiplier, min_multiplier, max_multiplier)
```

### Alternative: Dual MA System
```
if price > MA50 > MA200:  # Golden cross, strong uptrend
    multiplier = max_multiplier
elif price > MA50:  # Short-term uptrend
    multiplier = 1.0 + (max_multiplier - 1.0) × 0.5
elif price < MA50 < MA200:  # Death cross, strong downtrend
    multiplier = min_multiplier
elif price < MA50:  # Short-term downtrend
    multiplier = 1.0 - (1.0 - min_multiplier) × 0.5
else:
    multiplier = 1.0
```

## Hybrid Strategies

### RSI + Volatility Combo
```
# Weight factors
rsi_weight = 0.6
vol_weight = 0.4

# Calculate component multipliers
rsi_mult = calculate_rsi_multiplier(RSI)
vol_mult = calculate_volatility_multiplier(volatility_z)

# Combine
combined_multiplier = (rsi_mult × rsi_weight) + (vol_mult × vol_weight)
multiplier = clamp(combined_multiplier, min_mult, max_mult)
```

### Trend + Mean Reversion Filter
```
# Only apply mean reversion (RSI/VA) if trend confirms
if MA50_slope > 0:  # Uptrend
    use_mean_reversion = True  # Buy dips in uptrend
else:
    use_mean_reversion = False  # Avoid catching falling knife
    multiplier = min_multiplier  # Reduce exposure
```

## Risk Management Rules

### Position Sizing Constraints
```
max_position_pct = 0.25  # No single asset > 25% of portfolio
max_monthly_increase = 2.5  # Max 2.5x base in any period
drawdown_cutoff = -0.30  # Stop buying if portfolio down >30%
```

### Circuit Breakers
- **Extreme RSI**: If RSI < 10 or RSI > 90, require manual confirmation
- **Consecutive oversold**: If RSI < 30 for 3+ periods, check for fundamental issues
- **Volatility spike**: If volatility > 3 standard deviations, cap multiplier at 1.5x

### Cash Reserve
```
maintain_cash_pct = 0.10  # Keep 10% uninvested for opportunities
if cash_level < target_cash:
    reduce_multiplier_by = 0.2  # Reduce new investments 20%
```

## Backtesting Guidelines

### Test Periods
- Minimum: 2 years of historical data
- Preferred: 5+ years covering multiple market cycles
- Include: Bull market, bear market, sideways periods

### Metrics to Track
1. **Cost Basis Improvement**: eDCA avg cost vs standard DCA
2. **Total Units Accumulated**: More units = better DCA
3. **Maximum Drawdown**: Worst peak-to-trough decline
4. **Sharpe Ratio**: Risk-adjusted returns
5. **Behavioral Adherence**: How often user actually followed signals

### Scenario Testing
```
Bull Market: Sustained +20%/year for 2 years
Bear Market: Sustained -20%/year for 1 year
Sideways: ±5% volatility with no trend
Crash Recovery: -30% then +50% over 18 months
```

## Implementation Notes

### Data Requirements by Strategy
| Strategy | Minimum History | Key Indicators | Update Frequency |
|----------|----------------|----------------|------------------|
| Standard | 1 day | Price | Monthly |
| Value Averaging | Full history | Portfolio value | Monthly |
| RSI-Adjusted | 14 days | RSI | Daily/Weekly |
| Volatility-Based | 30 days | Std dev, returns | Weekly |
| Momentum | 50 days | MA50, MA200 | Daily |

### Common Mistakes to Avoid
1. **No constraints**: Always set min/max multipliers
2. **Ignoring fees**: High-frequency adjustments increase costs
3. **Overfitting**: Strategy optimized for past may fail in future
4. **Behavior gap**: User ignores signals during extreme fear/greed
5. **Single indicator**: Combine 2-3 factors for robustness

### Recommended Starting Parameters
```json
{
  "strategy": "rsi_adjusted",
  "base_amount": 500,
  "min_multiplier": 0.5,
  "max_multiplier": 2.0,
  "rsi_oversold": 30,
  "rsi_overbought": 70,
  "max_position_pct": 0.25,
  "cash_reserve_pct": 0.10
}
```

## References

- Marshall, P.S. (2000). "A Statistical Comparison of Value Averaging vs. Dollar Cost Averaging"
- Kirkby et al. (2020). "An Analysis of Dollar Cost Averaging and Market Timing Investment Strategies"
- Dunham & Friesen (2011). "Building a Better Mousetrap: Enhanced Dollar Cost Averaging"
