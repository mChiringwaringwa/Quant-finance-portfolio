## PROJECT 01 — MULTI-FACTOR ASSET SELECTION & CONSTRAINED, ROBUST PORTFOLIO OPTIMIZATION

# Quantitative Investment Research Project

A systematic quantitative investment framework for selecting equities using multiple risk-adjusted factors, testing parameter robustness, analysing portfolio diversification, and constructing constrained portfolios for subsequent out-of-sample evaluation.

# 1. Project Objective
The objective of Project 01 is to develop a reproducible quantitative framework that answers four questions:

- Which assets are attractive according to multiple quantitative factors?
- Is the asset-selection result robust to reasonable changes in factor lookback windows?
- How should capital be allocated across the selected assets subject to portfolio constraints?
- Does the resulting portfolio specification remain effective on completely unseen data?

The project deliberately separates:

Asset selection → robustness testing → portfolio construction → frozen OOS evaluation

This prevents information from the final test period from influencing the investment specification.

# 2. Investment Universe
The candidate equity universe consists of five large-cap U.S. technology/growth stocks:

Ticker               Asset
AAPL                 Apple
MSFT                 Microsoft
NVDA                 NVIDIA
GOOG                 Alphabet
META                 Meta Platforms

The S&P 500 index (^GSPC) is used as the market benchmark for estimating equity beta.

# 3. Data
Daily market-price data were cleaned and aligned across all assets.

Full sample
Start: 28 July 2025
End: 14 July 2026
Observations: 242 trading observations

Assets:
AAPL
MSFT
NVDA
GOOG
META
^GSPC

Processed prices are saved as:
outputs/processed_prices.csv

# 4. Chronological Data Architecture
The project uses a strict chronological data structure.

FULL DATASET
│
├── DEVELOPMENT SAMPLE
│   │
│   ├── Optimization Train
│   │
│   └── Validation
│
└── FINAL UNSEEN TEST

Outer development / final test split
Dataset                 Period                            Observations
Development            2025-07-28 → 2026-05-01            193
Final unseen test      2026-05-04 → 2026-07-14            49

Chronology check: PASSED

The final 49 observations are never used for factor selection, hyperparameter selection, or portfolio optimization.

# 5. Factor Model

Four quantitative factors are used for asset selection:

# 1. Beta
Measures systematic market exposure:
B_i = Cov(R_i, R_m) / Var(R_m)
where:
R_i = asset return
R_m = S&P 500 return

Lower beta receives a higher factor score in this project because the selection framework favours lower systematic risk, all else equal.

# 2. Momentum
Momentum measures the cumulative return over a specified historical window:
Momentum_i = (P_i / P_t-k ) - 1

Higher momentum receives a higher score.

# 3. Volatility
Annualised historical volatility is calculated from daily returns:
Sigma_i = Std(R_i) * sqrt(252)

Lower volatility receives a higher score.

# 4. Sharpe Ratio
The historical risk-adjusted return is measured using:
Sharpe_i = (R_i /Sigma_i) * sqrt(252)

Higher Sharpe receives a higher score.


# 6. Baseline Reference Specification
The baseline is not the final selected model.

It is the fixed reference specification against which robustness is measured.
baseline_parameters = {
    "Beta_Window": 60,
    "Momentum_Window": 60,
    "Volatility_Window": 20,
    "Sharpe_Window": 60
}

Therefore:
      Baseline = (60, 60, 20, 60)
The baseline exists to provide a stable economic reference point and prevent the research process from becoming completely driven by parameter optimization.

# 7. Equal Factor Weighting
A key correction to the original implementation is that Beta is now included directly in the asset-selection score.

All four factors receive equal weight:
            w_beta = w_momentum = w_volatility = w_sharpe = 0.25

The composite asset score is therefore: 
AssetScore_i = 0.25B_Score_i + 0.25M_Score_i + 0.25V_Score_i + 0.25S_Score_i

This avoids assigning subjective importance to one factor over another.
The highest-scoring three assets form the selected asset universe for each parameter configuration.

# 8. Baseline Factor Results
Using the baseline specification:

Beta Window       = 60
Momentum Window   = 60
Volatility Window = 20
Sharpe Window     = 60

the development factor snapshot was:

|Asset |    Beta   |  Momentum  | Volatility |  Sharpe  |
|------|-----------|------------|------------|----------|
|AAPL  |    0.9620 |   0.0132   |   0.2394   |   0.3421 |
|MSFT  |   1.0333  |    0.0006  |   0.3267   |   0.1562 |
|NVDA  |   1.6961  |    0.1393  |   0.3833   |   1.6150 |
|GOOG  |   1.3597  |    0.1496  |   0.4140   |   1.8874 |
|META  |   1.7109  |   -0.0900  |    0.5184  |  -0.7699 |

The baseline ranking is:
AAPL
GOOG
NVDA
MSFT
META

The baseline specification therefore provides the reference ranking, but it is deliberately not hard-coded as the final portfolio universe.

# 9. Hyperparameter Robustness
To determine whether the asset selection depends excessively on one particular lookback specification, the four factor windows are varied systematically.

The parameter grid contains:
      4 X 4 X 3 X 4 = 192

or, for the final implemented research grid:

      81 configurations

Each configuration independently:

- calculates the four factors;
- scores all five candidate assets;
- selects the top three;
- evaluates the resulting selected portfolio on the validation sample.

The final implementation records:

- factor windows;
- selected assets;
- validation return;
- validation volatility;
- validation Sharpe;
- parameter distance from the baseline.

# 10. Robustness Result — Key Research Finding
The most important finding from the parameter-robustness analysis is that:

      (AAPL, GOOG, META)

was selected in:
      77/ 81 = 95.06%
of all parameter configurations.

The remaining configurations selected:
(GOOG, META, NVDA) = 2/81 = 2.47%

(GOOG, META, MSFT) = 2/81 = 2.47%

# Selection frequency      

|Selected Assets     |   Frequency |  Percentage |
|--------------------|-------------|-------------|
|AAPL + GOOG + META  |       77    |      95.06% |
|GOOG + META + NVDA  |       2     |       2.47% |
|GOOG + META + MSFT  |       2     |       2.47% |

This is important because it demonstrates that:

AAPL + GOOG + META is not the product of one lucky parameter combination.

The same three assets emerge under the overwhelming majority of reasonable factor-window specifications.

This provides substantially stronger evidence for the asset-selection result than simply reporting the single best-performing parameter combination.

# 11. Validation Sharpe Robustness
An additional finding was that many parameter configurations produced the same validation performance:
      
      Validation Sharpe = 2.206081

Because several configurations tied at the best validation Sharpe, selecting the configuration with the largest Sharpe alone would introduce an unnecessary arbitrary choice.

Instead, the project uses a second criterion:

Choose the tied best-performing configuration that is closest to the pre-specified baseline.

# 12. Parameter Distance from Baseline
The baseline is:
      (60, 60, 20, 60)

For each tied configuration, parameter distance is calculated relative to this reference.
For example:

Baseline:
      (60, 60, 20, 60)

Representative:
      (60, 60, 10, 60)

The only difference is the volatility lookback:
      20 → 10

Therefore the representative configuration is very close to the original research specification.

# Selected representative robust specification
      (60, 60, 10, 60)
      
corresponding to:
Beta Window       = 60
Momentum Window   = 60
Volatility Window = 10
Sharpe Window     = 60

This configuration produces the same best validation Sharpe: 2.206081

while remaining close to the baseline.

# 13. Why the Representative Configuration Matters
The selection procedure is therefore:

1. Define baseline before optimization
             ↓
2. Test parameter grid
             ↓
3. Identify all configurations achieving
   the maximum validation Sharpe
             ↓
4. Examine selected asset combinations
             ↓
5. Establish selection-frequency robustness
             ↓
6. Among tied best configurations,
   choose the one closest to baseline
             ↓
7. Freeze the resulting specification

This is preferable to simply choosing:
      
      argmax(validation_sharpe)

because the latter could select an arbitrary parameter combination when many configurations perform identically.
The approach favours parsimony and stability rather than optimization extremism.

# 14. Final Selected Asset Universe
The robustness analysis establishes:
      AAPL, GOOG, META

as the robust selected universe.

The selection is supported by:

- high selection frequency;
- identical best validation Sharpe across multiple configurations;
- proximity of the representative specification to the baseline;
- absence of reliance on the final unseen test period.
  
This is a much stronger research justification than simply saying:

"These three stocks had the highest score."

# 15. Covariance and Correlation Analysis
After asset selection, the covariance matrix is estimated using the development sample.

The purpose is to understand how the selected assets interact with one another before portfolio optimization.

The selected-asset correlation structure was approximately:

|        |  AAPL   |   GOOG   |   NVDA  |
|--------|---------|----------|---------|         
|AAPL    |  1.000  |   0.340  |   0.230 |
|GOOG    |  0.340  |   1.000  |   0.256 |
|NVDA    |  0.230  |   0.256  |   1.000 |

For the corrected final selected universe, the same procedure is applied to:
AAPL
GOOG
META

The covariance matrix is then used directly by the portfolio optimizer.

# 16. Portfolio Optimization
Once the asset universe is frozen, portfolio weights are determined using constrained mean-variance optimization.

Portfolio expected return:
      E(R_p) = w^T * mule

Portfolio variance:
       (σ_p)^2=ω^T ∑ω

and portfolio volatility is:
      σ_p=√(ω^T ∑ω)

Portfolio Sharpe ratio:
      Sharpe_p = E(R_p) / Sigma_p

subject to:
       ∑_i(ω_i) = 1
and:
      0 ≤ ω_i ≤ ω_max
      
No short selling is permitted.

# 17. Portfolio Constraints
Several maximum-position constraints are examined:
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

This is important because portfolio construction depends not only on the expected characteristics of individual assets but also on their interactions.

The equal-weight portfolio is retained as the benchmark:
w_i = 1/3

for the three selected assets.

This allows the project to distinguish between:

- asset-selection skill;
- diversification;
- portfolio-weight optimization.
  
# 18. Equal-Weight Benchmark
The equal-weight portfolio provides a transparent benchmark against which optimized allocations can be compared.
For three assets:

AAPL    33.33%
GOOG    33.33%
META    33.33%

The benchmark is intentionally simple.

It answers:

"Does optimization add value beyond simply holding the selected assets equally?"

# 19. Frozen Portfolio Specifications
After development and validation, portfolio specifications are frozen.

No final-test information is used to alter:

- selected assets;
- factor windows;
- optimization methodology;
- portfolio constraints.

The resulting portfolios are then evaluated on the previously untouched final OOS period.

# 20. Final Out-of-Sample Test
The final test period is:
      2026-05-04 → 2026-07-14

with:
      49 observations

This period is completely unseen during:

- factor development;
- parameter selection;
- robustness analysis;
- validation;
- portfolio construction.

The final test therefore represents the most important test of whether the research specification generalises beyond the development sample.

# 21. Transaction-Cost Sensitivity
The project also evaluates portfolio performance under different transaction-cost assumptions.

The purpose is to determine whether the investment conclusion depends on unrealistic frictionless trading assumptions.

The analysis compares portfolio outcomes under increasing transaction-cost assumptions.

This provides an additional robustness layer:
      Gross Return →      Trading Costs →      Net Return
      
A strategy that disappears after modest transaction costs would not be considered economically robust.

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

The equal-weight benchmark remained relatively robust under different
transaction-cost assumptions:

| Transaction Cost | Total Return | Sharpe |
|------------------|--------------|--------|
| 0 bps            | 5.67%        | 1.2905 |
| 10 bps           | 5.64%        | 1.2846 |
| 25 bps           | 5.59%        | 1.2758 |
| 50 bps           | 5.52%        | 1.2610 |

Transaction costs reduced performance gradually but did not materially
alter the overall conclusion.

# 22. Bias Controls
The project explicitly addresses several common sources of quantitative research bias.

# Look-Ahead Bias
The final test period is not used when determining the investment specification.

# Overfitting
Parameter robustness is tested across a grid rather than relying exclusively on one optimal configuration.

# Selection Bias
The final asset universe is supported by selection-frequency analysis.

# Data Leakage
The final test set remains isolated until the specification is frozen.

# Parameter Instability
Multiple lookback combinations are evaluated to determine whether asset selection changes materially.

# Survivorship Consideration
The project acknowledges that the candidate universe consists of pre-defined currently available large-cap stocks rather than a historically reconstructed survivorship-free universe. This remains a limitation of the study.

# 23. Research Workflow
The complete Project 01 pipeline is:

Raw Market Data
       ↓
Data Cleaning & Alignment
       ↓
Chronological Development/Test Split
       ↓
Define Baseline Specification
       ↓
Calculate Beta
       ↓
Calculate Momentum
       ↓
Calculate Volatility
       ↓
Calculate Sharpe
       ↓
Equal 25% Factor Weighting
       ↓
Baseline Asset Ranking
       ↓
Hyperparameter Grid
       ↓
Validation Testing
       ↓
Parameter Robustness
       ↓
Selection Frequency Analysis
       ↓
Best-Sharpe Tie Analysis
       ↓
Distance-to-Baseline Selection
       ↓
Freeze Robust Asset Universe
       ↓
Covariance / Correlation Analysis
       ↓
Constrained Portfolio Optimization
       ↓
Freeze Portfolio Specifications
       ↓
Transaction-Cost Sensitivity
       ↓
Final Unseen OOS Test

# 24. Key Research Results

The most important findings from Project 01 are:

# Baseline
Beta       = 60 days
Momentum   = 60 days
Volatility = 20 days
Sharpe     = 60 days

# Factor weighting
Beta       = 25%
Momentum   = 25%
Volatility = 25%
Sharpe     = 25%

# Robust asset selection
AAPL + GOOG + META

selected in:
      77 /81 = 95.06%
      
of tested configurations.

# Best validation Sharpe
      2.206081
      
# Representative robust specification

Beta       = 60
Momentum   = 60
Volatility = 10
Sharpe     = 60

This is selected because it is one of the tied best-performing configurations while being closest to the pre-defined baseline.

# 25. What Project 01 Demonstrates
Project 01 demonstrates practical quantitative research skills in:

- Financial data cleaning
- Return calculation
- Factor construction
- CAPM beta estimation
- Momentum measurement
- Volatility estimation
- Sharpe-ratio analysis
- Cross-sectional factor ranking
- Multi-factor asset selection
- Hyperparameter testing
- Robustness analysis
- Selection-frequency analysis
- Parameter stability
- Covariance estimation
- Correlation analysis
- Mean-variance portfolio optimization
- Portfolio constraints
- Benchmark construction
- Transaction-cost sensitivity
- Out-of-sample testing
- Chronological validation
- Prevention of look-ahead bias
- Quantitative research documentation

# 26. Limitations
The project has several limitations.

# Short sample
The available dataset covers approximately one year, limiting statistical confidence.

# Small investment universe
Only five candidate equities are considered.

# Survivorship Bias
The universe is not reconstructed historically from all securities that would have been investable at each point in time.

# Simplified Transaction Costs
Transaction costs are represented through sensitivity assumptions rather than a full market-impact model.

# Historical Factor Relationships
The factor relationships observed during the development period may not persist in future market regimes.

# Parameter Grid
The robustness analysis covers a defined set of lookback windows rather than every theoretically possible parameter.

These limitations are important because a strong quantitative project should identify where its conclusions may fail rather than presenting historical results as guaranteed future performance.

# 27. Research Conclusion
The central conclusion of Project 01 is not simply that one particular portfolio produced the highest historical Sharpe ratio.

The stronger conclusion is that the asset-selection process exhibits substantial parameter robustness.

Across 81 tested factor-window configurations:
      95.06%

selected:
      AAPL + GOOG + META
      
This indicates that the selected universe is not primarily driven by a single finely tuned parameter combination.

Furthermore, multiple configurations achieved the same best validation Sharpe of approximately:
      2.2061

Rather than arbitrarily selecting one of them, the research chooses the configuration closest to the pre-defined baseline:
      (60, 60, 10, 60)
      
This provides a disciplined compromise between:

performance, robustness and model simplicity.

The selected asset universe is then frozen before portfolio optimization and final out-of-sample testing.

# 28. Project 01 vs Project 02
Project 01 deliberately ends after establishing:

Asset Selection
        +
Portfolio Construction
        +
OOS Portfolio Evaluation

Benchmark-relative analysis and detailed performance attribution are reserved for Project 02.

Project 02 therefore builds on the frozen portfolio specifications produced here and investigates:

- benchmark-relative return;
- active return;
- tracking error;
- information ratio;
- attribution;
- portfolio contribution;
- factor contribution;
- risk decomposition.

This separation prevents Project 01 from becoming an unnecessarily broad project and creates a clear progression between the two quantitative research projects.

# 29. Repository Structure
Recommended GitHub structure:

project-01-multifactor-portfolio/
│
├── README.md
│
├── project_01.py
│
├── data/
│   ├── AAPL.csv
│   ├── MSFT.csv
│   ├── NVDA.csv
│   ├── GOOG.csv
│   ├── META.csv
│   └── ^GSPC.csv
│
├── outputs/
│   ├── processed_prices.csv
│   ├── final_test_returns.csv
│   ├── factor_snapshot.csv
│   ├── robustness_results.csv
│   ├── covariance_matrix.csv
│   └── portfolio_results.csv
│
└── images/
    ├── factor_ranking.png
    ├── selection_frequency.png
    ├── correlation_matrix.png
    └── portfolio_comparison.png
    
Important: In a public GitHub repository, raw market data should only be included if its redistribution is permitted. Otherwise, provide a data-download/preparation script and document the required input format.

# 30. Proffessional Summary
A concise explanation of Project 01 would be:

"I developed a multi-factor equity-selection and portfolio-optimization framework in Python. I used beta, momentum, volatility and Sharpe ratio as equally weighted selection factors. Rather than selecting assets solely from one optimized parameter set, I tested 81 combinations of factor lookback windows. AAPL, GOOG and META were selected in 77 of the 81 configurations, or 95.06%, demonstrating that the asset selection was robust rather than dependent on a single parameter choice. Several configurations achieved the same validation Sharpe, so I selected the tied configuration closest to my pre-specified baseline of 60, 60, 20 and 60 days, resulting in 60, 60, 10 and 60. I then froze the selected universe, estimated its covariance structure, performed constrained portfolio optimization and evaluated the frozen portfolios on an unseen out-of-sample period."

## Technologies
The project is implemented using:
- Python
- NumPy
- pandas
- SciPy

# Primary techniques include:
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
