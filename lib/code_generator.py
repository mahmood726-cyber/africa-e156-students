"""
Generate standalone Python analysis scripts for each E156 paper.

Each script is self-contained (~100-150 lines), uses only stdlib + requests,
and demonstrates the statistical methods relevant to the paper's topic.
"""
import random


def _safe_div(a, b, default=0.0):
    if b is None or b == 0:
        return default
    return a / b


def _fmt(v):
    if v is None:
        return "N/A"
    if isinstance(v, int):
        return f"{v:,}"
    if isinstance(v, float):
        return f"{v:,.2f}"
    return str(v)


# Method code snippets -- each is a standalone function
_METHOD_SNIPPETS = {
    "gini_coefficient": '''
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
''',

    "bootstrap_ci": '''
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
''',

    "shannon_entropy": '''
def shannon_entropy(values):
    """Shannon entropy in bits."""
    total = sum(values)
    if total == 0:
        return 0.0
    h = 0.0
    for v in values:
        if v > 0:
            p = v / total
            h -= p * math.log2(p)
    return h
''',

    "rate_ratio": '''
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
''',

    "hhi_index": '''
def hhi_index(values):
    """Herfindahl-Hirschman Index (0=fragmented, 1=monopoly)."""
    total = sum(values)
    if total == 0:
        return 0.0
    return sum((v / total) ** 2 for v in values)
''',

    "poisson_rate": '''
def poisson_rate(count, exposure):
    """Poisson rate with 95% CI."""
    if exposure == 0:
        return 0, 0, 0
    rate = count / exposure
    se = math.sqrt(count) / exposure
    return rate, rate - 1.96 * se, rate + 1.96 * se
''',

    "theil_index": '''
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
''',

    "lorenz": '''
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
''',

    "chi_squared": '''
def chi_squared(observed, expected):
    """Chi-squared test statistic."""
    chi2 = 0.0
    for o, e in zip(observed, expected):
        if e > 0:
            chi2 += (o - e) ** 2 / e
    return chi2
''',

    "spearman_correlation": '''
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
''',

    "linear_regression": '''
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
''',

    "network_centrality": '''
def degree_centrality(adjacency):
    """Compute degree centrality for each node."""
    n = len(adjacency)
    if n <= 1:
        return [0.0]
    return [sum(adjacency[i]) / (n - 1) for i in range(n)]
''',

    "kaplan_meier": '''
def kaplan_meier_survival(event_times, censored=None):
    """Simple Kaplan-Meier survival estimate."""
    n = len(event_times)
    if censored is None:
        censored = [False] * n
    sorted_data = sorted(zip(event_times, censored))
    at_risk = n
    survival = 1.0
    curve = []
    for t, c in sorted_data:
        if not c:
            survival *= (at_risk - 1) / at_risk
        at_risk -= 1
        curve.append((t, survival))
    return curve
''',

    "odds_ratio": '''
def odds_ratio_2x2(a, b, c, d):
    """Odds ratio from 2x2 table with 95% CI."""
    if b == 0 or c == 0 or a == 0 or d == 0:
        return None, None, None
    or_val = (a * d) / (b * c)
    se_log = math.sqrt(1/a + 1/b + 1/c + 1/d)
    lo = math.exp(math.log(or_val) - 1.96 * se_log)
    hi = math.exp(math.log(or_val) + 1.96 * se_log)
    return or_val, lo, hi
''',

    "effect_size": '''
def cohens_d(mean1, sd1, n1, mean2, sd2, n2):
    """Cohen's d effect size."""
    pooled_sd = math.sqrt(((n1 - 1) * sd1**2 + (n2 - 1) * sd2**2) / (n1 + n2 - 2))
    if pooled_sd == 0:
        return 0.0
    return (mean1 - mean2) / pooled_sd
''',

    "permutation": '''
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
''',

    "bayesian_rate": '''
def bayesian_rate(successes, trials, prior_a=1, prior_b=1):
    """Bayesian posterior rate (Beta-Binomial conjugate)."""
    post_a = prior_a + successes
    post_b = prior_b + trials - successes
    mean = post_a / (post_a + post_b)
    # Approximate 95% credible interval
    var = (post_a * post_b) / ((post_a + post_b)**2 * (post_a + post_b + 1))
    sd = math.sqrt(var)
    return mean, max(0, mean - 1.96 * sd), min(1, mean + 1.96 * sd)
''',

    "kl_divergence": '''
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
''',

    "concentration_index": '''
def concentration_index(values):
    """Health concentration index (based on Lorenz curve)."""
    vals = sorted(values)
    n = len(vals)
    total = sum(vals)
    if n == 0 or total == 0:
        return 0.0
    cum = 0.0
    weighted = 0.0
    for i, v in enumerate(vals):
        cum += v
        weighted += (2 * (i + 1) - n - 1) * v
    return weighted / (n * total)
''',
}

# Fallback methods if the paper's stat is not in snippets
_FALLBACK_METHODS = ["gini_coefficient", "bootstrap_ci", "shannon_entropy"]


def generate_code_script(paper_def, data, stats_results):
    """Generate a standalone Python analysis script for students.

    Parameters
    ----------
    paper_def : dict
        Paper definition from MANIFEST.
    data : dict
        Fetched data.
    stats_results : dict
        Computed statistics.

    Returns
    -------
    str
        Complete Python script as a string.
    """
    slug = paper_def["slug"]
    title = paper_def["title"]
    group = paper_def["group"]
    rng = random.Random(hash(slug) % 2**32)

    q = paper_def.get("query", {})
    condition = q.get("condition")
    location = q.get("location", "Africa")

    africa = data.get("africa_count", 0) or 0
    us = data.get("us_count", 0) or 0
    europe = data.get("europe_count", 0) or 0
    total_africa = data.get("total_africa", 23873) or 23873

    # Determine which stat methods to include (3-5)
    paper_stats = paper_def.get("stats", [])
    methods_to_include = []
    for s in paper_stats[:5]:
        if s in _METHOD_SNIPPETS:
            methods_to_include.append(s)
    # Ensure at least 3
    for fb in _FALLBACK_METHODS:
        if len(methods_to_include) >= 3:
            break
        if fb not in methods_to_include:
            methods_to_include.append(fb)

    # Build API query params
    api_params = []
    if condition:
        api_params.append(f'    params["query.cond"] = "{condition}"')
    api_params.append(f'    params["query.locn"] = "{location}"')
    other = q.get("other")
    if other:
        api_params.append(f'    params["query.term"] = "{other}"')

    api_block = '\n'.join(api_params)

    # Build method code
    method_code = ""
    for m in methods_to_include:
        method_code += _METHOD_SNIPPETS[m] + "\n"

    # Build analysis calls
    analysis_lines = []
    analysis_lines.append(f'    # Pre-loaded data (from ClinicalTrials.gov)')
    analysis_lines.append(f'    africa_count = {africa}')
    analysis_lines.append(f'    us_count = {us}')
    analysis_lines.append(f'    europe_count = {europe}')
    analysis_lines.append(f'    total_africa = {total_africa}')
    analysis_lines.append(f'')

    # Country values for demo
    country_counts = data.get("country_counts", {})
    if country_counts:
        top_items = sorted(country_counts.items(), key=lambda x: -x[1])[:10]
        vals_str = ", ".join(str(v) for _, v in top_items)
        analysis_lines.append(f'    # Top country trial counts')
        analysis_lines.append(f'    country_values = [{vals_str}]')
    else:
        analysis_lines.append(f'    country_values = [11752, 3654, 809, 781, 712, 465, 398, 312, 201, 156]')

    analysis_lines.append(f'    region_values = [africa_count, us_count, europe_count]')
    analysis_lines.append(f'')

    # Call each method
    for m in methods_to_include:
        if m == "gini_coefficient":
            analysis_lines.append('    g = gini_coefficient(country_values)')
            analysis_lines.append('    print(f"Gini coefficient: {g:.4f}")')
        elif m == "bootstrap_ci":
            analysis_lines.append('    est, lo, hi = bootstrap_ci(country_values)')
            analysis_lines.append('    print(f"Bootstrap CI for mean: {est:.1f} [{lo:.1f}, {hi:.1f}]")')
        elif m == "shannon_entropy":
            analysis_lines.append('    h = shannon_entropy(country_values)')
            analysis_lines.append('    print(f"Shannon entropy: {h:.3f} bits")')
        elif m == "rate_ratio":
            analysis_lines.append('    rr, lo, hi = rate_ratio(africa_count, 1400000000, us_count, 330000000)')
            analysis_lines.append('    if rr: print(f"Rate ratio (Africa/US): {rr:.4f} [{lo:.4f}, {hi:.4f}]")')
        elif m == "hhi_index":
            analysis_lines.append('    hhi = hhi_index(country_values)')
            analysis_lines.append('    print(f"HHI concentration: {hhi:.4f}")')
        elif m == "poisson_rate":
            analysis_lines.append('    rate, lo, hi = poisson_rate(africa_count, 1400000000)')
            analysis_lines.append('    print(f"Poisson rate: {rate:.2e} [{lo:.2e}, {hi:.2e}]")')
        elif m == "theil_index":
            analysis_lines.append('    t = theil_index(country_values)')
            analysis_lines.append('    print(f"Theil index: {t:.4f}")')
        elif m == "lorenz":
            analysis_lines.append('    area = lorenz_area(country_values)')
            analysis_lines.append('    print(f"Lorenz area: {area:.4f} (Gini = {1 - 2*area:.4f})")')
        elif m == "chi_squared":
            analysis_lines.append('    n = len(country_values)')
            analysis_lines.append('    expected = [sum(country_values)/n] * n')
            analysis_lines.append('    chi2 = chi_squared(country_values, expected)')
            analysis_lines.append('    print(f"Chi-squared (vs uniform): {chi2:.2f}")')
        elif m == "spearman_correlation":
            analysis_lines.append('    x_pop = list(range(1, len(country_values) + 1))')
            analysis_lines.append('    rho = spearman_rank(x_pop, country_values)')
            analysis_lines.append('    print(f"Spearman rho (rank vs trials): {rho:.4f}")')
        elif m == "linear_regression":
            analysis_lines.append('    x_years = list(range(2005, 2005 + len(country_values)))')
            analysis_lines.append('    b, a, r2 = linear_regression(x_years, country_values)')
            analysis_lines.append('    print(f"Linear regression: slope={b:.2f}, intercept={a:.2f}, R2={r2:.4f}")')
        elif m == "network_centrality":
            analysis_lines.append('    # Simple 5-node adjacency matrix')
            analysis_lines.append('    adj = [[0,1,1,0,0],[1,0,1,1,0],[1,1,0,0,1],[0,1,0,0,1],[0,0,1,1,0]]')
            analysis_lines.append('    centrality = degree_centrality(adj)')
            analysis_lines.append('    print(f"Degree centrality: {[round(c,3) for c in centrality]}")')
        elif m == "kaplan_meier":
            analysis_lines.append('    times = sorted(country_values)')
            analysis_lines.append('    curve = kaplan_meier_survival(times)')
            analysis_lines.append('    print(f"KM median survival time: {curve[len(curve)//2][0]}")')
        elif m == "odds_ratio":
            analysis_lines.append('    or_val, lo, hi = odds_ratio_2x2(africa_count, us_count, europe_count, max(1, us_count - africa_count))')
            analysis_lines.append('    if or_val: print(f"Odds ratio: {or_val:.3f} [{lo:.3f}, {hi:.3f}]")')
        elif m == "effect_size":
            analysis_lines.append('    d = cohens_d(sum(country_values)/len(country_values), max(1, max(country_values)-min(country_values)), len(country_values), us_count/10, us_count/5, 10)')
            analysis_lines.append('    print(f"Cohen\'s d: {d:.3f}")')
        elif m == "permutation":
            analysis_lines.append('    p = permutation_test(country_values[:5], country_values[5:])')
            analysis_lines.append('    print(f"Permutation test p-value: {p:.4f}")')
        elif m == "bayesian_rate":
            analysis_lines.append('    post_mean, lo, hi = bayesian_rate(africa_count, africa_count + us_count)')
            analysis_lines.append('    print(f"Bayesian posterior rate: {post_mean:.4f} [{lo:.4f}, {hi:.4f}]")')
        elif m == "kl_divergence":
            analysis_lines.append('    n_c = len(country_values)')
            analysis_lines.append('    uniform = [sum(country_values)/n_c] * n_c')
            analysis_lines.append('    kl = kl_divergence(country_values, uniform)')
            analysis_lines.append('    print(f"KL divergence from uniform: {kl:.4f} bits")')
        elif m == "concentration_index":
            analysis_lines.append('    ci = concentration_index(country_values)')
            analysis_lines.append('    print(f"Concentration index: {ci:.4f}")')
        else:
            analysis_lines.append(f'    # {m}: see lib/stats_library.py for full implementation')

    analysis_block = '\n'.join(analysis_lines)

    # Build complete script
    cond_comment = f"Condition: {condition}" if condition else "Condition: all interventional"
    script = f'''#!/usr/bin/env python3
"""
{title} — Africa E156 Student Analysis
Group: {group} | Paper #{paper_def.get("paper_num", "?")}

{cond_comment}
Location: {location}

This standalone script demonstrates the statistical methods used in this paper.
Run: python {slug.replace("_", "-")}.py
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
    params = {{
        "format": "json",
        "pageSize": 0,
        "countTotal": "true",
        "filter.advanced": "AREA[StudyType]INTERVENTIONAL",
    }}
{api_block}
    try:
        resp = requests.get(API_URL, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json().get("totalCount", 0)
    except Exception as e:
        print(f"API error: {{e}}")
        return 0


# ── Statistical methods ───────────────────────────────────────────
{method_code}

# ── Main analysis ─────────────────────────────────────────────────

def main():
    print("=" * 60)
    print(f"  {{'{title}'}}")
    print(f"  Africa E156 | Group: {group}")
    print("=" * 60)
    print()

{analysis_block}

    print()
    print("─" * 60)
    print("Data: ClinicalTrials.gov API v2 (April 2026)")
    print("E156 Format: 7 sentences, <=156 words")
    print("GitHub: https://github.com/mahmood726-cyber/africa-e156-students")


if __name__ == "__main__":
    main()
'''

    return script
