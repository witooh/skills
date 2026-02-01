#!/usr/bin/env python3
"""
Fetch stock/ETF news from Massive API using official Python client.

Usage:
    fetch_news.py <ticker> [--limit N] [--from DATE] [--to DATE]

Examples:
    fetch_news.py AAPL
    fetch_news.py TSLA --limit 20
    fetch_news.py GOOGL --from 2024-01-01 --to 2024-01-31

Requirements:
    pip install massive

Environment:
    MASSIVE_API_KEY - Required API key (auto-detected by client)
"""

import argparse
import json
import sys
from datetime import datetime

try:
    from massive import RESTClient
    from massive.rest.models import TickerNews
    from massive.exceptions import AuthError
except ImportError:
    print(
        "Error: massive package not installed. Run: pip install massive",
        file=sys.stderr,
    )
    sys.exit(1)


def fetch_news(
    ticker: str,
    limit: int = 10,
    from_date: str = None,
    to_date: str = None,
    order: str = "desc",
) -> list:
    """
    Fetch news articles for a ticker using Massive Python client.

    Args:
        ticker: Stock/ETF ticker symbol (e.g., AAPL, TSLA)
        limit: Number of results (1-1000, default 10)
        from_date: Filter articles from this date (YYYY-MM-DD)
        to_date: Filter articles until this date (YYYY-MM-DD)
        order: Sort order (asc, desc)

    Returns:
        List of TickerNews objects
    """
    # RESTClient auto-reads MASSIVE_API_KEY from environment
    try:
        client = RESTClient()
    except AuthError:
        print(
            "Error: MASSIVE_API_KEY environment variable not set.\n"
            "Set it with: export MASSIVE_API_KEY=your_api_key",
            file=sys.stderr,
        )
        sys.exit(1)

    # Build kwargs for list_ticker_news
    kwargs = {
        "ticker": ticker,
        "limit": min(max(1, limit), 1000),
        "order": order,
    }

    # Add date filters
    if from_date:
        kwargs["published_utc_gte"] = from_date
    if to_date:
        kwargs["published_utc_lte"] = to_date

    # Fetch news (returns iterator)
    news = []
    try:
        for article in client.list_ticker_news(**kwargs):
            news.append(article)
            if len(news) >= limit:
                break
    except Exception as e:
        print(f"Error fetching news: {e}", file=sys.stderr)
        sys.exit(1)

    return news


def format_article(article: TickerNews) -> str:
    """Format a single news article for display."""
    lines = []

    title = article.title or "No title"
    author = article.author or "Unknown"
    published = article.published_utc or ""
    url = article.article_url or ""
    description = article.description or ""
    tickers = article.tickers or []

    # Get sentiment from insights
    sentiment = ""
    if article.insights:
        for insight in article.insights:
            if hasattr(insight, "sentiment") and insight.sentiment:
                sentiment = f" [{insight.sentiment}]"
                break

    lines.append(f"## {title}{sentiment}")
    lines.append(f"**Author:** {author} | **Published:** {published}")
    if tickers:
        lines.append(f"**Tickers:** {', '.join(tickers)}")
    if description:
        lines.append(f"\n{description}")
    if url:
        lines.append(f"\n[Read more]({url})")

    return "\n".join(lines)


def article_to_dict(article: TickerNews) -> dict:
    """Convert TickerNews to dictionary for JSON output."""
    return {
        "id": article.id,
        "title": article.title,
        "author": article.author,
        "published_utc": article.published_utc,
        "description": article.description,
        "article_url": article.article_url,
        "image_url": article.image_url,
        "amp_url": article.amp_url,
        "tickers": article.tickers,
        "keywords": article.keywords,
        "publisher": {
            "name": article.publisher.name if article.publisher else None,
            "homepage_url": article.publisher.homepage_url
            if article.publisher
            else None,
            "logo_url": article.publisher.logo_url if article.publisher else None,
        }
        if article.publisher
        else None,
        "insights": [
            {
                "ticker": i.ticker,
                "sentiment": i.sentiment,
                "sentiment_reasoning": i.sentiment_reasoning,
            }
            for i in (article.insights or [])
        ]
        if article.insights
        else [],
    }


def main():
    parser = argparse.ArgumentParser(
        description="Fetch stock/ETF news from Massive API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s AAPL                          # Latest 10 AAPL news
  %(prog)s TSLA --limit 20               # Latest 20 TSLA news  
  %(prog)s GOOGL --from 2024-01-01       # News from specific date
  %(prog)s MSFT --json                   # Output as JSON
""",
    )

    parser.add_argument("ticker", help="Stock/ETF ticker symbol (e.g., AAPL)")
    parser.add_argument(
        "--limit",
        "-n",
        type=int,
        default=10,
        help="Number of results (1-1000, default: 10)",
    )
    parser.add_argument(
        "--from", dest="from_date", metavar="DATE", help="Filter from date (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--to", dest="to_date", metavar="DATE", help="Filter to date (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--order",
        default="desc",
        choices=["asc", "desc"],
        help="Sort order (default: desc)",
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    # Validate dates
    for date_str, name in [(args.from_date, "--from"), (args.to_date, "--to")]:
        if date_str:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                print(f"Error: {name} must be in YYYY-MM-DD format", file=sys.stderr)
                sys.exit(1)

    # Fetch news
    articles = fetch_news(
        ticker=args.ticker.upper(),
        limit=args.limit,
        from_date=args.from_date,
        to_date=args.to_date,
        order=args.order,
    )

    # Output
    if args.json:
        output = {
            "count": len(articles),
            "results": [article_to_dict(a) for a in articles],
        }
        print(json.dumps(output, indent=2, default=str))
    else:
        print(f"# News for {args.ticker.upper()}")
        print(f"**Found {len(articles)} article(s)**\n")

        if not articles:
            print("No news articles found.")
        else:
            for article in articles:
                print(format_article(article))
                print("\n---\n")


if __name__ == "__main__":
    main()
