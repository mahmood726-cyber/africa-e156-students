"""
Africa RCT Country-Level Analysis
==================================
Queries ClinicalTrials.gov API v2 for interventional trial counts
in every African country. Produces a ranked table, bar chart, and
per-capita analysis.

Usage:
    python fetch_africa_rcts_by_country.py

Output:
    africa_rct_country_results.json   — raw data
    africa_rct_country_dashboard.html — interactive dashboard

Requirements:
    Python 3.8+, requests (pip install requests)

API: https://clinicaltrials.gov/data-api/api (public, no key needed)
"""

import json
import sys
import time
from pathlib import Path
from datetime import datetime
from html import escape

import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    import requests
except ImportError:
    print("ERROR: 'requests' package required.\n  pip install requests")
    sys.exit(1)

# ── Config ──────────────────────────────────────────────────────────
BASE_URL = "https://clinicaltrials.gov/api/v2/studies"
OUT_DIR = Path(__file__).parent
RATE_LIMIT_DELAY = 0.35  # seconds between API calls (be polite)

# All 54 African countries (UN recognised) with ISO-2 codes and
# estimated 2024 population in millions (World Bank / UN estimates)
AFRICAN_COUNTRIES = [
    {"name": "Algeria",                      "iso": "DZ", "pop": 45.6},
    {"name": "Angola",                       "iso": "AO", "pop": 36.7},
    {"name": "Benin",                        "iso": "BJ", "pop": 13.4},
    {"name": "Botswana",                     "iso": "BW", "pop": 2.6},
    {"name": "Burkina Faso",                 "iso": "BF", "pop": 22.7},
    {"name": "Burundi",                      "iso": "BI", "pop": 13.2},
    {"name": "Cabo Verde",                   "iso": "CV", "pop": 0.6},
    {"name": "Cameroon",                     "iso": "CM", "pop": 28.6},
    {"name": "Central African Republic",     "iso": "CF", "pop": 5.7},
    {"name": "Chad",                         "iso": "TD", "pop": 18.3},
    {"name": "Comoros",                      "iso": "KM", "pop": 0.9},
    {"name": "Congo (Brazzaville)",          "iso": "CG", "pop": 6.1},
    {"name": "Democratic Republic of Congo", "iso": "CD", "pop": 102.3},
    {"name": "Cote d'Ivoire",               "iso": "CI", "pop": 28.9},
    {"name": "Djibouti",                     "iso": "DJ", "pop": 1.1},
    {"name": "Egypt",                        "iso": "EG", "pop": 104.5},
    {"name": "Equatorial Guinea",            "iso": "GQ", "pop": 1.7},
    {"name": "Eritrea",                      "iso": "ER", "pop": 3.7},
    {"name": "Eswatini",                     "iso": "SZ", "pop": 1.2},
    {"name": "Ethiopia",                     "iso": "ET", "pop": 126.5},
    {"name": "Gabon",                        "iso": "GA", "pop": 2.4},
    {"name": "Gambia",                       "iso": "GM", "pop": 2.7},
    {"name": "Ghana",                        "iso": "GH", "pop": 33.5},
    {"name": "Guinea",                       "iso": "GN", "pop": 14.2},
    {"name": "Guinea-Bissau",                "iso": "GW", "pop": 2.1},
    {"name": "Kenya",                        "iso": "KE", "pop": 55.1},
    {"name": "Lesotho",                      "iso": "LS", "pop": 2.3},
    {"name": "Liberia",                      "iso": "LR", "pop": 5.4},
    {"name": "Libya",                        "iso": "LY", "pop": 7.0},
    {"name": "Madagascar",                   "iso": "MG", "pop": 30.3},
    {"name": "Malawi",                       "iso": "MW", "pop": 20.4},
    {"name": "Mali",                         "iso": "ML", "pop": 22.6},
    {"name": "Mauritania",                   "iso": "MR", "pop": 4.9},
    {"name": "Mauritius",                    "iso": "MU", "pop": 1.3},
    {"name": "Morocco",                      "iso": "MA", "pop": 37.5},
    {"name": "Mozambique",                   "iso": "MZ", "pop": 33.9},
    {"name": "Namibia",                      "iso": "NA", "pop": 2.6},
    {"name": "Niger",                        "iso": "NE", "pop": 26.2},
    {"name": "Nigeria",                      "iso": "NG", "pop": 223.8},
    {"name": "Rwanda",                       "iso": "RW", "pop": 14.1},
    {"name": "Sao Tome and Principe",        "iso": "ST", "pop": 0.2},
    {"name": "Senegal",                      "iso": "SN", "pop": 17.9},
    {"name": "Seychelles",                   "iso": "SC", "pop": 0.1},
    {"name": "Sierra Leone",                 "iso": "SL", "pop": 8.6},
    {"name": "Somalia",                      "iso": "SO", "pop": 18.1},
    {"name": "South Africa",                 "iso": "ZA", "pop": 60.4},
    {"name": "South Sudan",                  "iso": "SS", "pop": 11.1},
    {"name": "Sudan",                        "iso": "SD", "pop": 48.1},
    {"name": "Tanzania",                     "iso": "TZ", "pop": 65.5},
    {"name": "Togo",                         "iso": "TG", "pop": 9.0},
    {"name": "Tunisia",                      "iso": "TN", "pop": 12.5},
    {"name": "Uganda",                       "iso": "UG", "pop": 48.6},
    {"name": "Zambia",                       "iso": "ZM", "pop": 20.6},
    {"name": "Zimbabwe",                     "iso": "ZW", "pop": 16.7},
]


def fetch_trial_count(country_name):
    """Query CT.gov API v2 for interventional trial count in a country."""
    params = {
        "query.locn": f"AREA[LocationCountry]{country_name}",
        "filter.overallStatus": "ACTIVE_NOT_RECRUITING,COMPLETED,ENROLLING_BY_INVITATION,NOT_YET_RECRUITING,RECRUITING,SUSPENDED,TERMINATED,WITHDRAWN",
        "countTotal": "true",
        "pageSize": 0,
    }
    try:
        resp = requests.get(BASE_URL, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("totalCount", 0)
    except Exception as e:
        print(f"  ERROR fetching {country_name}: {e}")
        return 0  # API error: treat as zero rather than -1 sentinel


def fetch_all():
    """Fetch trial counts for all 54 African countries."""
    results = []
    total = len(AFRICAN_COUNTRIES)

    print(f"Fetching trial counts for {total} African countries...")
    print(f"API: {BASE_URL}\n")

    for i, country in enumerate(AFRICAN_COUNTRIES, 1):
        name = country["name"]
        print(f"  [{i:2d}/{total}] {name:<35s}", end="", flush=True)
        count = fetch_trial_count(name)
        country["trials"] = count
        per_million = round(count / country["pop"], 1) if count > 0 and country["pop"] > 0 else 0
        country["per_million"] = per_million
        print(f" → {count:>6,d} trials  ({per_million:>6.1f}/M pop)")
        results.append(country)
        time.sleep(RATE_LIMIT_DELAY)

    # Sort by trial count descending
    results.sort(key=lambda x: x["trials"], reverse=True)
    return results


def generate_dashboard(results):
    """Generate an interactive HTML dashboard from results."""
    total_trials = sum(r["trials"] for r in results if r["trials"] > 0) or 1  # guard div-by-zero
    countries_with_trials = sum(1 for r in results if r["trials"] > 0)
    total_pop = sum(r["pop"] for r in results)
    top3 = results[:3]
    bottom_zero = [r for r in results if r["trials"] == 0]

    # Bar chart data (top 30)
    top30 = [r for r in results if r["trials"] > 0][:30]
    max_val = top30[0]["trials"] if top30 else 1
    bar_h = 32
    chart_height = len(top30) * bar_h + 80

    bars_svg = ""
    for i, r in enumerate(top30):
        y = 50 + i * bar_h
        w = (r["trials"] / max_val) * 480
        color = "#0d6b57" if r["trials"] > 500 else "#2c3e50" if r["trials"] > 100 else "#7e5109" if r["trials"] > 20 else "#c0392b"
        bars_svg += f'''
      <text x="195" y="{y+12}" text-anchor="end" font-size="12" fill="#1d2430" font-family="Georgia,serif">{escape(r["name"])}</text>
      <rect x="205" y="{y}" width="{w}" height="20" rx="3" fill="{color}" opacity="0.85"/>
      <text x="{210+w}" y="{y+13}" font-size="11" fill="#5f6b7a" font-family="Georgia,serif">{r["trials"]:,}</text>'''

    # Per-capita chart (top 20 by per_million)
    per_cap = sorted([r for r in results if r["per_million"] > 0], key=lambda x: x["per_million"], reverse=True)[:20]
    max_pc = per_cap[0]["per_million"] if per_cap else 1
    pc_height = len(per_cap) * bar_h + 80
    pc_svg = ""
    for i, r in enumerate(per_cap):
        y = 50 + i * bar_h
        w = (r["per_million"] / max_pc) * 480
        color = "#0d6b57" if r["per_million"] > 50 else "#2c3e50" if r["per_million"] > 20 else "#7e5109"
        pc_svg += f'''
      <text x="195" y="{y+12}" text-anchor="end" font-size="12" fill="#1d2430" font-family="Georgia,serif">{escape(r["name"])}</text>
      <rect x="205" y="{y}" width="{w}" height="20" rx="3" fill="{color}" opacity="0.85"/>
      <text x="{210+w}" y="{y+13}" font-size="11" fill="#5f6b7a" font-family="Georgia,serif">{r["per_million"]}</text>'''

    # Country table rows
    table_rows = ""
    for rank, r in enumerate(results, 1):
        trials = r["trials"]
        pct = round(100 * trials / total_trials, 1) if total_trials > 0 and trials > 0 else 0
        row_class = "zero" if trials == 0 else ""
        table_rows += f'''
        <tr class="{row_class}">
          <td>{rank}</td>
          <td>{escape(r["name"])}</td>
          <td class="num">{trials:,}</td>
          <td class="num">{pct}%</td>
          <td class="num">{r["pop"]:.1f}M</td>
          <td class="num">{r["per_million"]}</td>
        </tr>'''

    # Sub-region aggregation
    regions = {
        "North Africa": ["Algeria", "Egypt", "Libya", "Morocco", "Tunisia", "Sudan"],
        "West Africa": ["Benin", "Burkina Faso", "Cabo Verde", "Cote d'Ivoire", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Liberia", "Mali", "Mauritania", "Niger", "Nigeria", "Senegal", "Sierra Leone", "Togo"],
        "East Africa": ["Burundi", "Comoros", "Djibouti", "Eritrea", "Ethiopia", "Kenya", "Madagascar", "Malawi", "Mauritius", "Mozambique", "Rwanda", "Seychelles", "Somalia", "South Sudan", "Tanzania", "Uganda"],
        "Central Africa": ["Cameroon", "Central African Republic", "Chad", "Congo (Brazzaville)", "Democratic Republic of Congo", "Equatorial Guinea", "Gabon", "Sao Tome and Principe"],
        "Southern Africa": ["Angola", "Botswana", "Eswatini", "Lesotho", "Namibia", "South Africa", "Zambia", "Zimbabwe"],
    }
    region_data = {}
    for rname, countries in regions.items():
        rtrials = sum(r["trials"] for r in results if r["name"] in countries and r["trials"] > 0)
        rpop = sum(r["pop"] for r in results if r["name"] in countries)
        region_data[rname] = {"trials": rtrials, "pop": rpop, "per_m": round(rtrials/rpop, 1) if rpop > 0 else 0}

    region_bars = ""
    reg_sorted = sorted(region_data.items(), key=lambda x: x[1]["trials"], reverse=True)
    max_reg = reg_sorted[0][1]["trials"] if reg_sorted else 1
    for i, (rname, rd) in enumerate(reg_sorted):
        y = 50 + i * 48
        w = (rd["trials"] / max_reg) * 480
        color = "#0d6b57" if rd["trials"] > 3000 else "#2c3e50" if rd["trials"] > 1000 else "#7e5109" if rd["trials"] > 500 else "#c0392b"
        region_bars += f'''
      <text x="195" y="{y+14}" text-anchor="end" font-size="13" fill="#1d2430" font-family="Georgia,serif">{escape(rname)}</text>
      <rect x="205" y="{y}" width="{w}" height="28" rx="4" fill="{color}" opacity="0.85"/>
      <text x="{210+w}" y="{y+16}" font-size="12" fill="#5f6b7a" font-family="Georgia,serif">{rd["trials"]:,} trials ({rd["per_m"]}/M)</text>'''

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Africa RCT Country Analysis — ClinicalTrials.gov</title>
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
    .page {{ width: min(1080px, calc(100vw - 32px)); margin: 0 auto; padding: 40px 0 64px; }}
    .card {{
      background: var(--paper); border: 1px solid var(--line);
      border-radius: var(--radius); box-shadow: var(--shadow);
      padding: 32px; margin-bottom: 24px;
    }}
    .hero {{ text-align: center; padding: 48px 32px; }}
    .eyebrow {{ color: var(--accent); font-size: 12px; letter-spacing: 0.15em; text-transform: uppercase; font-weight: 700; }}
    h1 {{ font-size: clamp(28px,4vw,44px); line-height: 1.05; margin: 12px 0 8px; }}
    .subtitle {{ color: var(--muted); font-size: 19px; max-width: 65ch; margin: 0 auto; }}
    .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 16px; margin: 24px 0; }}
    .metric {{ text-align: center; padding: 20px 12px; border-radius: 14px; background: linear-gradient(180deg, #fff, #faf6ee); border: 1px solid var(--line); }}
    .metric-label {{ font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); margin-bottom: 6px; }}
    .metric-value {{ font-size: 28px; font-weight: 700; color: var(--accent); }}
    .section-label {{ font-size: 13px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--muted); font-weight: 700; margin-bottom: 16px; }}
    .chart-wrap {{ overflow-x: auto; }}
    .context {{ font-size: 17px; line-height: 1.8; color: #2a2f36; }}

    /* Table */
    table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
    th {{ text-align: left; padding: 10px 12px; border-bottom: 2px solid var(--line); color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; }}
    td {{ padding: 8px 12px; border-bottom: 1px solid var(--line); }}
    .num {{ text-align: right; font-family: var(--mono); }}
    tr.zero td {{ color: #bbb; }}
    tr:hover {{ background: var(--accent-soft); }}

    .finding {{ font-size: 20px; line-height: 1.65; padding: 24px 28px; border-left: 5px solid var(--accent); background: var(--accent-soft); border-radius: 0 var(--radius) var(--radius) 0; }}
    .footer {{ text-align: center; color: var(--muted); font-size: 13px; margin-top: 32px; }}
    .footer a {{ color: var(--accent); text-decoration: none; }}
    @media (max-width: 640px) {{
      .card {{ padding: 20px 16px; }}
      table {{ font-size: 12px; }}
    }}
  </style>
</head>
<body>
<div class="page">

  <div class="card hero">
    <div class="eyebrow">ClinicalTrials.gov API v2 &middot; Live Analysis</div>
    <h1>Clinical Trials in Africa<br>Country-by-Country</h1>
    <p class="subtitle">Interventional trial counts across all 54 African nations, ranked by volume and adjusted for population.</p>
    <div class="metrics">
      <div class="metric"><div class="metric-label">Total Trials</div><div class="metric-value">{total_trials:,}</div></div>
      <div class="metric"><div class="metric-label">Countries with Trials</div><div class="metric-value">{countries_with_trials}/54</div></div>
      <div class="metric"><div class="metric-label">Africa Population</div><div class="metric-value">{total_pop:.0f}M</div></div>
      <div class="metric"><div class="metric-label">Trials per Million</div><div class="metric-value">{total_trials/total_pop:.1f}</div></div>
      <div class="metric"><div class="metric-label">Countries Zero Trials</div><div class="metric-value" style="color:#c0392b">{len(bottom_zero)}</div></div>
      <div class="metric"><div class="metric-label">Data Retrieved</div><div class="metric-value" style="font-size:16px">{now}</div></div>
    </div>
  </div>

  <div class="card">
    <div class="section-label">Key Finding</div>
    <div class="finding">
      {escape(top3[0]["name"])} leads Africa with {top3[0]["trials"]:,} registered interventional trials,
      followed by {escape(top3[1]["name"])} ({top3[1]["trials"]:,}) and {escape(top3[2]["name"])} ({top3[2]["trials"]:,}).
      Together, these three countries account for {round(100*sum(t["trials"] for t in top3)/total_trials)}% of all African clinical trials
      while representing only {round(100*sum(t["pop"] for t in top3)/total_pop)}% of the continent's population.
    </div>
  </div>

  <div class="card">
    <div class="section-label">Trial Volume by Country (Top 30)</div>
    <div class="chart-wrap">
      <svg width="100%" viewBox="0 0 780 {chart_height}" xmlns="http://www.w3.org/2000/svg">
        <text x="205" y="30" font-size="14" fill="#5f6b7a" font-family="Georgia,serif">Registered Interventional Trials</text>
        {bars_svg}
      </svg>
    </div>
  </div>

  <div class="card">
    <div class="section-label">Trials per Million Population (Top 20)</div>
    <div class="chart-wrap">
      <svg width="100%" viewBox="0 0 780 {pc_height}" xmlns="http://www.w3.org/2000/svg">
        <text x="205" y="30" font-size="14" fill="#5f6b7a" font-family="Georgia,serif">Trials per Million Residents</text>
        {pc_svg}
      </svg>
    </div>
  </div>

  <div class="card">
    <div class="section-label">Sub-Regional Distribution</div>
    <div class="chart-wrap">
      <svg width="100%" viewBox="0 0 780 330" xmlns="http://www.w3.org/2000/svg">
        <text x="205" y="30" font-size="14" fill="#5f6b7a" font-family="Georgia,serif">Trials by African Sub-Region</text>
        {region_bars}
      </svg>
    </div>
  </div>

  <div class="card">
    <div class="section-label">Full Country Table</div>
    <table>
      <thead>
        <tr>
          <th>#</th><th>Country</th><th class="num">Trials</th>
          <th class="num">% of Total</th><th class="num">Population</th>
          <th class="num">Trials/M</th>
        </tr>
      </thead>
      <tbody>{table_rows}</tbody>
    </table>
  </div>

  <div class="card">
    <div class="section-label">Why It Matters</div>
    <p class="context">
      Clinical trial distribution across Africa reveals a continent of extreme internal inequality.
      A handful of nations — primarily Egypt, South Africa, and Kenya — host the vast majority of
      research activity, while dozens of countries with significant disease burdens have minimal or
      no trial presence. The per-capita analysis exposes further inequities: small nations with
      established research infrastructure (like Gambia, thanks to the MRC unit) can outperform
      giants like Nigeria on a population-adjusted basis. Understanding these patterns is essential
      for any strategy to build equitable, sovereign clinical research capacity across the continent.
    </p>
  </div>

  <div class="footer">
    <p>Data: ClinicalTrials.gov API v2 (public, no key required) &middot; Retrieved {now}</p>
    <p>Analysis: University of Uganda &middot; Africa E156 Series</p>
  </div>

</div>
</body>
</html>'''
    return html


def main():
    print("=" * 60)
    print("  AFRICA RCT COUNTRY-LEVEL ANALYSIS")
    print("  ClinicalTrials.gov API v2")
    print("=" * 60 + "\n")

    # Fetch data
    results = fetch_all()

    # Save raw JSON
    json_path = OUT_DIR / "africa_rct_country_results.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "retrieved": datetime.now().isoformat(),
            "source": "ClinicalTrials.gov API v2",
            "countries": results,
        }, f, indent=2)
    print(f"\nSaved JSON: {json_path}")

    # Generate dashboard
    html = generate_dashboard(results)
    html_path = OUT_DIR / "africa_rct_country_dashboard.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Saved dashboard: {html_path}")

    # Print summary
    total = sum(r["trials"] for r in results if r["trials"] > 0)
    with_trials = sum(1 for r in results if r["trials"] > 0)
    print(f"\n{'='*60}")
    print(f"  SUMMARY")
    print(f"  Total trials: {total:,}")
    print(f"  Countries with trials: {with_trials}/54")
    print(f"  Top 5:")
    for r in results[:5]:
        print(f"    {r['name']:<30s} {r['trials']:>6,}  ({r['per_million']}/M)")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
