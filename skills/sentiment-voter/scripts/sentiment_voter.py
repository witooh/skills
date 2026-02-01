#!/usr/bin/env python3
"""
Sentiment Voter - Multi-LLM sentiment analysis with voting and caching.

Uses 3 LLMs to vote on sentiment (bullish/bearish/neutral) for stock/ETF/crypto articles.
Results are cached with configurable TTL (default: 4 hours).

Usage:
    python sentiment_voter.py --article "article text" [options]
    python sentiment_voter.py --file article.txt [options]

Options:
    --models MODEL1,MODEL2,MODEL3  Comma-separated list of 3 models (default: opencode/glm-4.7-free,opencode/kimi-k2.5-free,opencode/big-pickle)
    --ttl SECONDS                  Cache TTL in seconds (default: 14400 = 4 hours)
    --cache-dir PATH               Cache directory (default: ~/.cache/sentiment-voter)
    --no-cache                     Disable caching
    --symbol SYMBOL                Stock/ETF/crypto symbol for context
    --verbose                      Show detailed voting breakdown
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed

DEFAULT_MODELS = [
    "opencode/glm-4.7-free",
    "opencode/kimi-k2.5-free",
    "opencode/big-pickle",
]
DEFAULT_TTL = 14400  # 4 hours
DEFAULT_CACHE_DIR = Path.home() / ".cache" / "sentiment-voter"

SENTIMENT_PROMPT = """Analyze the following article about {symbol} and determine the market sentiment.

Article:
---
{article}
---

Respond with ONLY a JSON object in this exact format:
{{
    "sentiment": "bullish" | "bearish" | "neutral",
    "confidence": 0-100,
    "reasoning": "brief explanation (1-2 sentences)"
}}

Rules:
- "bullish" = positive outlook, expect price increase
- "bearish" = negative outlook, expect price decrease  
- "neutral" = no clear direction or mixed signals
- confidence = how certain you are (0-100)
"""


@dataclass
class Vote:
    model: str
    sentiment: str
    confidence: int
    reasoning: str


@dataclass
class SentimentResult:
    final_sentiment: str
    final_confidence: float
    votes: list
    symbol: str
    timestamp: float
    cached: bool = False


class Cache:
    """Simple file-based cache with TTL support."""

    def __init__(self, cache_dir: Path, ttl: int):
        self.cache_dir = cache_dir
        self.ttl = ttl
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_key(self, article: str, symbol: str, models: list) -> str:
        """Generate cache key from article content and config."""
        content = f"{article}|{symbol}|{','.join(sorted(models))}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _get_path(self, key: str) -> Path:
        return self.cache_dir / f"{key}.json"

    def get(self, article: str, symbol: str, models: list) -> Optional[SentimentResult]:
        """Get cached result if exists and not expired."""
        key = self._get_key(article, symbol, models)
        path = self._get_path(key)

        if not path.exists():
            return None

        try:
            with open(path) as f:
                data = json.load(f)

            # Check TTL
            if time.time() - data["timestamp"] > self.ttl:
                path.unlink()  # Remove expired cache
                return None

            data["cached"] = True
            return SentimentResult(
                final_sentiment=data["final_sentiment"],
                final_confidence=data["final_confidence"],
                votes=[Vote(**v) for v in data["votes"]],
                symbol=data["symbol"],
                timestamp=data["timestamp"],
                cached=True,
            )
        except (json.JSONDecodeError, KeyError):
            path.unlink()
            return None

    def set(self, article: str, symbol: str, models: list, result: SentimentResult):
        """Cache the result."""
        key = self._get_key(article, symbol, models)
        path = self._get_path(key)

        data = {
            "final_sentiment": result.final_sentiment,
            "final_confidence": result.final_confidence,
            "votes": [asdict(v) for v in result.votes],
            "symbol": result.symbol,
            "timestamp": result.timestamp,
        }

        with open(path, "w") as f:
            json.dump(data, f, indent=2)


def call_llm(model: str, prompt: str) -> str:
    """Call LLM via opencode run command."""
    try:
        result = subprocess.run(
            ["opencode", "run", "-m", model, prompt],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            raise RuntimeError(f"opencode run failed: {result.stderr}")
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"LLM call timed out for model {model}")
    except FileNotFoundError:
        raise RuntimeError(
            "opencode command not found. Make sure it's installed and in PATH."
        )


def parse_llm_response(response: str, model: str) -> Vote:
    """Parse LLM JSON response into Vote object."""
    try:
        # Find JSON in response
        start = response.find("{")
        end = response.rfind("}") + 1
        if start == -1 or end == 0:
            raise ValueError("No JSON found in response")

        json_str = response[start:end]
        data = json.loads(json_str)

        sentiment = data.get("sentiment", "neutral").lower()
        if sentiment not in ["bullish", "bearish", "neutral"]:
            sentiment = "neutral"

        confidence = int(data.get("confidence", 50))
        confidence = max(0, min(100, confidence))

        reasoning = data.get("reasoning", "No reasoning provided")

        return Vote(
            model=model, sentiment=sentiment, confidence=confidence, reasoning=reasoning
        )
    except (json.JSONDecodeError, ValueError) as e:
        # Fallback: try to detect sentiment from text
        response_lower = response.lower()
        if "bullish" in response_lower:
            sentiment = "bullish"
        elif "bearish" in response_lower:
            sentiment = "bearish"
        else:
            sentiment = "neutral"

        return Vote(
            model=model,
            sentiment=sentiment,
            confidence=50,
            reasoning=f"Parsed from text (JSON parse failed: {e})",
        )


def aggregate_votes(votes: list[Vote]) -> tuple[str, float]:
    """Aggregate votes to determine final sentiment and confidence."""
    counts = {"bullish": 0, "bearish": 0, "neutral": 0}
    confidence_sum = {"bullish": 0, "bearish": 0, "neutral": 0}

    for vote in votes:
        counts[vote.sentiment] += 1
        confidence_sum[vote.sentiment] += vote.confidence

    # Determine winner by majority vote
    max_count = max(counts.values())
    winners = [s for s, c in counts.items() if c == max_count]

    if len(winners) == 1:
        winner = winners[0]
    else:
        # Tie-breaker: use average confidence
        avg_conf = {
            s: confidence_sum[s] / counts[s] if counts[s] > 0 else 0 for s in winners
        }
        winner = max(avg_conf, key=avg_conf.get)

    # Calculate final confidence
    if counts[winner] == len(votes):
        # Unanimous: average confidence
        final_confidence = confidence_sum[winner] / counts[winner]
    elif counts[winner] > len(votes) / 2:
        # Majority: weighted average
        final_confidence = (confidence_sum[winner] / counts[winner]) * 0.8
    else:
        # No clear majority: lower confidence
        final_confidence = (confidence_sum[winner] / counts[winner]) * 0.5

    return winner, round(final_confidence, 1)


def analyze_sentiment(
    article: str,
    symbol: str = "asset",
    models: list[str] = None,
    cache: Optional[Cache] = None,
    verbose: bool = False,
) -> SentimentResult:
    """Analyze sentiment using multiple LLMs with voting."""
    models = models or DEFAULT_MODELS

    if len(models) != 3:
        raise ValueError("Exactly 3 models required for voting")

    # Check cache
    if cache:
        cached = cache.get(article, symbol, models)
        if cached:
            if verbose:
                print(
                    f"[Cache hit] Using cached result from {time.ctime(cached.timestamp)}"
                )
            return cached

    # Build prompt
    prompt = SENTIMENT_PROMPT.format(symbol=symbol, article=article[:8000])

    votes = []

    # Call all 3 LLMs in parallel
    if verbose:
        print(f"[Voting] Querying {len(models)} models...")

    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_model = {
            executor.submit(call_llm, model, prompt): model for model in models
        }

        for future in as_completed(future_to_model):
            model = future_to_model[future]
            try:
                response = future.result()
                vote = parse_llm_response(response, model)
                votes.append(vote)
                if verbose:
                    print(
                        f"  [{model}] {vote.sentiment} (confidence: {vote.confidence}%)"
                    )
            except Exception as e:
                if verbose:
                    print(f"  [{model}] Error: {e}")
                votes.append(
                    Vote(
                        model=model,
                        sentiment="neutral",
                        confidence=20,
                        reasoning=f"Error: {str(e)}",
                    )
                )

    # Aggregate votes
    final_sentiment, final_confidence = aggregate_votes(votes)

    result = SentimentResult(
        final_sentiment=final_sentiment,
        final_confidence=final_confidence,
        votes=votes,
        symbol=symbol,
        timestamp=time.time(),
        cached=False,
    )

    # Save to cache
    if cache:
        cache.set(article, symbol, models, result)

    return result


def format_result(result: SentimentResult, verbose: bool = False) -> str:
    """Format result for output."""
    output = {
        "symbol": result.symbol,
        "sentiment": result.final_sentiment,
        "confidence": result.final_confidence,
        "cached": result.cached,
        "timestamp": time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(result.timestamp)
        ),
    }

    if verbose:
        output["votes"] = [
            {
                "model": v.model,
                "sentiment": v.sentiment,
                "confidence": v.confidence,
                "reasoning": v.reasoning,
            }
            for v in result.votes
        ]

    return json.dumps(output, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Multi-LLM sentiment analysis with voting"
    )
    parser.add_argument("--article", "-a", help="Article text or JSON string")
    parser.add_argument("--file", "-f", help="Read article from file")
    parser.add_argument(
        "--models",
        "-m",
        default=",".join(DEFAULT_MODELS),
        help=f"Comma-separated list of 3 models (default: {','.join(DEFAULT_MODELS)})",
    )
    parser.add_argument(
        "--ttl",
        type=int,
        default=DEFAULT_TTL,
        help=f"Cache TTL in seconds (default: {DEFAULT_TTL})",
    )
    parser.add_argument(
        "--cache-dir",
        default=str(DEFAULT_CACHE_DIR),
        help=f"Cache directory (default: {DEFAULT_CACHE_DIR})",
    )
    parser.add_argument("--no-cache", action="store_true", help="Disable caching")
    parser.add_argument(
        "--symbol", "-s", default="asset", help="Stock/ETF/crypto symbol"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed voting breakdown"
    )

    args = parser.parse_args()

    # Get article content
    if args.file:
        with open(args.file) as f:
            article = f.read()
    elif args.article:
        article = args.article
    else:
        article = sys.stdin.read()

    if not article.strip():
        print("Error: No article content provided", file=sys.stderr)
        sys.exit(1)

    # Parse models
    models = [m.strip() for m in args.models.split(",")]
    if len(models) != 3:
        print("Error: Exactly 3 models required", file=sys.stderr)
        sys.exit(1)

    # Setup cache
    cache = None if args.no_cache else Cache(Path(args.cache_dir), args.ttl)

    try:
        result = analyze_sentiment(
            article=article,
            symbol=args.symbol,
            models=models,
            cache=cache,
            verbose=args.verbose,
        )
        print(format_result(result, args.verbose))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
