#!/usr/bin/env python3
"""
CoinDesk News Fetcher - Fetches cryptocurrency news from CoinDesk Data API

Usage:
    python fetch_news.py [options]

Options:
    --limit N          Number of articles (default: 10, max: 50)
    --categories CAT   Filter by categories (comma-separated, e.g., BTC,ETH)
    --sources SRC      Filter by source IDs (comma-separated)
    --lang LANG        Language filter (default: EN)
    --format FMT       Output format: json, summary, markdown (default: summary)
    --sentiment SENT   Filter by sentiment: POSITIVE, NEGATIVE, NEUTRAL

Examples:
    python fetch_news.py
    python fetch_news.py --limit 5 --categories BTC,ETH
    python fetch_news.py --format markdown --limit 3
    python fetch_news.py --sentiment NEGATIVE --limit 10
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
from datetime import datetime


BASE_URL = "https://data-api.coindesk.com/news/v1/article/list"
CATEGORIES_URL = "https://data-api.coindesk.com/news/v1/category/list"


def fetch_valid_categories():
    """Fetch list of valid category names from API."""
    try:
        req = urllib.request.Request(
            CATEGORIES_URL,
            headers={
                "Accept": "application/json",
                "User-Agent": "CoinDesk-News-Skill/1.0",
            },
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            if "Data" in data:
                return {cat.get("NAME", "").upper() for cat in data["Data"]}
    except Exception:
        pass
    return set()


def validate_categories(categories):
    """Validate category names and return invalid ones."""
    if not categories:
        return []

    valid_categories = fetch_valid_categories()
    if not valid_categories:
        return []  # Skip validation if we can't fetch categories

    invalid = []
    for cat in categories:
        cat_upper = cat.strip().upper()
        if cat_upper and cat_upper not in valid_categories:
            invalid.append(cat)

    return invalid


def fetch_news(limit=10, categories=None, sources=None, lang="EN", sentiment=None):
    """
    Fetch news articles from CoinDesk Data API.

    Args:
        limit: Number of articles to fetch (max 50)
        categories: List of category names (e.g., ['BTC', 'ETH'])
        sources: List of source IDs
        lang: Language code (default: EN)
        sentiment: Filter by sentiment (POSITIVE, NEGATIVE, NEUTRAL)

    Returns:
        dict: API response with 'Data' key containing articles
    """
    params = {"limit": min(limit, 50)}

    if categories:
        params["categories"] = ",".join(categories)
    if sources:
        params["source_ids"] = ",".join(str(s) for s in sources)
    if lang:
        params["lang"] = lang

    url = f"{BASE_URL}?{urllib.parse.urlencode(params)}"

    req = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": "CoinDesk-News-Skill/1.0"},
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))

            # Filter by sentiment if specified
            if sentiment and "Data" in data:
                data["Data"] = [
                    article
                    for article in data["Data"]
                    if article.get("SENTIMENT", "").upper() == sentiment.upper()
                ]

            return data
    except urllib.error.URLError as e:
        return {"error": str(e), "Data": []}
    except json.JSONDecodeError as e:
        return {"error": f"JSON parse error: {e}", "Data": []}


def format_timestamp(ts):
    """Convert Unix timestamp to readable format."""
    if not ts:
        return "N/A"
    try:
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
    except (ValueError, OSError):
        return "N/A"


def format_summary(articles):
    """Format articles as concise summary."""
    if not articles:
        return "No articles found."

    lines = []
    for i, article in enumerate(articles, 1):
        title = article.get("TITLE", "No title")
        source = article.get("SOURCE_DATA", {}).get("NAME", "Unknown")
        published = format_timestamp(article.get("PUBLISHED_ON"))
        sentiment = article.get("SENTIMENT", "N/A")
        url = article.get("URL", "")

        categories = [c.get("NAME", "") for c in article.get("CATEGORY_DATA", [])]
        cat_str = ", ".join(categories[:3]) if categories else "N/A"

        lines.append(f"{i}. [{sentiment}] {title}")
        lines.append(f"   Source: {source} | {published}")
        lines.append(f"   Categories: {cat_str}")
        lines.append(f"   URL: {url}")
        lines.append("")

    return "\n".join(lines)


def format_markdown(articles):
    """Format articles as markdown."""
    if not articles:
        return "# No articles found"

    lines = ["# CoinDesk Crypto News\n"]

    for article in articles:
        title = article.get("TITLE", "No title")
        source = article.get("SOURCE_DATA", {}).get("NAME", "Unknown")
        published = format_timestamp(article.get("PUBLISHED_ON"))
        sentiment = article.get("SENTIMENT", "N/A")
        url = article.get("URL", "")
        body = article.get("BODY", "")[:500]

        categories = [c.get("NAME", "") for c in article.get("CATEGORY_DATA", [])]

        sentiment_emoji = {"POSITIVE": "+", "NEGATIVE": "-", "NEUTRAL": "~"}.get(
            sentiment, "?"
        )

        lines.append(f"## [{sentiment_emoji}] {title}")
        lines.append(f"**Source:** {source} | **Published:** {published}")
        if categories:
            lines.append(f"**Categories:** {', '.join(categories)}")
        lines.append(f"\n{body}{'...' if len(article.get('BODY', '')) > 500 else ''}")
        lines.append(f"\n[Read more]({url})\n")
        lines.append("---\n")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch cryptocurrency news from CoinDesk"
    )
    parser.add_argument(
        "--limit", type=int, default=10, help="Number of articles (default: 10)"
    )
    parser.add_argument(
        "--categories", type=str, help="Filter by categories (comma-separated)"
    )
    parser.add_argument(
        "--sources", type=str, help="Filter by source IDs (comma-separated)"
    )
    parser.add_argument("--lang", type=str, default="EN", help="Language (default: EN)")
    parser.add_argument(
        "--format",
        type=str,
        default="summary",
        choices=["json", "summary", "markdown"],
        help="Output format (default: summary)",
    )
    parser.add_argument(
        "--sentiment",
        type=str,
        choices=["POSITIVE", "NEGATIVE", "NEUTRAL"],
        help="Filter by sentiment",
    )

    args = parser.parse_args()

    categories = args.categories.split(",") if args.categories else None
    sources = args.sources.split(",") if args.sources else None

    # Validate categories and warn about invalid ones
    if categories:
        invalid_cats = validate_categories(categories)
        if invalid_cats:
            print(
                f"Warning: Invalid categories (API will ignore): {', '.join(invalid_cats)}",
                file=sys.stderr,
            )
            print(
                "Use 'python list_categories.py' to see available categories.",
                file=sys.stderr,
            )
            print("", file=sys.stderr)

    result = fetch_news(
        limit=args.limit,
        categories=categories,
        sources=sources,
        lang=args.lang,
        sentiment=args.sentiment,
    )

    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    articles = result.get("Data", [])

    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.format == "markdown":
        print(format_markdown(articles))
    else:
        print(format_summary(articles))


if __name__ == "__main__":
    main()
