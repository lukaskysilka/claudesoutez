from __future__ import annotations

import re
from abc import ABC, abstractmethod

import requests

from app.config import settings
from app.models import ProductSignal


class SearchProvider(ABC):
    @abstractmethod
    def search_top_competitors(self, product_name: str, composition: str, region: str, top_k: int = 10) -> list[ProductSignal]:
        raise NotImplementedError


class SerperSearchProvider(SearchProvider):
    endpoint = "https://google.serper.dev/search"

    def _region_query_hint(self, region: str) -> str:
        mapping = {
            "CZ": "Czech Republic e-shop cena recenze",
            "EU": "Europe online store price reviews",
            "USA": "United States buy online price reviews",
        }
        return mapping.get(region, region)

    def _extract_title(self, title: str) -> str:
        cleaned = re.sub(r"\s*[\-|·|•].*$", "", title).strip()
        return cleaned or title

    def search_top_competitors(self, product_name: str, composition: str, region: str, top_k: int = 10) -> list[ProductSignal]:
        if not settings.serper_api_key:
            raise ValueError("SERPER_API_KEY is missing. Add it in your .env file.")

        query = (
            f"{product_name} {composition} {self._region_query_hint(region)} "
            "site:amazon.com OR site:heureka.cz OR site:alza.cz OR site:mall.cz"
        )

        payload = {"q": query, "num": top_k, "gl": "us" if region == "USA" else "cz" if region == "CZ" else "de"}
        headers = {"X-API-KEY": settings.serper_api_key, "Content-Type": "application/json"}
        response = requests.post(self.endpoint, json=payload, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()
        organic = data.get("organic", [])[:top_k]

        products: list[ProductSignal] = []
        for row in organic:
            products.append(
                ProductSignal(
                    name=self._extract_title(row.get("title", "Unknown product")),
                    region=region,
                    source_url=row.get("link", ""),
                    snippet=row.get("snippet", ""),
                )
            )
        return products


class MockSearchProvider(SearchProvider):
    def search_top_competitors(self, product_name: str, composition: str, region: str, top_k: int = 10) -> list[ProductSignal]:
        sample = []
        for idx in range(1, top_k + 1):
            sample.append(
                ProductSignal(
                    name=f"{product_name} Competitor {idx}",
                    region=region,
                    source_url=f"https://example.com/{region.lower()}/{idx}",
                    snippet=(
                        f"{product_name} with {composition}. {120 + idx * 7} reviews. "
                        f"Price ${9.99 + idx:.2f}."
                    ),
                )
            )
        return sample


def get_search_provider() -> SearchProvider:
    if settings.search_provider.lower() == "mock":
        return MockSearchProvider()
    return SerperSearchProvider()
