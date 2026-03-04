#!/usr/bin/env python3
"""
Food Tracker Database CLI - Phosphorus and Potassium intake tracking.

Usage:
    python db.py --init
    python db.py --log --food NAME --meal-time DT --phosphorus N --potassium N [options]
    python db.py --search QUERY
    python db.py --report daily [--date YYYY-MM-DD]
    python db.py --report monthly [--month YYYY-MM]
    python db.py --list [--date YYYY-MM-DD]
    python db.py --delete ID

All output is JSON to stdout.
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ── Constants ────────────────────────────────────────────────────────────────

SKILL_DIR = Path(__file__).resolve().parent.parent
DB_PATH = SKILL_DIR / "data" / "food_tracker.db"

PHOSPHORUS_DAILY_LIMIT = 1000  # mg (CKD general guideline)
POTASSIUM_DAILY_LIMIT = 3000   # mg (CKD general guideline)

BANGKOK_TZ = timezone(timedelta(hours=7))

# ── Schema ───────────────────────────────────────────────────────────────────

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS food_logs (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    food_name     TEXT    NOT NULL,
    meal_time     TEXT    NOT NULL,
    meal_period   TEXT,
    phosphorus_mg REAL    NOT NULL,
    potassium_mg  REAL    NOT NULL,
    serving_size  TEXT,
    source        TEXT    NOT NULL DEFAULT 'web',
    notes         TEXT,
    created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE VIRTUAL TABLE IF NOT EXISTS food_logs_fts
    USING fts5(
        food_name,
        content='food_logs',
        content_rowid='id',
        tokenize='unicode61'
    );

CREATE TRIGGER IF NOT EXISTS food_logs_ai
    AFTER INSERT ON food_logs BEGIN
        INSERT INTO food_logs_fts(rowid, food_name)
        VALUES (new.id, new.food_name);
    END;

CREATE TRIGGER IF NOT EXISTS food_logs_ad
    AFTER DELETE ON food_logs BEGIN
        INSERT INTO food_logs_fts(food_logs_fts, rowid, food_name)
        VALUES ('delete', old.id, old.food_name);
    END;

CREATE TRIGGER IF NOT EXISTS food_logs_au
    AFTER UPDATE ON food_logs BEGIN
        INSERT INTO food_logs_fts(food_logs_fts, rowid, food_name)
        VALUES ('delete', old.id, old.food_name);
        INSERT INTO food_logs_fts(rowid, food_name)
        VALUES (new.id, new.food_name);
    END;

CREATE INDEX IF NOT EXISTS idx_food_logs_meal_time ON food_logs(meal_time);
"""

# ── Helpers ──────────────────────────────────────────────────────────────────


def now_bangkok() -> str:
    return datetime.now(BANGKOK_TZ).isoformat()


def output_json(data: dict):
    print(json.dumps(data, ensure_ascii=False, indent=2))


def error_exit(msg: str):
    err = {"success": False, "error": msg, "timestamp": now_bangkok()}
    print(json.dumps(err, ensure_ascii=False), file=sys.stderr)
    sys.exit(1)


# ── Database ─────────────────────────────────────────────────────────────────


def get_connection(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Path) -> dict:
    conn = get_connection(db_path)
    conn.executescript(SCHEMA_SQL)
    conn.commit()
    conn.close()
    return {
        "success": True,
        "data": {"db_path": str(db_path), "message": "Database initialized"},
        "timestamp": now_bangkok(),
    }


def insert_log(
    db_path: Path,
    food_name: str,
    meal_time: str,
    phosphorus_mg: float,
    potassium_mg: float,
    serving_size: str = None,
    meal_period: str = None,
    source: str = "web",
    notes: str = None,
) -> dict:
    conn = get_connection(db_path)
    conn.executescript(SCHEMA_SQL)
    cur = conn.execute(
        """
        INSERT INTO food_logs
            (food_name, meal_time, meal_period, phosphorus_mg, potassium_mg,
             serving_size, source, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            food_name,
            meal_time,
            meal_period,
            phosphorus_mg,
            potassium_mg,
            serving_size,
            source,
            notes,
        ),
    )
    conn.commit()
    entry_id = cur.lastrowid
    conn.close()
    return {
        "success": True,
        "data": {
            "id": entry_id,
            "food_name": food_name,
            "meal_time": meal_time,
            "meal_period": meal_period,
            "phosphorus_mg": phosphorus_mg,
            "potassium_mg": potassium_mg,
            "serving_size": serving_size,
            "source": source,
        },
        "timestamp": now_bangkok(),
    }


def search_foods(db_path: Path, query: str) -> dict:
    conn = get_connection(db_path)
    conn.executescript(SCHEMA_SQL)

    results = []
    seen_ids = set()

    # FTS5 search with prefix matching
    try:
        tokens = query.split()
        if tokens:
            fts_query = " OR ".join(f'"{t}"*' for t in tokens)
            rows = conn.execute(
                """
                SELECT fl.id, fl.food_name, fl.meal_time, fl.meal_period,
                       fl.phosphorus_mg, fl.potassium_mg, fl.serving_size, fl.source
                FROM food_logs fl
                JOIN food_logs_fts fts ON fts.rowid = fl.id
                WHERE food_logs_fts MATCH ?
                ORDER BY fl.meal_time DESC
                LIMIT 10
                """,
                (fts_query,),
            ).fetchall()
            for r in rows:
                if r["id"] not in seen_ids:
                    seen_ids.add(r["id"])
                    results.append(dict(r))
    except sqlite3.OperationalError:
        pass  # FTS might fail on some queries, fall through to LIKE

    # LIKE fallback for Thai compound words (no spaces)
    like_rows = conn.execute(
        """
        SELECT id, food_name, meal_time, meal_period,
               phosphorus_mg, potassium_mg, serving_size, source
        FROM food_logs
        WHERE food_name LIKE ?
        ORDER BY meal_time DESC
        LIMIT 10
        """,
        (f"%{query}%",),
    ).fetchall()

    for r in like_rows:
        if r["id"] not in seen_ids:
            seen_ids.add(r["id"])
            results.append(dict(r))

    conn.close()
    return {
        "success": True,
        "data": {"query": query, "count": len(results), "results": results},
        "timestamp": now_bangkok(),
    }


def daily_report(db_path: Path, date_str: str) -> dict:
    conn = get_connection(db_path)
    conn.executescript(SCHEMA_SQL)

    rows = conn.execute(
        """
        SELECT id, food_name, meal_time, meal_period,
               phosphorus_mg, potassium_mg, serving_size, source
        FROM food_logs
        WHERE DATE(meal_time) = ?
        ORDER BY meal_time ASC
        """,
        (date_str,),
    ).fetchall()

    entries = [dict(r) for r in rows]
    total_p = sum(e["phosphorus_mg"] for e in entries)
    total_k = sum(e["potassium_mg"] for e in entries)

    conn.close()
    return {
        "success": True,
        "data": {
            "date": date_str,
            "entries": entries,
            "entry_count": len(entries),
            "total_phosphorus_mg": round(total_p, 1),
            "total_potassium_mg": round(total_k, 1),
            "phosphorus_pct": round(total_p / PHOSPHORUS_DAILY_LIMIT * 100, 1),
            "potassium_pct": round(total_k / POTASSIUM_DAILY_LIMIT * 100, 1),
        },
        "timestamp": now_bangkok(),
    }


def monthly_report(db_path: Path, month_str: str) -> dict:
    conn = get_connection(db_path)
    conn.executescript(SCHEMA_SQL)

    # Daily breakdown
    days = conn.execute(
        """
        SELECT DATE(meal_time) AS day,
               SUM(phosphorus_mg) AS phosphorus_mg,
               SUM(potassium_mg) AS potassium_mg,
               COUNT(*) AS entry_count
        FROM food_logs
        WHERE meal_time LIKE ? || '%'
        GROUP BY DATE(meal_time)
        ORDER BY day
        """,
        (month_str,),
    ).fetchall()

    # Top phosphorus foods
    top_p = conn.execute(
        """
        SELECT food_name,
               SUM(phosphorus_mg) AS total_phosphorus_mg,
               SUM(potassium_mg) AS total_potassium_mg,
               COUNT(*) AS frequency
        FROM food_logs
        WHERE meal_time LIKE ? || '%'
        GROUP BY food_name
        ORDER BY total_phosphorus_mg DESC
        LIMIT 10
        """,
        (month_str,),
    ).fetchall()

    # Top potassium foods
    top_k = conn.execute(
        """
        SELECT food_name,
               SUM(potassium_mg) AS total_potassium_mg,
               SUM(phosphorus_mg) AS total_phosphorus_mg,
               COUNT(*) AS frequency
        FROM food_logs
        WHERE meal_time LIKE ? || '%'
        GROUP BY food_name
        ORDER BY total_potassium_mg DESC
        LIMIT 10
        """,
        (month_str,),
    ).fetchall()

    # Overall totals
    totals = conn.execute(
        """
        SELECT COALESCE(SUM(phosphorus_mg), 0) AS total_phosphorus_mg,
               COALESCE(SUM(potassium_mg), 0) AS total_potassium_mg,
               COUNT(*) AS total_entries,
               COUNT(DISTINCT DATE(meal_time)) AS days_logged
        FROM food_logs
        WHERE meal_time LIKE ? || '%'
        """,
        (month_str,),
    ).fetchone()

    days_logged = totals["days_logged"] or 1

    # Days that exceeded daily limits
    exceeded_days = [
        {
            "day": d["day"],
            "phosphorus_mg": round(d["phosphorus_mg"], 1),
            "potassium_mg": round(d["potassium_mg"], 1),
            "phosphorus_exceeded": d["phosphorus_mg"] > PHOSPHORUS_DAILY_LIMIT,
            "potassium_exceeded": d["potassium_mg"] > POTASSIUM_DAILY_LIMIT,
        }
        for d in days
        if d["phosphorus_mg"] > PHOSPHORUS_DAILY_LIMIT
        or d["potassium_mg"] > POTASSIUM_DAILY_LIMIT
    ]

    # Foods to avoid: foods with high per-serving value AND high frequency
    # Score = avg_per_time * frequency (total contribution to the month)
    foods_to_avoid_p = conn.execute(
        """
        SELECT food_name,
               SUM(phosphorus_mg) AS total_mg,
               COUNT(*) AS frequency,
               AVG(phosphorus_mg) AS avg_per_time
        FROM food_logs
        WHERE meal_time LIKE ? || '%'
        GROUP BY food_name
        HAVING avg_per_time > ?
        ORDER BY total_mg DESC
        LIMIT 5
        """,
        (month_str, PHOSPHORUS_DAILY_LIMIT * 0.2),  # > 20% of daily limit per serving
    ).fetchall()

    foods_to_avoid_k = conn.execute(
        """
        SELECT food_name,
               SUM(potassium_mg) AS total_mg,
               COUNT(*) AS frequency,
               AVG(potassium_mg) AS avg_per_time
        FROM food_logs
        WHERE meal_time LIKE ? || '%'
        GROUP BY food_name
        HAVING avg_per_time > ?
        ORDER BY total_mg DESC
        LIMIT 5
        """,
        (month_str, POTASSIUM_DAILY_LIMIT * 0.2),  # > 20% of daily limit per serving
    ).fetchall()

    conn.close()
    return {
        "success": True,
        "data": {
            "month": month_str,
            "total_phosphorus_mg": round(totals["total_phosphorus_mg"], 1),
            "total_potassium_mg": round(totals["total_potassium_mg"], 1),
            "total_entries": totals["total_entries"],
            "days_logged": totals["days_logged"],
            "avg_daily_phosphorus_mg": round(
                totals["total_phosphorus_mg"] / days_logged, 1
            ),
            "avg_daily_potassium_mg": round(
                totals["total_potassium_mg"] / days_logged, 1
            ),
            "daily_breakdown": [dict(d) for d in days],
            "exceeded_days": exceeded_days,
            "top_phosphorus_foods": [
                {
                    "food_name": r["food_name"],
                    "total_mg": round(r["total_phosphorus_mg"], 1),
                    "frequency": r["frequency"],
                    "avg_per_time": round(
                        r["total_phosphorus_mg"] / r["frequency"], 1
                    ),
                }
                for r in top_p
            ],
            "top_potassium_foods": [
                {
                    "food_name": r["food_name"],
                    "total_mg": round(r["total_potassium_mg"], 1),
                    "frequency": r["frequency"],
                    "avg_per_time": round(
                        r["total_potassium_mg"] / r["frequency"], 1
                    ),
                }
                for r in top_k
            ],
            "foods_to_avoid": {
                "high_phosphorus": [
                    {
                        "food_name": r["food_name"],
                        "total_mg": round(r["total_mg"], 1),
                        "frequency": r["frequency"],
                        "avg_per_time": round(r["avg_per_time"], 1),
                    }
                    for r in foods_to_avoid_p
                ],
                "high_potassium": [
                    {
                        "food_name": r["food_name"],
                        "total_mg": round(r["total_mg"], 1),
                        "frequency": r["frequency"],
                        "avg_per_time": round(r["avg_per_time"], 1),
                    }
                    for r in foods_to_avoid_k
                ],
            },
        },
        "timestamp": now_bangkok(),
    }


def list_entries(db_path: Path, date_str: str) -> dict:
    conn = get_connection(db_path)
    conn.executescript(SCHEMA_SQL)

    rows = conn.execute(
        """
        SELECT id, food_name, meal_time, meal_period,
               phosphorus_mg, potassium_mg, serving_size, source, notes
        FROM food_logs
        WHERE DATE(meal_time) = ?
        ORDER BY meal_time ASC
        """,
        (date_str,),
    ).fetchall()

    conn.close()
    return {
        "success": True,
        "data": {"date": date_str, "entries": [dict(r) for r in rows]},
        "timestamp": now_bangkok(),
    }


def delete_entry(db_path: Path, entry_id: int) -> dict:
    conn = get_connection(db_path)
    conn.executescript(SCHEMA_SQL)

    # Check if exists
    row = conn.execute(
        "SELECT id, food_name FROM food_logs WHERE id = ?", (entry_id,)
    ).fetchone()

    if not row:
        conn.close()
        return {
            "success": False,
            "error": f"Entry ID {entry_id} not found",
            "timestamp": now_bangkok(),
        }

    food_name = row["food_name"]
    conn.execute("DELETE FROM food_logs WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()
    return {
        "success": True,
        "data": {"deleted_id": entry_id, "food_name": food_name},
        "timestamp": now_bangkok(),
    }


# ── CLI ──────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Food Tracker DB CLI")

    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--init", action="store_true", help="Initialize database")
    action.add_argument("--log", action="store_true", help="Log a food entry")
    action.add_argument("--search", metavar="QUERY", help="Search food names")
    action.add_argument(
        "--report", choices=["daily", "monthly"], help="Generate report"
    )
    action.add_argument("--list", action="store_true", help="List entries for a date")
    action.add_argument("--delete", type=int, metavar="ID", help="Delete entry by ID")

    # --log arguments
    parser.add_argument("--food", help="Food name")
    parser.add_argument("--meal-time", help="ISO datetime (default: now)")
    parser.add_argument("--phosphorus", type=float, help="Phosphorus in mg")
    parser.add_argument("--potassium", type=float, help="Potassium in mg")
    parser.add_argument("--serving", help="Serving size description")
    parser.add_argument(
        "--meal-period", help="Meal period (เช้า/กลางวัน/เย็น/ก่อนนอน)"
    )
    parser.add_argument(
        "--source", default="web", choices=["web", "ai_estimate"], help="Data source"
    )
    parser.add_argument("--notes", help="Additional notes")

    # --report / --list arguments
    parser.add_argument("--date", help="Date YYYY-MM-DD (default: today)")
    parser.add_argument("--month", help="Month YYYY-MM (default: this month)")

    # DB path override
    parser.add_argument("--db", default=str(DB_PATH), help="Database path override")

    args = parser.parse_args()
    db_path = Path(args.db)

    try:
        if args.init:
            output_json(init_db(db_path))

        elif args.log:
            for field in ["food", "phosphorus", "potassium"]:
                if getattr(args, field) is None:
                    error_exit(f"--{field} is required for --log")

            meal_time = args.meal_time
            if not meal_time or meal_time == "now":
                meal_time = datetime.now(BANGKOK_TZ).strftime("%Y-%m-%dT%H:%M:%S")

            output_json(
                insert_log(
                    db_path,
                    food_name=args.food,
                    meal_time=meal_time,
                    phosphorus_mg=args.phosphorus,
                    potassium_mg=args.potassium,
                    serving_size=args.serving,
                    meal_period=args.meal_period,
                    source=args.source,
                    notes=args.notes,
                )
            )

        elif args.search is not None:
            output_json(search_foods(db_path, args.search))

        elif args.report == "daily":
            date_str = args.date or datetime.now(BANGKOK_TZ).strftime("%Y-%m-%d")
            output_json(daily_report(db_path, date_str))

        elif args.report == "monthly":
            month_str = args.month or datetime.now(BANGKOK_TZ).strftime("%Y-%m")
            output_json(monthly_report(db_path, month_str))

        elif args.list:
            date_str = args.date or datetime.now(BANGKOK_TZ).strftime("%Y-%m-%d")
            output_json(list_entries(db_path, date_str))

        elif args.delete is not None:
            output_json(delete_entry(db_path, args.delete))

    except Exception as e:
        error_exit(str(e))


if __name__ == "__main__":
    main()
