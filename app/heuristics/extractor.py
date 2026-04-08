from __future__ import annotations

import re

from app.models import ProductSignal

REVIEW_PATTERNS = [
    re.compile(r"(\d{1,3}(?:[\s,.]\d{3})*|\d+)\s*(?:reviews?|hodnocen[ií]|ratings?)", re.IGNORECASE),
    re.compile(r"(?:reviews?|ratings?)\s*[:\-]?\s*(\d{1,3}(?:[\s,.]\d{3})*|\d+)", re.IGNORECASE),
]

PRICE_PATTERNS = [
    re.compile(r"\$\s?(\d+(?:[\.,]\d{1,2})?)"),
    re.compile(r"(\d+(?:[\.,]\d{1,2})?)\s?(?:USD|US\$)", re.IGNORECASE),
    re.compile(r"(\d+(?:[\.,]\d{1,2})?)\s?€", re.IGNORECASE),
    re.compile(r"(\d+(?:[\.,]\d{1,2})?)\s?(?:CZK|Kč)", re.IGNORECASE),
]


def _to_number(raw: str) -> int:
    normalized = raw.replace(" ", "").replace(".", "").replace(",", "")
    return int(normalized)


def _to_price(raw: str) -> float:
    normalized = raw.replace(" ", "").replace(",", ".")
    return float(normalized)


def _guess_currency(text: str) -> str:
    lower = text.lower()
    if "kč" in lower or "czk" in lower:
        return "CZK"
    if "€" in text or "eur" in lower:
        return "EUR"
    return "USD"


def enrich_product_signal(product: ProductSignal) -> ProductSignal:
    text = product.snippet or ""

    reviews = 0
    for pattern in REVIEW_PATTERNS:
        match = pattern.search(text)
        if match:
            reviews = _to_number(match.group(1))
            break

    price = 0.0
    for pattern in PRICE_PATTERNS:
        match = pattern.search(text)
        if match:
            price = _to_price(match.group(1))
            break

    return product.model_copy(update={"reviews": reviews, "avg_price": price, "currency": _guess_currency(text)})
