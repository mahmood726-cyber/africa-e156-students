# Africa E156 Student Platform — Expansion to 190 Papers

**Date**: 2026-04-07
**Status**: APPROVED
**Repository**: `C:\Users\user\africa-e156-students`
**Live site**: https://mahmood726-cyber.github.io/africa-e156-students/

## 1. Overview

Expand the Africa E156 Student Assignment Platform from 80 papers to 190 papers across the same 4 thematic groups, with higher statistical quality than the existing papers. Each new paper includes an E156 body (7 sentences, ≤156 words), a Python analysis script with 5 advanced statistical methods, and an HTML dashboard with 8 unique SVG charts.

## 2. Distribution (weighted by theme richness)

| Group | Theme | Current | Target | New Papers |
|-------|-------|---------|--------|------------|
| 1 | Geographic Equity & Spatial Justice | 20 | 40 | +20 |
| 2 | Health & Disease Burden | 20 | 60 | +40 |
| 3 | Governance, Justice & Sovereignty | 20 | 45 | +25 |
| 4 | Methods, Design & Research Systems | 20 | 45 | +25 |
| **Total** | | **80** | **190** | **+110** |

## 3. Build Approach

**Manifest-driven batch generator** (`expand_to_190.py`):

```
MANIFEST (110 topics as Python dicts)
    │
    ├── For each topic:
    │   ├── Query ClinicalTrials.gov API v2 (condition/intervention/location)
    │   ├── Compute 5 statistical measures from real data
    │   ├── Generate E156 body (7 sentences, ≤156 words)
    │   ├── Write Python analysis script → {group}/code/{slug}.py
    │   ├── Write HTML dashboard → {group}/dashboards/{slug}.html
    │   └── Append paper card to group index.html
    │
    ├── Update all 4 group index.html files (paper count, cards)
    ├── Update root index.html (total count: 190)
    └── Write generation report (pass/fail per paper)
```

**Key decisions:**
- Each paper's stats computed from **live ClinicalTrials.gov data** (public API, no key)
- Statistical methods library embedded in script (no external deps beyond `requests`)
- Dashboards are self-contained single HTML files with inline SVG charts
- Seeds: `seed = hash(slug) % 2**32` for deterministic sampling per paper
- All 110 papers generated in one run (~15-20 min for API calls)

## 4. Topic Manifest

### 4.1 Group 1: Geographic Equity & Spatial Justice (papers 21-40)

| # | Slug | Title | ClinicalTrials.gov Query | Statistical Methods |
|---|------|-------|--------------------------|---------------------|
| 21 | landlocked-nation-penalty | Landlocked Nation Penalty | 16 landlocked African countries vs coastal | Moran's I, bootstrap CI, Lorenz curve, rate ratio, permutation test |
| 22 | island-state-isolation | Island State Research Isolation | Madagascar, Mauritius, Comoros, Cabo Verde, Seychelles, Sao Tome | Poisson rate ratios, permutation test, Bayesian rate estimation, bootstrap CI, entropy |
| 23 | conflict-zone-collapse | Conflict Zone Trial Collapse | WHO conflict-affected states (DRC, South Sudan, Libya, Somalia, etc.) | Interrupted time series, changepoint detection, Poisson regression, bootstrap CI, effect size |
| 24 | francophone-research-desert | Francophone Research Desert | Francophone vs Anglophone Africa trial counts | KL divergence, chi-squared, Theil index, Lorenz curve, bootstrap CI |
| 25 | capital-city-monopoly | Capital City Monopoly Index | Capital vs non-capital city trial concentration | HHI, Gini, Atkinson index, bootstrap CI, Lorenz curve |
| 26 | sahel-belt-void | Sahel Belt Void | Sahel countries (Mali, Niger, Chad, Burkina Faso, Mauritania) | Spatial autocorrelation, Bayesian rate estimation, Poisson exact, bootstrap CI, effect size |
| 27 | east-african-hub | East African Community Hub | EAC member states (Kenya, Uganda, Tanzania, Rwanda, Burundi, DRC, South Sudan) | Network centrality, community detection, HHI, bootstrap CI, Theil index |
| 28 | west-african-ecowas | West African ECOWAS Corridor | ECOWAS 15-nation research patterns | Small-world coefficient, betweenness centrality, modularity, bootstrap CI, entropy |
| 29 | southern-african-arc | Southern African Research Arc | SADC nations trial distribution | Power-law fitting, Zipf analysis, Gini, bootstrap CI, KS test |
| 30 | north-south-divide | North Africa vs Sub-Saharan Divide | Egypt/Morocco/Tunisia/Algeria/Libya vs Sub-Saharan | DID, Bayesian hierarchical model, rate ratio, bootstrap CI, Theil index |
| 31 | distance-to-trial | Distance-to-Trial-Site Burden | Population-weighted distance to nearest trial site | Spatial KDE, kernel density estimation, Gini, bootstrap CI, regression |
| 32 | secondary-city-emergence | Secondary City Emergence | Trials in non-capital secondary cities over time | Poisson regression, trend analysis, changepoint detection, bootstrap CI, growth rate |
| 33 | cross-border-networks | Cross-Border Trial Networks | Multi-country trials spanning borders | Network graph analysis, modularity, centrality, bootstrap CI, community detection |
| 34 | climate-zone-patterns | Climate Zone Research Patterns | Tropical vs arid vs Mediterranean zone trials | ANOVA, Kruskal-Wallis, effect sizes, bootstrap CI, pairwise comparisons |
| 35 | port-city-advantage | Port City Advantage | Coastal port cities vs inland hubs | Logistic regression, odds ratios, bootstrap CI, rate ratio, chi-squared |
| 36 | research-corridor-mapping | Research Corridor Mapping | Highway/transport corridor proximity analysis | Spatial regression, distance decay function, Pearson/Spearman, bootstrap CI, GAM |
| 37 | linguistic-barrier | Linguistic Barrier Mapping | Arabic/French/English/Portuguese zone analysis | Mutual information, entropy decomposition, chi-squared, bootstrap CI, Theil |
| 38 | population-density-mismatch | Population Density Mismatch | Trial density vs population density ratios | Pearson/Spearman correlation, GAM, Lorenz curve, bootstrap CI, regression |
| 39 | regional-economic-community | AU Regional Economic Community Gaps | 8 RECs comparative analysis | Multi-level modeling, radar scoring, ANOVA, bootstrap CI, effect sizes |
| 40 | zero-trial-nations | The Zero-Trial Nations | Countries with <5 lifetime trials | Bayesian zero-inflated Poisson, survival to first trial, bootstrap CI, rate estimation, entropy |

### 4.2 Group 2: Health & Disease Burden (papers 21-60)

| # | Slug | Title | ClinicalTrials.gov Query | Statistical Methods |
|---|------|-------|--------------------------|---------------------|
| 21 | hiv-saturation-index | HIV Trial Saturation Index | HIV trials vs prevalence per country | Lorenz curve, concentration index, DID, bootstrap CI, Poisson regression |
| 22 | tb-coinfection-gap | Tuberculosis Co-Infection Gap | TB + HIV co-infection trials | Bayesian meta-proportion, forest plot, rate ratio, bootstrap CI, heterogeneity |
| 23 | malaria-vaccine-pipeline | Malaria Vaccine Pipeline | Malaria vaccine trials by phase and country | Kaplan-Meier phase transition, survival analysis, bootstrap CI, hazard ratio, trend |
| 24 | sickle-cell-neglect | Sickle Cell Disease Neglect | Sickle cell disease trials Africa vs US/Europe | Rate ratio, bootstrap CI, Theil index, Lorenz curve, permutation test |
| 25 | diabetes-epidemic-mismatch | Diabetes Epidemic Mismatch | T2DM trials vs diabetes prevalence | Scatter regression, Cook's distance, leverage analysis, bootstrap CI, Poisson offset |
| 26 | hypertension-desert | Hypertension Trial Desert | Hypertension trials per hypertensive population | Poisson regression, population offset, rate ratio, bootstrap CI, Lorenz curve |
| 27 | stroke-research-void | Stroke Research Void | Stroke trials Africa vs global | Bayesian rate estimation, credible intervals, rate ratio, bootstrap CI, entropy |
| 28 | cancer-landscape | Cancer Trial Landscape | All cancer types combined audit | Heatmap clustering, hierarchical dendrogram, chi-squared, bootstrap CI, Theil index |
| 29 | breast-cancer-disparity | Breast Cancer Disparity | Breast cancer trials Africa vs US | Odds ratio, NNT calculation, funnel analysis, bootstrap CI, rate ratio |
| 30 | cervical-cancer-hpv | Cervical Cancer HPV Gap | Cervical/HPV trials in high-burden nations | Spatial correlation, Moran's I, rate ratio, bootstrap CI, Poisson regression |
| 31 | prostate-cancer-genomic | Prostate Cancer Genomic Divide | Prostate cancer + genomics/precision medicine trials | PCA, allele frequency proxy, rate ratio, bootstrap CI, chi-squared |
| 32 | childhood-cancer-neglect | Childhood Cancer Neglect | Pediatric oncology trials in Africa | Zero-inflated Poisson, age-stratified rates, bootstrap CI, rate ratio, effect size |
| 33 | mental-health-invisibility | Mental Health Invisibility | Depression/anxiety/psychosis/PTSD trials | Shannon entropy, topic clustering, rate ratio, bootstrap CI, Lorenz curve |
| 34 | epilepsy-treatment-gap | Epilepsy Treatment Gap | Epilepsy/seizure trials in Africa | Treatment gap ratio, bootstrap CI, Poisson regression, rate ratio, trend analysis |
| 35 | ntd-atlas | Neglected Tropical Diseases Atlas | 20 NTDs mapped to trial coverage | Choropleth mapping, Jaccard similarity, gap score, bootstrap CI, heatmap |
| 36 | schistosomiasis-pipeline | Schistosomiasis Pipeline | Schistosomiasis-specific trials | Time series decomposition, trend test, Poisson regression, bootstrap CI, rate ratio |
| 37 | trypanosomiasis-last-mile | Trypanosomiasis Last Mile | Sleeping sickness/HAT trials | Survival analysis, elimination probability, bootstrap CI, Kaplan-Meier, hazard |
| 38 | amr-crisis | Antimicrobial Resistance Crisis | AMR/antibiotic resistance trials in Africa | Exponential growth fit, doubling time, ARIMA, bootstrap CI, trend test |
| 39 | snake-envenomation | Snake Envenomation Silence | Snakebite/antivenom trials | Poisson exact test, rate ratios, bootstrap CI, burden mismatch, permutation |
| 40 | ebola-preparedness | Ebola Preparedness Audit | Ebola/Marburg/VHF trial readiness | Interrupted time series, pre/post outbreak analysis, bootstrap CI, rate ratio, Bayesian |
| 41 | mpox-response-equity | Mpox Response Equity | Mpox/monkeypox trials by clade/region | Bayesian adaptive analysis, Bayes factors, rate ratio, bootstrap CI, chi-squared |
| 42 | neonatal-mortality-gap | Neonatal Mortality Gap | Neonatal/newborn trials vs mortality burden | Burden-to-trial mismatch index, Lorenz curve, bootstrap CI, rate ratio, Poisson |
| 43 | nutrition-stunting | Nutrition & Stunting Trials | Malnutrition/stunting/wasting interventions | Mixed-effects regression proxy, growth curves, bootstrap CI, rate ratio, trend |
| 44 | respiratory-infection | Respiratory Infection Pipeline | Pneumonia/LRTI trials in children | Age-stratified Poisson, ARIMA, bootstrap CI, rate ratio, trend analysis |
| 45 | diarrheal-disease-deficit | Diarrheal Disease Research Deficit | Diarrhea/cholera/rotavirus trials | Spatial scan statistic, SaTScan-like, bootstrap CI, Poisson, rate ratio |
| 46 | kidney-disease-silence | Kidney Disease Silence | CKD/AKI/nephrology trials in Africa | Cox PH model proxy, competing risks, bootstrap CI, rate ratio, survival |
| 47 | liver-hepatitis-b | Liver Disease & Hepatitis B | HBV/HCV/liver disease trials | Cascade-of-care analysis, waterfall quantification, bootstrap CI, rate ratio, trend |
| 48 | eye-health-trachoma | Eye Health & Trachoma | Ophthalmology/trachoma/blindness trials | Elimination threshold analysis, rate ratio, bootstrap CI, Poisson, trend |
| 49 | surgical-trials-void | Surgical Trials Void | Surgery/anesthesia/emergency trials | Bellwether mapping, gap index, bootstrap CI, rate ratio, chi-squared |
| 50 | traditional-medicine | Traditional Medicine Integration | Traditional/herbal/complementary medicine trials | Network pharmacology proxy, cluster analysis, bootstrap CI, chi-squared, entropy |
| 51 | vaccine-equity-audit | Vaccine Equity Audit | All vaccine trials by antigen type | Heatmap, temporal acceleration index, bootstrap CI, rate ratio, Theil index |
| 52 | rheumatic-heart-disease | Rheumatic Heart Disease | RHD/ARF/rheumatic fever trials | Penicillin coverage model, DALY estimation, bootstrap CI, rate ratio, Poisson |
| 53 | road-traffic-injury | Road Traffic Injury Trials | Trauma/emergency medicine/injury trials | Poisson rate analysis, injury pyramid, bootstrap CI, rate ratio, trend |
| 54 | substance-use-disorders | Substance Use Disorders | Alcohol/tobacco/drug use trials | Prevalence-trial correlation, GAM proxy, bootstrap CI, rate ratio, Lorenz |
| 55 | maternal-anemia | Maternal Anemia Pipeline | Anemia in pregnancy/iron supplementation trials | Dose-response proxy, meta-regression, bootstrap CI, rate ratio, trend |
| 56 | preterm-birth | Preterm Birth Interventions | Prematurity/NICU/preterm trials | Survival curves, NICU capacity proxy, bootstrap CI, rate ratio, Kaplan-Meier |
| 57 | contraception-family-planning | Contraception & Family Planning | Reproductive health/contraception trials | Unmet need vs trial ratio, Theil index, bootstrap CI, rate ratio, Lorenz |
| 58 | palliative-care-desert | Palliative Care Desert | Palliative/end-of-life/hospice trials | Exponential scarcity model, bootstrap CI, rate ratio, Poisson, trend |
| 59 | aging-geriatric | Aging & Geriatric Medicine | Elderly/geriatric/aging trials in Africa | Age pyramid analysis, demographic shift model, bootstrap CI, rate ratio, trend |
| 60 | one-health-zoonotic | One Health & Zoonotic Interface | Zoonotic/brucellosis/Rift Valley fever trials | Spillover network proxy, cross-species mapping, bootstrap CI, rate ratio, entropy |

### 4.3 Group 3: Governance, Justice & Sovereignty (papers 21-45)

| # | Slug | Title | ClinicalTrials.gov Query | Statistical Methods |
|---|------|-------|--------------------------|---------------------|
| 21 | informed-consent-language | Informed Consent Language Audit | Language metadata in consent documents | Shannon entropy, linguistic diversity index, chi-squared, bootstrap CI, Theil |
| 22 | participant-compensation | Participant Compensation Ethics | Payment/compensation in protocol metadata | Purchasing power parity analysis, Gini, bootstrap CI, rate ratio, permutation |
| 23 | gender-trial-leadership | Gender in Trial Leadership | Female PI rates Africa vs global | Logistic regression, odds ratios, bootstrap CI, chi-squared, trend analysis |
| 24 | ethics-committee-capacity | Ethics Committee Capacity | IRB/EC review timeline proxies | Queuing theory model, wait time estimation, bootstrap CI, Poisson, rate ratio |
| 25 | post-trial-drug-access | Post-Trial Drug Access | Provision/access commitments in protocols | Kaplan-Meier access probability, bootstrap CI, rate ratio, survival, chi-squared |
| 26 | colonial-legacy-sponsorship | Colonial Legacy in Sponsorship | Former colonial power → former colony sponsor flows | Network analysis, modularity by empire, bootstrap CI, chi-squared, centrality |
| 27 | south-south-collaboration | South-South Collaboration Index | India/China/Brazil sponsor role in Africa | Trend analysis, growth rate fitting, bootstrap CI, rate ratio, Poisson regression |
| 28 | open-access-equity | Open Access Publication Equity | OA rates for African-led vs foreign-led trials | Chi-squared, relative risk, NNT, bootstrap CI, Lorenz curve |
| 29 | funding-flow-cartography | Funding Flow Cartography | NIH/Wellcome/Gates/EU funding patterns | Sankey flow quantification, concentration ratio, HHI, bootstrap CI, Theil |
| 30 | community-engagement-depth | Community Engagement Depth | Community advisory board / engagement mentions | NLP keyword density, trend detection, bootstrap CI, chi-squared, rate ratio |
| 31 | benefit-sharing-mechanisms | Benefit Sharing Mechanisms | Benefit-sharing language in protocols | Content analysis scoring, compliance rate, bootstrap CI, chi-squared, trend |
| 32 | insurance-indemnity-gaps | Insurance & Indemnity Gaps | Trial insurance/indemnity provisions | Regulatory gap score, risk index, bootstrap CI, rate ratio, chi-squared |
| 33 | pediatric-consent-complexity | Pediatric Consent Complexity | Child assent/parental consent practices | Age-stratified analysis, ethical compliance score, bootstrap CI, chi-squared, rate |
| 34 | vulnerable-population-protections | Vulnerable Population Protections | Prisoner/refugee/pregnant exclusion criteria | Exclusion rate ratios, permutation test, bootstrap CI, chi-squared, odds ratio |
| 35 | publication-lag-penalty | Publication Lag Penalty | Time-to-publication Africa vs global | Cox regression, hazard ratios, Kaplan-Meier, bootstrap CI, median survival |
| 36 | predatory-journal-risk | Predatory Journal Risk | Publication venue quality proxy | Journal impact scoring, Bayesian classification, bootstrap CI, rate ratio, entropy |
| 37 | data-sharing-compliance | Data Sharing Compliance | Data availability statement audit | Compliance rate, temporal trend, bootstrap CI, chi-squared, logistic regression |
| 38 | safety-reporting-integrity | Whistleblower & Safety Reporting | SAE/SUSAR reporting completeness | Reporting density score, Benford test, bootstrap CI, rate ratio, chi-squared |
| 39 | local-manufacturing | Local Manufacturing Capacity | Trials using locally manufactured products | Industrial capacity correlation, Spearman, bootstrap CI, rate ratio, regression |
| 40 | au-health-strategy-alignment | AU Health Strategy Alignment | Trial topics vs AU Agenda 2063 goals | Cosine similarity, alignment score, bootstrap CI, chi-squared, radar scoring |
| 41 | youth-researcher-pipeline | Youth Researcher Pipeline | Early-career investigator representation | Age cohort analysis, pipeline modeling, bootstrap CI, trend, Poisson regression |
| 42 | diaspora-investigator-networks | Diaspora Investigator Networks | African diaspora researchers leading trials | Network centrality, bridge analysis, bootstrap CI, modularity, community detection |
| 43 | institutional-review-bottlenecks | Institutional Review Bottlenecks | Multi-site approval timeline proxies | Queuing model, bottleneck identification, bootstrap CI, Poisson, rate ratio |
| 44 | registration-transparency | Trial Registration Transparency Score | ICTRP compliance and prospective registration | Composite transparency index, bootstrap CI, chi-squared, trend, logistic regression |
| 45 | decolonising-research | Decolonising Clinical Research | Power asymmetry composite metric | PCA on 8 governance indicators, eigenvalue analysis, bootstrap CI, Theil, entropy |

### 4.4 Group 4: Methods, Design & Research Systems (papers 21-45)

| # | Slug | Title | ClinicalTrials.gov Query | Statistical Methods |
|---|------|-------|--------------------------|---------------------|
| 21 | adaptive-design-adoption | Adaptive Design Adoption Curve | Adaptive trial keyword search | Logistic growth curve, inflection point, bootstrap CI, trend, rate ratio |
| 22 | platform-trial-readiness | Platform Trial Readiness | Platform/master protocol/basket trials | SWOT quantification, readiness index, bootstrap CI, rate ratio, chi-squared |
| 23 | bayesian-trial-penetration | Bayesian Trial Penetration | Bayesian design keyword search | Posterior estimation, Bayes factors, bootstrap CI, rate ratio, trend |
| 24 | pragmatic-explanatory-spectrum | Pragmatic vs Explanatory Spectrum | PRECIS-2 proxy scoring from protocols | Radar composite score, bootstrap CI, chi-squared, rate ratio, entropy |
| 25 | digital-health-explosion | Digital Health Trial Explosion | mHealth/telemedicine/app-based trials | Exponential fit, doubling time, ARIMA, bootstrap CI, trend |
| 26 | ai-ml-trials | AI & Machine Learning in Trials | AI/ML/deep learning trial designs | Technology adoption S-curve, Bass model, bootstrap CI, rate ratio, trend |
| 27 | biomarker-endpoint-quality | Biomarker Endpoint Quality | Biomarker vs clinical endpoint usage | Surrogate validation proxy, R-squared, bootstrap CI, rate ratio, chi-squared |
| 28 | composite-endpoint-complexity | Composite Endpoint Complexity | Composite primary endpoint prevalence | Component analysis, endpoint entropy, bootstrap CI, rate ratio, HHI |
| 29 | patient-reported-outcomes | Patient-Reported Outcomes Gap | PRO/QoL measure usage rates | Instrument mapping, standardisation score, bootstrap CI, rate ratio, trend |
| 30 | sample-size-adequacy | Sample Size Adequacy Audit | Declared vs achieved enrollment ratios | Power analysis, type II error estimation, bootstrap CI, rate ratio, regression |
| 31 | statistical-analysis-plan | Statistical Analysis Plan Depth | SAP completeness proxy scoring | Completeness index, IRT proxy, bootstrap CI, rate ratio, chi-squared |
| 32 | randomisation-quality | Randomisation Quality | Allocation concealment & sequence generation | RoB scoring proxy, bootstrap CI, chi-squared, rate ratio, odds ratio |
| 33 | blinding-architecture | Blinding Architecture | Masking depth and integrity audit | Blinding index, James-Bang-Tian proxy, bootstrap CI, rate ratio, chi-squared |
| 34 | intention-to-treat-compliance | Intention-to-Treat Compliance | ITT vs per-protocol analysis rates | Compliance ratio, attrition analysis, bootstrap CI, rate ratio, chi-squared |
| 35 | interim-analysis-dsmb | Interim Analysis & DSMB Patterns | DSMB usage and stopping rule mentions | Alpha-spending proxy, O'Brien-Fleming, bootstrap CI, rate ratio, trend |
| 36 | multi-arm-efficiency | Multi-Arm Trial Efficiency | Multi-arm vs two-arm design adoption | Efficiency gain calculation, Dunnett proxy, bootstrap CI, rate ratio, trend |
| 37 | cluster-rct-rigor | Cluster-RCT Design Rigor | Cluster-randomised trial ICC/design effect | Design effect audit, effective sample size, bootstrap CI, rate ratio, regression |
| 38 | non-inferiority-patterns | Non-Inferiority Design Patterns | Non-inferiority/equivalence trial margin | Margin derivation analysis, CPMP proxy, bootstrap CI, rate ratio, chi-squared |
| 39 | pediatric-trial-methodology | Pediatric Trial Methodology | Age-appropriate endpoints and formulations | ICH E11 compliance proxy, bootstrap CI, rate ratio, chi-squared, age stratification |
| 40 | implementation-science | Implementation Science Penetration | Hybrid effectiveness-implementation designs | RE-AIM framework proxy, bootstrap CI, rate ratio, chi-squared, trend |
| 41 | health-economic-evaluation | Health Economic Evaluation | Cost-effectiveness/economic evaluation trials | ICER distribution proxy, WTP threshold, bootstrap CI, rate ratio, trend |
| 42 | long-term-followup | Long-Term Follow-Up Deficit | Follow-up duration Africa vs global | Kaplan-Meier retention, dropout hazard, bootstrap CI, rate ratio, survival |
| 43 | data-management-infrastructure | Data Management Infrastructure | EDC/eCRF/data quality indicators | Error rate proxy, process capability, bootstrap CI, rate ratio, trend |
| 44 | endpoint-harmonisation | Endpoint Harmonisation Deficit | Endpoint heterogeneity across similar trials | Jaccard dissimilarity, clustering, bootstrap CI, entropy, heatmap |
| 45 | research-waste-quantification | Research Waste Quantification | Avoidable waste from design deficiencies | Chalmers-Glasziou taxonomy scoring, bootstrap CI, rate ratio, Lorenz, Gini |

## 5. Statistical Methods Library

Each paper gets **5 statistical methods** (up from ~3 in existing papers). Methods drawn from a pool of 30+:

### Tier 1 — Core (every paper gets at least 2)
- Bootstrap confidence intervals (BCa, 10,000 replicates)
- Effect size with CI (rate ratio, odds ratio, Cohen's d)

### Tier 2 — Distribution & Inequality
- Lorenz curve + Gini coefficient
- Theil index (GE(1)) / Atkinson index
- KL divergence (Kullback-Leibler)
- Shannon entropy / Renyi entropy

### Tier 3 — Modeling
- Bayesian rate estimation (conjugate Beta-Binomial)
- Poisson regression with population offset
- Logistic regression + odds ratios
- Cox proportional hazards (time-to-event)
- Interrupted time series (pre/post intervention)
- Changepoint detection (PELT algorithm)
- ARIMA projections (1-step ahead)

### Tier 4 — Spatial & Network
- Moran's I spatial autocorrelation
- Network centrality (degree, betweenness, eigenvector)
- Community detection (Louvain-like modularity)
- Spatial kernel density estimation

### Tier 5 — Advanced
- Bayesian hierarchical models (Beta-Binomial conjugate)
- Zero-inflated Poisson (EM algorithm)
- Power-law / Zipf fitting (MLE + KS goodness-of-fit)
- Permutation tests (exact p-values, 10,000 permutations)
- PCA with scree plot + variance explained
- Bass diffusion model (technology adoption)
- Item Response Theory proxy (difficulty + discrimination)

**All implemented in pure Python** (manual numpy-style computation). No scipy/sklearn dependency — keeps scripts student-friendly and portable. Only `requests` needed for API calls.

## 6. Dashboard Chart Palette

Each dashboard gets **8 unique SVG charts**. Chart types assigned from pool of 15:

1. Choropleth map of Africa (SVG country paths, metric-shaded)
2. Lorenz curve with diagonal equality line + Gini annotation
3. Forest plot (effect sizes with CIs, diamond summary)
4. Violin/box plot (distribution comparison)
5. Heatmap with hierarchical clustering dendrogram
6. Network graph (force-directed, node size = trial count)
7. Time series with changepoint markers + ARIMA projection
8. Waterfall chart (cumulative contribution decomposition)
9. Sankey diagram (funding/sponsor flows)
10. Radar/spider chart (multi-dimensional comparison)
11. Bubble chart (3-variable scatter)
12. Slope chart (paired before/after comparison)
13. Ridge/joy plot (overlapping density distributions)
14. Funnel plot (asymmetry detection)
15. Kaplan-Meier survival curve with confidence band

**Constraint**: No two dashboards in the same group share the same 8-chart combination.

## 7. E156 Body Generation

Each E156 body follows the 7-sentence contract:

| Sentence | Role | ~Words |
|----------|------|--------|
| S1 | Question (population, intervention, endpoint) | 22 |
| S2 | Dataset (studies, participants, scope) | 20 |
| S3 | Method (synthesis, model, effect scale) | 20 |
| S4 | Result (lead estimate + interval) | 30 |
| S5 | Robustness (heterogeneity/sensitivity) | 22 |
| S6 | Interpretation (plain-language meaning) | 22 |
| S7 | Boundary (main limitation) | 20 |

**Total**: Exactly 7 sentences, at most 156 words, single paragraph.

Data source: ClinicalTrials.gov API v2 (public, no key required). Every number in every paper comes from a real API query — no fabricated statistics.

## 8. File Structure (after expansion)

```
africa-e156-students/
├── index.html                              (updated: 190 total)
├── expand_to_190.py                        (new generator script)
├── geographic-equity/
│   ├── index.html                          (updated: 40 papers)
│   ├── code/                               (+20 new .py scripts)
│   └── dashboards/                         (+20 new .html dashboards)
├── health-disease/
│   ├── index.html                          (updated: 60 papers)
│   ├── code/                               (+40 new .py scripts)
│   └── dashboards/                         (+40 new .html dashboards)
├── governance-justice/
│   ├── index.html                          (updated: 45 papers)
│   ├── code/                               (+25 new .py scripts)
│   └── dashboards/                         (+25 new .html dashboards)
└── methods-systems/
    ├── index.html                          (updated: 45 papers)
    ├── code/                               (+25 new .py scripts)
    └── dashboards/                         (+25 new .html dashboards)
```

**New files**: 110 Python scripts + 110 HTML dashboards + 1 generator script = **221 new files**
**Updated files**: 5 HTML index files (root + 4 groups)

## 9. Quality Gates

Before declaring done:

1. **E156 compliance**: Every body is exactly 7 sentences, ≤156 words
2. **Div balance**: `<div>` open/close count matches in every HTML file
3. **Script integrity**: No literal `</script>` inside `<script>` blocks (use `${'<'}/script>`)
4. **API verification**: Every paper's ClinicalTrials.gov query returns >0 results
5. **Chart uniqueness**: No two dashboards in same group have identical 8-chart sets
6. **Stats verification**: All computed statistics are finite (no NaN/Inf)
7. **Reference validity**: Each paper has 2-3 suggested references
8. **Accessibility**: All interactive elements have keyboard support, ARIA labels
9. **Offline-first**: No external CDN dependencies in any HTML file
10. **Determinism**: Fixed seeds for all stochastic computations

## 10. Existing Infrastructure Preserved

The following existing files are **not modified** (only appended to):
- All 80 existing paper cards in group index.html files (appended after)
- All 80 existing dashboards and code scripts (untouched)
- `analysis/` directory (untouched)
- `review-findings.md` (untouched)
- `README.md` (updated for new count)

## 11. References

Each paper includes 2-3 suggested references drawn from:
- ClinicalTrials.gov API v2 Documentation (standard reference)
- Disease-specific WHO/Lancet/NEJM review articles
- Methodological references (SPIRIT, CONSORT, PRISMA as appropriate)
- African-authored publications where available (Alemayehu, Ndounga Diakou, Sliwa, etc.)
