import { useState } from "react";
import { estimateMarket } from "./api.js";
import SearchForm from "./components/SearchForm.jsx";
import Dashboard from "./components/Dashboard.jsx";

const styles = {
  wrapper: {
    minHeight: "100vh",
    display: "flex",
    flexDirection: "column",
  },
  header: {
    background: "linear-gradient(135deg, #1a1d27 0%, #0f1117 100%)",
    borderBottom: "1px solid var(--border)",
    padding: "20px 32px",
    display: "flex",
    alignItems: "center",
    gap: 16,
  },
  logo: {
    width: 42,
    height: 42,
    background: "linear-gradient(135deg, #5c6ef8, #a78bfa)",
    borderRadius: 10,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: 22,
    fontWeight: 800,
    color: "#fff",
    flexShrink: 0,
  },
  headerText: {
    display: "flex",
    flexDirection: "column",
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: 700,
    color: "var(--text)",
    letterSpacing: "-0.3px",
  },
  headerSub: {
    fontSize: 12,
    color: "var(--text-muted)",
    fontWeight: 500,
  },
  main: {
    flex: 1,
    maxWidth: 1200,
    width: "100%",
    margin: "0 auto",
    padding: "40px 24px",
  },
  error: {
    background: "rgba(248,113,113,0.1)",
    border: "1px solid rgba(248,113,113,0.3)",
    borderRadius: 10,
    padding: "14px 18px",
    color: "var(--danger)",
    marginTop: 24,
    fontSize: 14,
  },
};

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(productName, ingredients) {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await estimateMarket(productName, ingredients);
      setResult(data);
    } catch (err) {
      const msg =
        err?.response?.data?.detail ||
        err?.message ||
        "Unknown error. Is the backend running?";
      setError(msg);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={styles.wrapper}>
      <header style={styles.header}>
        <div style={styles.logo}>M</div>
        <div style={styles.headerText}>
          <span style={styles.headerTitle}>Movit Energy</span>
          <span style={styles.headerSub}>Market Size Estimator</span>
        </div>
      </header>

      <main style={styles.main}>
        <SearchForm onSubmit={handleSubmit} loading={loading} />
        {error && <div style={styles.error}>⚠ {error}</div>}
        {result && <Dashboard data={result} />}
      </main>
    </div>
  );
}
