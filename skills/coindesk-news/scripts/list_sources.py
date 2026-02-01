#!/usr/bin/env python3
"""
List available news sources from CoinDesk Data API

Usage:
    python list_sources.py [--format json|table]
"""

import argparse
import json
import urllib.request


def fetch_sources():
    """Fetch available news sources."""
    url = "https://data-api.coindesk.com/news/v1/source/list"

    req = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": "CoinDesk-News-Skill/1.0"},
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e), "Data": []}


def format_table(sources):
    """Format sources as a table."""
    if not sources:
        return "No sources found."

    lines = [f"{'ID':<6} {'Name':<25} {'Score':<6} {'Status':<10}", "-" * 50]

    for src in sorted(sources, key=lambda x: x.get("BENCHMARK_SCORE", 0), reverse=True):
        lines.append(
            f"{src.get('ID', 'N/A'):<6} "
            f"{src.get('NAME', 'Unknown')[:24]:<25} "
            f"{src.get('BENCHMARK_SCORE', 0):<6} "
            f"{src.get('STATUS', 'N/A'):<10}"
        )

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="List CoinDesk news sources")
    parser.add_argument(
        "--format",
        type=str,
        default="table",
        choices=["json", "table"],
        help="Output format (default: table)",
    )

    args = parser.parse_args()

    result = fetch_sources()

    if "error" in result:
        print(f"Error: {result['error']}")
        return

    sources = result.get("Data", [])

    if args.format == "json":
        print(json.dumps(sources, indent=2, ensure_ascii=False))
    else:
        print(format_table(sources))


if __name__ == "__main__":
    main()
