#!/usr/bin/env python3
"""
Clear sentiment voter cache.

Usage:
    python clear_cache.py              # Clear all expired entries
    python clear_cache.py --all        # Clear entire cache
    python clear_cache.py --symbol BTC # Clear entries for specific symbol
"""

import argparse
import json
import time
from pathlib import Path

DEFAULT_CACHE_DIR = Path.home() / ".cache" / "sentiment-voter"
DEFAULT_TTL = 14400  # 4 hours


def clear_cache(
    cache_dir: Path,
    all_entries: bool = False,
    ttl: int = DEFAULT_TTL,
    symbol: str = None,
):
    """Clear cache entries."""
    if not cache_dir.exists():
        print("Cache directory does not exist")
        return 0

    removed = 0
    now = time.time()

    for cache_file in cache_dir.glob("*.json"):
        should_remove = False

        if all_entries:
            should_remove = True
        else:
            try:
                with open(cache_file) as f:
                    data = json.load(f)

                if now - data.get("timestamp", 0) > ttl:
                    should_remove = True

                if symbol and data.get("symbol", "").upper() == symbol.upper():
                    should_remove = True

            except (json.JSONDecodeError, KeyError):
                should_remove = True

        if should_remove:
            cache_file.unlink()
            removed += 1

    return removed


def main():
    parser = argparse.ArgumentParser(description="Clear sentiment voter cache")
    parser.add_argument("--all", "-a", action="store_true", help="Clear entire cache")
    parser.add_argument("--symbol", "-s", help="Clear entries for specific symbol")
    parser.add_argument(
        "--cache-dir",
        default=str(DEFAULT_CACHE_DIR),
        help=f"Cache directory (default: {DEFAULT_CACHE_DIR})",
    )
    parser.add_argument(
        "--ttl",
        type=int,
        default=DEFAULT_TTL,
        help=f"TTL for expired check (default: {DEFAULT_TTL})",
    )

    args = parser.parse_args()

    removed = clear_cache(
        Path(args.cache_dir), all_entries=args.all, ttl=args.ttl, symbol=args.symbol
    )

    print(f"Removed {removed} cache entries")


if __name__ == "__main__":
    main()
