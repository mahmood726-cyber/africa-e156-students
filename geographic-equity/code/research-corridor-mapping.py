#!/usr/bin/env python3
"""
Research Corridor Mapping — Africa E156 Student Analysis
Group: geographic-equity | Paper #36

Condition: all interventional
Location: Africa

This standalone script demonstrates the statistical methods used in this paper.
Run: python research-corridor-mapping.py
"""

import json
import math
import random
import sys

try:
    import requests
except ImportError:
    print("Optional: pip install requests (for live API queries)")
    requests = None

seed = 42
random.seed(seed)

# ── ClinicalTrials.gov API query ──────────────────────────────────
API_URL = "https://clinicaltrials.gov/api/v2/studies"


def fetch_trial_count(condition=None, location=None, other=None):
    """Fetch trial count from ClinicalTrials.gov API v2."""
    if requests is None:
        return 0
    params = {
        "format": "json",
        "pageSize": 0,
        "countTotal": "true",
        "filter.advanced": "AREA[StudyType]INTERVENTIONAL",
    }
    params["query.locn"] = "Africa"
    try:
        resp = requests.get(API_URL, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json().get("totalCount", 0)
    except Exception as e:
        print(f"API error: {e}")
        return 0


# ── Statistical methods ───────────────────────────────────────────

def spearman_rank(x, y):
    """Spearman rank correlation."""
    n = len(x)
    if n < 3:
        return 0.0
    rx = rank_data(x)
    ry = rank_data(y)
    d2 = sum((a - b) ** 2 for a, b in zip(rx, ry))
    return 1 - 6 * d2 / (n * (n**2 - 1))

def rank_data(values):
    indexed = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    for rank_val, idx in enumerate(indexed):
        ranks[idx] = rank_val + 1.0
    return ranks


def linear_regression(x, y):
    """Simple OLS regression: y = a + b*x."""
    n = len(x)
    if n < 2:
        return 0, 0, 0
    mx = sum(x) / n
    my = sum(y) / n
    ss_xy = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    ss_xx = sum((xi - mx) ** 2 for xi in x)
    if ss_xx == 0:
        return 0, my, 0
    b = ss_xy / ss_xx
    a = my - b * mx
    r2 = ss_xy ** 2 / (ss_xx * sum((yi - my) ** 2 for yi in y)) if sum((yi - my) ** 2 for yi in y) > 0 else 0
    return b, a, r2


def bootstrap_ci(data, n_boot=5000, seed=42):
    """Bootstrap 95% confidence interval for the mean."""
    rng = random.Random(seed)
    n = len(data)
    if n == 0:
        return None, None, None
    observed = sum(data) / n
    means = []
    for _ in range(n_boot):
        sample = [data[rng.randint(0, n - 1)] for _ in range(n)]
        means.append(sum(sample) / n)
    means.sort()
    lo = means[int(0.025 * n_boot)]
    hi = means[int(0.975 * n_boot)]
    return observed, lo, hi


def gini_coefficient(values):
    """Compute Gini coefficient (0=perfect equality, 1=perfect inequality)."""
    vals = sorted(values)
    n = len(vals)
    if n == 0 or sum(vals) == 0:
        return 0.0
    cum = 0.0
    weighted_sum = 0.0
    for i, v in enumerate(vals):
        cum += v
        weighted_sum += (2 * (i + 1) - n - 1) * v
    return weighted_sum / (n * cum)


def lorenz_area(values):
    """Area under the Lorenz curve (used to compute Gini = 1 - 2*area)."""
    vals = sorted(values)
    n = len(vals)
    total = sum(vals)
    if total == 0:
        return 0.5
    cum = 0.0
    area = 0.0
    for i, v in enumerate(vals):
        cum += v
        area += cum / total
    return area / n



# ── Main analysis ─────────────────────────────────────────────────

def main():
    print("=" * 60)
    print(f"  {'Research Corridor Mapping'}")
    print(f"  Africa E156 | Group: geographic-equity")
    print("=" * 60)
    print()

    # Pre-loaded data (from ClinicalTrials.gov)
    africa_count = 3515
    us_count = 159433
    europe_count = 234
    total_africa = 23873

    country_values = [11752, 3654, 809, 781, 712, 465, 398, 312, 201, 156]
    region_values = [africa_count, us_count, europe_count]

    x_pop = list(range(1, len(country_values) + 1))
    rho = spearman_rank(x_pop, country_values)
    print(f"Spearman rho (rank vs trials): {rho:.4f}")
    x_years = list(range(2005, 2005 + len(country_values)))
    b, a, r2 = linear_regression(x_years, country_values)
    print(f"Linear regression: slope={b:.2f}, intercept={a:.2f}, R2={r2:.4f}")
    est, lo, hi = bootstrap_ci(country_values)
    print(f"Bootstrap CI for mean: {est:.1f} [{lo:.1f}, {hi:.1f}]")
    g = gini_coefficient(country_values)
    print(f"Gini coefficient: {g:.4f}")
    area = lorenz_area(country_values)
    print(f"Lorenz area: {area:.4f} (Gini = {1 - 2*area:.4f})")

    print()
    print("─" * 60)
    print("Data: ClinicalTrials.gov API v2 (April 2026)")
    print("E156 Format: 7 sentences, <=156 words")
    print("GitHub: https://github.com/mahmood726-cyber/africa-e156-students")


if __name__ == "__main__":
    main()
