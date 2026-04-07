"""
Paper manifest for 110 new papers (80→190 expansion).
Each paper: slug, title, group, paper_num, query params, assigned stats, assigned charts, context, references.
"""

# Africa countries for geographic queries
LANDLOCKED = ["Mali", "Niger", "Chad", "Burkina Faso", "Central African Republic",
              "South Sudan", "Uganda", "Rwanda", "Burundi", "Malawi",
              "Zambia", "Zimbabwe", "Botswana", "Lesotho", "Eswatini", "Ethiopia"]
ISLAND_STATES = ["Madagascar", "Mauritius", "Comoros", "Cabo Verde", "Seychelles", "Sao Tome and Principe"]
CONFLICT_STATES = ["Democratic Republic of the Congo", "South Sudan", "Libya", "Somalia",
                   "Central African Republic", "Mali", "Mozambique", "Burkina Faso", "Nigeria", "Ethiopia"]
FRANCOPHONE = ["Senegal", "Mali", "Guinea", "Ivory Coast", "Burkina Faso", "Niger", "Togo", "Benin",
               "Cameroon", "Central African Republic", "Chad", "Republic of the Congo",
               "Democratic Republic of the Congo", "Gabon", "Madagascar", "Comoros",
               "Djibouti", "Burundi", "Rwanda"]
ANGLOPHONE = ["Nigeria", "Ghana", "Kenya", "Uganda", "Tanzania", "South Africa", "Malawi",
              "Zambia", "Zimbabwe", "Botswana", "Sierra Leone", "Liberia", "Gambia"]
SAHEL = ["Mali", "Niger", "Chad", "Burkina Faso", "Mauritania", "Senegal"]
EAC = ["Kenya", "Uganda", "Tanzania", "Rwanda", "Burundi", "Democratic Republic of the Congo", "South Sudan"]
ECOWAS = ["Nigeria", "Ghana", "Senegal", "Mali", "Guinea", "Ivory Coast", "Burkina Faso", "Niger",
          "Togo", "Benin", "Sierra Leone", "Liberia", "Gambia", "Guinea-Bissau", "Cabo Verde"]
SADC = ["South Africa", "Mozambique", "Tanzania", "Democratic Republic of the Congo", "Zambia",
        "Zimbabwe", "Malawi", "Botswana", "Namibia", "Angola", "Lesotho", "Eswatini", "Mauritius", "Madagascar"]
NORTH_AFRICA = ["Egypt", "Morocco", "Tunisia", "Algeria", "Libya"]
AU_RECS = {
    "ECOWAS": ECOWAS, "EAC": EAC, "SADC": SADC,
    "AMU": ["Morocco", "Algeria", "Tunisia", "Libya", "Mauritania"],
    "ECCAS": ["Cameroon", "Central African Republic", "Chad", "Republic of the Congo",
              "Democratic Republic of the Congo", "Gabon", "Equatorial Guinea", "Sao Tome and Principe"],
    "IGAD": ["Ethiopia", "Kenya", "Uganda", "Sudan", "South Sudan", "Djibouti", "Somalia", "Eritrea"],
    "CEN-SAD": ["Libya", "Chad", "Niger", "Mali", "Burkina Faso", "Nigeria", "Senegal"],
    "COMESA": ["Egypt", "Kenya", "Ethiopia", "Uganda", "Zambia", "Zimbabwe", "Malawi", "Rwanda", "Burundi"]
}

CHART_TYPES = [
    "choropleth", "lorenz", "forest", "violin", "heatmap",
    "network", "timeseries", "waterfall", "sankey", "radar",
    "bubble", "slope", "ridge", "funnel", "kaplan_meier"
]

# Sentence role colors for dashboards
ROLE_COLORS = ["#1b4f72", "#0e6251", "#4a235a", "#922b21", "#7e5109", "#0b5345", "#566573"]

# Standard references
REF_CTGOV = 'ClinicalTrials.gov API v2 Documentation. U.S. National Library of Medicine. https://clinicaltrials.gov/data-api/about-api'
REF_ALEMAYEHU = 'Alemayehu C, et al. "Behind the mask of the African clinical trials landscape." Trials. 2018;19:519.'
REF_DRAIN = 'Drain PK, et al. "Global migration of clinical trials." Nat Rev Drug Discov. 2018;17:765-766.'
REF_NDOUNGA = 'Ndounga Diakou LA, et al. "Mapping of clinical trials in sub-Saharan Africa." Trials. 2022;23:490.'
REF_WHO_MATERNAL = 'WHO. "Trends in maternal mortality 2000 to 2020." Geneva, 2023.'
REF_SLIWA = 'Sliwa K, et al. "Readmission and death after an acute heart failure event." Eur Heart J. 2017;38:1508-1518.'
REF_LANG = 'Lang T, Siribaddana S. "Clinical trials have gone global: is this a good thing?" PLoS Med. 2012;9:e1001228.'
REF_HEDT = 'Hedt-Gauthier BL, et al. "Stuck in the middle: authorship in collaborative health research in Africa." BMJ Glob Health. 2019;4:e001853.'
REF_CHAN = 'Chan AW, et al. "SPIRIT 2013 statement." Ann Intern Med. 2013;158:200-207.'
REF_GBD = 'GBD 2021 Collaborators. "Global burden of disease study 2021." Lancet. 2024.'


def _charts(indices):
    """Select 8 chart types by index from CHART_TYPES."""
    return [CHART_TYPES[i % len(CHART_TYPES)] for i in indices]


# ═══════════════════════════════════════════════════════════
#  GROUP 1: GEOGRAPHIC EQUITY & SPATIAL JUSTICE (papers 21-40)
# ═══════════════════════════════════════════════════════════
GEO_PAPERS = [
    {
        "slug": "landlocked-nation-penalty", "title": "Landlocked Nation Penalty",
        "group": "geographic-equity", "paper_num": 21,
        "query": {"condition": None, "countries": LANDLOCKED},
        "stats": ["morans_i", "bootstrap_ci", "lorenz", "rate_ratio", "permutation"],
        "charts": _charts([0, 1, 2, 3, 4, 6, 7, 9]),
        "context": "Landlocked African nations face compounded research access barriers — no port infrastructure for temperature-sensitive biologics, higher import costs for trial supplies, and limited international connectivity for monitoring visits.",
        "refs": [REF_NDOUNGA, REF_DRAIN, REF_CTGOV]
    },
    {
        "slug": "island-state-isolation", "title": "Island State Research Isolation",
        "group": "geographic-equity", "paper_num": 22,
        "query": {"condition": None, "countries": ISLAND_STATES},
        "stats": ["poisson_rate", "permutation", "bayesian_rate", "bootstrap_ci", "shannon_entropy"],
        "charts": _charts([0, 2, 3, 6, 7, 9, 10, 14]),
        "context": "African island states face unique challenges: small populations limit enrollment, geographic isolation increases monitoring costs, and limited healthcare infrastructure restricts trial site eligibility.",
        "refs": [REF_ALEMAYEHU, REF_CTGOV]
    },
    {
        "slug": "conflict-zone-collapse", "title": "Conflict Zone Trial Collapse",
        "group": "geographic-equity", "paper_num": 23,
        "query": {"condition": None, "countries": CONFLICT_STATES},
        "stats": ["interrupted_time_series", "changepoint_detection", "poisson_rate", "bootstrap_ci", "effect_size"],
        "charts": _charts([0, 6, 7, 2, 3, 13, 14, 9]),
        "context": "Armed conflict destroys research infrastructure, displaces trained staff, and makes participant follow-up impossible. Trial collapse in conflict zones creates evidence deserts precisely where health needs are greatest.",
        "refs": [REF_NDOUNGA, REF_CTGOV, REF_GBD]
    },
    {
        "slug": "francophone-research-desert", "title": "Francophone Research Desert",
        "group": "geographic-equity", "paper_num": 24,
        "query": {"condition": None, "countries": FRANCOPHONE[:8]},
        "stats": ["kl_divergence", "chi_squared", "theil_index", "lorenz", "bootstrap_ci"],
        "charts": _charts([0, 1, 4, 7, 9, 3, 6, 11]),
        "context": "Francophone Africa hosts fewer clinical trials per capita than Anglophone Africa, reflecting language barriers in international collaboration, fewer English-language publication outlets, and historic underinvestment in Francophone research networks.",
        "refs": [REF_ALEMAYEHU, REF_NDOUNGA, REF_CTGOV]
    },
    {
        "slug": "capital-city-monopoly", "title": "Capital City Monopoly Index",
        "group": "geographic-equity", "paper_num": 25,
        "query": {"condition": None, "location": "Africa"},
        "stats": ["hhi_index", "gini_coefficient", "atkinson_index", "bootstrap_ci", "lorenz"],
        "charts": _charts([0, 1, 7, 3, 9, 4, 11, 6]),
        "context": "Capital cities monopolize African clinical trial infrastructure because they host the major teaching hospitals, have reliable electricity and internet, and offer the transport links that sponsors require for monitoring.",
        "refs": [REF_DRAIN, REF_CTGOV]
    },
    {
        "slug": "sahel-belt-void", "title": "Sahel Belt Void",
        "group": "geographic-equity", "paper_num": 26,
        "query": {"condition": None, "countries": SAHEL},
        "stats": ["bayesian_rate", "poisson_rate", "bootstrap_ci", "effect_size", "shannon_entropy"],
        "charts": _charts([0, 2, 3, 6, 7, 9, 10, 14]),
        "context": "The Sahel belt — stretching from Mauritania to Chad — combines extreme poverty, climate vulnerability, and active conflict, creating a vast research void across six nations with a combined population exceeding 100 million.",
        "refs": [REF_NDOUNGA, REF_GBD, REF_CTGOV]
    },
    {
        "slug": "east-african-hub", "title": "East African Community Hub",
        "group": "geographic-equity", "paper_num": 27,
        "query": {"condition": None, "countries": EAC},
        "stats": ["network_centrality", "hhi_index", "theil_index", "bootstrap_ci", "shannon_entropy"],
        "charts": _charts([5, 0, 1, 4, 6, 9, 7, 3]),
        "context": "The EAC has emerged as Africa's most productive research bloc, anchored by Kenya and Uganda's mature trial infrastructure, KEMRI and MRC networks, and deep PEPFAR/Wellcome/Gates funding pipelines.",
        "refs": [REF_ALEMAYEHU, REF_NDOUNGA, REF_CTGOV]
    },
    {
        "slug": "west-african-ecowas", "title": "West African ECOWAS Corridor",
        "group": "geographic-equity", "paper_num": 28,
        "query": {"condition": None, "countries": ECOWAS[:8]},
        "stats": ["network_centrality", "hhi_index", "shannon_entropy", "bootstrap_ci", "gini_coefficient"],
        "charts": _charts([5, 0, 1, 9, 6, 4, 7, 3]),
        "context": "ECOWAS spans 15 nations with 400 million people, but Nigeria dominates the research corridor so heavily that other member states function as research satellites rather than sovereign partners.",
        "refs": [REF_DRAIN, REF_NDOUNGA, REF_CTGOV]
    },
    {
        "slug": "southern-african-arc", "title": "Southern African Research Arc",
        "group": "geographic-equity", "paper_num": 29,
        "query": {"condition": None, "countries": SADC[:8]},
        "stats": ["power_law_fit", "gini_coefficient", "bootstrap_ci", "lorenz", "shannon_entropy"],
        "charts": _charts([0, 1, 2, 7, 6, 9, 3, 12]),
        "context": "The Southern African arc is anchored by South Africa's world-class research infrastructure — SAMRC, Wits, UCT — but this dominance means that SADC neighbours receive spillover rather than sovereign capacity.",
        "refs": [REF_ALEMAYEHU, REF_CTGOV]
    },
    {
        "slug": "north-south-divide", "title": "North Africa vs Sub-Saharan Divide",
        "group": "geographic-equity", "paper_num": 30,
        "query": {"condition": None, "countries": NORTH_AFRICA},
        "stats": ["rate_ratio", "bayesian_rate", "theil_index", "bootstrap_ci", "chi_squared"],
        "charts": _charts([0, 7, 11, 3, 6, 1, 9, 4]),
        "context": "North Africa (Egypt, Morocco, Tunisia) operates in a fundamentally different research ecosystem than Sub-Saharan Africa — higher GDP, stronger regulatory frameworks, Mediterranean clinical trial networks, and proximity to European sponsors.",
        "refs": [REF_NDOUNGA, REF_DRAIN, REF_CTGOV]
    },
    {
        "slug": "distance-to-trial", "title": "Distance-to-Trial-Site Burden",
        "group": "geographic-equity", "paper_num": 31,
        "query": {"condition": None, "location": "Africa"},
        "stats": ["gini_coefficient", "linear_regression", "bootstrap_ci", "lorenz", "spearman_correlation"],
        "charts": _charts([0, 1, 10, 6, 9, 3, 7, 12]),
        "context": "For the average rural African, the nearest clinical trial site may be hundreds of kilometers away — a distance measured not in hours but in days of travel, multiple transport modes, and significant out-of-pocket costs.",
        "refs": [REF_NDOUNGA, REF_GBD, REF_CTGOV]
    },
    {
        "slug": "secondary-city-emergence", "title": "Secondary City Emergence",
        "group": "geographic-equity", "paper_num": 32,
        "query": {"condition": None, "location": "Africa"},
        "stats": ["poisson_rate", "changepoint_detection", "bootstrap_ci", "linear_regression", "arima_forecast"],
        "charts": _charts([6, 0, 7, 11, 3, 9, 10, 2]),
        "context": "Secondary cities like Mombasa, Kumasi, and Blantyre are beginning to emerge as trial sites, driven by growing university hospital capacity and sponsor interest in diverse recruitment beyond capital cities.",
        "refs": [REF_ALEMAYEHU, REF_CTGOV]
    },
    {
        "slug": "cross-border-networks", "title": "Cross-Border Trial Networks",
        "group": "geographic-equity", "paper_num": 33,
        "query": {"condition": None, "location": "Africa", "other": "multi-site OR multicenter"},
        "stats": ["network_centrality", "jaccard_similarity", "bootstrap_ci", "shannon_entropy", "hhi_index"],
        "charts": _charts([5, 0, 4, 9, 6, 8, 7, 3]),
        "context": "Cross-border trial networks in Africa are dominated by disease-specific consortia (EDCTP, EANETT) rather than sovereign African regulatory frameworks, meaning collaboration structures reflect donor priorities.",
        "refs": [REF_DRAIN, REF_NDOUNGA, REF_CTGOV]
    },
    {
        "slug": "climate-zone-patterns", "title": "Climate Zone Research Patterns",
        "group": "geographic-equity", "paper_num": 34,
        "query": {"condition": None, "location": "Africa"},
        "stats": ["chi_squared", "effect_size", "bootstrap_ci", "kl_divergence", "permutation"],
        "charts": _charts([0, 3, 4, 7, 9, 6, 12, 10]),
        "context": "Africa's climate zones determine disease burden — tropical zones have malaria and NTDs, arid zones face meningitis belts, Mediterranean zones see cardiovascular disease. Trial distribution should mirror this epidemiological geography.",
        "refs": [REF_GBD, REF_NDOUNGA, REF_CTGOV]
    },
    {
        "slug": "port-city-advantage", "title": "Port City Advantage",
        "group": "geographic-equity", "paper_num": 35,
        "query": {"condition": None, "location": "Africa"},
        "stats": ["odds_ratio", "bootstrap_ci", "rate_ratio", "chi_squared", "logistic_regression"],
        "charts": _charts([0, 2, 11, 3, 7, 9, 6, 10]),
        "context": "Port cities have a natural advantage for clinical trials: cold-chain logistics for biologics, international airport access for monitors, and the cosmopolitan healthcare infrastructure that colonial-era investment concentrated on the coast.",
        "refs": [REF_DRAIN, REF_CTGOV]
    },
    {
        "slug": "research-corridor-mapping", "title": "Research Corridor Mapping",
        "group": "geographic-equity", "paper_num": 36,
        "query": {"condition": None, "location": "Africa"},
        "stats": ["spearman_correlation", "linear_regression", "bootstrap_ci", "gini_coefficient", "lorenz"],
        "charts": _charts([0, 10, 1, 6, 9, 7, 3, 12]),
        "context": "Research corridors follow transport infrastructure — the Nairobi-Mombasa, Lagos-Ibadan, and Cairo-Alexandria axes host the majority of trials in their respective countries, creating linear research geographies.",
        "refs": [REF_NDOUNGA, REF_CTGOV]
    },
    {
        "slug": "linguistic-barrier", "title": "Linguistic Barrier Mapping",
        "group": "geographic-equity", "paper_num": 37,
        "query": {"condition": None, "location": "Africa"},
        "stats": ["mutual_information", "shannon_entropy", "chi_squared", "bootstrap_ci", "theil_index"],
        "charts": _charts([0, 4, 9, 7, 3, 6, 1, 12]),
        "context": "Africa's linguistic landscape — Arabic in the north, French in the west/center, English in the east/south, Portuguese in the lusophone states — creates invisible barriers to research collaboration and knowledge transfer.",
        "refs": [REF_ALEMAYEHU, REF_CTGOV]
    },
    {
        "slug": "population-density-mismatch", "title": "Population Density Mismatch",
        "group": "geographic-equity", "paper_num": 38,
        "query": {"condition": None, "location": "Africa"},
        "stats": ["spearman_correlation", "linear_regression", "lorenz", "bootstrap_ci", "gini_coefficient"],
        "charts": _charts([10, 1, 0, 6, 9, 3, 7, 12]),
        "context": "If trials were distributed by population density, Nigeria (220M) should host far more trials than Egypt (105M). The mismatch between population and trial density reveals that research access is determined by infrastructure rather than need.",
        "refs": [REF_NDOUNGA, REF_DRAIN, REF_CTGOV]
    },
    {
        "slug": "regional-economic-community", "title": "AU Regional Economic Community Gaps",
        "group": "geographic-equity", "paper_num": 39,
        "query": {"condition": None, "location": "Africa"},
        "stats": ["chi_squared", "effect_size", "bootstrap_ci", "shannon_entropy", "hhi_index"],
        "charts": _charts([9, 0, 4, 7, 3, 6, 1, 11]),
        "context": "The African Union recognizes 8 Regional Economic Communities, but their research productivity varies enormously — from SADC's strong South African anchor to ECCAS's near-total research void.",
        "refs": [REF_ALEMAYEHU, REF_NDOUNGA, REF_CTGOV]
    },
    {
        "slug": "zero-trial-nations", "title": "The Zero-Trial Nations",
        "group": "geographic-equity", "paper_num": 40,
        "query": {"condition": None, "location": "Africa"},
        "stats": ["bayesian_rate", "poisson_rate", "bootstrap_ci", "shannon_entropy", "kaplan_meier"],
        "charts": _charts([0, 14, 2, 7, 6, 9, 3, 1]),
        "context": "Several African nations have fewer than 5 lifetime clinical trial registrations — effectively zero participation in global evidence generation despite populations in the millions. These nations are invisible to evidence-based medicine.",
        "refs": [REF_NDOUNGA, REF_GBD, REF_CTGOV]
    },
]

# ═══════════════════════════════════════════════════════════
#  GROUP 2: HEALTH & DISEASE BURDEN (papers 21-60)
# ═══════════════════════════════════════════════════════════
HEALTH_PAPERS = [
    {"slug": "hiv-saturation-index", "title": "HIV Trial Saturation Index", "group": "health-disease", "paper_num": 21,
     "query": {"condition": "HIV"}, "stats": ["lorenz", "concentration_index", "rate_ratio", "bootstrap_ci", "poisson_rate"],
     "charts": _charts([1, 0, 2, 7, 6, 9, 3, 11]), "context": "HIV research dominates Africa's trial portfolio, yet even within HIV, trials concentrate in a handful of countries while high-prevalence nations in West and Central Africa remain underserved.", "refs": [REF_NDOUNGA, REF_CTGOV]},
    {"slug": "tb-coinfection-gap", "title": "Tuberculosis Co-Infection Gap", "group": "health-disease", "paper_num": 22,
     "query": {"condition": "tuberculosis"}, "stats": ["bayesian_rate", "rate_ratio", "bootstrap_ci", "chi_squared", "forest_plot"],
     "charts": _charts([2, 0, 3, 6, 7, 9, 4, 14]), "context": "TB kills more Africans than any other infectious disease, yet TB trials lag far behind HIV in volume, funding, and pharmaceutical industry interest.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "malaria-vaccine-pipeline", "title": "Malaria Vaccine Pipeline", "group": "health-disease", "paper_num": 23,
     "query": {"condition": "malaria vaccine"}, "stats": ["kaplan_meier", "bootstrap_ci", "rate_ratio", "poisson_rate", "arima_forecast"],
     "charts": _charts([14, 6, 0, 2, 7, 9, 3, 11]), "context": "The malaria vaccine pipeline — from RTS,S to R21 — represents one of Africa's most important research investments, but trial infrastructure remains concentrated in East African sites.", "refs": [REF_NDOUNGA, REF_GBD, REF_CTGOV]},
    {"slug": "sickle-cell-neglect", "title": "Sickle Cell Disease Neglect", "group": "health-disease", "paper_num": 24,
     "query": {"condition": "sickle cell disease"}, "stats": ["rate_ratio", "bootstrap_ci", "theil_index", "lorenz", "permutation"],
     "charts": _charts([1, 0, 2, 7, 3, 6, 9, 11]), "context": "Sickle cell disease affects more Africans than any other genetic condition, yet trial investment is a fraction of what cystic fibrosis receives in the US, reflecting whose diseases get funded.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "diabetes-epidemic-mismatch", "title": "Diabetes Epidemic Mismatch", "group": "health-disease", "paper_num": 25,
     "query": {"condition": "diabetes"}, "stats": ["linear_regression", "bootstrap_ci", "poisson_rate", "lorenz", "rate_ratio"],
     "charts": _charts([10, 1, 0, 6, 7, 9, 3, 2]), "context": "Africa's diabetes epidemic is accelerating faster than any other continent, driven by urbanization and dietary shifts, yet diabetes trial infrastructure barely exists outside South Africa and Egypt.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "hypertension-desert", "title": "Hypertension Trial Desert", "group": "health-disease", "paper_num": 26,
     "query": {"condition": "hypertension"}, "stats": ["poisson_rate", "rate_ratio", "bootstrap_ci", "lorenz", "gini_coefficient"],
     "charts": _charts([0, 1, 2, 6, 7, 9, 3, 11]), "context": "With 30-40% prevalence in many African populations, hypertension is the leading risk factor for cardiovascular death, yet trial investment is negligible compared to the disease burden.", "refs": [REF_SLIWA, REF_GBD, REF_CTGOV]},
    {"slug": "stroke-research-void", "title": "Stroke Research Void", "group": "health-disease", "paper_num": 27,
     "query": {"condition": "stroke"}, "stats": ["bayesian_rate", "bootstrap_ci", "rate_ratio", "shannon_entropy", "poisson_rate"],
     "charts": _charts([0, 2, 3, 6, 7, 9, 14, 11]), "context": "Stroke kills more young Africans than in any other region, with a median age of onset a decade earlier than in Europe, yet stroke trial infrastructure is virtually nonexistent.", "refs": [REF_SLIWA, REF_GBD, REF_CTGOV]},
    {"slug": "cancer-landscape", "title": "Cancer Trial Landscape", "group": "health-disease", "paper_num": 28,
     "query": {"condition": "cancer"}, "stats": ["hhi_index", "chi_squared", "bootstrap_ci", "theil_index", "lorenz"],
     "charts": _charts([4, 0, 1, 7, 6, 9, 3, 12]), "context": "Cancer is Africa's fastest-growing killer, but the trial landscape is dominated by HIV-related cancers (Kaposi, cervical) while the epidemiological transition brings rising breast, prostate, and colorectal cancers.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "breast-cancer-disparity", "title": "Breast Cancer Disparity", "group": "health-disease", "paper_num": 29,
     "query": {"condition": "breast cancer"}, "stats": ["odds_ratio", "bootstrap_ci", "rate_ratio", "chi_squared", "effect_size"],
     "charts": _charts([2, 0, 3, 6, 13, 9, 7, 11]), "context": "African women present with breast cancer at younger ages and more aggressive subtypes (triple-negative), yet the evidence base for treatment is derived almost entirely from older European patients.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "cervical-cancer-hpv", "title": "Cervical Cancer HPV Gap", "group": "health-disease", "paper_num": 30,
     "query": {"condition": "cervical cancer OR HPV"}, "stats": ["morans_i", "rate_ratio", "bootstrap_ci", "poisson_rate", "lorenz"],
     "charts": _charts([0, 1, 2, 6, 7, 9, 3, 10]), "context": "Cervical cancer is the leading cancer killer of African women, driven by HPV infection, yet vaccination and screening trial infrastructure is concentrated in East African research hubs.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "prostate-cancer-genomic", "title": "Prostate Cancer Genomic Divide", "group": "health-disease", "paper_num": 31,
     "query": {"condition": "prostate cancer"}, "stats": ["rate_ratio", "bootstrap_ci", "chi_squared", "shannon_entropy", "effect_size"],
     "charts": _charts([0, 2, 3, 4, 6, 9, 7, 12]), "context": "African men have the highest prostate cancer mortality globally, with distinct genomic profiles that require Africa-specific precision medicine trials rather than extrapolation from European data.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "childhood-cancer-neglect", "title": "Childhood Cancer Neglect", "group": "health-disease", "paper_num": 32,
     "query": {"condition": "pediatric cancer OR childhood cancer"}, "stats": ["poisson_rate", "rate_ratio", "bootstrap_ci", "bayesian_rate", "effect_size"],
     "charts": _charts([0, 2, 7, 6, 3, 9, 14, 11]), "context": "Childhood cancer survival in Africa is under 20% compared to 80%+ in high-income countries. The gap is driven by late diagnosis and treatment, but the trial infrastructure to test adapted protocols barely exists.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "mental-health-invisibility", "title": "Mental Health Invisibility", "group": "health-disease", "paper_num": 33,
     "query": {"condition": "depression OR anxiety OR psychosis OR mental health"}, "stats": ["shannon_entropy", "rate_ratio", "bootstrap_ci", "lorenz", "chi_squared"],
     "charts": _charts([1, 0, 3, 4, 6, 9, 7, 12]), "context": "Mental health disorders affect an estimated 100 million Africans, but mental health trial investment is among the lowest of any disease category, reflecting persistent stigma and health system neglect.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "epilepsy-treatment-gap", "title": "Epilepsy Treatment Gap", "group": "health-disease", "paper_num": 34,
     "query": {"condition": "epilepsy OR seizure"}, "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "lorenz", "arima_forecast"],
     "charts": _charts([0, 1, 2, 6, 7, 9, 3, 14]), "context": "The epilepsy treatment gap in Africa exceeds 80% — four out of five people with epilepsy receive no treatment — yet the trial pipeline for affordable antiepileptic regimens is nearly empty.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "ntd-atlas", "title": "Neglected Tropical Diseases Atlas", "group": "health-disease", "paper_num": 35,
     "query": {"condition": "neglected tropical disease OR NTD OR schistosomiasis OR onchocerciasis OR lymphatic filariasis"},
     "stats": ["jaccard_similarity", "hhi_index", "bootstrap_ci", "lorenz", "shannon_entropy"],
     "charts": _charts([0, 4, 1, 7, 6, 9, 3, 10]), "context": "Twenty NTDs collectively affect over 500 million Africans, yet most NTDs have fewer than 10 active trials each, making them the most neglected diseases in the most neglected continent.", "refs": [REF_GBD, REF_NDOUNGA, REF_CTGOV]},
    {"slug": "schistosomiasis-pipeline", "title": "Schistosomiasis Pipeline", "group": "health-disease", "paper_num": 36,
     "query": {"condition": "schistosomiasis OR bilharzia"}, "stats": ["poisson_rate", "arima_forecast", "bootstrap_ci", "rate_ratio", "changepoint_detection"],
     "charts": _charts([6, 0, 2, 7, 3, 9, 14, 11]), "context": "Schistosomiasis affects 200 million people, mostly children, with praziquantel as the sole treatment for 40 years. The pipeline for new drugs and a vaccine is critically thin.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "trypanosomiasis-last-mile", "title": "Trypanosomiasis Last Mile", "group": "health-disease", "paper_num": 37,
     "query": {"condition": "trypanosomiasis OR sleeping sickness"}, "stats": ["kaplan_meier", "bootstrap_ci", "poisson_rate", "bayesian_rate", "rate_ratio"],
     "charts": _charts([14, 0, 6, 2, 7, 9, 3, 11]), "context": "Human African trypanosomiasis is approaching elimination, but the last-mile challenge requires sustained trial investment in diagnostics and treatment for the most remote populations.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "amr-crisis", "title": "Antimicrobial Resistance Crisis", "group": "health-disease", "paper_num": 38,
     "query": {"condition": "antimicrobial resistance OR antibiotic resistance OR AMR"},
     "stats": ["arima_forecast", "bootstrap_ci", "rate_ratio", "poisson_rate", "logistic_growth"],
     "charts": _charts([6, 0, 2, 7, 10, 9, 3, 14]), "context": "AMR kills more people in Sub-Saharan Africa than anywhere else, yet the continent has the fewest AMR-specific trials, least surveillance data, and weakest antibiotic stewardship infrastructure.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "snake-envenomation", "title": "Snake Envenomation Silence", "group": "health-disease", "paper_num": 39,
     "query": {"condition": "snakebite OR snake envenomation OR antivenom"},
     "stats": ["poisson_rate", "rate_ratio", "bootstrap_ci", "permutation", "bayesian_rate"],
     "charts": _charts([0, 2, 7, 6, 3, 9, 14, 11]), "context": "Snakebite kills 30,000 Africans annually and disables 400,000 more, yet the global antivenom pipeline has collapsed and trial investment is near zero — making it the most neglected tropical emergency.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "ebola-preparedness", "title": "Ebola Preparedness Audit", "group": "health-disease", "paper_num": 40,
     "query": {"condition": "Ebola OR Marburg OR viral hemorrhagic fever"},
     "stats": ["interrupted_time_series", "bootstrap_ci", "rate_ratio", "bayesian_rate", "changepoint_detection"],
     "charts": _charts([6, 0, 2, 7, 14, 9, 3, 11]), "context": "Ebola preparedness trials surge during outbreaks then collapse between them, creating a boom-bust research cycle that leaves Africa permanently underprepared for the next emergence.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "mpox-response-equity", "title": "Mpox Response Equity", "group": "health-disease", "paper_num": 41,
     "query": {"condition": "mpox OR monkeypox"}, "stats": ["bayesian_rate", "bootstrap_ci", "rate_ratio", "chi_squared", "poisson_rate"],
     "charts": _charts([0, 2, 6, 7, 3, 9, 14, 11]), "context": "The 2022-2024 mpox response exposed stark equity gaps — vaccines and antivirals flowed to high-income countries while African nations with endemic clade I received minimal trial investment.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "neonatal-mortality-gap", "title": "Neonatal Mortality Gap", "group": "health-disease", "paper_num": 42,
     "query": {"condition": "neonatal OR newborn"}, "stats": ["rate_ratio", "lorenz", "bootstrap_ci", "poisson_rate", "gini_coefficient"],
     "charts": _charts([1, 0, 2, 6, 7, 9, 3, 14]), "context": "Sub-Saharan Africa accounts for 43% of global neonatal deaths, yet neonatal trial investment is a fraction of what's needed to test context-appropriate interventions for low-resource settings.", "refs": [REF_WHO_MATERNAL, REF_GBD, REF_CTGOV]},
    {"slug": "nutrition-stunting", "title": "Nutrition & Stunting Trials", "group": "health-disease", "paper_num": 43,
     "query": {"condition": "malnutrition OR stunting OR wasting OR nutrition"},
     "stats": ["linear_regression", "bootstrap_ci", "rate_ratio", "poisson_rate", "arima_forecast"],
     "charts": _charts([6, 0, 10, 2, 7, 9, 3, 11]), "context": "Stunting affects 30% of African children under five, with lifelong consequences for cognitive development and economic productivity, yet nutrition intervention trials remain underfunded.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "respiratory-infection", "title": "Respiratory Infection Pipeline", "group": "health-disease", "paper_num": 44,
     "query": {"condition": "pneumonia OR lower respiratory infection"},
     "stats": ["poisson_rate", "arima_forecast", "bootstrap_ci", "rate_ratio", "changepoint_detection"],
     "charts": _charts([6, 0, 2, 7, 3, 9, 14, 12]), "context": "Pneumonia is the leading killer of African children under five, yet pediatric pneumonia trial investment pales compared to adult respiratory research driven by COVID.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "diarrheal-disease-deficit", "title": "Diarrheal Disease Research Deficit", "group": "health-disease", "paper_num": 45,
     "query": {"condition": "diarrhea OR cholera OR rotavirus"},
     "stats": ["poisson_rate", "bootstrap_ci", "rate_ratio", "bayesian_rate", "morans_i"],
     "charts": _charts([0, 2, 6, 7, 3, 9, 14, 11]), "context": "Diarrheal diseases kill 500,000 African children annually despite proven interventions (ORS, zinc, rotavirus vaccine), yet the trial pipeline for improved treatments remains thin.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "kidney-disease-silence", "title": "Kidney Disease Silence", "group": "health-disease", "paper_num": 46,
     "query": {"condition": "chronic kidney disease OR acute kidney injury OR nephrology"},
     "stats": ["rate_ratio", "bootstrap_ci", "kaplan_meier", "poisson_rate", "bayesian_rate"],
     "charts": _charts([14, 0, 2, 6, 7, 9, 3, 11]), "context": "CKD prevalence in Africa is estimated at 13-16%, driven by hypertension, diabetes, and HIV nephropathy, yet renal trial investment is negligible and dialysis access is under 5%.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "liver-hepatitis-b", "title": "Liver Disease & Hepatitis B", "group": "health-disease", "paper_num": 47,
     "query": {"condition": "hepatitis B OR hepatitis C OR liver disease"},
     "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "arima_forecast", "lorenz"],
     "charts": _charts([7, 0, 1, 6, 2, 9, 3, 14]), "context": "Africa carries 25% of the global hepatitis B burden, yet the cascade of care — screening, diagnosis, treatment — has trial gaps at every stage, especially in cure-focused research.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "eye-health-trachoma", "title": "Eye Health & Trachoma", "group": "health-disease", "paper_num": 48,
     "query": {"condition": "trachoma OR ophthalmology OR blindness OR cataract"},
     "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "bayesian_rate", "arima_forecast"],
     "charts": _charts([0, 6, 2, 7, 3, 9, 14, 11]), "context": "Trachoma remains the leading infectious cause of blindness globally, concentrated in Africa, yet the elimination endgame requires sustained trial investment in the SAFE strategy.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "surgical-trials-void", "title": "Surgical Trials Void", "group": "health-disease", "paper_num": 49,
     "query": {"condition": "surgery OR surgical OR anesthesia", "other": "INTERVENTIONAL"},
     "stats": ["rate_ratio", "bootstrap_ci", "chi_squared", "poisson_rate", "effect_size"],
     "charts": _charts([0, 2, 7, 3, 6, 9, 11, 4]), "context": "Five billion people lack access to safe surgery, with Africa bearing the greatest burden, yet surgical trials are among the rarest of all trial types on the continent.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "traditional-medicine", "title": "Traditional Medicine Integration", "group": "health-disease", "paper_num": 50,
     "query": {"condition": "traditional medicine OR herbal OR complementary medicine"},
     "stats": ["chi_squared", "bootstrap_ci", "shannon_entropy", "network_centrality", "rate_ratio"],
     "charts": _charts([5, 0, 4, 7, 3, 9, 6, 12]), "context": "80% of Africans use traditional medicine as first-line care, yet rigorous clinical trials of traditional remedies remain rare, creating a parallel healthcare system operating without an evidence base.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "vaccine-equity-audit", "title": "Vaccine Equity Audit", "group": "health-disease", "paper_num": 51,
     "query": {"condition": "vaccine"}, "stats": ["hhi_index", "bootstrap_ci", "rate_ratio", "theil_index", "arima_forecast"],
     "charts": _charts([4, 0, 6, 7, 1, 9, 3, 11]), "context": "Africa manufactures less than 1% of the vaccines it uses, and vaccine trial distribution reflects this dependency — most trials are sponsored by foreign manufacturers testing products for global markets.", "refs": [REF_NDOUNGA, REF_CTGOV]},
    {"slug": "rheumatic-heart-disease", "title": "Rheumatic Heart Disease", "group": "health-disease", "paper_num": 52,
     "query": {"condition": "rheumatic heart disease OR rheumatic fever"},
     "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "bayesian_rate", "lorenz"],
     "charts": _charts([0, 1, 2, 6, 7, 9, 3, 14]), "context": "RHD kills 240,000 people annually, mostly in Africa, and is entirely preventable with penicillin prophylaxis — yet trial investment in delivery strategies is almost nonexistent.", "refs": [REF_SLIWA, REF_GBD, REF_CTGOV]},
    {"slug": "road-traffic-injury", "title": "Road Traffic Injury Trials", "group": "health-disease", "paper_num": 53,
     "query": {"condition": "trauma OR road traffic injury OR emergency medicine"},
     "stats": ["poisson_rate", "bootstrap_ci", "rate_ratio", "arima_forecast", "chi_squared"],
     "charts": _charts([0, 6, 2, 7, 3, 9, 14, 11]), "context": "Africa has the highest road traffic fatality rate globally, yet emergency medicine and trauma trial investment is negligible, reflecting a health system built around infectious disease.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "substance-use-disorders", "title": "Substance Use Disorders", "group": "health-disease", "paper_num": 54,
     "query": {"condition": "alcohol OR tobacco OR substance use OR addiction"},
     "stats": ["spearman_correlation", "bootstrap_ci", "rate_ratio", "lorenz", "poisson_rate"],
     "charts": _charts([10, 1, 0, 6, 7, 9, 3, 12]), "context": "Alcohol use disorders alone account for 4% of Africa's disease burden, yet addiction medicine trials are virtually absent from the continent's research portfolio.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "maternal-anemia", "title": "Maternal Anemia Pipeline", "group": "health-disease", "paper_num": 55,
     "query": {"condition": "anemia AND pregnancy OR iron supplementation"},
     "stats": ["rate_ratio", "bootstrap_ci", "linear_regression", "poisson_rate", "arima_forecast"],
     "charts": _charts([6, 0, 2, 10, 7, 9, 3, 14]), "context": "Anemia affects 40% of pregnant African women, contributing to maternal mortality and low birth weight, yet iron supplementation trial designs rarely account for malaria co-endemicity.", "refs": [REF_WHO_MATERNAL, REF_GBD, REF_CTGOV]},
    {"slug": "preterm-birth", "title": "Preterm Birth Interventions", "group": "health-disease", "paper_num": 56,
     "query": {"condition": "preterm birth OR prematurity OR NICU"},
     "stats": ["kaplan_meier", "bootstrap_ci", "rate_ratio", "poisson_rate", "bayesian_rate"],
     "charts": _charts([14, 0, 2, 6, 7, 9, 3, 11]), "context": "Africa has the highest preterm birth rate globally, yet NICU capacity is critically limited and the trial pipeline for low-resource neonatal interventions is thin.", "refs": [REF_WHO_MATERNAL, REF_GBD, REF_CTGOV]},
    {"slug": "contraception-family-planning", "title": "Contraception & Family Planning", "group": "health-disease", "paper_num": 57,
     "query": {"condition": "contraception OR family planning OR reproductive health"},
     "stats": ["theil_index", "bootstrap_ci", "rate_ratio", "lorenz", "poisson_rate"],
     "charts": _charts([1, 0, 2, 6, 7, 9, 3, 11]), "context": "Unmet need for family planning affects 60 million African women, yet contraception trial investment focuses on new methods rather than delivery strategies for existing ones.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "palliative-care-desert", "title": "Palliative Care Desert", "group": "health-disease", "paper_num": 58,
     "query": {"condition": "palliative care OR end of life OR hospice"},
     "stats": ["poisson_rate", "bootstrap_ci", "rate_ratio", "bayesian_rate", "arima_forecast"],
     "charts": _charts([0, 6, 2, 7, 3, 9, 14, 11]), "context": "Less than 5% of Africans who need palliative care receive it, and morphine availability is critically restricted, yet the trial pipeline for affordable pain management is nearly empty.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "aging-geriatric", "title": "Aging & Geriatric Medicine", "group": "health-disease", "paper_num": 59,
     "query": {"condition": "elderly OR geriatric OR aging", "other": "INTERVENTIONAL"},
     "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "arima_forecast", "linear_regression"],
     "charts": _charts([6, 0, 2, 10, 7, 9, 3, 14]), "context": "Africa's over-60 population will triple by 2050, yet geriatric medicine trials are almost nonexistent — the continent is ageing into an evidence vacuum.", "refs": [REF_GBD, REF_CTGOV]},
    {"slug": "one-health-zoonotic", "title": "One Health & Zoonotic Interface", "group": "health-disease", "paper_num": 60,
     "query": {"condition": "zoonotic OR brucellosis OR Rift Valley fever OR rabies"},
     "stats": ["network_centrality", "bootstrap_ci", "rate_ratio", "shannon_entropy", "poisson_rate"],
     "charts": _charts([5, 0, 6, 7, 3, 9, 4, 14]), "context": "Africa is the global hotspot for zoonotic spillover events, but One Health trial infrastructure — integrating human, animal, and environmental health — barely exists.", "refs": [REF_GBD, REF_CTGOV]},
]

# ═══════════════════════════════════════════════════════════
#  GROUP 3: GOVERNANCE, JUSTICE & SOVEREIGNTY (papers 21-45)
# ═══════════════════════════════════════════════════════════
GOV_PAPERS = [
    {"slug": "informed-consent-language", "title": "Informed Consent Language Audit", "group": "governance-justice", "paper_num": 21,
     "query": {"condition": None, "location": "Africa"}, "stats": ["shannon_entropy", "chi_squared", "theil_index", "bootstrap_ci", "rate_ratio"],
     "charts": _charts([4, 0, 9, 7, 3, 6, 1, 12]), "context": "Informed consent in African trials often occurs in languages that participants do not fully understand, creating a fundamental ethical gap between regulatory compliance and genuine comprehension.", "refs": [REF_HEDT, REF_CTGOV]},
    {"slug": "participant-compensation", "title": "Participant Compensation Ethics", "group": "governance-justice", "paper_num": 22,
     "query": {"condition": None, "location": "Africa"}, "stats": ["gini_coefficient", "bootstrap_ci", "rate_ratio", "permutation", "lorenz"],
     "charts": _charts([1, 0, 3, 7, 11, 9, 6, 2]), "context": "Trial participant compensation in Africa raises unique ethical tensions — too little exploits poverty, too much creates undue inducement — and standards vary wildly across countries.", "refs": [REF_LANG, REF_CTGOV]},
    {"slug": "gender-trial-leadership", "title": "Gender in Trial Leadership", "group": "governance-justice", "paper_num": 23,
     "query": {"condition": None, "location": "Africa"}, "stats": ["odds_ratio", "bootstrap_ci", "chi_squared", "rate_ratio", "arima_forecast"],
     "charts": _charts([2, 0, 6, 11, 7, 9, 3, 4]), "context": "Female principal investigators lead a minority of African trials despite women comprising the majority of healthcare workers, reflecting structural barriers in academic promotion.", "refs": [REF_HEDT, REF_CTGOV]},
    {"slug": "ethics-committee-capacity", "title": "Ethics Committee Capacity", "group": "governance-justice", "paper_num": 24,
     "query": {"condition": None, "location": "Africa"}, "stats": ["poisson_rate", "bootstrap_ci", "rate_ratio", "bayesian_rate", "linear_regression"],
     "charts": _charts([7, 0, 6, 3, 9, 2, 14, 11]), "context": "Many African countries have fewer than 5 accredited ethics committees reviewing hundreds of protocols, creating bottlenecks that delay research and may compromise review quality.", "refs": [REF_LANG, REF_CTGOV]},
    {"slug": "post-trial-drug-access", "title": "Post-Trial Drug Access", "group": "governance-justice", "paper_num": 25,
     "query": {"condition": None, "location": "Africa"}, "stats": ["kaplan_meier", "bootstrap_ci", "rate_ratio", "chi_squared", "bayesian_rate"],
     "charts": _charts([14, 0, 2, 6, 7, 9, 3, 11]), "context": "Post-trial access — the obligation to provide beneficial treatments after a trial ends — is poorly enforced in Africa, leaving participants who helped prove a drug's efficacy unable to access it.", "refs": [REF_LANG, REF_HEDT, REF_CTGOV]},
    {"slug": "colonial-legacy-sponsorship", "title": "Colonial Legacy in Sponsorship", "group": "governance-justice", "paper_num": 26,
     "query": {"condition": None, "location": "Africa"}, "stats": ["network_centrality", "chi_squared", "bootstrap_ci", "mutual_information", "hhi_index"],
     "charts": _charts([5, 8, 0, 4, 7, 9, 6, 3]), "context": "Former colonial powers remain disproportionately represented as sponsors in their former colonies — France in Francophone Africa, UK in Anglophone Africa — perpetuating dependency structures.", "refs": [REF_HEDT, REF_DRAIN, REF_CTGOV]},
    {"slug": "south-south-collaboration", "title": "South-South Collaboration Index", "group": "governance-justice", "paper_num": 27,
     "query": {"condition": None, "location": "Africa", "other": "India OR China OR Brazil"},
     "stats": ["arima_forecast", "bootstrap_ci", "rate_ratio", "poisson_rate", "logistic_growth"],
     "charts": _charts([6, 0, 10, 7, 3, 9, 11, 2]), "context": "India, China, and Brazil are emerging as alternative research partners for Africa, potentially disrupting the traditional North-South axis of clinical trial sponsorship.", "refs": [REF_DRAIN, REF_CTGOV]},
    {"slug": "open-access-equity", "title": "Open Access Publication Equity", "group": "governance-justice", "paper_num": 28,
     "query": {"condition": None, "location": "Africa"}, "stats": ["chi_squared", "rate_ratio", "bootstrap_ci", "lorenz", "odds_ratio"],
     "charts": _charts([11, 0, 1, 2, 7, 9, 6, 3]), "context": "African researchers face a double bind: publish in high-impact paywalled journals for career advancement, or choose open access to benefit local readers — with OA article processing charges often unaffordable.", "refs": [REF_HEDT, REF_CTGOV]},
    {"slug": "funding-flow-cartography", "title": "Funding Flow Cartography", "group": "governance-justice", "paper_num": 29,
     "query": {"condition": None, "location": "Africa"}, "stats": ["hhi_index", "theil_index", "bootstrap_ci", "lorenz", "gini_coefficient"],
     "charts": _charts([8, 0, 1, 7, 4, 9, 6, 3]), "context": "Global health funding for African trials flows through a handful of channels — NIH, Wellcome, Gates, EDCTP — creating concentration risk and agenda-setting power for a few institutions.", "refs": [REF_DRAIN, REF_LANG, REF_CTGOV]},
    {"slug": "community-engagement-depth", "title": "Community Engagement Depth", "group": "governance-justice", "paper_num": 30,
     "query": {"condition": None, "location": "Africa", "other": "community engagement OR community advisory"},
     "stats": ["rate_ratio", "bootstrap_ci", "chi_squared", "arima_forecast", "poisson_rate"],
     "charts": _charts([6, 0, 7, 3, 9, 2, 11, 4]), "context": "Meaningful community engagement goes beyond tokenistic community advisory boards — it requires genuine power-sharing, which most African trial protocols do not demonstrate.", "refs": [REF_HEDT, REF_CTGOV]},
    {"slug": "benefit-sharing-mechanisms", "title": "Benefit Sharing Mechanisms", "group": "governance-justice", "paper_num": 31,
     "query": {"condition": None, "location": "Africa"}, "stats": ["chi_squared", "bootstrap_ci", "rate_ratio", "bayesian_rate", "arima_forecast"],
     "charts": _charts([7, 0, 6, 3, 9, 2, 11, 4]), "context": "Benefit-sharing — ensuring that communities hosting trials receive tangible benefits beyond the research itself — is a Nagoya Protocol principle rarely operationalized in clinical research.", "refs": [REF_LANG, REF_CTGOV]},
    {"slug": "insurance-indemnity-gaps", "title": "Insurance & Indemnity Gaps", "group": "governance-justice", "paper_num": 32,
     "query": {"condition": None, "location": "Africa"}, "stats": ["rate_ratio", "bootstrap_ci", "chi_squared", "odds_ratio", "permutation"],
     "charts": _charts([11, 0, 2, 7, 3, 9, 6, 4]), "context": "Clinical trial insurance and participant indemnity provisions in Africa are often inadequate or absent, leaving trial participants without recourse for research-related injuries.", "refs": [REF_LANG, REF_CTGOV]},
    {"slug": "pediatric-consent-complexity", "title": "Pediatric Consent Complexity", "group": "governance-justice", "paper_num": 33,
     "query": {"condition": "pediatric OR child", "location": "Africa"},
     "stats": ["chi_squared", "bootstrap_ci", "rate_ratio", "bayesian_rate", "odds_ratio"],
     "charts": _charts([9, 0, 2, 7, 3, 6, 11, 4]), "context": "Pediatric trials in Africa face unique consent challenges: child assent norms vary by culture, parental literacy affects comprehension, and extended family decision-making structures may not align with Western consent models.", "refs": [REF_LANG, REF_CTGOV]},
    {"slug": "vulnerable-population-protections", "title": "Vulnerable Population Protections", "group": "governance-justice", "paper_num": 34,
     "query": {"condition": None, "location": "Africa"}, "stats": ["odds_ratio", "permutation", "bootstrap_ci", "chi_squared", "rate_ratio"],
     "charts": _charts([2, 0, 3, 7, 9, 6, 11, 4]), "context": "Refugees, prisoners, pregnant women, and other vulnerable populations in Africa often face either over-protection (blanket exclusion from trials) or under-protection (inadequate safeguards when included).", "refs": [REF_LANG, REF_HEDT, REF_CTGOV]},
    {"slug": "publication-lag-penalty", "title": "Publication Lag Penalty", "group": "governance-justice", "paper_num": 35,
     "query": {"condition": None, "location": "Africa"}, "stats": ["kaplan_meier", "bootstrap_ci", "rate_ratio", "linear_regression", "bayesian_rate"],
     "charts": _charts([14, 6, 0, 2, 7, 9, 3, 11]), "context": "African trials take longer to publish than trials from other regions, creating a delay penalty that means African evidence arrives too late to influence treatment guidelines.", "refs": [REF_HEDT, REF_CTGOV]},
    {"slug": "predatory-journal-risk", "title": "Predatory Journal Risk", "group": "governance-justice", "paper_num": 36,
     "query": {"condition": None, "location": "Africa"}, "stats": ["bayesian_rate", "bootstrap_ci", "rate_ratio", "shannon_entropy", "chi_squared"],
     "charts": _charts([13, 0, 6, 7, 3, 9, 4, 12]), "context": "African researchers face higher exposure to predatory journals due to pay-to-publish pressure, limited institutional library support, and the publish-or-perish academic culture imported from the Global North.", "refs": [REF_HEDT, REF_CTGOV]},
    {"slug": "data-sharing-compliance", "title": "Data Sharing Compliance", "group": "governance-justice", "paper_num": 37,
     "query": {"condition": None, "location": "Africa"}, "stats": ["chi_squared", "arima_forecast", "bootstrap_ci", "rate_ratio", "logistic_growth"],
     "charts": _charts([6, 0, 7, 3, 11, 9, 2, 4]), "context": "Data sharing mandates from funders and journals are creating new tensions in Africa — between transparency goals and data sovereignty concerns about Northern institutions mining African datasets.", "refs": [REF_HEDT, REF_CTGOV]},
    {"slug": "safety-reporting-integrity", "title": "Whistleblower & Safety Reporting", "group": "governance-justice", "paper_num": 38,
     "query": {"condition": None, "location": "Africa"}, "stats": ["benford_test", "bootstrap_ci", "rate_ratio", "chi_squared", "poisson_rate"],
     "charts": _charts([13, 0, 7, 3, 6, 9, 2, 4]), "context": "Adverse event reporting in African trials may be compromised by limited pharmacovigilance infrastructure, under-trained site staff, and cultural barriers to reporting negative outcomes.", "refs": [REF_LANG, REF_CTGOV]},
    {"slug": "local-manufacturing", "title": "Local Manufacturing Capacity", "group": "governance-justice", "paper_num": 39,
     "query": {"condition": None, "location": "Africa", "other": "locally manufactured OR local production"},
     "stats": ["spearman_correlation", "bootstrap_ci", "rate_ratio", "poisson_rate", "linear_regression"],
     "charts": _charts([10, 0, 6, 7, 3, 9, 11, 2]), "context": "Africa manufactures less than 2% of the medicines it consumes. Trials using locally manufactured products could build pharmaceutical sovereignty, but they remain extremely rare.", "refs": [REF_DRAIN, REF_CTGOV]},
    {"slug": "au-health-strategy-alignment", "title": "AU Health Strategy Alignment", "group": "governance-justice", "paper_num": 40,
     "query": {"condition": None, "location": "Africa"}, "stats": ["jaccard_similarity", "bootstrap_ci", "chi_squared", "shannon_entropy", "rate_ratio"],
     "charts": _charts([9, 0, 4, 7, 3, 6, 1, 11]), "context": "The AU Agenda 2063 health targets prioritize infectious disease, maternal health, and health system strengthening — but Africa's trial portfolio only partially aligns with these continental priorities.", "refs": [REF_ALEMAYEHU, REF_CTGOV]},
    {"slug": "youth-researcher-pipeline", "title": "Youth Researcher Pipeline", "group": "governance-justice", "paper_num": 41,
     "query": {"condition": None, "location": "Africa"}, "stats": ["arima_forecast", "bootstrap_ci", "poisson_rate", "linear_regression", "logistic_growth"],
     "charts": _charts([6, 0, 7, 10, 3, 9, 11, 14]), "context": "Africa's median age is 19, yet the research leadership pipeline fails to translate this demographic dividend into a new generation of investigators who could build sovereign research capacity.", "refs": [REF_HEDT, REF_CTGOV]},
    {"slug": "diaspora-investigator-networks", "title": "Diaspora Investigator Networks", "group": "governance-justice", "paper_num": 42,
     "query": {"condition": None, "location": "Africa"}, "stats": ["network_centrality", "bootstrap_ci", "jaccard_similarity", "shannon_entropy", "rate_ratio"],
     "charts": _charts([5, 0, 4, 7, 9, 6, 3, 8]), "context": "African diaspora researchers in Northern institutions serve as bridge figures — connecting African trial sites with global networks — but their role can perpetuate dependency rather than build sovereignty.", "refs": [REF_HEDT, REF_DRAIN, REF_CTGOV]},
    {"slug": "institutional-review-bottlenecks", "title": "Institutional Review Bottlenecks", "group": "governance-justice", "paper_num": 43,
     "query": {"condition": None, "location": "Africa"}, "stats": ["poisson_rate", "bootstrap_ci", "bayesian_rate", "rate_ratio", "linear_regression"],
     "charts": _charts([7, 0, 6, 3, 9, 14, 2, 11]), "context": "Multi-site trials in Africa face serial ethics review across multiple national committees, creating delays that can exceed 18 months and discourage sponsors from including African sites.", "refs": [REF_LANG, REF_CTGOV]},
    {"slug": "registration-transparency", "title": "Trial Registration Transparency Score", "group": "governance-justice", "paper_num": 44,
     "query": {"condition": None, "location": "Africa"}, "stats": ["chi_squared", "bootstrap_ci", "logistic_growth", "rate_ratio", "arima_forecast"],
     "charts": _charts([6, 0, 7, 9, 3, 11, 2, 4]), "context": "Prospective trial registration — registering before the first participant is enrolled — is an ICMJE requirement that many African trials fail to meet, undermining the integrity of the evidence base.", "refs": [REF_CHAN, REF_CTGOV]},
    {"slug": "decolonising-research", "title": "Decolonising Clinical Research", "group": "governance-justice", "paper_num": 45,
     "query": {"condition": None, "location": "Africa"}, "stats": ["shannon_entropy", "theil_index", "bootstrap_ci", "gini_coefficient", "network_centrality"],
     "charts": _charts([9, 0, 5, 1, 4, 7, 8, 3]), "context": "Decolonising clinical research means shifting from Africa as a data source for Northern analysis to Africa as a sovereign knowledge producer — a transformation that requires structural, not cosmetic, change.", "refs": [REF_HEDT, REF_LANG, REF_CTGOV]},
]

# ═══════════════════════════════════════════════════════════
#  GROUP 4: METHODS, DESIGN & RESEARCH SYSTEMS (papers 21-45)
# ═══════════════════════════════════════════════════════════
METHODS_PAPERS = [
    {"slug": "adaptive-design-adoption", "title": "Adaptive Design Adoption Curve", "group": "methods-systems", "paper_num": 21,
     "query": {"condition": None, "location": "Africa", "other": "adaptive design OR adaptive trial"},
     "stats": ["logistic_growth", "bootstrap_ci", "rate_ratio", "arima_forecast", "poisson_rate"],
     "charts": _charts([6, 0, 10, 7, 3, 9, 2, 11]), "context": "Adaptive trial designs could benefit Africa most — allowing mid-trial modifications based on emerging data — yet adoption lags decades behind high-income countries.", "refs": [REF_CHAN, REF_CTGOV]},
    {"slug": "platform-trial-readiness", "title": "Platform Trial Readiness", "group": "methods-systems", "paper_num": 22,
     "query": {"condition": None, "location": "Africa", "other": "platform trial OR master protocol OR basket"},
     "stats": ["rate_ratio", "bootstrap_ci", "chi_squared", "poisson_rate", "bayesian_rate"],
     "charts": _charts([9, 0, 2, 7, 3, 6, 11, 14]), "context": "Platform trials like RECOVERY proved their value in COVID but require standing infrastructure that Africa largely lacks — networked sites, central randomization, real-time data systems.", "refs": [REF_CHAN, REF_CTGOV]},
    {"slug": "bayesian-trial-penetration", "title": "Bayesian Trial Penetration", "group": "methods-systems", "paper_num": 23,
     "query": {"condition": None, "location": "Africa", "other": "bayesian"},
     "stats": ["bayesian_rate", "bootstrap_ci", "rate_ratio", "arima_forecast", "poisson_rate"],
     "charts": _charts([6, 0, 2, 7, 9, 3, 14, 11]), "context": "Bayesian methods are ideally suited for Africa's small-sample reality — incorporating prior knowledge to strengthen inference — yet Bayesian trial designs remain extremely rare on the continent.", "refs": [REF_CHAN, REF_CTGOV]},
    {"slug": "pragmatic-explanatory-spectrum", "title": "Pragmatic vs Explanatory Spectrum", "group": "methods-systems", "paper_num": 24,
     "query": {"condition": None, "location": "Africa"}, "stats": ["shannon_entropy", "bootstrap_ci", "chi_squared", "rate_ratio", "radar_scoring"],
     "charts": _charts([9, 0, 3, 4, 7, 6, 12, 2]), "context": "Africa needs pragmatic trials that test interventions under real-world conditions, yet most African trials use explanatory designs borrowed from well-resourced settings.", "refs": [REF_CHAN, REF_CTGOV]},
    {"slug": "digital-health-explosion", "title": "Digital Health Trial Explosion", "group": "methods-systems", "paper_num": 25,
     "query": {"condition": None, "location": "Africa", "other": "mHealth OR telemedicine OR digital health OR mobile health"},
     "stats": ["arima_forecast", "logistic_growth", "bootstrap_ci", "rate_ratio", "poisson_rate"],
     "charts": _charts([6, 0, 10, 7, 3, 9, 2, 11]), "context": "Africa's mobile phone penetration (80%+) creates a unique opportunity for digital health trials that could leapfrog traditional clinical infrastructure.", "refs": [REF_ALEMAYEHU, REF_CTGOV]},
    {"slug": "ai-ml-trials", "title": "AI & Machine Learning in Trials", "group": "methods-systems", "paper_num": 26,
     "query": {"condition": None, "location": "Africa", "other": "artificial intelligence OR machine learning OR deep learning"},
     "stats": ["logistic_growth", "bootstrap_ci", "rate_ratio", "arima_forecast", "poisson_rate"],
     "charts": _charts([6, 0, 10, 7, 3, 9, 2, 14]), "context": "AI/ML-augmented trial designs are emerging globally but barely present in Africa, risking a new digital divide in research methodology that could further marginalize the continent.", "refs": [REF_CTGOV]},
    {"slug": "biomarker-endpoint-quality", "title": "Biomarker Endpoint Quality", "group": "methods-systems", "paper_num": 27,
     "query": {"condition": None, "location": "Africa", "other": "biomarker"},
     "stats": ["rate_ratio", "bootstrap_ci", "chi_squared", "spearman_correlation", "linear_regression"],
     "charts": _charts([10, 0, 2, 7, 3, 9, 6, 4]), "context": "Biomarker-driven trials enable precision medicine and faster drug development, but Africa's limited laboratory infrastructure constrains biomarker endpoint adoption.", "refs": [REF_CHAN, REF_CTGOV]},
    {"slug": "composite-endpoint-complexity", "title": "Composite Endpoint Complexity", "group": "methods-systems", "paper_num": 28,
     "query": {"condition": None, "location": "Africa"}, "stats": ["shannon_entropy", "hhi_index", "bootstrap_ci", "rate_ratio", "chi_squared"],
     "charts": _charts([4, 0, 9, 7, 3, 6, 2, 12]), "context": "Composite endpoints increase statistical power but can mask clinically important differences between components — a particular risk when endpoints validated in Northern populations may not apply in Africa.", "refs": [REF_CHAN, REF_CTGOV]},
    {"slug": "patient-reported-outcomes", "title": "Patient-Reported Outcomes Gap", "group": "methods-systems", "paper_num": 29,
     "query": {"condition": None, "location": "Africa", "other": "patient reported outcome OR quality of life OR PRO"},
     "stats": ["rate_ratio", "bootstrap_ci", "arima_forecast", "poisson_rate", "chi_squared"],
     "charts": _charts([6, 0, 2, 7, 3, 9, 11, 4]), "context": "Patient-reported outcomes capture what matters to patients, but most PRO instruments are developed and validated in English-speaking, high-income populations and may not be culturally appropriate for African contexts.", "refs": [REF_CHAN, REF_CTGOV]},
    {"slug": "sample-size-adequacy", "title": "Sample Size Adequacy Audit", "group": "methods-systems", "paper_num": 30,
     "query": {"condition": None, "location": "Africa"}, "stats": ["rate_ratio", "bootstrap_ci", "linear_regression", "poisson_rate", "chi_squared"],
     "charts": _charts([10, 0, 2, 13, 7, 9, 3, 6]), "context": "Underpowered trials waste resources and participants' altruism by producing inconclusive results, yet many African trials fail to achieve their planned enrollment.", "refs": [REF_CHAN, REF_CTGOV]},
    {"slug": "statistical-analysis-plan", "title": "Statistical Analysis Plan Depth", "group": "methods-systems", "paper_num": 31,
     "query": {"condition": None, "location": "Africa"}, "stats": ["chi_squared", "bootstrap_ci", "rate_ratio", "bayesian_rate", "shannon_entropy"],
     "charts": _charts([4, 0, 9, 7, 3, 6, 2, 11]), "context": "A pre-specified SAP prevents outcome switching and p-hacking, but SAP completeness in African trials lags behind global standards, partly due to limited biostatistics capacity.", "refs": [REF_CHAN, REF_CTGOV]},
    {"slug": "randomisation-quality", "title": "Randomisation Quality", "group": "methods-systems", "paper_num": 32,
     "query": {"condition": None, "location": "Africa"}, "stats": ["chi_squared", "bootstrap_ci", "rate_ratio", "odds_ratio", "permutation"],
     "charts": _charts([2, 0, 9, 3, 7, 6, 11, 4]), "context": "Proper randomization — allocation concealment and sequence generation — is the gold standard for bias prevention, but reporting of randomization methods in African trials is often incomplete.", "refs": [REF_CHAN, REF_CTGOV]},
    {"slug": "blinding-architecture", "title": "Blinding Architecture", "group": "methods-systems", "paper_num": 33,
     "query": {"condition": None, "location": "Africa"}, "stats": ["chi_squared", "bootstrap_ci", "rate_ratio", "odds_ratio", "poisson_rate"],
     "charts": _charts([7, 0, 2, 3, 9, 6, 11, 4]), "context": "Blinding integrity in African trials faces practical challenges: matching placebos may be unavailable locally, and cultural expectations about treatment effects can compromise the blind.", "refs": [REF_CHAN, REF_CTGOV]},
    {"slug": "intention-to-treat-compliance", "title": "Intention-to-Treat Compliance", "group": "methods-systems", "paper_num": 34,
     "query": {"condition": None, "location": "Africa"}, "stats": ["chi_squared", "bootstrap_ci", "rate_ratio", "odds_ratio", "effect_size"],
     "charts": _charts([11, 0, 2, 7, 3, 9, 6, 4]), "context": "ITT analysis preserves the benefits of randomization, but high loss-to-follow-up rates in African trials (often 15-30%) can undermine ITT validity and necessitate sensitivity analyses.", "refs": [REF_CHAN, REF_CTGOV]},
    {"slug": "interim-analysis-dsmb", "title": "Interim Analysis & DSMB Patterns", "group": "methods-systems", "paper_num": 35,
     "query": {"condition": None, "location": "Africa"}, "stats": ["rate_ratio", "bootstrap_ci", "arima_forecast", "poisson_rate", "chi_squared"],
     "charts": _charts([6, 0, 2, 7, 9, 3, 14, 11]), "context": "Data Safety Monitoring Boards provide independent oversight, but DSMB formation and interim analysis planning in African trials is often ad hoc rather than protocol-mandated.", "refs": [REF_CHAN, REF_CTGOV]},
    {"slug": "multi-arm-efficiency", "title": "Multi-Arm Trial Efficiency", "group": "methods-systems", "paper_num": 36,
     "query": {"condition": None, "location": "Africa", "other": "multi-arm OR multiple arm"},
     "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "arima_forecast", "chi_squared"],
     "charts": _charts([7, 0, 6, 2, 3, 9, 11, 14]), "context": "Multi-arm trials share a common control group, increasing efficiency — a property that is especially valuable in Africa where every enrolled participant represents a scarce resource.", "refs": [REF_CHAN, REF_CTGOV]},
    {"slug": "cluster-rct-rigor", "title": "Cluster-RCT Design Rigor", "group": "methods-systems", "paper_num": 37,
     "query": {"condition": None, "location": "Africa", "other": "cluster randomized OR cluster randomised"},
     "stats": ["linear_regression", "bootstrap_ci", "rate_ratio", "poisson_rate", "effect_size"],
     "charts": _charts([10, 0, 2, 7, 3, 9, 6, 13]), "context": "Cluster-RCTs are Africa's most common advanced design, ideal for community-level interventions, but many fail to report ICC values and design effect calculations.", "refs": [REF_CHAN, REF_CTGOV]},
    {"slug": "non-inferiority-patterns", "title": "Non-Inferiority Design Patterns", "group": "methods-systems", "paper_num": 38,
     "query": {"condition": None, "location": "Africa", "other": "non-inferiority OR equivalence"},
     "stats": ["rate_ratio", "bootstrap_ci", "chi_squared", "poisson_rate", "bayesian_rate"],
     "charts": _charts([2, 0, 7, 3, 9, 6, 11, 14]), "context": "Non-inferiority trials are critical for testing cheaper or simpler alternatives to standard treatments — exactly what Africa needs — but NI margin justification is often inadequately reported.", "refs": [REF_CHAN, REF_CTGOV]},
    {"slug": "pediatric-trial-methodology", "title": "Pediatric Trial Methodology", "group": "methods-systems", "paper_num": 39,
     "query": {"condition": "pediatric OR child", "location": "Africa"},
     "stats": ["rate_ratio", "bootstrap_ci", "chi_squared", "poisson_rate", "bayesian_rate"],
     "charts": _charts([9, 0, 2, 7, 3, 6, 14, 11]), "context": "Pediatric trials require age-appropriate formulations, endpoints, and consent processes that most African trial sites are not equipped to provide, creating a childhood evidence gap.", "refs": [REF_CHAN, REF_CTGOV]},
    {"slug": "implementation-science", "title": "Implementation Science Penetration", "group": "methods-systems", "paper_num": 40,
     "query": {"condition": None, "location": "Africa", "other": "implementation science OR implementation research"},
     "stats": ["rate_ratio", "bootstrap_ci", "chi_squared", "arima_forecast", "poisson_rate"],
     "charts": _charts([6, 0, 9, 7, 3, 2, 11, 4]), "context": "Implementation science — testing how to deliver proven interventions effectively — is arguably more important than efficacy research in Africa, where the know-do gap is the primary barrier to health improvement.", "refs": [REF_CHAN, REF_CTGOV]},
    {"slug": "health-economic-evaluation", "title": "Health Economic Evaluation", "group": "methods-systems", "paper_num": 41,
     "query": {"condition": None, "location": "Africa", "other": "cost-effectiveness OR economic evaluation OR health economics"},
     "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "arima_forecast", "linear_regression"],
     "charts": _charts([6, 0, 10, 7, 3, 9, 2, 14]), "context": "Health economic evaluations alongside trials are critical for resource-limited African health systems making allocation decisions, yet cost-effectiveness data from African trials remains scarce.", "refs": [REF_CHAN, REF_CTGOV]},
    {"slug": "long-term-followup", "title": "Long-Term Follow-Up Deficit", "group": "methods-systems", "paper_num": 42,
     "query": {"condition": None, "location": "Africa"}, "stats": ["kaplan_meier", "bootstrap_ci", "rate_ratio", "linear_regression", "bayesian_rate"],
     "charts": _charts([14, 0, 6, 7, 3, 9, 2, 11]), "context": "Long-term follow-up is essential for safety monitoring and durability assessment, but mobile populations, limited tracing systems, and high mortality rates make it challenging in Africa.", "refs": [REF_CHAN, REF_CTGOV]},
    {"slug": "data-management-infrastructure", "title": "Data Management Infrastructure", "group": "methods-systems", "paper_num": 43,
     "query": {"condition": None, "location": "Africa"}, "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "arima_forecast", "chi_squared"],
     "charts": _charts([7, 0, 6, 3, 9, 2, 11, 4]), "context": "Electronic data capture, data quality assurance, and Good Clinical Data Management Practice are prerequisites for reliable trials, but African sites often rely on paper-based systems.", "refs": [REF_CHAN, REF_CTGOV]},
    {"slug": "endpoint-harmonisation", "title": "Endpoint Harmonisation Deficit", "group": "methods-systems", "paper_num": 44,
     "query": {"condition": None, "location": "Africa"}, "stats": ["jaccard_similarity", "shannon_entropy", "bootstrap_ci", "hhi_index", "chi_squared"],
     "charts": _charts([4, 0, 9, 7, 3, 6, 1, 12]), "context": "Heterogeneous endpoint definitions across similar African trials prevent meta-analysis and evidence synthesis, wasting the continent's limited research output.", "refs": [REF_CHAN, REF_CTGOV]},
    {"slug": "research-waste-quantification", "title": "Research Waste Quantification", "group": "methods-systems", "paper_num": 45,
     "query": {"condition": None, "location": "Africa"}, "stats": ["gini_coefficient", "lorenz", "bootstrap_ci", "rate_ratio", "linear_regression"],
     "charts": _charts([1, 0, 7, 6, 3, 9, 2, 11]), "context": "Avoidable research waste — from poor design, incomplete reporting, and non-publication — is estimated at 85% globally but may be even higher in Africa where resource constraints amplify the cost of waste.", "refs": [REF_CHAN, REF_CTGOV]},
]

# ═══════════════════════════════════════════════════════════
#  COMBINED MANIFEST
# ═══════════════════════════════════════════════════════════
MANIFEST = GEO_PAPERS + HEALTH_PAPERS + GOV_PAPERS + METHODS_PAPERS

# Validation
assert len(MANIFEST) == 110, f"Expected 110 papers, got {len(MANIFEST)}"
assert len(GEO_PAPERS) == 20, f"Expected 20 geo papers, got {len(GEO_PAPERS)}"
assert len(HEALTH_PAPERS) == 40, f"Expected 40 health papers, got {len(HEALTH_PAPERS)}"
assert len(GOV_PAPERS) == 25, f"Expected 25 gov papers, got {len(GOV_PAPERS)}"
assert len(METHODS_PAPERS) == 25, f"Expected 25 methods papers, got {len(METHODS_PAPERS)}"
assert len(set(p["slug"] for p in MANIFEST)) == 110, "Duplicate slugs found!"
