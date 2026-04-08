const REGION_META = {
  CZ: { label: "Czech Republic", flag: "🇨🇿", color: "var(--cz)", bg: "rgba(96,165,250,0.08)" },
  EU: { label: "European Union",  flag: "🇪🇺", color: "var(--eu)", bg: "rgba(52,211,153,0.08)" },
  USA: { label: "United States",  flag: "🇺🇸", color: "var(--usa)", bg: "rgba(249,115,22,0.08)" },
};

function fmt(value, currency) {
  if (!value && value !== 0) return "—";
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
    maximumFractionDigits: 0,
  }).format(value);
}

function fmtUSD(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(value);
}

export default function RegionCard({ summary }) {
  const meta = REGION_META[summary.region] || {};

  const S = {
    card: {
      background: "var(--surface)",
      border: `1px solid ${meta.color}33`,
      borderRadius: 14,
      padding: "24px 26px",
      display: "flex",
      flexDirection: "column",
      gap: 16,
    },
    header: {
      display: "flex",
      alignItems: "center",
      gap: 10,
    },
    flag: { fontSize: 26 },
    region: {
      display: "flex",
      flexDirection: "column",
    },
    regionCode: {
      fontSize: 16,
      fontWeight: 700,
      color: meta.color,
    },
    regionLabel: {
      fontSize: 12,
      color: "var(--text-muted)",
    },
    divider: {
      height: 1,
      background: "var(--border)",
    },
    stat: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
    },
    statLabel: {
      fontSize: 12,
      color: "var(--text-muted)",
      fontWeight: 500,
    },
    statValue: {
      fontSize: 14,
      fontWeight: 600,
      color: "var(--text)",
    },
    bigValue: {
      fontSize: 26,
      fontWeight: 800,
      color: meta.color,
      letterSpacing: "-0.5px",
    },
    bigSub: {
      fontSize: 11,
      color: "var(--text-muted)",
      marginTop: 2,
    },
    usdBadge: {
      fontSize: 11,
      color: meta.color,
      background: meta.bg,
      borderRadius: 6,
      padding: "2px 8px",
      fontWeight: 600,
    },
  };

  return (
    <div style={S.card}>
      <div style={S.header}>
        <span style={S.flag}>{meta.flag}</span>
        <div style={S.region}>
          <span style={S.regionCode}>{summary.region}</span>
          <span style={S.regionLabel}>{meta.label}</span>
        </div>
      </div>

      <div>
        <div style={S.bigValue}>
          {fmt(summary.total_revenue, summary.currency)}
        </div>
        <div style={S.bigSub}>
          Estimated market volume ({summary.currency})
        </div>
        {summary.currency !== "USD" && (
          <span style={S.usdBadge}>{fmtUSD(summary.total_revenue_usd)} USD</span>
        )}
      </div>

      <div style={S.divider} />

      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        <div style={S.stat}>
          <span style={S.statLabel}>Competitors found</span>
          <span style={S.statValue}>{summary.total_competitors}</span>
        </div>
        <div style={S.stat}>
          <span style={S.statLabel}>Avg. product price</span>
          <span style={S.statValue}>{fmt(summary.avg_price, summary.currency)}</span>
        </div>
      </div>
    </div>
  );
}
