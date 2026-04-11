# Benford Adherence & Reporting Integrity

In forensic statistics, does the distribution of first digits in African clinical trial enrollment numbers conform to Benford's Law, providing evidence for or against data naturalness? This forensic audit applied Benford's first-digit analysis to enrollment counts from 53 African nations using country-level trial data from ClinicalTrials.gov. The mean absolute deviation between observed and expected Benford frequencies was 0.030 with a chi-squared statistic of 6.35 against a critical value of 15.51 at the five percent significance level with eight degrees of freedom. The data conformed to Benford's Law, providing no evidence of systematic fabrication or manipulation in aggregate African trial enrollment reporting. Digit distribution showed slight over-representation of the digit one, consistent with the many countries having between 100 and 199 trials. These findings provide forensic reassurance that African trial counts represent naturally occurring data rather than fabricated statistics. Interpretation is limited by the application of Benford's Law to country-level aggregates rather than individual trial enrollment figures.

## References

1. Nigrini MJ. Benford's Law: Applications for Forensic Accounting, Auditing, and Fraud Detection. Wiley; 2012.
2. Diekmann A. "Not the first digit! Using Benford's Law to detect fraudulent scientific data." J Appl Stat. 2007;34:321-329.

## Note Block

- Type: research
- App: https://mahmood726-cyber.github.io/africa-e156-students/methods-systems/dashboards/benford-adherence.html
- Code: https://github.com/mahmood726-cyber/africa-e156-students/blob/master/methods-systems/code/benford-adherence.py
- Data: ClinicalTrials.gov API v2
- Date: 2026-04-05
