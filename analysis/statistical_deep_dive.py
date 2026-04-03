#!/usr/bin/env python3
"""
Statistical Deep Dive: Africa Clinical Trial Distribution
==========================================================
Advanced mathematical analysis of trial distribution across 54 African nations.
Uses data from fetch_africa_rcts_by_country.py (africa_rct_country_results.json).

Methods:
  1. Gini Coefficient & Lorenz Curve (inequality)
  2. Shannon Entropy & Normalised Entropy (diversity)
  3. Herfindahl-Hirschman Index (market concentration)
  4. Pareto / 80-20 Analysis
  5. Zipf's Law / Rank-Size Distribution
  6. Benford's Law (first-digit analysis)
  7. Log-Linear Regression (population → trials)
  8. Coefficient of Variation & descriptive stats
  9. Regional inequality decomposition
 10. Bubble chart: population × trials × per-capita

Outputs:
  statistical_deep_dive.html — rich dashboard with SVG charts

Requirements: Python 3.8+ (no external packages — pure stdlib math)
"""

import json
import math
import os
import sys
import io
from pathlib import Path
from html import escape
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DATA_FILE = Path(__file__).parent / "africa_rct_country_results.json"
OUTPUT_HTML = Path(__file__).parent / "statistical_deep_dive.html"


# ═══════════════════════════════════════════════════════════
#  PURE-PYTHON STATISTICAL FUNCTIONS
# ═══════════════════════════════════════════════════════════

def gini_coefficient(values):
    """Gini coefficient: 0 = perfect equality, 1 = perfect inequality."""
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    if n == 0 or sum(sorted_vals) == 0:
        return 0.0
    cumulative = 0
    weighted_sum = 0
    for i, v in enumerate(sorted_vals):
        cumulative += v
        weighted_sum += (i + 1) * v
    return (2 * weighted_sum) / (n * cumulative) - (n + 1) / n


def lorenz_curve(values):
    """Return (x, y) pairs for Lorenz curve. x = cumulative % of pop, y = cumulative % of value."""
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    total = sum(sorted_vals)
    if total == 0:
        return [(0, 0), (1, 1)]
    points = [(0, 0)]
    cumsum = 0
    for i, v in enumerate(sorted_vals):
        cumsum += v
        points.append(((i + 1) / n, cumsum / total))
    return points


def shannon_entropy(values):
    """Shannon entropy in bits."""
    total = sum(values)
    if total == 0:
        return 0.0
    H = 0
    for v in values:
        if v > 0:
            p = v / total
            H -= p * math.log2(p)
    return H


def max_entropy(n):
    """Maximum possible Shannon entropy for n categories."""
    return math.log2(n) if n > 0 else 0


def hhi(values):
    """Herfindahl-Hirschman Index. Range: 1/n (equal) to 1 (monopoly)."""
    total = sum(values)
    if total == 0:
        return 0.0
    return sum((v / total) ** 2 for v in values)


def coefficient_of_variation(values):
    """CV = std / mean. Higher = more variable."""
    n = len(values)
    if n == 0:
        return 0.0
    mean = sum(values) / n
    if mean == 0:
        return 0.0
    variance = sum((v - mean) ** 2 for v in values) / n
    return math.sqrt(variance) / mean


def descriptive_stats(values):
    """Mean, median, std, min, max, IQR."""
    n = len(values)
    if n == 0:
        return {}
    s = sorted(values)
    mean = sum(s) / n
    median = s[n // 2] if n % 2 == 1 else (s[n // 2 - 1] + s[n // 2]) / 2
    variance = sum((v - mean) ** 2 for v in s) / n
    std = math.sqrt(variance)
    q1 = s[n // 4]
    q3 = s[3 * n // 4]
    return {
        "n": n, "mean": round(mean, 1), "median": median,
        "std": round(std, 1), "min": s[0], "max": s[-1],
        "q1": q1, "q3": q3, "iqr": q3 - q1,
        "cv": round(coefficient_of_variation(values), 2),
    }


def pareto_analysis(values_with_labels):
    """Find how many items account for 80% of total."""
    sorted_items = sorted(values_with_labels, key=lambda x: x[1], reverse=True)
    total = sum(v for _, v in sorted_items)
    if total == 0:
        return 0, 0, []
    cumsum = 0
    count = 0
    for label, val in sorted_items:
        cumsum += val
        count += 1
        if cumsum >= 0.8 * total:
            break
    return count, round(100 * count / len(sorted_items), 1), sorted_items[:count]


def benford_analysis(values):
    """Compare first-digit distribution to Benford's Law expected frequencies."""
    # Benford expected: P(d) = log10(1 + 1/d)
    benford_expected = {d: math.log10(1 + 1 / d) for d in range(1, 10)}
    digit_counts = {d: 0 for d in range(1, 10)}
    valid = 0
    for v in values:
        if v > 0:
            first_digit = int(str(v)[0])
            if 1 <= first_digit <= 9:
                digit_counts[first_digit] += 1
                valid += 1
    if valid == 0:
        return benford_expected, {d: 0 for d in range(1, 10)}, 0.0
    observed = {d: digit_counts[d] / valid for d in range(1, 10)}
    # Mean Absolute Deviation
    mad = sum(abs(observed[d] - benford_expected[d]) for d in range(1, 10)) / 9
    # Chi-squared statistic
    chi2 = sum(valid * (observed[d] - benford_expected[d]) ** 2 / benford_expected[d] for d in range(1, 10))
    return benford_expected, observed, round(mad, 4), round(chi2, 2), valid


def log_regression(x_vals, y_vals):
    """Simple OLS regression on log-transformed data. Returns slope, intercept, R²."""
    pairs = [(math.log(x), math.log(y)) for x, y in zip(x_vals, y_vals) if x > 0 and y > 0]
    n = len(pairs)
    if n < 3:
        return 0, 0, 0, []
    sx = sum(p[0] for p in pairs)
    sy = sum(p[1] for p in pairs)
    sxx = sum(p[0] ** 2 for p in pairs)
    sxy = sum(p[0] * p[1] for p in pairs)
    denom = n * sxx - sx ** 2
    if abs(denom) < 1e-10:
        return 0, 0, 0, []
    slope = (n * sxy - sx * sy) / denom
    intercept = (sy - slope * sx) / n
    # R²
    y_mean = sy / n
    ss_tot = sum((p[1] - y_mean) ** 2 for p in pairs)
    ss_res = sum((p[1] - (slope * p[0] + intercept)) ** 2 for p in pairs)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return round(slope, 3), round(intercept, 3), round(r2, 3), pairs


def zipf_analysis(values):
    """Rank-size analysis. If Zipf's law holds, log(rank) vs log(value) is linear with slope ≈ -1."""
    sorted_vals = sorted(values, reverse=True)
    # Filter zeros
    nonzero = [(i + 1, v) for i, v in enumerate(sorted_vals) if v > 0]
    if len(nonzero) < 3:
        return 0, 0, 0, []
    ranks = [r for r, _ in nonzero]
    vals = [v for _, v in nonzero]
    slope, intercept, r2, pairs = log_regression(ranks, vals)
    return slope, intercept, r2, nonzero


def z_scores(values):
    """Return z-scores for each value."""
    n = len(values)
    if n == 0:
        return []
    mean = sum(values) / n
    std = math.sqrt(sum((v - mean) ** 2 for v in values) / n)
    if std == 0:
        return [0.0] * n
    return [round((v - mean) / std, 2) for v in values]


# ═══════════════════════════════════════════════════════════
#  SVG CHART GENERATORS
# ═══════════════════════════════════════════════════════════

def svg_lorenz(points, gini_val):
    """Generate Lorenz curve SVG."""
    w, h = 400, 400
    margin = 50
    pw = w - 2 * margin
    ph = h - 2 * margin

    def tx(x): return margin + x * pw
    def ty(y): return margin + (1 - y) * ph

    # Equality line
    path_eq = f"M {tx(0)} {ty(0)} L {tx(1)} {ty(1)}"
    # Lorenz curve
    path_data = " ".join(f"{'M' if i == 0 else 'L'} {tx(x):.1f} {ty(y):.1f}" for i, (x, y) in enumerate(points))
    # Fill between equality line and Lorenz curve
    fill_path = path_data + f" L {tx(1):.1f} {ty(1):.1f} L {tx(0):.1f} {ty(0):.1f} Z"

    return f'''<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" style="max-width:420px;">
  <rect x="{margin}" y="{margin}" width="{pw}" height="{ph}" fill="#fafaf7" stroke="#d8cfbf"/>
  <path d="{fill_path}" fill="rgba(192,57,43,0.15)" stroke="none"/>
  <path d="{path_eq}" stroke="#0d6b57" stroke-width="1.5" stroke-dasharray="6 4" fill="none"/>
  <path d="{path_data}" stroke="#c0392b" stroke-width="2.5" fill="none"/>
  <!-- Axes labels -->
  <text x="{w/2}" y="{h-8}" text-anchor="middle" font-size="12" fill="#5f6b7a" font-family="Georgia,serif">Cumulative % of Countries (ranked low→high)</text>
  <text x="14" y="{h/2}" text-anchor="middle" font-size="12" fill="#5f6b7a" font-family="Georgia,serif" transform="rotate(-90,14,{h/2})">Cumulative % of Trials</text>
  <!-- Gini label -->
  <text x="{tx(0.55)}" y="{ty(0.25)}" font-size="18" font-weight="700" fill="#c0392b" font-family="Georgia,serif">Gini = {gini_val:.3f}</text>
  <text x="{tx(0.7)}" y="{ty(0.7)}" font-size="12" fill="#0d6b57" font-family="Georgia,serif">Line of equality</text>
  <!-- Axis ticks -->
  {"".join(f'<line x1="{tx(t)}" x2="{tx(t)}" y1="{ty(0)}" y2="{ty(0)+5}" stroke="#5f6b7a"/><text x="{tx(t)}" y="{ty(0)+18}" text-anchor="middle" font-size="11" fill="#5f6b7a">{int(t*100)}%</text>' for t in [0, 0.25, 0.5, 0.75, 1.0])}
  {"".join(f'<line x1="{tx(0)-5}" x2="{tx(0)}" y1="{ty(t)}" y2="{ty(t)}" stroke="#5f6b7a"/><text x="{tx(0)-8}" y="{ty(t)+4}" text-anchor="end" font-size="11" fill="#5f6b7a">{int(t*100)}%</text>' for t in [0, 0.25, 0.5, 0.75, 1.0])}
</svg>'''


def svg_benford(expected, observed, mad_val, n_vals):
    """Generate Benford's Law comparison bar chart."""
    w, h = 600, 300
    margin_l, margin_b = 50, 60
    bar_w = 50
    gap = 8

    bars = ""
    for d in range(1, 10):
        x = margin_l + (d - 1) * (bar_w + gap)
        # Expected bar
        eh = expected[d] * 600
        bars += f'<rect x="{x}" y="{h - margin_b - eh}" width="{bar_w/2-2}" height="{eh}" fill="#0d6b57" opacity="0.6" rx="2"/>'
        # Observed bar
        oh = observed[d] * 600
        bars += f'<rect x="{x + bar_w/2}" y="{h - margin_b - oh}" width="{bar_w/2-2}" height="{oh}" fill="#c0392b" opacity="0.7" rx="2"/>'
        # Label
        bars += f'<text x="{x + bar_w/2}" y="{h - margin_b + 16}" text-anchor="middle" font-size="13" fill="#1d2430">{d}</text>'
        # Expected %
        bars += f'<text x="{x + bar_w/4}" y="{h - margin_b - eh - 4}" text-anchor="middle" font-size="9" fill="#0d6b57">{expected[d]*100:.1f}%</text>'
        # Observed %
        bars += f'<text x="{x + 3*bar_w/4}" y="{h - margin_b - oh - 4}" text-anchor="middle" font-size="9" fill="#c0392b">{observed[d]*100:.1f}%</text>'

    return f'''<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" style="max-width:620px;">
  <text x="{w/2}" y="20" text-anchor="middle" font-size="14" fill="#5f6b7a" font-family="Georgia,serif">First-Digit Distribution: Expected (green) vs Observed (red)</text>
  <text x="{w/2}" y="38" text-anchor="middle" font-size="12" fill="#5f6b7a" font-family="Georgia,serif">MAD = {mad_val:.4f} | n = {n_vals} countries</text>
  {bars}
  <text x="{w/2}" y="{h-8}" text-anchor="middle" font-size="12" fill="#5f6b7a" font-family="Georgia,serif">First Digit</text>
</svg>'''


def svg_zipf(data_points, slope, r2):
    """Generate Zipf's law log-log scatter plot."""
    w, h = 500, 350
    margin = 55
    pw = w - 2 * margin
    ph = h - 2 * margin

    if not data_points:
        return '<svg viewBox="0 0 500 350"><text x="250" y="175">No data</text></svg>'

    max_rank = max(r for r, _ in data_points)
    max_val = max(v for _, v in data_points)
    log_max_r = math.log(max_rank)
    log_max_v = math.log(max_val)

    def tx(log_r): return margin + (log_r / log_max_r) * pw if log_max_r > 0 else margin
    def ty(log_v): return margin + (1 - log_v / log_max_v) * ph if log_max_v > 0 else margin

    dots = ""
    for rank, val in data_points:
        if val > 0:
            x = tx(math.log(rank))
            y = ty(math.log(val))
            dots += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#c0392b" opacity="0.7"/>'

    # Regression line
    x1 = tx(0)
    y1 = ty(slope * 0 + math.log(max_val))  # at log(rank)=0
    # Clamp properly
    lr1 = math.log(1)
    lr2 = math.log(max_rank)
    lv1 = slope * lr1 + math.log(max_val)  # approximate intercept
    lv2 = slope * lr2 + math.log(max_val)

    return f'''<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" style="max-width:520px;">
  <rect x="{margin}" y="{margin}" width="{pw}" height="{ph}" fill="#fafaf7" stroke="#d8cfbf"/>
  {dots}
  <text x="{w/2}" y="20" text-anchor="middle" font-size="14" fill="#5f6b7a" font-family="Georgia,serif">Rank-Size Distribution (log-log)</text>
  <text x="{w/2}" y="38" text-anchor="middle" font-size="12" fill="#5f6b7a" font-family="Georgia,serif">Zipf slope = {slope:.2f} | R² = {r2:.3f}</text>
  <text x="{w/2}" y="{h-8}" text-anchor="middle" font-size="12" fill="#5f6b7a" font-family="Georgia,serif">log(Rank)</text>
  <text x="14" y="{h/2}" text-anchor="middle" font-size="12" fill="#5f6b7a" font-family="Georgia,serif" transform="rotate(-90,14,{h/2})">log(Trials)</text>
</svg>'''


def svg_regression(pairs, slope, intercept, r2, labels):
    """Generate pop vs trials log-log scatter with regression line."""
    w, h = 500, 380
    margin = 55
    pw = w - 2 * margin
    ph = h - 2 * margin

    if not pairs:
        return '<svg viewBox="0 0 500 380"><text x="250" y="190">No data</text></svg>'

    all_x = [p[0] for p in pairs]
    all_y = [p[1] for p in pairs]
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)
    rx = max_x - min_x if max_x != min_x else 1
    ry = max_y - min_y if max_y != min_y else 1

    def tx(lx): return margin + ((lx - min_x) / rx) * pw
    def ty(ly): return margin + (1 - (ly - min_y) / ry) * ph

    dots = ""
    for i, (lx, ly) in enumerate(pairs):
        x = tx(lx)
        y = ty(ly)
        label = labels[i] if i < len(labels) else ""
        color = "#c0392b" if ly < slope * lx + intercept - 0.5 else "#0d6b57" if ly > slope * lx + intercept + 0.5 else "#2c3e50"
        dots += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{color}" opacity="0.7"/>'
        # Label outliers
        residual = ly - (slope * lx + intercept)
        if abs(residual) > 1.0 or label in ["Egypt", "Nigeria", "Rwanda", "South Africa", "Uganda"]:
            dots += f'<text x="{x+7:.1f}" y="{y-5:.1f}" font-size="10" fill="{color}" font-family="Georgia,serif">{escape(label)}</text>'

    # Regression line
    rl_x1 = tx(min_x)
    rl_y1 = ty(slope * min_x + intercept)
    rl_x2 = tx(max_x)
    rl_y2 = ty(slope * max_x + intercept)
    line = f'<line x1="{rl_x1:.1f}" y1="{rl_y1:.1f}" x2="{rl_x2:.1f}" y2="{rl_y2:.1f}" stroke="#7A5A10" stroke-width="2" stroke-dasharray="6 4"/>'

    return f'''<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" style="max-width:520px;">
  <rect x="{margin}" y="{margin}" width="{pw}" height="{ph}" fill="#fafaf7" stroke="#d8cfbf"/>
  {line}
  {dots}
  <text x="{w/2}" y="20" text-anchor="middle" font-size="14" fill="#5f6b7a" font-family="Georgia,serif">Population vs Trials (log-log)</text>
  <text x="{w/2}" y="38" text-anchor="middle" font-size="12" fill="#5f6b7a" font-family="Georgia,serif">slope = {slope:.2f} | R² = {r2:.3f}</text>
  <text x="{w/2}" y="{h-8}" text-anchor="middle" font-size="12" fill="#5f6b7a" font-family="Georgia,serif">log(Population in millions)</text>
  <text x="14" y="{h/2}" text-anchor="middle" font-size="12" fill="#5f6b7a" font-family="Georgia,serif" transform="rotate(-90,14,{h/2})">log(Trial count)</text>
  <text x="{w-margin}" y="{margin+16}" text-anchor="end" font-size="11" fill="#0d6b57">Green = overperforms</text>
  <text x="{w-margin}" y="{margin+30}" text-anchor="end" font-size="11" fill="#c0392b">Red = underperforms</text>
</svg>'''


# ═══════════════════════════════════════════════════════════
#  MAIN ANALYSIS
# ═══════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  STATISTICAL DEEP DIVE: AFRICA RCT DISTRIBUTION")
    print("=" * 60)

    # Load data
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)
    countries = raw["countries"]

    trial_counts = [c["trials"] for c in countries]
    nonzero_counts = [c["trials"] for c in countries if c["trials"] > 0]
    populations = [c["pop"] for c in countries]
    per_million = [c["per_million"] for c in countries]
    names = [c["name"] for c in countries]
    total_trials = sum(trial_counts)

    # ── 1. Descriptive Statistics ──
    print("\n1. DESCRIPTIVE STATISTICS")
    stats = descriptive_stats(trial_counts)
    print(f"   n={stats['n']}, mean={stats['mean']}, median={stats['median']}, "
          f"std={stats['std']}, min={stats['min']}, max={stats['max']}")
    print(f"   Q1={stats['q1']}, Q3={stats['q3']}, IQR={stats['iqr']}, CV={stats['cv']}")

    # ── 2. Gini Coefficient & Lorenz Curve ──
    print("\n2. INEQUALITY (GINI)")
    gini = gini_coefficient(trial_counts)
    lorenz = lorenz_curve(trial_counts)
    print(f"   Gini coefficient = {gini:.4f}")
    print(f"   (0 = equal, 1 = one country has all trials)")
    print(f"   Interpretation: {'Extreme' if gini > 0.7 else 'High' if gini > 0.5 else 'Moderate'} inequality")

    # ── 3. Shannon Entropy ──
    print("\n3. DIVERSITY (SHANNON ENTROPY)")
    H = shannon_entropy(trial_counts)
    H_max = max_entropy(len(trial_counts))
    H_norm = H / H_max if H_max > 0 else 0
    print(f"   Shannon entropy = {H:.3f} bits")
    print(f"   Maximum possible = {H_max:.3f} bits")
    print(f"   Normalised entropy = {H_norm:.3f} (1.0 = perfectly even)")

    # ── 4. HHI ──
    print("\n4. CONCENTRATION (HHI)")
    hhi_val = hhi(trial_counts)
    hhi_equiv = round(1 / hhi_val, 1) if hhi_val > 0 else 0
    print(f"   HHI = {hhi_val:.4f}")
    print(f"   Equivalent number of equal-sized countries = {hhi_equiv}")
    print(f"   ({54} actual countries behave like {hhi_equiv} equal ones)")

    # ── 5. Pareto Analysis ──
    print("\n5. PARETO (80/20) ANALYSIS")
    labeled = [(c["name"], c["trials"]) for c in countries]
    p_count, p_pct, p_items = pareto_analysis(labeled)
    print(f"   {p_count} countries ({p_pct}%) account for 80% of all trials:")
    for name, val in p_items:
        print(f"     {name}: {val:,} ({100*val/total_trials:.1f}%)")

    # ── 6. Zipf's Law ──
    print("\n6. ZIPF'S LAW (RANK-SIZE)")
    z_slope, z_int, z_r2, z_data = zipf_analysis(trial_counts)
    print(f"   Zipf slope = {z_slope:.3f} (ideal = -1.0)")
    print(f"   R² = {z_r2:.3f}")
    print(f"   {'Good' if z_r2 > 0.9 else 'Moderate' if z_r2 > 0.7 else 'Poor'} fit to Zipf's law")

    # ── 7. Benford's Law ──
    print("\n7. BENFORD'S LAW (FIRST-DIGIT)")
    b_exp, b_obs, b_mad, b_chi2, b_n = benford_analysis(nonzero_counts)
    print(f"   MAD = {b_mad} (< 0.015 = close conformity)")
    print(f"   Chi² = {b_chi2} (df=8, critical 15.51 at 5%)")
    print(f"   {'CONFORMS' if b_chi2 < 15.51 else 'DEVIATES'} to Benford at 5% level")

    # ── 8. Log-linear Regression ──
    print("\n8. REGRESSION: POPULATION → TRIALS")
    reg_pop = [c["pop"] for c in countries if c["trials"] > 0]
    reg_tri = [c["trials"] for c in countries if c["trials"] > 0]
    reg_names = [c["name"] for c in countries if c["trials"] > 0]
    r_slope, r_int, r_r2, r_pairs = log_regression(reg_pop, reg_tri)
    print(f"   log(trials) = {r_slope} * log(pop) + {r_int}")
    print(f"   R² = {r_r2}")
    print(f"   Slope {'> 1 (super-linear: big countries have more per-capita)' if r_slope > 1 else '< 1 (sub-linear: big countries have less per-capita)' if r_slope < 1 else '= 1 (proportional)'}")

    # Residuals (over/underperformers)
    residuals = []
    for i, (lx, ly) in enumerate(r_pairs):
        predicted = r_slope * lx + r_int
        residual = ly - predicted
        residuals.append((reg_names[i], round(residual, 2), reg_tri[i], reg_pop[i]))
    residuals.sort(key=lambda x: x[1], reverse=True)
    print("\n   Top overperformers (positive residual):")
    for name, res, tri, pop in residuals[:5]:
        print(f"     {name}: residual={res:+.2f} ({tri} trials, {pop}M pop)")
    print("   Top underperformers (negative residual):")
    for name, res, tri, pop in residuals[-5:]:
        print(f"     {name}: residual={res:+.2f} ({tri} trials, {pop}M pop)")

    # ── 9. Regional Decomposition ──
    print("\n9. REGIONAL INEQUALITY DECOMPOSITION")
    regions = {
        "North": ["Algeria", "Egypt", "Libya", "Morocco", "Tunisia", "Sudan"],
        "West": ["Benin", "Burkina Faso", "Cabo Verde", "Cote d'Ivoire", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Liberia", "Mali", "Mauritania", "Niger", "Nigeria", "Senegal", "Sierra Leone", "Togo"],
        "East": ["Burundi", "Comoros", "Djibouti", "Eritrea", "Ethiopia", "Kenya", "Madagascar", "Malawi", "Mauritius", "Mozambique", "Rwanda", "Seychelles", "Somalia", "South Sudan", "Tanzania", "Uganda"],
        "Central": ["Cameroon", "Central African Republic", "Chad", "Congo (Brazzaville)", "Democratic Republic of Congo", "Equatorial Guinea", "Gabon", "Sao Tome and Principe"],
        "Southern": ["Angola", "Botswana", "Eswatini", "Lesotho", "Namibia", "South Africa", "Zambia", "Zimbabwe"],
    }
    for rname, rcountries in regions.items():
        r_trials = [c["trials"] for c in countries if c["name"] in rcountries]
        r_gini = gini_coefficient(r_trials)
        r_total = sum(r_trials)
        r_pct = round(100 * r_total / total_trials, 1)
        print(f"   {rname:10s}: {r_total:>6,} trials ({r_pct:>5.1f}%), internal Gini = {r_gini:.3f}")

    # ── 10. Z-scores ──
    print("\n10. Z-SCORES (OUTLIER DETECTION)")
    z = z_scores(trial_counts)
    outliers = [(names[i], trial_counts[i], z[i]) for i in range(len(z)) if abs(z[i]) > 2]
    for name, trials, zscore in sorted(outliers, key=lambda x: x[2], reverse=True):
        print(f"   {name}: {trials:,} trials, z = {zscore:+.2f} {'(extreme outlier)' if abs(zscore) > 3 else '(outlier)'}")

    # ═══ Generate Dashboard ═══
    print("\nGenerating dashboard...")

    lorenz_svg = svg_lorenz(lorenz, gini)
    benford_svg = svg_benford(b_exp, b_obs, b_mad, b_n)
    zipf_svg = svg_zipf(z_data, z_slope, z_r2)
    regression_svg = svg_regression(r_pairs, r_slope, r_int, r_r2, reg_names)

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Residuals table
    res_rows = ""
    for name, res, tri, pop in residuals:
        color = "#0d6b57" if res > 0.5 else "#c0392b" if res < -0.5 else "#2c3e50"
        res_rows += f'<tr><td>{escape(name)}</td><td class="num">{tri:,}</td><td class="num">{pop}M</td><td class="num" style="color:{color}">{res:+.2f}</td></tr>'

    # Regional table
    reg_rows = ""
    for rname, rcountries in regions.items():
        r_trials_list = [c["trials"] for c in countries if c["name"] in rcountries]
        r_gini_val = gini_coefficient(r_trials_list)
        r_total = sum(r_trials_list)
        r_pop = sum(c["pop"] for c in countries if c["name"] in rcountries)
        r_pm = round(r_total / r_pop, 1) if r_pop > 0 else 0
        reg_rows += f'<tr><td>{rname}</td><td class="num">{r_total:,}</td><td class="num">{r_pop:.0f}M</td><td class="num">{r_pm}</td><td class="num">{r_gini_val:.3f}</td></tr>'

    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Statistical Deep Dive — Africa RCT Distribution</title>
  <style>
    :root {{ --bg:#f5f2ea;--paper:#fffdf8;--ink:#1d2430;--muted:#5f6b7a;--line:#d8cfbf;--accent:#0d6b57;--accent-soft:#dcefe8;--warm:#7A5A10;--shadow:0 18px 40px rgba(42,47,54,0.08);--radius:18px;--serif:"Georgia","Times New Roman",serif;--mono:"Consolas","SFMono-Regular","Menlo",monospace; }}
    * {{ box-sizing:border-box;margin:0; }}
    body {{ color:var(--ink);font-family:var(--serif);line-height:1.6;background:radial-gradient(circle at top left,rgba(13,107,87,0.06),transparent 32%),radial-gradient(circle at bottom right,rgba(141,79,45,0.06),transparent 28%),var(--bg); }}
    .page {{ width:min(1080px,calc(100vw - 32px));margin:0 auto;padding:40px 0 64px; }}
    .card {{ background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:32px;margin-bottom:24px; }}
    .hero {{ text-align:center;padding:48px 32px; }}
    .eyebrow {{ color:var(--accent);font-size:12px;letter-spacing:0.15em;text-transform:uppercase;font-weight:700; }}
    h1 {{ font-size:clamp(28px,4vw,44px);line-height:1.05;margin:12px 0 8px; }}
    h2 {{ font-size:22px;margin:0 0 16px;color:var(--warm); }}
    .subtitle {{ color:var(--muted);font-size:19px;max-width:65ch;margin:0 auto; }}
    .metrics {{ display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:16px;margin:24px 0; }}
    .metric {{ text-align:center;padding:20px 12px;border-radius:14px;background:linear-gradient(180deg,#fff,#faf6ee);border:1px solid var(--line); }}
    .metric-label {{ font-size:11px;text-transform:uppercase;letter-spacing:0.08em;color:var(--muted);margin-bottom:6px; }}
    .metric-value {{ font-size:28px;font-weight:700;color:var(--accent); }}
    .section-label {{ font-size:13px;text-transform:uppercase;letter-spacing:0.1em;color:var(--muted);font-weight:700;margin-bottom:16px; }}
    .chart-wrap {{ display:flex;justify-content:center;overflow-x:auto;padding:8px 0; }}
    .two-col {{ display:grid;grid-template-columns:1fr 1fr;gap:24px; }}
    .context {{ font-size:16px;line-height:1.8;color:#2a2f36;margin-top:16px; }}
    .formula {{ font-family:var(--mono);font-size:14px;background:#f4f1ea;padding:12px 16px;border-radius:8px;margin:12px 0;overflow-x:auto; }}
    table {{ width:100%;border-collapse:collapse;font-size:14px; }}
    th {{ text-align:left;padding:10px 12px;border-bottom:2px solid var(--line);color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:0.05em; }}
    td {{ padding:8px 12px;border-bottom:1px solid var(--line); }}
    .num {{ text-align:right;font-family:var(--mono); }}
    tr:hover {{ background:var(--accent-soft); }}
    .finding {{ font-size:20px;line-height:1.65;padding:24px 28px;border-left:5px solid var(--accent);background:var(--accent-soft);border-radius:0 var(--radius) var(--radius) 0;margin:16px 0; }}
    .footer {{ text-align:center;color:var(--muted);font-size:13px;margin-top:32px; }}
    .footer a {{ color:var(--accent);text-decoration:none; }}
    @media (max-width:768px) {{ .two-col {{ grid-template-columns:1fr; }} }}
  </style>
</head>
<body>
<div class="page">

  <div class="card hero">
    <div class="eyebrow">Mathematical Analysis &middot; ClinicalTrials.gov</div>
    <h1>Statistical Deep Dive<br>Africa RCT Distribution</h1>
    <p class="subtitle">Ten mathematical lenses applied to the distribution of {total_trials:,} clinical trials across 54 African nations.</p>
    <div class="metrics">
      <div class="metric"><div class="metric-label">Gini Coefficient</div><div class="metric-value" style="color:#c0392b">{gini:.3f}</div></div>
      <div class="metric"><div class="metric-label">Shannon Entropy</div><div class="metric-value">{H:.2f} bits</div></div>
      <div class="metric"><div class="metric-label">Normalised Entropy</div><div class="metric-value">{H_norm:.3f}</div></div>
      <div class="metric"><div class="metric-label">HHI</div><div class="metric-value">{hhi_val:.4f}</div></div>
      <div class="metric"><div class="metric-label">Zipf Slope</div><div class="metric-value">{z_slope:.2f}</div></div>
      <div class="metric"><div class="metric-label">Benford MAD</div><div class="metric-value">{b_mad}</div></div>
      <div class="metric"><div class="metric-label">Pop→Trial R²</div><div class="metric-value">{r_r2}</div></div>
      <div class="metric"><div class="metric-label">Pareto Countries</div><div class="metric-value">{p_count}/{len(countries)}</div></div>
    </div>
  </div>

  <div class="card">
    <div class="finding">
      Africa's clinical trial distribution has a Gini coefficient of {gini:.3f} — comparable to the world's most
      unequal income distributions. Just {p_count} countries ({p_pct}% of the continent) account for 80% of all trials.
      Egypt alone hosts {round(100*countries[0]["trials"]/total_trials)}% of the total.
    </div>
  </div>

  <div class="card">
    <h2>1. Inequality: Gini Coefficient & Lorenz Curve</h2>
    <div class="formula">Gini = (2 &middot; &Sigma;(i &middot; x_i)) / (n &middot; &Sigma;x_i) &minus; (n+1)/n = {gini:.4f}</div>
    <div class="two-col">
      <div>
        <p class="context">
          The <strong>Gini coefficient</strong> measures inequality on a 0–1 scale. A value of {gini:.3f} indicates
          <strong>{'extreme' if gini > 0.7 else 'high' if gini > 0.5 else 'moderate'} inequality</strong> in trial distribution.
          For comparison, South Africa's income Gini is ~0.63 — Africa's trial Gini is {'even higher' if gini > 0.63 else 'comparable'}.
        </p>
        <p class="context" style="margin-top:12px;">
          The <strong>Lorenz curve</strong> shows the cumulative share of trials held by each percentile of countries.
          The red area between the curve and the equality line is proportional to the Gini coefficient.
        </p>
      </div>
      <div class="chart-wrap">{lorenz_svg}</div>
    </div>
  </div>

  <div class="card">
    <h2>2. Diversity: Shannon Entropy</h2>
    <div class="formula">H = &minus;&Sigma; p_i &middot; log₂(p_i) = {H:.3f} bits &nbsp; | &nbsp; H_max = log₂({len(trial_counts)}) = {H_max:.3f} bits &nbsp; | &nbsp; H/H_max = {H_norm:.3f}</div>
    <p class="context">
      Shannon entropy measures the <strong>diversity</strong> of trial distribution. With a normalised entropy of {H_norm:.3f},
      the distribution uses only {H_norm*100:.0f}% of its maximum possible diversity.
      If trials were spread equally across all {len(trial_counts)} countries, entropy would be {H_max:.2f} bits.
      The actual value of {H:.2f} bits reflects heavy concentration in a few nations.
    </p>
  </div>

  <div class="card">
    <h2>3. Market Concentration: Herfindahl-Hirschman Index</h2>
    <div class="formula">HHI = &Sigma;(s_i)² = {hhi_val:.4f} &nbsp; | &nbsp; Equivalent firms = 1/HHI = {hhi_equiv}</div>
    <p class="context">
      The HHI, borrowed from antitrust economics, treats each country as a "market participant."
      An HHI of {hhi_val:.4f} means the 54 African countries behave, in terms of concentration,
      like <strong>only {hhi_equiv} equal-sized countries</strong>. In antitrust terms,
      {'this would indicate a highly concentrated market' if hhi_val > 0.25 else 'this indicates moderate concentration'}.
      The US DOJ considers HHI > 0.25 as "highly concentrated."
    </p>
  </div>

  <div class="card">
    <h2>4. Pareto Analysis (80/20 Rule)</h2>
    <p class="context">
      <strong>{p_count} countries ({p_pct}%)</strong> account for 80% of all {total_trials:,} African clinical trials:
    </p>
    <table style="margin-top:12px;">
      <thead><tr><th>Country</th><th class="num">Trials</th><th class="num">% of Total</th><th class="num">Cumulative %</th></tr></thead>
      <tbody>'''

    cum = 0
    for name, val in p_items:
        cum += val
        html += f'<tr><td>{escape(name)}</td><td class="num">{val:,}</td><td class="num">{100*val/total_trials:.1f}%</td><td class="num">{100*cum/total_trials:.1f}%</td></tr>'

    html += f'''</tbody></table>
  </div>

  <div class="card">
    <h2>5. Zipf's Law (Rank-Size Distribution)</h2>
    <div class="formula">log(trials) = {z_slope:.3f} &middot; log(rank) + C &nbsp; | &nbsp; R² = {z_r2:.3f} &nbsp; | &nbsp; Ideal Zipf slope = &minus;1.0</div>
    <div class="two-col">
      <div>
        <p class="context">
          <strong>Zipf's law</strong> predicts that the second-largest city is half the size of the largest, the third is a third, etc.
          Applied to trial counts, a slope of {z_slope:.2f} {'is close to' if abs(z_slope + 1) < 0.3 else 'deviates from'} the ideal &minus;1.0.
          {'The distribution is more top-heavy than Zipf predicts — Egypt dominates even more than expected.' if z_slope < -1.3 else 'The distribution follows Zipf reasonably well.' if abs(z_slope + 1) < 0.3 else 'The distribution is flatter than Zipf predicts.'}
          R² = {z_r2:.3f} indicates {'excellent' if z_r2 > 0.9 else 'good' if z_r2 > 0.8 else 'moderate' if z_r2 > 0.7 else 'poor'} fit.
        </p>
      </div>
      <div class="chart-wrap">{zipf_svg}</div>
    </div>
  </div>

  <div class="card">
    <h2>6. Benford's Law (First-Digit Test)</h2>
    <div class="formula">MAD = {b_mad} &nbsp; | &nbsp; &chi;² = {b_chi2} (df=8, critical=15.51 at &alpha;=0.05) &nbsp; → &nbsp; {'CONFORMS' if b_chi2 < 15.51 else 'DEVIATES'}</div>
    <div class="two-col">
      <div>
        <p class="context">
          <strong>Benford's Law</strong> predicts that in naturally occurring datasets, the digit 1 appears as the first digit ~30% of the time,
          digit 2 ~17.6%, and so on. {'The trial counts conform to Benford at the 5% significance level, suggesting natural (non-fabricated) data.' if b_chi2 < 15.51 else 'The trial counts deviate from Benford, which may reflect structural patterns rather than fabrication.'}
          MAD of {b_mad} is {'well within' if b_mad < 0.015 else 'close to' if b_mad < 0.025 else 'outside'} the close-conformity threshold of 0.015.
        </p>
      </div>
      <div class="chart-wrap">{benford_svg}</div>
    </div>
  </div>

  <div class="card">
    <h2>7. Log-Linear Regression: Population → Trials</h2>
    <div class="formula">log(trials) = {r_slope} &times; log(population) + {r_int} &nbsp; | &nbsp; R² = {r_r2}</div>
    <div class="two-col">
      <div>
        <p class="context">
          A <strong>log-log regression</strong> tests whether trial counts scale proportionally with population.
          A slope of {r_slope:.2f} means that doubling a country's population is associated with a
          {2**r_slope:.1f}-fold increase in trials.
          {'Population is a strong predictor of trial activity.' if r_r2 > 0.6 else 'Population alone poorly predicts trial activity — other factors dominate.'}
        </p>
        <p class="context" style="margin-top:12px;">
          <strong>Green dots</strong> are overperformers (more trials than population predicts).
          <strong>Red dots</strong> are underperformers. Countries above the regression line have stronger
          research infrastructure relative to their size.
        </p>
      </div>
      <div class="chart-wrap">{regression_svg}</div>
    </div>
  </div>

  <div class="card">
    <h2>8. Regression Residuals (Over/Underperformers)</h2>
    <table>
      <thead><tr><th>Country</th><th class="num">Trials</th><th class="num">Population</th><th class="num">Residual</th></tr></thead>
      <tbody>{res_rows}</tbody>
    </table>
    <p class="context" style="margin-top:12px;">
      Positive residuals indicate countries with more trials than their population would predict.
      Negative residuals indicate underperformance. The residual captures the effect of governance,
      infrastructure, language, colonial history, and funding beyond what population alone explains.
    </p>
  </div>

  <div class="card">
    <h2>9. Regional Inequality Decomposition</h2>
    <table>
      <thead><tr><th>Region</th><th class="num">Trials</th><th class="num">Population</th><th class="num">Trials/M</th><th class="num">Internal Gini</th></tr></thead>
      <tbody>{reg_rows}</tbody>
    </table>
    <p class="context" style="margin-top:12px;">
      Internal Gini measures inequality <em>within</em> each sub-region. High internal Gini means
      one country dominates the region (e.g., Egypt in North, South Africa in Southern).
      Low internal Gini means trials are more evenly distributed across the region's countries.
    </p>
  </div>

  <div class="card">
    <h2>10. Descriptive Statistics Summary</h2>
    <div class="metrics">
      <div class="metric"><div class="metric-label">Mean</div><div class="metric-value">{stats["mean"]}</div></div>
      <div class="metric"><div class="metric-label">Median</div><div class="metric-value">{stats["median"]}</div></div>
      <div class="metric"><div class="metric-label">Std Dev</div><div class="metric-value">{stats["std"]}</div></div>
      <div class="metric"><div class="metric-label">CV</div><div class="metric-value">{stats["cv"]}</div></div>
      <div class="metric"><div class="metric-label">IQR</div><div class="metric-value">{stats["iqr"]}</div></div>
      <div class="metric"><div class="metric-label">Min / Max</div><div class="metric-value">{stats["min"]} / {stats["max"]:,}</div></div>
    </div>
    <div class="formula">CV = &sigma;/&mu; = {stats["std"]}/{stats["mean"]} = {stats["cv"]} &nbsp; | &nbsp; IQR = Q3 &minus; Q1 = {stats["q3"]} &minus; {stats["q1"]} = {stats["iqr"]}</div>
    <p class="context">
      A coefficient of variation of {stats["cv"]} (mean = {stats["mean"]}, std = {stats["std"]}) indicates
      {'extreme' if stats["cv"] > 3 else 'very high' if stats["cv"] > 2 else 'high' if stats["cv"] > 1 else 'moderate'} variability.
      The median ({stats["median"]}) is {'far below' if stats["median"] < stats["mean"]/3 else 'below'} the mean ({stats["mean"]}),
      confirming a heavily right-skewed distribution dominated by a few large values.
    </p>
  </div>

  <div class="card">
    <h2>Methods Summary</h2>
    <table>
      <thead><tr><th>Method</th><th>Origin</th><th>What It Measures</th><th>Result</th></tr></thead>
      <tbody>
        <tr><td>Gini Coefficient</td><td>Economics (Corrado Gini, 1912)</td><td>Inequality of distribution</td><td>{gini:.3f}</td></tr>
        <tr><td>Shannon Entropy</td><td>Information Theory (Claude Shannon, 1948)</td><td>Diversity / evenness</td><td>{H:.2f} bits ({H_norm:.1%} of max)</td></tr>
        <tr><td>HHI</td><td>Antitrust Economics</td><td>Market concentration</td><td>{hhi_val:.4f} (equiv. {hhi_equiv} countries)</td></tr>
        <tr><td>Pareto Analysis</td><td>Management Science (Vilfredo Pareto)</td><td>80/20 concentration</td><td>{p_count} countries = 80% of trials</td></tr>
        <tr><td>Zipf's Law</td><td>Linguistics / Complex Systems (George Zipf)</td><td>Rank-size regularity</td><td>slope = {z_slope:.2f}, R² = {z_r2:.3f}</td></tr>
        <tr><td>Benford's Law</td><td>Number Theory (Frank Benford, 1938)</td><td>First-digit naturalness</td><td>MAD = {b_mad}, &chi;² = {b_chi2}</td></tr>
        <tr><td>Log-Linear Regression</td><td>Statistics (OLS)</td><td>Population → Trial scaling</td><td>&beta; = {r_slope}, R² = {r_r2}</td></tr>
        <tr><td>Coefficient of Variation</td><td>Descriptive Statistics</td><td>Relative variability</td><td>CV = {stats["cv"]}</td></tr>
        <tr><td>Regional Gini</td><td>Decomposition Analysis</td><td>Within-region inequality</td><td>5 sub-regions</td></tr>
        <tr><td>Z-Score Outliers</td><td>Standardisation</td><td>Extreme values</td><td>{len(outliers)} outlier(s)</td></tr>
      </tbody>
    </table>
  </div>

  <div class="footer">
    <p>Data: ClinicalTrials.gov API v2 &middot; Retrieved {raw["retrieved"][:10]} &middot; Analysis: {now}</p>
    <p>Pure Python (no external packages) &middot; University of Uganda &middot; Africa E156 Series</p>
  </div>

</div>
</body>
</html>'''

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\nDashboard saved: {OUTPUT_HTML}")

    # Save stats JSON
    stats_json = {
        "gini": gini, "shannon_entropy": H, "normalised_entropy": round(H_norm, 4),
        "hhi": round(hhi_val, 4), "hhi_equivalent": hhi_equiv,
        "pareto_count": p_count, "pareto_pct": p_pct,
        "zipf_slope": z_slope, "zipf_r2": z_r2,
        "benford_mad": b_mad, "benford_chi2": b_chi2, "benford_conforms": b_chi2 < 15.51,
        "regression_slope": r_slope, "regression_r2": r_r2,
        "descriptive": stats,
        "residuals": [{"country": r[0], "residual": r[1], "trials": r[2], "pop": r[3]} for r in residuals],
    }
    stats_path = Path(__file__).parent / "statistical_deep_dive_results.json"
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats_json, f, indent=2)
    print(f"Stats JSON saved: {stats_path}")
    print("\nDone.")


if __name__ == "__main__":
    main()
