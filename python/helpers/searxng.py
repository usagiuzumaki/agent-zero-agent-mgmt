"""
Web search helper using Tavily.

This mimics the old SearxNG JSON structure so that
python/tools/search_engine.py can consume it without changes.

Return shape:

{
    "results": [
        {
            "title": str,
            "url": str,
            "content": str,
        },
        ...
    ]
}
"""

import os
from typing import List, Dict, Any
import aiohttp

try:
    from python.helpers.print_style import PrintStyle
    logger = PrintStyle()
except Exception:
    logger = None


TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
TAVILY_URL = "https://api.tavily.com/search"


async def search(query: str, max_results: int = 5) -> Dict[str, List[Dict[str, Any]]]:
    """
    Perform a web search using Tavily and return a dict with a `results` list,
    to match the expected SearxNG-style response.
    """
    # If there's no API key, fail softly
    if not TAVILY_API_KEY:
        if logger:
            logger.error("TAVILY_API_KEY not set; returning empty search results.")
        return {"results": []}

    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "max_results": max_results,
        "include_answer": False,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(TAVILY_URL, json=payload, timeout=15) as resp:
                resp.raise_for_status()
                data = await resp.json()
    except Exception as e:
        if logger:
            logger.error(f"Tavily search failed: {e}")
        return {"results": []}

    items: List[Dict[str, Any]] = []
    for r in data.get("results", [])[:max_results]:
        items.append(
            {
                "title": r.get("title") or "",
                "url": r.get("url") or "",
                "content": r.get("content") or "",
            }
        )

    return {"results": items}
