# Project 02 — Portfolio Risk & Performance Analytics

## Objective
This project evaluates a constrained equity portfolio against an
equal-weight benchmark using portfolio performance, risk decomposition,
active return analysis, tracking error, information ratio, and
performance attribution.

The analysis investigates whether imposing a maximum 40% allocation
constraint provides a more risk-controlled portfolio relative to an
equal-weight benchmark.

---

## Portfolio
The final portfolio consists of:

| Asset | Portfolio Weight | Benchmark Weight |
|-------|------------------|------------------|
| AAPL  | 40%              | 33.33%           |
| GOOG  | 40%              | 33.33%           |
| META  | 20%              | 33.33%           |

The benchmark is an equal-weight portfolio:

- AAPL: 33.33%
- GOOG: 33.33%
- META: 33.33%

---

## Data

- Assets: AAPL, MSFT, NVDA, GOOG, META
- Final portfolio universe: AAPL, GOOG, META
- Data source: Yahoo Finance
- Frequency: Daily
- Period: 16 July 2025 – 15 July 2026
- Adjusted closing prices used for return calculations

---

## Methodology
The analysis includes:

1. Daily return calculation
2. Portfolio return calculation
3. Equal-weight benchmark construction
4. Volatility estimation
5. Sharpe ratio
6. Maximum drawdown
7. Covariance and correlation analysis
8. Portfolio risk contribution
9. Active return analysis
10. Active weight decomposition
11. Tracking error
12. Information ratio
13. Performance attribution
14. Transaction-cost sensitivity

---

## Active Portfolio Analysis
Relative to the equal-weight benchmark, the maximum 40% portfolio
held:

| Asset | Active Weight |
|-------|---------------|
| AAPL  | +6.67%        |
| GOOG  | +6.67%        |
| META  | -13.33%       |

The portfolio therefore represented an overweight to AAPL and GOOG
and an underweight to META.

---

## Out-of-Sample Performance
The final out-of-sample results were:

| Metric                    | Portfolio | Benchmark |
|---------------------------|-----------|-----------|
| Total Return              | 4.98%     |   5.67%   |
| Active Return             | -0.68%    |    —      |
| Information Ratio         | -0.73     |    —      |
| Annualized Tracking Error | 5.38%     |    —      |

The constrained portfolio underperformed the equal-weight benchmark
during the final test period.

---

## Risk Decomposition

Portfolio daily volatility was approximately:

1.31%

Risk contribution was:

| Asset | Risk Contribution |
|-------|-------------------|
| AAPL  | 33.18% |
| GOOG  | 46.02% |
| META  | 20.80% |

The results demonstrate that capital allocation and risk contribution
are not equivalent. GOOG represented 40% of portfolio capital but
contributed approximately 46% of total portfolio risk.

---

## Performance Attribution

Active performance contribution was:

| Asset | Active Contribution     |
|-------|-------------------------|
| AAPL  | +0.91 percentage points |
| GOOG  | -0.35 percentage points |
| META  | -1.31 percentage points |
| Total | -0.74 percentage points |

The underweight to META was the largest negative contributor to active
performance, while the overweight to AAPL generated a positive
contribution.

---

## Transaction Cost Sensitivity

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

---

## Key Findings

### 1. Constraints can control concentration risk

The maximum 40% constraint prevents the portfolio from becoming
excessively concentrated in a single asset.

### 2. Equal weighting remains a useful benchmark

The equal-weight portfolio provides a transparent reference point
against which the effect of active allocation decisions can be measured.

### 3. Portfolio weights do not fully describe portfolio risk

GOOG contributed approximately 46% of portfolio risk despite having
a 40% portfolio weight.

### 4. Active allocation can create negative active performance

The maximum 40% portfolio underperformed the equal-weight benchmark
during the final out-of-sample period.

### 5. Attribution explains the source of underperformance

META was the largest negative contributor to active performance,
while AAPL was the largest positive contributor.

---

## Professional Interpretation
The project demonstrates the importance of separating portfolio
construction from portfolio risk analysis.

A portfolio can have apparently reasonable allocation weights while
still exhibiting disproportionate risk contributions.

Similarly, a constrained portfolio may provide better concentration
control without necessarily producing higher out-of-sample returns.

The results therefore support evaluating portfolio construction using
both performance and risk measures rather than relying solely on
return or Sharpe ratio.

---

## Tools

- Python
- NumPy
- pandas
- Matplotlib
- yfinance

---

## Files
`portfolio_risk_performance.py`

Contains the complete Python implementation of the portfolio risk,
performance, attribution, and transaction-cost analysis.
