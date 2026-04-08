from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ── Search API (swap freely) ──────────────────────────────────────────────
    SERPER_API_KEY: str = ""          # https://serper.dev  (primary)
    GOOGLE_API_KEY: str = ""          # Google Custom Search fallback
    GOOGLE_CSE_ID: str = ""           # Google Custom Search Engine ID

    # ── Estimation tuning ─────────────────────────────────────────────────────
    REVIEW_TO_SALES_RATIO: int = 50   # 1 review ≈ 50 sales (industry heuristic)
    MAX_COMPETITORS_PER_REGION: int = 10

    # ── Scraper ───────────────────────────────────────────────────────────────
    REQUEST_TIMEOUT: int = 10         # seconds
    MAX_CONCURRENT_SCRAPES: int = 5

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
