# Movit Energy - Market Size Estimator

Streamlit web app to estimate market size for a product using competitor discovery in CZ, EU, and USA.

## Super quick run (no API key)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app starts in **MOCK mode** by default so you can run it immediately.

## Optional: real search with Serper

```bash
cp .env.example .env
```

Then set:

```env
SEARCH_PROVIDER=serper
SERPER_API_KEY=<your-key>
```

Run again:

```bash
streamlit run app.py
```

## Features

- Input fields for **Product Name** and **Ingredients/Composition**.
- Search module with pluggable providers:
  - `mock` (default, offline demo)
  - `serper` (real integration)
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

## Modular architecture

- `app/search/providers.py` -> search provider interface + Serper integration.
- `app/heuristics/extractor.py` -> regex extraction of reviews/price.
- `app/engine/estimator.py` -> market-size calculation engine.
- `app/config.py` -> env-based settings.
- `app.py` -> Streamlit UI.
