"""
Scrape player game logs from StatMuse using BeautifulSoup.
"""
import re
from typing import Any
from urllib.parse import quote_plus

import httpx
from bs4 import BeautifulSoup

STATMUSE_BASE = "https://www.statmuse.com"
GAME_LOG_COLUMNS = ("DATE", "TM", "OPP", "SCORE", "MIN", "PTS", "REB", "AST", "STL", "BLK", "TOV")

# Match StatMuse player URL slug with trailing numeric ID (e.g. tyrese-maxey-10164)
_PLAYER_SLUG_WITH_ID_RE = re.compile(r"/nba/player/([a-z0-9]+(?:-[a-z0-9]+)*-\d+)/", re.I)


def _slug(name: str) -> str:
    """Turn player name into URL-friendly StatMuse-style slug (lowercase, hyphens)."""
    return re.sub(r"[^\w\s-]", "", name.lower()).strip().replace(" ", "-")


async def _search_player_slug(query: str, client: httpx.AsyncClient) -> str | None:
    """
    Search StatMuse for a player by name; return the first player slug with numeric ID, or None.
    Uses /nba/ask?q= so that we can resolve e.g. 'Tyrese Maxey' -> 'tyrese-maxey-10164'.
    """
    q = query.strip().replace("-", " ")
    if not q:
        return None
    url = f"{STATMUSE_BASE}/nba/ask?q={quote_plus(q)}"
    try:
        resp = await client.get(url)
        resp.raise_for_status()
    except httpx.HTTPError:
        return None
    soup = BeautifulSoup(resp.text, "html.parser")
    for a in soup.find_all("a", href=True):
        href = a.get("href") or ""
        m = _PLAYER_SLUG_WITH_ID_RE.search(href)
        if m:
            return m.group(1).lower()
    return None


def _parse_number(s: str) -> float:
    """Parse a table cell to number; return 0 if empty or invalid."""
    s = (s or "").strip().replace(",", "")
    if not s or s in ("-", "—"):
        return 0.0
    try:
        return float(s)
    except ValueError:
        return 0.0


async def _fetch_game_logs(client: httpx.AsyncClient, slug: str) -> list[dict[str, Any]]:
    """Fetch and parse game log table for a given slug; returns [] on HTTP error or no table."""
    url = f"{STATMUSE_BASE}/nba/player/{slug}/game-log"
    try:
        resp = await client.get(url)
        resp.raise_for_status()
    except httpx.HTTPError:
        return []
    soup = BeautifulSoup(resp.text, "html.parser")
    games: list[dict[str, Any]] = []

    for table in soup.find_all("table"):
        thead = table.find("thead")
        tbody = table.find("tbody") or table
        if not thead:
            continue

        headers = [th.get_text(strip=True).upper().replace(" ", "") for th in thead.find_all("th")]
        if not headers:
            continue

        col_map: dict[int, str] = {}
        for idx, h in enumerate(headers):
            for known in GAME_LOG_COLUMNS:
                if known in h or h in known:
                    col_map[idx] = known
                    break
            if idx not in col_map and h:
                col_map[idx] = h

        if not col_map:
            continue

        rows = (tbody.find_all("tr") if tbody != table else table.find_all("tr"))[1:]
        for tr in rows:
            cells = tr.find_all(["td", "th"])
            if not cells:
                continue
            row: dict[str, Any] = {}
            for i, cell in enumerate(cells):
                if i not in col_map:
                    continue
                key = col_map[i]
                text = cell.get_text(strip=True)
                if key in ("PTS", "REB", "AST", "STL", "BLK", "TOV", "MIN", "FGM", "FGA", "3PM", "3PA", "FTM", "FTA"):
                    row[key] = _parse_number(text)
                else:
                    row[key] = text
            if row:
                games.append(row)

        if games:
            break

    return games


async def scrape_player_game_logs(
    player_slug: str,
    *,
    client: httpx.AsyncClient | None = None,
) -> list[dict[str, Any]]:
    """
    Fetch and parse game log table for a player from StatMuse.
    Accepts a normal name (e.g. 'Tyrese Maxey') or a slug ('tyrese-maxey', 'tyrese-maxey-10164').
    Names are converted to a URL-friendly slug for the first request. If that returns no results,
    StatMuse is searched to find the correct player slug with numeric ID and the game log is
    fetched again.
    Returns list of dicts, one per game, with keys like DATE, PTS, REB, AST, etc.
    """
    raw_input = player_slug.strip()
    is_slug_like = bool(re.match(r"^[\w-]+$", raw_input))
    slug = raw_input if is_slug_like else _slug(raw_input)
    search_query = raw_input.replace("-", " ").strip()

    own_client = client is None
    if own_client:
        client = httpx.AsyncClient(
            follow_redirects=True,
            headers={"User-Agent": "SportsAnalytics/1.0"},
            timeout=15.0,
        )

    try:
        games = await _fetch_game_logs(client, slug)
        if not games and search_query:
            found_slug = await _search_player_slug(search_query, client)
            if found_slug and found_slug != slug:
                games = await _fetch_game_logs(client, found_slug)
        return games
    finally:
        if own_client:
            await client.aclose()
