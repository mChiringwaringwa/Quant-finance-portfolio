# Factor-Based Asset Selection & Robust Portfolio Optimisation

## Objective

Develop a systematic quantitative portfolio construction framework that combines:

- Multi-factor asset selection
- Rolling factor estimation
- Hyperparameter optimisation
- Parameter stability analysis
- Covariance and correlation analysis
- Constrained maximum-Sharpe portfolio optimisation
- Frozen portfolio candidate generation
- Chronological out-of-sample validation

The objective is not simply to identify the best-performing portfolio in historical data, but to build a process that separates model development from genuinely unseen testing.

---

## Investment Universe

The initial investment universe consists of five large-cap US equities:

- AAPL — Apple
- MSFT — Microsoft
- NVDA — NVIDIA
- GOOG — Alphabet
- META — Meta Platforms

The S&P 500 (^GSPC) is used as the market benchmark for beta estimation.

### Data Period

Common usable period:

**28 July 2025 – 14 July 2026**

The data is divided chronologically into:

1. Development dataset
2. Final unseen out-of-sample test dataset

No future observations are used during model development.

---

# Methodology

## 1. Data Preparation

Historical price data is loaded from CSV files using pandas.

The datasets are:

- converted to datetime format,
- aligned to a common period,
- converted into a unified asset universe,
- sorted chronologically,
- divided into development and final test datasets.

The final test period remains unseen until all model and portfolio decisions are frozen.

---

## 2. Development / Final Test Split

The complete dataset is divided chronologically using an 80/20 split.

### Development Dataset

Used for:

- factor construction,
- asset selection,
- covariance estimation,
- correlation analysis,
- hyperparameter optimisation,
- portfolio optimisation.

### Final Test Dataset

Used only for final out-of-sample evaluation.

This separation reduces the risk of evaluating a strategy on information that influenced its construction.

---

# Factor Model

Four quantitative factors are calculated for each candidate asset.

## 1. Rolling Beta

Beta measures the sensitivity of an asset to movements in the S&P 500.

\[
\beta_i =
\frac{\operatorname{Cov}(R_i,R_m)}
{\operatorname{Var}(R_m)}
\]

A rolling beta is calculated using different candidate windows.

Lower beta receives a higher factor score.

---

## 2. Momentum

Momentum measures the historical price appreciation over a rolling window.

\[
Momentum_t =
\frac{P_t}{P_{t-k}}-1
\]

Higher momentum receives a higher score.

---

## 3. Volatility

Annualised rolling volatility is calculated from daily returns.

\[
\sigma_{annual}
=
\sigma_{daily}\sqrt{252}
\]

Lower volatility receives a higher score.

---

## 4. Rolling Sharpe Ratio

Rolling risk-adjusted performance is measured as:

\[
Sharpe =
\frac{\mu}{\sigma}\sqrt{252}
\]

Higher Sharpe receives a higher score.

---

# Factor Ranking

Each factor is converted into a percentile-based cross-sectional score.

The current specification gives equal weight to the four factors:

\[
AssetScore =
0.25(BetaScore)
+0.25(MomentumScore)
+0.25(VolatilityScore)
+0.25(SharpeScore)
\]

The three highest-scoring assets are selected for portfolio construction.

---

# Hyperparameter Optimisation

Rather than assuming that one lookback period is universally optimal, the model evaluates alternative factor windows.

### Parameter grid

| Factor    | Candidate Windows |
|-----------|-------------------|
| Beta      | 40, 60, 80 days   |
| Momentum  | 40, 60, 80 days   |
| Volatility| 10, 20, 30 days   |
| Sharpe    | 40, 60, 80 days   |

This produces:

\[
3\times3\times3\times3 = 81
\]

parameter combinations.

Each combination is evaluated using an internal chronological split of the development dataset.

---

# Parameter Stability

Parameter sensitivity is assessed by examining:

- validation Sharpe ratios,
- the range and dispersion of Sharpe ratios,
- frequency of selected asset combinations,
- parameter frequencies among configurations producing the leading portfolio,
- distance from the original baseline specification.

This provides a robustness diagnostic rather than selecting a parameter set solely because it produced the single highest historical score.

---

# Portfolio Selection

The factor optimisation repeatedly identified the following three-asset portfolio:

- AAPL
- GOOG
- META

This portfolio became the candidate universe for subsequent portfolio-weight optimisation.

---

# Covariance & Correlation Analysis

The development dataset is used to estimate:

- annualised covariance,
- pairwise correlation,
- individual asset volatility,
- portfolio volatility,
- diversification effects.

Portfolio variance is calculated as:

\[
\sigma_p^2 =
w^T\Sigma w
\]

and portfolio volatility as:

\[
\sigma_p = \sqrt{w^T\Sigma w}
\]

This allows the portfolio construction process to consider not only individual asset characteristics but also interactions between assets.

---

# Constrained Maximum-Sharpe Optimisation

After selecting AAPL, GOOG and META, portfolio weights are optimised using `scipy.optimize.minimize`.

The objective is:

\[
\max_w
\frac{w^T\mu-r_f}
{\sqrt{w^T\Sigma w}}
\]

subject to:

\[
\sum_i w_i=1
\]

and:

\[
0\leq w_i\leq w_{max}
\]

Several maximum-weight constraints are tested:

- 33.33%
- 40%
- 50%
- 75%
- 100%

This demonstrates how portfolio concentration constraints affect the risk-return trade-off.

---

# Frozen Portfolio Candidates

Before examining the final test dataset, five portfolio candidates were frozen:

| Portfolio    | AAPL | GOOG | META |
|--------------|---:|---:|---:|
| Equal Weight | 33.33% | 33.33% | 33.33% |
| Max 40       | 40% | 40% | 20% |
| Max 50       | 50% | 50% | 0% |
| Max 75       | 25% | 75% | 0% |
| Unconstrained| 20.42% | 79.58% | 0% |

These portfolios were determined before evaluation on the final unseen dataset.

---

# Final Out-of-Sample Test

The frozen portfolios are evaluated on the previously unseen final test period.

Performance measures include:

- Total Return
- Annualised Return
- Annualised Volatility
- Sharpe Ratio
- Maximum Drawdown
- Final Wealth

### Final OOS Result

The Equal-Weight portfolio was the strongest of the five frozen candidates on the final unseen dataset.

### Equal-Weight Portfolio

**AAPL 33.33% / GOOG 33.33% / META 33.33%**

Results:

- Total Return: **5.67%**
- Annualised Return: **33.56%**
- Annualised Volatility: **24.76%**
- Sharpe Ratio: **1.29**
- Maximum Drawdown: **−12.44%**

This is an important result because the equal-weight portfolio was not selected by maximising the final test performance. Its weights were frozen before the unseen test was examined.

---

# Transaction-Cost Sensitivity

Transaction costs are incorporated into a daily target-weight rebalancing framework.

The model estimates:

- portfolio turnover,
- transaction costs,
- net portfolio returns,
- volatility,
- Sharpe ratio,
- maximum drawdown.

The sensitivity analysis tests:

- 0 bps
- 10 bps
- 25 bps
- 50 bps

This provides a practical check on whether portfolio performance is sensitive to implementation costs.

---

# Look-Ahead Bias Control

The research process follows chronological information flow:

```text
Historical Data
      │
      ▼
Development Data
      │
      ├── Factor Construction
      ├── Hyperparameter Optimisation
      ├── Asset Selection
      ├── Covariance Estimation
      └── Portfolio Optimisation
      │
      ▼
Freeze Portfolio Candidates
      │
      ▼
Final Unseen Test Data
      │
      ▼
Out-of-Sample Evaluation
