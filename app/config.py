from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    search_provider: str = os.getenv("SEARCH_PROVIDER", "serper")
    serper_api_key: str = os.getenv("SERPER_API_KEY", "")
    review_to_sales_multiplier: int = int(os.getenv("REVIEW_TO_SALES_MULTIPLIER", "50"))
    usd_to_czk: float = float(os.getenv("USD_TO_CZK", "23.2"))
    eur_to_czk: float = float(os.getenv("EUR_TO_CZK", "25.3"))


settings = Settings()
