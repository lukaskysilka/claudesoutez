const REGION_COLORS = { CZ: "var(--cz)", EU: "var(--eu)", USA: "var(--usa)" };

function fmtCurrency(value, currency) {
  if (value == null) return "—";
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
    maximumFractionDigits: 0,
  }).format(value);
}

function fmtNumber(n) {
  if (n == null) return "—";
  return new Intl.NumberFormat("en-US").format(n);
}

function truncate(str, max = 60) {
  if (!str) return "—";
  return str.length > max ? str.slice(0, max) + "…" : str;
}

const S = {
  wrapper: {
    background: "var(--surface)",
    border: "1px solid var(--border)",
    borderRadius: 14,
    overflow: "hidden",
  },
  header: {
    padding: "20px 24px 16px",
    borderBottom: "1px solid var(--border)",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  },
  headerTitle: { fontSize: 16, fontWeight: 700 },
  headerSub: { fontSize: 12, color: "var(--text-muted)" },
  scrollWrapper: { overflowX: "auto" },
  table: {
    width: "100%",
    borderCollapse: "collapse",
    fontSize: 13,
  },
  th: {
    textAlign: "left",
    padding: "10px 16px",
    background: "var(--surface-2)",
    color: "var(--text-muted)",
    fontWeight: 600,
    fontSize: 11,
    letterSpacing: "0.05em",
    whiteSpace: "nowrap",
    borderBottom: "1px solid var(--border)",
  },
  td: {
    padding: "11px 16px",
    borderBottom: "1px solid var(--border)",
    verticalAlign: "middle",
  },
  tdMuted: {
    padding: "11px 16px",
    borderBottom: "1px solid var(--border)",
    color: "var(--text-muted)",
    verticalAlign: "middle",
  },
};

function DefaultBadge() {
  return (
    <span
      title="Value estimated from regional default — no live data scraped"
      style={{
        fontSize: 10,
        background: "rgba(251,191,36,0.15)",
        color: "var(--warning)",
        borderRadius: 4,
        padding: "1px 5px",
        fontWeight: 600,
        marginLeft: 4,
        cursor: "help",
      }}
    >
      est.
    </span>
  );
}

export default function CompetitorTable({ competitors }) {
  if (!competitors?.length) return null;

  return (
    <div style={S.wrapper}>
      <div style={S.header}>
        <span style={S.headerTitle}>Identified Competitors</span>
        <span style={S.headerSub}>{competitors.length} results</span>
      </div>
      <div style={S.scrollWrapper}>
        <table style={S.table}>
          <thead>
            <tr>
              {["#", "Product / Page", "Region", "Price", "Reviews", "Est. Sales", "Est. Revenue"].map(
                (h) => (
                  <th key={h} style={S.th}>
                    {h}
                  </th>
                )
              )}
            </tr>
          </thead>
          <tbody>
            {competitors.map((c, i) => (
              <tr
                key={i}
                style={{ transition: "background 0.1s" }}
                onMouseEnter={(e) =>
                  (e.currentTarget.style.background = "var(--surface-2)")
                }
                onMouseLeave={(e) =>
                  (e.currentTarget.style.background = "transparent")
                }
              >
                <td style={S.tdMuted}>{i + 1}</td>
                <td style={S.td}>
                  <a
                    href={c.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    title={c.name}
                  >
                    {truncate(c.name, 55)}
                  </a>
                  <div style={{ fontSize: 11, color: "var(--text-muted)", marginTop: 2 }}>
                    {new URL(c.url).hostname.replace(/^www\./, "")}
                  </div>
                </td>
                <td style={S.td}>
                  <span
                    style={{
                      color: REGION_COLORS[c.region],
                      fontWeight: 600,
                      background: `${REGION_COLORS[c.region]}18`,
                      borderRadius: 5,
                      padding: "2px 8px",
                      fontSize: 12,
                    }}
                  >
                    {c.region}
                  </span>
                </td>
                <td style={S.td}>
                  {fmtCurrency(c.price, c.currency)}
                  {c.price_is_default && <DefaultBadge />}
                </td>
                <td style={S.td}>
                  {fmtNumber(c.reviews)}
                  {c.reviews_is_default && <DefaultBadge />}
                </td>
                <td style={S.tdMuted}>{fmtNumber(c.estimated_sales)}</td>
                <td style={{ ...S.td, fontWeight: 600 }}>
                  {fmtCurrency(c.estimated_revenue, c.currency)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
