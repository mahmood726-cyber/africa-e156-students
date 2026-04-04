# Multi-Persona Review: Africa E156 Student Platform
### Date: 2026-04-04
### Status: REVIEW CLEAN (all P0 and P1 fixed)
### Summary: 13 P0, 24 P1, 27 P2

---

## P0 — Critical (must fix)

### Statistical Methodologist
- **P0-STAT-1** [FIXED] Kendall tau-b mislabeled — is actually tau-a (no tie correction). With many tied zeros, materially wrong. (`advanced_statistics.py:154-163`) Fix: rename to tau-a or implement tau-b.
- **P0-STAT-2** [FIXED] Atkinson index wrong when zeros present: epsilon>=1 should return 1.0 (max inequality) but code computes non-trivial ratio using only positives. (`advanced_statistics.py:111-118`) Fix: return 1.0 when any value is 0 and epsilon>=1.
- **P0-STAT-3** [FIXED] Cramer's rule quadratic regression: Da uses `sx2**2` where `sx3**2` is correct; Dc determinant formula has wrong terms. (`statistical_deep_dive.py:298-303`) Fix: correct the 3x3 determinant expansions.

### Security Auditor
- (No P0 found — all data is developer-controlled, no user input at runtime)

### UX/Accessibility
- **P0-UX-1** [FIXED] No semantic landmarks (`<main>`, `<header>`, `<footer>`) — all files are div soup. Blocks screen reader navigation. (all HTML files)
- **P0-UX-2** [FIXED] Zero `:focus` styles — keyboard users have no visual indicator. (all CSS)
- **P0-UX-3** [FIXED] All SVG charts invisible to screen readers — no `role="img"`, no `aria-label`, no `<title>`. (all dashboards, 640 SVGs)
- **P0-UX-4** [FIXED] Color-only information in sentence strips — color-blind users cannot distinguish roles. (health-disease/index.html, all dashboards)
- **P0-UX-5** [FIXED] `onclick` with `href="#"` on Download Paper buttons — not keyboard-accessible, jumps to top if JS fails. (all group pages, 80 instances)

### Software Engineer
- **P0-ENG-1** [FIXED] Duplicate ISO code "CD" for Chad (should be "TD") and DRC — data collision. (`fetch_africa_rcts_by_country.py:54,57`)
- **P0-ENG-2** [FIXED] `patch_dashboards.py` crashes if JSON files missing — no guard at module-level load. (lines 26-29)

### Domain Expert
- **P0-DOM-1** [FIXED] Dashboard shows TWO contradictory heart failure numbers (41/1,855/45x in hero vs 167/2,499/15x in body text from real data). (`heart-failure-africa.html`) Fix: align all numbers to source data.
- **P0-DOM-2** [FIXED] `placebo-ethics` paper claims Africa's placebo rate "exceeded" US rate — data shows opposite (13.9% < 17.8%). (`rewrite_all_papers.py:181`) Fix: correct the comparison direction.
- **P0-DOM-3** [FIXED] `masking-depth` paper claims Africa's double-blind rate "exceeded" US — data shows opposite (10.3% < 11.2%). (`rewrite_all_papers.py:250`)
- **P0-DOM-4** [FIXED] `angle-13_rural-reach-coefficients` claims "thirty-fold gap" but ratio is 4.25x. (`rewrite_all_papers.py:81`)

---

## P1 — Important (should fix)

### Statistical Methodologist
- **P1-STAT-1** [FIXED] Theil L (GE(0)) understated with zeros — skips infinite contributions, divides by full n. (`advanced_statistics.py:96-101`)
- **P1-STAT-2** [FIXED] KL divergence computed on mismatched vectors (filtered vs full). (`advanced_statistics.py:375`)
- **P1-STAT-3** [FIXED] Jackknife SE uses theta_full instead of theta_bar (biased). (`advanced_statistics.py:261`)
- **P1-STAT-4** [FIXED] Power-law MLE uses continuous formula for discrete data (~5-10% bias). (`advanced_statistics.py:228`)
- **P1-STAT-5** [FIXED] Descriptive stats use population variance (n) not sample (n-1) — undocumented. (`statistical_deep_dive.py:108,120`)
- **P1-STAT-6** [FIXED] Quartile computation uses nearest-rank, not interpolation. (`statistical_deep_dive.py:122-123`)
- **P1-STAT-7** [FIXED] Concentration index formula may be off by a constant factor. (`advanced_statistics.py:312-321`)
- **P1-STAT-8** [FIXED] Hardcoded Gini=0.857 in papers may be stale if data changes. (`rewrite_all_papers.py:58`)
- **P1-STAT-9** [FIXED] Multiple hardcoded stats in papers (MAD=0.030, H/Hmax=0.49, HHI=0.315). (various lines)

### UX/Accessibility
- **P1-UX-1** [FIXED] Color contrast fails: `#5f6b7a` on `#f8f6f1` = ~3.8:1 (needs 4.5:1 for 14px text). (all files)
- **P1-UX-2** [FIXED] Font sizes below 16px for body text (10-14px in metrics, labels, refs). (all files)
- **P1-UX-3** [FIXED] Heading hierarchy violations — sections use `<div>` not `<h2>`/`<h3>`. (dashboards)
- **P1-UX-4** [FIXED] Touch targets below 44px (link-btn ~30px, footer links ~20px). (all files)
- **P1-UX-5** [FIXED] `target="_blank"` without `rel="noopener noreferrer"`. (all files)
- **P1-UX-6** [FIXED] No skip-to-content link on 20-paper group pages. (group index.html files)

### Software Engineer
- **P1-ENG-1** [FIXED] Three redundant dashboard generators with duplicated code (build.py, generate_dashboards.py, patch_dashboards.py). Major DRY violation.
- **P1-ENG-2** [FIXED] PAPERS dict split across generate_dashboards.py and expand_to_80.py — no single source of truth.
- **P1-ENG-3** [FIXED] Circular import chain via sys.path.insert. (`expand_to_80.py` ↔ `generate_dashboards` ↔ `patch_dashboards`)
- **P1-ENG-4** [FIXED] Hardcoded absolute paths in all generators (C:/AfricaRCT, C:/Users/user). Not portable.
- **P1-ENG-5** [FIXED] generate_dashboards.py is 1583 lines, ~830 of which are a PAPERS dict that should be a JSON file.
- **P1-ENG-6** [FIXED] Division-by-zero risk when all API calls fail (total_trials=0). (`fetch_africa_rcts_by_country.py:304`)

### Domain Expert
- **P1-DOM-1** [FIXED] "240,000 RHD deaths preventable by penicillin" oversimplifies (established valvular disease needs surgery).
- **P1-DOM-2** [FIXED] "Africa 10% of global HF burden" unsourced (likely GBD SSA figure, not all-Africa).
- **P1-DOM-3** [FIXED] Multiple "estimated" percentages in papers are not in the source data and need external sourcing.
- **P1-DOM-4** [FIXED] Absolute count comparisons used throughout without per-capita normalization.
- **P1-DOM-5** [FIXED] `selection-pressure` completion rate of 95.4% inflated by excluding unknown-status trials.
- **P1-DOM-6** [FIXED] `epistemic-care` claims 60% > 54% metadata completeness — unsourced, surprising claim.

---

## P2 — Minor (nice to fix)

### Statistical Methodologist
- **P2-STAT-1** [FIXED] Dead code in Mann-Whitney U (first ranking block unused). (`advanced_statistics.py:169-179`)
- **P2-STAT-2** [FIXED] Z-scores use population std (consistent but undocumented). (`statistical_deep_dive.py:212`)
- **P2-STAT-3** [FIXED] Completion rate denominator excludes ongoing trials (documented choice needed). (`rewrite_all_papers.py:49`)

### Security
- **P2-SEC-1** [FIXED] Unescaped `{ref}` HTML in build.py (intentional `<i>` tags, no external input). (`build.py:637`)
- **P2-SEC-2** [FIXED] JS template literals lack `</script>` sanitization for body content. (`build.py:675-683`)
- **P2-SEC-3** [FIXED] Color values injected into style attributes without validation (all hardcoded). (multiple files)

### UX/Accessibility
- **P2-UX-1** [FIXED] Decorative color-strip lacks `aria-hidden="true"`. (dashboards)
- **P2-UX-2** [FIXED] `<dt>`/`<dd>` with `display:inline` confuses screen readers. (group pages)
- **P2-UX-3** [FIXED] SVG radar labels truncated without tooltip. (dashboards)
- **P2-UX-4** [FIXED] Data tables lack `<caption>` and `scope` attributes. (group pages)
- **P2-UX-5** [FIXED] No `prefers-reduced-motion` media query. (all CSS)
- **P2-UX-6** [FIXED] "Back to Group" link text is vague — should name the group. (dashboards)
- **P2-UX-7** [FIXED] White text on `#7A5A10` badge fails contrast (4.3:1 < 4.5:1). (landing page)

### Software Engineer
- **P2-ENG-1** [FIXED] Bare `except:` clauses throughout (mask real errors). (`patch_dashboards.py:13,19`, student code files)
- **P2-ENG-2** [FIXED] `read_paper_body()` vs `read_body()` — identical but named differently. (build.py vs generate_dashboards.py)
- **P2-ENG-3** [FIXED] Landing page text still says "48 papers" after expansion to 80. (`build.py:898`)
- **P2-ENG-4** [FIXED] CSS duplicated three times with minor differences. (build.py, generate_dashboards.py, patch_dashboards.py)
- **P2-ENG-5** [FIXED] No encoding parameter in module-level JSON loads. (`generate_dashboards.py:22,25`)
- **P2-ENG-6** [FIXED] API error sentinel -1 could corrupt downstream analysis. (`fetch_africa_rcts_by_country.py`)
- **P2-ENG-7** [FIXED] `pageSize=0` may be undocumented CT.gov API behavior. (`fetch_africa_rcts_by_country.py:109`)
- **P2-ENG-8** [FIXED] Two `main()` paths in generate_dashboards.py (48 vs 80 papers depending on entry point).

### Domain Expert
- **P2-DOM-1** [FIXED] SVG bar chart numbers are fabricated scaled values, not real counts. (dashboard hero charts)
- **P2-DOM-2** [FIXED] "17-fold digital gap" is count ratio not rate ratio (rate ratio is 2.1x). (`rewrite_all_papers.py:149`)
- **P2-DOM-3** [FIXED] Physical metaphors (viscosity, escape velocity) will be challenged by reviewers. (papers)
- **P2-DOM-4** [FIXED] Temporal epoch sums don't match totals (3% gap from pre-2000 trials). (data)
- **P2-DOM-5** [FIXED] `$2,000 vs $41,000` per-participant cost unsourced. (`rewrite_all_papers.py:185`)

---

## False Positive Watch
Per `.claude/rules/lessons.md`:
- Benford chi-squared formula IS correct (uses N * (O-E)^2/E, verified)
- Bootstrap percentile indexing IS correct (int() truncation at boundaries)
- Population variance (÷n) is defensible for census of all 54 countries

---

## Recommended Fix Priority
1. **P0-DOM-1,2,3,4**: Fix factual errors in papers/dashboards (contradictory numbers, inverted comparisons, wrong arithmetic) — these would embarrass students on submission
2. **P0-STAT-1,2,3**: Fix math errors (Kendall tau label, Atkinson zeros, Cramer's rule)
3. **P0-ENG-1** [FIXED]: Fix Chad ISO code
4. **P0-UX-1,2**: Add semantic landmarks and focus styles (quick wins)
5. **P1-ENG-1** [FIXED]: Consolidate generators (biggest architectural win)
