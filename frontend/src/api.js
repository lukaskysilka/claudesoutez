/**
 * API client — swap BASE_URL if you deploy the backend elsewhere.
 */
import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_URL || "";

const client = axios.create({ baseURL: BASE_URL, timeout: 120_000 });

/**
 * @param {string} productName
 * @param {string} ingredients
 * @returns {Promise<import('./types').MarketEstimationResponse>}
 */
export async function estimateMarket(productName, ingredients) {
  const { data } = await client.post("/api/estimate", {
    product_name: productName,
    ingredients,
  });
  return data;
}

export async function checkHealth() {
  const { data } = await client.get("/health");
  return data;
}
