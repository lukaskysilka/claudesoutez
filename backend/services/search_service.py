"""
Search Service
--------------
Uses Serper API (https://serper.dev) to find competing products in CZ, EU, USA.
Swap API key via SERPER_API_KEY in .env.  To plug in a different provider
(e.g. Google Custom Search), subclass BaseSearchService and override _fetch().
"""

import logging
from typing import Any, Dict, List

import httpx

from config import settings

logger = logging.getLogger(__name__)

# ── Region configuration ────────────────────────────────────────────────────
REGIONS: Dict[str, Dict[str, Any]] = {
    "CZ": {
        "gl": "cz",
        "hl": "cs",
        "currency": "CZK",
        "queries": [
            "{product} koupit",
            "{product} cena",
            "{ingredients} doplněk stravy",
        ],
    },
    "EU": {
        "gl": "de",         # Germany as EU proxy → decent EUR prices
        "hl": "en",
        "currency": "EUR",
        "queries": [
            "{product} supplement buy europe",
            "{product} buy EU",
            "{ingredients} supplement",
        ],
    },
    "USA": {
        "gl": "us",
        "hl": "en",
        "currency": "USD",
        "queries": [
            "{product} supplement buy",
            "{product} amazon",
            "{ingredients} supplement usa",
        ],
    },
}


class SearchService:
    SERPER_URL = "https://google.serper.dev/search"

    def __init__(self) -> None:
        self._headers = {
            "X-API-KEY": settings.SERPER_API_KEY,
            "Content-Type": "application/json",
        }

    async def search_all_regions(
        self, product_name: str, ingredients: str
    ) -> Dict[str, List[Dict]]:
        results: Dict[str, List[Dict]] = {}
        for region in REGIONS:
            results[region] = await self._search_region(product_name, ingredients, region)
        return results

    async def _search_region(
        self, product_name: str, ingredients: str, region: str
    ) -> List[Dict]:
        cfg = REGIONS[region]
        seen_urls: set = set()
        hits: List[Dict] = []

        # Truncate ingredients so queries stay reasonable
        short_ingredients = ingredients[:60]

        async with httpx.AsyncClient(timeout=15) as client:
            for template in cfg["queries"]:
                if len(hits) >= settings.MAX_COMPETITORS_PER_REGION:
                    break

                query = template.format(
                    product=product_name,
                    ingredients=short_ingredients,
                )
                payload = {
                    "q": query,
                    "gl": cfg["gl"],
                    "hl": cfg["hl"],
                    "num": 10,
                }

                try:
                    resp = await client.post(
                        self.SERPER_URL, headers=self._headers, json=payload
                    )
                    resp.raise_for_status()
                    organic = resp.json().get("organic", [])
                except Exception as exc:
                    logger.warning("Serper error [%s / %s]: %s", region, query, exc)
                    continue

                for item in organic:
                    url = item.get("link", "")
                    if url and url not in seen_urls:
                        seen_urls.add(url)
                        hits.append(
                            {
                                "title": item.get("title", ""),
                                "url": url,
                                "snippet": item.get("snippet", ""),
                                "region": region,
                                "currency": cfg["currency"],
                            }
                        )
                        if len(hits) >= settings.MAX_COMPETITORS_PER_REGION:
                            break

        logger.info("Region %s: found %d competitors", region, len(hits))
        return hits
