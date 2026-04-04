#!/usr/bin/env python3
"""
Build script for Africa E156 Student Assignment Platform.
Generates GitHub Pages site with 4 group pages (12 papers each).
"""

import os
import re
import shutil
from pathlib import Path
from html import escape

# ── Paths ──
# NOTE: These paths are for the author's build machine. Students use the generated HTML.
SOURCE = Path("C:/AfricaRCT")
E156 = SOURCE / "E156"
SCRIPTS = SOURCE / "scripts"
OUT = Path("C:/Users/user/africa-e156-students")
GITHUB_PAGES = "https://mahmood726-cyber.github.io/africa-e156-students"
GITHUB_REPO = "https://github.com/mahmood726-cyber/africa-e156-students"
JOURNAL_URL = "https://www.synthesis-medicine.org/index.php/journal"

# ── Group definitions ──
GROUPS = {
    "geographic-equity": {
        "title": "Geographic Equity & Spatial Justice",
        "desc": "Where do clinical trials happen in Africa? These 12 papers analyse the spatial distribution of research sites, urban-rural gaps, cross-border access barriers, and geographic concentration patterns using ClinicalTrials.gov data.",
        "papers": [
            {"slug": "angle-11_city-dispersion-rates", "title": "City Dispersion Rates",
             "code_src": "scripts/forty_angles_audit.py",
             "refs": [
                 'Drain PK, et al. "Global migration of clinical trials." <i>Nat Rev Drug Discov</i>. 2018;17:765-766.',
                 'Alemayehu C, et al. "Behind the mask of the African clinical trials landscape." <i>Trials</i>. 2018;19:519.',
                 'ClinicalTrials.gov API v2 Documentation. U.S. National Library of Medicine. https://clinicaltrials.gov/data-api/about-api'
             ]},
            {"slug": "angle-12_site-clustering-indices", "title": "Site Clustering Indices",
             "code_src": "scripts/forty_angles_audit.py",
             "refs": [
                 'Siegfried N, et al. "Where does all the money go? An analysis of the global funding for clinical trials." <i>Cochrane Database Syst Rev</i>. 2022.',
                 'Ndounga Diakou LA, et al. "Mapping of clinical trials in sub-Saharan Africa." <i>Trials</i>. 2022;23:490.',
             ]},
            {"slug": "angle-13_rural-reach-coefficients", "title": "Rural Reach Coefficients",
             "code_src": "scripts/forty_angles_audit.py",
             "refs": [
                 'Isaakidis P, et al. "Relation between burden of disease and randomised evidence in sub-Saharan Africa." <i>BMJ</i>. 2002;324:702.',
                 'World Health Organization. "World Health Statistics 2024." WHO, Geneva.',
                 'Alemayehu C, et al. "Behind the mask of the African clinical trials landscape." <i>Trials</i>. 2018;19:519.',
             ]},
            {"slug": "angle-14_urban-hub-monopolies", "title": "Urban Hub Monopolies",
             "code_src": "scripts/forty_angles_audit.py",
             "refs": [
                 'Drain PK, et al. "Global migration of clinical trials." <i>Nat Rev Drug Discov</i>. 2018;17:765-766.',
                 'Lang T, Siribaddana S. "Clinical trials have gone global: is this a good thing?" <i>PLoS Med</i>. 2012;9:e1001228.',
             ]},
            {"slug": "angle-15_geographic-site-density", "title": "Geographic Site Density",
             "code_src": "scripts/forty_angles_audit.py",
             "refs": [
                 'Ndounga Diakou LA, et al. "Mapping of clinical trials in sub-Saharan Africa." <i>Trials</i>. 2022;23:490.',
                 'ClinicalTrials.gov API v2 Documentation. U.S. National Library of Medicine.',
             ]},
            {"slug": "angle-16_regional-site-fragmentation", "title": "Regional Site Fragmentation",
             "code_src": "scripts/forty_angles_audit.py",
             "refs": [
                 'Alemayehu C, et al. "Behind the mask of the African clinical trials landscape." <i>Trials</i>. 2018;19:519.',
                 'Siegfried N, et al. "Where does all the money go?" <i>Cochrane Database Syst Rev</i>. 2022.',
             ]},
            {"slug": "angle-20_spatial-equity-indices", "title": "Spatial Equity Indices",
             "code_src": "scripts/forty_angles_audit.py",
             "refs": [
                 'Lang T, Siribaddana S. "Clinical trials have gone global: is this a good thing?" <i>PLoS Med</i>. 2012;9:e1001228.',
                 'Drain PK, et al. "Global migration of clinical trials." <i>Nat Rev Drug Discov</i>. 2018;17:765-766.',
                 'World Health Organization. "World Health Statistics 2024." WHO, Geneva.',
             ]},
            {"slug": "angle-19_border-integration-rates", "title": "Border Integration Rates",
             "code_src": "scripts/forty_angles_audit.py",
             "refs": [
                 'African Union. "Africa Health Strategy 2016-2030." AU Commission, Addis Ababa.',
                 'Ndounga Diakou LA, et al. "Mapping of clinical trials in sub-Saharan Africa." <i>Trials</i>. 2022;23:490.',
             ]},
            {"slug": "intra-african-disparity", "title": "Intra-African Disparity & Regional Fractures",
             "code_src": "scripts/compare_africa_europe.py",
             "refs": [
                 'Isaakidis P, et al. "Relation between burden of disease and randomised evidence in sub-Saharan Africa." <i>BMJ</i>. 2002;324:702.',
                 'Alemayehu C, et al. "Behind the mask of the African clinical trials landscape." <i>Trials</i>. 2018;19:519.',
                 'ClinicalTrials.gov API v2 Documentation. U.S. National Library of Medicine.',
             ]},
            {"slug": "site-fragmentation", "title": "Site Fragmentation & Token Site Metric",
             "code_src": "scripts/cluster_audit.py",
             "refs": [
                 'Drain PK, et al. "Global migration of clinical trials." <i>Nat Rev Drug Discov</i>. 2018;17:765-766.',
                 'Siegfried N, et al. "Where does all the money go?" <i>Cochrane Database Syst Rev</i>. 2022.',
             ]},
            {"slug": "spatial-entropy", "title": "Spatial Entropy",
             "code_src": "scripts/topology_analysis.py",
             "refs": [
                 'Lang T, Siribaddana S. "Clinical trials have gone global: is this a good thing?" <i>PLoS Med</i>. 2012;9:e1001228.',
                 'Ndounga Diakou LA, et al. "Mapping of clinical trials in sub-Saharan Africa." <i>Trials</i>. 2022;23:490.',
             ]},
            {"slug": "selection-pressure", "title": "Selection Pressure & Hardy Hub",
             "code_src": "scripts/power_audit.py",
             "refs": [
                 'Alemayehu C, et al. "Behind the mask of the African clinical trials landscape." <i>Trials</i>. 2018;19:519.',
                 'Drain PK, et al. "Global migration of clinical trials." <i>Nat Rev Drug Discov</i>. 2018;17:765-766.',
                 'ClinicalTrials.gov API v2 Documentation. U.S. National Library of Medicine.',
             ]},
        ]
    },
    "health-disease": {
        "title": "Health & Disease Burden",
        "desc": "What diseases get studied in Africa, and which are ignored? These 12 papers examine heart failure, maternal mortality, COVID displacement, genomic gaps, and the mismatch between disease burden and research investment.",
        "papers": [
            {"slug": "heart-failure-africa", "title": "Heart Failure in Africa",
             "code_src": "scripts/fetch_heart_failure_africa.py",
             "refs": [
                 'Mbewu A, Mbanya JC. "Cardiovascular disease." In: <i>Disease and Mortality in Sub-Saharan Africa</i>. 2nd ed. World Bank; 2006.',
                 'Sliwa K, et al. "Readmission and death after an acute heart failure event." <i>Eur Heart J</i>. 2017;38:1508-1518.',
                 'ClinicalTrials.gov API v2 Documentation. U.S. National Library of Medicine.',
             ]},
            {"slug": "maternal-mortality", "title": "The Maternal Mortality Scandal",
             "code_src": "scripts/fetch_maternal_mortality.py",
             "refs": [
                 'WHO. "Trends in maternal mortality 2000 to 2020." WHO, UNICEF, UNFPA, World Bank. Geneva, 2023.',
                 'Say L, et al. "Global causes of maternal death: a WHO systematic analysis." <i>Lancet Glob Health</i>. 2014;2:e323-e333.',
                 'ClinicalTrials.gov API v2 Documentation. U.S. National Library of Medicine.',
             ]},
            {"slug": "covid-displacement", "title": "COVID Displacement",
             "code_src": "scripts/fetch_covid_impact.py",
             "refs": [
                 'Makoni M. "COVID-19 in Africa: half a year later." <i>Lancet Infect Dis</i>. 2020;20:1127.',
                 'Alemayehu C, et al. "Behind the mask of the African clinical trials landscape." <i>Trials</i>. 2018;19:519.',
             ]},
            {"slug": "global-diseasome-mismatch", "title": "Global Diseasome Mismatch",
             "code_src": "scripts/fetch_forgotten_diseases.py",
             "refs": [
                 'Isaakidis P, et al. "Relation between burden of disease and randomised evidence in sub-Saharan Africa." <i>BMJ</i>. 2002;324:702.',
                 'GBD 2019 Diseases and Injuries Collaborators. "Global burden of 369 diseases." <i>Lancet</i>. 2020;396:1204-1222.',
                 'ClinicalTrials.gov API v2 Documentation. U.S. National Library of Medicine.',
             ]},
            {"slug": "ethnicity-void", "title": "The Demographic Void & Genomic Diversity",
             "code_src": "scripts/fetch_diversity_audit.py",
             "refs": [
                 'Popejoy AB, Fullerton SM. "Genomics is failing on diversity." <i>Nature</i>. 2016;538:161-164.',
                 'Sirugo G, et al. "The missing diversity in human genetic studies." <i>Cell</i>. 2019;177:26-31.',
             ]},
            {"slug": "genomic-resilience", "title": "Genomic Resilience & Precision Gaps",
             "code_src": "scripts/genomic_audit.py",
             "refs": [
                 'Munung NS, et al. "Obtaining informed consent for genomics research in Africa." <i>BMC Med Ethics</i>. 2016;17:15.',
                 'Popejoy AB, Fullerton SM. "Genomics is failing on diversity." <i>Nature</i>. 2016;538:161-164.',
                 'H3Africa Consortium. "Research capacity for genomics in Africa." <i>Science</i>. 2014;344:1346-1348.',
             ]},
            {"slug": "cognitive-deficit", "title": "The Global Cognitive Deficit",
             "code_src": "scripts/fetch_diversity_audit.py",
             "refs": [
                 'Sirugo G, et al. "The missing diversity in human genetic studies." <i>Cell</i>. 2019;177:26-31.',
                 'Lang T, Siribaddana S. "Clinical trials have gone global: is this a good thing?" <i>PLoS Med</i>. 2012;9:e1001228.',
             ]},
            {"slug": "biological-extraction", "title": "Biological Sovereignty & Extraction",
             "code_src": "scripts/biological_audit.py",
             "refs": [
                 'de Vries J, et al. ""; returning"; individual research results in Africa." <i>Nat Genet</i>. 2012;44:370-374.',
                 'Benatar SR. "Reflections and recommendations on research ethics in developing countries." <i>Soc Sci Med</i>. 2002;54:1131-1141.',
             ]},
            {"slug": "clinical-interconnectivity", "title": "Clinical Interconnectivity & Global Grids",
             "code_src": "scripts/fetch_network_analysis.py",
             "refs": [
                 'Drain PK, et al. "Global migration of clinical trials." <i>Nat Rev Drug Discov</i>. 2018;17:765-766.',
                 'Alemayehu C, et al. "Behind the mask of the African clinical trials landscape." <i>Trials</i>. 2018;19:519.',
             ]},
            {"slug": "modality-symmetry", "title": "Modality Symmetry & Innovation Gaps",
             "code_src": "scripts/complexity_audit.py",
             "refs": [
                 'Lang T, Siribaddana S. "Clinical trials have gone global: is this a good thing?" <i>PLoS Med</i>. 2012;9:e1001228.',
                 'ClinicalTrials.gov API v2 Documentation. U.S. National Library of Medicine.',
             ]},
            {"slug": "rct_equity", "title": "Global RCT Equity (Africa vs Europe)",
             "code_src": "scripts/compare_africa_europe.py",
             "refs": [
                 'Ndounga Diakou LA, et al. "Mapping of clinical trials in sub-Saharan Africa." <i>Trials</i>. 2022;23:490.',
                 'Isaakidis P, et al. "Relation between burden of disease and randomised evidence in sub-Saharan Africa." <i>BMJ</i>. 2002;324:702.',
                 'ClinicalTrials.gov API v2 Documentation. U.S. National Library of Medicine.',
             ]},
            {"slug": "expanded-access", "title": "Expanded Access & Post-Trial Justice",
             "code_src": "scripts/fetch_patient_access.py",
             "refs": [
                 'Participants in the 2001 Conference. "Moral standards for research in developing countries." <i>Hastings Cent Rep</i>. 2004;34:17-27.',
                 'Benatar SR. "Reflections and recommendations on research ethics in developing countries." <i>Soc Sci Med</i>. 2002;54:1131-1141.',
             ]},
        ]
    },
    "governance-justice": {
        "title": "Governance, Justice & Sovereignty",
        "desc": "Who controls clinical research in Africa? These 12 papers examine authorship gaps, corporate capture, data sovereignty, knowledge extraction, placebo ethics, and the structural power dynamics that shape African research.",
        "papers": [
            {"slug": "author-sovereignty-gap", "title": "Author Sovereignty Gap",
             "code_src": "scripts/sovereignty_audit.py",
             "refs": [
                 'Hedt-Gauthier BL, et al. "Stuck in the middle: authorship in collaborative health research in Africa." <i>BMJ Glob Health</i>. 2019;4:e001853.',
                 'Mbaye R, et al. "Who is telling the stories of Africa?" <i>BMJ Glob Health</i>. 2019;4:e001855.',
             ]},
            {"slug": "corporate-capture", "title": "Corporate Capture",
             "code_src": "scripts/fetch_pharma_extraction.py",
             "refs": [
                 'Lang T, Siribaddana S. "Clinical trials have gone global: is this a good thing?" <i>PLoS Med</i>. 2012;9:e1001228.',
                 'Drain PK, et al. "Global migration of clinical trials." <i>Nat Rev Drug Discov</i>. 2018;17:765-766.',
             ]},
            {"slug": "data-sovereignty", "title": "Data Sovereignty & Mandatory Transparency",
             "code_src": "scripts/sharing_sovereignty_audit.py",
             "refs": [
                 'de Vries J, et al. ""; returning"; individual research results in Africa." <i>Nat Genet</i>. 2012;44:370-374.',
                 'African Union. "Africa Health Strategy 2016-2030." AU Commission, Addis Ababa.',
                 'ClinicalTrials.gov API v2 Documentation. U.S. National Library of Medicine.',
             ]},
            {"slug": "intellectual-capital", "title": "Intellectual Capital & Leadership Gaps",
             "code_src": "scripts/hegemony_audit.py",
             "refs": [
                 'Hedt-Gauthier BL, et al. "Stuck in the middle." <i>BMJ Glob Health</i>. 2019;4:e001853.',
                 'Mbaye R, et al. "Who is telling the stories of Africa?" <i>BMJ Glob Health</i>. 2019;4:e001855.',
                 'Alemayehu C, et al. "Behind the mask of the African clinical trials landscape." <i>Trials</i>. 2018;19:519.',
             ]},
            {"slug": "knowledge-extraction", "title": "Knowledge Extraction & Sharing Gap",
             "code_src": "scripts/fetch_extraction_index.py",
             "refs": [
                 'Mbaye R, et al. "Who is telling the stories of Africa?" <i>BMJ Glob Health</i>. 2019;4:e001855.',
                 'Benatar SR. "Reflections and recommendations on research ethics in developing countries." <i>Soc Sci Med</i>. 2002;54:1131-1141.',
             ]},
            {"slug": "placebo-ethics", "title": "Placebo Ethics Audit",
             "code_src": "scripts/fetch_placebo_ethics.py",
             "refs": [
                 'World Medical Association. "Declaration of Helsinki." JAMA. 2013;310:2191-2194.',
                 'Participants in the 2001 Conference. "Moral standards for research in developing countries." <i>Hastings Cent Rep</i>. 2004;34:17-27.',
                 'Benatar SR. "Reflections on research ethics in developing countries." <i>Soc Sci Med</i>. 2002;54:1131-1141.',
             ]},
            {"slug": "sponsor-sovereignty", "title": "Sponsor Sovereignty",
             "code_src": "scripts/sovereignty_audit.py",
             "refs": [
                 'Lang T, Siribaddana S. "Clinical trials have gone global: is this a good thing?" <i>PLoS Med</i>. 2012;9:e1001228.',
                 'Alemayehu C, et al. "Behind the mask of the African clinical trials landscape." <i>Trials</i>. 2018;19:519.',
             ]},
            {"slug": "value-transfer", "title": "The Economic Value of African Altruism",
             "code_src": "scripts/value_chain_audit.py",
             "refs": [
                 'Petryna A. <i>When Experiments Travel: Clinical Trials and the Global Search for Human Subjects</i>. Princeton University Press; 2009.',
                 'Drain PK, et al. "Global migration of clinical trials." <i>Nat Rev Drug Discov</i>. 2018;17:765-766.',
             ]},
            {"slug": "altruism-efficiency", "title": "Altruism Efficiency & Health Expenditure",
             "code_src": "scripts/value_chain_audit.py",
             "refs": [
                 'Petryna A. <i>When Experiments Travel</i>. Princeton University Press; 2009.',
                 'World Health Organization. "World Health Statistics 2024." WHO, Geneva.',
             ]},
            {"slug": "who-alignment", "title": "WHO Alignment & Disease Burden Gaps",
             "code_src": "scripts/who_alignment_audit.py",
             "refs": [
                 'GBD 2019 Diseases and Injuries Collaborators. "Global burden of 369 diseases." <i>Lancet</i>. 2020;396:1204-1222.',
                 'World Health Organization. "World Health Statistics 2024." WHO, Geneva.',
                 'ClinicalTrials.gov API v2 Documentation. U.S. National Library of Medicine.',
             ]},
            {"slug": "structural-inequity", "title": "Structural Inequity",
             "code_src": "scripts/structural_inequity_analysis.py",
             "refs": [
                 'Isaakidis P, et al. "Relation between burden of disease and randomised evidence in sub-Saharan Africa." <i>BMJ</i>. 2002;324:702.',
                 'Lang T, Siribaddana S. "Clinical trials have gone global: is this a good thing?" <i>PLoS Med</i>. 2012;9:e1001228.',
             ]},
            {"slug": "unified-theory", "title": "Unified Field Theory of Research Inequity",
             "code_src": "scripts/gods_eye_meta_synthesis.py",
             "refs": [
                 'Alemayehu C, et al. "Behind the mask of the African clinical trials landscape." <i>Trials</i>. 2018;19:519.',
                 'Ndounga Diakou LA, et al. "Mapping of clinical trials in sub-Saharan Africa." <i>Trials</i>. 2022;23:490.',
                 'Drain PK, et al. "Global migration of clinical trials." <i>Nat Rev Drug Discov</i>. 2018;17:765-766.',
             ]},
        ]
    },
    "methods-systems": {
        "title": "Methods, Design & Research Systems",
        "desc": "What trial methods does Africa receive? These 12 papers audit protocol quality, recruitment speed, Benford's law adherence, network entropy, and whether Africa gets cutting-edge or second-class methodology.",
        "papers": [
            {"slug": "design-quality", "title": "Methodological Quality Audit",
             "code_src": "scripts/fetch_design_quality.py",
             "refs": [
                 'Schwartz D, Lellouch J. "Explanatory and pragmatic attitudes in therapeutical trials." <i>J Clin Epidemiol</i>. 2009;62:499-505.',
                 'Alemayehu C, et al. "Behind the mask of the African clinical trials landscape." <i>Trials</i>. 2018;19:519.',
                 'ClinicalTrials.gov API v2 Documentation. U.S. National Library of Medicine.',
             ]},
            {"slug": "protocol-granularity", "title": "Protocol Granularity & Rigor",
             "code_src": "scripts/deep_granularity_audit.py",
             "refs": [
                 'Chan AW, et al. "SPIRIT 2013 statement." <i>Ann Intern Med</i>. 2013;158:200-207.',
                 'Ndounga Diakou LA, et al. "Mapping of clinical trials in sub-Saharan Africa." <i>Trials</i>. 2022;23:490.',
             ]},
            {"slug": "protocol-volatility", "title": "Protocol Volatility & Mutation Rates",
             "code_src": "scripts/deep_analysis.py",
             "refs": [
                 'Chan AW, et al. "SPIRIT 2013 statement." <i>Ann Intern Med</i>. 2013;158:200-207.',
                 'Li G, et al. "Outcome reporting in clinical trials." <i>JAMA</i>. 2007;295:1921-1928.',
             ]},
            {"slug": "quan-rigor", "title": "The Methodological Signal: Global Rigor",
             "code_src": "scripts/quan_totality_audit.py",
             "refs": [
                 'Schwartz D, Lellouch J. "Explanatory and pragmatic attitudes." <i>J Clin Epidemiol</i>. 2009;62:499-505.',
                 'Lang T, Siribaddana S. "Clinical trials have gone global?" <i>PLoS Med</i>. 2012;9:e1001228.',
             ]},
            {"slug": "benford-adherence", "title": "Benford Adherence & Reporting Integrity",
             "code_src": "scripts/advanced_stats_analysis.py",
             "refs": [
                 'Nigrini MJ. <i>Benford\'s Law: Applications for Forensic Accounting, Auditing, and Fraud Detection</i>. Wiley; 2012.',
                 'Diekmann A. "Not the first digit! Using Benford\'s Law to detect fraudulent scientific data." <i>J Appl Stat</i>. 2007;34:321-329.',
             ]},
            {"slug": "clinical-fitness", "title": "Survival Analysis & Research Fitness",
             "code_src": "scripts/fetch_trial_lifecycle.py",
             "refs": [
                 'Alemayehu C, et al. "Behind the mask of the African clinical trials landscape." <i>Trials</i>. 2018;19:519.',
                 'ClinicalTrials.gov API v2 Documentation. U.S. National Library of Medicine.',
             ]},
            {"slug": "recruitment-velocity", "title": "Recruitment Velocity & Enrollment Power",
             "code_src": "scripts/recruitment_audit.py",
             "refs": [
                 'Drain PK, et al. "Global migration of clinical trials." <i>Nat Rev Drug Discov</i>. 2018;17:765-766.',
                 'Murthy S, et al. "Participation in global health research." <i>Lancet</i>. 2015;386:1775-1776.',
             ]},
            {"slug": "completion-velocity", "title": "Completion Velocity",
             "code_src": "scripts/fetch_trial_lifecycle.py",
             "refs": [
                 'Ndounga Diakou LA, et al. "Mapping of clinical trials in sub-Saharan Africa." <i>Trials</i>. 2022;23:490.',
                 'ClinicalTrials.gov API v2 Documentation. U.S. National Library of Medicine.',
             ]},
            {"slug": "registration-proactivity", "title": "Registration Proactivity",
             "code_src": "scripts/fetch_trial_lifecycle.py",
             "refs": [
                 'Alemayehu C, et al. "Behind the mask of the African clinical trials landscape." <i>Trials</i>. 2018;19:519.',
                 'WHO. "International Clinical Trials Registry Platform." WHO, Geneva.',
             ]},
            {"slug": "network-entropy", "title": "Network Entropy & Structural Disorder",
             "code_src": "scripts/fetch_network_analysis.py",
             "refs": [
                 'Lang T, Siribaddana S. "Clinical trials have gone global?" <i>PLoS Med</i>. 2012;9:e1001228.',
                 'Drain PK, et al. "Global migration of clinical trials." <i>Nat Rev Drug Discov</i>. 2018;17:765-766.',
             ]},
            {"slug": "pca-variance", "title": "PCA Variance & Structural Drivers",
             "code_src": "scripts/info_topology_audit.py",
             "refs": [
                 'Ndounga Diakou LA, et al. "Mapping of clinical trials in sub-Saharan Africa." <i>Trials</i>. 2022;23:490.',
                 'Alemayehu C, et al. "Behind the mask of the African clinical trials landscape." <i>Trials</i>. 2018;19:519.',
             ]},
            {"slug": "regression-model", "title": "Regression Model of Trial Density",
             "code_src": "scripts/fetch_regression_model.py",
             "refs": [
                 'Isaakidis P, et al. "Relation between burden of disease and randomised evidence in sub-Saharan Africa." <i>BMJ</i>. 2002;324:702.',
                 'World Health Organization. "World Health Statistics 2024." WHO, Geneva.',
                 'ClinicalTrials.gov API v2 Documentation. U.S. National Library of Medicine.',
             ]},
        ]
    },
}

# ── Sentence role colors (E156 standard) ──
ROLE_COLORS = [
    ("#1b4f72", "#d4e6f1"),  # S1 Question - blue
    ("#0e6251", "#d1f2eb"),  # S2 Dataset - green
    ("#4a235a", "#e8daef"),  # S3 Method - purple
    ("#922b21", "#fadbd8"),  # S4 Result - red
    ("#7e5109", "#fdebd0"),  # S5 Robustness - orange
    ("#0b5345", "#d0ece7"),  # S6 Interpretation - teal
    ("#566573", "#d5d8dc"),  # S7 Boundary - gray
]
ROLE_NAMES = ["Question", "Dataset", "Method", "Primary Result", "Robustness", "Interpretation", "Boundary"]


def read_paper_body(slug):
    """Read E156 markdown and extract the body text (before ## Note Block)."""
    path = E156 / f"{slug}_e156.md"
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    # Remove BOM
    text = text.lstrip("\ufeff")
    # Remove the title line (# TITLE)
    lines = text.split("\n")
    body_lines = []
    started = False
    for line in lines:
        if line.startswith("# "):
            started = True
            continue
        if line.startswith("## "):
            break
        if started:
            body_lines.append(line)
    body = " ".join(body_lines).strip()
    # Collapse multiple spaces
    body = re.sub(r"\s+", " ", body)
    return body


def split_sentences(body):
    """Split body into sentences. E156 = exactly 7 sentences."""
    # Split on period followed by space and capital letter, or end of string
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', body)
    return sentences[:7]  # Cap at 7


def generate_dashboard_html(slug, title, body):
    """Generate a minimal dashboard for papers missing one."""
    sentences = split_sentences(body)
    sent_html = ""
    for i, s in enumerate(sentences[:7]):
        color, bg = ROLE_COLORS[i] if i < len(ROLE_COLORS) else ("#333", "#f0f0f0")
        role = ROLE_NAMES[i] if i < len(ROLE_NAMES) else f"S{i+1}"
        sent_html += f'''
        <div style="background:{bg};border-left:4px solid {color};padding:12px 16px;margin:8px 0;border-radius:6px;">
          <span style="color:{color};font-weight:700;font-size:12px;text-transform:uppercase;letter-spacing:0.05em;">{role}</span>
          <p style="margin:6px 0 0;color:#1d2430;line-height:1.6;">{escape(s)}</p>
        </div>'''

    words = body.split()
    word_count = len(words)

    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)} Dashboard</title>
  <style>
    :root {{
      --bg: #f5f2ea; --paper: #fffdf8; --ink: #1d2430; --muted: #5f6b7a;
      --line: #d8cfbf; --accent: #0d6b57; --accent-soft: #dcefe8;
      --shadow: 0 18px 40px rgba(42,47,54,0.08); --radius: 18px;
      --sans: "Georgia","Times New Roman",serif;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0; color: var(--ink); font-family: var(--sans); line-height: 1.5;
      background: radial-gradient(circle at top left, rgba(13,107,87,0.08), transparent 32%),
                  radial-gradient(circle at bottom right, rgba(141,79,45,0.08), transparent 28%),
                  var(--bg);
    }}
    .page {{ width: min(900px, calc(100vw - 32px)); margin: 32px auto 48px; }}
    .card {{
      background: var(--paper); border: 1px solid var(--line);
      border-radius: var(--radius); box-shadow: var(--shadow); padding: 28px; margin: 20px 0;
    }}
    .eyebrow {{
      color: var(--accent); font-size: 13px; letter-spacing: 0.08em;
      text-transform: uppercase; font-weight: 700; margin-bottom: 8px;
    }}
    h1 {{ margin: 0 0 12px; font-size: clamp(24px,3.5vw,36px); line-height: 1.1; }}
    .metric-row {{ display: flex; gap: 20px; flex-wrap: wrap; margin: 16px 0; }}
    .metric {{
      background: var(--accent-soft); padding: 12px 20px; border-radius: 10px;
      text-align: center; min-width: 120px;
    }}
    .metric-val {{ font-size: 28px; font-weight: 700; color: var(--accent); }}
    .metric-lab {{ font-size: 12px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; }}
    .body-text {{ font-size: 17px; line-height: 1.8; color: var(--ink); margin: 20px 0; }}
    .footer {{ text-align: center; color: var(--muted); font-size: 13px; margin-top: 32px; }}
    .footer a {{ color: var(--accent); }}
  </style>
</head>
<body>
  <div class="page">
    <div class="card">
      <div class="eyebrow">E156 Micro-Paper Dashboard</div>
      <h1>{escape(title)}</h1>
      <div class="metric-row">
        <div class="metric"><div class="metric-val">{word_count}</div><div class="metric-lab">Words</div></div>
        <div class="metric"><div class="metric-val">{len(sentences)}</div><div class="metric-lab">Sentences</div></div>
        <div class="metric"><div class="metric-val">Africa</div><div class="metric-lab">Region</div></div>
      </div>
    </div>
    <div class="card">
      <h2 style="margin:0 0 16px;font-size:20px;">Full Text</h2>
      <div class="body-text">{escape(body)}</div>
    </div>
    <div class="card">
      <h2 style="margin:0 0 16px;font-size:20px;">Sentence Structure</h2>
      {sent_html}
    </div>
    <div class="footer">
      <p>E156 Micro-Paper Format &middot; Data: ClinicalTrials.gov API v2</p>
      <p><a href="{GITHUB_REPO}">GitHub Repository</a></p>
    </div>
  </div>
</body>
</html>'''


# ── Shared CSS for group pages ──
SHARED_CSS = '''
:root {
  --bg: #f8f6f1; --paper: #fffdf8; --ink: #1d2430; --muted: #5f6b7a;
  --line: #d8cfbf; --accent: #0d6b57; --accent2: #7A5A10; --warn: #b33;
  --shadow: 0 12px 32px rgba(42,47,54,0.07); --radius: 14px;
  --serif: "Georgia","Times New Roman",serif;
  --mono: "Consolas","SFMono-Regular","Menlo",monospace;
}
* { box-sizing: border-box; margin: 0; }
body {
  color: var(--ink); font-family: var(--serif); line-height: 1.6;
  background: linear-gradient(135deg, #f0ede4 0%, #f8f6f1 50%, #efeadf 100%);
  min-height: 100vh;
}
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }

.page { width: min(1080px, calc(100vw - 32px)); margin: 0 auto; padding: 32px 0 64px; }

/* Header */
.masthead {
  text-align: center; padding: 40px 24px 32px; margin-bottom: 32px;
  border-bottom: 3px double var(--line);
}
.masthead .eyebrow {
  color: var(--accent); font-size: 13px; letter-spacing: 0.12em;
  text-transform: uppercase; font-weight: 700;
}
.masthead h1 {
  font-size: clamp(28px, 4vw, 44px); line-height: 1.08;
  margin: 8px 0 12px; font-weight: 700;
}
.masthead .desc {
  color: var(--muted); max-width: 70ch; margin: 0 auto; font-size: 17px;
}

/* Instructions */
.instructions {
  background: #fef9e7; border: 2px solid #f0d060; border-radius: var(--radius);
  padding: 28px 32px; margin-bottom: 36px;
}
.instructions h2 { font-size: 20px; margin-bottom: 16px; color: var(--accent2); }
.instructions ol { padding-left: 24px; }
.instructions li { margin: 8px 0; font-size: 15px; }
.instructions .warning {
  background: #fde8e8; border: 1px solid var(--warn); border-radius: 8px;
  padding: 12px 16px; margin-top: 16px; font-size: 14px; color: var(--warn);
}

/* Paper cards */
.paper-card {
  background: var(--paper); border: 1px solid var(--line);
  border-radius: var(--radius); box-shadow: var(--shadow);
  padding: 28px 32px; margin-bottom: 28px;
  page-break-inside: avoid;
}
.paper-card .num {
  display: inline-block; background: var(--accent); color: white;
  width: 32px; height: 32px; border-radius: 50%; text-align: center;
  line-height: 32px; font-size: 14px; font-weight: 700; margin-right: 12px;
}
.paper-card h3 { display: inline; font-size: 22px; vertical-align: middle; }
.paper-body {
  font-size: 16px; line-height: 1.85; margin: 20px 0;
  padding: 20px; background: #fafaf7; border-radius: 10px;
  border-left: 4px solid var(--accent);
}

/* Sentence breakdown */
.sent-strip { display: flex; gap: 3px; margin: 12px 0 20px; border-radius: 6px; overflow: hidden; }
.sent-strip .seg { height: 8px; flex: 1; }

/* Buttons */
.actions { display: flex; gap: 10px; flex-wrap: wrap; margin: 16px 0; }
.btn {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 8px 18px; border-radius: 8px; font-size: 14px;
  font-family: var(--serif); font-weight: 600; cursor: pointer;
  border: 1px solid var(--line); background: white; color: var(--ink);
  transition: all 0.15s;
}
.btn:hover { background: var(--accent); color: white; border-color: var(--accent); text-decoration: none; }
.btn-primary { background: var(--accent); color: white; border-color: var(--accent); }
.btn-primary:hover { background: #0a5444; }

/* References */
.refs { margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--line); }
.refs h4 { font-size: 14px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; }
.refs ol { padding-left: 20px; font-size: 14px; color: var(--muted); }
.refs li { margin: 4px 0; }

/* Note block */
.note-block {
  background: #f4f1ea; border-radius: 8px; padding: 14px 18px;
  margin-top: 16px; font-size: 13px; font-family: var(--mono);
}
.note-block dt { color: var(--accent); font-weight: 700; display: inline; }
.note-block dd { display: inline; margin: 0 16px 0 4px; color: var(--muted); }

/* E156 rules */
.rules {
  background: var(--paper); border: 1px solid var(--line);
  border-radius: var(--radius); padding: 24px 28px; margin-top: 36px;
}
.rules h2 { font-size: 18px; margin-bottom: 12px; }
.rules summary { cursor: pointer; font-weight: 600; color: var(--accent); }
.rules table { width: 100%; border-collapse: collapse; font-size: 14px; margin-top: 12px; }
.rules th, .rules td { padding: 6px 12px; text-align: left; border-bottom: 1px solid var(--line); }
.rules th { background: #f4f1ea; }

/* Footer */
.footer {
  text-align: center; margin-top: 48px; padding-top: 24px;
  border-top: 2px solid var(--line); color: var(--muted); font-size: 13px;
}
.footer a { color: var(--accent); }

@media (max-width: 640px) {
  .page { padding: 16px 8px 40px; }
  .paper-card { padding: 20px 16px; }
  .instructions { padding: 20px 16px; }
  .actions { flex-direction: column; }
}
'''


def generate_group_page(group_id, group):
    """Generate the full HTML page for a group."""
    cards_html = ""
    for i, paper in enumerate(group["papers"], 1):
        slug = paper["slug"]
        title = paper["title"]
        body = read_paper_body(slug)
        if not body:
            body = f"[Paper text not found for {slug}]"

        sentences = split_sentences(body)
        # Sentence color strip
        strip = '<div class="sent-strip">'
        for j in range(min(len(sentences), 7)):
            color, _ = ROLE_COLORS[j]
            strip += f'<div class="seg" style="background:{color};" title="{ROLE_NAMES[j]}"></div>'
        strip += '</div>'

        # References
        refs_html = ""
        if paper.get("refs"):
            refs_html = '<div class="refs"><h4>Suggested References</h4><ol>'
            for ref in paper["refs"]:
                refs_html += f"<li>{ref}</li>"
            refs_html += "</ol></div>"

        # Note block
        code_filename = slug.replace("_", "-") + ".py"
        note_html = f'''<div class="note-block">
          <dl>
            <dt>Type:</dt><dd>research</dd>
            <dt>App:</dt><dd><a href="{GITHUB_PAGES}/{group_id}/dashboards/{slug}.html">{slug} dashboard</a></dd>
            <dt>Code:</dt><dd><a href="{GITHUB_REPO}/tree/main/{group_id}/code/{code_filename}">{code_filename}</a></dd>
            <dt>Data:</dt><dd>ClinicalTrials.gov API v2</dd>
            <dt>Date:</dt><dd>2026-04-03</dd>
          </dl>
        </div>'''

        cards_html += f'''
    <div class="paper-card" id="paper-{i}">
      <div><span class="num">{i}</span><h3>{escape(title)}</h3></div>
      {strip}
      <div class="paper-body">{escape(body)}</div>
      <div class="actions">
        <a class="btn btn-primary" href="dashboards/{slug}.html" target="_blank" rel="noopener noreferrer">View Dashboard</a>
        <a class="btn" href="code/{code_filename}" download>Download Code (.py)</a>
        <a class="btn" href="#" onclick="downloadMd('{slug}', this); return false;">Download Paper (.md)</a>
      </div>
      {refs_html}
      {note_html}
    </div>'''

    # Paper data for markdown download
    paper_data_js = "const PAPERS = {\n"
    for paper in group["papers"]:
        slug = paper["slug"]
        body = read_paper_body(slug) or ""
        title = paper["title"]
        refs = paper.get("refs", [])
        code_filename = slug.replace("_", "-") + ".py"
        # Escape for JS string
        body_js = body.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
        title_js = title.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
        refs_js = "\\n".join(f"  {j+1}. {r}" for j, r in enumerate(refs))
        refs_js = refs_js.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${").replace("<i>", "").replace("</i>", "").replace('";', "")

        paper_data_js += f'  "{slug}": {{\n'
        paper_data_js += f'    title: `{title_js}`,\n'
        paper_data_js += f'    body: `{body_js}`,\n'
        paper_data_js += f'    refs: `{refs_js}`,\n'
        paper_data_js += f'    dashboard: `{GITHUB_PAGES}/{group_id}/dashboards/{slug}.html`,\n'
        paper_data_js += f'    code: `{GITHUB_REPO}/tree/main/{group_id}/code/{code_filename}`,\n'
        paper_data_js += f'  }},\n'
    paper_data_js += "};"

    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(group["title"])} — Africa E156 Student Papers</title>
  <style>{SHARED_CSS}</style>
</head>
<body>
  <div class="page">
    <div class="masthead">
      <div class="eyebrow">University of Uganda &middot; Africa E156 Series</div>
      <h1>{escape(group["title"])}</h1>
      <p class="desc">{escape(group["desc"])}</p>
    </div>

    <div class="instructions">
      <h2>Your Assignment: Rewrite &amp; Submit</h2>
      <ol>
        <li><strong>Read</strong> each AI-drafted E156 paper below. These are starting points, not finished work.</li>
        <li><strong>Study</strong> the interactive HTML dashboard to understand the underlying data and findings.</li>
        <li><strong>Download the code</strong> (.py) and review how the analysis was performed.</li>
        <li><strong>Rewrite the paper in your own voice.</strong> Keep the 7-sentence, 156-word E156 format. Add your own clinical context and Uganda-specific insights.</li>
        <li><strong>Add 2-3 references</strong> &mdash; verify the suggested ones below, and add PubMed or WHO sources you find relevant.</li>
        <li><strong>Include the GitHub links</strong> (dashboard + code) in your paper's Outside Note Block when submitting.</li>
        <li><strong>Submit</strong> to: <a href="{JOURNAL_URL}" target="_blank" rel="noopener noreferrer">Synthesis Medicine Journal</a></li>
      </ol>
      <div class="warning">
        <strong>Important:</strong> These papers are AI-generated drafts. The journal will check for originality.
        You must rewrite each paper substantially in your own words. Your perspective as a Ugandan researcher is valuable &mdash; add local context, verify the data, and make the paper yours.
        Each of the 12 papers below can be submitted as an independent publication.
      </div>
    </div>

    {cards_html}

    <div class="rules">
      <details>
        <summary>E156 Format Rules (click to expand)</summary>
        <p style="margin:12px 0;color:var(--muted);">Every E156 paper must follow these constraints exactly:</p>
        <table>
          <tr><th>Rule</th><th>Requirement</th></tr>
          <tr><td>Word count</td><td>Exactly 156 words</td></tr>
          <tr><td>Sentences</td><td>Exactly 7 sentences</td></tr>
          <tr><td>Paragraph</td><td>Single paragraph, no headings or links in body</td></tr>
          <tr><td>S1 (Question)</td><td>Population, intervention, main endpoint (~22 words)</td></tr>
          <tr><td>S2 (Dataset)</td><td>Studies, participants, scope, follow-up (~20 words)</td></tr>
          <tr><td>S3 (Method)</td><td>Synthesis design, model, effect scale (~20 words)</td></tr>
          <tr><td>S4 (Result)</td><td>Primary estimate with confidence interval (~30 words)</td></tr>
          <tr><td>S5 (Robustness)</td><td>Heterogeneity, sensitivity, consistency (~22 words)</td></tr>
          <tr><td>S6 (Interpretation)</td><td>Restrained plain-language meaning (~22 words)</td></tr>
          <tr><td>S7 (Boundary)</td><td>Limitation, scope restriction, or caution (~20 words)</td></tr>
        </table>
        <p style="margin:12px 0;font-size:14px;color:var(--muted);">
          <strong>House style:</strong> One idea per sentence. Numbers over adjectives. No hype or causal overreach.
          Limitation is mandatory. Body must make sense as a standalone screenshot.
        </p>
      </details>
    </div>

    <div class="rules" style="margin-top:20px;">
      <details>
        <summary>Outside Note Block Template (for your submission)</summary>
        <pre style="background:#f4f1ea;padding:16px;border-radius:8px;font-size:13px;margin-top:12px;overflow-x:auto;">
Type: research
Primary estimand: [your main metric]
App: {GITHUB_PAGES}/{group_id}/dashboards/[your-paper-slug].html
Data: ClinicalTrials.gov API v2 (public)
Code: {GITHUB_REPO}/tree/main/{group_id}/code/[your-paper-slug].py
DOI: [assigned after acceptance]
Version: 1.0
Date: [your submission date]
Certainty: [LOW | MODERATE | HIGH]

AI Transparency: This paper was drafted with AI assistance (Claude, Anthropic).
The author rewrote, verified, and takes full responsibility for the final content.</pre>
      </details>
    </div>

    <div class="footer">
      <p><a href="../">Back to All Groups</a></p>
      <p style="margin-top:8px;">
        <a href="{JOURNAL_URL}" target="_blank" rel="noopener noreferrer">Synthesis Medicine Journal</a> &middot;
        <a href="{GITHUB_REPO}" target="_blank" rel="noopener noreferrer">GitHub Repository</a> &middot;
        E156 Micro-Paper Format
      </p>
      <p style="margin-top:8px;">Mahmood Ahmad &middot; ORCID: 0009-0003-7781-4478</p>
    </div>
  </div>

  <script>
  {paper_data_js}

  function downloadMd(slug, el) {{
    const p = PAPERS[slug];
    if (!p) return;
    let md = "# " + p.title + "\\n\\n";
    md += p.body + "\\n\\n";
    md += "## References\\n\\n" + p.refs + "\\n\\n";
    md += "## Note Block\\n\\n";
    md += "- Type: research\\n";
    md += "- App: " + p.dashboard + "\\n";
    md += "- Code: " + p.code + "\\n";
    md += "- Data: ClinicalTrials.gov API v2\\n";
    md += "- Date: 2026-04-03\\n";
    const blob = new Blob([md], {{ type: "text/markdown" }});
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = slug + ".md";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }}
  ''' + '</scr' + '''ipt>
</body>
</html>'''


def generate_landing_page():
    """Generate the main index.html landing page."""
    group_cards = ""
    colors = ["#1b4f72", "#922b21", "#7e5109", "#0b5345"]
    for i, (gid, g) in enumerate(GROUPS.items()):
        color = colors[i]
        group_cards += f'''
    <a href="{gid}/" class="group-card" style="border-top: 4px solid {color};">
      <div class="group-num" style="background:{color};">Group {i+1}</div>
      <h2>{escape(g["title"])}</h2>
      <p>{escape(g["desc"])}</p>
      <div class="paper-count">12 papers</div>
    </a>'''

    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Africa E156 Series — University of Uganda Student Assignment</title>
  <style>
    :root {{
      --bg: #f8f6f1; --paper: #fffdf8; --ink: #1d2430; --muted: #5f6b7a;
      --line: #d8cfbf; --accent: #0d6b57;
      --serif: "Georgia","Times New Roman",serif;
    }}
    * {{ box-sizing: border-box; margin: 0; }}
    body {{
      color: var(--ink); font-family: var(--serif); line-height: 1.6;
      background: linear-gradient(135deg, #f0ede4 0%, #f8f6f1 50%, #efeadf 100%);
      min-height: 100vh;
    }}
    a {{ color: var(--accent); text-decoration: none; }}
    .page {{ width: min(1080px, calc(100vw - 32px)); margin: 0 auto; padding: 48px 0 64px; }}
    .masthead {{
      text-align: center; margin-bottom: 40px; padding-bottom: 32px;
      border-bottom: 3px double var(--line);
    }}
    .masthead .eyebrow {{
      color: var(--accent); font-size: 13px; letter-spacing: 0.12em;
      text-transform: uppercase; font-weight: 700;
    }}
    .masthead h1 {{
      font-size: clamp(32px, 5vw, 52px); line-height: 1.05;
      margin: 12px 0; font-weight: 700;
    }}
    .masthead .sub {{
      color: var(--muted); font-size: 18px; max-width: 65ch; margin: 0 auto;
    }}
    .intro {{
      background: var(--paper); border: 1px solid var(--line);
      border-radius: 14px; padding: 28px 32px; margin-bottom: 36px;
      box-shadow: 0 12px 32px rgba(42,47,54,0.07);
    }}
    .intro h2 {{ font-size: 20px; margin-bottom: 12px; }}
    .intro p {{ color: var(--muted); margin: 8px 0; }}
    .intro a {{ font-weight: 600; }}
    .groups {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; }}
    .group-card {{
      display: block; background: var(--paper); border: 1px solid var(--line);
      border-radius: 14px; padding: 24px 28px; text-decoration: none; color: var(--ink);
      box-shadow: 0 8px 24px rgba(42,47,54,0.06); transition: transform 0.2s, box-shadow 0.2s;
    }}
    .group-card:hover {{ transform: translateY(-4px); box-shadow: 0 16px 40px rgba(42,47,54,0.12); text-decoration: none; }}
    .group-num {{
      display: inline-block; color: white; padding: 4px 14px;
      border-radius: 6px; font-size: 13px; font-weight: 700;
      letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 12px;
    }}
    .group-card h2 {{ font-size: 20px; margin-bottom: 8px; }}
    .group-card p {{ color: var(--muted); font-size: 14px; margin-bottom: 12px; }}
    .paper-count {{
      font-size: 13px; color: var(--accent); font-weight: 600;
      text-transform: uppercase; letter-spacing: 0.05em;
    }}
    .footer {{
      text-align: center; margin-top: 48px; padding-top: 24px;
      border-top: 2px solid var(--line); color: var(--muted); font-size: 13px;
    }}
    @media (max-width: 640px) {{
      .groups {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <div class="page">
    <div class="masthead">
      <div class="eyebrow">E156 Micro-Paper Series</div>
      <h1>Africa Clinical Trials<br>Under the Microscope</h1>
      <p class="sub">48 evidence papers on clinical trial equity in Africa. Four thematic groups, twelve papers each. Your assignment: rewrite, verify, and submit.</p>
    </div>

    <div class="intro">
      <h2>What is this?</h2>
      <p>Each group below contains 12 AI-drafted E156 micro-papers about clinical trial inequity in Africa. Each paper is exactly 7 sentences and 156 words, backed by ClinicalTrials.gov data, with an interactive HTML dashboard and Python analysis code.</p>
      <p><strong>Your task:</strong> Read each paper, study the dashboard, understand the code, then <strong>rewrite the paper in your own voice</strong> before submitting to the <a href="{JOURNAL_URL}" target="_blank" rel="noopener noreferrer">Synthesis Medicine Journal</a>.</p>
      <p>Click your group below to get started.</p>
    </div>

    <div class="groups">
      {group_cards}
    </div>

    <div class="footer">
      <p>
        <a href="{JOURNAL_URL}" target="_blank" rel="noopener noreferrer">Synthesis Medicine Journal</a> &middot;
        <a href="{GITHUB_REPO}" target="_blank" rel="noopener noreferrer">GitHub Repository</a>
      </p>
      <p style="margin-top:8px;">Mahmood Ahmad &middot; ORCID: 0009-0003-7781-4478</p>
    </div>
  </div>
</body>
</html>'''


def copy_files():
    """Copy dashboards and code to output directory."""
    missing_dashboards = []

    for gid, group in GROUPS.items():
        dash_dir = OUT / gid / "dashboards"
        code_dir = OUT / gid / "code"
        dash_dir.mkdir(parents=True, exist_ok=True)
        code_dir.mkdir(parents=True, exist_ok=True)

        for paper in group["papers"]:
            slug = paper["slug"]

            # Dashboard
            src_dash = E156 / f"{slug}_dashboard.html"
            dst_dash = dash_dir / f"{slug}.html"
            if src_dash.exists():
                shutil.copy2(src_dash, dst_dash)
            else:
                missing_dashboards.append((gid, slug, paper["title"]))

            # Code
            code_src_path = SOURCE / paper["code_src"]
            code_filename = slug.replace("_", "-") + ".py"
            dst_code = code_dir / code_filename
            if code_src_path.exists():
                shutil.copy2(code_src_path, dst_code)
            else:
                print(f"WARNING: Code not found: {code_src_path}")

    return missing_dashboards


def generate_missing_dashboards(missing):
    """Generate dashboards for papers that don't have one."""
    for gid, slug, title in missing:
        body = read_paper_body(slug)
        if not body:
            print(f"WARNING: No body for {slug}, skipping dashboard generation")
            continue
        html = generate_dashboard_html(slug, title, body)
        dst = OUT / gid / "dashboards" / f"{slug}.html"
        dst.write_text(html, encoding="utf-8")
        print(f"Generated dashboard: {dst}")


def main():
    print("=== Africa E156 Student Platform Builder ===\n")

    # 1. Copy files
    print("Copying dashboards and code...")
    missing = copy_files()
    print(f"  Copied files. {len(missing)} dashboards need generation.\n")

    # 2. Generate missing dashboards
    if missing:
        print("Generating missing dashboards...")
        generate_missing_dashboards(missing)
        print()

    # 3. Generate group pages
    print("Generating group pages...")
    for gid, group in GROUPS.items():
        html = generate_group_page(gid, group)
        path = OUT / gid / "index.html"
        path.write_text(html, encoding="utf-8")
        print(f"  {path}")
    print()

    # 4. Generate landing page
    print("Generating landing page...")
    landing = generate_landing_page()
    (OUT / "index.html").write_text(landing, encoding="utf-8")
    print(f"  {OUT / 'index.html'}\n")

    # 5. Summary
    total_papers = sum(len(g["papers"]) for g in GROUPS.values())
    total_dashboards = sum(
        1 for gid, g in GROUPS.items()
        for p in g["papers"]
        if (OUT / gid / "dashboards" / f"{p['slug']}.html").exists()
    )
    total_code = sum(
        1 for gid, g in GROUPS.items()
        for p in g["papers"]
        if (OUT / gid / "code" / (p["slug"].replace("_", "-") + ".py")).exists()
    )
    print(f"DONE: {total_papers} papers, {total_dashboards} dashboards, {total_code} code files")
    print(f"Landing page: {OUT / 'index.html'}")
    for gid in GROUPS:
        print(f"  {gid}: {OUT / gid / 'index.html'}")


if __name__ == "__main__":
    main()
