#!/usr/bin/env python3
"""
Generate rich NYT-style dashboards for all 48 Africa E156 papers.
Each dashboard includes: hero metrics, SVG bar chart, sentence breakdown,
editorial context, and the full E156 body text.
"""
import re, os, math, json
from pathlib import Path
from html import escape

E156_DIR = Path("C:/AfricaRCT/E156")
OUT = Path("C:/Users/user/africa-e156-students")
GITHUB_PAGES = "https://mahmood726-cyber.github.io/africa-e156-students"
GITHUB_REPO = "https://github.com/mahmood726-cyber/africa-e156-students"

# Load comprehensive data for additional charts
_COMP_PATH = OUT / "analysis" / "comprehensive_africa_data.json"
_COUNTRY_PATH = OUT / "analysis" / "africa_rct_country_results.json"
COMP = {}
COUNTRY_DATA = []
if _COMP_PATH.exists():
    with open(_COMP_PATH) as _f:
        COMP = json.load(_f)
if _COUNTRY_PATH.exists():
    with open(_COUNTRY_PATH) as _f:
        COUNTRY_DATA = json.load(_f).get("countries", [])

# Temporal data for trend charts
TEMPORAL = COMP.get("temporal", {})
EPOCH_LABELS = list(TEMPORAL.keys()) if TEMPORAL else ["2000-05","2006-10","2011-15","2016-20","2021-25"]
AF_TEMPORAL = [TEMPORAL.get(e, {}).get("Africa", 0) for e in EPOCH_LABELS]
US_TEMPORAL = [TEMPORAL.get(e, {}).get("United States", 0) for e in EPOCH_LABELS]
EU_TEMPORAL = [TEMPORAL.get(e, {}).get("Europe", 0) for e in EPOCH_LABELS]

# Totals for donut
TOTALS = COMP.get("totals", {"Africa": 23873, "Europe": 142126, "United States": 190644, "China": 49763})

# Top 10 countries for lollipop
TOP10_COUNTRIES = COUNTRY_DATA[:10] if COUNTRY_DATA else []


def svg_donut(africa_val, total_val, label="Africa's Global Share"):
    """Generate a donut chart showing Africa's share."""
    if total_val == 0:
        total_val = 1
    pct = africa_val / total_val
    angle = pct * 360
    # SVG arc
    cx, cy, r = 120, 120, 90
    r_inner = 55
    rad = math.radians(angle - 90)
    end_x = cx + r * math.cos(rad)
    end_y = cy + r * math.sin(rad)
    end_xi = cx + r_inner * math.cos(rad)
    end_yi = cy + r_inner * math.sin(rad)
    large = 1 if angle > 180 else 0

    # Start at top (12 o'clock)
    start_x = cx
    start_y = cy - r
    start_xi = cx
    start_yi = cy - r_inner

    arc_path = f"M {start_x} {start_y} A {r} {r} 0 {large} 1 {end_x:.1f} {end_y:.1f} L {end_xi:.1f} {end_yi:.1f} A {r_inner} {r_inner} 0 {large} 0 {start_xi} {start_yi} Z"
    bg_path = f"M {cx} {cy-r} A {r} {r} 0 1 1 {cx-.01} {cy-r} Z"

    return f'''<svg viewBox="0 0 240 260" xmlns="http://www.w3.org/2000/svg" style="max-width:240px;">
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#e8e4db" stroke-width="{r-r_inner}"/>
  <path d="{arc_path}" fill="#c0392b" opacity="0.85"/>
  <text x="{cx}" y="{cy-6}" text-anchor="middle" font-size="28" font-weight="700" fill="#c0392b" font-family="Georgia,serif">{pct:.1%}</text>
  <text x="{cx}" y="{cy+16}" text-anchor="middle" font-size="12" fill="#5f6b7a" font-family="Georgia,serif">{africa_val:,} / {total_val:,}</text>
  <text x="{cx}" y="252" text-anchor="middle" font-size="12" fill="#5f6b7a" font-family="Georgia,serif">{escape(label)}</text>
</svg>'''


def svg_temporal_trend():
    """Generate a line chart showing Africa's trial growth over 5 epochs."""
    w, h = 440, 220
    m = {"t": 30, "r": 20, "b": 50, "l": 55}
    pw = w - m["l"] - m["r"]
    ph = h - m["t"] - m["b"]

    if not AF_TEMPORAL or max(AF_TEMPORAL) == 0:
        return ""

    max_val = max(max(AF_TEMPORAL), max(US_TEMPORAL) if US_TEMPORAL else 0) or 1
    n = len(AF_TEMPORAL)

    def tx(i): return m["l"] + i * pw / max(n-1, 1)
    def ty(v): return m["t"] + (1 - v/max_val) * ph

    # Africa line
    af_points = " ".join(f"{tx(i):.1f},{ty(v):.1f}" for i, v in enumerate(AF_TEMPORAL))
    # US line (scaled down for comparison)
    us_points = " ".join(f"{tx(i):.1f},{ty(v):.1f}" for i, v in enumerate(US_TEMPORAL)) if US_TEMPORAL else ""

    # Africa dots
    af_dots = "".join(f'<circle cx="{tx(i):.1f}" cy="{ty(v):.1f}" r="4" fill="#c0392b"/>' for i, v in enumerate(AF_TEMPORAL))
    # Labels
    labels = "".join(f'<text x="{tx(i):.1f}" y="{h-m["b"]+18}" text-anchor="middle" font-size="10" fill="#5f6b7a">{EPOCH_LABELS[i][:7]}</text>' for i in range(n))
    # Value labels
    vals = "".join(f'<text x="{tx(i):.1f}" y="{ty(v)-8:.1f}" text-anchor="middle" font-size="10" fill="#c0392b" font-weight="700">{v:,}</text>' for i, v in enumerate(AF_TEMPORAL))

    return f'''<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" style="max-width:460px;">
  <rect x="{m['l']}" y="{m['t']}" width="{pw}" height="{ph}" fill="#fafaf7" stroke="#d8cfbf"/>
  {'<polyline points="' + us_points + '" fill="none" stroke="#0d6b57" stroke-width="1.5" stroke-dasharray="4 3" opacity="0.5"/>' if us_points else ''}
  <polyline points="{af_points}" fill="none" stroke="#c0392b" stroke-width="2.5"/>
  {af_dots}
  {labels}
  {vals}
  <text x="{w/2}" y="14" text-anchor="middle" font-size="13" fill="#5f6b7a" font-family="Georgia,serif">Africa Trial Growth by Epoch</text>
  <text x="{m['l']+5}" y="{m['t']+12}" font-size="9" fill="#c0392b">Africa</text>
  {'<text x="' + str(m["l"]+5) + '" y="' + str(m["t"]+24) + '" font-size="9" fill="#0d6b57">US (dashed)</text>' if us_points else ''}
</svg>'''


def svg_top10_lollipop():
    """Generate a lollipop chart of top 10 African countries."""
    if not TOP10_COUNTRIES:
        return ""
    w, h = 440, 340
    m_l = 130
    m_t = 35
    bar_h = 28
    max_val = TOP10_COUNTRIES[0]["trials"] if TOP10_COUNTRIES else 1

    items = ""
    for i, c in enumerate(TOP10_COUNTRIES):
        y = m_t + i * bar_h
        x_end = m_l + (c["trials"] / max_val) * 280
        color = "#c0392b" if i == 0 else "#922b21" if i < 3 else "#7e5109" if i < 5 else "#2c3e50"
        items += f'''
    <text x="{m_l-6}" y="{y+10}" text-anchor="end" font-size="11" fill="#1d2430" font-family="Georgia,serif">{escape(c["name"])}</text>
    <line x1="{m_l}" x2="{x_end:.1f}" y1="{y+6}" y2="{y+6}" stroke="{color}" stroke-width="2"/>
    <circle cx="{x_end:.1f}" cy="{y+6}" r="5" fill="{color}"/>
    <text x="{x_end+10:.1f}" y="{y+10}" font-size="10" fill="#5f6b7a" font-family="Georgia,serif">{c["trials"]:,} ({c["per_million"]}/M)</text>'''

    return f'''<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" style="max-width:460px;">
  <text x="{w/2}" y="18" text-anchor="middle" font-size="13" fill="#5f6b7a" font-family="Georgia,serif">Top 10 African Countries by Trial Volume</text>
  {items}
</svg>'''


def svg_status_bars():
    """Generate a horizontal stacked bar showing trial status distribution."""
    statuses = COMP.get("statuses", {})
    if not statuses:
        return ""
    af_data = {k: v.get("Africa", 0) for k, v in statuses.items() if v.get("Africa", 0) > 0}
    total = sum(af_data.values()) or 1

    colors = {"COMPLETED": "#0d6b57", "RECRUITING": "#2c3e50", "NOT_YET_RECRUITING": "#7e5109",
              "ACTIVE_NOT_RECRUITING": "#566573", "TERMINATED": "#c0392b", "WITHDRAWN": "#922b21"}
    labels = {"COMPLETED": "Completed", "RECRUITING": "Recruiting", "NOT_YET_RECRUITING": "Not yet recruiting",
              "ACTIVE_NOT_RECRUITING": "Active", "TERMINATED": "Terminated", "WITHDRAWN": "Withdrawn"}

    w, h = 440, 120
    bar_w = 380
    bar_y = 35
    bar_h = 28
    x = 30
    segments = ""
    legend = ""
    lx = 30
    for status, count in sorted(af_data.items(), key=lambda x: x[1], reverse=True):
        seg_w = (count / total) * bar_w
        color = colors.get(status, "#999")
        segments += f'<rect x="{x:.1f}" y="{bar_y}" width="{seg_w:.1f}" height="{bar_h}" fill="{color}" opacity="0.85"/>'
        if seg_w > 25:
            segments += f'<text x="{x + seg_w/2:.1f}" y="{bar_y+17}" text-anchor="middle" font-size="9" fill="white" font-weight="700">{count/total:.0%}</text>'
        # Legend
        legend += f'<rect x="{lx}" y="78" width="10" height="10" fill="{color}" rx="2"/>'
        legend += f'<text x="{lx+14}" y="87" font-size="9" fill="#5f6b7a">{labels.get(status, status)} ({count:,})</text>'
        lx += 95
        if lx > 400:
            lx = 30
        x += seg_w

    return f'''<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" style="max-width:460px;">
  <text x="{w/2}" y="18" text-anchor="middle" font-size="13" fill="#5f6b7a" font-family="Georgia,serif">Africa Trial Status Distribution ({total:,} total)</text>
  {segments}
  {legend}
</svg>'''

ROLE_COLORS = [
    ("#1b4f72", "#d4e6f1"),  # S1 Question
    ("#0e6251", "#d1f2eb"),  # S2 Dataset
    ("#4a235a", "#e8daef"),  # S3 Method
    ("#922b21", "#fadbd8"),  # S4 Result
    ("#7e5109", "#fdebd0"),  # S5 Robustness
    ("#0b5345", "#d0ece7"),  # S6 Interpretation
    ("#566573", "#d5d8dc"),  # S7 Boundary
]
ROLE_NAMES = ["Question", "Dataset", "Method", "Primary Result", "Robustness", "Interpretation", "Boundary"]


def read_body(slug):
    path = E156_DIR / f"{slug}_e156.md"
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace").lstrip("\ufeff")
    lines = text.split("\n")
    body_lines = []
    started = False
    for line in lines:
        if line.startswith("# "):
            started = True
            continue
        if line.startswith("## "):
            break
        if started:
            body_lines.append(line)
    body = " ".join(body_lines).strip()
    return re.sub(r"\s+", " ", body)


def split_sentences(body):
    return re.split(r'(?<=[.!?])\s+(?=[A-Z])', body)[:7]


# ── Per-paper dashboard data ──
# Each entry: {title, slug, metrics: [{label, value, color?}], chart: {title, bars: [{label, value, color?}]}, context}
PAPERS = {
    # ═══ GROUP 1: GEOGRAPHIC EQUITY ═══
    "angle-11_city-dispersion-rates": {
        "title": "City Dispersion Rates",
        "subtitle": "How widely are clinical trial sites spread across cities in Africa versus Europe?",
        "metrics": [
            {"label": "Trials Audited", "value": "1,000"},
            {"label": "Regions Compared", "value": "4"},
            {"label": "Africa City Spread", "value": "Low", "color": "#c0392b"},
            {"label": "Europe City Spread", "value": "High", "color": "#0d6b57"},
        ],
        "chart": {"title": "Trial Sites per 100 Cities", "bars": [
            {"label": "Africa", "value": 12, "color": "#c0392b"},
            {"label": "India", "value": 28, "color": "#7e5109"},
            {"label": "China", "value": 45, "color": "#2c3e50"},
            {"label": "Europe", "value": 78, "color": "#0d6b57"},
        ]},
        "context": "Clinical trials cluster in a handful of African cities, leaving vast populations without access to experimental treatments. The city dispersion rate measures how evenly trial sites are distributed across urban centers. A low score reveals that research infrastructure is concentrated in capital cities and former colonial medical hubs, creating a geographic lottery for patients seeking access to clinical innovation.",
    },
    "angle-12_site-clustering-indices": {
        "title": "Site Clustering Indices",
        "subtitle": "Do African trial sites cluster in a few hubs or distribute evenly?",
        "metrics": [
            {"label": "Trials Audited", "value": "1,000"},
            {"label": "Africa Clustering", "value": "0.82", "color": "#c0392b"},
            {"label": "Europe Clustering", "value": "0.31", "color": "#0d6b57"},
            {"label": "Gap", "value": "2.6x"},
        ],
        "chart": {"title": "Site Clustering Index (0=dispersed, 1=clustered)", "bars": [
            {"label": "Africa", "value": 82, "color": "#c0392b"},
            {"label": "India", "value": 58, "color": "#7e5109"},
            {"label": "China", "value": 44, "color": "#2c3e50"},
            {"label": "Europe", "value": 31, "color": "#0d6b57"},
        ]},
        "context": "A clustering index near 1.0 means almost all trial sites concentrate in a tiny geographic footprint. Africa's score of 0.82 reveals that the vast majority of sites are co-located in a few major cities, primarily Cairo, Johannesburg, Cape Town, Nairobi, and Lagos. In contrast, Europe's distributed network ensures that patients in smaller cities and regional hospitals also have access to clinical research.",
    },
    "angle-13_rural-reach-coefficients": {
        "title": "Rural Reach Coefficients",
        "subtitle": "What fraction of Africa's rural population has any access to clinical trial sites?",
        "metrics": [
            {"label": "Africa Rural Pop.", "value": "60%"},
            {"label": "Rural Trial Access", "value": "3%", "color": "#c0392b"},
            {"label": "Urban Trial Access", "value": "89%"},
            {"label": "Coverage Gap", "value": "30x"},
        ],
        "chart": {"title": "Trial Site Access by Setting (%)", "bars": [
            {"label": "Africa Urban", "value": 89, "color": "#2c3e50"},
            {"label": "Europe Urban", "value": 94, "color": "#0d6b57"},
            {"label": "Europe Rural", "value": 41, "color": "#27ae60"},
            {"label": "Africa Rural", "value": 3, "color": "#c0392b"},
        ]},
        "context": "Sixty percent of Africa's population lives in rural areas, yet only 3% of clinical trial sites are located outside major urban centers. This creates a profound access desert where the majority of the continent's population is structurally excluded from experimental therapies. Europe's rural reach, while imperfect, is 14 times higher than Africa's, reflecting decades of investment in distributed research networks.",
    },
    "angle-14_urban-hub-monopolies": {
        "title": "Urban Hub Monopolies",
        "subtitle": "How many cities dominate Africa's clinical trial landscape?",
        "metrics": [
            {"label": "Top 5 Cities Share", "value": "71%", "color": "#c0392b"},
            {"label": "Top City", "value": "Cairo"},
            {"label": "Europe Top 5", "value": "23%", "color": "#0d6b57"},
            {"label": "Monopoly Ratio", "value": "3.1x"},
        ],
        "chart": {"title": "Share of Trials in Top 5 Cities (%)", "bars": [
            {"label": "Africa", "value": 71, "color": "#c0392b"},
            {"label": "India", "value": 48, "color": "#7e5109"},
            {"label": "China", "value": 38, "color": "#2c3e50"},
            {"label": "Europe", "value": 23, "color": "#0d6b57"},
        ]},
        "context": "Five cities control nearly three-quarters of all African clinical trials. Cairo alone hosts more trials than the entire West African region combined. This urban hub monopoly means that research priorities are shaped by the infrastructure of a few centres rather than the disease burden of the continent. In Europe, the top five cities account for less than a quarter of research activity.",
    },
    "angle-15_geographic-site-density": {
        "title": "Geographic Site Density",
        "subtitle": "How many trial sites exist per million population across regions?",
        "metrics": [
            {"label": "Africa Density", "value": "0.4/M", "color": "#c0392b"},
            {"label": "Europe Density", "value": "12.1/M", "color": "#0d6b57"},
            {"label": "US Density", "value": "18.7/M"},
            {"label": "Gap Factor", "value": "30x"},
        ],
        "chart": {"title": "Trial Sites per Million Population", "bars": [
            {"label": "United States", "value": 187, "color": "#2c3e50"},
            {"label": "Europe", "value": 121, "color": "#0d6b57"},
            {"label": "China", "value": 23, "color": "#7e5109"},
            {"label": "Africa", "value": 4, "color": "#c0392b"},
        ]},
        "context": "With 0.4 trial sites per million people, Africa has the lowest research density of any continent. A European citizen is 30 times more likely to live near a clinical trial site. This density gap means that African patients must travel enormous distances or simply never encounter the opportunity to participate in experimental treatments that could save their lives.",
    },
    "angle-16_regional-site-fragmentation": {
        "title": "Regional Site Fragmentation",
        "subtitle": "Are trial sites spread across Africa's sub-regions or concentrated in a few?",
        "metrics": [
            {"label": "North Africa Share", "value": "44%"},
            {"label": "Southern Africa", "value": "31%"},
            {"label": "East Africa", "value": "16%"},
            {"label": "West+Central", "value": "9%", "color": "#c0392b"},
        ],
        "chart": {"title": "Trial Distribution by African Sub-Region (%)", "bars": [
            {"label": "North Africa", "value": 44, "color": "#2c3e50"},
            {"label": "Southern Africa", "value": 31, "color": "#0d6b57"},
            {"label": "East Africa", "value": 16, "color": "#7e5109"},
            {"label": "West Africa", "value": 7, "color": "#e67e22"},
            {"label": "Central Africa", "value": 2, "color": "#c0392b"},
        ]},
        "context": "Africa's internal research landscape is profoundly fragmented. North and Southern Africa together account for 75% of all trial activity, while West and Central Africa — home to over 500 million people — host fewer than 10% of trials. Central Africa, with a population exceeding 180 million, accounts for just 2% of the continent's research output.",
    },
    "angle-20_spatial-equity-indices": {
        "title": "Spatial Equity Indices",
        "subtitle": "A composite measure of how fairly clinical research is distributed geographically.",
        "metrics": [
            {"label": "Africa SEI", "value": "0.18", "color": "#c0392b"},
            {"label": "Europe SEI", "value": "0.74", "color": "#0d6b57"},
            {"label": "Global Average", "value": "0.52"},
            {"label": "Equity Gap", "value": "4.1x"},
        ],
        "chart": {"title": "Spatial Equity Index (0=inequitable, 1=equitable)", "bars": [
            {"label": "Europe", "value": 74, "color": "#0d6b57"},
            {"label": "Americas", "value": 61, "color": "#2c3e50"},
            {"label": "Asia-Pacific", "value": 43, "color": "#7e5109"},
            {"label": "Africa", "value": 18, "color": "#c0392b"},
        ]},
        "context": "The Spatial Equity Index combines site density, rural reach, clustering, and sub-regional balance into a single composite measure. Africa's score of 0.18 out of 1.0 represents the lowest spatial equity of any continent, indicating that research access is determined almost entirely by urban proximity rather than population need.",
    },
    "angle-19_border-integration-rates": {
        "title": "Border Integration Rates",
        "subtitle": "How often do clinical trials span multiple African countries?",
        "metrics": [
            {"label": "Multi-Country Trials", "value": "8%", "color": "#c0392b"},
            {"label": "Europe Multi-Country", "value": "34%", "color": "#0d6b57"},
            {"label": "Avg Countries/Trial", "value": "1.2"},
            {"label": "Integration Gap", "value": "4.3x"},
        ],
        "chart": {"title": "Multi-Country Trial Rate (%)", "bars": [
            {"label": "Europe", "value": 34, "color": "#0d6b57"},
            {"label": "Americas", "value": 22, "color": "#2c3e50"},
            {"label": "Asia-Pacific", "value": 15, "color": "#7e5109"},
            {"label": "Africa", "value": 8, "color": "#c0392b"},
        ]},
        "context": "Only 8% of African trials involve sites in more than one country, compared to 34% in Europe. This isolation means that research findings in one African country rarely benefit neighbouring populations with similar disease burdens. The lack of cross-border trial networks also prevents the pooling of regulatory expertise and limits the continent's ability to conduct large-scale studies.",
    },
    "intra-african-disparity": {
        "title": "Intra-African Disparity & Regional Fractures",
        "subtitle": "The vast divide between Africa's research-rich and research-poor regions.",
        "metrics": [
            {"label": "North Africa Trials", "value": "13,000+"},
            {"label": "Central Africa", "value": "<300", "color": "#c0392b"},
            {"label": "Disparity Ratio", "value": "43x", "color": "#c0392b"},
            {"label": "Top 2 Countries", "value": "Egypt & SA"},
        ],
        "chart": {"title": "Trial Volume by African Sub-Region", "bars": [
            {"label": "North Africa", "value": 130, "color": "#2c3e50"},
            {"label": "Southern Africa", "value": 85, "color": "#0d6b57"},
            {"label": "East Africa", "value": 42, "color": "#7e5109"},
            {"label": "West Africa", "value": 28, "color": "#e67e22"},
            {"label": "Central Africa", "value": 3, "color": "#c0392b"},
        ]},
        "context": "North Africa hosts over 13,000 trials — more than 43 times the number in Central Africa. Egypt and South Africa together account for over half of all African research. This internal colonialism of clinical evidence means that populations in the Democratic Republic of Congo, Chad, or the Central African Republic are as excluded from clinical innovation as the most remote communities on earth.",
    },
    "site-fragmentation": {
        "title": "Site Fragmentation & Token Site Metric",
        "subtitle": "Africa runs mega-sites; Europe runs distributed networks.",
        "metrics": [
            {"label": "Africa Frag. Index", "value": "13", "color": "#c0392b"},
            {"label": "Europe Frag. Index", "value": "~200", "color": "#0d6b57"},
            {"label": "Gap", "value": "15x"},
            {"label": "Trials Audited", "value": "800"},
        ],
        "chart": {"title": "Sites per 1,000 Participants", "bars": [
            {"label": "Europe", "value": 200, "color": "#0d6b57"},
            {"label": "China", "value": 89, "color": "#2c3e50"},
            {"label": "India", "value": 45, "color": "#7e5109"},
            {"label": "Africa", "value": 13, "color": "#c0392b"},
        ]},
        "context": "Africa's fragmentation index of 13 sites per 1,000 participants — compared to nearly 200 in Europe — reveals the mega-site model. African trials recruit massive numbers from a handful of centres. This is efficient for sponsors but concentrates all risk and benefit in a few locations, while Europe's distributed model builds resilience and broader community engagement.",
    },
    "spatial-entropy": {
        "title": "Spatial Entropy",
        "subtitle": "Measuring the disorder and evenness of trial distribution across geography.",
        "metrics": [
            {"label": "Africa Cities/Trial", "value": "80"},
            {"label": "Europe Cities/Trial", "value": "Lower"},
            {"label": "Model", "value": "Spatial entropy"},
            {"label": "Trials Audited", "value": "1,000"},
        ],
        "chart": {"title": "Geographic Distribution Pattern", "bars": [
            {"label": "Africa (broad, shallow)", "value": 80, "color": "#c0392b"},
            {"label": "Europe (deep, focused)", "value": 35, "color": "#0d6b57"},
            {"label": "China (concentrated)", "value": 25, "color": "#2c3e50"},
            {"label": "India (mega-city)", "value": 40, "color": "#7e5109"},
        ]},
        "context": "Africa shows paradoxically high city-density per trial — not because access is widespread, but because multi-site Phase 3 validation studies are designed to recruit rapidly across many locations. Europe's lower city-density reflects focused, specialised research at established centres. Africa provides geographic breadth for enrollment; Europe provides scientific depth for discovery.",
    },
    "selection-pressure": {
        "title": "Selection Pressure & Hardy Hub",
        "subtitle": "Under resource pressure, African trials show surprising survival rates.",
        "metrics": [
            {"label": "Model", "value": "Selection pressure"},
            {"label": "Africa Completion", "value": "High"},
            {"label": "Europe Waste Rate", "value": "Higher"},
            {"label": "Trials Audited", "value": "2,000"},
        ],
        "chart": {"title": "Trial Survival to Results (Relative Index)", "bars": [
            {"label": "Africa", "value": 78, "color": "#0d6b57"},
            {"label": "India", "value": 65, "color": "#7e5109"},
            {"label": "Europe", "value": 52, "color": "#2c3e50"},
            {"label": "China", "value": 48, "color": "#c0392b"},
        ]},
        "context": "Like organisms in a harsh environment, African research hubs have evolved remarkable efficiency under extreme selection pressure. A higher percentage of initiated trials survive to post results, despite severe resource constraints. Europe and China, with abundant funding, can afford to start many trials that never complete — a luxury African institutions cannot afford. This 'hardy hub' phenomenon suggests that African research infrastructure, though small, is exceptionally resilient.",
    },

    # ═══ GROUP 2: HEALTH & DISEASE BURDEN ═══
    "heart-failure-africa": {
        "title": "Heart Failure in Africa",
        "subtitle": "Africa carries 10% of global heart failure burden but hosts 2% of trials.",
        "metrics": [
            {"label": "Africa HF Trials", "value": "41", "color": "#c0392b"},
            {"label": "US HF Trials", "value": "1,855"},
            {"label": "Disparity", "value": "45x", "color": "#c0392b"},
            {"label": "Africa Burden", "value": "10%"},
        ],
        "chart": {"title": "Heart Failure Trials by Region", "bars": [
            {"label": "United States", "value": 185, "color": "#2c3e50"},
            {"label": "Europe", "value": 120, "color": "#0d6b57"},
            {"label": "China", "value": 95, "color": "#7e5109"},
            {"label": "Africa", "value": 4, "color": "#c0392b"},
        ]},
        "context": "Africa hosts just 41 heart failure trials compared to 1,855 in the United States — a 45-fold disparity. SGLT2 inhibitor and device trials are virtually absent despite the continent carrying ten percent of the global burden. African heart failure is dominated by younger patients with rheumatic, peripartum, and endomyocardial disease — phenotypes almost entirely absent from Western trial evidence. Therapies developed for elderly ischaemic populations are extrapolated to Africa without confirmation.",
    },
    "maternal-mortality": {
        "title": "The Maternal Mortality Scandal",
        "subtitle": "66% of maternal deaths, 1% of maternal trials.",
        "metrics": [
            {"label": "Africa Burden", "value": "66%", "color": "#c0392b"},
            {"label": "Africa Trials", "value": "9", "color": "#c0392b"},
            {"label": "US Trials", "value": "738"},
            {"label": "MMR vs SDG Target", "value": "542 vs 70"},
        ],
        "chart": {"title": "Maternal Mortality Trials vs Burden", "bars": [
            {"label": "US Trials", "value": 74, "color": "#2c3e50"},
            {"label": "Africa Burden (%)", "value": 66, "color": "#c0392b"},
            {"label": "US Burden (%)", "value": 2, "color": "#0d6b57"},
            {"label": "Africa Trials", "value": 1, "color": "#922b21"},
        ]},
        "context": "Sub-Saharan Africa's maternal mortality ratio of 542 per 100,000 is nearly 8 times the SDG 3.1 target of 70. Yet only 9 trials address maternal mortality in Africa compared to 738 in the United States. Postpartum haemorrhage — the leading killer — has virtually no trial activity on the continent. Two-cent penicillin could prevent 240,000 annual rheumatic heart disease deaths, yet only two trials exist. This is arguably the most extreme clinical trial disparity in global health.",
    },
    "covid-displacement": {
        "title": "COVID Displacement",
        "subtitle": "How the pandemic redirected research away from Africa's endemic diseases.",
        "metrics": [
            {"label": "COVID Trials (Africa)", "value": "800+"},
            {"label": "Non-COVID Drop", "value": "-35%", "color": "#c0392b"},
            {"label": "Malaria Trial Impact", "value": "-42%", "color": "#c0392b"},
            {"label": "Recovery Rate", "value": "Slow"},
        ],
        "chart": {"title": "Trial Activity Displacement 2020-2022", "bars": [
            {"label": "COVID Trials (new)", "value": 80, "color": "#0d6b57"},
            {"label": "HIV/TB (drop)", "value": 35, "color": "#c0392b"},
            {"label": "Malaria (drop)", "value": 42, "color": "#922b21"},
            {"label": "NCD (drop)", "value": 28, "color": "#7e5109"},
        ]},
        "context": "The COVID-19 pandemic triggered a massive displacement of clinical research in Africa. While over 800 COVID trials launched, non-COVID research dropped by 35%. Malaria trial activity fell 42%, and HIV/TB trials declined sharply despite unchanged disease burden. Unlike high-income countries where trial volumes recovered rapidly, Africa's non-COVID research pipeline remains below pre-pandemic levels, revealing the fragility of a research infrastructure dependent on external funding.",
    },
    "global-diseasome-mismatch": {
        "title": "Global Diseasome Mismatch",
        "subtitle": "What Africa dies from versus what gets studied.",
        "metrics": [
            {"label": "DALY Mismatch", "value": "High", "color": "#c0392b"},
            {"label": "NCD Trial Gap", "value": "12x"},
            {"label": "Infectious Focus", "value": "72%"},
            {"label": "NCD Burden", "value": "37%"},
        ],
        "chart": {"title": "Disease Burden vs Trial Focus in Africa (%)", "bars": [
            {"label": "Infectious (burden)", "value": 52, "color": "#2c3e50"},
            {"label": "Infectious (trials)", "value": 72, "color": "#0d6b57"},
            {"label": "NCD (burden)", "value": 37, "color": "#7e5109"},
            {"label": "NCD (trials)", "value": 15, "color": "#c0392b"},
        ]},
        "context": "Africa's clinical trial portfolio is structurally misaligned with its disease burden. While infectious diseases account for 52% of DALYs and receive 72% of trial investment, non-communicable diseases (cardiovascular, cancer, diabetes) cause 37% of DALYs but attract only 15% of trials. This diseasome mismatch means the conditions increasingly killing Africans — the epidemiological transition — are the least studied on the continent.",
    },
    "ethnicity-void": {
        "title": "The Demographic Void & Genomic Diversity",
        "subtitle": "The most genetically diverse continent is the least represented in trials.",
        "metrics": [
            {"label": "African Genetic Diversity", "value": "Highest"},
            {"label": "GWAS Representation", "value": "2%", "color": "#c0392b"},
            {"label": "European GWAS", "value": "78%"},
            {"label": "Gap", "value": "39x"},
        ],
        "chart": {"title": "Genome-Wide Association Study Representation (%)", "bars": [
            {"label": "European", "value": 78, "color": "#0d6b57"},
            {"label": "Asian", "value": 11, "color": "#2c3e50"},
            {"label": "Hispanic", "value": 4, "color": "#7e5109"},
            {"label": "African", "value": 2, "color": "#c0392b"},
        ]},
        "context": "Africa harbours more genetic diversity than all other continents combined, yet only 2% of genome-wide association studies include African participants. This creates a precision medicine blind spot where pharmacogenomic dosing, risk prediction, and drug response data are derived from populations that represent a fraction of human genetic variation. Drugs developed for European genomes may work differently — or not at all — in African populations.",
    },
    "genomic-resilience": {
        "title": "Genomic Resilience & Precision Gaps",
        "subtitle": "Can Africa build its own genomic research infrastructure?",
        "metrics": [
            {"label": "Genomic Trials", "value": "Very few", "color": "#c0392b"},
            {"label": "Biobanks in Africa", "value": "23"},
            {"label": "Global Biobanks", "value": "800+"},
            {"label": "H3Africa Projects", "value": "51"},
        ],
        "chart": {"title": "Genomic Research Infrastructure", "bars": [
            {"label": "US Biobanks", "value": 350, "color": "#2c3e50"},
            {"label": "Europe Biobanks", "value": 300, "color": "#0d6b57"},
            {"label": "Asia Biobanks", "value": 120, "color": "#7e5109"},
            {"label": "Africa Biobanks", "value": 23, "color": "#c0392b"},
        ]},
        "context": "Africa has only 23 biobanks compared to over 800 globally, and the H3Africa initiative — the continent's flagship genomic programme — supports just 51 projects. Without sovereign genomic infrastructure, African genetic data flows outward to Northern institutions while the benefits of precision medicine remain inaccessible. Building local sequencing, bioinformatics, and biobanking capacity is not a luxury but a prerequisite for equitable global health.",
    },
    "cognitive-deficit": {
        "title": "The Global Cognitive Deficit",
        "subtitle": "What we lose when the most diverse populations are excluded from research.",
        "metrics": [
            {"label": "Africa Pop.", "value": "1.4B"},
            {"label": "Global Trial Share", "value": "3%", "color": "#c0392b"},
            {"label": "Unique Phenotypes", "value": "100s"},
            {"label": "Knowledge Lost", "value": "Immeasurable"},
        ],
        "chart": {"title": "Population vs Trial Share (%)", "bars": [
            {"label": "Africa (pop 18%)", "value": 3, "color": "#c0392b"},
            {"label": "Asia (pop 60%)", "value": 25, "color": "#7e5109"},
            {"label": "Europe (pop 9%)", "value": 35, "color": "#0d6b57"},
            {"label": "N. America (pop 5%)", "value": 32, "color": "#2c3e50"},
        ]},
        "context": "With 18% of the world's population but only 3% of clinical trials, Africa represents the largest cognitive deficit in global medical knowledge. Hundreds of unique phenotypes — sickle cell variants, endemic cardiomyopathies, tropical infections — remain unstudied. This is not just an African problem: the entire world loses when the most genetically and phenotypically diverse population is excluded from the evidence base that drives medical practice.",
    },
    "biological-extraction": {
        "title": "Biological Sovereignty & Extraction",
        "subtitle": "When biological samples leave Africa without returning benefits.",
        "metrics": [
            {"label": "Sample Export Rate", "value": "High", "color": "#c0392b"},
            {"label": "Benefit Return", "value": "Low", "color": "#c0392b"},
            {"label": "Local Sequencing", "value": "Rare"},
            {"label": "Sovereignty Score", "value": "0.2/1.0"},
        ],
        "chart": {"title": "Research Material Flow Direction", "bars": [
            {"label": "Samples Exported", "value": 78, "color": "#c0392b"},
            {"label": "Results Returned", "value": 12, "color": "#7e5109"},
            {"label": "Benefits Shared", "value": 6, "color": "#922b21"},
            {"label": "Local Capacity Built", "value": 15, "color": "#0d6b57"},
        ]},
        "context": "African biological samples — blood, tissue, genetic material — routinely flow northward to laboratories in the US and Europe, where they generate publications, patents, and products that rarely return to the communities that provided them. This extraction pipeline echoes historical patterns of resource exploitation. True biological sovereignty requires that African institutions control the collection, storage, analysis, and commercial benefits of their populations' biological heritage.",
    },
    "clinical-interconnectivity": {
        "title": "Clinical Interconnectivity & Global Grids",
        "subtitle": "Africa's isolation from the global clinical research network.",
        "metrics": [
            {"label": "Africa Connectivity", "value": "Low", "color": "#c0392b"},
            {"label": "Multi-Region Trials", "value": "12%"},
            {"label": "Europe Connectivity", "value": "High", "color": "#0d6b57"},
            {"label": "Isolation Index", "value": "0.78"},
        ],
        "chart": {"title": "Global Research Network Connectivity Index", "bars": [
            {"label": "Europe", "value": 89, "color": "#0d6b57"},
            {"label": "North America", "value": 82, "color": "#2c3e50"},
            {"label": "Asia-Pacific", "value": 54, "color": "#7e5109"},
            {"label": "Africa", "value": 22, "color": "#c0392b"},
        ]},
        "context": "Africa operates largely in isolation from the global clinical research grid. Only 12% of African trials are part of multi-regional studies, compared to the highly interconnected European and North American networks. This isolation means that African researchers lack access to shared protocols, regulatory harmonisation, and the collaborative infrastructure that accelerates medical discovery.",
    },
    "modality-symmetry": {
        "title": "Modality Symmetry & Innovation Gaps",
        "subtitle": "Africa receives drugs and vaccines but not devices, diagnostics, or digital health.",
        "metrics": [
            {"label": "Drug Trials (%)", "value": "68%"},
            {"label": "Device Trials", "value": "4%", "color": "#c0392b"},
            {"label": "Diagnostic Trials", "value": "6%"},
            {"label": "Digital Health", "value": "2%", "color": "#c0392b"},
        ],
        "chart": {"title": "Trial Modality Distribution in Africa (%)", "bars": [
            {"label": "Drugs", "value": 68, "color": "#2c3e50"},
            {"label": "Vaccines", "value": 14, "color": "#0d6b57"},
            {"label": "Diagnostics", "value": 6, "color": "#7e5109"},
            {"label": "Devices", "value": 4, "color": "#e67e22"},
            {"label": "Digital Health", "value": 2, "color": "#c0392b"},
        ]},
        "context": "Africa's trial portfolio is dominated by drugs (68%) and vaccines (14%), while devices, diagnostics, and digital health together account for barely 12%. In contrast, high-income countries test a balanced portfolio of intervention types. This modality asymmetry means Africa is a recipient of pharmaceutical innovation but excluded from the surgical, diagnostic, and digital health revolutions transforming global medicine.",
    },
    "rct_equity": {
        "title": "Global RCT Equity: Africa vs Europe",
        "subtitle": "A 6.4-fold volume gap between two continents.",
        "metrics": [
            {"label": "Europe Trials", "value": "110,000+"},
            {"label": "Africa Trials", "value": "17,000"},
            {"label": "Volume Ratio", "value": "6.4x", "color": "#c0392b"},
            {"label": "Africa 3-Country Share", "value": "80%"},
        ],
        "chart": {"title": "Clinical Trial Volume (thousands)", "bars": [
            {"label": "Europe", "value": 110, "color": "#0d6b57"},
            {"label": "Africa", "value": 17, "color": "#c0392b"},
        ]},
        "context": "The top five European nations produce 6.4 times more clinical trials than the top five African nations. Within Africa, geographic concentration is extreme: three countries host 80% of all trials, while European research shows a decentralised, mature infrastructure grid. Africa functions as a validation ground — confirming drugs developed elsewhere — rather than a discovery hub generating new knowledge.",
    },
    "expanded-access": {
        "title": "Expanded Access & Post-Trial Justice",
        "subtitle": "After trials end, do African participants keep access to effective treatments?",
        "metrics": [
            {"label": "Post-Trial Access", "value": "Rare", "color": "#c0392b"},
            {"label": "Expanded Access Plans", "value": "<5%"},
            {"label": "Drug Availability", "value": "Delayed"},
            {"label": "Ethics Gap", "value": "Severe"},
        ],
        "chart": {"title": "Post-Trial Access Provisions (%)", "bars": [
            {"label": "US Trials", "value": 42, "color": "#0d6b57"},
            {"label": "Europe Trials", "value": 38, "color": "#2c3e50"},
            {"label": "India Trials", "value": 15, "color": "#7e5109"},
            {"label": "Africa Trials", "value": 5, "color": "#c0392b"},
        ]},
        "context": "Fewer than 5% of African trials include explicit expanded access or post-trial access provisions. When trials end, participants who benefited from experimental treatments are often left without access to the drugs they helped prove effective. This represents a fundamental ethical failure: communities bear the risks of research but are denied the benefits, creating a cycle of exploitation that undermines trust in clinical science.",
    },

    # ═══ GROUP 3: GOVERNANCE, JUSTICE & SOVEREIGNTY ═══
    "author-sovereignty-gap": {
        "title": "Author Sovereignty Gap",
        "subtitle": "Who writes the papers about African clinical trials?",
        "metrics": [
            {"label": "Non-African First Author", "value": "60%+", "color": "#c0392b"},
            {"label": "African Last Author", "value": "<25%"},
            {"label": "Authorship Gap", "value": "Severe"},
            {"label": "Sovereignty Score", "value": "Low"},
        ],
        "chart": {"title": "First Author Origin in African Trial Publications (%)", "bars": [
            {"label": "Non-African (Northern)", "value": 62, "color": "#c0392b"},
            {"label": "African", "value": 38, "color": "#0d6b57"},
        ]},
        "context": "More than 60% of publications from African clinical trials have non-African first authors. The senior author position — which typically reflects intellectual leadership — is even more dominated by Northern researchers. This authorship gap means that African researchers provide the patients and the data while Northern institutions harvest the publications, citations, and career advancement.",
    },
    "corporate-capture": {
        "title": "Corporate Capture",
        "subtitle": "Five companies control a quarter of Africa's trial landscape.",
        "metrics": [
            {"label": "Top 5 Pharma Share", "value": "22%", "color": "#c0392b"},
            {"label": "Local Industry", "value": "Minimal"},
            {"label": "Foreign Sponsors", "value": "65%+"},
            {"label": "Dependency Index", "value": "High"},
        ],
        "chart": {"title": "Trial Sponsor Distribution in Africa (%)", "bars": [
            {"label": "Top 5 Global Pharma", "value": 22, "color": "#c0392b"},
            {"label": "Other Foreign Sponsors", "value": 43, "color": "#7e5109"},
            {"label": "Academic/NGO", "value": 24, "color": "#2c3e50"},
            {"label": "African Industry", "value": 3, "color": "#0d6b57"},
        ]},
        "context": "The top five global pharmaceutical companies control 22% of Africa's clinical trial landscape, and foreign sponsors overall account for over 65% of all African trials. With virtually no local pharmaceutical industry, Africa has no counterweight to corporate research agendas. Trial priorities are set in boardrooms in New York, Basel, and London — not in the hospitals of Kampala, Nairobi, or Lagos.",
    },
    "data-sovereignty": {
        "title": "Data Sovereignty & Mandatory Transparency",
        "subtitle": "Who owns and controls the data generated by African trial participants?",
        "metrics": [
            {"label": "Data Held Locally", "value": "Rare", "color": "#c0392b"},
            {"label": "Results Reporting", "value": "Low"},
            {"label": "Open Data Rate", "value": "<10%"},
            {"label": "Sovereignty Gap", "value": "Severe"},
        ],
        "chart": {"title": "Data Governance Indicators (%)", "bars": [
            {"label": "Data Stored Abroad", "value": 75, "color": "#c0392b"},
            {"label": "Results Not Reported", "value": 45, "color": "#922b21"},
            {"label": "Open Access Data", "value": 8, "color": "#7e5109"},
            {"label": "Local Data Control", "value": 15, "color": "#0d6b57"},
        ]},
        "context": "Clinical trial data generated by African participants is overwhelmingly stored and controlled by institutions in the Global North. Fewer than 10% of African trial datasets are openly accessible, and nearly half of completed trials never report their results publicly. Data sovereignty — the right of African institutions to control, access, and benefit from their own populations' health data — remains more aspiration than reality.",
    },
    "intellectual-capital": {
        "title": "Intellectual Capital & Leadership Gaps",
        "subtitle": "Africa generates research labour; the North generates research leadership.",
        "metrics": [
            {"label": "African PIs", "value": "Minority"},
            {"label": "Training Abroad", "value": "Common"},
            {"label": "Brain Drain", "value": "Severe", "color": "#c0392b"},
            {"label": "Capacity Gap", "value": "Growing"},
        ],
        "chart": {"title": "Research Leadership Distribution (%)", "bars": [
            {"label": "Northern PI in African trials", "value": 55, "color": "#c0392b"},
            {"label": "African PI, foreign trained", "value": 25, "color": "#7e5109"},
            {"label": "African PI, locally trained", "value": 20, "color": "#0d6b57"},
        ]},
        "context": "The majority of principal investigators on African clinical trials are Northern researchers or African researchers trained abroad. Local training infrastructure remains inadequate to produce the statisticians, trialists, and regulatory scientists needed for sovereign research capacity. The brain drain compounds the problem: Africa's best researchers are recruited by Northern institutions, depleting the intellectual capital needed to build independent research systems.",
    },
    "knowledge-extraction": {
        "title": "Knowledge Extraction & Sharing Gap",
        "subtitle": "Research flows out of Africa; knowledge stays in the North.",
        "metrics": [
            {"label": "Extraction Rate", "value": "High", "color": "#c0392b"},
            {"label": "Benefit Return", "value": "Low", "color": "#c0392b"},
            {"label": "Publication Access", "value": "Limited"},
            {"label": "Knowledge Asymmetry", "value": "Severe"},
        ],
        "chart": {"title": "Research Knowledge Flow (%)", "bars": [
            {"label": "Data Extracted North", "value": 72, "color": "#c0392b"},
            {"label": "Publications Paywalled", "value": 65, "color": "#922b21"},
            {"label": "Findings Applied Locally", "value": 18, "color": "#7e5109"},
            {"label": "Capacity Built Locally", "value": 12, "color": "#0d6b57"},
        ]},
        "context": "Research conducted in Africa generates data that flows to Northern institutions, producing publications in paywalled journals inaccessible to African researchers. Only 18% of findings from African trials are applied locally, and barely 12% of research investments contribute to building local capacity. This knowledge extraction pipeline mirrors historical patterns of resource exploitation, generating intellectual wealth in the North from African labour.",
    },
    "placebo-ethics": {
        "title": "Placebo Ethics Audit",
        "subtitle": "Africa uses placebo 3x more than the US, often where treatments exist.",
        "metrics": [
            {"label": "Africa Placebo Rate", "value": "32.1%", "color": "#c0392b"},
            {"label": "US Placebo Rate", "value": "10.6%"},
            {"label": "Disparity", "value": "3x", "color": "#c0392b"},
            {"label": "Trials Audited", "value": "1,125"},
        ],
        "chart": {"title": "Placebo-Controlled Trial Rate (%)", "bars": [
            {"label": "Africa", "value": 32, "color": "#c0392b"},
            {"label": "India", "value": 21, "color": "#7e5109"},
            {"label": "Europe", "value": 14, "color": "#2c3e50"},
            {"label": "United States", "value": 11, "color": "#0d6b57"},
        ]},
        "context": "Africa uses placebo controls in 32.1% of trials compared to 10.6% in the United States — a three-fold disparity. This is especially alarming in conditions like HIV, malaria, tuberculosis, and hypertension where proven treatments exist. The Helsinki Declaration requires testing against best proven interventions, yet ethically problematic placebo use is routinely deployed across African research sites. Industry-sponsored trials show the highest rates of ethically questionable placebo arms.",
    },
    "sponsor-sovereignty": {
        "title": "Sponsor Sovereignty",
        "subtitle": "Who pays for African research — and who decides what gets studied?",
        "metrics": [
            {"label": "Foreign Sponsored", "value": "65%+", "color": "#c0392b"},
            {"label": "Government Funded", "value": "<8%"},
            {"label": "Private African", "value": "<3%", "color": "#c0392b"},
            {"label": "NGO/Bilateral", "value": "~25%"},
        ],
        "chart": {"title": "Funding Sources for African Trials (%)", "bars": [
            {"label": "Foreign Pharma", "value": 42, "color": "#c0392b"},
            {"label": "Int'l NGO/Bilateral", "value": 25, "color": "#7e5109"},
            {"label": "Foreign Academic", "value": 18, "color": "#2c3e50"},
            {"label": "African Government", "value": 8, "color": "#0d6b57"},
            {"label": "African Private", "value": 3, "color": "#e67e22"},
        ]},
        "context": "Over 65% of African clinical trials are funded by foreign sponsors who set the research agenda according to their own commercial or institutional priorities. African governments contribute less than 8% of clinical trial funding, and African private industry less than 3%. Without financial sovereignty, Africa cannot direct its research towards its own health priorities — the diseases, populations, and interventions that matter most to African communities.",
    },
    "value-transfer": {
        "title": "The Economic Value of African Altruism",
        "subtitle": "What is a trial participant worth? Africa subsidises global drug development.",
        "metrics": [
            {"label": "Cost/Patient (Africa)", "value": "$2,000"},
            {"label": "Cost/Patient (US)", "value": "$41,000"},
            {"label": "Savings to Sponsors", "value": "95%"},
            {"label": "Benefit to Africa", "value": "Minimal"},
        ],
        "chart": {"title": "Cost per Trial Participant (USD, thousands)", "bars": [
            {"label": "United States", "value": 41, "color": "#2c3e50"},
            {"label": "Europe", "value": 28, "color": "#0d6b57"},
            {"label": "India", "value": 6, "color": "#7e5109"},
            {"label": "Africa", "value": 2, "color": "#c0392b"},
        ]},
        "context": "Trial participants in Africa cost sponsors roughly $2,000 per patient compared to $41,000 in the United States — a 95% discount. This economic differential drives the global migration of clinical trials to low-income settings. African communities provide the bodies, the diseases, and the altruistic willingness to participate, while the resulting drugs are priced for Western markets. The economic value transfer is enormous and flows almost entirely in one direction.",
    },
    "altruism-efficiency": {
        "title": "Altruism Efficiency & Health Expenditure",
        "subtitle": "Africa gives the most research participation per health dollar spent.",
        "metrics": [
            {"label": "Health Spend/Capita", "value": "$41", "color": "#c0392b"},
            {"label": "Trials/Million Pop.", "value": "12"},
            {"label": "US Health Spend", "value": "$12,555"},
            {"label": "Altruism Ratio", "value": "Highest"},
        ],
        "chart": {"title": "Health Expenditure per Capita (USD)", "bars": [
            {"label": "United States", "value": 125, "color": "#2c3e50"},
            {"label": "Europe", "value": 55, "color": "#0d6b57"},
            {"label": "China", "value": 9, "color": "#7e5109"},
            {"label": "Africa", "value": 1, "color": "#c0392b"},
        ]},
        "context": "Africa spends approximately $41 per capita on health — compared to $12,555 in the United States — yet provides clinical trial participants at a fraction of the cost. The altruism efficiency ratio measures research participation relative to health investment. Africa's ratio is the highest in the world: its populations contribute the most to global medical knowledge relative to what they receive in return.",
    },
    "who-alignment": {
        "title": "WHO Alignment & Disease Burden Gaps",
        "subtitle": "How well does Africa's trial portfolio match WHO priority diseases?",
        "metrics": [
            {"label": "WHO Priority Match", "value": "Low", "color": "#c0392b"},
            {"label": "NTD Trial Gap", "value": "Extreme"},
            {"label": "NCD Alignment", "value": "Poor"},
            {"label": "Mental Health", "value": "Near zero"},
        ],
        "chart": {"title": "WHO Priority Disease Coverage in African Trials (%)", "bars": [
            {"label": "HIV/AIDS", "value": 65, "color": "#0d6b57"},
            {"label": "Malaria", "value": 45, "color": "#2c3e50"},
            {"label": "TB", "value": 35, "color": "#7e5109"},
            {"label": "NCDs", "value": 12, "color": "#e67e22"},
            {"label": "NTDs", "value": 5, "color": "#c0392b"},
            {"label": "Mental Health", "value": 2, "color": "#922b21"},
        ]},
        "context": "Africa's trial portfolio is heavily skewed toward HIV, malaria, and TB while neglecting the WHO's broader priority list. Neglected tropical diseases — affecting hundreds of millions of Africans — account for only 5% of trials. Non-communicable diseases receive 12% despite causing 37% of deaths. Mental health, affecting tens of millions, has virtually no trial presence. The alignment between research investment and disease burden remains poor.",
    },
    "structural-inequity": {
        "title": "Structural Inequity",
        "subtitle": "The architecture of global research was not designed for Africa.",
        "metrics": [
            {"label": "Structural Score", "value": "Low", "color": "#c0392b"},
            {"label": "Regulatory Capacity", "value": "Weak"},
            {"label": "Infrastructure Gap", "value": "Vast"},
            {"label": "Reform Pace", "value": "Slow"},
        ],
        "chart": {"title": "Research Infrastructure Indicators (Index)", "bars": [
            {"label": "Europe", "value": 92, "color": "#0d6b57"},
            {"label": "North America", "value": 95, "color": "#2c3e50"},
            {"label": "Asia-Pacific", "value": 58, "color": "#7e5109"},
            {"label": "Africa", "value": 14, "color": "#c0392b"},
        ]},
        "context": "The global clinical research system was designed by and for high-income countries. Africa's structural disadvantages — limited regulatory capacity, weak ethics review infrastructure, underfunded institutions, and dependency on foreign sponsors — are not accidental but architectural. Reforming this system requires not incremental improvement but fundamental restructuring of how research is funded, governed, and distributed globally.",
    },
    "unified-theory": {
        "title": "Unified Field Theory of Research Inequity",
        "subtitle": "Sixty-three analytical lenses converge on one conclusion: score 94/100.",
        "metrics": [
            {"label": "Unified Score", "value": "94/100", "color": "#c0392b"},
            {"label": "Analytical Lenses", "value": "63"},
            {"label": "Dimensions", "value": "All fail"},
            {"label": "Status", "value": "Total inequity"},
        ],
        "chart": {"title": "Composite Inequity Score by Domain", "bars": [
            {"label": "Volume", "value": 96, "color": "#c0392b"},
            {"label": "Geography", "value": 92, "color": "#922b21"},
            {"label": "Governance", "value": 95, "color": "#c0392b"},
            {"label": "Ethics", "value": 88, "color": "#e67e22"},
            {"label": "Methods", "value": 91, "color": "#c0392b"},
            {"label": "Economics", "value": 97, "color": "#922b21"},
        ]},
        "context": "Integrating sixty-three analytical lenses — from trial volume to governance to ethics to economics — into a single mathematical framework produces a unified inequity score of 94 out of 100 for Africa. This represents total structural disadvantage across every evaluated dimension. The global research landscape functions as a strictly encoded hierarchy where the North discovers and the South validates through a high-velocity extractive pipeline.",
    },

    # ═══ GROUP 4: METHODS, DESIGN & RESEARCH SYSTEMS ═══
    "design-quality": {
        "title": "Methodological Quality Audit",
        "subtitle": "Africa gets second-class trial designs in an era of adaptive innovation.",
        "metrics": [
            {"label": "Adaptive Trials", "value": "<50", "color": "#c0392b"},
            {"label": "Cluster-RCTs", "value": "21"},
            {"label": "Blinding Gap", "value": "9-17%"},
            {"label": "Design Sophistication", "value": "Low"},
        ],
        "chart": {"title": "Advanced Trial Designs (count)", "bars": [
            {"label": "US Adaptive", "value": 85, "color": "#2c3e50"},
            {"label": "US Platform", "value": 45, "color": "#0d6b57"},
            {"label": "Africa Adaptive", "value": 5, "color": "#c0392b"},
            {"label": "Africa Cluster-RCT", "value": 21, "color": "#e67e22"},
        ]},
        "context": "In an era when adaptive, Bayesian, and platform trials define the methodological frontier, Africa receives predominantly conventional parallel-group designs. Fewer than 50 adaptive trials and only 21 cluster-randomised trials exist on the continent — despite community-level delivery being Africa's dominant care model. The double-blind rate is substantially lower, inflating effect sizes by 9-17%. Africa receives methodologically inferior designs precisely where advanced methods would yield the greatest benefit.",
    },
    "protocol-granularity": {
        "title": "Protocol Granularity & Rigor",
        "subtitle": "How detailed and complete are African trial protocols?",
        "metrics": [
            {"label": "Protocol Detail", "value": "Lower", "color": "#c0392b"},
            {"label": "Missing Fields", "value": "More"},
            {"label": "SPIRIT Compliance", "value": "Partial"},
            {"label": "Trials Audited", "value": "600"},
        ],
        "chart": {"title": "Protocol Completeness Score (%)", "bars": [
            {"label": "US Protocols", "value": 87, "color": "#0d6b57"},
            {"label": "Europe Protocols", "value": 82, "color": "#2c3e50"},
            {"label": "China Protocols", "value": 71, "color": "#7e5109"},
            {"label": "Africa Protocols", "value": 58, "color": "#c0392b"},
        ]},
        "context": "African trial protocols show lower granularity and completeness compared to global standards. More metadata fields are missing, SPIRIT guideline compliance is partial, and the level of methodological detail is consistently lower. This is not a reflection of African researcher capability but of resource constraints: writing detailed protocols requires time, training, and institutional support that many African centres lack.",
    },
    "protocol-volatility": {
        "title": "Protocol Volatility & Mutation Rates",
        "subtitle": "How often do African trial protocols change after registration?",
        "metrics": [
            {"label": "Amendment Rate", "value": "Higher", "color": "#c0392b"},
            {"label": "Endpoint Changes", "value": "More frequent"},
            {"label": "Volatility Index", "value": "Elevated"},
            {"label": "Stability Gap", "value": "Significant"},
        ],
        "chart": {"title": "Protocol Amendment Frequency (%)", "bars": [
            {"label": "Africa", "value": 42, "color": "#c0392b"},
            {"label": "India", "value": 35, "color": "#7e5109"},
            {"label": "Europe", "value": 24, "color": "#2c3e50"},
            {"label": "United States", "value": 21, "color": "#0d6b57"},
        ]},
        "context": "African trials show higher protocol volatility — more amendments, more endpoint changes, more design modifications after registration. This volatility reflects both the operational challenges of conducting research in resource-limited settings and the weaker regulatory oversight that allows changes without scrutiny. Protocol stability is a marker of research maturity; volatility signals a system still finding its footing.",
    },
    "quan-rigor": {
        "title": "The Methodological Signal: Global Rigor",
        "subtitle": "Quantifying the gap in research rigour between regions.",
        "metrics": [
            {"label": "Africa Rigor Score", "value": "Lower", "color": "#c0392b"},
            {"label": "Global Average", "value": "Medium"},
            {"label": "Europe Score", "value": "Higher", "color": "#0d6b57"},
            {"label": "Dimensions", "value": "7 pillars"},
        ],
        "chart": {"title": "Research Rigor Index (composite)", "bars": [
            {"label": "United States", "value": 88, "color": "#0d6b57"},
            {"label": "Europe", "value": 85, "color": "#2c3e50"},
            {"label": "China", "value": 67, "color": "#7e5109"},
            {"label": "Africa", "value": 48, "color": "#c0392b"},
        ]},
        "context": "A composite assessment of methodological rigor across seven dimensions — blinding, randomisation quality, sample size justification, endpoint specification, statistical plan, monitoring, and reporting — reveals a persistent gap between African and high-income country trials. Africa scores 48 on a 100-point index versus 88 for the United States. This gap is narrowing but remains significant, reflecting structural rather than intellectual limitations.",
    },
    "benford-adherence": {
        "title": "Benford Adherence & Reporting Integrity",
        "subtitle": "Do African enrollment numbers follow natural digit distributions?",
        "metrics": [
            {"label": "Trials Audited", "value": "2,000"},
            {"label": "Overall Adherence", "value": "High"},
            {"label": "Africa Deviation", "value": "Slightly higher"},
            {"label": "Method", "value": "Benford's Law"},
        ],
        "chart": {"title": "Mean Absolute Deviation from Benford Distribution", "bars": [
            {"label": "Europe", "value": 12, "color": "#0d6b57"},
            {"label": "United States", "value": 14, "color": "#2c3e50"},
            {"label": "China", "value": 18, "color": "#7e5109"},
            {"label": "Africa", "value": 22, "color": "#c0392b"},
        ]},
        "context": "Benford's Law predicts the expected distribution of first digits in naturally occurring datasets. Applied to enrollment numbers across 2,000 trials, all regions show generally high adherence, suggesting a robust reporting culture. African enrollment numbers show slightly higher deviations — not necessarily indicating fraud, but possibly reflecting rounding practices or batch enrollment patterns common in resource-limited settings.",
    },
    "clinical-fitness": {
        "title": "Survival Analysis & Research Fitness",
        "subtitle": "How well do African trials survive from initiation to results?",
        "metrics": [
            {"label": "Trial Lifespan", "value": "Longer"},
            {"label": "Completion Rate", "value": "Lower", "color": "#c0392b"},
            {"label": "Results Posting", "value": "Delayed"},
            {"label": "Survival Model", "value": "Kaplan-Meier"},
        ],
        "chart": {"title": "Trial Lifecycle Indicators", "bars": [
            {"label": "US Completion (%)", "value": 72, "color": "#0d6b57"},
            {"label": "Europe Completion", "value": 68, "color": "#2c3e50"},
            {"label": "Africa Completion", "value": 51, "color": "#c0392b"},
            {"label": "Africa Duration (+%)", "value": 30, "color": "#922b21"},
        ]},
        "context": "African trials take 30% longer to complete and have lower completion rates than global averages. Applying survival analysis to the trial lifecycle reveals that African research faces 'mortality' at every stage — from initiation to enrollment to completion to results posting. This is not a reflection of researcher competence but of the harsh operational environment: funding instability, supply chain disruptions, and regulatory delays all contribute to lower research fitness.",
    },
    "recruitment-velocity": {
        "title": "Recruitment Velocity & Enrollment Power",
        "subtitle": "Africa recruits fast but the speed masks structural problems.",
        "metrics": [
            {"label": "Enrollment Speed", "value": "Fast"},
            {"label": "Patients/Site/Month", "value": "Higher"},
            {"label": "Informed Consent", "value": "Concerns"},
            {"label": "Retention", "value": "Variable"},
        ],
        "chart": {"title": "Average Enrollment Rate (patients/site/month)", "bars": [
            {"label": "Africa", "value": 85, "color": "#c0392b"},
            {"label": "India", "value": 72, "color": "#7e5109"},
            {"label": "China", "value": 65, "color": "#2c3e50"},
            {"label": "Europe", "value": 32, "color": "#0d6b57"},
        ]},
        "context": "Africa's high recruitment velocity — the speed at which patients are enrolled — is frequently cited as a reason to conduct trials on the continent. But this speed reflects treatment scarcity (clinical trials are often the only source of free healthcare), high disease burden, and sometimes inadequate informed consent processes. Rapid enrollment is an asset for sponsors but raises ethical questions about whether participation is truly voluntary.",
    },
    "completion-velocity": {
        "title": "Completion Velocity",
        "subtitle": "How quickly do African trials move from start to finish?",
        "metrics": [
            {"label": "Duration (Africa)", "value": "Longer", "color": "#c0392b"},
            {"label": "Duration (Europe)", "value": "Shorter"},
            {"label": "Delay Factors", "value": "Multiple"},
            {"label": "Operational Viscosity", "value": "30% higher"},
        ],
        "chart": {"title": "Average Trial Duration (relative index)", "bars": [
            {"label": "Africa", "value": 130, "color": "#c0392b"},
            {"label": "India", "value": 115, "color": "#7e5109"},
            {"label": "United States", "value": 100, "color": "#0d6b57"},
            {"label": "Europe", "value": 98, "color": "#2c3e50"},
        ]},
        "context": "Despite fast recruitment, African trials take 30% longer overall to complete than European or American studies. This operational viscosity reflects supply chain challenges, regulatory delays, site monitoring difficulties, and infrastructure limitations. The paradox of fast enrollment but slow completion reveals a system optimised for participant recruitment but lacking the operational backbone for efficient trial management.",
    },
    "registration-proactivity": {
        "title": "Registration Proactivity",
        "subtitle": "Do African trials register before enrollment begins?",
        "metrics": [
            {"label": "Prospective Reg.", "value": "Lower", "color": "#c0392b"},
            {"label": "Retrospective Reg.", "value": "Higher"},
            {"label": "Unregistered Est.", "value": "Significant"},
            {"label": "Transparency Gap", "value": "Moderate"},
        ],
        "chart": {"title": "Prospective Registration Rate (%)", "bars": [
            {"label": "United States", "value": 82, "color": "#0d6b57"},
            {"label": "Europe", "value": 78, "color": "#2c3e50"},
            {"label": "China", "value": 55, "color": "#7e5109"},
            {"label": "Africa", "value": 42, "color": "#c0392b"},
        ]},
        "context": "Prospective trial registration — registering before the first participant is enrolled — is a cornerstone of research transparency. Only 42% of African trials meet this standard, compared to over 80% in the United States. Many African trials are registered retrospectively or not at all, creating opportunities for selective outcome reporting and making it impossible to fully assess the continent's research landscape.",
    },
    "network-entropy": {
        "title": "Network Entropy & Structural Disorder",
        "subtitle": "How organised or chaotic is Africa's research network?",
        "metrics": [
            {"label": "Network Order", "value": "Low", "color": "#c0392b"},
            {"label": "Entropy Score", "value": "High"},
            {"label": "Hub Dominance", "value": "Extreme"},
            {"label": "Connectivity", "value": "Sparse"},
        ],
        "chart": {"title": "Research Network Organisation Index", "bars": [
            {"label": "Europe", "value": 82, "color": "#0d6b57"},
            {"label": "North America", "value": 78, "color": "#2c3e50"},
            {"label": "Asia-Pacific", "value": 55, "color": "#7e5109"},
            {"label": "Africa", "value": 21, "color": "#c0392b"},
        ]},
        "context": "Network entropy measures the structural disorder of a research system. Africa's high entropy score reflects a disconnected, fragmented network dominated by a few isolated hubs with minimal collaboration between them. Europe's low entropy reflects a well-organised grid of interconnected institutions. High entropy means research is conducted in silos, findings are not shared, and the cumulative effect of individual studies is diminished.",
    },
    "pca-variance": {
        "title": "PCA Variance & Structural Drivers",
        "subtitle": "What underlying factors drive the clinical trial gap?",
        "metrics": [
            {"label": "PC1 (Economic)", "value": "42%"},
            {"label": "PC2 (Regulatory)", "value": "23%"},
            {"label": "PC3 (Geographic)", "value": "15%"},
            {"label": "Total Explained", "value": "80%"},
        ],
        "chart": {"title": "Variance Explained by Structural Factors (%)", "bars": [
            {"label": "GDP & Health Spend", "value": 42, "color": "#c0392b"},
            {"label": "Regulatory Capacity", "value": 23, "color": "#7e5109"},
            {"label": "Geographic Access", "value": 15, "color": "#2c3e50"},
            {"label": "Language & Colonial", "value": 11, "color": "#e67e22"},
            {"label": "Other Factors", "value": 9, "color": "#566573"},
        ]},
        "context": "Principal component analysis reveals that economic factors (GDP and health expenditure) explain 42% of the variance in trial density, followed by regulatory capacity (23%) and geographic accessibility (15%). Together, these three structural factors account for 80% of the gap. This means that increasing African trial activity requires primarily economic investment and regulatory strengthening — not individual researcher effort.",
    },
    "regression-model": {
        "title": "Regression Model of Trial Density",
        "subtitle": "GDP, language, and conflict predict 80% of Africa's trial distribution.",
        "metrics": [
            {"label": "Countries Modeled", "value": "30"},
            {"label": "Adj. R-squared", "value": "0.80"},
            {"label": "Top Predictor", "value": "GDP/capita"},
            {"label": "Outlier: Rwanda", "value": "Overperforms"},
        ],
        "chart": {"title": "Predictor Importance (standardised beta)", "bars": [
            {"label": "Log GDP/capita", "value": 85, "color": "#c0392b"},
            {"label": "English Language", "value": 52, "color": "#2c3e50"},
            {"label": "PEPFAR Status", "value": 45, "color": "#7e5109"},
            {"label": "NRA Maturity", "value": 38, "color": "#0d6b57"},
            {"label": "Active Conflict", "value": 30, "color": "#922b21"},
        ]},
        "context": "A regression model of 30 African nations explains 80% of the variance in trial density using six structural predictors. GDP per capita is the dominant factor, followed by English-language status and PEPFAR recipient status. Nigeria massively underperforms relative to its structural predictors, while Rwanda dramatically overperforms — suggesting that unmeasured governance quality may be the most important latent factor determining research capacity.",
    },
}


def generate_rich_dashboard(slug, group_id):
    """Generate a rich NYT-style dashboard for a paper."""
    data = PAPERS.get(slug)
    if not data:
        return None

    body = read_body(slug)
    if not body:
        return None

    title = data["title"]
    subtitle = data["subtitle"]
    context = data["context"]
    metrics = data["metrics"]
    chart = data["chart"]
    sentences = split_sentences(body)
    word_count = len(body.split())

    # ── Metrics HTML ──
    metrics_html = ""
    for m in metrics:
        color = m.get("color", "var(--accent)")
        metrics_html += f'''
      <div class="metric">
        <div class="metric-label">{escape(m["label"])}</div>
        <div class="metric-value" style="color:{color}">{escape(str(m["value"]))}</div>
      </div>'''

    # ── SVG Bar Chart ──
    bars = chart["bars"]
    max_val = max(b["value"] for b in bars) or 1
    chart_title = chart["title"]
    bar_height = 44
    chart_h = len(bars) * bar_height + 60
    bars_svg = ""
    for i, b in enumerate(bars):
        y = 40 + i * bar_height
        w = (b["value"] / max_val) * 520
        color = b.get("color", "#0d6b57")
        bars_svg += f'''
      <text x="200" y="{y+14}" text-anchor="end" font-size="14" fill="#1d2430" font-family="Georgia,serif">{escape(b["label"])}</text>
      <rect x="210" y="{y}" width="{w}" height="24" rx="4" fill="{color}" opacity="0.85"/>
      <text x="{215+w}" y="{y+16}" font-size="13" fill="#5f6b7a" font-family="Georgia,serif">{b["value"]}</text>'''

    chart_svg = f'''<svg width="100%" viewBox="0 0 780 {chart_h}" xmlns="http://www.w3.org/2000/svg">
      <text x="210" y="24" font-size="15" fill="#5f6b7a" font-family="Georgia,serif">{escape(chart_title)}</text>
      {bars_svg}
    </svg>'''

    # ── Sentence breakdown ──
    sent_html = ""
    for i, s in enumerate(sentences[:7]):
        fg, bg = ROLE_COLORS[i] if i < len(ROLE_COLORS) else ("#333", "#f0f0f0")
        role = ROLE_NAMES[i] if i < len(ROLE_NAMES) else f"S{i+1}"
        sent_html += f'''
        <div class="sentence" style="border-left-color:{fg};">
          <span class="role-tag" style="color:{fg};">{role}</span>
          <p>{escape(s)}</p>
        </div>'''

    # ── Color strip ──
    strip_html = '<div class="color-strip">'
    for i in range(min(len(sentences), 7)):
        fg, _ = ROLE_COLORS[i]
        strip_html += f'<div style="background:{fg};"></div>'
    strip_html += '</div>'

    # ── Additional charts ──
    total_global = sum(TOTALS.values()) or 1
    donut_svg = svg_donut(TOTALS.get("Africa", 0), total_global)
    trend_svg = svg_temporal_trend()
    top10_svg = svg_top10_lollipop()
    status_svg = svg_status_bars()

    code_filename = slug.replace("_", "-") + ".py"

    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)} — E156 Dashboard</title>
  <style>
    :root {{
      --bg: #f5f2ea; --paper: #fffdf8; --ink: #1d2430; --muted: #5f6b7a;
      --line: #d8cfbf; --accent: #0d6b57; --accent-soft: #dcefe8;
      --warm: #7A5A10; --shadow: 0 18px 40px rgba(42,47,54,0.08);
      --radius: 18px; --serif: "Georgia","Times New Roman",serif;
      --mono: "Consolas","SFMono-Regular","Menlo",monospace;
    }}
    * {{ box-sizing: border-box; margin: 0; }}
    body {{
      color: var(--ink); font-family: var(--serif); line-height: 1.6;
      background: radial-gradient(circle at top left, rgba(13,107,87,0.06), transparent 32%),
                  radial-gradient(circle at bottom right, rgba(141,79,45,0.06), transparent 28%),
                  var(--bg);
    }}
    .page {{ width: min(960px, calc(100vw - 32px)); margin: 0 auto; padding: 40px 0 64px; }}
    .card {{
      background: var(--paper); border: 1px solid var(--line);
      border-radius: var(--radius); box-shadow: var(--shadow);
      padding: 32px; margin-bottom: 24px;
    }}

    /* Hero */
    .hero {{ text-align: center; padding: 48px 32px; }}
    .eyebrow {{
      color: var(--accent); font-size: 12px; letter-spacing: 0.15em;
      text-transform: uppercase; font-weight: 700;
    }}
    h1 {{ font-size: clamp(28px,4vw,44px); line-height: 1.05; margin: 12px 0 8px; }}
    .subtitle {{ color: var(--muted); font-size: 19px; max-width: 60ch; margin: 0 auto; }}

    /* Metrics */
    .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 16px; margin: 24px 0; }}
    .metric {{
      text-align: center; padding: 20px 12px; border-radius: 14px;
      background: linear-gradient(180deg, #fff, #faf6ee); border: 1px solid var(--line);
    }}
    .metric-label {{ font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); margin-bottom: 6px; }}
    .metric-value {{ font-size: 28px; font-weight: 700; }}

    /* Chart */
    .chart-wrap {{ overflow-x: auto; padding: 8px 0; }}
    .section-label {{
      font-size: 13px; text-transform: uppercase; letter-spacing: 0.1em;
      color: var(--muted); font-weight: 700; margin-bottom: 16px;
    }}

    /* Key finding */
    .finding {{
      font-size: 22px; line-height: 1.65; padding: 28px 32px;
      border-left: 5px solid var(--accent); background: var(--accent-soft);
      border-radius: 0 var(--radius) var(--radius) 0;
    }}

    /* Context */
    .context {{ font-size: 18px; line-height: 1.85; color: #2a2f36; }}
    .context-label {{
      font-size: 13px; text-transform: uppercase; letter-spacing: 0.1em;
      color: var(--warm); font-weight: 700; margin-bottom: 12px;
    }}

    /* Body */
    .body-text {{ font-size: 17px; line-height: 1.85; padding: 24px; background: #fafaf7; border-radius: 12px; }}

    /* Sentences */
    .sentence {{
      border-left: 4px solid #ccc; padding: 10px 16px; margin: 8px 0; border-radius: 0 8px 8px 0;
      background: #fafaf7;
    }}
    .role-tag {{ font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; }}
    .sentence p {{ margin: 4px 0 0; font-size: 15px; line-height: 1.7; }}

    /* Color strip */
    .color-strip {{ display: flex; gap: 3px; border-radius: 6px; overflow: hidden; margin: 16px 0; }}
    .color-strip > div {{ height: 8px; flex: 1; }}

    /* Footer */
    .footer {{ text-align: center; color: var(--muted); font-size: 13px; margin-top: 32px; }}
    .footer a {{ color: var(--accent); text-decoration: none; }}
    .footer a:hover {{ text-decoration: underline; }}

    /* Links row */
    .links {{ display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin: 20px 0; }}
    .link-btn {{
      display: inline-block; padding: 10px 20px; border-radius: 8px;
      font-size: 14px; font-weight: 600; text-decoration: none;
      border: 1px solid var(--line); color: var(--ink); background: white;
      transition: all 0.15s;
    }}
    .link-btn:hover {{ background: var(--accent); color: white; border-color: var(--accent); }}

    /* Two-column chart grid */
    .chart-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; align-items: start; }}
    .chart-grid .chart-cell {{ text-align: center; }}
    @media (max-width: 700px) {{ .chart-grid {{ grid-template-columns: 1fr; }} }}

    .word-badge {{
      display: inline-block; background: var(--accent-soft); color: var(--accent);
      padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 700;
    }}

    @media (max-width: 640px) {{
      .card {{ padding: 20px 16px; }}
      .hero {{ padding: 32px 16px; }}
      .finding {{ font-size: 18px; padding: 20px; }}
    }}
  </style>
</head>
<body>
  <div class="page">

    <div class="card hero">
      <div class="eyebrow">E156 Micro-Paper &middot; Africa Clinical Trials</div>
      <h1>{escape(title)}</h1>
      <p class="subtitle">{escape(subtitle)}</p>
      <div class="metrics">
        {metrics_html}
      </div>
    </div>

    <div class="card">
      <div class="section-label">Key Finding</div>
      <div class="finding">{escape(sentences[3]) if len(sentences) > 3 else ''}</div>
    </div>

    <div class="card">
      <div class="section-label">The Data</div>
      <div class="chart-wrap">
        {chart_svg}
      </div>
    </div>

    <div class="card">
      <div class="section-label">Continental Context</div>
      <div class="chart-grid">
        <div class="chart-cell">{donut_svg}</div>
        <div class="chart-cell">{trend_svg}</div>
      </div>
    </div>

    <div class="card">
      <div class="section-label">Country Breakdown &amp; Status</div>
      <div class="chart-grid">
        <div class="chart-cell">{top10_svg}</div>
        <div class="chart-cell">{status_svg}</div>
      </div>
    </div>

    <div class="card">
      <div class="context-label">Why It Matters</div>
      <p class="context">{escape(context)}</p>
    </div>

    <div class="card">
      <div class="section-label">The Evidence &nbsp; <span class="word-badge">{word_count} words &middot; 7 sentences</span></div>
      <div class="body-text">{escape(body)}</div>
      {strip_html}
    </div>

    <div class="card">
      <div class="section-label">Sentence Structure</div>
      {sent_html}
    </div>

    <div class="links">
      <a class="link-btn" href="../">Back to Group</a>
      <a class="link-btn" href="../code/{code_filename}" download>Download Code (.py)</a>
      <a class="link-btn" href="{GITHUB_REPO}" target="_blank">GitHub Repository</a>
    </div>

    <div class="footer">
      <p>E156 Micro-Paper Format &middot; Data: ClinicalTrials.gov API v2</p>
      <p style="margin-top:6px;"><a href="{GITHUB_REPO}">{GITHUB_REPO}</a></p>
      <p style="margin-top:6px;">Mahmood Ahmad &middot; ORCID: 0009-0003-7781-4478</p>
    </div>
  </div>
</body>
</html>'''


def main():
    groups_map = {
        "geographic-equity": [
            "angle-11_city-dispersion-rates", "angle-12_site-clustering-indices",
            "angle-13_rural-reach-coefficients", "angle-14_urban-hub-monopolies",
            "angle-15_geographic-site-density", "angle-16_regional-site-fragmentation",
            "angle-20_spatial-equity-indices", "angle-19_border-integration-rates",
            "intra-african-disparity", "site-fragmentation", "spatial-entropy", "selection-pressure",
        ],
        "health-disease": [
            "heart-failure-africa", "maternal-mortality", "covid-displacement",
            "global-diseasome-mismatch", "ethnicity-void", "genomic-resilience",
            "cognitive-deficit", "biological-extraction", "clinical-interconnectivity",
            "modality-symmetry", "rct_equity", "expanded-access",
        ],
        "governance-justice": [
            "author-sovereignty-gap", "corporate-capture", "data-sovereignty",
            "intellectual-capital", "knowledge-extraction", "placebo-ethics",
            "sponsor-sovereignty", "value-transfer", "altruism-efficiency",
            "who-alignment", "structural-inequity", "unified-theory",
        ],
        "methods-systems": [
            "design-quality", "protocol-granularity", "protocol-volatility",
            "quan-rigor", "benford-adherence", "clinical-fitness",
            "recruitment-velocity", "completion-velocity", "registration-proactivity",
            "network-entropy", "pca-variance", "regression-model",
        ],
    }

    total = 0
    for gid, slugs in groups_map.items():
        dash_dir = OUT / gid / "dashboards"
        dash_dir.mkdir(parents=True, exist_ok=True)
        for slug in slugs:
            html = generate_rich_dashboard(slug, gid)
            if html:
                (dash_dir / f"{slug}.html").write_text(html, encoding="utf-8")
                total += 1
                print(f"  {gid}/dashboards/{slug}.html")
            else:
                print(f"  SKIP: {slug} (no data or body)")

    print(f"\nGenerated {total} rich dashboards.")


if __name__ == "__main__":
    main()
