# Project 02 — Portfolio Risk & Performance Analytics

## Objective
Evaluate the risk and benchmark-relative performance of the constrained
40/40/20 portfolio developed in Project 01.

Project 01 established the selected asset universe and produced two portfolio specifications: an equal-weight benchmark and a constrained 40/40/20 alternative.

Project 02 takes these frozen portfolios as inputs and performs detailed risk, benchmark-relative performance, attribution, and implementation analysis.

The 40/40/20 portfolio was selected as the constrained alternative model, while the-weight portfolio served as the transparent benchmark.

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

## Methodology
The analysis includes:

1. Portfolio risk contribution
2. Active return analysis
3. Active weight decomposition
4. Tracking error
5. Information ratio
6. Performance attribution

---
# Why Compare Equal Weight and 40/40/20?

The purpose is not to assume that optimisation must outperform equal weighting.

Instead, the analysis asks two separate questions:

### Question 1

Does the constrained optimisation model improve investment performance?

### Question 2

Does the constrained model provide a more controlled risk profile?

The final unseen test showed that the equal-weight benchmark produced stronger
performance than the 40/40/20 alternative.

However, the constrained portfolio provides a less concentrated alternative
to more aggressive optimisation solutions.

This highlights an important quantitative-finance principle:

> Optimisation should be evaluated on both return and risk, particularly on
> genuinely unseen data.

## Benchmark-Relative Performance
The 40/40/20 portfolio is compared with the equal-weight benchmark.

Active return is:
      R_(A,t) = R_(P,t) - R_(B,t)
where:
(R_P) = constrained portfolio return
(R_B) = equal-weight benchmark return

Active weights are:
(ActiveWeight)_i=ω_(P,i) - ω_(B,i)

For the 40/40/20 portfolio:

|Asset | Portfolio | Benchmark  | Active Weight |
|-----|---:|---:|---:|
|AAPL | 40.00% | 33.33% | +6.67% |
|GOOG | 40.00% | 33.33% | +6.67% |
|META | 20.00% | 33.33% |−13.33% |

The active weights sum to zero.

The portfolio therefore represented an overweight to AAPL and GOOG
and an underweight to META.

## Tracking Error
Tracking error measures the volatility of active returns:
      (TE)_daily=Std(R_P-R_B )

Annualised tracking error is:
      (TE)_annual=(TE)_daily √252

This measures how much the alternative portfolio deviates from the equal-weight benchmark.

## Information Ratio

The Information Ratio evaluates active return relative to active risk:
      IR=(Annualised Active Return)/(Annualised Tracking Error)
This provides a benchmark-relative assessment of whether active risk generated positive excess performance.

## Portfolio Risk Contribution
Portfolio risk is decomposed into asset-level contributions.

Portfolio variance:
      (σ_p)^2 = ω^T ∑ω

Marginal risk contribution:
(MRC)_i = (∑ω)_i /σ_P 

Component risk contribution:
(CRC)_i = ω_i (MRC)_i

Percentage contribution:
(RC)_i={(CRC)_i /σ_P} ×100

This distinguishes between capital allocation and risk allocation.
An asset with a smaller portfolio weight can still contribute substantially to portfolio risk because of its volatility and covariance relationships with the other assets.

## Performance Attribution
Active performance is also examined through the active portfolio weights and asset returns.

The analysis identifies which active positions contributed positively or negatively relative to the equal-weight benchmark.
This provides an additional explanation of the final out-of-sample result.

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
# Risk and Performance Framework

The project follows the framework:

40/40/20 Portfolio
        │
        ├── Absolute Performance
        │      ├── Return
        │      ├── Volatility
        │      ├── Sharpe
        │      └── Drawdown
        │
        ├── Benchmark Comparison
        │      ├── Active Return
        │      ├── Active Weights
        │      ├── Tracking Error
        │      └── Information Ratio
        │
        ├── Risk Decomposition
        │      ├── Covariance
        │      ├── Marginal Risk Contribution
        │      ├── Component Risk Contribution
        │      └── Percentage Risk Contribution
        │
        ├── Performance Attribution
              └── Asset-Level Active Contributions

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
