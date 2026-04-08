"""
Movit Energy — Market Size Estimator API
========================================
Start: uvicorn main:app --reload --port 8000
"""

import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from models import MarketEstimationResponse, SearchRequest
from services.estimation_service import EstimationService
from services.scraper_service import ScraperService
from services.search_service import SearchService

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Movit Market Estimator starting up")
    yield
    logger.info("Shutting down")


app = FastAPI(
    title="Movit Energy — Market Size Estimator",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

search_svc = SearchService()
scraper_svc = ScraperService()
estimation_svc = EstimationService()


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok", "serper_configured": bool(settings.SERPER_API_KEY)}


@app.post("/api/estimate", response_model=MarketEstimationResponse)
async def estimate_market(req: SearchRequest):
    if not settings.SERPER_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="SERPER_API_KEY is not set. Add it to your .env file.",
        )
    if not req.product_name.strip():
        raise HTTPException(status_code=422, detail="product_name cannot be empty.")

    logger.info("Estimate request: product=%r ingredients=%r", req.product_name, req.ingredients[:40])

    # Step 1 — Search competitors in all three regions
    raw_results = await search_svc.search_all_regions(req.product_name, req.ingredients)

    # Step 2 — Enrich each result with scraped price + review data
    semaphore = asyncio.Semaphore(settings.MAX_CONCURRENT_SCRAPES)

    async def enrich(item: dict) -> dict:
        async with semaphore:
            price, reviews = scraper_svc.extract_from_snippet(
                item.get("snippet", ""), item["currency"]
            )
            if price is None or reviews is None:
                sp, sr = await scraper_svc.scrape_page(item["url"], item["currency"])
                price = price if price is not None else sp
                reviews = reviews if reviews is not None else sr
            return {**item, "price": price, "reviews": reviews}

    enriched: dict[str, list[dict]] = {}
    for region, items in raw_results.items():
        tasks = [enrich(i) for i in items]
        enriched[region] = list(await asyncio.gather(*tasks))

    # Step 3 — Apply estimation formula and build response
    return estimation_svc.build_response(req.product_name, req.ingredients, enriched)
