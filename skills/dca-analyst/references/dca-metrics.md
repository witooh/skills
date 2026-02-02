# DCA Metrics Reference

Use this reference to calculate metrics consistently when analyzing DCA portfolios. Compute only what inputs support.

## Inputs

- **Fixed Investment Amount**: contribution per interval
- **Frequency**: weekly / bi-weekly / monthly / quarterly
- **Horizon**: start date → end date
- **Price Series**: at least current price, optional historical prices
- **Total Units**: current units accumulated (if known)
- **Average Cost**: weighted average purchase price (if provided)
- **Fees** (optional): per-transaction or percentage

## Core Formulas

### Total Invested

```
total_invested = contribution_amount × number_of_contributions
```

If a contribution history exists, sum each contribution instead.

### Current Value

```
current_value = total_units × current_price
```

### Average Cost Basis

```
average_cost = total_invested / total_units
```

Use provided average cost if user supplies it; do not recompute unless full data is available.

### Unrealized P/L

```
unrealized_pl = current_value - total_invested
unrealized_pl_percent = (unrealized_pl / total_invested) × 100
```

### Break-even Price

```
break_even = total_invested / total_units
```

## Optional Metrics (Only if data supports it)

### DCA vs Lump Sum

```
dca_vs_lump_sum = (dca_return - lump_sum_return)
```

Requires a single purchase price at start date and comparable holdings.

### CAGR (Annualized Return)

```
cagr = (current_value / total_invested)^(1/years) - 1
```

### Max Drawdown

Compute from historical portfolio value series. Requires price history.

### Volatility

Compute from periodic returns if historical prices exist.

### Sharpe Ratio

```
sharpe = (portfolio_return - risk_free_rate) / portfolio_std_dev
```

Requires risk-free rate and volatility.

## Enhanced DCA (eDCA) Metrics

### Strategy Multiplier Calculation

**RSI-Adjusted Multiplier**:
```
if RSI <= 30: multiplier = max_mult (e.g., 2.0)
if RSI >= 70: multiplier = min_mult (e.g., 0.5)
if 30 < RSI < 70:
    multiplier = 1.0 + ((50 - RSI) / 20) × (max_mult - 1.0)
multiplier = clamp(multiplier, min_mult, max_mult)
```

**Volatility-Adjusted Multiplier**:
```
vol_z = (current_vol - avg_vol) / std_vol
multiplier = 1.0 + (vol_z × sensitivity)
multiplier = clamp(multiplier, min_mult, max_mult)
```

### eDCA Investment Amount

```
investment_amount = base_amount × multiplier
```

### eDCA Cost Basis Improvement

```
# Compare to standard DCA
standard_avg_cost = total_invested_standard / total_units_standard
edca_avg_cost = total_invested_edca / total_units_edca
cost_improvement = ((standard_avg_cost - edca_avg_cost) / standard_avg_cost) × 100
```

### Value Averaging Gap

```
target_value = base_amount × period_number
current_value = units_held × current_price
gap = target_value - current_value
investment = base_amount + gap
```

### eDCA Efficiency Ratio

```
# How much better is eDCA vs standard
edca_units = sum(edca_periodic_investments / prices)
standard_units = sum(standard_amount / prices)
efficiency_ratio = edca_units / standard_units
```

**Interpretation**:
- Ratio > 1.0: eDCA acquired more units (better)
- Ratio = 1.0: Same as standard DCA
- Ratio < 1.0: eDCA acquired fewer units (worse)

### Scenario Analysis

**Bull Case Projection**:
```
bull_price = current_price × 1.20
bull_units = current_units + (future_investment_bull / bull_price)
bull_value = bull_units × bull_price
```

**Bear Case Projection**:
```
bear_price = current_price × 0.80
bear_units = current_units + (future_investment_bear / bear_price)
bear_value = bear_units × bear_price
```

**Base Case Projection**:
```
base_price = current_price × (1 + expected_growth_rate)^years
base_units = current_units + (future_investment_base / avg_future_price)
base_value = base_units × base_price
```

### eDCA Stress Metrics

**Maximum Multiplier Hit**:
```
max_multiplier_used = max(historical_multipliers)
frequency_of_max = count(multiplier == max_multiplier) / total_periods
```

**Cash Utilization**:
```
target_total_investment = base_amount × periods
actual_total_investment = sum(investment_amounts)
cash_utilization = actual_total_investment / target_total_investment
```

**Opportunity Miss Rate**:
```
# Periods when strategy suggested buying but user didn't
missed_opportunities = count(signal_buy ∧ no_investment)
opportunity_miss_rate = missed_opportunities / total_buy_signals
```

## Data Gaps Handling

- If units are unknown → skip current value and P/L.
- If contribution history is unknown → estimate contributions using plan + horizon and flag assumption.
- If historical prices are missing → skip drawdown/volatility/CAGR comparisons.
- If RSI/volatility/MA data unavailable → fall back to standard DCA with note.
- If no strategy parameters provided → use default multiplier range 0.5x - 2.0x.

## Reporting Notes

- Always list which metrics were computed and which were skipped.
- Provide assumptions explicitly in the report.
- For eDCA, report both "What was recommended" and "What was executed" separately.
- Include confidence level for technical indicator-based calculations.
- Note behavioral adherence: did user actually follow the strategy signals?
