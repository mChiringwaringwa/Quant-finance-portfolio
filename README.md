### Quantitative Finance Portfolio

## Overview

This repository contains a sequence of quantitative finance projects developed in Python, covering:

- Systematic asset selection
- Factor modelling
- Portfolio construction
- Constrained portfolio optimization
- Portfolio risk analysis
- Performance attribution
- Systematic short-term trading
- Walk-forward validation
- Parameter sensitivity
- Regime robustness
- Out-of-sample evaluation

The projects apply mathematical, statistical, and financial engineering techniques to historical market data, with particular emphasis on robust quantitative research rather than relying solely on in-sample performance.

A central principle throughout the repository is the separation of:

**Model Development → Validation → Final Unseen Out-of-Sample Evaluation**

The three projects are deliberately separated so that asset selection, portfolio construction, portfolio analytics, and trading decisions are not mixed together.

---

# Research Architecture

The repository follows a three-stage quantitative investment workflow:

```text
PROJECT 01
Factor-Based Asset Selection & Portfolio Construction
                    |
                    | Frozen Portfolio Specification
                    v
PROJECT 02
Portfolio Risk & Performance Analytics
                    |
                    | Same Frozen Portfolio
                    v
PROJECT 03
Systematic Short-Term Trading Engine
---

Each project answers a different research question.

Project 01
Which assets should be selected and how should the portfolio be constructed?

Project 02
How did the selected portfolio perform, what risks did it carry, and where did those risks and returns come from?

Project 03
Can systematic short-term trading dynamically control exposure to the same selected portfolio?

This separation creates a clean quantitative research architecture:

Asset Selection
      ↓
Portfolio Construction
      ↓
Portfolio Risk & Performance Analysis
      ↓
Short-Term Trading Overlay

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

# Equal-Weight Benchmark
The selected assets are first assigned 

equal weights:
    ω_i=1/N

For three selected assets this produces:
    (33.33%, 33.33%, 33.33%)

This portfolio serves as the transparent benchmark for evaluating whether optimization adds value.

The equal-weight portfolio is important because it provides a simple, model-independent reference point. 
The optimized portfolio therefore has to demonstrate value beyond simply producing attractive in-sample statistics.

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

** Does constrained portfolio optimization provide a meaningful improvement over a simple equal-weight allocation? **

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
** An optimization model can improve the risk characteristics of a portfolio without necessarily improving absolute or risk-adjusted out-of-sample returns. **

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

This demonstrates that portfolio weights do not necessarily correspond directly to portfolio risk contributions.

An asset's contribution to total portfolio risk depends on its:
-Portfolio weight
-Volatility
-Covariance with the other holdings

## Transaction-Cost Sensitivity
The project tests the effect of transaction costs using:
- 0 bps
- 10 bps
- 25 bps
- 50 bps

The analysis examines whether portfolio performance remains economically meaningful after allowing for trading costs.

## Validation Framework
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
      |
      +---- 80% Development
      |          |
      |          +---- 80% Optimization Train
      |          |
      |          +---- 20% Validation
      |
      +---- 20% Final Unseen Test
      
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

## Data Workflow
The repository uses locally saved CSV market data rather than repeatedly downloading historical data during each project.

Project 01:
- Reads the prepared CSV files
- Identifies and standardizes the date and closing-price fields
- Aligns all assets to common trading dates
- Removes observations with missing prices
- Creates a reusable processed price dataset
- Saves the processed dataset for use by subsequent projects

The principal frozen portfolio is:
AAPL    40%
GOOG    40%
META    20%

Once this portfolio specification is frozen, downstream projects do not perform asset selection or portfolio-weight optimization.

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

The purpose is to answer:
** How did the portfolios produced by Project 01 perform during the final out-of-sample period, what risks did they carry, and where did those risks and returns come from? **

Project 02 treats the Project 01 portfolio specifications as frozen inputs.

It does not:
-Re-select assets
-Re-optimize portfolio weights
-Change the portfolio construction methodology

# Portfolios
Two Project 01 portfolio specifications are analysed.

Equal-Weight Benchmark
AAPL = 33.33%
GOOG = 33.33%
META = 33.33%

Max-40 Alternative
AAPL = 40%
GOOG = 40%
META = 20%

The Max-40 portfolio is inherited from Project 01 rather than being re-created or re-optimized in Project 02.

## Risk and Performance Analysis
The analysis includes:

- Total return
- Annualized return
- Annualized volatility
- Sharpe ratio
- Maximum drawdown
- Final wealth
- Covariance matrix
- Portfolio variance
- Portfolio volatility
- Marginal risk contribution
- Component risk contribution
- Active return
- Active weights
- Tracking error
- Information ratio
- Historical Value at Risk
- Expected Shortfall
- Performance attribution

The project demonstrates how a portfolio performance can be evaluated from both an absolute risk-return perspective and a benchmark-relative perspective.


## Key Findings
The final out-of-sample analysis showed approximately:

|Portfolio  | Total Return| |---------|-------------------|
|Equal Weight | 5.75% |
|Max-40 | 5.07% |

The Max-40 portfolio therefore did not outperform the equal-weight benchmark during the analysed period.

The analysis also showed that:
- Active allocation generated negative benchmark-relative performance.
- Risk contributions were not proportional to portfolio weights.
- Historical VaR and Expected Shortfall provided additional information about tail risk.
- Benchmark-relative analysis showed that taking active portfolio risk did not translate into superior performance during the analysed period.

The important research lesson is:

** Portfolio construction should be evaluated using both performance and risk rather than relying solely on expected return or optimization statistics.**
---

### Project 03 — Systematic Short-Term Trading Engine

**File:** project_03_systematic_trading/systematic_trading.py

Project 03 develops and validates a systematic short-term trading overlay applied to the portfolio selected and frozen in Project 01.

The central question is:
** Can systematic technical trading dynamically control short-term exposure to the frozen portfolio? **

Project 03 does not attempt to determine which assets should be held.

That question was already addressed in Project 01.

Instead, Project 03 keeps the portfolio composition fixed and focuses on:
- Trading signals
- Trading parameter selection
- Exposure management
- Walk-forward validation
- Out-of-sample trading performance

# Frozen Portfolio
The trading engine inherits the Project 01 portfolio:

| Asset | Frozen Weight| |---------|------------|
|AAPL | 40% |
|GOOG | 40% |
|META | 20% |

The portfolio weights are not redefined or optimized by Project 03.

Project 03 therefore does not perform:
- Asset selection
- Portfolio-weight optimization
- Strategic portfolio construction

Only trading parameters are optimized.

# Trading Strategy
The strategy combines:
- Simple Moving Averages
- Relative Strength Index (RSI)

Two moving averages are calculated:
SMA_short 
And:
SMA_long

A long signal requires:
SMA_short > SMA_long 
And:
RSI > RSI_threshold

The signal is therefore:
Signal = 1  → Invested
Signal = 0  → No exposure / Cash

# Look-Ahead Bias Control
Trading signals are lagged by one trading day before being applied to returns.

The strategy return is:
R_strategy,t = Signal_t-1 * R_t

Rather than:
Signal_t * R_t 

This prevents information from day t from being used to generate a return on the same day.

This is an important safeguard against look-ahead bias.

# Portfolio-Level Trading
Signals are generated separately for:
AAPL
GOOG
META

The resulting asset-level strategy returns are then combined using the frozen Project 01 weights.

For example, if:

AAPL = Invested
GOOG = Not Invested
META = Invested

the portfolio exposure remains:
AAPL = 40%
GOOG = 0%
META = 20%

The active assets are not renormalised.
Renormalising the active assets would dynamically change the Project 01 portfolio weights and therefore violate the frozen-portfolio architecture.

This means the strategy can reduce total portfolio exposure and effectively hold the remaining capital outside active positions.

# Development / Final Test Framework

The historical sample is divided chronologically into:

80% Development
20% Final Unseen Test

Development Period
28 July 2025
to
1 May 2026

Observations:
193

Final Unseen Test Period
4 May 2026
to
14 July 2026

Observations:
49

The final test period remains outside the initial parameter-selection process.

# Parameter Optimisation

The initial parameter grid contains:

Short SMA
10
15
20
25

Long SMA
40
50
60

RSI Threshold
60
70
80

Total combinations:
4 * 3 * 3 = 36

The best development specification was:
Short SMA = 25
Long SMA  = 40
RSI       = 60

Development-period return:
7.39%

The development result is not treated as evidence of future profitability.

It is used to establish a candidate trading specification before final unseen testing.

## Expanding Walk-Forward Validation
An expanding walk-forward procedure was implemented using:

Training window = 100 observations
Test window     = 30 observations

At each step:
- Historical observations available at that point are used for training.
- Trading parameter combinations are evaluated.
- The best parameters are selected.
- The selected parameters are applied to the following unseen test window.
- The training sample is expanded.
- The process is repeated.

The expanding procedure selected:
25 / 60 / 60
for all three reported test windows.

This indicates strong parameter stability across the observed expanding windows.

Project 03 Expanding Walk-Forward Results

|Method |Average Return | Total Compounded Return|
|-------|--------------|-----------------|
|Optimized | -0.355% | -1.074% |
|Fixed | 0.986% | 2.973% |
|Buy & Hold | 2.067% | 5.529% |

Robustness statistics:

Average Optimized - Fixed = -0.013408
Std. Dev. Difference      = 0.007588
T-statistic               = -3.060644
Optimized Wins             = 0

Frequent re-optimization therefore did not improve performance relative to the fixed specification during the observed expanding walk-forward periods.

## Rolling Walk-Forward Validation
A rolling walk-forward procedure was also implemented.

Configuration:
Training window = 100 observations
Test window     = 30 observations

Unlike the expanding approach, the rolling procedure keeps the training window fixed and uses the most recent historical observations.

The rolling parameter selections were:
25 / 60 / 60
25 / 50 / 60
20 / 40 / 60

This indicates greater adaptation to recent data than the expanding procedure.

However, the additional adaptation did not produce better walk-forward performance.

# Rolling Walk-Forward Results

|Method |Average Return | Total Compounded Return|
|-------|--------------|-----------------|
|Optimized | -0.026% | -0.958% |
|Fixed | 0.986% | 2.973% |
|Buy & Hold | 2.067% | 5.529% |

Rolling robustness statistics:
Average Optimized - Fixed = -0.010116
Std. Dev. Difference      = 0.003696
T-statistic               = -4.740825
Optimized Wins             = 0

Again, repeated optimization did not improve performance relative to the fixed strategy.

# Parameter Stability
The expanding procedure showed:
25 / 60 / 60
25 / 60 / 60
25 / 60 / 60

The rolling procedure showed:
25 / 60 / 60
25 / 50 / 60
20 / 40 / 60

The expanding approach therefore showed stronger parameter stability, while the rolling approach adapted more substantially to recent data.

However, additional adaptation did not translate into better walk-forward performance.

# Parameter Sensitivity
A separate development-period sensitivity analysis examined:

Short SMA = 8 to 17
Long SMA  = 38 to 52
RSI       = 70

The resulting heatmap evaluates development-period return across combinations of short and long moving-average windows.

The heatmap shows a relatively broad region of stronger development-period performance, particularly around approximately:

Short SMA ≈ 14–17
Long SMA  ≈ 43–52

This suggests that development performance is not entirely concentrated in one precise short/long SMA combination.

However, RSI was fixed at 70 in this sensitivity analysis.

Therefore, the heatmap should be interpreted as a parameter-sensitivity diagnostic rather than confirmation of a universal optimum.

# Regime Robustness
The strategy was evaluated across different market regimes.

The regime framework distinguishes environments such as:

Bull_LowVol
Bull_HighVol
Bear_LowVol
Bear_HighVol

The purpose is to investigate whether strategy behaviour changes under different combinations of trend and volatility.

The development analysis showed meaningful differences between regimes.

This indicates that strategy effectiveness is potentially regime dependent rather than uniform across all market environments.

# Active Exposure Analysis
The strategy does not remain continuously invested.

Asset-level diagnostics showed:

Asset   Frozen Weight   Average Signal  Signal = 1 Days   Signal = 0 Days
|--------|-------|-----------|----------|-------|
| AAPL | 40% | 29.34% | 71 | 171|
|GOOG  | 40% | 30.58% | 74 | 168|
|META  | 20% | 1.24%  | 3  | 239|

Portfolio-level active exposure was:

Average active exposure = 24.21%
Minimum active exposure  = 0%
Maximum active exposure  = 80%

This indicates that the trading overlay is highly selective and frequently reduces market exposure.

The strategy therefore behaves more like an exposure-management overlay than a continuously invested replacement for the strategic portfolio.

## Final Unseen Out-of-Sample Test
The final 20% of observations were kept completely outside the initial parameter-selection process.

Three trading approaches were evaluated:
- Expanding Optimized
- Rolling Optimized
- General Fixed

These were compared with:
- Frozen Portfolio Buy & Hold

The final parameter specifications converged to:

Expanding Optimized:
25 / 40 / 60

Rolling Optimized:
25 / 40 / 60

General Fixed:
25 / 40 / 60

Therefore, all three trading approaches generated the same final OOS trading path.

## Final OOS Results

|Strategy | Total Return |  Annualized Return | Annualized Volatility | Sharpe | Max Drawdown|
|--------|-------------|-----------------|------------------|-------|-----------|
|Expanding Optimized | 4.071% | 22.780%| 9.177% | 2.282 | -1.409%|
|Rolling Optimized | 4.071% | 22.780%| 9.177% | 2.282 | -1.409%|
|General Fixed | 4.071% | 22.780% | 9.177%| 2.282  | -1.409%|
|Frozen Portfolio Buy & Hold | 4.235%| 23.776%  | 22.508%  | 1.058  | -12.014%|

## Final OOS Interpretation
The systematic trading overlay did not outperform Buy & Hold in absolute return.

Trading Strategy = 4.071%
Buy & Hold       = 4.235%

The difference was approximately:
-0.164 percentage points

However, the risk characteristics were substantially different.

Annualized Volatility
Trading Strategy = 9.18%
Buy & Hold       = 22.51%

Maximum Drawdown
Trading Strategy = -1.41%
Buy & Hold       = -12.01%

Sharpe Ratio
Trading Strategy = 2.28
Buy & Hold       = 1.06

The principal observed benefit was therefore:
- Risk reduction rather than superior absolute return.
- The strategy sacrificed a small amount of return while substantially reducing realised volatility and maximum drawdown during the final unseen period.

# Final OOS Equity Curve
The final OOS equity curve provides a visual comparison between:
- Expanding Optimized
- Rolling Optimized
- General Fixed
- Frozen Portfolio Buy & Hold

The Buy & Hold portfolio experienced a substantial drawdown during part of the final test period before recovering.

The systematic trading overlay substantially reduced participation during this period.

The three trading curves overlap because all three final OOS approaches converged to:
25 / 40 / 60

This is not a failure of the validation framework.

Rather, it demonstrates convergence of the different parameter-selection procedures during the final unseen period.

---

### Research Interpretation

## Overall Research Findings
The three projects collectively demonstrate several important quantitative research principles.

# 1. Systematic Asset Selection Can Be Separated from Portfolio Construction

Project 01 establishes a quantitative investment universe using multiple factors before constructing alternative portfolios.

This prevents discretionary asset selection from being mixed with portfolio optimization.

# 2. Portfolio Optimization Does Not Guarantee Superior Out-of-Sample Performance

Project 01 showed that the constrained 40% / 40% / 20% portfolio did not outperform the equal-weight benchmark in the final unseen period.

This demonstrates why optimized in-sample statistics should not be treated as proof of investment superiority.

# 3. Portfolio Weights Do Not Fully Describe Portfolio Risk

Project 02 demonstrates that an asset's contribution to total portfolio risk depends on:
- Its weight
- Its volatility
- Its covariance with the other holdings

Therefore:
Nominal portfolio allocation and actual risk allocation are different concepts.

# 4. Benchmark-Relative Performance Matters

Project 02 evaluates the alternative portfolio through:
- Active return
- Active weights
- Tracking error
- Information ratio
- Risk contribution
- Performance attribution
- VaR
- Expected Shortfall

This provides a more complete assessment than looking only at total return.

# 5. Trading Can Reduce Exposure Without Changing the Strategic Portfolio

Project 03 demonstrates that a short-term trading overlay can be applied to the frozen Project 01 portfolio without changing the strategic portfolio weights.

The architecture is:

Strategic Portfolio
        ↓
Frozen Weights
        ↓
Trading Signals
        ↓
Dynamic Exposure
        ↓
Portfolio Trading Return

This separates strategic asset allocation from tactical trading decisions.

# 6. Frequent Parameter Re-optimization Did Not Improve Walk-Forward Performance

Both expanding and rolling walk-forward analysis showed that optimized trading parameters underperformed the fixed strategy during the observed validation periods.

This provides an important quantitative research lesson:

** More frequent optimization does not necessarily produce better out-of-sample performance.**

It may instead introduce unnecessary adaptation to historical noise.

# 7. The Trading Overlay Showed Substantial Risk Reduction in the Final Unseen Test

The final OOS test showed:

|Metric | Buy & Hold | Trading Overlay|
|------|-------------|-----------------|
|Total Return  | 4.235%  | 4.071%|
|Annualized Volatility | 22.51% | 9.18%|
|Sharpe Ratio | 1.06 |  2.28|
|Maximum Drawdown | -12.01% | -1.41%|

The trading overlay therefore produced a similar absolute return while materially reducing realised volatility and drawdown in the final unseen sample.

## Key Quantitative Research Principles

The repository emphasizes:
- Chronological data splitting
- Development versus final-test separation
- Out-of-sample evaluation
- Hyperparameter optimization
- Parameter sensitivity
- Parameter stability
- Walk-forward validation
- Expanding-window validation
- Rolling-window validation
- Factor-based asset selection
- Portfolio diversification
- Constrained portfolio optimization
- Covariance-based risk analysis
- Risk contribution
- Performance attribution
- Benchmark-relative analysis
- Technical trading signals
- Active exposure analysis
- Regime robustness
- Look-ahead-bias control
- Risk-adjusted performance measurement

The overall philosophy is:
A quantitative model should be judged by how it behaves on data that was not used to construct or tune it.

## Data Workflow
The repository uses locally saved CSV market data rather than repeatedly downloading historical data during each project.

# Project 01
Project 01:
Reads prepared CSV files
Identifies and standardizes date and price fields

Aligns assets to common trading dates
Removes observations with missing prices
Creates a reusable processed price dataset
Produces the frozen portfolio specification

# Project 02
Project 02 reads the processed market data and frozen portfolio specifications generated by Project 01.
It does not redefine the investment universe or portfolio weights.

# Project 03
Project 03 reads the frozen portfolio specification and applies the trading engine to the same selected assets.

This creates a reproducible data flow:

Raw Market Data
      ↓
Project 01
Data Preparation
      ↓
Factor Analysis
      ↓
Asset Selection
      ↓
Portfolio Construction
      ↓
Frozen Portfolio
      ↓
      ┌───────────────────────┐
      ↓                       ↓
Project 02               Project 03
Risk & Performance        Short-Term
Analytics                 Trading Overlay


## Project Responsibilities

| Research component  | Project 01 |   Project 02|Project 03 |
|-----------|-------------------|-----------------|-----------------|
|Raw CSV loading     |            ✓     |               —|Reads prepared data | 
|Data cleaning/alignment |         ✓    |                —|Uses prepared data | 
|Processed data         |          ✓    |                Reads|Reads | 
|Factor construction     |         ✓    |                —|— | 
|Beta                  |          ✓   |                 —|— | 
|Momentum               |          ✓   |                 —|— | 
|Volatility             |          ✓  |                  —|— | 
|Sharpe factor          |          ✓  |                  —|— | 
|Factor ranking         |          ✓   |                 —|— | 
|Asset selection        |          ✓  |                  —|— | 
|Hyperparameter optimisation|      ✓  |                  —|— | 
|Parameter robustness    |         ✓  |                  —|— | 
|Covariance for construction|      ✓   |                 —|— | 
|Constrained optimisation  |       ✓   |                 —|— | 
|Equal-weight benchmark  |         ✓   |                 Reads|— | 
|40/40/20 alternative |            ✓   |                 Reads|Reads | 
|Freeze portfolios   |             ✓   |                 Reads|Reads | 
| Portfolio risk analysis |  — | ✓|  — | 
| Portfolio performance analysis |  — | ✓ | ✓ | 
|Final OOS test      |             ✓  |                  Uses|— | 
|Transaction-cost sensitivity |    ✓  |                  —|— | 
|Active return   |                 —   |                 ✓|— | 
|Active weights   |                —   |                 ✓|— | 
|Tracking error    |               —   |                 ✓|— | 
|Information ratio   |             —  |                  ✓|— | 
|Risk contribution    |            —   |                 ✓|— | 
|Performance attribution |         —   |                 ✓|— | 

| VaR / Expected Shortfall |  — | ✓|  —| 
| Trading signals |  — |  — | ✓| 
| SMA strategy |  — |  — | ✓| 
| RSI strategy |  — |  — | ✓| 
| Trading parameter optimization |  — |  — | ✓| 
| Look-ahead-bias control |  — |  — | ✓| 
| Expanding walk-forward |  — |  — | ✓| 
| Rolling walk-forward |  — |  — | ✓| 
| Trading parameter stability |  — |  — | ✓| 
| Trading parameter sensitivity |  — |  — | ✓| 
| Regime robustness |  — |  — | ✓| 
| Active trading exposure |  — |  — | ✓| 
| Final trading OOS test |  — |  — | ✓ |

---
 
### Project Outputs

# Project 01
Key outputs include:
-Selected asset universe
- Factor snapshots
- Factor rankings
- Hyperparameter results
- Portfolio specifications
- Optimized portfolio weights
- Out-of-sample portfolio results
- Covariance and correlation analysis

# Project 02
Key outputs include:
- performance_comparison.csv
- active_weights.csv
- performance_attribution.csv
- risk_contribution.csv
- portfolio_returns.csv
- daily_active_contribution.csv
- oos_covariance_matrix.csv
- risk_performance_summary.csv

# Project 03
Key outputs include:
- inherited_frozen_portfolio.csv
- asset_trading_signals.csv
- asset_strategy_returns.csv
- portfolio_daily_returns.csv
- expanding_walk_forward_results.csv
- expanding_parameter_history.csv
- expanding_robustness.csv
- rolling_walk_forward_results.csv
- rolling_parameter_history.csv
- rolling_robustness.csv
- parameter_sensitivity.csv
- regime_robustness.csv
- signal_statistics.csv

Visual outputs include:
- Final OOS Equity Curve
- SMA Parameter Sensitivity Heatmap

# Technology Stack
The projects are implemented primarily using:
- Python
- pandas
- NumPy
- SciPy
- Matplotlib

Key quantitative techniques include:
- Data manipulation
- Time-series analysis
- Statistical calculations
- Factor modelling
- Cross-sectional ranking
- Covariance and correlation analysis
- Portfolio mathematics
- Constrained numerical optimization
- Technical indicators
- Backtesting
- Walk-forward validation
- Parameter sensitivity analysis
- Regime analysis
- Risk-adjusted performance analysis
- Benchmark-relative analysis
- Risk attribution

## Overall Research Methodology
The complete research process follows:

1. Define Investment Universe
             ↓
2. Prepare Market Data
             ↓
3. Construct Quantitative Factors
             ↓
4. Rank Assets
             ↓
5. Select Investment Universe
             ↓
6. Construct Candidate Portfolios
             ↓
7. Optimize Portfolio Allocations
             ↓
8. Validate Portfolio Construction
             ↓
9. Freeze Portfolio Specification
             ↓
10. Analyse Portfolio Risk & Performance
             ↓
11. Develop Trading Overlay
             ↓
12. Optimise Trading Parameters
             ↓
13. Expanding Walk-Forward Validation
             ↓
14. Rolling Walk-Forward Validation
             ↓
15. Parameter Sensitivity
             ↓
16. Regime Robustness
             ↓
17. Final Unseen OOS Trading Test

This creates a complete quantitative investment research workflow from asset selection through portfolio construction, risk analysis, and tactical trading.

---
## Overall Research Interpretation
An important principle demonstrated by this portfolio is that model complexity does not automatically translate into superior investment performance.

Project 01 demonstrates that quantitative factor selection and constrained optimization can provide a systematic and mathematically disciplined approach to portfolio construction.

Project 02 demonstrates that the resulting portfolio must then be evaluated independently through risk, performance, attribution, and benchmark-relative analysis.

Project 03 extends the research by asking whether a systematic trading overlay can dynamically manage short-term exposure to the same frozen portfolio.

The empirical results do not support the claim that optimization or trading automatically produces superior absolute returns.

Instead, the projects demonstrate several broader quantitative research principles:
Simple benchmarks are essential.

Out-of-sample performance matters more than in-sample optimization results.

Portfolio weights and portfolio risk contributions are not the same thing.

More frequent parameter optimization does not necessarily improve generalization.

Trading strategies should be evaluated on both return and risk.

A strategy that reduces drawdown may have a different investment role from a strategy designed primarily to maximize returns.

Asset selection, portfolio construction, risk analysis, and trading should be separated when building a quantitative research system.

## Overall Portfolio Conclusion
The three projects form an integrated quantitative investment research portfolio:

PROJECT 01
Asset Selection & Portfolio Construction
             ↓
       Frozen Portfolio
             ↓
PROJECT 02
Risk & Performance Analytics
             ↓
PROJECT 03
Systematic Short-Term Trading Overlay

The research demonstrates the progression from:

Market Data
    ↓
Quantitative Factors
    ↓
Asset Selection
    ↓
Portfolio Construction
    ↓
Portfolio Risk Analysis
    ↓
Trading Signal Development
    ↓
Walk-Forward Validation
    ↓
Final Unseen OOS Evaluation

The most important conclusion is that quantitative finance research should not be judged simply by whether a model produces a high historical return.

A stronger research process asks:

**Was the investment universe selected systematically?**

**Were portfolio weights constructed using a transparent methodology?**

**Was the model compared with a simple benchmark?**

**Was risk analysed independently from return?**

**Were parameters validated rather than assumed?**

**Was look-ahead bias controlled?**

**Was walk-forward validation performed?**

**Was parameter sensitivity examined?**

**Was regime behaviour investigated?**

**Was the final evaluation performed on genuinely unseen data?**

This portfolio is designed around those principles.

The results demonstrate both successful implementation and important negative findings.

In particular:
Project 01 shows that quantitative asset selection and constrained optimization do not guarantee superior out-of-sample performance.

Project 02 demonstrates that portfolio performance must be evaluated together with risk, attribution, and benchmark-relative behaviour.

Project 03 shows that a systematic trading overlay can potentially reduce short-term portfolio exposure and downside risk without changing the strategic portfolio construction.

The overall research therefore does not claim that the models are universally superior investment strategies.

Instead, it demonstrates a disciplined quantitative research process in which models are developed systematically, validated chronologically, challenged against simple benchmarks, and evaluated on genuinely unseen data.



## Author

McDonald Chiringwaringwa

BSc Honours Applied Mathematics  
MSc Financial Engineering  
Actuarial Professional Examinations: CT1, CT3, CT4, CT8

---

## Disclaimer

These projects are for research, educational, and portfolio demonstration purposes only. 
They do not constitute investment advice or a recommendation to buy or sell any security.
