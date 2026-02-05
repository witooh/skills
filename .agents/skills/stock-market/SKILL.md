---
name: stock-market
description: Fetch real-time stock and ETF prices from global markets including US (NYSE, NASDAQ) and Thai SET. Use when user asks about stock prices, market data, ETF quotes, or wants to compare securities. Trigger phrases include "ราคาหุ้น", "stock price", "ETF quote", "ดูตลาด", "AAPL", "SET", "NASDAQ".
compatibility: opencode
metadata:
  author: witooh
  version: "1.0"
  api: Yahoo Finance
---

## Quick Start

```bash
# Install dependencies first
cd skills/stock-market && bun install

# Get current price
bun scripts/cli.ts get_price '{"symbol": "AAPL"}'

# Search for symbols
bun scripts/cli.ts search_symbol '{"query": "Apple"}'

# Get Thai SET stock (add .BK suffix)
bun scripts/cli.ts get_price '{"symbol": "PTT.BK"}'

# Get ETF price
bun scripts/cli.ts get_price '{"symbol": "QQQ"}'

# List all tools
bun scripts/cli.ts --list
```

## When to Use This Skill

- 📈 Check current stock prices (US, Thai SET, global)
- 📈 Get ETF quotes and market data
- 📈 Search for company symbols/tickers
- 📈 Compare multiple securities
- 📈 View market summary and trends

## Tools (5 total)

| Tool                  | Purpose                                                |
| --------------------- | ------------------------------------------------------ |
| `get_price`           | Get current price and key metrics for a symbol         |
| `get_multiple_prices` | Get prices for multiple symbols at once                |
| `search_symbol`       | Search for stock/ETF symbols by company name           |
| `get_market_summary`  | Get major indices summary (S&P 500, NASDAQ, SET, etc.) |
| `get_historical`      | Get historical price data for charting                 |

## Supported Markets

**US Markets:**

- NYSE: `IBM`, `JPM`, `DIS`
- NASDAQ: `AAPL`, `MSFT`, `GOOGL`, `TSLA`, `NVDA`
- ETFs: `SPY`, `QQQ`, `VTI`, `VOO`

**Thai SET:**

- Add `.BK` suffix: `PTT.BK`, `AOT.BK`, `SCB.BK`, `KBANK.BK`
- Without suffix auto-resolves if unique

**Other Markets:**

- Crypto: `BTC-USD`, `ETH-USD`
- International: `SHEL.L` (London), `7203.T` (Tokyo)

## Common Examples

**Thai Language:**

```
User: "ราคาหุ้น PTT"
→ bun scripts/cli.ts get_price '{"symbol": "PTT.BK"}'

User: "ดูราคา AOT"
→ bun scripts/cli.ts get_price '{"symbol": "AOT.BK"}'

User: "หุ้น Apple ราคาเท่าไร"
→ bun scripts/cli.ts get_price '{"symbol": "AAPL"}'

User: "เปรียบเทียบ TSLA NVDA"
→ bun scripts/cli.ts get_multiple_prices '{"symbols": ["TSLA", "NVDA"]}'

User: "ค้นหาหุ้น Amazon"
→ bun scripts/cli.ts search_symbol '{"query": "Amazon"}'

User: "สรุปตลาดวันนี้"
→ bun scripts/cli.ts get_market_summary
```

**English:**

```
User: "What's the price of SPY?"
→ bun scripts/cli.ts get_price '{"symbol": "SPY"}'

User: "Compare AAPL and MSFT"
→ bun scripts/cli.ts get_multiple_prices '{"symbols": ["AAPL", "MSFT"]}'

User: "Search for Tesla stock"
→ bun scripts/cli.ts search_symbol '{"query": "Tesla"}'
```

## Symbol Format Guide

**US Stocks:** Symbol only

- `AAPL` → Apple Inc.
- `MSFT` → Microsoft
- `TSLA` → Tesla

**Thai SET Stocks:** Add `.BK`

- `PTT.BK` → ปตท.
- `AOT.BK` → ท่าอากาศยานไทย
- `SCB.BK` → ธนาคารไทยพาณิชย์

**ETFs:** Standard symbols

- `SPY` → S&P 500 ETF
- `QQQ` → NASDAQ-100 ETF
- `VTI` → Total Stock Market ETF

**Crypto:** Add `-USD`

- `BTC-USD` → Bitcoin
- `ETH-USD` → Ethereum

## Output Format

All tools return JSON:

```json
{
  "success": true,
  "data": {
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "price": 185.92,
    "currency": "USD",
    "change": 2.15,
    "change_percent": 1.17,
    "market_time": "2024-01-15T16:00:00-05:00",
    "volume": 52438900,
    "market_cap": "2.89T"
  },
  "timestamp": "2024-01-15T10:00:00+07:00"
}
```

## Rate Limits

Yahoo Finance API (unofficial):

- ~2,000 requests/hour per IP
- No API key required
- Free for personal use

## Error Handling

Common errors:

- `"Symbol not found"` → Check spelling or use `search_symbol`
- `"Invalid symbol format"` → Thai stocks need `.BK` suffix
- `"Market closed"` → Returns last closing price

## Implementation Notes

- Uses Yahoo Finance unofficial API (free, no key required)
- Thai SET symbols require `.BK` suffix
- All prices in local market currency
- Timestamps in ISO 8601 format
