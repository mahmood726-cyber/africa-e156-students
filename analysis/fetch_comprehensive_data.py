#!/usr/bin/env python3
"""
Comprehensive Africa RCT Data Fetcher
======================================
Fetches multi-dimensional data from ClinicalTrials.gov API v2:
  - Country-level counts (already cached)
  - Condition-level: 20 conditions × 4 regions
  - Phase distribution × 4 regions
  - Sponsor type × 4 regions
  - Design features × 4 regions
  - Status distribution × 4 regions
  - Temporal (by 5-year epoch) × 4 regions

Saves to comprehensive_africa_data.json (~200 API calls, ~90 seconds)

Requirements: Python 3.8+, requests
"""
import json, sys, io, time
from pathlib import Path
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    import requests
except ImportError:
    print("pip install requests"); sys.exit(1)

BASE = "https://clinicaltrials.gov/api/v2/studies"
OUT = Path(__file__).parent / "comprehensive_africa_data.json"
DELAY = 0.3

# Use OR-combined country queries since LocationContinent is not a valid API field
_AF_COUNTRIES = ["South Africa", "Egypt", "Kenya", "Uganda", "Nigeria", "Tanzania",
                 "Ethiopia", "Ghana", "Tunisia", "Morocco", "Malawi", "Zambia",
                 "Cameroon", "Mozambique", "Zimbabwe", "Rwanda", "Senegal"]
_EU_COUNTRIES = ["United Kingdom", "France", "Germany", "Spain", "Italy",
                 "Netherlands", "Sweden", "Denmark", "Belgium", "Switzerland"]
_AF_QUERY = " OR ".join(f"AREA[LocationCountry]{c}" for c in _AF_COUNTRIES)
_EU_QUERY = " OR ".join(f"AREA[LocationCountry]{c}" for c in _EU_COUNTRIES)

REGIONS = {
    "Africa": _AF_QUERY,
    "Europe": _EU_QUERY,
    "United States": "AREA[LocationCountry]United States",
    "China": "AREA[LocationCountry]China",
}

CONDITIONS = [
    "HIV", "malaria", "tuberculosis", "cancer", "cardiovascular",
    "diabetes", "hypertension", "mental health", "stroke", "maternal",
    "sickle cell", "heart failure", "pneumonia", "diarrhea", "neonatal",
    "neglected tropical diseases", "epilepsy", "kidney", "liver", "respiratory",
]

PHASES = ["EARLY_PHASE1", "PHASE1", "PHASE2", "PHASE3", "PHASE4"]
STATUSES = ["RECRUITING", "COMPLETED", "TERMINATED", "WITHDRAWN", "NOT_YET_RECRUITING", "ACTIVE_NOT_RECRUITING"]
SPONSORS = ["INDUSTRY", "NIH", "FED", "OTHER"]

# Design features to search for in brief title/description
DESIGN_KEYWORDS = {
    "adaptive": "adaptive",
    "cluster": "cluster randomized",
    "platform": "platform trial",
    "bayesian": "bayesian",
    "placebo": "placebo",
    "double-blind": "double blind",
    "open-label": "open label",
    "biomarker": "biomarker",
    "immunotherapy": "immunotherapy",
    "genomic": "genomic OR pharmacogenomic",
    "digital": "decentralized OR virtual OR wearable",
    "community": "community advisory OR community engagement",
}

EPOCHS = [
    ("2000-2005", "2000-01-01", "2005-12-31"),
    ("2006-2010", "2006-01-01", "2010-12-31"),
    ("2011-2015", "2011-01-01", "2015-12-31"),
    ("2016-2020", "2016-01-01", "2020-12-31"),
    ("2021-2025", "2021-01-01", "2025-12-31"),
]


def count(region_query, extra_params=None):
    """Get trial count with region filter + optional extra params."""
    params = {
        "query.locn": region_query,
        "countTotal": "true",
        "pageSize": 0,
    }
    if extra_params:
        params.update(extra_params)
    try:
        r = requests.get(BASE, params=params, timeout=30)
        r.raise_for_status()
        return r.json().get("totalCount", 0)
    except Exception as e:
        print(f"    ERROR: {e}")
        return -1


def count_term(region_query, term, extra_params=None):
    """Get trial count with region + search term."""
    params = {
        "query.locn": region_query,
        "query.cond": term,
        "countTotal": "true",
        "pageSize": 0,
    }
    if extra_params:
        params.update(extra_params)
    try:
        r = requests.get(BASE, params=params, timeout=30)
        r.raise_for_status()
        return r.json().get("totalCount", 0)
    except Exception as e:
        print(f"    ERROR: {e}")
        return -1


def main():
    print("=" * 60)
    print("  COMPREHENSIVE AFRICA RCT DATA FETCH")
    print("  ClinicalTrials.gov API v2")
    print("=" * 60)

    data = {"retrieved": datetime.now().isoformat(), "source": "ClinicalTrials.gov API v2"}
    call_count = 0

    # 1. Total counts by region
    print("\n1. TOTAL TRIAL COUNTS BY REGION")
    totals = {}
    for rname, rquery in REGIONS.items():
        c = count(rquery)
        totals[rname] = c
        call_count += 1
        print(f"   {rname}: {c:,}")
        time.sleep(DELAY)
    data["totals"] = totals

    # 2. Condition × Region
    print("\n2. CONDITION × REGION")
    conditions = {}
    for cond in CONDITIONS:
        conditions[cond] = {}
        for rname, rquery in REGIONS.items():
            c = count_term(rquery, cond)
            conditions[cond][rname] = c
            call_count += 1
            time.sleep(DELAY)
        af = conditions[cond]["Africa"]
        us = conditions[cond]["United States"]
        ratio = f"{us/af:.0f}x" if af > 0 else "inf"
        print(f"   {cond:<30s} AF={af:>6,}  US={us:>7,}  ratio={ratio}")
    data["conditions"] = conditions

    # 3. Phase × Region
    print("\n3. PHASE × REGION")
    phases = {}
    for phase in PHASES:
        phases[phase] = {}
        for rname, rquery in REGIONS.items():
            c = count(rquery, {"filter.phase": phase})
            phases[phase][rname] = c
            call_count += 1
            time.sleep(DELAY)
        print(f"   {phase:<15s} AF={phases[phase]['Africa']:>6,}  US={phases[phase]['United States']:>7,}")
    data["phases"] = phases

    # 4. Status × Region
    print("\n4. STATUS × REGION")
    statuses = {}
    for status in STATUSES:
        statuses[status] = {}
        for rname, rquery in REGIONS.items():
            c = count(rquery, {"filter.overallStatus": status})
            statuses[status][rname] = c
            call_count += 1
            time.sleep(DELAY)
        print(f"   {status:<25s} AF={statuses[status]['Africa']:>6,}")
    data["statuses"] = statuses

    # 5. Sponsor type × Region
    print("\n5. SPONSOR TYPE × REGION")
    sponsors = {}
    for stype in SPONSORS:
        sponsors[stype] = {}
        for rname, rquery in REGIONS.items():
            c = count(rquery, {"filter.leadSponsorType": stype})
            sponsors[stype][rname] = c
            call_count += 1
            time.sleep(DELAY)
        print(f"   {stype:<10s} AF={sponsors[stype]['Africa']:>6,}  US={sponsors[stype]['United States']:>7,}")
    data["sponsors"] = sponsors

    # 6. Design keywords × Region (Africa + US only for speed)
    print("\n6. DESIGN FEATURES (keyword search)")
    designs = {}
    for dname, dterm in DESIGN_KEYWORDS.items():
        designs[dname] = {}
        for rname in ["Africa", "United States"]:
            rquery = REGIONS[rname]
            params = {
                "query.locn": rquery,
                "query.term": dterm,
                "countTotal": "true",
                "pageSize": 0,
            }
            try:
                r = requests.get(BASE, params=params, timeout=30)
                r.raise_for_status()
                c = r.json().get("totalCount", 0)
            except:
                c = -1
            designs[dname][rname] = c
            call_count += 1
            time.sleep(DELAY)
        af = designs[dname]["Africa"]
        us = designs[dname]["United States"]
        print(f"   {dname:<20s} AF={af:>6,}  US={us:>7,}")
    data["designs"] = designs

    # 7. Temporal epochs × Region
    print("\n7. TEMPORAL EPOCHS")
    temporal = {}
    for epoch_name, start, end in EPOCHS:
        temporal[epoch_name] = {}
        for rname, rquery in REGIONS.items():
            params = {
                "query.locn": rquery,
                "filter.advanced": f"AREA[StartDate]RANGE[{start},{end}]",
                "countTotal": "true",
                "pageSize": 0,
            }
            try:
                r = requests.get(BASE, params=params, timeout=30)
                r.raise_for_status()
                c = r.json().get("totalCount", 0)
            except:
                c = -1
            temporal[epoch_name][rname] = c
            call_count += 1
            time.sleep(DELAY)
        print(f"   {epoch_name}: AF={temporal[epoch_name]['Africa']:>6,}  US={temporal[epoch_name]['United States']:>7,}")
    data["temporal"] = temporal

    # 8. Africa-specific: top conditions
    print("\n8. AFRICA TOP CONDITIONS (detailed)")
    africa_conditions = {}
    detailed_conds = [
        "HIV", "malaria", "tuberculosis", "cancer", "cardiovascular",
        "diabetes", "hypertension", "maternal mortality", "sickle cell disease",
        "heart failure", "stroke", "pneumonia", "diarrheal disease",
        "neglected tropical diseases", "mental health", "epilepsy",
        "kidney disease", "respiratory infection", "hepatitis", "meningitis",
        "rheumatic heart disease", "peripartum cardiomyopathy",
        "schistosomiasis", "dengue", "Ebola",
    ]
    for cond in detailed_conds:
        c = count_term(REGIONS["Africa"], cond)
        africa_conditions[cond] = c
        call_count += 1
        time.sleep(DELAY)
        print(f"   {cond:<35s} {c:>5,}")
    data["africa_conditions_detailed"] = africa_conditions

    # Save
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"\nSaved: {OUT}")
    print(f"Total API calls: {call_count}")
    print(f"Total trials (Africa): {totals.get('Africa', '?'):,}")


if __name__ == "__main__":
    main()
