import logging
import time

import httpx

logger = logging.getLogger(__name__)

_puzzle_cache: tuple[float, dict] | None = None
PUZZLE_CACHE_TTL = 3600  # 1 hour


async def get_daily_puzzle() -> dict:
    global _puzzle_cache

    if _puzzle_cache:
        ts, data = _puzzle_cache
        if time.time() - ts < PUZZLE_CACHE_TTL:
            return data

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get("https://lichess.org/api/puzzle/daily")
            resp.raise_for_status()
            data = resp.json()

        puzzle = {
            "id": data.get("puzzle", {}).get("id"),
            "fen": data.get("game", {}).get("pgn", ""),
            "initialPly": data.get("puzzle", {}).get("initialPly", 0),
            "solution": data.get("puzzle", {}).get("solution", []),
            "rating": data.get("puzzle", {}).get("rating", 0),
            "themes": data.get("puzzle", {}).get("themes", []),
            "gameUrl": f"https://lichess.org/training/{data.get('puzzle', {}).get('id', '')}",
        }

        _puzzle_cache = (time.time(), puzzle)
        return puzzle
    except Exception:
        logger.exception("Failed to fetch Lichess daily puzzle")
        if _puzzle_cache:
            return _puzzle_cache[1]
        return {"error": "Could not fetch puzzle"}
