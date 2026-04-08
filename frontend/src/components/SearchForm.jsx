import { useState } from "react";

const S = {
  card: {
    background: "var(--surface)",
    border: "1px solid var(--border)",
    borderRadius: 14,
    padding: "32px 36px",
  },
  title: {
    fontSize: 22,
    fontWeight: 700,
    marginBottom: 6,
    color: "var(--text)",
  },
  subtitle: {
    fontSize: 14,
    color: "var(--text-muted)",
    marginBottom: 28,
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: 20,
    marginBottom: 24,
  },
  field: { display: "flex", flexDirection: "column", gap: 7 },
  label: { fontSize: 13, fontWeight: 600, color: "var(--text-muted)" },
  input: {
    background: "var(--surface-2)",
    border: "1px solid var(--border)",
    borderRadius: 8,
    padding: "11px 14px",
    color: "var(--text)",
    fontSize: 14,
    outline: "none",
    transition: "border-color 0.15s",
    width: "100%",
    fontFamily: "inherit",
  },
  textarea: {
    background: "var(--surface-2)",
    border: "1px solid var(--border)",
    borderRadius: 8,
    padding: "11px 14px",
    color: "var(--text)",
    fontSize: 14,
    outline: "none",
    resize: "vertical",
    minHeight: 90,
    width: "100%",
    fontFamily: "inherit",
    transition: "border-color 0.15s",
  },
  btn: {
    background: "linear-gradient(135deg, #5c6ef8, #7c55f8)",
    color: "#fff",
    border: "none",
    borderRadius: 9,
    padding: "13px 32px",
    fontSize: 15,
    fontWeight: 600,
    cursor: "pointer",
    display: "inline-flex",
    alignItems: "center",
    gap: 10,
    transition: "opacity 0.15s",
    fontFamily: "inherit",
  },
  btnDisabled: {
    opacity: 0.55,
    cursor: "not-allowed",
  },
  note: {
    fontSize: 12,
    color: "var(--text-muted)",
    marginTop: 12,
  },
};

export default function SearchForm({ onSubmit, loading }) {
  const [productName, setProductName] = useState("");
  const [ingredients, setIngredients] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (!productName.trim()) return;
    onSubmit(productName.trim(), ingredients.trim());
  }

  const disabled = loading || !productName.trim();

  return (
    <form style={S.card} onSubmit={handleSubmit}>
      <div style={S.title}>Analyze Market Size</div>
      <div style={S.subtitle}>
        Enter a product name and its key ingredients to discover the competitive
        landscape and estimate market volume across CZ, EU, and USA.
      </div>

      <div style={S.grid}>
        <div style={S.field}>
          <label style={S.label}>PRODUCT NAME *</label>
          <input
            style={S.input}
            type="text"
            placeholder="e.g. Movit Energy Drink"
            value={productName}
            onChange={(e) => setProductName(e.target.value)}
            onFocus={(e) => (e.target.style.borderColor = "var(--accent)")}
            onBlur={(e) => (e.target.style.borderColor = "var(--border)")}
            required
          />
        </div>
        <div style={S.field}>
          <label style={S.label}>INGREDIENTS / COMPOSITION</label>
          <textarea
            style={S.textarea}
            placeholder="e.g. caffeine, creatine, beta-alanine, B vitamins"
            value={ingredients}
            onChange={(e) => setIngredients(e.target.value)}
            onFocus={(e) => (e.target.style.borderColor = "var(--accent)")}
            onBlur={(e) => (e.target.style.borderColor = "var(--border)")}
          />
        </div>
      </div>

      <button
        type="submit"
        style={{ ...S.btn, ...(disabled ? S.btnDisabled : {}) }}
        disabled={disabled}
      >
        {loading ? (
          <>
            <Spinner /> Searching markets…
          </>
        ) : (
          <>⚡ Estimate Market Size</>
        )}
      </button>

      <p style={S.note}>
        Searches CZ, EU &amp; USA markets · Extracts reviews &amp; prices ·
        Applies 1 review ≈ 50 sales ratio
      </p>
    </form>
  );
}

function Spinner() {
  return (
    <span
      style={{
        display: "inline-block",
        width: 16,
        height: 16,
        border: "2px solid rgba(255,255,255,0.3)",
        borderTop: "2px solid #fff",
        borderRadius: "50%",
        animation: "spin 0.7s linear infinite",
      }}
    />
  );
}

// Inject keyframe once
if (typeof document !== "undefined" && !document.getElementById("spin-style")) {
  const s = document.createElement("style");
  s.id = "spin-style";
  s.textContent = "@keyframes spin { to { transform: rotate(360deg); } }";
  document.head.appendChild(s);
}
