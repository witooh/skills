---
name: massive-news
description: Fetch stock and ETF news from Massive API using official Python client. Includes sentiment analysis. Use when users ask for stock news, market news, ticker news, or financial news for specific symbols (e.g., "ดูข่าว AAPL", "news for TSLA", "ข่าว stock วันนี้").
---

# Massive News

Fetch latest news articles for stocks and ETFs from Massive API.

## Prerequisites

1. Install official client:
```bash
pip install massive
```

2. Set API key:
```bash
export MASSIVE_API_KEY="your-api-key"
```

## Quick Start

### Latest news for a ticker
```bash
python scripts/fetch_news.py AAPL
```

### More results
```bash
python scripts/fetch_news.py TSLA --limit 20
```

### Filter by date range
```bash
python scripts/fetch_news.py GOOGL --from 2024-01-01 --to 2024-01-31
```

### Raw JSON output
```bash
python scripts/fetch_news.py MSFT --json
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ticker` | Stock/ETF symbol (required) | - |
| `--limit` | Number of results (1-1000) | 10 |
| `--from` | Start date (YYYY-MM-DD) | - |
| `--to` | End date (YYYY-MM-DD) | - |
| `--order` | Sort order (asc/desc) | desc |
| `--json` | Output as JSON | false |

## Using Python Directly

```python
from massive import RESTClient

client = RESTClient()  # Uses MASSIVE_API_KEY env var

# Latest 10 news for AAPL
for news in client.list_ticker_news("AAPL", limit=10, order="desc"):
    print(f"{news.published_utc}: {news.title}")
    if news.insights:
        print(f"  Sentiment: {news.insights[0].sentiment}")

# With date filter
for news in client.list_ticker_news(
    "TSLA",
    published_utc_gte="2024-01-01",
    published_utc_lte="2024-01-31"
):
    print(news.title)
```

## Response Fields

Each article includes:
- **title**: Article headline
- **author**: Article author
- **published_utc**: Publication timestamp
- **description**: Article summary
- **article_url**: Link to full article
- **tickers**: Related stock symbols
- **insights**: Sentiment analysis (positive/negative/neutral)

## API Reference

See [references/api.md](references/api.md) for complete API documentation.
