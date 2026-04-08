from pydantic import BaseModel
from typing import List, Optional


class SearchRequest(BaseModel):
    product_name: str
    ingredients: str


class Competitor(BaseModel):
    name: str
    url: str
    region: str
    currency: str
    price: Optional[float] = None
    reviews: Optional[int] = None
    estimated_sales: Optional[int] = None
    estimated_revenue: Optional[float] = None
    price_is_default: bool = False
    reviews_is_default: bool = False


class RegionSummary(BaseModel):
    region: str
    currency: str
    total_revenue: float
    total_revenue_usd: float
    total_competitors: int
    avg_price: float


class MarketEstimationResponse(BaseModel):
    product_name: str
    ingredients: str
    competitors: List[Competitor]
    region_summaries: List[RegionSummary]
    total_market_size_usd: float
    review_to_sales_ratio: int
    methodology: str
