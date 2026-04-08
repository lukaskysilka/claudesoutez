from __future__ import annotations

import pandas as pd
import streamlit as st

from app.engine.estimator import estimate_market_size
from app.heuristics.extractor import enrich_product_signal
from app.search.providers import get_search_provider

st.set_page_config(page_title="Movit Energy | Market Size Estimator", layout="wide")

st.title("⚡ Movit Energy - Market Size Estimator")
st.caption("Estimate market volume from competing products in CZ / EU / USA using review and pricing heuristics.")

with st.sidebar:
    st.header("Input")
    product_name = st.text_input("Product Name", placeholder="e.g., Energy Gel")
    composition = st.text_area("Ingredients / Composition", placeholder="e.g., caffeine, taurine, B vitamins")
    run_btn = st.button("Run estimation", type="primary")

if run_btn:
    if not product_name.strip() or not composition.strip():
        st.warning("Please provide both Product Name and Ingredients/Composition.")
        st.stop()

    provider = get_search_provider()
    regions = ["CZ", "EU", "USA"]

    with st.spinner("Collecting competitors and estimating market size..."):
        all_products = []
        for region in regions:
            region_products = provider.search_top_competitors(product_name, composition, region, top_k=10)
            all_products.extend(enrich_product_signal(product) for product in region_products)

        estimates = estimate_market_size(all_products)

    st.subheader("Estimated Market Volume by Region")

    cards = st.columns(3)
    for idx, estimate in enumerate(estimates):
        with cards[idx % 3]:
            st.metric(f"{estimate.region} Market Volume", f"${estimate.estimated_market_volume_usd:,.0f}")
            st.caption(f"≈ {estimate.estimated_market_volume_czk:,.0f} CZK")

    st.divider()

    st.subheader("Identified Top Competitors")
    table_rows = []
    for estimate in estimates:
        for p in estimate.competitors:
            table_rows.append(
                {
                    "Region": p.region,
                    "Product": p.name,
                    "Reviews": p.reviews,
                    "Average Price": p.avg_price,
                    "Currency": p.currency,
                    "Source": p.source_url,
                }
            )

    df = pd.DataFrame(table_rows).sort_values(by=["Region", "Reviews"], ascending=[True, False])
    st.dataframe(df, use_container_width=True)

    st.info(
        "Formula used: Market Size = Σ(Reviews × Review-to-Sales Multiplier × Average Price). "
        "Default multiplier is 50 and can be changed in .env."
    )
else:
    st.write("Fill in product details and click **Run estimation**.")
