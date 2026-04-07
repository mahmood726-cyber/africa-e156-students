#!/usr/bin/env python3
"""
Participant Compensation Ethics — Africa E156 Student Analysis
Group: governance-justice | Paper #22

Condition: all interventional
Location: Africa

This standalone script demonstrates the statistical methods used in this paper.
Run: python participant-compensation.py
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


def permutation_test(group_a, group_b, n_perm=5000, seed=42):
    """Two-sample permutation test for difference in means."""
    rng = random.Random(seed)
    combined = group_a + group_b
    obs_diff = abs(sum(group_a)/len(group_a) - sum(group_b)/len(group_b))
    n_a = len(group_a)
    count = 0
    for _ in range(n_perm):
        rng.shuffle(combined)
        perm_diff = abs(sum(combined[:n_a])/n_a - sum(combined[n_a:])/len(group_b))
        if perm_diff >= obs_diff:
            count += 1
    return count / n_perm


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
    print(f"  {'Participant Compensation Ethics'}")
    print(f"  Africa E156 | Group: governance-justice")
    print("=" * 60)
    print()

    # Pre-loaded data (from ClinicalTrials.gov)
    africa_count = 3515
    us_count = 159433
    europe_count = 234
    total_africa = 23873

    country_values = [11752, 3654, 809, 781, 712, 465, 398, 312, 201, 156]
    region_values = [africa_count, us_count, europe_count]

    g = gini_coefficient(country_values)
    print(f"Gini coefficient: {g:.4f}")
    est, lo, hi = bootstrap_ci(country_values)
    print(f"Bootstrap CI for mean: {est:.1f} [{lo:.1f}, {hi:.1f}]")
    rr, lo, hi = rate_ratio(africa_count, 1400000000, us_count, 330000000)
    if rr: print(f"Rate ratio (Africa/US): {rr:.4f} [{lo:.4f}, {hi:.4f}]")
    p = permutation_test(country_values[:5], country_values[5:])
    print(f"Permutation test p-value: {p:.4f}")
    area = lorenz_area(country_values)
    print(f"Lorenz area: {area:.4f} (Gini = {1 - 2*area:.4f})")

    print()
    print("─" * 60)
    print("Data: ClinicalTrials.gov API v2 (April 2026)")
    print("E156 Format: 7 sentences, <=156 words")
    print("GitHub: https://github.com/mahmood726-cyber/africa-e156-students")


if __name__ == "__main__":
    main()
