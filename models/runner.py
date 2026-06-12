"""
Model evaluation runner.

Loads match + year data (from DB or CSV), iterates matches chronologically,
and collects win-probability predictions from any Model implementation.

Usage (from the models/ directory)
-----------------------------------
    poetry run python runner.py --model epa --matches-csv matches.csv --years-csv years.csv
    poetry run python runner.py --model wins --db "postgresql://root@localhost:26257/statbotics3?sslmode=disable"
"""

from __future__ import annotations

from typing import Optional, Tuple

import pandas as pd

from base import Model


# ── Data loading ──────────────────────────────────────────────────────────────

_MATCH_QUERY = """
    SELECT
        m.year, m.event, m.comp_level, m.elim, m.time,
        m.red_1, m.red_2, m.red_3,
        m.blue_1, m.blue_2, m.blue_3,
        m.red_score, m.red_no_foul,
        m.blue_score, m.blue_no_foul,
        m.winner
    FROM matches m
    WHERE m.winner   IS NOT NULL
      AND m.red_score  IS NOT NULL
      AND m.blue_score IS NOT NULL
    ORDER BY m.year, m.time
"""

_YEAR_QUERY = """
    SELECT year, score_mean, score_sd, no_foul_mean
    FROM years
    ORDER BY year
"""


def load_from_db(conn_str: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Connect to CockroachDB/PostgreSQL and return (matches, years)."""
    import sqlalchemy

    engine = sqlalchemy.create_engine(conn_str)
    with engine.connect() as conn:
        matches = pd.read_sql(_MATCH_QUERY, conn)
        years = pd.read_sql(_YEAR_QUERY, conn)
    return matches, years


def load_from_csv(
    matches_path: str = "matches.csv",
    years_path: str = "years.csv",
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load pre-exported CSV files."""
    return pd.read_csv(matches_path), pd.read_csv(years_path)


# ── Evaluation loop ───────────────────────────────────────────────────────────

def evaluate(model: Model, matches: pd.DataFrame, years: pd.DataFrame) -> pd.DataFrame:
    """
    Iterate matches chronologically, predict then update.

    Returns a DataFrame with one row per match:
        year, event, comp_level, elim, winner,
        pred          – P(red wins)
        red_score, blue_score          – post-foul scores
        red_no_foul, blue_no_foul      – pre-foul scores (NaN pre-2016)
    """
    year_stats = (
        years.set_index("year")
        [["score_mean", "score_sd", "no_foul_mean"]]
        .to_dict("index")
    )

    records = []
    current_year: Optional[int] = None

    for _, m in matches.iterrows():
        year = int(m["year"])

        if year != current_year:
            current_year = year
            stats = year_stats.get(year, {})
            model.start_year(
                year,
                score_mean=float(stats.get("score_mean") or 0),
                score_sd=float(stats.get("score_sd") or 1),
                no_foul_mean=float(stats.get("no_foul_mean") or 0),
            )

        def _int(v) -> Optional[int]:
            return None if pd.isna(v) else int(v)

        red1, red2, red3 = _int(m["red_1"]), _int(m["red_2"]), _int(m["red_3"])
        blue1, blue2, blue3 = _int(m["blue_1"]), _int(m["blue_2"]), _int(m["blue_3"])
        if red1 is None or red2 is None or blue1 is None or blue2 is None:
            continue

        winner = str(m["winner"]).upper()
        red_score = float(m["red_score"])
        blue_score = float(m["blue_score"])
        elim = bool(m["elim"])

        pred = model.predict(red1, red2, red3, blue1, blue2, blue3)
        model.update(
            red1, red2, red3, blue1, blue2, blue3,
            winner, red_score, blue_score, elim=elim,
        )

        records.append(
            {
                "year": year,
                "event": m["event"],
                "comp_level": m["comp_level"],
                "elim": elim,
                "winner": winner,
                "pred": pred,
                "red_score": red_score,
                "blue_score": blue_score,
                "red_no_foul": m.get("red_no_foul"),
                "blue_no_foul": m.get("blue_no_foul"),
            }
        )

    return pd.DataFrame(records)


# ── Metrics ───────────────────────────────────────────────────────────────────

def _compute(df: pd.DataFrame) -> dict:
    """Accuracy and Brier score on a slice of predictions (ties excluded)."""
    df = df[df["winner"].isin({"RED", "BLUE"})].copy()
    if df.empty:
        return {"count": 0, "accuracy": None, "brier": None}

    actual = (df["winner"] == "RED").astype(float)
    correct = (df["pred"] >= 0.5) == (actual == 1)
    return {
        "count": len(df),
        "accuracy": float(correct.mean()),
        "brier": float(((df["pred"] - actual) ** 2).mean()),
    }


def _is_champs(event_series: pd.Series) -> pd.Series:
    """True for championship events (key contains 'cmp')."""
    return event_series.str.contains("cmp", case=False, na=False)


def metrics(preds: pd.DataFrame) -> dict:
    """
    Return a dict with overall, champs, and per-year accuracy + Brier scores.

    Example output::

        {
            "overall": {"count": 120000, "accuracy": 0.721, "brier": 0.183},
            "champs":  {"count":   8000, "accuracy": 0.731, "brier": 0.178},
            "by_year": {
                2024: {"all": {...}, "champs": {...}},
                ...
            },
        }
    """
    champs_mask = _is_champs(preds["event"])

    result: dict = {
        "overall": _compute(preds),
        "champs": _compute(preds[champs_mask]),
        "by_year": {},
    }

    for year in sorted(preds["year"].unique()):
        year_mask = preds["year"] == year
        result["by_year"][int(year)] = {
            "all": _compute(preds[year_mask]),
            "champs": _compute(preds[year_mask & champs_mask]),
        }

    return result


# ── Reporting ─────────────────────────────────────────────────────────────────

def report(preds: pd.DataFrame) -> None:
    """Print a formatted summary table to stdout."""
    m = metrics(preds)

    def _fmt(d: dict) -> str:
        if d["count"] == 0:
            return f"{'—':>6}  {'—':>5}  {'—':>6}"
        return f"{d['count']:>6}  {d['accuracy']:.3f}  {d['brier']:.4f}"

    col = "  "
    print(f"{'year':>6}{col}{'n':>6}  {'acc':>5}  {'brier':>6}{col}{'champs_n':>8}  {'champs_acc':>10}  {'champs_brier':>12}")
    print("-" * 72)

    for year, yd in m["by_year"].items():
        print(f"{year:>6}{col}{_fmt(yd['all'])}{col}{_fmt(yd['champs'])}")

    print("-" * 72)
    print(f"{'ALL':>6}{col}{_fmt(m['overall'])}{col}{_fmt(m['champs'])}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    import argparse

    from epa_model import EPAModel
    from wins_model import WinsModel

    parser = argparse.ArgumentParser(description="Evaluate a match prediction model.")
    parser.add_argument("--model", default="epa", choices=["epa", "wins"],
                        help="Model to evaluate (default: epa)")
    parser.add_argument("--db",
                        default="postgresql://root@localhost:26257/statbotics3?sslmode=disable",
                        help="SQLAlchemy connection string (used if --matches-csv is not set)")
    parser.add_argument("--matches-csv", default=None,
                        help="Path to matches CSV exported from data.sql")
    parser.add_argument("--years-csv", default="years.csv",
                        help="Path to years CSV exported from data.sql (default: years.csv)")
    args = parser.parse_args()

    model: Model = EPAModel() if args.model == "epa" else WinsModel()

    if args.matches_csv:
        matches, years = load_from_csv(args.matches_csv, args.years_csv)
    else:
        matches, years = load_from_db(args.db)

    print(f"Loaded {len(matches):,} matches across {matches['year'].nunique()} years.\n")
    preds = evaluate(model, matches, years)
    report(preds)


if __name__ == "__main__":
    main()
