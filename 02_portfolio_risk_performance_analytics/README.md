# Project 02 — Portfolio Risk & Performance Analytics

## Objective

Evaluate the risk and benchmark-relative performance of the constrained **40/40/20 portfolio** developed in Project 01.

Project 01 established the selected asset universe and produced two portfolio specifications:

- An **equal-weight benchmark**
- A **constrained 40/40/20 alternative**

Project 02 takes these **frozen portfolios as inputs** and performs detailed risk, benchmark-relative performance, attribution, and tail-risk analysis.

The 40/40/20 portfolio was selected as the constrained alternative model, while the equal-weight portfolio served as the transparent benchmark.

---

## Portfolio

The final portfolio consists of:

| Asset | Portfolio Weight | Benchmark Weight |
|---|---:|---:|
| AAPL | 40.00% | 33.33% |
| GOOG | 40.00% | 33.33% |
| META | 20.00% | 33.33% |

The benchmark is an equal-weight portfolio:

- **AAPL:** 33.33%
- **GOOG:** 33.33%
- **META:** 33.33%

---

## Methodology

The analysis includes:

1. **Portfolio performance analysis**
2. **Active return analysis**
3. **Active weight decomposition**
4. **Tracking error**
5. **Information ratio**
6. **Portfolio risk contribution**
7. **Performance attribution**
8. **Historical Value at Risk (VaR)**
9. **Expected Shortfall (ES)**

Project 02 does **not**:

- Select assets
- Calculate investment factors
- Optimise portfolio weights
- Optimise trading parameters
- Redefine the portfolio established in Project 01

Instead, Project 02 evaluates the **frozen portfolio specifications** produced by Project 01.

---

# Why Compare Equal Weight and 40/40/20?

The purpose is not to assume that optimisation must outperform equal weighting.

Instead, the analysis asks two separate questions:

### Question 1

Does the constrained optimisation model improve investment performance?

### Question 2

Does the constrained model provide a more controlled risk profile?

The final unseen test showed that the equal-weight benchmark produced stronger performance than the 40/40/20 alternative.

This highlights an important quantitative-finance principle:

> **Optimisation should be evaluated on both return and risk, particularly on genuinely unseen data.**

---

## Benchmark-Relative Performance

The 40/40/20 portfolio is compared with the equal-weight benchmark.

Active return is:

$$
R_{A,t}=R_{P,t}-R_{B,t}
$$

where:

- $R_P$ = constrained portfolio return
- $R_B$ = equal-weight benchmark return

Active weights are:

$$
ActiveWeight_i=\omega_{P,i}-\omega_{B,i}
$$

For the 40/40/20 portfolio:

| Asset | Portfolio | Benchmark | Active Weight |
|---|---:|---:|---:|
| AAPL | 40.00% | 33.33% | +6.67% |
| GOOG | 40.00% | 33.33% | +6.67% |
| META | 20.00% | 33.33% | -13.33% |

The active weights sum to zero.

The portfolio therefore represented:

- An **overweight to AAPL**
- An **overweight to GOOG**
- An **underweight to META**

---

## Tracking Error

Tracking error measures the volatility of active returns:

$$
TE_{daily}=Std(R_P-R_B)
$$

Annualised tracking error is:

$$
TE_{annual}=TE_{daily}\sqrt{252}
$$

This measures how much the alternative portfolio deviates from the equal-weight benchmark.

The final out-of-sample annualised tracking error was:

**5.38%**

---

## Information Ratio

The Information Ratio evaluates active return relative to active risk:

$$
IR=
\frac{\text{Annualised Active Return}}
{\text{Annualised Tracking Error}}
$$

This provides a benchmark-relative assessment of whether active risk generated positive excess performance.

The final out-of-sample Information Ratio was:

**-0.73**

The negative Information Ratio indicates that the active allocation generated negative benchmark-relative performance relative to the tracking risk taken.

---

# Portfolio Risk Contribution

Portfolio risk is decomposed into asset-level contributions.

Portfolio variance:

$$
\sigma_P^2=\omega^T\Sigma\omega
$$

Marginal risk contribution:

$$
MRC_i=\frac{(\Sigma\omega)_i}{\sigma_P}
$$

Component risk contribution:

$$
CRC_i=\omega_i(MRC_i)
$$

Percentage contribution:

$$
RC_i=
\frac{CRC_i}{\sigma_P}\times100
$$

This distinguishes between **capital allocation** and **risk allocation**.

An asset with a smaller portfolio weight can still contribute substantially to portfolio risk because of its volatility and covariance relationships with the other assets.

---

## Performance Attribution

Active performance is also examined through the active portfolio weights and asset returns.

The analysis identifies which active positions contributed positively or negatively relative to the equal-weight benchmark.

This provides an additional explanation of the final out-of-sample result.

---

# Tail Risk Analysis — VaR and Expected Shortfall

Project 02 also evaluates portfolio downside tail risk using return observations from the final out-of-sample period.

## Historical Value at Risk

Historical VaR at the **95% confidence level** is estimated from the 5th percentile of the portfolio return distribution.

$$
VaR_{95\%}=Q_{0.05}(R_P)
$$

The negative-return convention used in the analysis represents the portfolio return threshold associated with the worst 5% of historical observations.

## Expected Shortfall

Expected Shortfall measures the average portfolio return in the tail beyond the 95% VaR threshold:

$$
ES_{95\%}
=
E[R_P\mid R_P\leq VaR_{95\%}]
$$

ES therefore provides additional information about the severity of losses once the VaR threshold has been breached.

### Final OOS Tail-Risk Results

| Portfolio | Historical VaR 95% | Expected Shortfall 95% |
|---|---:|---:|
| Equal Weight | **-2.62%** | **-2.94%** |
| Max 40 | **-2.38%** | **-2.81%** |

The Max-40 portfolio therefore experienced a slightly less severe historical left tail during the final OOS period than the equal-weight benchmark.

---

# Out-of-Sample Performance

The final out-of-sample results were:

| Metric | Max-40 Portfolio | Equal-Weight Benchmark |
|---|---:|---:|
| Total Return | **5.07%** | **5.75%** |
| Active Return | **-0.77%** | — |
| Information Ratio | **-0.73** | — |
| Annualized Tracking Error | **5.38%** | — |

The constrained portfolio underperformed the equal-weight benchmark during the final test period.

The final wealth values were:

- **Equal Weight:** 1.057545
- **Max-40:** 1.050666

This means that an initial investment of 1.00 would have grown to approximately:

- **1.0575** under Equal Weight
- **1.0507** under Max-40

during the final out-of-sample period.

---

# Risk Decomposition

The final OOS annualised covariance matrix was:

| | AAPL | GOOG | META |
|---|---:|---:|---:|
| **AAPL** | 0.079086 | 0.007578 | 0.022679 |
| **GOOG** | 0.007578 | 0.094217 | 0.059941 |
| **META** | 0.022679 | 0.059941 | 0.198375 |

Risk contribution was:

| Asset | Portfolio Weight | Risk Contribution |
|---|---:|---:|
| AAPL | 40.00% | **30.56%** |
| GOOG | 40.00% | **41.09%** |
| META | 20.00% | **28.35%** |

The results demonstrate that **capital allocation and risk contribution are not equivalent**.

GOOG represented 40% of portfolio capital but contributed approximately **41.09%** of total portfolio risk.

AAPL also represented 40% of capital but contributed only **30.56%** of portfolio risk, illustrating the effect of individual asset volatility and covariance relationships.

---

# Performance Attribution

Active performance contribution was:

| Asset | Active Contribution |
|---|---:|
| AAPL | **+0.92 percentage points** |
| GOOG | **-0.39 percentage points** |
| META | **-1.12 percentage points** |
| **Total simplified contribution** | **-0.58 percentage points** |

The underweight to META was the largest negative contributor to active performance, while the overweight to AAPL generated a positive contribution.

The simplified additive attribution sums to approximately **-0.58 percentage points**, while the actual compounded active return was **-0.77%**.

The difference arises because the simplified attribution calculation uses active weights multiplied by cumulative asset returns, whereas the actual active portfolio return is calculated from the compounded daily portfolio returns.

---

# Risk and Performance Framework

The project follows the framework:

```text
40/40/20 Portfolio
│
├── Absolute Performance
│   ├── Return
│   ├── Volatility
│   ├── Sharpe
│   └── Drawdown
│
├── Benchmark Comparison
│   ├── Active Return
│   ├── Active Weights
│   ├── Tracking Error
│   └── Information Ratio
│
├── Risk Decomposition
│   ├── Covariance
│   ├── Marginal Risk Contribution
│   ├── Component Risk Contribution
│   └── Percentage Risk Contribution
│
├── Tail Risk
│   ├── Historical VaR 95%
│   └── Expected Shortfall 95%
│
└── Performance Attribution
    └── Asset-Level Active Contributions


# Key Findings

## 1. Equal weighting remains a useful benchmark

The equal-weight portfolio provides a transparent reference point against which the effect of active allocation decisions can be measured.

## 2. Portfolio weights do not fully describe portfolio risk

GOOG contributed approximately 41.09% of portfolio risk despite having a 40% portfolio weight.

AAPL also had a 40% portfolio weight but contributed only 30.56% of portfolio risk.

This demonstrates the importance of considering volatility and covariance rather than looking only at capital weights.

## 3. Active allocation can create negative active performance

The Max-40 portfolio underperformed the equal-weight benchmark during the final out-of-sample period.

The Max-40 portfolio returned approximately 5.07%, compared with 5.75% for the equal-weight benchmark.

## 4. Attribution explains the source of underperformance

META was the largest negative contributor to active performance, while AAPL was the largest positive contributor.

## 5. The Max-40 portfolio exhibited slightly lower tail losses

Historical VaR and Expected Shortfall were both less negative for the Max-40 portfolio:

- **VaR 95%:** -2.38% versus -2.62% for Equal Weight
- **ES 95%:** -2.81% versus -2.94% for Equal Weight

This indicates that, during the final OOS period, the Max-40 portfolio experienced somewhat less severe losses in the historical left tail.

## 6. Active risk did not translate into positive benchmark-relative performance

The annualised tracking error was 5.38%, while the Information Ratio was -0.73.

Therefore, the active allocation generated negative benchmark-relative performance relative to the amount of active risk taken.

---

# Professional Interpretation

The project demonstrates the importance of separating portfolio construction from portfolio risk analysis.

A portfolio can have apparently reasonable allocation weights while still exhibiting disproportionate risk contributions.

Similarly, a constrained portfolio may provide better concentration control without necessarily producing higher out-of-sample returns.

The results therefore support evaluating portfolio construction using both performance and risk measures rather than relying solely on return or Sharpe ratio.

The addition of VaR and Expected Shortfall extends the analysis from conventional volatility-based risk measures to tail-risk assessment, providing a clearer view of potential losses during adverse return observations.

Most importantly, Project 02 does not alter the portfolio selected by Project 01. It treats the portfolio specifications as frozen inputs and focuses on answering:

> **How did the selected portfolios actually perform, what risks did they take, and where did those risks and returns come from during the final unseen period?**

---

# Project 02 Position in the Overall Architecture

```text
PROJECT 01
Asset Selection & Portfolio Construction
        │
        │ Frozen portfolio specifications
        ▼
PROJECT 02
Portfolio Risk & Performance Analytics
        │
        ├── Long-term performance
        ├── Portfolio risk
        ├── Benchmark-relative analysis
        ├── VaR / ES
        ├── Risk contribution
        └── Performance attribution
        │
        ▼
PROJECT 03
Short-Term Trading Engine
        │
        ├── Same selected portfolio
        ├── Short-term signals
        ├── Trading decisions
        └── Execution / backtesting

The three-project architecture separates the responsibilities clearly:
Project
Primary Question
Project 01
What should we invest in and how should the portfolio be constructed?
Project 02
How does the selected portfolio perform and what risks does it carry?
Project 03
How can we trade the same selected portfolio over the short term?
Project 03 therefore operates on the same selected investment universe established by Project 01, rather than independently redefining the portfolio.
Tools
Python
NumPy
pandas
Matplotlib
yfinance
Files
portfolio_risk_performance.py
Contains the complete Python implementation of the portfolio:
Risk analysis
Performance analysis
Benchmark-relative analysis
Active weights
Tracking error
Information ratio
Risk contribution
Performance attribution
Historical VaR
Expected Shortfall
Project 02 Outputs
The analysis produces:
performance_comparison.csv
active_weights.csv
performance_attribution.csv
risk_contribution.csv
portfolio_returns.csv
daily_active_contribution.csv
oos_covariance_matrix.csv
risk_performance_summary.csv
These outputs provide the numerical evidence supporting the risk, performance, attribution, and benchmark-relative conclusions documented above.
Conclusion
Project 02 provides an independent risk and performance analytics layer for the portfolios produced by Project 01.
Rather than changing the portfolio construction decision, it evaluates the realised behaviour of the frozen portfolios across:
performance → benchmark-relative performance → risk decomposition → tail risk → attribution
The final OOS results show that the equal-weight benchmark achieved the higher return, while the Max-40 portfolio displayed slightly lower historical tail risk.
The analysis therefore demonstrates that portfolio evaluation requires a multi-dimensional assessment of:
Return
Active risk
Portfolio risk contribution
Volatility
Drawdown
Tail risk
Performance attribution
rather than relying on a single performance metric.

Project 02 is complete.