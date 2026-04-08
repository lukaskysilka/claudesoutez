"""
Scraper Service
---------------
Extracts price and review count from:
  1. Search snippet (fast, no extra request)
  2. JSON-LD structured data on the product page
  3. Raw page text (fallback regex)

All extraction is best-effort; callers get None when nothing is found.
"""

import json
import logging
import re
from typing import Optional, Tuple

import httpx
from bs4 import BeautifulSoup

from config import settings

logger = logging.getLogger(__name__)

# ── Regex patterns ────────────────────────────────────────────────────────────
PRICE_PATTERNS: dict[str, list[str]] = {
    "CZK": [
        r"(\d[\d\s]*(?:[.,]\d{1,2})?)\s*(?:Kč|CZK)",
        r"(?:Kč|CZK)\s*(\d[\d\s]*(?:[.,]\d{1,2})?)",
    ],
    "EUR": [
        r"€\s*(\d+(?:[.,]\d{1,2})?)",
        r"(\d+(?:[.,]\d{1,2})?)\s*(?:€|EUR)",
    ],
    "USD": [
        r"\$\s*(\d+(?:[.,]\d{1,2})?)",
        r"(\d+(?:[.,]\d{1,2})?)\s*USD",
    ],
}

REVIEW_PATTERNS = [
    r"(\d[\d,\s]+)\s*(?:reviews?|recenzí|Bewertungen|ratings?|hodnocení)",
    r"(?:reviews?|recenzí|ratings?|hodnocení)[:\s]+(\d[\d,\s]+)",
    r"(\d[\d,\s]+)\s*(?:verified purchases?|zákazník)",
    r"Based on\s+(\d[\d,\s]+)",
]

_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


class ScraperService:
    # ── Public API ─────────────────────────────────────────────────────────────

    def extract_from_snippet(
        self, snippet: str, currency: str
    ) -> Tuple[Optional[float], Optional[int]]:
        """Fast extraction from the search result snippet (no HTTP request)."""
        return self._extract_price(snippet, currency), self._extract_reviews(snippet)

    async def scrape_page(
        self, url: str, currency: str
    ) -> Tuple[Optional[float], Optional[int]]:
        """Full page scrape: structured data first, then raw text fallback."""
        try:
            async with httpx.AsyncClient(
                follow_redirects=True,
                timeout=settings.REQUEST_TIMEOUT,
                headers={"User-Agent": _USER_AGENT, "Accept-Language": "en-US,en;q=0.5"},
            ) as client:
                resp = await client.get(url)
                if resp.status_code != 200:
                    return None, None

                soup = BeautifulSoup(resp.text, "lxml")
                price, reviews = self._from_structured_data(soup)

                if price is None or reviews is None:
                    text = soup.get_text(" ", strip=True)
                    price = price or self._extract_price(text, currency)
                    reviews = reviews or self._extract_reviews(text)

                return price, reviews
        except Exception as exc:
            logger.debug("Scrape failed [%s]: %s", url, exc)
            return None, None

    # ── Internal helpers ───────────────────────────────────────────────────────

    def _extract_price(self, text: str, currency: str) -> Optional[float]:
        patterns = PRICE_PATTERNS.get(currency, PRICE_PATTERNS["USD"])
        for pattern in patterns:
            m = re.search(pattern, text, re.IGNORECASE)
            if m:
                raw = m.group(1).replace(" ", "").replace(",", ".")
                try:
                    value = float(raw)
                    if 0.5 < value < 50_000:
                        return value
                except ValueError:
                    continue
        return None

    def _extract_reviews(self, text: str) -> Optional[int]:
        for pattern in REVIEW_PATTERNS:
            m = re.search(pattern, text, re.IGNORECASE)
            if m:
                raw = m.group(1).replace(",", "").replace(" ", "")
                try:
                    value = int(raw)
                    if 0 < value < 10_000_000:
                        return value
                except ValueError:
                    continue
        return None

    def _from_structured_data(
        self, soup: BeautifulSoup
    ) -> Tuple[Optional[float], Optional[int]]:
        for tag in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(tag.string or "{}")
            except (json.JSONDecodeError, TypeError):
                continue

            items = data if isinstance(data, list) else [data]
            for item in items:
                price, reviews = self._parse_ld_item(item)
                if price or reviews:
                    return price, reviews
        return None, None

    @staticmethod
    def _parse_ld_item(data: dict) -> Tuple[Optional[float], Optional[int]]:
        price: Optional[float] = None
        reviews: Optional[int] = None

        offers = data.get("offers") or {}
        if isinstance(offers, list):
            offers = offers[0] if offers else {}
        if isinstance(offers, dict):
            try:
                v = float(offers.get("price") or 0)
                price = v if v > 0 else None
            except (TypeError, ValueError):
                pass

        agg = data.get("aggregateRating") or {}
        if isinstance(agg, dict):
            raw = agg.get("reviewCount") or agg.get("ratingCount") or 0
            try:
                v = int(float(raw))
                reviews = v if v > 0 else None
            except (TypeError, ValueError):
                pass

        return price, reviews
