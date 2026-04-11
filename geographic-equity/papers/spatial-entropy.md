# Spatial Entropy

In information theory applied to clinical research, does the Shannon entropy of trial site distribution reveal differences in geographic diversity between African and European research ecosystems? This analysis computed Shannon entropy in bits for the distribution of 23,873 African and 142,126 European trials across national units using ClinicalTrials.gov API v2 data. The normalised entropy (H/H_max) served as the primary estimand for distributional evenness, where 1.0 indicates perfect equality across all countries. Africa's normalised entropy was 0.49, meaning the continent uses only half its maximum possible geographic diversity for trial placement. Europe achieved a normalised entropy of 0.82, reflecting substantially more even distribution across its constituent nations. The information-theoretic deficit of 0.33 quantifies the geographic knowledge loss from Africa's concentrated research model. These findings frame research equity as a measurable information-theoretic property rather than a subjective political judgment. Interpretation is limited by the use of national rather than sub-national geographic units.

## References

1. Lang T, Siribaddana S. "Clinical trials have gone global: is this a good thing?" PLoS Med. 2012;9:e1001228.
2. Ndounga Diakou LA, et al. "Mapping of clinical trials in sub-Saharan Africa." Trials. 2022;23:490.

## Note Block

- Type: research
- App: https://mahmood726-cyber.github.io/africa-e156-students/geographic-equity/dashboards/spatial-entropy.html
- Code: https://github.com/mahmood726-cyber/africa-e156-students/blob/master/geographic-equity/code/spatial-entropy.py
- Data: ClinicalTrials.gov API v2
- Date: 2026-04-05
