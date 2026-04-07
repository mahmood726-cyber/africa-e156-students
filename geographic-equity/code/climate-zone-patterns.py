#!/usr/bin/env python3
"""
Climate Zone Research Patterns — Africa E156 Student Analysis
Group: geographic-equity | Paper #34

Condition: all interventional
Location: Africa

This standalone script demonstrates the statistical methods used in this paper.
Run: python climate-zone-patterns.py
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

def chi_squared(observed, expected):
    """Chi-squared test statistic."""
    chi2 = 0.0
    for o, e in zip(observed, expected):
        if e > 0:
            chi2 += (o - e) ** 2 / e
    return chi2


def cohens_d(mean1, sd1, n1, mean2, sd2, n2):
    """Cohen's d effect size."""
    pooled_sd = math.sqrt(((n1 - 1) * sd1**2 + (n2 - 1) * sd2**2) / (n1 + n2 - 2))
    if pooled_sd == 0:
        return 0.0
    return (mean1 - mean2) / pooled_sd


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


def kl_divergence(p_vals, q_vals):
    """Kullback-Leibler divergence D_KL(P||Q)."""
    total_p = sum(p_vals)
    total_q = sum(q_vals)
    if total_p == 0 or total_q == 0:
        return 0.0
    kl = 0.0
    for p, q in zip(p_vals, q_vals):
        pp = p / total_p
        qq = q / total_q
        if pp > 0 and qq > 0:
            kl += pp * math.log2(pp / qq)
    return kl


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



# ── Main analysis ─────────────────────────────────────────────────

def main():
    print("=" * 60)
    print(f"  {'Climate Zone Research Patterns'}")
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

    n = len(country_values)
    expected = [sum(country_values)/n] * n
    chi2 = chi_squared(country_values, expected)
    print(f"Chi-squared (vs uniform): {chi2:.2f}")
    d = cohens_d(sum(country_values)/len(country_values), max(1, max(country_values)-min(country_values)), len(country_values), us_count/10, us_count/5, 10)
    print(f"Cohen's d: {d:.3f}")
    est, lo, hi = bootstrap_ci(country_values)
    print(f"Bootstrap CI for mean: {est:.1f} [{lo:.1f}, {hi:.1f}]")
    n_c = len(country_values)
    uniform = [sum(country_values)/n_c] * n_c
    kl = kl_divergence(country_values, uniform)
    print(f"KL divergence from uniform: {kl:.4f} bits")
    p = permutation_test(country_values[:5], country_values[5:])
    print(f"Permutation test p-value: {p:.4f}")

    print()
    print("─" * 60)
    print("Data: ClinicalTrials.gov API v2 (April 2026)")
    print("E156 Format: 7 sentences, <=156 words")
    print("GitHub: https://github.com/mahmood726-cyber/africa-e156-students")


if __name__ == "__main__":
    main()
