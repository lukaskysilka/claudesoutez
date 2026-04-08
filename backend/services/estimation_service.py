"""
Estimation Service
------------------
Core market-size formula:

    Estimated Sales   = Reviews × REVIEW_TO_SALES_RATIO
    Estimated Revenue = Estimated Sales × Price
    Market Size (USD) = Σ revenue_i × fx_rate_i   (across all competitors)

Industry default values are applied when price or review data cannot be scraped,
so the output is always a plausible estimate (clearly flagged in the response).
"""

import logging
from typing import Dict, List

from config import settings
from models import Competitor, MarketEstimationResponse, RegionSummary

logger = logging.getLogger(__name__)

# ── FX rates (approx). Replace with a live feed if needed. ─────────────────
FX_TO_USD: Dict[str, float] = {
    "USD": 1.00,
    "EUR": 1.08,
    "CZK": 0.043,
}

# ── Industry defaults when scraped data is unavailable ──────────────────────
# Based on typical sports/energy supplement markets.
REGION_DEFAULTS: Dict[str, Dict] = {
    "CZ": {"price": 499.0,  "reviews": 45},   # ~499 CZK, small CZ market
    "EU": {"price":  34.99, "reviews": 180},   # ~35 EUR mid-range EU product
    "USA": {"price": 44.99, "reviews": 450},   # ~45 USD Amazon-style product
}


class EstimationService:
    def __init__(self, ratio: int | None = None) -> None:
        self.ratio = ratio or settings.REVIEW_TO_SALES_RATIO

    # ── Public API ─────────────────────────────────────────────────────────────

    def build_response(
        self,
        product_name: str,
        ingredients: str,
        enriched: Dict[str, List[Dict]],
    ) -> MarketEstimationResponse:
        competitors: List[Competitor] = []
        for region, results in enriched.items():
            for item in results:
                competitors.append(self._estimate_competitor(item, region))

        summaries = [
            self._region_summary(competitors, region)
            for region in ["CZ", "EU", "USA"]
        ]

        total_usd = sum(s.total_revenue_usd for s in summaries)

        return MarketEstimationResponse(
            product_name=product_name,
            ingredients=ingredients,
            competitors=competitors,
            region_summaries=summaries,
            total_market_size_usd=round(total_usd, 2),
            review_to_sales_ratio=self.ratio,
            methodology=(
                f"Top competitors identified via Serper/Google search. "
                f"Reviews × {self.ratio} = estimated annual sales. "
                f"Revenue = Sales × Price. "
                f"Missing values filled with regional industry defaults "
                f"(flagged in competitor table). "
                f"FX: 1 EUR = {FX_TO_USD['EUR']} USD, 1 CZK = {FX_TO_USD['CZK']} USD."
            ),
        )

    # ── Internal helpers ───────────────────────────────────────────────────────

    def _estimate_competitor(self, item: Dict, region: str) -> Competitor:
        defaults = REGION_DEFAULTS[region]

        price = item.get("price")
        reviews = item.get("reviews")
        price_is_default = price is None
        reviews_is_default = reviews is None

        price = price if price is not None else defaults["price"]
        reviews = reviews if reviews is not None else defaults["reviews"]

        estimated_sales = reviews * self.ratio
        estimated_revenue = round(estimated_sales * price, 2)

        return Competitor(
            name=item.get("title", "Unknown")[:120],
            url=item.get("url", ""),
            region=region,
            currency=item.get("currency", "USD"),
            price=round(price, 2),
            reviews=reviews,
            estimated_sales=estimated_sales,
            estimated_revenue=estimated_revenue,
            price_is_default=price_is_default,
            reviews_is_default=reviews_is_default,
        )

    def _region_summary(
        self, competitors: List[Competitor], region: str
    ) -> RegionSummary:
        region_comps = [c for c in competitors if c.region == region]
        currency_map = {"CZ": "CZK", "EU": "EUR", "USA": "USD"}
        currency = currency_map[region]

        if not region_comps:
            return RegionSummary(
                region=region,
                currency=currency,
                total_revenue=0.0,
                total_revenue_usd=0.0,
                total_competitors=0,
                avg_price=0.0,
            )

        total_revenue = sum(c.estimated_revenue or 0 for c in region_comps)
        avg_price = sum(c.price or 0 for c in region_comps) / len(region_comps)
        fx = FX_TO_USD.get(currency, 1.0)

        return RegionSummary(
            region=region,
            currency=currency,
            total_revenue=round(total_revenue, 2),
            total_revenue_usd=round(total_revenue * fx, 2),
            total_competitors=len(region_comps),
            avg_price=round(avg_price, 2),
        )
