from __future__ import annotations

from collections import defaultdict

from app.config import settings
from app.models import ProductSignal, RegionEstimate


def to_usd(price: float, currency: str) -> float:
    if currency == "CZK":
        return price / settings.usd_to_czk
    if currency == "EUR":
        return (price * settings.eur_to_czk) / settings.usd_to_czk
    return price


def estimate_market_size(products: list[ProductSignal]) -> list[RegionEstimate]:
    grouped: dict[str, list[ProductSignal]] = defaultdict(list)
    for product in products:
        grouped[product.region].append(product)

    region_estimates: list[RegionEstimate] = []
    for region, competitors in grouped.items():
        region_total_usd = 0.0
        for product in competitors:
            usd_price = to_usd(product.avg_price, product.currency)
            region_total_usd += product.reviews * settings.review_to_sales_multiplier * usd_price

        region_estimates.append(
            RegionEstimate(
                region=region,
                estimated_market_volume_usd=region_total_usd,
                estimated_market_volume_czk=region_total_usd * settings.usd_to_czk,
                competitors=competitors,
            )
        )

    return sorted(region_estimates, key=lambda x: x.region)
