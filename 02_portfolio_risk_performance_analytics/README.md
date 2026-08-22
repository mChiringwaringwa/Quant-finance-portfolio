# Portfolio Risk & Performance Analytics

## Objective
Develop a quantitative framework for evaluating an existing investment portfolio from a risk, performance and benchmark-relative perspective.

The project focuses on measuring portfolio performance, identifying sources of risk and return, and assessing whether active portfolio decisions generated value relative to a benchmark.

## Scope
This project builds on an already constructed portfolio and focuses specifically on portfolio analytics rather than asset selection or portfolio construction.
The analysis covers:

- Benchmark comparison
- Active return analysis
- Tracking error
- Information ratio
- Risk contribution
- Performance attribution
- Transaction-cost sensitivity
- Portfolio risk and performance interpretation

## Methodology

### 1. Benchmark Analysis
The portfolio was evaluated against an equal-weight benchmark representing a passive allocation to the same investment universe.

Portfolio and benchmark returns were compared over the evaluation period.

### 2. Active Return
Active return was calculated as:

Active Return = Portfolio Return - Benchmark Return

This measures the additional return generated relative to the benchmark.

### 3. Tracking Error
Tracking error was calculated using the volatility of active returns:

Tracking Error = Std(Portfolio Return - Benchmark Return)

This measures the consistency of the portfolio's deviation from benchmark performance.

### 4. Information Ratio
The Information Ratio was calculated as:

Information Ratio = Active Return / Tracking Error

This evaluates active performance relative to the risk taken against the benchmark.

### 5. Risk Contribution
Portfolio risk was decomposed into the contribution of individual assets.

The analysis uses portfolio weights and the covariance structure of asset returns to identify how much each asset contributes to total portfolio volatility.

This provides a more informative view of portfolio risk than considering asset weights alone.

### 6. Performance Attribution
Portfolio performance was decomposed to identify the contribution of individual holdings to overall portfolio returns.

This analysis helps explain which portfolio positions were responsible for positive or negative performance.

### 7. Transaction-Cost Sensitivity
The portfolio was evaluated under different transaction-cost assumptions to assess the robustness of observed performance after allowing for implementation costs.

This tests whether the strategy's apparent performance remains economically meaningful after accounting for trading frictions.

## Key Risk and Performance Measures
The framework evaluates:

- Portfolio return
- Benchmark return
- Active return
- Volatility
- Tracking error
- Information ratio
- Risk contribution
- Asset-level performance contribution
- Transaction-cost sensitivity

## Tools
- Python
- pandas
- NumPy
- SciPy
- Matplotlib
- yfinance

## Key Outcome
The project demonstrates the ability to evaluate an existing quantitative portfolio beyond headline returns by analysing benchmark-relative performance, active risk, information efficiency, asset-level risk contribution and performance attribution.

The framework also incorporates transaction-cost sensitivity to assess the robustness of portfolio performance under realistic implementation assumptions.

## Relationship to Project 01
Project 01 focuses on:

**Factor-based asset selection → portfolio construction → optimisation → robust validation**
This project focuses on:

**Existing portfolio → risk measurement → benchmark-relative analysis → performance attribution**
Together, the two projects demonstrate both portfolio construction capability and post-construction portfolio analytics.
