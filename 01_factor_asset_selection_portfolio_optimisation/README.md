# Factor-Based Asset Selection & Robust Portfolio Optimisation

## Objective

Develop a systematic quantitative investment framework that combines:

- Multi-factor asset selection
- Rolling factor estimation
- Hyperparameter optimisation
- Parameter stability analysis
- Covariance and correlation analysis
- Constrained portfolio optimisation
- Benchmark portfolio construction
- Alternative portfolio construction
- Chronological out-of-sample testing
- Transaction-cost sensitivity
- Benchmark-relative performance analysis
- Portfolio risk decomposition

The objective is not simply to find the portfolio with the highest historical
return.

Instead, the project investigates whether a systematic factor-based selection
process can produce a diversified portfolio and whether constrained portfolio
optimisation can provide a useful alternative to a simple equal-weight
allocation.

Particular emphasis is placed on maintaining a strict separation between model
development and the genuinely unseen final test period.

---

## Investment Universe

The initial investment universe consists of five large-cap US equities:

- AAPL — Apple
- MSFT — Microsoft
- NVDA — NVIDIA
- GOOG — Alphabet
- META — Meta Platforms

The S&P 500 (`^GSPC`) is used as the market benchmark for rolling beta
estimation.

### Data 

Historical market data is stored locally as CSV files and loaded into Python
using pandas.

Expected input files include:

```text
data/
├── AAPL.csv
├── MSFT.csv
├── NVDA.csv
├── GOOG.csv
├── META.csv
└── ^GSPC.csv

The raw files are:
- loaded from CSV,
- converted to datetime format,
- converted to numeric price data,
- aligned to a common trading-date intersection,
- sorted chronologically,
- checked for missing observations.

A reusable processed dataset is then saved as:
      data/processed_prices.csv

This allows subsequent projects to work from the same cleaned and aligned dataset rather than repeatedly preparing the raw data.

## Development and Final Test Framework

The complete dataset is divided chronologically into:
- 80% Development
- 20% Final Unseen Test

No random shuffling is performed.

The development dataset is used for:
- factor estimation,
- asset selection,
- hyperparameter optimisation,
- covariance estimation,
- correlation analysis,
- portfolio construction.

The final test dataset remains untouched until the portfolio specifications have been frozen.
This provides a genuine out-of-sample evaluation.

## Inner Development Validation
The development dataset is further divided chronologically into:
- 80% Optimisation Train
- 20% Validation

The optimisation-train period is used to calculate factor snapshots and test different factor lookback parameters.

The validation period is used to compare the resulting asset-selection portfolios.

The final 20% test period is not used during this process.

Therefore the information flow is:

Full Historical Data
        │
        ├── 80% Development
        │      │
        │      ├── 80% Optimisation Train
        │      │
        │      └── 20% Validation
        │
        └── 20% Final Unseen Test

## Factor Model
Four quantitative factors are calculated for each candidate asset.
1. Rolling Beta
Beta measures the sensitivity of an asset's return to movements in the S&P 500.
      β_i = Cov(R_i,R_m )/Var(R_m ) 
Rolling windows of 40, 60 and 80 trading days are tested.
Lower beta receives a higher factor score.

2. Rolling Momentum
Momentum measures historical price appreciation over a specified lookback period.
      Momentum_t = {P_t/P_(t-k)} -1
Higher momentum receives a higher score.
Rolling windows of 40, 60 and 80 trading days are tested.

3. Rolling Volatility
Rolling volatility is calculated from daily returns and annualised using 252 trading days.
      σ_annual=σ_daily √252
Rolling windows of 10, 20 and 30 trading days are tested.
Lower volatility receives a higher factor score.

4. Rolling Sharpe Ratio
Rolling risk-adjusted performance is measured using:
      Sharpe = {μ/σ} √252
Rolling windows of 40, 60 and 80 trading days are tested.
Higher Sharpe receives a higher factor score.

## Factor Ranking
Each factor is converted into a cross-sectional percentile score.

The four factors receive equal weights:
      AssetScore = 0.25(BetaScore) + 0.25(MomentumScore) + 0.25(VolatilityScore) + 0.25(Sharpe)
The three highest-scoring assets are selected.

This produces a systematic asset-selection mechanism rather than manually choosing stocks.

## Hyperparameter Optimisation
Four factor lookback parameters are tested.

| Factor    | Candidate Windows |
|-----------|-------------------|
| Beta      | 40, 60, 80 days   |
| Momentum  | 40, 60, 80 days   |
| Volatility| 10, 20, 30 days   |
| Sharpe    | 40, 60, 80 days   |

The total number of combinations is:
      3 × 3 × 3 × 3 = 81

Each parameter combination:
- calculates the factor snapshot using optimisation-train data,
- ranks the candidate assets,
- selects the top three assets,
- constructs an equal-weight portfolio,
- evaluates that portfolio on the validation period.

The parameter combination producing the highest validation Sharpe is identified, but parameter stability is also examined rather than relying exclusively on one maximum value.

## Parameter Robustness
Parameter robustness is investigated through:
- Validation Sharpe distribution
- Minimum and maximum validation Sharpe
- Standard deviation of validation Sharpe
- Frequency of selected asset combinations
- Frequency of factor-window values among top-performing configurations
- Distance from the baseline parameter specification

The baseline specification is:
Beta       = 60 days
Momentum   = 60 days
Volatility = 20 days
Sharpe     = 60 days

A representative robust configuration is selected based on its proximity to the baseline while remaining among the leading validation solutions.

This provides a more stable research approach than simply selecting the single configuration with the highest historical validation result.

## Selected Asset Portfolio
The factor-selection process identifies:
- AAPL
- GOOG
- META
as the three selected assets for subsequent portfolio construction.

These three assets form the investment set used for the portfolio-weight analysis.

## Covariance and Correlation Analysis
The development data is used to estimate:
- annualised covariance,
- pairwise correlation,
- individual asset volatility,
- portfolio volatility,
- diversification effects.

Portfolio variance is:
      (σ_p)^2=ω^T ∑ω
and portfolio volatility is:
      σ_p=√(ω^T ∑ω)
This is important because portfolio construction depends not only on the expected characteristics of individual assets but also on their interactions.

## Benchmark Portfolio
The equal-weight portfolio is used as the primary benchmark for the portfolio construction analysis.

For the three selected assets:
      ω_B = (1⁄3,1⁄3,1⁄3)

Therefore:
| Asset | Benchmark Weight |
|-------|------------------|
| AAPL  | 33.33%  |
| GOOG  | 33.33%  |
| META  | 33.33%  |

The equal-weight portfolio provides a transparent and non-optimised benchmark against which the constrained optimisation alternatives can be evaluated.

## Constrained Maximum-Sharpe Optimisation
After selecting AAPL, GOOG and META, portfolio weights are optimised using {scipy.optimize.minimize}.

The optimisation maximises the estimated Sharpe ratio:
      max┬ω⁡〖(ω^T μ - r_f)/√(ω^T ∑ω)〗
subject to:
      ∑_i(ω_i) = 1
and:
      0 ≤ ω_i ≤ ω_max

Several maximum-weight constraints are tested:
- 33.33%
- 40%
- 50%
- 75%
- unconstrained 

The purpose of these constraints is to investigate how portfolio concentration affects the risk-return profile.

## Equal Weight vs Constrained Optimisation
The project deliberately compares two different portfolio-construction approaches.

# Benchmark
The benchmark is the simple equal-weight allocation:
AAPL = 33.33%
GOOG = 33.33%
META = 33.33%

This allocation requires no optimisation and provides a transparent reference point.

# Alternative Model
The constrained optimisation framework produces portfolios subject to maximum position limits.

The 40% maximum-weight constraint produced the following allocation:
AAPL = 40%
GOOG = 40%
META = 20%
This became the preferred constrained alternative because it provides a moderate optimisation solution without allowing the portfolio to become excessively concentrated.

The 40/40/20 portfolio should therefore be interpreted as an alternative model, not as the benchmark.

## Frozen Portfolio Candidates
Before examining the final unseen test period, the portfolio specifications are frozen.

The candidates include:

|Portfolio |     Description |
|---------|------------------|
|Equal Weight | 33.33% / 33.33% / 33.33% benchmark |
|Max 40 | Constrained alternative |
|Max 50 | More concentrated constrained alternative |
|Max 75  | Highly concentrated alternative |
|Unconstrained | No maximum position constraint |

The exact optimised weights are generated from the development covariance and expected-return estimates.
No final-test information is used to modify these weights.

The model keeps want to give more weight to GOOG at the expense of META, the out was as follows

| Portfolio    | AAPL | GOOG | META |
|--------------|---:|---:|---:|
| Equal Weight | 33.33% | 33.33% | 33.33% |
| Max 40       | 40% | 40% | 20% |
| Max 50       | 50% | 50% | 0% |
| Max 75       | 25% | 75% | 0% |
| Unconstrained| 20.42% | 79.58% | 0% |


## Final Unseen Out-of-Sample Test
After the portfolio candidates are frozen, they are evaluated on the final 20% of the historical dataset.

The final test is therefore used only for performance evaluation.

The following metrics are calculated:
- Total Return
- Annualised Return
- Annualised Volatility
- Sharpe Ratio
- Maximum Drawdown
- Final Wealth

## Key Research Result
The equal-weight portfolio performed better than the constrained alternatives on the final unseen test period.

The important distinction is therefore:
Equal Weight
    │
    └── Best benchmark performance OOS

40/40/20 Constrained Portfolio
    │
    └── Preferred alternative model
        with lower concentration / risk characteristics
        but weaker OOS performance than equal weight

The result does not imply that optimisation was unsuccessful.
Instead, it demonstrates an important quantitative-finance finding:
A more sophisticated optimisation process does not automatically produce superior out-of-sample performance.

The equal-weight portfolio provided the stronger final-test result, while the 40/40/20 constrained portfolio provided a more controlled alternative to the more concentrated optimisation solutions.

This distinction between performance maximisation and risk-controlled portfolio construction is an important part of the research conclusion.

## Transaction-Cost Sensitivity
The project includes transaction-cost sensitivity analysis using:
- 0 bps
- 10 bps
- 25 bps
- 50 bps

The analysis examines how transaction costs affect:
- net returns,
- volatility,
- Sharpe ratio,
- maximum drawdown,
- portfolio turnover.

Transaction-cost analysis provides an additional implementation check rather than relying solely on gross historical performance.


# Research Process
The complete research process can be summarised as:

Raw CSV Data
      │
      ▼
Data Cleaning & Alignment
      │
      ▼
80% Development / 20% Final Test
      │
      ▼
Development Data
      │
      ├── Factor Construction
      ├── Hyperparameter Optimisation
      ├── Asset Selection
      ├── Covariance Analysis
      └── Portfolio Construction
      │
      ▼
Equal-Weight Benchmark
          +
Constrained Optimisation Alternatives
      │
      ▼
Freeze Portfolio Specifications
      │
      ▼
Final Unseen Test
      │
      ▼
Transaction-Cost Sensitivity

## Key Research Lessons
The project demonstrates several important quantitative-investment principles:

- Asset selection and portfolio weighting are separate decisions.
- Historical optimisation does not guarantee superior out-of-sample performance.
- Equal-weight portfolios provide useful transparent benchmarks.
- Position constraints can reduce concentration.
- Risk and return must be evaluated jointly.
- Parameter stability is important when building systematic models.
- Chronological out-of-sample testing is essential.
- Transaction costs should be considered when assessing implementability.
- A simpler model can outperform a more complex optimised model out of sample.

## Technologies
The project is implemented using:
- Python
- NumPy
- pandas
- SciPy

Primary techniques include:
- Time-series analysis
- Cross-sectional ranking
- Portfolio mathematics
- Covariance analysis
- Constrained numerical optimisation
- Risk measurement
- Out-of-sample validation

## Disclaimer
This project is for quantitative research, educational, and portfolio demonstration purposes only.
It does not constitute investment advice or a recommendation to buy or sell any security.

---
