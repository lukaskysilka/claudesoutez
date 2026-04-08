# Movit Energy - Market Size Estimator

Streamlit web app to estimate market size for a product using competitor discovery in CZ, EU, and USA.

## Features

- Input fields for **Product Name** and **Ingredients/Composition**.
- Search module with pluggable providers:
  - `serper` (real integration)
  - `mock` (offline demo)
- Heuristic extraction for:
  - Number of reviews
  - Average price + currency guess
- Estimation formula:
  - `Market Size = Σ (Reviews * Multiplier * Price)`
  - Default multiplier: `50`
- Dashboard output with:
  - Region split (CZ / EU / USA)
  - USD and CZK values
  - Top competitor table with source URLs

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and set:

```env
SEARCH_PROVIDER=serper
SERPER_API_KEY=<your-key>
REVIEW_TO_SALES_MULTIPLIER=50
USD_TO_CZK=23.2
EUR_TO_CZK=25.3
```

Run:

```bash
streamlit run app.py
```

## Modular architecture

- `app/search/providers.py` -> search provider interface + Serper integration.
- `app/heuristics/extractor.py` -> regex extraction of reviews/price.
- `app/engine/estimator.py` -> market-size calculation engine.
- `app/config.py` -> env-based settings.
- `app.py` -> Streamlit UI.

## Notes

- The search snippets may not always include review counts and prices. In such cases, values default to `0`.
- You can add another provider (Google Custom Search, scraping pipeline, etc.) by implementing the `SearchProvider` interface.
