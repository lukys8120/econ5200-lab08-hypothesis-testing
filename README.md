# Diagnosing Underpowered Studies and P-Hacking

**ECON 5200 · Causal Machine Learning & Applied Analytics · Lab 08**

## Objective

I audited two flawed conclusions, one from a pilot study too small to detect a real effect and one from a researcher who tested 20 subgroups and reported the one that came out significant, and then compared four tests on heavy-tailed earnings data.

## Methodology

- Computed the observed effect size and the achieved power of a 15-per-group pilot study against the true effect of $800 on an SD of $3,000 (d = 0.27), using `TTestIndPower` from statsmodels.
- Solved for the sample size per group needed for 80% power and reran the study at that size from the same population.
- Applied a Benjamini-Hochberg (BH) correction to the p-values from 20 subgroup tests in which no subgroup had a real effect.
- Calculated the chance of at least one false positive among 20 independent tests at alpha = 0.05, and checked it with 1,000 simulated replications.
- Wrote my own `bh_reject()` function, checked it against statsmodels, and ran it on a version of the subgroup data with two real effects planted.
- Compared Welch's t-test, Yuen's trimmed t-test and two permutation tests (difference in means and difference in 20% trimmed means) on log-normal earnings data with one extreme earner in each group.
- Simulated 5,000 study z-statistics and nudged the borderline ones (z between 1.5 and 1.96) to reproduce the "camel" shape of p-hacked results.
- Saved a `power_utils.py` module with a power summary function and a power curve plot.

## Key Findings

**The pilot study could not have detected the effect.** With 15 people per group it had 10.9% power, so it would miss the real $800 effect about 89% of the time. Its p = 0.6925 was not evidence that the program does not work. 80% power needed 222 people per group, and at that size the rerun gave p = 0.0012.

**The "significant" subgroup was noise.** The researcher's best result was Subgroup 12 with p = 0.018. After a BH correction, 0 of the 20 subgroups stayed significant. With 20 tests of true nulls there is a 64.2% chance of at least one p < 0.05 in theory, and 65.8% of my 1,000 simulated replications had one.

**My BH function matched statsmodels.** On the original data it rejected 0 of 20. With two real effects planted, BH flagged both of them, while Bonferroni flagged only 1.

**On heavy-tailed data the tests split by the statistic, not by the method.** The two tests on plain means found nothing (Welch's p = 0.2650, permutation p = 0.3496), because the outliers make the mean very noisy. The two tests on 20% trimmed means both found the effect (Yuen's p = 0.0066, permutation p = 0.0056).

**P-hacking inflated the share of significant results.** Pushing borderline studies over the line raised the share with |z| > 1.96 from 0.242 to 0.313.

## Repository Contents

| File | Description |
|---|---|
| `lab-ch08-diagnostic.ipynb` | Full lab notebook with rendered output |
| `src/power_utils.py` | Power summary and power curve functions for two-group t-tests |

## Data

All data is simulated with fixed seeds (`RANDOM_STATE = 42`): the pilot and rerun samples, the 20 subgroups, the log-normal earnings data with two planted outliers, and the 5,000 z-statistics.
