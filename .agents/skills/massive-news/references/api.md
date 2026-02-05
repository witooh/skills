# Massive News API Reference

## Official Python Client

```bash
pip install massive
```

GitHub: https://github.com/massive-com/client-python

## list_ticker_news() Method

```python
from massive import RESTClient

client = RESTClient()  # Uses MASSIVE_API_KEY env var

news = client.list_ticker_news(
    ticker="AAPL",           # Stock symbol
    published_utc_gte=None,  # From date (YYYY-MM-DD)
    published_utc_lte=None,  # To date (YYYY-MM-DD)
    limit=10,                # Results per page (1-1000)
    order="desc",            # Sort order (asc/desc)
)

for article in news:
    print(article.title)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `ticker` | str | Stock/ETF symbol |
| `published_utc_gte` | str | Articles from date (YYYY-MM-DD) |
| `published_utc_lte` | str | Articles until date (YYYY-MM-DD) |
| `limit` | int | Results count (1-1000, default: 10) |
| `order` | str | Sort order: `asc`, `desc` |

## TickerNews Model

```python
class TickerNews:
    id: str                    # Unique article ID
    title: str                 # Article headline
    author: str                # Author name
    published_utc: str         # Publication timestamp (RFC3339)
    description: str           # Article summary
    article_url: str           # Link to original article
    image_url: str             # Article image URL
    amp_url: str               # Mobile AMP URL
    tickers: List[str]         # Related stock symbols
    keywords: List[str]        # Article keywords
    publisher: Publisher       # Publisher info
    insights: List[Insight]    # Sentiment analysis
```

## Insight Model (Sentiment)

```python
class Insight:
    ticker: str                # Related ticker
    sentiment: str             # "positive", "negative", "neutral"
    sentiment_reasoning: str   # Explanation
```

## Plan Access

| Plan | Recency | History |
|------|---------|---------|
| Stocks Basic | Hourly | 2 years |
| Stocks Starter+ | Hourly | All history |
