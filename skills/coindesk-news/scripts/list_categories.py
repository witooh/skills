#!/usr/bin/env python3
"""
List available news categories from CoinDesk Data API

Usage:
    python list_categories.py [--format json|table] [--filter TERM]
"""

import argparse
import json
import urllib.request


def fetch_categories():
    """Fetch available news categories."""
    url = "https://data-api.coindesk.com/news/v1/category/list"

    req = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": "CoinDesk-News-Skill/1.0"},
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e), "Data": []}


def format_table(categories, filter_term=None):
    """Format categories as a table."""
    if not categories:
        return "No categories found."

    if filter_term:
        filter_upper = filter_term.upper()
        categories = [
            c for c in categories if filter_upper in c.get("NAME", "").upper()
        ]

    lines = [f"{'ID':<6} {'Name':<30} {'Status':<10}", "-" * 50]

    for cat in sorted(categories, key=lambda x: x.get("NAME", "")):
        lines.append(
            f"{cat.get('ID', 'N/A'):<6} "
            f"{cat.get('NAME', 'Unknown')[:29]:<30} "
            f"{cat.get('STATUS', 'N/A'):<10}"
        )

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="List CoinDesk news categories")
    parser.add_argument(
        "--format",
        type=str,
        default="table",
        choices=["json", "table"],
        help="Output format (default: table)",
    )
    parser.add_argument("--filter", type=str, help="Filter categories by name")

    args = parser.parse_args()

    result = fetch_categories()

    if "error" in result:
        print(f"Error: {result['error']}")
        return

    categories = result.get("Data", [])

    if args.format == "json":
        if args.filter:
            filter_upper = args.filter.upper()
            categories = [
                c for c in categories if filter_upper in c.get("NAME", "").upper()
            ]
        print(json.dumps(categories, indent=2, ensure_ascii=False))
    else:
        print(format_table(categories, args.filter))


if __name__ == "__main__":
    main()
