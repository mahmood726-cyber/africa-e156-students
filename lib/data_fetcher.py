"""
Fetch trial data from ClinicalTrials.gov API v2 for each paper topic.
Uses JSON file caching to avoid redundant API calls.
"""
import json, time, sys, io
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: pip install requests")
    sys.exit(1)

API_BASE = "https://clinicaltrials.gov/api/v2/studies"
CACHE_DIR = Path(__file__).parent.parent / "data_cache"
# Preloaded comprehensive data from prior analysis
COMP_PATH = Path(__file__).parent.parent / "analysis" / "comprehensive_africa_data.json"
COUNTRY_PATH = Path(__file__).parent.parent / "analysis" / "africa_rct_country_results.json"

_comp_data = None
_country_data = None

def _load_comprehensive():
    """Load cached comprehensive data from prior analysis runs."""
    global _comp_data, _country_data
    if _comp_data is None and COMP_PATH.exists():
        with open(COMP_PATH, encoding="utf-8") as f:
            _comp_data = json.load(f)
    if _country_data is None and COUNTRY_PATH.exists():
        with open(COUNTRY_PATH, encoding="utf-8") as f:
            _country_data = json.load(f)
    return _comp_data or {}, _country_data or {}


def fetch_trial_count(condition=None, location=None, other_terms=None):
    """Fetch total trial count for a query from ClinicalTrials.gov API v2."""
    params = {
        "format": "json",
        "pageSize": 0,
        "countTotal": "true",
        "filter.advanced": "AREA[StudyType]INTERVENTIONAL"
    }
    if condition:
        params["query.cond"] = condition
    if location:
        params["query.locn"] = location
    if other_terms:
        params["query.term"] = other_terms
    try:
        resp = requests.get(API_BASE, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json().get("totalCount", 0)
    except Exception as e:
        print(f"  API error: {e}")
        return 0


def fetch_studies(condition=None, location=None, other_terms=None, max_results=100):
    """Fetch study records for deeper analysis."""
    params = {
        "format": "json",
        "pageSize": min(max_results, 200),
        "filter.advanced": "AREA[StudyType]INTERVENTIONAL"
    }
    if condition:
        params["query.cond"] = condition
    if location:
        params["query.locn"] = location
    if other_terms:
        params["query.term"] = other_terms
    try:
        resp = requests.get(API_BASE, params=params, timeout=60)
        resp.raise_for_status()
        return resp.json().get("studies", [])
    except Exception as e:
        print(f"  API error fetching studies: {e}")
        return []


def extract_study_metrics(studies):
    """Extract useful metrics from a list of study records."""
    metrics = {
        "total": len(studies),
        "statuses": {},
        "phases": {},
        "enrollment_values": [],
        "start_years": [],
        "countries": {},
        "designs": {"randomized": 0, "non_randomized": 0, "observational": 0},
        "conditions_list": [],
    }
    for s in studies:
        proto = s.get("protocolSection", {})
        status_mod = proto.get("statusModule", {})
        design_mod = proto.get("designModule", {})
        elig_mod = proto.get("eligibilityModule", {})
        loc_mod = proto.get("contactsLocationsModule", {})

        # Status
        status = status_mod.get("overallStatus", "UNKNOWN")
        metrics["statuses"][status] = metrics["statuses"].get(status, 0) + 1

        # Phase
        phases = design_mod.get("phases", [])
        for ph in phases:
            metrics["phases"][ph] = metrics["phases"].get(ph, 0) + 1

        # Enrollment
        enroll = design_mod.get("enrollmentInfo", {})
        count = enroll.get("count")
        if count and isinstance(count, (int, float)) and count > 0:
            metrics["enrollment_values"].append(int(count))

        # Start year
        start = status_mod.get("startDateStruct", {}).get("date", "")
        if start and len(start) >= 4:
            try:
                year = int(start[:4])
                if 1990 <= year <= 2030:
                    metrics["start_years"].append(year)
            except ValueError:
                pass

        # Countries
        locations = loc_mod.get("locations", [])
        for loc in locations:
            country = loc.get("country", "")
            if country:
                metrics["countries"][country] = metrics["countries"].get(country, 0) + 1

        # Design
        design_info = design_mod.get("designInfo", {})
        alloc = design_info.get("allocation", "")
        if "RANDOMIZED" in alloc.upper():
            metrics["designs"]["randomized"] += 1
        elif alloc:
            metrics["designs"]["non_randomized"] += 1

        # Conditions
        conds = proto.get("conditionsModule", {}).get("conditions", [])
        metrics["conditions_list"].extend(conds[:3])

    return metrics


def fetch_paper_data(paper_def):
    """Fetch all data needed for a single paper. Uses cache."""
    CACHE_DIR.mkdir(exist_ok=True)
    cache_file = CACHE_DIR / f"{paper_def['slug']}.json"

    # Return cached data if available
    if cache_file.exists():
        with open(cache_file, encoding="utf-8") as f:
            return json.load(f)

    comp, country = _load_comprehensive()
    q = paper_def.get("query", {})
    condition = q.get("condition")
    location = q.get("location", "Africa")
    other = q.get("other")
    countries = q.get("countries")

    data = {"slug": paper_def["slug"]}

    # 1. Get counts from comprehensive data if condition matches
    if condition and comp.get("conditions", {}).get(condition.split(" OR ")[0].lower().strip()):
        cond_key = condition.split(" OR ")[0].lower().strip()
        cond_data = comp["conditions"].get(cond_key, {})
        data["africa_count"] = cond_data.get("Africa", 0)
        data["us_count"] = cond_data.get("United States", 0)
        data["europe_count"] = cond_data.get("Europe", 0)
        data["china_count"] = cond_data.get("China", 0)
    else:
        # Fetch from API
        data["africa_count"] = fetch_trial_count(condition, "Africa", other)
        time.sleep(0.3)
        data["us_count"] = fetch_trial_count(condition, "United States", other)
        time.sleep(0.3)
        data["europe_count"] = fetch_trial_count(condition, "Europe", other)
        time.sleep(0.3)

    # 2. Get totals from comprehensive data
    totals = comp.get("totals", {})
    data["total_africa"] = totals.get("Africa", 23873)
    data["total_us"] = totals.get("United States", 190644)
    data["total_europe"] = totals.get("Europe", 142126)

    # 3. Country-specific data
    if countries:
        data["country_counts"] = {}
        country_list = country.get("countries", []) if country else []
        for c in countries:
            # Check preloaded country data first
            found = False
            for cd in country_list:
                if cd.get("name", "").lower() == c.lower():
                    data["country_counts"][c] = cd.get("trials", 0)
                    found = True
                    break
            if not found:
                data["country_counts"][c] = fetch_trial_count(condition, c, other)
                time.sleep(0.2)

    # 4. Fetch sample studies for metrics
    studies = fetch_studies(condition, location, other, max_results=100)
    data["study_metrics"] = extract_study_metrics(studies)
    time.sleep(0.3)

    # 5. Temporal data from comprehensive
    temporal = comp.get("temporal", {})
    if temporal:
        data["temporal"] = {}
        for epoch, regions in temporal.items():
            data["temporal"][epoch] = {
                "Africa": regions.get("Africa", 0),
                "United States": regions.get("United States", 0),
                "Europe": regions.get("Europe", 0)
            }

    # 6. All-Africa country distribution
    if country:
        all_countries = country.get("countries", [])
        data["africa_countries"] = all_countries[:20]  # Top 20
    else:
        data["africa_countries"] = []

    # Cache the result
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)

    return data
