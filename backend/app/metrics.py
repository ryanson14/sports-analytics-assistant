"""
Calculate fantasy scoring averages from scraped game log data.
"""
from typing import Any

# Default fantasy points per stat (common league settings; customizable)
DEFAULT_SCORING: dict[str, float] = {
    "PTS": 1.0,
    "REB": 1.2,
    "AST": 1.5,
    "STL": 3.0,
    "BLK": 3.0,
    "TOV": -1.0,
}


def _safe_float(val: Any) -> float:
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, str):
        try:
            return float(val.replace(",", "").strip() or 0)
        except ValueError:
            return 0.0
    return 0.0


def fantasy_points_for_game(game: dict[str, Any], scoring: dict[str, float] | None = None) -> float:
    """Compute fantasy points for a single game using the given scoring rules."""
    scoring = scoring or DEFAULT_SCORING
    total = 0.0
    for stat, pts_per in scoring.items():
        total += _safe_float(game.get(stat, 0)) * pts_per
    return total


def fantasy_averages(
    games: list[dict[str, Any]],
    scoring: dict[str, float] | None = None,
) -> dict[str, Any]:
    """
    From a list of game log dicts, compute:
    - fantasy_ppg: average fantasy points per game
    - stats_ppg: per-game averages for PTS, REB, AST, STL, BLK, TOV
    - games_used: number of games in the sample
    """
    scoring = scoring or DEFAULT_SCORING
    if not games:
        return {
            "fantasy_ppg": 0.0,
            "stats_ppg": {k: 0.0 for k in ("PTS", "REB", "AST", "STL", "BLK", "TOV")},
            "games_used": 0,
        }

    totals: dict[str, float] = {k: 0.0 for k in ("PTS", "REB", "AST", "STL", "BLK", "TOV")}
    fantasy_sum = 0.0

    for g in games:
        fantasy_sum += fantasy_points_for_game(g, scoring)
        for k in totals:
            totals[k] += _safe_float(g.get(k, 0))

    n = len(games)
    return {
        "fantasy_ppg": round(fantasy_sum / n, 2),
        "stats_ppg": {k: round(totals[k] / n, 2) for k in totals},
        "games_used": n,
    }
