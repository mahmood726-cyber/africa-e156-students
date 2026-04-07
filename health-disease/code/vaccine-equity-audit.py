#!/usr/bin/env python3
"""
Vaccine Equity Audit — Africa E156 Student Analysis
Group: health-disease | Paper #51

Condition: vaccine
Location: Africa

This standalone script demonstrates the statistical methods used in this paper.
Run: python vaccine-equity-audit.py
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
    params["query.cond"] = "vaccine"
    params["query.locn"] = "Africa"
    try:
        resp = requests.get(API_URL, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json().get("totalCount", 0)
    except Exception as e:
        print(f"API error: {e}")
        return 0


# ── Statistical methods ───────────────────────────────────────────

def hhi_index(values):
    """Herfindahl-Hirschman Index (0=fragmented, 1=monopoly)."""
    total = sum(values)
    if total == 0:
        return 0.0
    return sum((v / total) ** 2 for v in values)


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


def rate_ratio(count_a, pop_a, count_b, pop_b):
    """Rate ratio with 95% CI (Wald method on log scale)."""
    if pop_a == 0 or pop_b == 0 or count_a == 0 or count_b == 0:
        return None, None, None
    rate_a = count_a / pop_a
    rate_b = count_b / pop_b
    rr = rate_a / rate_b
    se_log = math.sqrt(1/count_a + 1/count_b)
    lo = math.exp(math.log(rr) - 1.96 * se_log)
    hi = math.exp(math.log(rr) + 1.96 * se_log)
    return rr, lo, hi


def theil_index(values):
    """Theil T index of inequality."""
    n = len(values)
    if n == 0:
        return 0.0
    mu = sum(values) / n
    if mu == 0:
        return 0.0
    t = 0.0
    for v in values:
        if v > 0:
            t += (v / mu) * math.log(v / mu)
    return t / n



# ── Main analysis ─────────────────────────────────────────────────

def main():
    print("=" * 60)
    print(f"  {'Vaccine Equity Audit'}")
    print(f"  Africa E156 | Group: health-disease")
    print("=" * 60)
    print()

    # Pre-loaded data (from ClinicalTrials.gov)
    africa_count = 177
    us_count = 3486
    europe_count = 4
    total_africa = 23873

    country_values = [11752, 3654, 809, 781, 712, 465, 398, 312, 201, 156]
    region_values = [africa_count, us_count, europe_count]

    hhi = hhi_index(country_values)
    print(f"HHI concentration: {hhi:.4f}")
    est, lo, hi = bootstrap_ci(country_values)
    print(f"Bootstrap CI for mean: {est:.1f} [{lo:.1f}, {hi:.1f}]")
    rr, lo, hi = rate_ratio(africa_count, 1400000000, us_count, 330000000)
    if rr: print(f"Rate ratio (Africa/US): {rr:.4f} [{lo:.4f}, {hi:.4f}]")
    t = theil_index(country_values)
    print(f"Theil index: {t:.4f}")

    print()
    print("─" * 60)
    print("Data: ClinicalTrials.gov API v2 (April 2026)")
    print("E156 Format: 7 sentences, <=156 words")
    print("GitHub: https://github.com/mahmood726-cyber/africa-e156-students")


if __name__ == "__main__":
    main()
