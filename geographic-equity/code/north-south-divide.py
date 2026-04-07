#!/usr/bin/env python3
"""
North Africa vs Sub-Saharan Divide — Africa E156 Student Analysis
Group: geographic-equity | Paper #30

Condition: all interventional
Location: Africa

This standalone script demonstrates the statistical methods used in this paper.
Run: python north-south-divide.py
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


def bayesian_rate(successes, trials, prior_a=1, prior_b=1):
    """Bayesian posterior rate (Beta-Binomial conjugate)."""
    post_a = prior_a + successes
    post_b = prior_b + trials - successes
    mean = post_a / (post_a + post_b)
    # Approximate 95% credible interval
    var = (post_a * post_b) / ((post_a + post_b)**2 * (post_a + post_b + 1))
    sd = math.sqrt(var)
    return mean, max(0, mean - 1.96 * sd), min(1, mean + 1.96 * sd)


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


def chi_squared(observed, expected):
    """Chi-squared test statistic."""
    chi2 = 0.0
    for o, e in zip(observed, expected):
        if e > 0:
            chi2 += (o - e) ** 2 / e
    return chi2



# ── Main analysis ─────────────────────────────────────────────────

def main():
    print("=" * 60)
    print(f"  {'North Africa vs Sub-Saharan Divide'}")
    print(f"  Africa E156 | Group: geographic-equity")
    print("=" * 60)
    print()

    # Pre-loaded data (from ClinicalTrials.gov)
    africa_count = 3515
    us_count = 159433
    europe_count = 234
    total_africa = 23873

    # Top country trial counts
    country_values = [11752, 540, 162, 114, 12]
    region_values = [africa_count, us_count, europe_count]

    rr, lo, hi = rate_ratio(africa_count, 1400000000, us_count, 330000000)
    if rr: print(f"Rate ratio (Africa/US): {rr:.4f} [{lo:.4f}, {hi:.4f}]")
    post_mean, lo, hi = bayesian_rate(africa_count, africa_count + us_count)
    print(f"Bayesian posterior rate: {post_mean:.4f} [{lo:.4f}, {hi:.4f}]")
    t = theil_index(country_values)
    print(f"Theil index: {t:.4f}")
    est, lo, hi = bootstrap_ci(country_values)
    print(f"Bootstrap CI for mean: {est:.1f} [{lo:.1f}, {hi:.1f}]")
    n = len(country_values)
    expected = [sum(country_values)/n] * n
    chi2 = chi_squared(country_values, expected)
    print(f"Chi-squared (vs uniform): {chi2:.2f}")

    print()
    print("─" * 60)
    print("Data: ClinicalTrials.gov API v2 (April 2026)")
    print("E156 Format: 7 sentences, <=156 words")
    print("GitHub: https://github.com/mahmood726-cyber/africa-e156-students")


if __name__ == "__main__":
    main()
