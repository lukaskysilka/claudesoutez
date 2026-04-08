import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import RegionCard from "./RegionCard.jsx";
import CompetitorTable from "./CompetitorTable.jsx";

const REGION_COLORS = {
  CZ: "#60a5fa",
  EU: "#34d399",
  USA: "#f97316",
};

function fmtUSD(v) {
  if (!v && v !== 0) return "$0";
  if (v >= 1_000_000_000)
    return `$${(v / 1_000_000_000).toFixed(2)}B`;
  if (v >= 1_000_000)
    return `$${(v / 1_000_000).toFixed(2)}M`;
  if (v >= 1_000)
    return `$${(v / 1_000).toFixed(1)}K`;
  return `$${v.toFixed(0)}`;
}

const CustomTooltip = ({ active, payload }) => {
  if (active && payload?.length) {
    const { region, value } = payload[0].payload;
    return (
      <div
        style={{
          background: "#1a1d27",
          border: "1px solid #2d3150",
          borderRadius: 8,
          padding: "10px 14px",
          fontSize: 13,
        }}
      >
        <div style={{ fontWeight: 700, color: REGION_COLORS[region] }}>{region}</div>
        <div style={{ color: "#e8eaf6", marginTop: 4 }}>{fmtUSD(value)}</div>
      </div>
    );
  }
  return null;
};

const S = {
  section: { marginTop: 36 },
  sectionTitle: {
    fontSize: 13,
    fontWeight: 700,
    color: "var(--text-muted)",
    letterSpacing: "0.06em",
    marginBottom: 16,
  },
  totalCard: {
    background: "linear-gradient(135deg, #1a1d27 0%, #22263a 100%)",
    border: "1px solid var(--accent)44",
    borderRadius: 14,
    padding: "28px 32px",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    flexWrap: "wrap",
    gap: 16,
  },
  totalLeft: { display: "flex", flexDirection: "column", gap: 4 },
  totalLabel: { fontSize: 13, color: "var(--text-muted)", fontWeight: 500 },
  totalValue: {
    fontSize: 44,
    fontWeight: 800,
    letterSpacing: "-1.5px",
    background: "linear-gradient(135deg, #5c6ef8, #a78bfa)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
    backgroundClip: "text",
  },
  totalMeta: { fontSize: 12, color: "var(--text-muted)" },
  ratioBadge: {
    background: "var(--accent-glow)",
    border: "1px solid var(--accent)44",
    borderRadius: 10,
    padding: "12px 20px",
    textAlign: "center",
  },
  ratioNum: {
    fontSize: 28,
    fontWeight: 800,
    color: "var(--accent)",
  },
  ratioLabel: { fontSize: 12, color: "var(--text-muted)" },
  regionGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
    gap: 18,
  },
  chartCard: {
    background: "var(--surface)",
    border: "1px solid var(--border)",
    borderRadius: 14,
    padding: "24px",
  },
  methodology: {
    background: "var(--surface)",
    border: "1px solid var(--border)",
    borderRadius: 12,
    padding: "16px 20px",
    fontSize: 13,
    color: "var(--text-muted)",
    lineHeight: 1.7,
  },
};

export default function Dashboard({ data }) {
  const chartData = data.region_summaries.map((s) => ({
    region: s.region,
    value: s.total_revenue_usd,
  }));

  return (
    <div>
      {/* ── Total Market Size ──────────────────────────────── */}
      <div style={S.section}>
        <div style={S.sectionTitle}>TOTAL ESTIMATED MARKET SIZE</div>
        <div style={S.totalCard}>
          <div style={S.totalLeft}>
            <span style={S.totalLabel}>
              Combined market volume for "{data.product_name}"
            </span>
            <span style={S.totalValue}>{fmtUSD(data.total_market_size_usd)}</span>
            <span style={S.totalMeta}>
              Across {data.region_summaries.reduce((a, s) => a + s.total_competitors, 0)} competitors
              in CZ · EU · USA
            </span>
          </div>
          <div style={S.ratioBadge}>
            <div style={S.ratioNum}>×{data.review_to_sales_ratio}</div>
            <div style={S.ratioLabel}>review-to-sales ratio</div>
          </div>
        </div>
      </div>

      {/* ── Region Cards ───────────────────────────────────── */}
      <div style={S.section}>
        <div style={S.sectionTitle}>BREAKDOWN BY REGION</div>
        <div style={S.regionGrid}>
          {data.region_summaries.map((s) => (
            <RegionCard key={s.region} summary={s} />
          ))}
        </div>
      </div>

      {/* ── Bar Chart ─────────────────────────────────────── */}
      <div style={S.section}>
        <div style={S.sectionTitle}>REVENUE DISTRIBUTION (USD)</div>
        <div style={S.chartCard}>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={chartData} barSize={56}>
              <XAxis
                dataKey="region"
                axisLine={false}
                tickLine={false}
                tick={{ fill: "#8b90b8", fontSize: 13, fontWeight: 600 }}
              />
              <YAxis
                tickFormatter={fmtUSD}
                axisLine={false}
                tickLine={false}
                tick={{ fill: "#8b90b8", fontSize: 11 }}
                width={72}
              />
              <Tooltip content={<CustomTooltip />} cursor={{ fill: "rgba(255,255,255,0.04)" }} />
              <Bar dataKey="value" radius={[6, 6, 0, 0]}>
                {chartData.map((entry) => (
                  <Cell key={entry.region} fill={REGION_COLORS[entry.region]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* ── Competitor Table ───────────────────────────────── */}
      <div style={S.section}>
        <div style={S.sectionTitle}>TOP COMPETITORS</div>
        <CompetitorTable competitors={data.competitors} />
      </div>

      {/* ── Methodology note ──────────────────────────────── */}
      <div style={{ ...S.section, marginBottom: 48 }}>
        <div style={S.sectionTitle}>METHODOLOGY</div>
        <div style={S.methodology}>{data.methodology}</div>
      </div>
    </div>
  );
}
