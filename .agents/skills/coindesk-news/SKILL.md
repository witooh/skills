---
name: coindesk-news
description: Fetch cryptocurrency news from CoinDesk Data API. Use when users ask for crypto news, Bitcoin/Ethereum updates, market sentiment analysis, or want to stay updated on cryptocurrency market movements. Supports filtering by coin (BTC, ETH, SOL, etc.), sentiment (positive/negative/neutral), and news sources.
---

# CoinDesk News

Fetch cryptocurrency news from CoinDesk Data API. No API key required.

## Quick Start

```bash
# Fetch latest 10 crypto news articles
python scripts/fetch_news.py

# Fetch Bitcoin-specific news
python scripts/fetch_news.py --categories BTC --limit 5

# Fetch negative sentiment news (market crashes, etc.)
python scripts/fetch_news.py --sentiment NEGATIVE --limit 10

# Output as markdown
python scripts/fetch_news.py --format markdown --limit 3
```

## API Endpoints

| Endpoint | Script | Description |
|----------|--------|-------------|
| `/news/v1/article/list` | `fetch_news.py` | Fetch news articles |
| `/news/v1/source/list` | `list_sources.py` | List news sources |
| `/news/v1/category/list` | `list_categories.py` | List categories |

## Fetch News Options

| Option | Description | Example |
|--------|-------------|---------|
| `--limit N` | Number of articles (max 50) | `--limit 20` |
| `--categories` | Filter by coin/topic | `--categories BTC,ETH` |
| `--sentiment` | Filter by sentiment | `--sentiment NEGATIVE` |
| `--sources` | Filter by source IDs | `--sources 5,55` |
| `--format` | Output: json, summary, markdown | `--format markdown` |
| `--lang` | Language (default: EN) | `--lang EN` |

## Common Categories

| Category | Description |
|----------|-------------|
| `BTC` | Bitcoin news |
| `ETH` | Ethereum news |
| `SOL` | Solana news |
| `XRP` | XRP/Ripple news |
| `MARKET` | Market analysis |
| `DEFI` | DeFi protocols |
| `NFT` | NFT/Collectibles |
| `REGULATION` | Regulatory news |
| `BUSINESS` | Business/Corporate |

## Output Formats

**Summary (default):** Concise list with title, source, date, sentiment, categories, URL

**Markdown:** Formatted articles with body preview, suitable for reports

**JSON:** Raw API response for programmatic use

## API Behavior Notes

⚠️ **Invalid Category Filters:** The CoinDesk API ignores invalid category filters and returns all articles instead of empty results. To ensure valid categories, use `list_categories.py` first to see available options.

## Example Use Cases

1. **Daily crypto briefing:** `python scripts/fetch_news.py --limit 10 --format markdown`
2. **Bitcoin-only news:** `python scripts/fetch_news.py --categories BTC --limit 5`
3. **Market crash alerts:** `python scripts/fetch_news.py --sentiment NEGATIVE`
4. **Find news sources:** `python scripts/list_sources.py`
5. **Find available categories:** `python scripts/list_categories.py --filter SOL`
