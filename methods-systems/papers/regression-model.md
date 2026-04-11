# Regression Model of Trial Density

What country-level structural factors determine the distribution of 23,873 interventional clinical trials across 53 trial-active African nations? This ecological regression analysed log-transformed trials per million population as the dependent variable using six predictors: log GDP per capita, English-language status, PEPFAR recipient status, active conflict, WHO regulatory maturity level, and log population. The model achieved an adjusted R-squared of 0.80 using ordinary least squares with Gauss-Jordan matrix inversion implemented in pure Python. GDP per capita was the single strongest predictor (standardised beta 0.85), followed by English-language status and PEPFAR recipient status. Nigeria (379 trials, 223.8M population) massively underperformed while Rwanda (138 trials, 14.1M) dramatically overperformed. These findings suggest that governance quality is the dominant latent factor beyond structural predictors. Interpretation is limited by cross-sectional design and unmeasured confounders.

## References

1. Isaakidis P, et al. "Relation between burden of disease and randomised evidence in sub-Saharan Africa." BMJ. 2002;324:702.
2. World Health Organization. "World Health Statistics 2024." WHO, Geneva.
3. ClinicalTrials.gov API v2 Documentation. U.S. National Library of Medicine.

## Note Block

- Type: research
- App: https://mahmood726-cyber.github.io/africa-e156-students/methods-systems/dashboards/regression-model.html
- Code: https://github.com/mahmood726-cyber/africa-e156-students/blob/master/methods-systems/code/regression-model.py
- Data: ClinicalTrials.gov API v2
- Date: 2026-04-05
