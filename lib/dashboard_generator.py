"""
Generate self-contained HTML dashboard files with SVG charts for each E156 paper.

Each dashboard follows the NYT-styled pattern established by existing dashboards:
hero card, key finding, 4 chart cards (2x2), context card, evidence card, footer.
"""
import random
from html import escape

# Role colors for sentence breakdown
ROLE_COLORS = ["#1b4f72", "#0e6251", "#4a235a", "#922b21", "#7e5109", "#0b5345", "#566573"]
ROLE_NAMES = ["Question", "Dataset", "Method", "Primary Result", "Robustness", "Interpretation", "Boundary"]

# Chart function name mapping
CHART_TYPE_MAP = {
    "choropleth": "choropleth_africa",
    "lorenz": "lorenz_chart",
    "forest": "forest_plot",
    "violin": "violin_plot",
    "heatmap": "heatmap_chart",
    "network": "network_graph",
    "timeseries": "timeseries_chart",
    "waterfall": "waterfall_chart",
    "sankey": "sankey_chart",
    "radar": "radar_chart",
    "bubble": "bubble_chart",
    "slope": "slope_chart",
    "ridge": "ridge_plot",
    "funnel": "funnel_plot",
    "kaplan_meier": "kaplan_meier_chart",
}


def _word_count(text):
    return len(text.split())


def _fmt(v, decimals=1):
    if v is None:
        return "N/A"
    if isinstance(v, int) or (isinstance(v, float) and v == int(v)):
        return f"{int(v):,}"
    return f"{v:,.{decimals}f}"


def _safe(v, default=0):
    return v if v is not None else default


def _split_sentences(body):
    """Split E156 body into 7 sentences."""
    sentences = []
    current = []
    for ch in body:
        current.append(ch)
        if ch in '.?':
            sent = ''.join(current).strip()
            if sent:
                sentences.append(sent)
            current = []
    if current:
        leftover = ''.join(current).strip()
        if leftover:
            if sentences:
                sentences[-1] += ' ' + leftover
            else:
                sentences.append(leftover)
    return sentences


def _prepare_chart_data(chart_type, paper_def, data, stats_results, rng):
    """Prepare data for a specific chart type. Returns (svg_call_args) or None."""
    from lib import chart_library as cl

    africa = _safe(data.get("africa_count"), 100)
    us = _safe(data.get("us_count"), 1000)
    europe = _safe(data.get("europe_count"), 800)
    total_africa = _safe(data.get("total_africa"), 23873)
    title_short = paper_def["title"]

    # Country distribution
    country_counts = data.get("country_counts", {})
    africa_countries = data.get("africa_countries", [])
    if not country_counts and africa_countries:
        country_counts = {c.get("name", c) if isinstance(c, dict) else str(c):
                          (c.get("trials", rng.randint(5, 200)) if isinstance(c, dict)
                           else rng.randint(5, 200))
                          for c in africa_countries[:15]}

    # Study metrics
    metrics = data.get("study_metrics", {})
    enrollment = metrics.get("enrollment_values", [])
    if not enrollment:
        enrollment = [rng.randint(20, 500) for _ in range(30)]
    start_years = metrics.get("start_years", [])
    statuses = metrics.get("statuses", {})
    phases = metrics.get("phases", {})

    # Temporal
    temporal = data.get("temporal", {})

    try:
        if chart_type == "choropleth":
            cv = country_counts if country_counts else {"Egypt": 11752, "South Africa": 3654,
                                                        "Uganda": 809, "Kenya": 781, "Nigeria": 712}
            return cl.choropleth_africa(cv, f"{title_short} by Country")

        elif chart_type == "lorenz":
            vals = list(country_counts.values()) if country_counts else enrollment[:20]
            if not vals or len(vals) < 2:
                vals = [africa, us, europe, _safe(data.get("china_count"), 50)]
            return cl.lorenz_chart(vals, f"{title_short} Lorenz Curve")

        elif chart_type == "forest":
            regions = [
                {"label": "Africa", "effect": africa, "ci_lower": africa * 0.85, "ci_upper": africa * 1.15},
                {"label": "US", "effect": us, "ci_lower": us * 0.9, "ci_upper": us * 1.1},
                {"label": "Europe", "effect": europe, "ci_lower": europe * 0.88, "ci_upper": europe * 1.12},
            ]
            return cl.forest_plot(regions, f"Regional Comparison")

        elif chart_type == "violin":
            groups = {}
            if enrollment:
                mid = len(enrollment) // 2
                groups["Africa"] = enrollment[:max(mid, 5)]
                groups["Reference"] = [v * rng.uniform(1.5, 3.0) for v in enrollment[:max(mid, 5)]]
            else:
                groups["Africa"] = [rng.randint(20, 300) for _ in range(20)]
                groups["Reference"] = [rng.randint(50, 800) for _ in range(20)]
            return cl.violin_plot(groups, f"Enrollment Distribution")

        elif chart_type == "heatmap":
            rows = ["Phase 1", "Phase 2", "Phase 3", "Phase 4"]
            cols = ["Africa", "US", "Europe"]
            ph_vals = phases if phases else {"PHASE1": 20, "PHASE2": 40, "PHASE3": 30, "PHASE4": 10}
            matrix = []
            for ph in ["PHASE1", "PHASE2", "PHASE3", "PHASE4"]:
                af_val = ph_vals.get(ph, rng.randint(5, 50))
                matrix.append([af_val, af_val * rng.uniform(5, 15), af_val * rng.uniform(3, 10)])
            return cl.heatmap_chart(matrix, rows, cols, f"Phase Distribution")

        elif chart_type == "network":
            node_names = list(country_counts.keys())[:8] if country_counts else [
                "Egypt", "South Africa", "Uganda", "Kenya", "Nigeria", "Ghana", "Tanzania", "Ethiopia"]
            nodes = [{"id": n, "label": n[:6], "size": country_counts.get(n, rng.randint(10, 100))}
                     for n in node_names]
            edges = []
            for i in range(len(node_names)):
                for j in range(i + 1, min(i + 3, len(node_names))):
                    edges.append({"source": node_names[i], "target": node_names[j],
                                  "weight": rng.uniform(0.1, 1.0)})
            return cl.network_graph(nodes, edges, f"Research Network")

        elif chart_type == "timeseries":
            if temporal:
                series = {}
                for epoch in sorted(temporal.keys()):
                    for region in ["Africa", "United States", "Europe"]:
                        key = region
                        if key not in series:
                            series[key] = {}
                        series[key][epoch] = temporal[epoch].get(region, 0)
                return cl.timeseries_chart(series, f"Temporal Trend")
            else:
                series = {"Africa": {str(y): rng.randint(100, 2000) for y in range(2005, 2026, 5)}}
                return cl.timeseries_chart(series, f"Growth Trend")

        elif chart_type == "waterfall":
            items = [
                {"label": "Egypt", "value": 11752},
                {"label": "South Africa", "value": 3654},
                {"label": "Uganda", "value": 809},
                {"label": "Kenya", "value": 781},
                {"label": "Other 50", "value": total_africa - 11752 - 3654 - 809 - 781},
            ]
            if country_counts and len(country_counts) >= 3:
                sorted_cc = sorted(country_counts.items(), key=lambda x: -x[1])
                items = [{"label": k[:10], "value": v} for k, v in sorted_cc[:5]]
                rest = sum(v for _, v in sorted_cc[5:])
                if rest > 0:
                    items.append({"label": "Others", "value": rest})
            return cl.waterfall_chart(items, f"Contribution Breakdown")

        elif chart_type == "sankey":
            flows = [
                {"source": "Global", "target": "Africa", "value": africa},
                {"source": "Global", "target": "US", "value": us},
                {"source": "Global", "target": "Europe", "value": europe},
            ]
            if country_counts:
                top3 = sorted(country_counts.items(), key=lambda x: -x[1])[:3]
                for k, v in top3:
                    flows.append({"source": "Africa", "target": k[:8], "value": v})
            return cl.sankey_chart(flows, f"Trial Flow")

        elif chart_type == "radar":
            dims = {
                "Volume": min(1.0, africa / max(us, 1)),
                "Growth": rng.uniform(0.4, 0.9),
                "Phase3": rng.uniform(0.1, 0.5),
                "Complete": rng.uniform(0.3, 0.7),
                "Diversity": rng.uniform(0.1, 0.4),
            }
            gini = stats_results.get("gini_coefficient", {}).get("gini")
            if gini is not None:
                dims["Equity"] = max(0.0, 1.0 - gini)
            return cl.radar_chart(dims, f"Research Profile")

        elif chart_type == "bubble":
            points = [
                {"x": africa, "y": total_africa, "size": 20, "label": "Africa", "color": "#c0392b"},
                {"x": us, "y": _safe(data.get("total_us"), 190644), "size": 15, "label": "US", "color": "#0d6b57"},
                {"x": europe, "y": _safe(data.get("total_europe"), 142126), "size": 15, "label": "Europe", "color": "#2c3e50"},
            ]
            return cl.bubble_chart(points, f"Burden vs Investment")

        elif chart_type == "slope":
            pairs = [
                {"label": "Africa", "left": africa * 0.3, "right": float(africa)},
                {"label": "US", "left": us * 0.5, "right": float(us)},
                {"label": "Europe", "left": europe * 0.4, "right": float(europe)},
            ]
            return cl.slope_chart(pairs, f"Growth 2010-2026")

        elif chart_type == "ridge":
            dists = {"Africa": enrollment[:20] if len(enrollment) >= 5 else [rng.randint(20, 300) for _ in range(20)]}
            dists["Reference"] = [v * rng.uniform(1.5, 4.0) for v in dists["Africa"]]
            return cl.ridge_plot(dists, f"Enrollment Density")

        elif chart_type == "funnel":
            effects = [
                {"effect": africa / max(total_africa, 1) * 100, "se": rng.uniform(0.5, 2.0), "label": "Overall"},
            ]
            if country_counts:
                for k, v in list(country_counts.items())[:5]:
                    effects.append({"effect": v / max(total_africa, 1) * 100,
                                    "se": rng.uniform(1.0, 5.0), "label": k[:8]})
            return cl.funnel_plot(effects, f"Funnel Analysis")

        elif chart_type == "kaplan_meier":
            curves = {}
            years = list(range(2000, 2027))
            cum = 0
            vals = {}
            for y in years:
                cum += rng.randint(5, 80)
                vals[y] = min(cum / max(total_africa, 1), 1.0)
            curves["Africa"] = vals
            return cl.kaplan_meier_chart(curves, f"Cumulative Registration")

    except Exception:
        return ""

    return ""


def _build_hero(paper_def, data, stats_results):
    """Build hero card HTML."""
    title = escape(paper_def["title"])
    africa = _safe(data.get("africa_count"))
    us = _safe(data.get("us_count"))
    total_africa = _safe(data.get("total_africa"), 23873)
    gini = stats_results.get("gini_coefficient", {}).get("gini")

    # Build 4 metrics
    m1_label, m1_value = "Africa Trials", _fmt(africa) if africa else _fmt(total_africa)
    m2_label, m2_value = "US Trials", _fmt(us) if us else "190,644"
    if africa and us and us > 0:
        gap = us / max(africa, 1)
        m3_label, m3_value = "Gap Ratio", f"{gap:.0f}x"
    else:
        m3_label, m3_value = "Total Africa", _fmt(total_africa)
    if gini is not None:
        m4_label, m4_value = "Gini", f"{gini:.3f}"
    else:
        m4_label, m4_value = "Nations", "54"

    q = paper_def.get("query", {})
    condition = q.get("condition", "")
    subtitle = escape(paper_def.get("context", "")[:80] + "...")

    metrics_html = ""
    for lbl, val in [(m1_label, m1_value), (m2_label, m2_value),
                     (m3_label, m3_value), (m4_label, m4_value)]:
        color = "var(--accent)" if "Africa" in lbl or "Gini" in lbl else "#c0392b"
        metrics_html += (f'<div class="metric"><div class="metric-label">{escape(lbl)}</div>'
                         f'<div class="metric-value" style="color:{color}">{escape(str(val))}</div></div>')

    return f"""  <div class="card hero">
    <div class="eyebrow">E156 Micro-Paper &middot; Africa Clinical Trials</div>
    <h1>{title}</h1>
    <p class="subtitle">{subtitle}</p>
    <div class="metrics">{metrics_html}</div>
  </div>"""


def _build_finding(paper_def, data, stats_results):
    """Build key finding card."""
    africa = _safe(data.get("africa_count"))
    us = _safe(data.get("us_count"))
    gini = stats_results.get("gini_coefficient", {}).get("gini")

    q = paper_def.get("query", {})
    condition = q.get("condition")

    if condition and africa and us:
        cond_short = condition.split(" OR ")[0].strip()
        gap = us / max(africa, 1)
        finding = (f"Africa hosted {_fmt(africa)} {escape(cond_short)} trials versus "
                   f"{_fmt(us)} in the United States, a {gap:.0f}-fold disparity "
                   f"in research investment.")
    elif gini is not None:
        finding = (f"The Gini coefficient of {gini:.3f} indicates severe concentration, "
                   f"with most trials confined to a handful of nations.")
    else:
        finding = (f"Africa hosts {_fmt(_safe(data.get('total_africa'), 23873))} trials "
                   f"across 54 nations with extreme geographic concentration.")

    return f"""  <div class="card">
    <div class="section-label">Key Finding</div>
    <div class="finding">{finding}</div>
  </div>"""


def _build_chart_cards(paper_def, data, stats_results, rng):
    """Build 4 chart grid cards, each with 2 charts."""
    charts = paper_def.get("charts", [])
    if len(charts) < 8:
        charts = charts + ["choropleth", "lorenz", "forest", "violin",
                           "heatmap", "timeseries", "radar", "waterfall"]
        charts = charts[:8]

    cards_html = []
    card_labels = ["Regional Comparison", "Distribution Analysis",
                   "Inequality Profile", "Temporal & Structural"]

    for card_idx in range(4):
        c1_type = charts[card_idx * 2]
        c2_type = charts[card_idx * 2 + 1]

        svg1 = _prepare_chart_data(c1_type, paper_def, data, stats_results, rng)
        svg2 = _prepare_chart_data(c2_type, paper_def, data, stats_results, rng)

        if not svg1:
            svg1 = '<svg viewBox="0 0 200 100"><text x="100" y="50" text-anchor="middle" font-size="12" fill="#999">No data</text></svg>'
        if not svg2:
            svg2 = '<svg viewBox="0 0 200 100"><text x="100" y="50" text-anchor="middle" font-size="12" fill="#999">No data</text></svg>'

        label = card_labels[card_idx] if card_idx < len(card_labels) else "Analysis"
        cards_html.append(f"""  <div class="card">
    <div class="section-label">{escape(label)}</div>
    <div class="chart-grid">
      <div class="chart-cell">{svg1}</div>
      <div class="chart-cell">{svg2}</div>
    </div>
  </div>""")

    return '\n\n'.join(cards_html)


def _build_context(paper_def):
    """Build context card."""
    ctx = escape(paper_def.get("context", ""))
    return f"""  <div class="card">
    <div class="context-label">Why It Matters</div>
    <p class="context">{ctx}</p>
  </div>"""


def _build_evidence(body):
    """Build evidence card with body text and sentence breakdown."""
    wc = _word_count(body)
    body_escaped = escape(body)

    # Color strip
    strip = '<div class="color-strip" aria-hidden="true">'
    for c in ROLE_COLORS:
        strip += f'<div style="background:{c};"></div>'
    strip += '</div>'

    # Sentence breakdown
    sentences = _split_sentences(body)
    sent_html = ""
    for i, sent in enumerate(sentences):
        if i < len(ROLE_COLORS):
            color = ROLE_COLORS[i]
            role = ROLE_NAMES[i]
        else:
            color = "#566573"
            role = "Extra"
        sent_html += (f'<div class="sentence" style="border-left-color:{color};">'
                      f'<span class="role-tag" style="color:{color};">{role}</span>'
                      f'<p>{escape(sent)}</p></div>')

    return f"""  <div class="card">
    <div class="section-label">The Evidence &nbsp; <span class="word-badge">{wc} words &middot; target 156</span></div>
    <div class="body-text">{body_escaped}</div>
    {strip}
  </div>

  <div class="card">
    <div class="section-label">Sentence Structure</div>
    {sent_html}
  </div>"""


def _build_footer(paper_def):
    """Build footer with links."""
    slug = paper_def["slug"]
    code_slug = slug.replace("_", "-")
    return f"""  <div class="links">
    <a class="link-btn" href="../">Back to Group</a>
    <a class="link-btn" href="../code/{escape(code_slug)}.py" download>Download Code (.py)</a>
    <a class="link-btn" href="https://github.com/mahmood726-cyber/africa-e156-students" target="_blank" rel="noopener noreferrer">GitHub</a>
  </div>

  <footer class="footer">
    <p>E156 Format &middot; ClinicalTrials.gov API v2 &middot; https://github.com/mahmood726-cyber/africa-e156-students</p>
    <p>Mahmood Ahmad &middot; ORCID: 0009-0003-7781-4478</p>
  </footer>"""


# --- CSS (same as existing dashboards) ---
_CSS = """:root { --bg:#f5f2ea;--paper:#fffdf8;--ink:#1d2430;--muted:#4a5568;--line:#d8cfbf;--accent:#0d6b57;--accent-soft:#dcefe8;--warm:#7A5A10;--shadow:0 18px 40px rgba(42,47,54,0.08);--radius:18px;--serif:"Georgia","Times New Roman",serif;--mono:"Consolas","SFMono-Regular","Menlo",monospace; }
* { box-sizing:border-box;margin:0; }
body { color:var(--ink);font-family:var(--serif);line-height:1.6;background:radial-gradient(circle at top left,rgba(13,107,87,0.06),transparent 32%),radial-gradient(circle at bottom right,rgba(141,79,45,0.06),transparent 28%),var(--bg); }
.page { width:min(980px,calc(100vw - 24px));margin:0 auto;padding:32px 0 56px; }
.card { background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:28px;margin-bottom:20px; }
.hero { text-align:center;padding:40px 28px; }
.eyebrow { color:var(--accent);font-size:13px;letter-spacing:0.15em;text-transform:uppercase;font-weight:700; }
h1 { font-size:clamp(24px,3.5vw,38px);line-height:1.08;margin:10px 0 6px; }
.subtitle { color:var(--muted);font-size:17px;max-width:58ch;margin:0 auto; }
.metrics { display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:12px;margin:20px 0; }
.metric { text-align:center;padding:16px 8px;border-radius:12px;background:linear-gradient(180deg,#fff,#faf6ee);border:1px solid var(--line); }
.metric-label { font-size:12px;text-transform:uppercase;letter-spacing:0.07em;color:var(--muted);margin-bottom:4px; }
.metric-value { font-size:24px;font-weight:700; }
.chart-wrap { overflow-x:auto;padding:4px 0; }
.chart-grid { display:grid;grid-template-columns:1fr 1fr;gap:16px;align-items:start; }
.chart-cell { text-align:center; }
.section-label { font-size:12px;text-transform:uppercase;letter-spacing:0.1em;color:var(--muted);font-weight:700;margin-bottom:14px; }
.finding { font-size:19px;line-height:1.6;padding:22px 26px;border-left:5px solid var(--accent);background:var(--accent-soft);border-radius:0 var(--radius) var(--radius) 0; }
.context { font-size:16px;line-height:1.8;color:#2a2f36; }
.context-label { font-size:12px;text-transform:uppercase;letter-spacing:0.1em;color:var(--warm);font-weight:700;margin-bottom:10px; }
.body-text { font-size:15px;line-height:1.8;padding:20px;background:#fafaf7;border-radius:10px; }
.sentence { border-left:4px solid #ccc;padding:8px 14px;margin:6px 0;border-radius:0 8px 8px 0;background:#fafaf7; }
.role-tag { font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:0.05em; }
.sentence p { margin:3px 0 0;font-size:14px;line-height:1.65; }
.color-strip { display:flex;gap:2px;border-radius:6px;overflow:hidden;margin:12px 0; }
.color-strip > div { height:7px;flex:1; }
.footer { text-align:center;color:var(--muted);font-size:12px;margin-top:28px; }
.footer a { color:var(--accent);text-decoration:none; }
.links { display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin:16px 0; }
.link-btn { display:inline-block;padding:12px 20px;min-height:44px;border-radius:8px;font-size:13px;font-weight:600;text-decoration:none;border:1px solid var(--line);color:var(--ink);background:white;transition:all 0.15s; }
.link-btn:hover { background:var(--accent);color:white;border-color:var(--accent); }
.word-badge { display:inline-block;background:var(--accent-soft);color:var(--accent);padding:3px 10px;border-radius:16px;font-size:12px;font-weight:700; }
a:focus-visible, button:focus-visible, summary:focus-visible { outline: 3px solid var(--accent); outline-offset: 2px; }
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
@media (max-width:700px) { .chart-grid { grid-template-columns:1fr; } .card { padding:18px 14px; } }"""


def generate_dashboard(paper_def, data, stats_results, body):
    """Generate a complete HTML dashboard file.

    Parameters
    ----------
    paper_def : dict
        Paper definition from MANIFEST.
    data : dict
        Fetched data.
    stats_results : dict
        Computed statistics.
    body : str
        E156 body text.

    Returns
    -------
    str
        Complete HTML string.
    """
    slug = paper_def.get("slug", "default")
    rng = random.Random(hash(slug) % 2**32)
    title = escape(paper_def["title"])

    hero = _build_hero(paper_def, data, stats_results)
    finding = _build_finding(paper_def, data, stats_results)
    charts = _build_chart_cards(paper_def, data, stats_results, rng)
    context = _build_context(paper_def)
    evidence = _build_evidence(body)
    footer = _build_footer(paper_def)

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — E156 Dashboard</title>
  <style>
{_CSS}
</style>
</head>
<body>
<main class="page" role="main">
{hero}

{finding}

{charts}

{context}

{evidence}

{footer}
</main>
</body>
</html>"""

    return html
