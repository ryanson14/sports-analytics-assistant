"""
Format player stats and context into a clean prompt for Ollama.
"""
from typing import Any


def format_game_log_summary(games: list[dict[str, Any]], max_games: int = 10) -> str:
    """Turn recent game log list into a short readable summary."""
    if not games:
        return "No game log data available."
    lines = []
    for i, g in enumerate(games[:max_games]):
        pts = g.get("PTS", "-")
        reb = g.get("REB", "-")
        ast = g.get("AST", "-")
        date = g.get("DATE", "?")
        opp = g.get("OPP", "?")
        lines.append(f"  {date} vs {opp}: PTS {pts}, REB {reb}, AST {ast}")
    return "Recent games:\n" + "\n".join(lines) if lines else "No game log data available."


def build_prompt(
    player_name: str,
    user_query: str,
    games: list[dict[str, Any]],
    fantasy_avgs: dict[str, Any],
) -> str:
    """
    Build a single prompt string for Ollama with player name, user question,
    game log summary, and fantasy averages.
    """
    game_summary = format_game_log_summary(games)
    ppg = fantasy_avgs.get("stats_ppg") or {}
    fantasy_ppg = fantasy_avgs.get("fantasy_ppg", 0)
    games_used = fantasy_avgs.get("games_used", 0)

    stats_block = (
        f"Fantasy average: {fantasy_ppg} PPG (over {games_used} games). "
        f"Stat averages: PTS {ppg.get('PTS', 0)}, REB {ppg.get('REB', 0)}, "
        f"AST {ppg.get('AST', 0)}, STL {ppg.get('STL', 0)}, BLK {ppg.get('BLK', 0)}, TOV {ppg.get('TOV', 0)}."
    )

    return (
        "You are a sports analytics assistant. Answer concisely based on the following data.\n\n"
        f"Player: {player_name}\n\n"
        f"{game_summary}\n\n"
        f"{stats_block}\n\n"
        f"Question: {user_query}\n\n"
        "Answer:"
    ).strip()
