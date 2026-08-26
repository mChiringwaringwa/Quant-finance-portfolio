
# Quantitative Finance Portfolio

## Overview

This repository contains quantitative finance projects developed in Python, focusing on systematic asset selection, factor modelling, portfolio construction, portfolio optimization, risk measurement, and out-of-sample performance evaluation.

The projects apply mathematical, statistical, and financial engineering techniques to historical market data, with particular emphasis on robust quantitative research rather than relying solely on in-sample performance.

A key principle throughout the repository is the separation of model development, validation, and genuinely unseen out-of-sample testing.

---

## Projects

### Project 01 — Factor-Based Asset Selection & Robust Portfolio Optimization

**File:** `01_factor_asset_selection_portfolio_optimisation/asset_selection.py`

This project develops a systematic framework for selecting assets using multiple quantitative factors and subsequently constructing and evaluating alternative portfolio allocations.

# Asset Universe
The candidate investment universe consists of:
- AAPL
- MSFT
- NVDA
- GOOG
- META

The S&P 500 (^GSPC) is used as the market benchmark for the calculation of market-related factors, particularly rolling beta.

# Factor-Based Asset Selection

Four quantitative factors are calculated for each candidate asset:
- Rolling Beta
- Momentum
- Rolling Volatility
- Rolling Sharpe Ratio
  
The factors are ranked cross-sectionally across the candidate assets.

The ranking preferences are:
- Lower Beta → preferred
- Higher Momentum → preferred
- Lower Volatility → preferred
- Higher Sharpe Ratio → preferred
  
Each factor receives an equal 25% contribution to the composite asset score.
The three highest-scoring assets are then selected for portfolio construction.

# Robust Hyperparameter Selection
Rather than arbitrarily choosing factor lookback periods, the project evaluates a systematic hyperparameter grid:

| Factor    | Candidate Windows |
|-----------|-------------------|
| Beta      | 40, 60, 80 days   |
| Momentum  | 40, 60, 80 days   |
| Volatility| 10, 20, 30 days   |
| Sharpe    | 40, 60, 80 days   |

This produces:
3 × 3 × 3 × 3 = 81 parameter combinations
Each parameter combination is evaluated using a validation period that remains separate from the final unseen test period.

The analysis also examines:
- Validation Sharpe distribution
- Parameter sensitivity
- Frequency of parameter values among top-performing solutions
- Similarity to economically interpretable baseline parameters
  
This helps distinguish a potentially robust configuration from a parameter combination that performs well only because of the particular validation sample.

## Portfolio Construction
After selecting the investment universe, the project compares simple equal weighting with constrained portfolio optimization.
Equal-Weight Benchmark
The selected assets are first assigned equal weights:
    ω_i=1/N
For three selected assets this produces:
    (33.33%, 33.33%, 33.33%)
This portfolio serves as the transparent benchmark for evaluating whether optimization adds value.
The equal-weight portfolio is important because it provides a simple, model-independent reference point. The optimized portfolio therefore has to demonstrate value beyond simply producing attractive in-sample statistics.

# Constrained Maximum-Sharpe Optimization
The project then applies constrained portfolio optimization using the estimated expected returns and covariance matrix.
The optimization objective is to maximize:
  Sharpe=(ω^T μ)/√(ω^T ∑ω)
subject to:
  ∑_i(ω_i)=1
and:
  0 ≤ ω_i ≤ ω_max
Several maximum-weight constraints are tested:
- 33.3%
- 40%
- 50%
- 75%
- unconstrained

This allows the analysis to examine how concentration constraints affect the portfolio's expected return, volatility, and Sharpe ratio.

# Equal Weight vs Optimized Portfolio
A central research question in the project is:

Does constrained portfolio optimization provide a meaningful improvement over a simple equal-weight allocation?

The answer is evaluated using the final unseen out-of-sample period rather than relying only on optimization-period results.

The equal-weight portfolio is treated as the benchmark, while the constrained optimized portfolios are treated as alternative models.

Among the constrained alternatives, the 40% maximum-weight constraint produced the 40% / 40% / 20% portfolio, which was selected as the principal alternative allocation for further analysis.

The resulting portfolio therefore represents a controlled departure from equal weighting:

Equal-weight benchmark:
  33.33% /  33.33% / 33.33%

Constrained optimized alternative:
  40% / 40% / 20%
  
The purpose was not to force the optimized portfolio to outperform. Instead, the project tests whether the optimization process produces a useful improvement in the risk-return profile.

## Out-of-Sample Findings
The final evaluation uses a genuinely unseen test period.

The final test data is not used to:
- Select factor windows
- Select assets
- Optimize portfolio weights
- Modify the model
- Tune parameters
  
This creates a clean separation between model development and final evaluation.

The final analysis showed that the 40% / 40% / 20% constrained portfolio reduced portfolio risk relative to the equal-weight benchmark, but did not outperform the equal-weight benchmark in final out-of-sample performance.

This is an important research result rather than a failure of the project.

It demonstrates that:
An optimization model can improve the risk characteristics of a portfolio without necessarily improving absolute or risk-adjusted out-of-sample returns.

The result also highlights the importance of using simple benchmarks when evaluating quantitative models.

## Risk and Performance Analysis
The project evaluates portfolios using:
- Total return
- Annualized return
- Annualized volatility
- Sharpe ratio
- Maximum drawdown
- Final wealth
- Covariance matrix
- Correlation matrix
- Portfolio variance
- Portfolio volatility
- Marginal risk contribution
- Component risk contribution
  
The analysis also examines the diversification effect by comparing individual asset volatility with portfolio-level volatility and comparing average pairwise correlations between portfolios.

# Benchmark-Relative Analysis
The 40% / 40% / 20% portfolio is compared directly with the equal-weight benchmark using:

Active Return
  R_active = R_portfolio - R_benchmark

Active Weights
  ω_active = ω_portfolio - ω_benchmark

Tracking Error
  TE = σ(R_portfolio - R_benchmark )

Information Ratio
  IR = (Annualized Active Return)/(Annualized Tracking Error)

This allows the project to evaluate the optimized portfolio from both an absolute-performance and benchmark-relative perspective.

# Risk Contribution
The project also decomposes portfolio risk into individual asset contributions.

For a portfolio with covariance matrix ∑ and weights ω:
  σ_p=√(ω^T ∑ω)

The analysis calculates:
- Marginal Risk Contribution
- Component Risk Contribution
- Percentage Risk Contribution

This provides an additional perspective on whether the optimized allocation is producing a more balanced or concentrated risk profile.

# Transaction-Cost Sensitivity
The project tests the effect of transaction costs using:
- 0 bps
- 10 bps
- 25 bps
- 50 bps

The analysis examines whether portfolio performance remains economically meaningful after allowing for trading costs.

# Validation Framework
The project uses two chronological layers of validation.

Outer Split
80% Development / 20% Final Unseen Test

The final 20% is held completely untouched until all model-development decisions have been completed.

Inner Development Split
The development period is further divided into:

80% Optimization Train / 20% Validation

The validation period is used for hyperparameter selection.

This produces the following research structure:
 Historical Data 
       │ 
       ├── 80% Development 
       │      │ 
       │      ├── 80% Optimization Train 
       │      │ 
       │      └── 20% Validation 
       │
       └── 20% Final Unseen Test 
      
The final test is therefore used only for final model evaluation.

## Key Research Principles
The projects emphasize the following quantitative research principles:

- Chronological data splitting
- Separation of model development and final testing
- Out-of-sample evaluation
- Hyperparameter sensitivity
- Parameter robustness
- Factor-based asset selection
- Portfolio diversification
- Constrained optimization
- Risk-adjusted performance measurement
- Benchmark-relative analysis
- Transaction-cost sensitivity
- Risk attribution
- Avoidance of look-ahead bias

# Data Workflow
The repository uses locally saved CSV market data rather than repeatedly downloading historical data during each project.

Project 01:
- Reads the prepared CSV files
- Identifies and standardizes the date and closing-price fields
- Aligns all assets to common trading dates
- Removes observations with missing prices
- Creates a reusable processed price dataset
- Saves the processed dataset for use by subsequent projects

This makes the research workflow more reproducible and prevents downstream projects from unnecessarily re-downloading the same historical data.

# Technologies
The projects are implemented primarily using:
- Python
- pandas
- NumPy
- SciPy

Key techniques include:
- Data manipulation with pandas
- Numerical computation with NumPy
- Statistical calculations
- Covariance and correlation analysis
- Portfolio mathematics
- Constrained numerical optimization using SciPy

---

### Project 02 — Portfolio Risk & Performance Analytics

**File:** `project_02_portfolio_risk/portfolio_risk_performance.py`

This project extends the quantitative research workflow into portfolio risk and performance analytics.

The analysis includes:

- Daily return calculation
- Portfolio return calculation
- Benchmark comparison
- Annualized return
- Annualized volatility
- Sharpe ratio
- Maximum drawdown
- Covariance matrix analysis
- Portfolio variance
- Portfolio volatility
- Marginal risk contribution
- Component risk contribution
- Transaction-cost sensitivity
- Active return
- Active weights
- Tracking error
- Information ratio

The project demonstrates how a portfolio performance can be evaluated from both an absolute risk-return perspective and a benchmark-relative perspective.

---

The final division is becomes very clean Work
|               | Project 01 |   Project 02|
|-----------|-------------------|-----------------|
|Raw CSV loading     |             ✓     |               —|
|Data cleaning/alignment |         ✓    |                —|
|Processed data         |          ✓    |                Reads|
|Factor construction     |         ✓    |                —|
|Beta                   |          ✓   |                 —|
|Momentum               |          ✓   |                 —|
|Volatility             |          ✓  |                  —|
|Sharpe factor          |          ✓  |                  —|
|Factor ranking         |          ✓   |                 —|
|Asset selection        |          ✓  |                  —|
|Hyperparameter optimisation|      ✓  |                  —|
|Parameter robustness    |         ✓  |                  —|
|Covariance for construction|      ✓   |                 —|
|Constrained optimisation  |       ✓   |                 —|
|Equal-weight benchmark  |         ✓   |                 Reads|
|40/40/20 alternative |            ✓   |                 Reads|
|Freeze portfolios   |             ✓   |                 Reads|
|Final OOS test      |             ✓  |                  Uses|
|Transaction-cost sensitivity |    ✓  |                  —|
|Active return   |                 —   |                 ✓|
|Active weights   |                —   |                 ✓|
|Tracking error    |               —   |                 ✓|
|Information ratio   |             —  |                  ✓|
|Risk contribution    |            —   |                 ✓|
|Performance attribution |         —   |                 ✓|

---
## Research Interpretation
An important principle demonstrated by these projects is that model complexity does not automatically translate into superior investment performance.

The factor-selection and constrained-optimization framework provides a systematic and mathematically disciplined approach to portfolio construction. However, the final out-of-sample comparison demonstrates the importance of testing the model against a simple benchmark.

In this study:
- Equal weighting provided a transparent benchmark.
- Constrained optimization produced alternative allocations.
- The 40% maximum-weight constraint produced a 40% / 40% / 20% allocation.
- The constrained portfolio demonstrated lower risk than the equal-weight benchmark.
- However, it did not outperform the equal-weight benchmark in the final unseen period.

Therefore, the research conclusion is not that optimization universally improves investment performance.

Instead, the project demonstrates a more important quantitative research principle:

Portfolio optimization should be judged by genuinely out-of-sample risk-adjusted performance and benchmark-relative results, rather than by in-sample optimization statistics alone.


## Author

McDonald Chiringwaringwa

BSc Honours Applied Mathematics  
MSc Financial Engineering  
Actuarial Professional Examinations: CT1, CT3, CT4, CT8

---

## Disclaimer

These projects are for research, educational, and portfolio demonstration purposes only. 
They do not constitute investment advice or a recommendation to buy or sell any security.
