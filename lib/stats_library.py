"""
Pure-Python statistical methods library for Africa E156 Student Platform.

31 methods covering inequality, information theory, epidemiology,
spatial statistics, survival analysis, regression, and more.

Dependencies: math, random (stdlib only). No numpy/scipy/sklearn.
"""

import math
import random

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _rank(values):
    """Assign average ranks to *values* (handles ties)."""
    n = len(values)
    indexed = sorted(range(n), key=lambda i: values[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j < n - 1 and values[indexed[j + 1]] == values[indexed[i]]:
            j += 1
        avg_rank = (i + j) / 2.0 + 1.0  # 1-based
        for k in range(i, j + 1):
            ranks[indexed[k]] = avg_rank
        i = j + 1
    return ranks


def _normal_cdf(z):
    """Approximate standard-normal CDF (Abramowitz & Stegun 26.2.17)."""
    if z < -8.0:
        return 0.0
    if z > 8.0:
        return 1.0
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    p = 0.3275911
    sign = 1
    if z < 0:
        sign = -1
        z = -z
    t = 1.0 / (1.0 + p * z)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-z * z / 2.0)
    return 0.5 * (1.0 + sign * y)


def _normal_ppf(p):
    """Approximate standard-normal quantile (Beasley-Springer-Moro)."""
    if p <= 0:
        return -8.0
    if p >= 1:
        return 8.0
    if p == 0.5:
        return 0.0

    # Rational approx for central region
    a = [
        -3.969683028665376e+01, 2.209460984245205e+02,
        -2.759285104469687e+02, 1.383577518672690e+02,
        -3.066479806614716e+01, 2.506628277459239e+00,
    ]
    b = [
        -5.447609879822406e+01, 1.615858368580409e+02,
        -1.556989798598866e+02, 6.680131188771972e+01,
        -1.328068155288572e+01,
    ]
    c = [
        -7.784894002430293e-03, -3.223964580411365e-01,
        -2.400758277161838e+00, -2.549732539343734e+00,
        4.374664141464968e+00, 2.938163982698783e+00,
    ]
    d = [
        7.784695709041462e-03, 3.224671290700398e-01,
        2.445134137142996e+00, 3.754408661907416e+00,
    ]
    p_low = 0.02425
    p_high = 1.0 - p_low

    if p_low <= p <= p_high:
        q = p - 0.5
        r = q * q
        num = (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5])
        den = ((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1.0
        return q * num / den
    else:
        if p < p_low:
            q = math.sqrt(-2.0 * math.log(p))
        else:
            q = math.sqrt(-2.0 * math.log(1.0 - p))
        num = (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5])
        den = (((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0
        result = num / den
        if p < p_low:
            return -result
        return result


def _chi2_cdf(x, df):
    """Approximate chi-squared CDF via Wilson-Hilferty normal approximation."""
    if x <= 0 or df <= 0:
        return 0.0
    # Wilson-Hilferty: ((x/df)^(1/3) - (1 - 2/(9*df))) / sqrt(2/(9*df))
    ratio = x / df
    cube_root = ratio ** (1.0 / 3.0)
    mean_term = 1.0 - 2.0 / (9.0 * df)
    var_term = math.sqrt(2.0 / (9.0 * df))
    z = (cube_root - mean_term) / var_term
    return _normal_cdf(z)


def _chi2_ppf(p, df):
    """Approximate chi-squared quantile via Wilson-Hilferty inversion."""
    if df <= 0 or p <= 0:
        return 0.0
    if p >= 1:
        return float('inf')
    z = _normal_ppf(p)
    # Wilson-Hilferty inversion
    term = 1.0 - 2.0 / (9.0 * df) + z * math.sqrt(2.0 / (9.0 * df))
    if term <= 0:
        return 0.0
    return df * (term ** 3)


def _mean(values):
    """Arithmetic mean."""
    if not values:
        return 0.0
    return sum(values) / len(values)


def _var(values, ddof=1):
    """Sample variance."""
    n = len(values)
    if n <= ddof:
        return 0.0
    m = _mean(values)
    return sum((v - m) ** 2 for v in values) / (n - ddof)


def _std(values, ddof=1):
    """Sample standard deviation."""
    return math.sqrt(_var(values, ddof))


def _gamma_ln(x):
    """Log-gamma via Lanczos approximation (g=7, n=9)."""
    if x <= 0:
        return float('inf')
    coefs = [
        0.99999999999980993, 676.5203681218851, -1259.1392167224028,
        771.32342877765313, -176.61502916214059, 12.507343278686905,
        -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7,
    ]
    if x < 0.5:
        return math.log(math.pi / math.sin(math.pi * x)) - _gamma_ln(1.0 - x)
    x -= 1.0
    a = coefs[0]
    t = x + 7.5
    for i in range(1, 9):
        a += coefs[i] / (x + i)
    return 0.5 * math.log(2.0 * math.pi) + (x + 0.5) * math.log(t) - t + math.log(a)


def _incomplete_beta(x, a, b, max_iter=200):
    """Regularized incomplete beta I_x(a, b) via continued fraction."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    if a <= 0 or b <= 0:
        return 0.0

    # Use symmetry if needed for faster convergence
    if x > (a + 1.0) / (a + b + 2.0):
        return 1.0 - _incomplete_beta(1.0 - x, b, a, max_iter)

    ln_prefix = (
        _gamma_ln(a + b) - _gamma_ln(a) - _gamma_ln(b)
        + a * math.log(x) + b * math.log(1.0 - x)
    )
    prefix = math.exp(ln_prefix)

    # Lentz's continued fraction
    eps = 1e-30
    f = 1.0 + eps
    c = f
    d_cf = 0.0

    for m in range(1, max_iter + 1):
        # Even step
        m2 = 2 * m
        # a_{2m}
        num = m * (b - m) * x / ((a + m2 - 1.0) * (a + m2))
        d_cf = 1.0 + num * d_cf
        if abs(d_cf) < eps:
            d_cf = eps
        d_cf = 1.0 / d_cf
        c = 1.0 + num / c
        if abs(c) < eps:
            c = eps
        f *= c * d_cf

        # Odd step: a_{2m+1}
        num = -(a + m) * (a + b + m) * x / ((a + m2) * (a + m2 + 1.0))
        d_cf = 1.0 + num * d_cf
        if abs(d_cf) < eps:
            d_cf = eps
        d_cf = 1.0 / d_cf
        c = 1.0 + num / c
        if abs(c) < eps:
            c = eps
        delta = c * d_cf
        f *= delta

        if abs(delta - 1.0) < 1e-10:
            break

    return prefix * (f - 1.0) / a


def _t_cdf(t_val, df):
    """CDF of Student's t-distribution using incomplete beta."""
    if df <= 0:
        return 0.5
    x = df / (df + t_val * t_val)
    beta_val = 0.5 * _incomplete_beta(x, df / 2.0, 0.5)
    if t_val >= 0:
        return 1.0 - beta_val
    return beta_val


# ---------------------------------------------------------------------------
# 1. Bootstrap CI (BCa)
# ---------------------------------------------------------------------------


def bootstrap_ci(data, stat_fn=None, n_boot=10000, alpha=0.05, seed=42):
    """BCa bootstrap confidence interval.

    Parameters
    ----------
    data : list of float
        Sample data.
    stat_fn : callable, optional
        Statistic function; defaults to arithmetic mean.
    n_boot : int
        Number of bootstrap resamples.
    alpha : float
        Significance level (default 0.05 for 95% CI).
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    dict with keys: estimate, ci_lower, ci_upper, se, n_boot
    """
    if not data:
        return {"estimate": None, "ci_lower": None, "ci_upper": None, "se": 0.0, "n_boot": 0}
    if stat_fn is None:
        stat_fn = _mean

    n = len(data)
    rng = random.Random(seed)
    theta_hat = stat_fn(data)

    # Bootstrap distribution
    boot_stats = []
    for _ in range(n_boot):
        sample = [data[rng.randint(0, n - 1)] for _ in range(n)]
        boot_stats.append(stat_fn(sample))
    boot_stats.sort()

    se = _std(boot_stats, ddof=1) if len(boot_stats) > 1 else 0.0

    # --- BCa correction ---
    # Bias correction z0
    count_below = sum(1 for b in boot_stats if b < theta_hat)
    prop_below = count_below / n_boot
    prop_below = max(1e-10, min(1.0 - 1e-10, prop_below))
    z0 = _normal_ppf(prop_below)

    # Acceleration a (jackknife)
    jack_stats = []
    for i in range(n):
        jack_sample = data[:i] + data[i + 1:]
        jack_stats.append(stat_fn(jack_sample))
    jack_mean = _mean(jack_stats)
    num_acc = sum((jack_mean - js) ** 3 for js in jack_stats)
    den_acc = sum((jack_mean - js) ** 2 for js in jack_stats)
    den_acc = den_acc ** 1.5
    a_hat = num_acc / (6.0 * den_acc) if den_acc != 0 else 0.0

    # Adjusted percentiles
    z_alpha_low = _normal_ppf(alpha / 2.0)
    z_alpha_high = _normal_ppf(1.0 - alpha / 2.0)

    def _bca_percentile(z_alpha):
        num = z0 + z_alpha
        denom = 1.0 - a_hat * num
        if abs(denom) < 1e-15:
            denom = 1e-15
        adj = z0 + num / denom
        p = _normal_cdf(adj)
        p = max(0.0, min(1.0, p))
        idx = p * (n_boot - 1)
        lo_idx = int(math.floor(idx))
        hi_idx = min(lo_idx + 1, n_boot - 1)
        frac = idx - lo_idx
        return boot_stats[lo_idx] * (1 - frac) + boot_stats[hi_idx] * frac

    ci_lower = _bca_percentile(z_alpha_low)
    ci_upper = _bca_percentile(z_alpha_high)

    return {
        "estimate": theta_hat,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "se": se,
        "n_boot": n_boot,
    }


# ---------------------------------------------------------------------------
# 2. Gini coefficient
# ---------------------------------------------------------------------------


def gini_coefficient(values):
    """Gini inequality coefficient (0 = perfect equality, 1 = max inequality).

    Parameters
    ----------
    values : list of float
        Non-negative values.

    Returns
    -------
    dict with key: gini
    """
    if not values or len(values) < 2:
        return {"gini": 0.0}
    vals = sorted(v for v in values if v >= 0)
    n = len(vals)
    if n < 2 or sum(vals) == 0:
        return {"gini": 0.0}
    total = sum(vals)
    cum = 0.0
    numerator = 0.0
    for i, v in enumerate(vals):
        cum += v
        numerator += (2 * (i + 1) - n - 1) * v
    gini = numerator / (n * total)
    return {"gini": max(0.0, min(1.0, gini))}


# ---------------------------------------------------------------------------
# 3. Lorenz curve
# ---------------------------------------------------------------------------


def lorenz_curve(values, n_points=20):
    """Lorenz curve points for inequality visualisation.

    Parameters
    ----------
    values : list of float
        Non-negative values.
    n_points : int
        Number of output points (including 0,0 and 1,1).

    Returns
    -------
    dict with key: points — list of (x, y) tuples
    """
    if not values:
        return {"points": [(0.0, 0.0), (1.0, 1.0)]}
    vals = sorted(v for v in values if v >= 0)
    n = len(vals)
    if n == 0 or sum(vals) == 0:
        return {"points": [(0.0, 0.0), (1.0, 1.0)]}

    total = sum(vals)
    cum = [0.0]
    running = 0.0
    for v in vals:
        running += v
        cum.append(running / total)

    points = [(0.0, 0.0)]
    for i in range(1, n_points):
        frac = i / (n_points - 1) if n_points > 1 else 1.0
        idx_f = frac * n
        lo = int(math.floor(idx_f))
        hi = min(lo + 1, n)
        w = idx_f - lo
        y = cum[lo] * (1 - w) + cum[hi] * w
        x = frac
        points.append((round(x, 6), round(y, 6)))
    # Ensure endpoint
    if points[-1] != (1.0, 1.0):
        points[-1] = (1.0, 1.0)
    return {"points": points}


# ---------------------------------------------------------------------------
# 4. Theil index
# ---------------------------------------------------------------------------


def theil_index(values):
    """Theil index (GE(1)): generalized entropy inequality measure.

    Parameters
    ----------
    values : list of float
        Positive values.

    Returns
    -------
    dict with key: theil
    """
    pos = [v for v in (values or []) if v > 0]
    if len(pos) < 2:
        return {"theil": 0.0}
    mu = _mean(pos)
    n = len(pos)
    t = sum((v / mu) * math.log(v / mu) for v in pos) / n
    return {"theil": max(0.0, t)}


# ---------------------------------------------------------------------------
# 5. Atkinson index
# ---------------------------------------------------------------------------


def atkinson_index(values, epsilon=1.0):
    """Atkinson inequality index.

    Parameters
    ----------
    values : list of float
        Positive values.
    epsilon : float
        Inequality aversion parameter (default 1.0).

    Returns
    -------
    dict with keys: atkinson, epsilon
    """
    pos = [v for v in (values or []) if v > 0]
    if len(pos) < 2:
        return {"atkinson": 0.0, "epsilon": epsilon}
    mu = _mean(pos)
    n = len(pos)

    if abs(epsilon - 1.0) < 1e-12:
        # Geometric mean / arithmetic mean
        log_sum = sum(math.log(v) for v in pos) / n
        geo_mean = math.exp(log_sum)
        a = 1.0 - geo_mean / mu
    else:
        power = 1.0 - epsilon
        gen_mean = (sum((v / mu) ** power for v in pos) / n) ** (1.0 / power)
        a = 1.0 - gen_mean
    return {"atkinson": max(0.0, min(1.0, a)), "epsilon": epsilon}


# ---------------------------------------------------------------------------
# 6. Shannon entropy
# ---------------------------------------------------------------------------


def shannon_entropy(values):
    """Shannon entropy in bits.

    Parameters
    ----------
    values : list of float
        Non-negative values (treated as counts/weights, normalised internally).

    Returns
    -------
    dict with key: entropy
    """
    if not values:
        return {"entropy": 0.0}
    pos = [v for v in values if v > 0]
    if not pos:
        return {"entropy": 0.0}
    total = sum(pos)
    h = -sum((v / total) * math.log2(v / total) for v in pos)
    return {"entropy": h}


# ---------------------------------------------------------------------------
# 7. Normalized entropy
# ---------------------------------------------------------------------------


def normalized_entropy(values):
    """Normalized Shannon entropy H/H_max in [0, 1].

    Parameters
    ----------
    values : list of float
        Non-negative values.

    Returns
    -------
    dict with keys: normalized_entropy, entropy, h_max
    """
    if not values:
        return {"normalized_entropy": 0.0, "entropy": 0.0, "h_max": 0.0}
    pos = [v for v in values if v > 0]
    k = len(pos)
    if k <= 1:
        return {"normalized_entropy": 0.0, "entropy": 0.0, "h_max": 0.0}
    h = shannon_entropy(pos)["entropy"]
    h_max = math.log2(k)
    return {
        "normalized_entropy": h / h_max if h_max > 0 else 0.0,
        "entropy": h,
        "h_max": h_max,
    }


# ---------------------------------------------------------------------------
# 8. KL divergence
# ---------------------------------------------------------------------------


def kl_divergence(p_values, q_values):
    """Kullback-Leibler divergence D_KL(P || Q) in bits.

    Parameters
    ----------
    p_values, q_values : list of float
        Non-negative weight vectors (same length, normalised internally).

    Returns
    -------
    dict with key: kl_divergence
    """
    if not p_values or not q_values or len(p_values) != len(q_values):
        return {"kl_divergence": None}
    p_total = sum(p_values)
    q_total = sum(q_values)
    if p_total <= 0 or q_total <= 0:
        return {"kl_divergence": None}
    p_norm = [v / p_total for v in p_values]
    q_norm = [v / q_total for v in q_values]
    kl = 0.0
    for pi, qi in zip(p_norm, q_norm):
        if pi > 0:
            if qi <= 0:
                return {"kl_divergence": float('inf')}
            kl += pi * math.log2(pi / qi)
    return {"kl_divergence": kl}


# ---------------------------------------------------------------------------
# 9. HHI
# ---------------------------------------------------------------------------


def hhi_index(values):
    """Herfindahl-Hirschman Index (0-10000 scale).

    Parameters
    ----------
    values : list of float
        Non-negative market share values (normalised internally).

    Returns
    -------
    dict with keys: hhi, hhi_normalized, n_categories
    """
    if not values:
        return {"hhi": 0.0, "hhi_normalized": 0.0, "n_categories": 0}
    pos = [v for v in values if v > 0]
    n = len(pos)
    if n == 0:
        return {"hhi": 0.0, "hhi_normalized": 0.0, "n_categories": 0}
    total = sum(pos)
    shares = [v / total for v in pos]
    hhi = sum(s * s for s in shares) * 10000
    hhi_norm = (hhi / 10000 - 1.0 / n) / (1.0 - 1.0 / n) if n > 1 else 0.0
    return {"hhi": hhi, "hhi_normalized": max(0.0, hhi_norm), "n_categories": n}


# ---------------------------------------------------------------------------
# 10. Rate ratio
# ---------------------------------------------------------------------------


def rate_ratio(count_a, pop_a, count_b, pop_b):
    """Rate ratio with 95% Wald CI on log scale.

    Parameters
    ----------
    count_a, pop_a : int/float
        Events and person-time for group A.
    count_b, pop_b : int/float
        Events and person-time for group B.

    Returns
    -------
    dict with keys: rate_a, rate_b, rate_ratio, ci_lower, ci_upper
    """
    if pop_a <= 0 or pop_b <= 0:
        return {"rate_a": None, "rate_b": None, "rate_ratio": None,
                "ci_lower": None, "ci_upper": None}
    rate_a = count_a / pop_a
    rate_b = count_b / pop_b
    if count_b == 0:
        return {"rate_a": rate_a, "rate_b": 0.0, "rate_ratio": float('inf'),
                "ci_lower": None, "ci_upper": None}
    rr = rate_a / rate_b
    if count_a <= 0:
        return {"rate_a": 0.0, "rate_b": rate_b, "rate_ratio": 0.0,
                "ci_lower": 0.0, "ci_upper": None}
    # Wald CI on log scale
    se_log = math.sqrt(1.0 / max(count_a, 0.5) + 1.0 / max(count_b, 0.5))
    log_rr = math.log(rr)
    z = 1.96
    ci_lower = math.exp(log_rr - z * se_log)
    ci_upper = math.exp(log_rr + z * se_log)
    return {"rate_a": rate_a, "rate_b": rate_b, "rate_ratio": rr,
            "ci_lower": ci_lower, "ci_upper": ci_upper}


# ---------------------------------------------------------------------------
# 11. Odds ratio
# ---------------------------------------------------------------------------


def odds_ratio(a, b, c, d):
    """Odds ratio from a 2x2 table with Woolf logit CI.

    Layout: [[a, b], [c, d]]
    OR = (a*d) / (b*c)

    Parameters
    ----------
    a, b, c, d : int/float
        Cell counts (with 0.5 continuity correction if any zero).

    Returns
    -------
    dict with keys: odds_ratio, ci_lower, ci_upper, log_or, se_log_or
    """
    # Continuity correction
    if any(v == 0 for v in [a, b, c, d]):
        a, b, c, d = a + 0.5, b + 0.5, c + 0.5, d + 0.5
    if b * c == 0:
        return {"odds_ratio": float('inf'), "ci_lower": None, "ci_upper": None,
                "log_or": None, "se_log_or": None}
    or_val = (a * d) / (b * c)
    log_or = math.log(or_val) if or_val > 0 else None
    se = math.sqrt(1.0 / a + 1.0 / b + 1.0 / c + 1.0 / d)
    z = 1.96
    if log_or is not None:
        ci_lower = math.exp(log_or - z * se)
        ci_upper = math.exp(log_or + z * se)
    else:
        ci_lower = ci_upper = None
    return {"odds_ratio": or_val, "ci_lower": ci_lower, "ci_upper": ci_upper,
            "log_or": log_or, "se_log_or": se}


# ---------------------------------------------------------------------------
# 12. Chi-squared test
# ---------------------------------------------------------------------------


def chi_squared_test(observed, expected):
    """Chi-squared goodness-of-fit test with Wilson-Hilferty p-value.

    Parameters
    ----------
    observed, expected : list of float
        Same-length vectors.

    Returns
    -------
    dict with keys: chi2, df, p_value
    """
    if not observed or not expected or len(observed) != len(expected):
        return {"chi2": None, "df": None, "p_value": None}
    k = len(observed)
    chi2 = 0.0
    for o, e in zip(observed, expected):
        if e <= 0:
            continue
        chi2 += (o - e) ** 2 / e
    df = k - 1
    if df <= 0:
        return {"chi2": chi2, "df": 0, "p_value": 1.0}
    p_value = 1.0 - _chi2_cdf(chi2, df)
    return {"chi2": chi2, "df": df, "p_value": max(0.0, p_value)}


# ---------------------------------------------------------------------------
# 13. Permutation test
# ---------------------------------------------------------------------------


def permutation_test(group_a, group_b, stat_fn=None, n_perm=10000, seed=42):
    """Two-sample permutation test (two-sided).

    Parameters
    ----------
    group_a, group_b : list of float
        Two independent samples.
    stat_fn : callable, optional
        Test statistic function(a, b); defaults to difference in means.
    n_perm : int
        Number of permutations.
    seed : int
        Random seed.

    Returns
    -------
    dict with keys: observed_stat, p_value, n_perm
    """
    if not group_a or not group_b:
        return {"observed_stat": None, "p_value": None, "n_perm": 0}

    if stat_fn is None:
        stat_fn = lambda a, b: _mean(a) - _mean(b)

    rng = random.Random(seed)
    observed = stat_fn(group_a, group_b)
    combined = group_a + group_b
    na = len(group_a)
    count = 0
    for _ in range(n_perm):
        rng.shuffle(combined)
        perm_a = combined[:na]
        perm_b = combined[na:]
        perm_stat = stat_fn(perm_a, perm_b)
        if abs(perm_stat) >= abs(observed):
            count += 1
    p_value = count / n_perm
    return {"observed_stat": observed, "p_value": p_value, "n_perm": n_perm}


# ---------------------------------------------------------------------------
# 14. Poisson rate with Garwood CI
# ---------------------------------------------------------------------------


def poisson_rate(count, exposure, ci=True):
    """Poisson rate with exact Garwood confidence interval.

    Uses chi-squared quantiles (Wilson-Hilferty) for CI bounds.

    Parameters
    ----------
    count : int
        Observed event count.
    exposure : float
        Person-time or denominator.
    ci : bool
        Whether to compute CI.

    Returns
    -------
    dict with keys: rate, ci_lower, ci_upper, count, exposure
    """
    if exposure <= 0:
        return {"rate": None, "ci_lower": None, "ci_upper": None,
                "count": count, "exposure": exposure}
    rate = count / exposure
    if not ci:
        return {"rate": rate, "ci_lower": None, "ci_upper": None,
                "count": count, "exposure": exposure}

    alpha = 0.05
    # Lower: chi2(alpha/2, 2*count) / (2*exposure)
    if count == 0:
        ci_lower = 0.0
    else:
        ci_lower = _chi2_ppf(alpha / 2, 2 * count) / (2 * exposure)

    # Upper: chi2(1-alpha/2, 2*(count+1)) / (2*exposure)
    ci_upper = _chi2_ppf(1 - alpha / 2, 2 * (count + 1)) / (2 * exposure)

    return {"rate": rate, "ci_lower": ci_lower, "ci_upper": ci_upper,
            "count": count, "exposure": exposure}


# ---------------------------------------------------------------------------
# 15. Moran's I
# ---------------------------------------------------------------------------


def morans_i(values, weights_matrix):
    """Moran's I spatial autocorrelation statistic.

    Parameters
    ----------
    values : list of float
        Observed values at n locations.
    weights_matrix : list of list of float
        n x n spatial weights matrix.

    Returns
    -------
    dict with keys: morans_i, expected_i, z_score, p_value
    """
    n = len(values) if values else 0
    if n < 2 or len(weights_matrix) != n:
        return {"morans_i": None, "expected_i": None, "z_score": None, "p_value": None}

    mu = _mean(values)
    dev = [v - mu for v in values]
    denom = sum(d * d for d in dev)
    if denom == 0:
        return {"morans_i": 0.0, "expected_i": -1.0 / (n - 1),
                "z_score": 0.0, "p_value": 1.0}

    w_sum = 0.0
    numerator = 0.0
    for i in range(n):
        row = weights_matrix[i]
        if len(row) != n:
            return {"morans_i": None, "expected_i": None, "z_score": None, "p_value": None}
        for j in range(n):
            w = row[j]
            w_sum += w
            numerator += w * dev[i] * dev[j]

    if w_sum == 0:
        return {"morans_i": 0.0, "expected_i": -1.0 / (n - 1),
                "z_score": 0.0, "p_value": 1.0}

    I = (n / w_sum) * (numerator / denom)
    expected = -1.0 / (n - 1)

    # Variance under normality assumption (simplified)
    s1 = 0.0
    s2 = 0.0
    for i in range(n):
        row_sum = sum(weights_matrix[i])
        col_sum = sum(weights_matrix[j][i] for j in range(n))
        s2 += (row_sum + col_sum) ** 2
        for j in range(n):
            s1 += (weights_matrix[i][j] + weights_matrix[j][i]) ** 2
    s1 *= 0.5

    n2 = n * n
    w2 = w_sum * w_sum
    var_I = (n2 * s1 - n * s2 + 3 * w2) / (w2 * (n2 - 1)) - expected ** 2
    if var_I <= 0:
        var_I = 1e-10

    z_score = (I - expected) / math.sqrt(var_I)
    p_value = 2 * (1 - _normal_cdf(abs(z_score)))

    return {"morans_i": I, "expected_i": expected, "z_score": z_score, "p_value": p_value}


# ---------------------------------------------------------------------------
# 16. Bayesian rate (Beta-Binomial)
# ---------------------------------------------------------------------------


def bayesian_rate(successes, trials, prior_alpha=1, prior_beta=1):
    """Beta-Binomial conjugate posterior for a rate.

    Parameters
    ----------
    successes : int
        Number of successes.
    trials : int
        Number of trials.
    prior_alpha, prior_beta : float
        Beta prior hyperparameters (default: uniform).

    Returns
    -------
    dict with keys: posterior_mean, posterior_mode, ci_lower, ci_upper,
                    posterior_alpha, posterior_beta
    """
    if trials < 0 or successes < 0:
        return {"posterior_mean": None, "posterior_mode": None,
                "ci_lower": None, "ci_upper": None,
                "posterior_alpha": None, "posterior_beta": None}
    a = prior_alpha + successes
    b = prior_beta + (trials - successes)
    post_mean = a / (a + b) if (a + b) > 0 else 0.0
    post_mode = (a - 1) / (a + b - 2) if (a + b) > 2 and a >= 1 and b >= 1 else post_mean

    # Approximate CI using normal approximation to Beta
    var = (a * b) / ((a + b) ** 2 * (a + b + 1))
    sd = math.sqrt(var) if var > 0 else 0.0
    ci_lower = max(0.0, post_mean - 1.96 * sd)
    ci_upper = min(1.0, post_mean + 1.96 * sd)

    return {
        "posterior_mean": post_mean,
        "posterior_mode": max(0.0, min(1.0, post_mode)),
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "posterior_alpha": a,
        "posterior_beta": b,
    }


# ---------------------------------------------------------------------------
# 17. Interrupted time series
# ---------------------------------------------------------------------------


def interrupted_time_series(pre_values, post_values):
    """Interrupted time series analysis (level + slope change).

    Fits OLS segments to pre and post periods and reports the
    immediate level change and the slope change.

    Parameters
    ----------
    pre_values : list of float
        Outcome values in pre-intervention period.
    post_values : list of float
        Outcome values in post-intervention period.

    Returns
    -------
    dict with keys: level_change, slope_change, pre_slope, post_slope,
                    pre_intercept, post_intercept
    """
    if not pre_values or not post_values:
        return {"level_change": None, "slope_change": None,
                "pre_slope": None, "post_slope": None,
                "pre_intercept": None, "post_intercept": None}

    def _fit_line(vals):
        n = len(vals)
        if n < 2:
            return vals[0] if vals else 0.0, 0.0
        x = list(range(n))
        mx = _mean(x)
        my = _mean(vals)
        num = sum((xi - mx) * (yi - my) for xi, yi in zip(x, vals))
        den = sum((xi - mx) ** 2 for xi in x)
        slope = num / den if den > 0 else 0.0
        intercept = my - slope * mx
        return intercept, slope

    pre_int, pre_slope = _fit_line(pre_values)
    post_int, post_slope = _fit_line(post_values)

    # Predicted value at the last pre-period time point
    t_break = len(pre_values) - 1
    predicted_end_pre = pre_int + pre_slope * t_break
    # Predicted value at first post-period time point (t=0 of post)
    predicted_start_post = post_int

    level_change = predicted_start_post - predicted_end_pre
    slope_change = post_slope - pre_slope

    return {
        "level_change": level_change,
        "slope_change": slope_change,
        "pre_slope": pre_slope,
        "post_slope": post_slope,
        "pre_intercept": pre_int,
        "post_intercept": post_int,
    }


# ---------------------------------------------------------------------------
# 18. Changepoint detection (CUSUM)
# ---------------------------------------------------------------------------


def changepoint_detection(values, min_segment=3):
    """Changepoint detection via max cumulative sum (CUSUM) deviation.

    Parameters
    ----------
    values : list of float
        Time series values.
    min_segment : int
        Minimum segment length on each side.

    Returns
    -------
    dict with keys: changepoint_index, max_stat, mean_before, mean_after
    """
    n = len(values) if values else 0
    if n < 2 * min_segment:
        return {"changepoint_index": None, "max_stat": 0.0,
                "mean_before": None, "mean_after": None}

    total = sum(values)
    overall_mean = total / n
    # CUSUM: S_k = sum_{i=0}^{k-1} (x_i - mean)
    cusum = [0.0]
    s = 0.0
    for v in values:
        s += v - overall_mean
        cusum.append(s)

    best_stat = -1.0
    best_idx = min_segment
    for k in range(min_segment, n - min_segment + 1):
        stat = abs(cusum[k])
        if stat > best_stat:
            best_stat = stat
            best_idx = k

    mean_before = _mean(values[:best_idx])
    mean_after = _mean(values[best_idx:])

    return {
        "changepoint_index": best_idx,
        "max_stat": best_stat,
        "mean_before": mean_before,
        "mean_after": mean_after,
    }


# ---------------------------------------------------------------------------
# 19. Power-law fit (MLE + KS)
# ---------------------------------------------------------------------------


def power_law_fit(values):
    """MLE power-law exponent with KS goodness-of-fit statistic.

    Fits P(x) ~ x^(-alpha) for continuous values >= x_min.

    Parameters
    ----------
    values : list of float
        Positive values.

    Returns
    -------
    dict with keys: alpha, x_min, ks_statistic, n
    """
    pos = sorted(v for v in (values or []) if v > 0)
    n = len(pos)
    if n < 3:
        return {"alpha": None, "x_min": None, "ks_statistic": None, "n": n}

    x_min = pos[0]
    if x_min <= 0:
        x_min = 1e-10

    # MLE: alpha = 1 + n / sum(ln(x_i / x_min))
    log_sum = sum(math.log(v / x_min) for v in pos if v >= x_min)
    if log_sum <= 0:
        return {"alpha": None, "x_min": x_min, "ks_statistic": None, "n": n}
    alpha = 1.0 + n / log_sum

    # KS statistic: max |F_empirical - F_theoretical|
    tail = [v for v in pos if v >= x_min]
    nt = len(tail)
    if nt == 0:
        return {"alpha": alpha, "x_min": x_min, "ks_statistic": None, "n": n}
    ks = 0.0
    for i, v in enumerate(tail):
        f_emp = (i + 1) / nt
        f_theo = 1.0 - (x_min / v) ** (alpha - 1)
        ks = max(ks, abs(f_emp - f_theo))

    return {"alpha": alpha, "x_min": x_min, "ks_statistic": ks, "n": n}


# ---------------------------------------------------------------------------
# 20. Concentration index
# ---------------------------------------------------------------------------


def concentration_index(values):
    """Health-specific concentration index (Kakwani).

    Measures income-related inequality in health.
    Values should be sorted by socioeconomic rank.

    Parameters
    ----------
    values : list of float
        Health variable sorted by socioeconomic rank (poorest to richest).

    Returns
    -------
    dict with keys: concentration_index, n
    """
    if not values or len(values) < 2:
        return {"concentration_index": 0.0, "n": len(values) if values else 0}

    n = len(values)
    mu = _mean(values)
    if mu == 0:
        return {"concentration_index": 0.0, "n": n}

    # C = (2 / (n * mu)) * sum_i( (R_i - 0.5) * y_i ) - 1   [wrong]
    # Actually: C = (2 / (n * mu)) * sum( y_i * R_i ) - 1
    # where R_i = (i + 0.5) / n is the fractional rank
    ci_val = 0.0
    for i, v in enumerate(values):
        r_i = (i + 0.5) / n
        ci_val += v * r_i
    ci_val = (2.0 / (n * mu)) * ci_val - 1.0

    return {"concentration_index": ci_val, "n": n}


# ---------------------------------------------------------------------------
# 21. Kaplan-Meier
# ---------------------------------------------------------------------------


def kaplan_meier(event_times, censored=None):
    """Kaplan-Meier survival estimates.

    Parameters
    ----------
    event_times : list of float
        Observed times.
    censored : list of bool, optional
        True if censored at that time. Default: all events (no censoring).

    Returns
    -------
    dict with keys: survival_table (list of dicts with time, n_risk, n_event,
                    n_censor, survival), median_survival
    """
    if not event_times:
        return {"survival_table": [], "median_survival": None}

    n = len(event_times)
    if censored is None:
        censored = [False] * n

    # Build event table
    events = sorted(zip(event_times, censored), key=lambda x: x[0])
    # Group by unique times
    unique_times = {}
    for t, c in events:
        if t not in unique_times:
            unique_times[t] = {"n_event": 0, "n_censor": 0}
        if c:
            unique_times[t]["n_censor"] += 1
        else:
            unique_times[t]["n_event"] += 1

    table = []
    n_risk = n
    survival = 1.0
    median = None

    for t in sorted(unique_times.keys()):
        info = unique_times[t]
        d = info["n_event"]
        c = info["n_censor"]
        if n_risk > 0 and d > 0:
            survival *= (1.0 - d / n_risk)
        table.append({
            "time": t,
            "n_risk": n_risk,
            "n_event": d,
            "n_censor": c,
            "survival": survival,
        })
        if median is None and survival <= 0.5:
            median = t
        n_risk -= (d + c)

    return {"survival_table": table, "median_survival": median}


# ---------------------------------------------------------------------------
# 22. Spearman correlation
# ---------------------------------------------------------------------------


def spearman_correlation(x, y):
    """Spearman rank correlation with t-statistic and p-value.

    Parameters
    ----------
    x, y : list of float
        Paired observations (same length).

    Returns
    -------
    dict with keys: rho, t_statistic, p_value, n
    """
    if not x or not y or len(x) != len(y):
        return {"rho": None, "t_statistic": None, "p_value": None, "n": 0}
    n = len(x)
    if n < 3:
        return {"rho": None, "t_statistic": None, "p_value": None, "n": n}

    rx = _rank(x)
    ry = _rank(y)

    # Pearson r on ranks
    mx = _mean(rx)
    my = _mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den_x = math.sqrt(sum((a - mx) ** 2 for a in rx))
    den_y = math.sqrt(sum((b - my) ** 2 for b in ry))
    if den_x == 0 or den_y == 0:
        return {"rho": 0.0, "t_statistic": 0.0, "p_value": 1.0, "n": n}

    rho = num / (den_x * den_y)
    rho = max(-1.0, min(1.0, rho))

    # t-statistic
    if abs(rho) >= 1.0:
        t_stat = float('inf') if rho > 0 else float('-inf')
        p_val = 0.0
    else:
        t_stat = rho * math.sqrt((n - 2) / (1 - rho ** 2))
        p_val = 2 * (1 - _t_cdf(abs(t_stat), n - 2))

    return {"rho": rho, "t_statistic": t_stat, "p_value": p_val, "n": n}


# ---------------------------------------------------------------------------
# 23. Linear regression
# ---------------------------------------------------------------------------


def linear_regression(x, y):
    """Simple ordinary least-squares linear regression.

    Parameters
    ----------
    x, y : list of float
        Predictor and outcome (same length).

    Returns
    -------
    dict with keys: slope, intercept, r_squared, se_slope, se_intercept, n
    """
    if not x or not y or len(x) != len(y):
        return {"slope": None, "intercept": None, "r_squared": None,
                "se_slope": None, "se_intercept": None, "n": 0}
    n = len(x)
    if n < 2:
        return {"slope": 0.0, "intercept": y[0] if y else 0.0, "r_squared": None,
                "se_slope": None, "se_intercept": None, "n": n}

    mx = _mean(x)
    my = _mean(y)
    ss_xx = sum((xi - mx) ** 2 for xi in x)
    ss_xy = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    ss_yy = sum((yi - my) ** 2 for yi in y)

    if ss_xx == 0:
        return {"slope": 0.0, "intercept": my, "r_squared": 0.0,
                "se_slope": None, "se_intercept": None, "n": n}

    slope = ss_xy / ss_xx
    intercept = my - slope * mx
    r_squared = (ss_xy ** 2) / (ss_xx * ss_yy) if ss_yy > 0 else 0.0

    # Standard errors
    residuals = [yi - (slope * xi + intercept) for xi, yi in zip(x, y)]
    mse = sum(r ** 2 for r in residuals) / (n - 2) if n > 2 else 0.0
    se_slope = math.sqrt(mse / ss_xx) if mse > 0 and ss_xx > 0 else 0.0
    se_intercept = math.sqrt(mse * (1.0 / n + mx ** 2 / ss_xx)) if mse > 0 else 0.0

    return {
        "slope": slope,
        "intercept": intercept,
        "r_squared": r_squared,
        "se_slope": se_slope,
        "se_intercept": se_intercept,
        "n": n,
    }


# ---------------------------------------------------------------------------
# 24. Cohen's d
# ---------------------------------------------------------------------------


def effect_size_cohens_d(mean1, sd1, n1, mean2, sd2, n2):
    """Cohen's d (pooled SD) with 95% confidence interval.

    Parameters
    ----------
    mean1, sd1, n1 : float
        Group 1 statistics.
    mean2, sd2, n2 : float
        Group 2 statistics.

    Returns
    -------
    dict with keys: cohens_d, ci_lower, ci_upper, pooled_sd, se
    """
    if n1 <= 0 or n2 <= 0:
        return {"cohens_d": None, "ci_lower": None, "ci_upper": None,
                "pooled_sd": None, "se": None}

    # Pooled SD
    if n1 + n2 - 2 <= 0:
        pooled_sd = 0.0
    else:
        pooled_var = ((n1 - 1) * sd1 ** 2 + (n2 - 1) * sd2 ** 2) / (n1 + n2 - 2)
        pooled_sd = math.sqrt(max(0.0, pooled_var))

    if pooled_sd == 0:
        d = 0.0
    else:
        d = (mean1 - mean2) / pooled_sd

    # SE of Cohen's d
    se = math.sqrt((n1 + n2) / (n1 * n2) + d ** 2 / (2 * (n1 + n2)))
    ci_lower = d - 1.96 * se
    ci_upper = d + 1.96 * se

    return {
        "cohens_d": d,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "pooled_sd": pooled_sd,
        "se": se,
    }


# ---------------------------------------------------------------------------
# 25. Network centrality
# ---------------------------------------------------------------------------


def network_centrality(adjacency):
    """Degree centrality from an adjacency matrix.

    Parameters
    ----------
    adjacency : list of list of float/int
        n x n adjacency matrix (0 or 1, or weighted).

    Returns
    -------
    dict with keys: degree_centrality (list), max_node, max_centrality, n
    """
    if not adjacency:
        return {"degree_centrality": [], "max_node": None, "max_centrality": 0.0, "n": 0}
    n = len(adjacency)
    if n < 2:
        return {"degree_centrality": [0.0], "max_node": 0, "max_centrality": 0.0, "n": 1}

    centrality = []
    for i in range(n):
        row = adjacency[i] if i < len(adjacency) else []
        degree = sum(1 for j, v in enumerate(row) if j != i and v > 0)
        centrality.append(degree / (n - 1))

    max_c = max(centrality)
    max_node = centrality.index(max_c)

    return {
        "degree_centrality": centrality,
        "max_node": max_node,
        "max_centrality": max_c,
        "n": n,
    }


# ---------------------------------------------------------------------------
# 26. Jaccard similarity
# ---------------------------------------------------------------------------


def jaccard_similarity(set_a, set_b):
    """Jaccard coefficient |A intersect B| / |A union B|.

    Parameters
    ----------
    set_a, set_b : set or list
        Two collections.

    Returns
    -------
    dict with keys: jaccard, intersection_size, union_size
    """
    a = set(set_a) if set_a else set()
    b = set(set_b) if set_b else set()
    intersection = a & b
    union = a | b
    if not union:
        return {"jaccard": 0.0, "intersection_size": 0, "union_size": 0}
    return {
        "jaccard": len(intersection) / len(union),
        "intersection_size": len(intersection),
        "union_size": len(union),
    }


# ---------------------------------------------------------------------------
# 27. Mutual information
# ---------------------------------------------------------------------------


def mutual_information(x_values, y_values, n_bins=10):
    """Binned mutual information estimate.

    Parameters
    ----------
    x_values, y_values : list of float
        Paired observations.
    n_bins : int
        Number of histogram bins per dimension.

    Returns
    -------
    dict with keys: mutual_information, normalized_mi, n
    """
    if not x_values or not y_values or len(x_values) != len(y_values):
        return {"mutual_information": None, "normalized_mi": None, "n": 0}

    n = len(x_values)
    if n < 4:
        return {"mutual_information": 0.0, "normalized_mi": 0.0, "n": n}

    # Bin edges
    def _bin_idx(v, vmin, vmax, nb):
        if vmax == vmin:
            return 0
        idx = int((v - vmin) / (vmax - vmin) * nb)
        return min(idx, nb - 1)

    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = min(y_values), max(y_values)

    # Joint + marginal counts
    joint = {}
    x_counts = {}
    y_counts = {}
    for xv, yv in zip(x_values, y_values):
        xi = _bin_idx(xv, x_min, x_max, n_bins)
        yi = _bin_idx(yv, y_min, y_max, n_bins)
        joint[(xi, yi)] = joint.get((xi, yi), 0) + 1
        x_counts[xi] = x_counts.get(xi, 0) + 1
        y_counts[yi] = y_counts.get(yi, 0) + 1

    mi = 0.0
    for (xi, yi), c_xy in joint.items():
        p_xy = c_xy / n
        p_x = x_counts[xi] / n
        p_y = y_counts[yi] / n
        if p_xy > 0 and p_x > 0 and p_y > 0:
            mi += p_xy * math.log2(p_xy / (p_x * p_y))

    # Marginal entropies for normalization
    hx = -sum((c / n) * math.log2(c / n) for c in x_counts.values() if c > 0)
    hy = -sum((c / n) * math.log2(c / n) for c in y_counts.values() if c > 0)
    h_min = min(hx, hy)
    nmi = mi / h_min if h_min > 0 else 0.0

    return {"mutual_information": mi, "normalized_mi": nmi, "n": n}


# ---------------------------------------------------------------------------
# 28. Zero-inflated Poisson (EM)
# ---------------------------------------------------------------------------


def zero_inflated_poisson_em(values, max_iter=100):
    """Zero-inflated Poisson model fit via EM algorithm.

    Parameters
    ----------
    values : list of int/float
        Non-negative count data.
    max_iter : int
        Maximum EM iterations.

    Returns
    -------
    dict with keys: pi (zero-inflation), lambda_ (Poisson rate),
                    n_iter, log_likelihood, n_zeros, n
    """
    if not values:
        return {"pi": None, "lambda_": None, "n_iter": 0,
                "log_likelihood": None, "n_zeros": 0, "n": 0}

    vals = [max(0, v) for v in values]
    n = len(vals)
    n_zeros = sum(1 for v in vals if v == 0)

    if n_zeros == n:
        return {"pi": 1.0, "lambda_": 0.0, "n_iter": 0,
                "log_likelihood": 0.0, "n_zeros": n_zeros, "n": n}

    total = sum(vals)
    if n_zeros == 0:
        lam = total / n
        return {"pi": 0.0, "lambda_": lam, "n_iter": 0,
                "log_likelihood": None, "n_zeros": 0, "n": n}

    # Initialize
    pi = n_zeros / n * 0.5
    lam = total / n

    for iteration in range(max_iter):
        # E-step: posterior prob that zero observation came from zero component
        exp_neg_lam = math.exp(-lam) if lam < 700 else 0.0
        z_probs = []
        for v in vals:
            if v == 0:
                num = pi
                den = pi + (1 - pi) * exp_neg_lam
                z_probs.append(num / den if den > 0 else 0.5)
            else:
                z_probs.append(0.0)

        # M-step
        sum_z = sum(z_probs)
        pi_new = sum_z / n
        den_lam = sum(1.0 - z for z in z_probs)
        if den_lam > 0:
            lam_new = sum((1.0 - z) * v for z, v in zip(z_probs, vals)) / den_lam
        else:
            lam_new = lam

        # Convergence check
        if abs(pi_new - pi) < 1e-8 and abs(lam_new - lam) < 1e-8:
            pi, lam = pi_new, lam_new
            break
        pi, lam = pi_new, lam_new

    # Log-likelihood
    ll = 0.0
    exp_neg_lam = math.exp(-lam) if lam < 700 else 0.0
    for v in vals:
        if v == 0:
            p = pi + (1 - pi) * exp_neg_lam
        else:
            # Poisson PMF: e^(-lam) * lam^v / v!
            log_pmf = -lam + v * math.log(max(lam, 1e-300)) - _gamma_ln(v + 1)
            p = (1 - pi) * math.exp(log_pmf)
        ll += math.log(max(p, 1e-300))

    return {
        "pi": pi,
        "lambda_": lam,
        "n_iter": iteration + 1 if 'iteration' in dir() else max_iter,
        "log_likelihood": ll,
        "n_zeros": n_zeros,
        "n": n,
    }


# ---------------------------------------------------------------------------
# 29. Logistic growth fit
# ---------------------------------------------------------------------------


def logistic_growth_fit(x, y):
    """Fit logistic growth curve y = L / (1 + exp(-k*(x - x0))).

    Uses iterative grid-search refinement (no scipy).

    Parameters
    ----------
    x, y : list of float
        Independent and dependent variables.

    Returns
    -------
    dict with keys: L (carrying capacity), k (growth rate), x0 (midpoint),
                    r_squared, n
    """
    if not x or not y or len(x) != len(y):
        return {"L": None, "k": None, "x0": None, "r_squared": None, "n": 0}

    n = len(x)
    if n < 3:
        return {"L": max(y) if y else 0.0, "k": 0.0, "x0": _mean(x),
                "r_squared": None, "n": n}

    y_max = max(y)
    y_min = min(y)
    x_min = min(x)
    x_max = max(x)

    if y_max == y_min:
        return {"L": y_max, "k": 0.0, "x0": _mean(x), "r_squared": 1.0, "n": n}

    def _logistic(xi, L, k, x0):
        z = -k * (xi - x0)
        z = max(-500, min(500, z))
        return L / (1.0 + math.exp(z))

    def _sse(L, k, x0):
        return sum((yi - _logistic(xi, L, k, x0)) ** 2 for xi, yi in zip(x, y))

    ss_tot = sum((yi - _mean(y)) ** 2 for yi in y)

    # Grid search with refinement
    best_sse = float('inf')
    best_params = (y_max, 1.0, _mean(x))

    for _round in range(4):
        if _round == 0:
            L_range = [y_max * f for f in [0.8, 1.0, 1.2, 1.5, 2.0]]
            k_range = [0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0]
            x0_range = [x_min + (x_max - x_min) * f for f in [0.0, 0.25, 0.5, 0.75, 1.0]]
        else:
            L_c, k_c, x0_c = best_params
            dL = max(abs(L_c) * 0.3, 0.1) / (2 ** _round)
            dk = max(abs(k_c) * 0.3, 0.01) / (2 ** _round)
            dx0 = max(abs(x0_c) * 0.3, 0.1) / (2 ** _round)
            L_range = [L_c + dL * i for i in range(-3, 4)]
            k_range = [k_c + dk * i for i in range(-3, 4)]
            x0_range = [x0_c + dx0 * i for i in range(-3, 4)]

        for L in L_range:
            if L <= 0:
                continue
            for k in k_range:
                if k <= 0:
                    continue
                for x0 in x0_range:
                    sse = _sse(L, k, x0)
                    if sse < best_sse:
                        best_sse = sse
                        best_params = (L, k, x0)

    L_best, k_best, x0_best = best_params
    r_squared = 1.0 - best_sse / ss_tot if ss_tot > 0 else 0.0

    return {
        "L": L_best,
        "k": k_best,
        "x0": x0_best,
        "r_squared": max(0.0, r_squared),
        "n": n,
    }


# ---------------------------------------------------------------------------
# 30. ARIMA(1,1,0) forecast
# ---------------------------------------------------------------------------


def arima_forecast(values, steps=3):
    """Simple ARIMA(1,1,0) forecast.

    Differences the series once, fits AR(1) on differences,
    then forecasts *steps* ahead.

    Parameters
    ----------
    values : list of float
        Time series values (at least 4 observations).
    steps : int
        Number of steps to forecast.

    Returns
    -------
    dict with keys: forecast (list), phi (AR coefficient),
                    mean_diff, last_value, n
    """
    if not values or len(values) < 4:
        return {"forecast": [], "phi": None, "mean_diff": None,
                "last_value": values[-1] if values else None, "n": len(values) if values else 0}

    n = len(values)
    # First difference
    diffs = [values[i] - values[i - 1] for i in range(1, n)]
    nd = len(diffs)
    mu_d = _mean(diffs)

    # AR(1) on centred differences: (d_t - mu) = phi * (d_{t-1} - mu) + e
    centered = [d - mu_d for d in diffs]
    if nd < 3:
        phi = 0.0
    else:
        num = sum(centered[i] * centered[i - 1] for i in range(1, nd))
        den = sum(centered[i - 1] ** 2 for i in range(1, nd))
        phi = num / den if den > 0 else 0.0
        phi = max(-0.99, min(0.99, phi))  # stationarity constraint

    # Forecast
    last_val = values[-1]
    last_centered = centered[-1] if centered else 0.0
    forecasts = []
    for _ in range(steps):
        next_centered = phi * last_centered
        next_diff = next_centered + mu_d
        next_val = last_val + next_diff
        forecasts.append(next_val)
        last_val = next_val
        last_centered = next_centered

    return {
        "forecast": forecasts,
        "phi": phi,
        "mean_diff": mu_d,
        "last_value": values[-1],
        "n": n,
    }


# ---------------------------------------------------------------------------
# 31. Benford's law test
# ---------------------------------------------------------------------------


def benford_test(values):
    """Benford's law adherence test (chi-squared on first digits).

    Parameters
    ----------
    values : list of float/int
        Numerical values (absolute values used, zeros skipped).

    Returns
    -------
    dict with keys: chi2, p_value, digit_counts (dict), expected_freqs (dict),
                    n_valid, mad (mean absolute deviation from Benford)
    """
    if not values:
        return {"chi2": None, "p_value": None, "digit_counts": {},
                "expected_freqs": {}, "n_valid": 0, "mad": None}

    # Benford expected proportions: P(d) = log10(1 + 1/d)
    benford_probs = {d: math.log10(1 + 1 / d) for d in range(1, 10)}

    # Extract first digits
    digit_counts = {d: 0 for d in range(1, 10)}
    for v in values:
        av = abs(v)
        if av == 0:
            continue
        s = f"{av:.10e}"  # scientific notation
        first = s[0]
        if first == '-':
            first = s[1]
        if first.isdigit() and int(first) >= 1:
            digit_counts[int(first)] += 1

    n_valid = sum(digit_counts.values())
    if n_valid == 0:
        return {"chi2": None, "p_value": None, "digit_counts": digit_counts,
                "expected_freqs": {d: round(p, 4) for d, p in benford_probs.items()},
                "n_valid": 0, "mad": None}

    observed = [digit_counts[d] for d in range(1, 10)]
    expected = [benford_probs[d] * n_valid for d in range(1, 10)]

    result = chi_squared_test(observed, expected)

    # MAD (Nigrini's statistic)
    mad = sum(abs(digit_counts[d] / n_valid - benford_probs[d]) for d in range(1, 10)) / 9

    return {
        "chi2": result["chi2"],
        "p_value": result["p_value"],
        "digit_counts": digit_counts,
        "expected_freqs": {d: round(p, 4) for d, p in benford_probs.items()},
        "n_valid": n_valid,
        "mad": mad,
    }
