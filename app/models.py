from __future__ import annotations

from pydantic import BaseModel, Field


class ProductSignal(BaseModel):
    name: str
    region: str
    source_url: str
    snippet: str = ""
    reviews: int = Field(default=0, ge=0)
    avg_price: float = Field(default=0.0, ge=0.0)
    currency: str = "USD"


class RegionEstimate(BaseModel):
    region: str
    estimated_market_volume_usd: float
    estimated_market_volume_czk: float
    competitors: list[ProductSignal]
