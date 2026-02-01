---
name: sentiment-voter
description: Analyze market sentiment for stocks, ETFs, and crypto using multi-LLM voting. Uses 3 LLMs to vote (bullish/bearish/neutral) for consensus with confidence scoring. Integrates with coindesk-news (crypto) and massive-news (stock/ETF) skills for article sourcing. Includes file-based caching with configurable TTL (default 4 hours). Use when analyzing news articles for trading signals, market sentiment, or investment research.
---

# Sentiment Voter

Multi-LLM sentiment analysis with voting and caching for stock/ETF/crypto articles.

## Workflow

1. **Get news** - Use `coindesk-news` (crypto) or `massive-news` (stock/ETF) skill
2. **Analyze sentiment** - Run `sentiment_voter.py` with article
3. **Get consensus** - 3 LLMs vote, majority wins

## Quick Start

### Crypto (via coindesk-news)

```bash
# Get Bitcoin news and analyze
news=$(opencode run "use coindesk-news skill to get latest BTC article")
python scripts/sentiment_voter.py -a "$news" -s BTC -v
```

### Stock/ETF (via massive-news)

```bash
# Get AAPL news and analyze
news=$(opencode run "use massive-news skill to get latest AAPL article")
python scripts/sentiment_voter.py -a "$news" -s AAPL -v
```

## Script Usage

### sentiment_voter.py

```bash
# From text
python scripts/sentiment_voter.py -a "article text here" -s SYMBOL

# From file
python scripts/sentiment_voter.py -f article.txt -s SYMBOL

# From stdin (pipe)
cat article.txt | python scripts/sentiment_voter.py -s SYMBOL

# Custom models
python scripts/sentiment_voter.py -a "..." -m "gpt-4o,claude-3-opus,gemini-pro"

# Custom cache TTL (1 hour)
python scripts/sentiment_voter.py -a "..." --ttl 3600

# Disable cache
python scripts/sentiment_voter.py -a "..." --no-cache

# Verbose output (show all votes)
python scripts/sentiment_voter.py -a "..." -v
```

**Options:**

| Flag | Description | Default |
|------|-------------|---------|
| `-a, --article` | Article text | - |
| `-f, --file` | Read from file | - |
| `-s, --symbol` | Asset symbol | "asset" |
| `-m, --models` | 3 comma-separated models | opencode/glm-4.7-free,opencode/kimi-k2.5-free,opencode/big-pickle |
| `--ttl` | Cache TTL in seconds | 14400 (4 hours) |
| `--cache-dir` | Cache directory | ~/.cache/sentiment-voter |
| `--no-cache` | Disable caching | false |
| `-v, --verbose` | Show vote breakdown | false |

### Output Format

```json
{
  "symbol": "BTC",
  "sentiment": "bullish",
  "confidence": 78.5,
  "cached": false,
  "timestamp": "2024-01-15 14:30:00"
}
```

With `-v` (verbose):

```json
{
  "symbol": "BTC",
  "sentiment": "bullish",
  "confidence": 78.5,
  "cached": false,
  "timestamp": "2024-01-15 14:30:00",
  "votes": [
    {"model": "opencode/glm-4.7-free", "sentiment": "bullish", "confidence": 75, "reasoning": "..."},
    {"model": "opencode/kimi-k2.5-free", "sentiment": "bullish", "confidence": 85, "reasoning": "..."},
    {"model": "opencode/big-pickle", "sentiment": "neutral", "confidence": 60, "reasoning": "..."}
  ]
}
```

### clear_cache.py

```bash
# Clear expired entries
python scripts/clear_cache.py

# Clear all cache
python scripts/clear_cache.py --all

# Clear specific symbol
python scripts/clear_cache.py -s BTC
```

## Voting Logic

1. **Majority wins** - 2/3 or 3/3 agreement
2. **Tie-breaker** - Higher average confidence wins
3. **Confidence adjustment**:
   - Unanimous: 100% of average confidence
   - Majority: 80% of average confidence
   - Split: 50% of average confidence

## Integration Examples

### Batch Analysis

```python
symbols = ["BTC", "ETH", "SOL"]
for symbol in symbols:
    # Get news via opencode
    result = subprocess.run(
        ["opencode", "run", f"use coindesk-news to get {symbol} news"],
        capture_output=True, text=True
    )
    news = result.stdout
    
    # Analyze sentiment
    result = subprocess.run(
        ["python", "scripts/sentiment_voter.py", "-a", news, "-s", symbol],
        capture_output=True, text=True
    )
    print(f"{symbol}: {result.stdout}")
```

### Custom Models

Use any OpenAI-compatible API models:

```bash
python scripts/sentiment_voter.py \
  -a "article..." \
  -m "gpt-4o,claude-3-opus-20240229,gemini-1.5-pro" \
  -s NVDA
```
