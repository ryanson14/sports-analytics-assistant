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


def build_comparison_prompt(
    player1_name: str,
    player2_name: str,
    games1: list[dict[str, Any]],
    games2: list[dict[str, Any]],
    fantasy_avgs1: dict[str, Any],
    fantasy_avgs2: dict[str, Any],
    user_query: str,
    max_games_each: int = 10,
) -> str:
    """
    Build a prompt for comparing two players: stats and recent games side by side,
    then the user's comparison question.
    """
    ppg1 = fantasy_avgs1.get("stats_ppg") or {}
    ppg2 = fantasy_avgs2.get("stats_ppg") or {}
    fp1 = fantasy_avgs1.get("fantasy_ppg", 0)
    fp2 = fantasy_avgs2.get("fantasy_ppg", 0)
    n1 = fantasy_avgs1.get("games_used", 0)
    n2 = fantasy_avgs2.get("games_used", 0)

    stats1 = (
        f"Fantasy PPG: {fp1} ({n1} games). "
        f"PTS {ppg1.get('PTS', 0)}, REB {ppg1.get('REB', 0)}, AST {ppg1.get('AST', 0)}, "
        f"STL {ppg1.get('STL', 0)}, BLK {ppg1.get('BLK', 0)}, TOV {ppg1.get('TOV', 0)}."
    )
    stats2 = (
        f"Fantasy PPG: {fp2} ({n2} games). "
        f"PTS {ppg2.get('PTS', 0)}, REB {ppg2.get('REB', 0)}, AST {ppg2.get('AST', 0)}, "
        f"STL {ppg2.get('STL', 0)}, BLK {ppg2.get('BLK', 0)}, TOV {ppg2.get('TOV', 0)}."
    )

    summary1 = format_game_log_summary(games1, max_games=max_games_each)
    summary2 = format_game_log_summary(games2, max_games=max_games_each)

    return (
        "You are a direct sports analytics assistant. Answer the user's question with a clear recommendation based only on the stats provided. Do not refuse to make a pick or recommendation — the user wants a direct answer, not a disclaimer.\n\n"
        "--- PLAYER 1 ---\n"
        f"Name: {player1_name}\n"
        f"{stats1}\n"
        f"{summary1}\n\n"
        "--- PLAYER 2 ---\n"
        f"Name: {player2_name}\n"
        f"{stats2}\n"
        f"{summary2}\n\n"
        f"Question: {user_query}\n\n"
        "Answer:"
    ).strip()
