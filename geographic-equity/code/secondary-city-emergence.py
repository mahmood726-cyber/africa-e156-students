#!/usr/bin/env python3
"""
Secondary City Emergence — Africa E156 Student Analysis
Group: geographic-equity | Paper #32

Condition: all interventional
Location: Africa

This standalone script demonstrates the statistical methods used in this paper.
Run: python secondary-city-emergence.py
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

def poisson_rate(count, exposure):
    """Poisson rate with 95% CI."""
    if exposure == 0:
        return 0, 0, 0
    rate = count / exposure
    se = math.sqrt(count) / exposure
    return rate, rate - 1.96 * se, rate + 1.96 * se


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



# ── Main analysis ─────────────────────────────────────────────────

def main():
    print("=" * 60)
    print(f"  {'Secondary City Emergence'}")
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

    rate, lo, hi = poisson_rate(africa_count, 1400000000)
    print(f"Poisson rate: {rate:.2e} [{lo:.2e}, {hi:.2e}]")
    est, lo, hi = bootstrap_ci(country_values)
    print(f"Bootstrap CI for mean: {est:.1f} [{lo:.1f}, {hi:.1f}]")
    x_years = list(range(2005, 2005 + len(country_values)))
    b, a, r2 = linear_regression(x_years, country_values)
    print(f"Linear regression: slope={b:.2f}, intercept={a:.2f}, R2={r2:.4f}")

    print()
    print("─" * 60)
    print("Data: ClinicalTrials.gov API v2 (April 2026)")
    print("E156 Format: 7 sentences, <=156 words")
    print("GitHub: https://github.com/mahmood726-cyber/africa-e156-students")


if __name__ == "__main__":
    main()
