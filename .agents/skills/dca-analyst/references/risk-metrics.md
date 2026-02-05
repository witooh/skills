# Risk Metrics Reference

Advanced risk calculations for portfolio analysis. Use when analyzing Enhanced DCA (eDCA) strategies or providing risk-adjusted performance metrics.

## Core Risk Metrics

### 1. Value at Risk (VaR)

**Definition**: Maximum expected loss at a given confidence level over a specific time period.

**Formula (Historical VaR)**:
```
VaR_95 = percentile(historical_returns, 5)  # 5th percentile = 95% confidence
VaR_99 = percentile(historical_returns, 1)  # 1st percentile = 99% confidence
```

**Interpretation**:
- "95% VaR of -$500" means: 95% of the time, losses won't exceed $500
- Tail risk: 5% of the time, losses could exceed $500

**Calculation Steps**:
1. Get daily returns series: `return_t = (price_t - price_t-1) / price_t-1`
2. Sort returns from worst to best
3. Find the return at the percentile threshold (e.g., 5th percentile)
4. Apply to portfolio value: `VaR_amount = portfolio_value × VaR_return`

**Example**:
```
Portfolio value: $10,000
Daily returns (last 252 days): [...]
5th percentile return: -2.3%
95% Daily VaR = $10,000 × 0.023 = $230

Interpretation: On 95% of days, losses won't exceed $230
```

### 2. Conditional Value at Risk (CVaR) / Expected Shortfall

**Definition**: Expected loss when VaR threshold is breached (average of worst cases).

**Formula**:
```
CVaR_95 = average(returns below VaR_95 threshold)
```

**Use Case**: Better captures tail risk than VaR alone.

### 3. Maximum Drawdown (MDD)

**Definition**: Largest peak-to-trough decline in portfolio value.

**Formula**:
```
running_max = cumulative_max(portfolio_values)
drawdown = (portfolio_value - running_max) / running_max
MDD = min(drawdown)  # Most negative value
```

**Calculation Steps**:
1. Calculate running maximum value at each point
2. Compute drawdown at each point: `(current - running_max) / running_max`
3. Find minimum (worst) drawdown

**Example**:
```
Portfolio values: [100, 120, 90, 110, 130]
Running max: [100, 120, 120, 120, 130]
Drawdowns: [0%, 0%, -25%, -8.3%, 0%]
MDD = -25%
```

### 4. Calmar Ratio

**Definition**: Return per unit of maximum drawdown risk.

**Formula**:
```
Calmar = Annualized_Return / |MDD|
```

**Interpretation**: Higher is better. >1.0 is generally good.

### 5. Sortino Ratio

**Definition**: Return per unit of downside risk (only considers negative volatility).

**Formula**:
```
downside_returns = [r for r in returns if r < 0]
downside_std = std_dev(downside_returns)
Sortino = (Annualized_Return - Risk_Free_Rate) / downside_std
```

**vs Sharpe Ratio**:
- Sharpe: Total risk (upside + downside)
- Sortino: Only downside risk (more relevant for investors)

### 6. Ulcer Index

**Definition**: Measure of depth and duration of drawdowns (investor stress indicator).

**Formula**:
```
UI = sqrt(mean(drawdown^2))
```

**Interpretation**: Lower is better. Measures both how bad and how long drawdowns last.

### 7. Beta (Market Correlation)

**Definition**: Sensitivity to market movements.

**Formula**:
```
Beta = Covariance(asset_returns, market_returns) / Variance(market_returns)
```

**Interpretation**:
- Beta = 1: Moves with market
- Beta > 1: More volatile than market
- Beta < 1: Less volatile than market
- Beta < 0: Inverse correlation (rare)

### 8. Volatility (Standard Deviation)

**Definition**: Dispersion of returns around mean.

**Formula**:
```
Volatility = std_dev(returns) × sqrt(trading_periods_per_year)

# For daily returns
Annualized_Vol = std_dev(daily_returns) × sqrt(252)

# For monthly returns
Annualized_Vol = std_dev(monthly_returns) × sqrt(12)
```

### 9. Tracking Error

**Definition**: Volatility of excess returns relative to benchmark.

**Formula**:
```
excess_returns = portfolio_returns - benchmark_returns
Tracking_Error = std_dev(excess_returns) × sqrt(252)
```

## Risk-Adjusted Return Metrics

### Sharpe Ratio
```
Sharpe = (Portfolio_Return - Risk_Free_Rate) / Portfolio_Volatility
```

### Information Ratio
```
Information_Ratio = (Portfolio_Return - Benchmark_Return) / Tracking_Error
```

### Treynor Ratio
```
Treynor = (Portfolio_Return - Risk_Free_Rate) / Beta
```

## eDCA-Specific Risk Considerations

### Strategy Risk Factors

| Strategy | Primary Risk | Mitigation |
|----------|--------------|------------|
| Standard DCA | Opportunity cost (miss dips) | None needed |
| Value Averaging | Over-investment in crashes | Max multiplier cap |
| RSI-Adjusted | False signals in trends | Trend confirmation filter |
| Volatility-Based | Buying into sustained volatility | Volatility regime check |
| Momentum | Late entry in trends | Dual MA confirmation |

### Behavioral Risk Metrics

**Adherence Score**:
```
planned_investments = [i1, i2, i3, ...]
actual_investments = [a1, a2, a3, ...]
adherence = correlation(planned, actual)
```

**Panic Selling Risk**:
```
if MDD > user_stated_pain_threshold:
    risk_level = "HIGH"
    recommendation = "Reduce position size"
```

## Stress Testing Scenarios

### 1. Black Swan Event
```
shock_return = -0.30  # 30% single period drop
portfolio_after_shock = portfolio_value × (1 + shock_return)
recovery_periods = calculate_recovery_time(history, shock_return)
```

### 2. Extended Bear Market
```
monthly_decline = -0.05  # 5% per month
months = 12
final_value = portfolio_value × (1 + monthly_decline)^months
```

### 3. Volatility Spike
```
normal_vol = 0.15  # 15% annualized
crisis_vol = 0.50  # 50% annualized
VaR_normal = calculate_VaR(returns, vol=normal_vol)
VaR_crisis = calculate_VaR(returns, vol=crisis_vol)
stress_impact = VaR_crisis / VaR_normal
```

## Reporting Risk Metrics

### Risk Dashboard Format
```
## Risk Analysis Summary
| Metric | Value | Interpretation |
|--------|-------|----------------|
| 95% VaR (Daily) | -$X | 95% confidence limit |
| Max Drawdown | -Y% | Worst peak-to-trough |
| Volatility | Z% | Annualized std dev |
| Sharpe Ratio | A | Risk-adjusted return |
| Sortino Ratio | B | Downside-adjusted return |
| Beta | C | Market sensitivity |

## Stress Test Results
| Scenario | Portfolio Impact | Recovery Time |
|----------|------------------|---------------|
| Black Swan (-30%) | -$X | Y months |
| Bear Market (12mo) | -Z% | N months |
| High Volatility | VaR increases by M% | - |

## Risk Warnings
- [ ] High concentration in single asset
- [ ] Maximum drawdown approaching user threshold
- [ ] Volatility regime shift detected
- [ ] Correlation breakdown risk
```

## Implementation Notes

### Data Requirements
- Minimum 30 days for basic VaR
- Minimum 1 year for reliable volatility estimates
- Minimum 3 years for maximum drawdown analysis

### Common Pitfalls
1. **Assuming normal distribution**: Returns have fat tails
2. **Static risk metrics**: Risk changes over time
3. **Ignoring correlation**: Assets don't move independently
4. **Overconfidence in backtests**: Past =/= future

### Risk-Free Rate Reference
- Use 3-month Treasury yield for USD
- Use comparable government securities for other currencies
- Typical default: 0.04 (4%) if no current data

## References

- Jorion, P. (2006). "Value at Risk: The New Benchmark for Managing Financial Risk"
- Bacon, C. (2008). "Practical Portfolio Performance Measurement and Attribution"
- CFA Institute. "Managing Investment Portfolios: A Dynamic Process"
