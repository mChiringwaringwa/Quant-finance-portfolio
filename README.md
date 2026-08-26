
# Quantitative Finance Portfolio

## Overview

This repository contains quantitative finance projects developed in Python, with a focus on financial data analysis, quantitative asset selection, portfolio construction, risk measurement, performance evaluation, and systematic investment research.

The projects demonstrate the application of mathematical and statistical methods to real financial market data.

---

## Projects

### Project 01 — Quantitative Asset Selection

**File:** `01_factor_asset_selection_portfolio_optimisation/asset_selection.py`

This project develops a systematic asset-selection framework using multiple quantitative factors.

The analysis includes:

- Rolling beta estimation
- Momentum
- Volatility
- Sharpe ratio
- Cross-sectional factor ranking
- Composite asset scoring
- Asset selection
- Chronological development/test splitting
- Hyperparameter optimization
- Parameter sensitivity and robustness analysis
- Portfolio construction
- Out-of-sample testing
- Transaction-cost sensitivity
- Active return analysis
- Tracking error
- Information ratio
- Risk contribution analysis

The project uses a universe consisting of:

- AAPL
- MSFT
- NVDA
- GOOG
- META

with the S&P 500 used as the market benchmark where appropriate.

---

### Project 02 — Portfolio Risk & Performance Analytics

**File:** `project_02_portfolio_risk_performance_analytics/portfolio_risk_performance.py`

This project focuses on portfolio risk and performance measurement using historical market data.

The analysis includes:

- Daily return calculation
- Portfolio return calculation
- Benchmark comparison
- Annualized return
- Annualized volatility
- Sharpe ratio
- Maximum drawdown
- Transaction-cost sensitivity
- Active return
- Active weights
- Tracking error
- Information ratio
- Covariance matrix analysis
- Portfolio variance
- Portfolio volatility
- Marginal risk contribution
- Component risk contribution

The project demonstrates how portfolio performance can be evaluated from both an absolute and benchmark-relative perspective.

---

## Methodology

The projects emphasize realistic quantitative research practices, including:

1. Historical financial data preparation
2. Return calculation
3. Factor construction
4. Cross-sectional ranking
5. Portfolio construction
6. Risk measurement
7. Out-of-sample evaluation
8. Robustness testing
9. Transaction-cost analysis
10. Benchmark-relative performance attribution

Particular attention is given to avoiding look-ahead bias by maintaining chronological separation between development, validation, and final unseen test data.

---

## Technologies

The projects are implemented in Python using:

- Python
- NumPy
- pandas
- SciPy
- Matplotlib
- Seaborn
- yfinance

---

## Research Principles

The portfolio follows several principles used in quantitative investment research:

- Chronological data splitting
- Out-of-sample testing
- Walk-forward validation
- Parameter robustness
- Risk-adjusted performance evaluation
- Diversification analysis
- Transaction-cost sensitivity
- Benchmark-relative performance analysis

---

## Author

McDonald Chiringwaringwa

BSc Honours Applied Mathematics  
MSc Financial Engineering  
Actuarial Professional Examinations: CT1, CT3, CT4, CT5, CT8

---

## Disclaimer

These projects are for research, educational, and portfolio demonstration purposes only. They do not constitute investment advice or a recommendation to buy or sell any security.
