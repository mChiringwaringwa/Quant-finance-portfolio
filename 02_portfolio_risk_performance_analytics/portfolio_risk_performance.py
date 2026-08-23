# ============================================================
# PROJECT 02
# PORTFOLIO RISK & PERFORMANCE ANALYTICS
# ============================================================
#
# Purpose:
# Analyse portfolio performance and risk using the cleaned
# price data produced by Project 01.
#
# Data source:
# ../data/processed_prices.csv
#
# No new market-data download is required.
#
# Main analysis:
#   1. Load reusable price data
#   2. Calculate portfolio and benchmark returns
#   3. Construct equal-weight portfolio
#   4. Calculate return and risk measures
#   5. Calculate covariance and correlation
#   6. Calculate Value at Risk (VaR)
#   7. Calculate Expected Shortfall (ES)
#   8. Calculate maximum drawdown
#   9. Calculate portfolio beta
#  10. Compare portfolio with benchmark
#  11. Calculate active return
#  12. Calculate tracking error
#  13. Calculate information ratio
#  14. Calculate portfolio risk contribution
#
# ============================================================


# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import os
import numpy as np
import pandas as pd


# ============================================================
# 2. PROJECT SETTINGS
# ============================================================

assets = [
    "AAPL",
    "MSFT",
    "NVDA",
    "GOOG",
    "META"
]

benchmark = "^GSPC"

confidence_level = 0.95

trading_days = 252


# ============================================================
# 3. LOAD REUSABLE PRICE DATA
# ============================================================
#
# Project 01 created:
#
# ../data/processed_prices.csv
#
# Project 02 reads that file instead of downloading the
# market data again.
#
# ============================================================

data_path = "../data/processed_prices.csv"

if not os.path.exists(data_path):

    raise FileNotFoundError(
        "\nProcessed price data was not found.\n"
        "Expected file:\n"
        f"{data_path}\n\n"
        "Run Project 01 first and make sure "
        "processed_prices.csv is saved in ../data/"
    )


prices_all = pd.read_csv(
    data_path,
    index_col=0,
    parse_dates=True
)


# ============================================================
# 4. CHECK REQUIRED COLUMNS
# ============================================================

required_columns = assets + [benchmark]

missing_columns = [
    column
    for column in required_columns
    if column not in prices_all.columns
]

if missing_columns:

    raise ValueError(
        "The following required columns are missing "
        f"from processed_prices.csv: {missing_columns}"
    )


# ============================================================
# 5. SEPARATE ASSETS AND BENCHMARK
# ============================================================

prices = prices_all[assets].copy()

benchmark_prices = prices_all[benchmark].copy()


# Remove rows where all asset prices are missing

prices = prices.dropna(
    how="all"
)

benchmark_prices = benchmark_prices.dropna()


print("\n" + "=" * 60)
print("PROJECT 02 — PORTFOLIO RISK & PERFORMANCE ANALYTICS")
print("=" * 60)


# ============================================================
# 6. INSPECT LOADED PRICE DATA
# ============================================================

print("\n--- LOADED PRICE DATA ---")

print(
    prices.head()
)

print(
    "\nStart:",
    prices.index.min()
)

print(
    "End:",
    prices.index.max()
)

print(
    "Observations:",
    len(prices)
)

print(
    "Assets:",
    list(prices.columns)
)


# ============================================================
# 7. CALCULATE DAILY RETURNS
# ============================================================

returns = (
    prices
    .pct_change()
    .dropna()
)


benchmark_returns = (
    benchmark_prices
    .pct_change()
    .dropna()
)


print("\n--- PORTFOLIO DAILY RETURNS ---")

print(
    returns.head()
)


print("\n--- BENCHMARK DAILY RETURNS ---")

print(
    benchmark_returns.head()
)


# ============================================================
# 8. DATA QUALITY CHECK
# ============================================================

print("\n--- DATA CHECK ---")

print(
    "Price observations:",
    len(prices)
)

print(
    "Return observations:",
    len(returns)
)

print(
    "Missing price values:",
    prices.isna().sum().sum()
)

print(
    "Missing return values:",
    returns.isna().sum().sum()
)

print(
    "Missing benchmark return values:",
    benchmark_returns.isna().sum()
)


# ============================================================
# 9. ALIGN PORTFOLIO AND BENCHMARK RETURNS
# ============================================================

common_index = (
    returns.index
    .intersection(benchmark_returns.index)
)

returns = returns.loc[common_index]

benchmark_returns = benchmark_returns.loc[common_index]


# ============================================================
# 10. EQUAL-WEIGHT PORTFOLIO
# ============================================================

weights = pd.Series(
    1 / len(assets),
    index=assets
)


print("\n--- PORTFOLIO WEIGHTS ---")

print(
    weights
)

print(
    "\nWeight Sum:",
    weights.sum()
)


# ============================================================
# 11. PORTFOLIO DAILY RETURNS
# ============================================================

portfolio_returns = (
    returns
    .dot(weights)
)


print("\n--- PORTFOLIO DAILY RETURNS ---")

print(
    portfolio_returns.head()
)


# ============================================================
# 12. PORTFOLIO TOTAL RETURN
# ============================================================

portfolio_total_return = (
    (1 + portfolio_returns).prod()
    - 1
)


# ============================================================
# 13. PORTFOLIO ANNUALIZED RETURN
# ============================================================

number_of_days = len(portfolio_returns)

years = (
    number_of_days /
    trading_days
)


if years > 0:

    portfolio_annualized_return = (
        (1 + portfolio_total_return)
        ** (1 / years)
        - 1
    )

else:

    portfolio_annualized_return = np.nan


# ============================================================
# 14. PORTFOLIO ANNUALIZED VOLATILITY
# ============================================================

portfolio_annualized_volatility = (
    portfolio_returns.std()
    * np.sqrt(trading_days)
)


# ============================================================
# 15. PORTFOLIO SHARPE RATIO
# ============================================================
#
# Risk-free rate is assumed to be zero for this project.
#
# Sharpe = Annualized Return / Annualized Volatility
#
# ============================================================

if portfolio_annualized_volatility != 0:

    portfolio_sharpe = (
        portfolio_annualized_return /
        portfolio_annualized_volatility
    )

else:

    portfolio_sharpe = np.nan


# ============================================================
# 16. PORTFOLIO PERFORMANCE SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("PORTFOLIO PERFORMANCE")
print("=" * 60)

print(
    "Total Return:",
    round(portfolio_total_return, 6)
)

print(
    "Annualized Return:",
    round(portfolio_annualized_return, 6)
)

print(
    "Annualized Volatility:",
    round(portfolio_annualized_volatility, 6)
)

print(
    "Sharpe Ratio:",
    round(portfolio_sharpe, 6)
)


# ============================================================
# 17. CUMULATIVE PORTFOLIO WEALTH
# ============================================================

portfolio_wealth = (
    1 + portfolio_returns
).cumprod()


# ============================================================
# 18. MAXIMUM DRAWDOWN
# ============================================================

running_peak = (
    portfolio_wealth
    .cummax()
)

drawdown = (
    portfolio_wealth /
    running_peak
    - 1
)

maximum_drawdown = (
    drawdown.min()
)


print("\n--- DRAWDOWN ANALYSIS ---")

print(
    "Maximum Drawdown:",
    round(maximum_drawdown, 6)
)


# ============================================================
# 19. VALUE AT RISK
# ============================================================
#
# Historical VaR:
#
# VaR at 95% confidence is the 5th percentile of
# historical portfolio returns.
#
# A negative number represents a loss.
#
# ============================================================

alpha = 1 - confidence_level

historical_var = (
    portfolio_returns
    .quantile(alpha)
)


# ============================================================
# 20. EXPECTED SHORTFALL
# ============================================================
#
# Expected Shortfall is the average return of observations
# worse than the VaR threshold.
#
# ============================================================

tail_returns = (
    portfolio_returns[
        portfolio_returns <= historical_var
    ]
)

expected_shortfall = (
    tail_returns.mean()
)


print("\n--- DOWNSIDE RISK ---")

print(
    "Confidence Level:",
    confidence_level
)

print(
    "Historical VaR:",
    round(historical_var, 6)
)

print(
    "Expected Shortfall:",
    round(expected_shortfall, 6)
)


# ============================================================
# 21. COVARIANCE MATRIX
# ============================================================
#
# Annualized covariance:
#
# Daily covariance × 252
#
# ============================================================

covariance_matrix = (
    returns
    .cov()
    * trading_days
)


print("\n--- ANNUALIZED COVARIANCE MATRIX ---")

print(
    covariance_matrix
)


# ============================================================
# 22. CORRELATION MATRIX
# ============================================================

correlation_matrix = (
    returns
    .corr()
)


print("\n--- CORRELATION MATRIX ---")

print(
    correlation_matrix
)


# ============================================================
# 23. PORTFOLIO VARIANCE
# ============================================================
#
# Portfolio variance:
#
# σ²p = w' Σ w
#
# ============================================================

weight_vector = weights.values

covariance_matrix_values = (
    covariance_matrix.values
)

portfolio_variance = (
    weight_vector
    @ covariance_matrix_values
    @ weight_vector
)


# ============================================================
# 24. PORTFOLIO VOLATILITY FROM COVARIANCE MATRIX
# ============================================================

portfolio_volatility_from_matrix = (
    np.sqrt(portfolio_variance)
)


print("\n--- PORTFOLIO VARIANCE ---")

print(
    "Portfolio Variance:",
    round(portfolio_variance, 6)
)

print(
    "Portfolio Volatility:",
    round(
        portfolio_volatility_from_matrix,
        6
    )
)


# ============================================================
# 25. ASSET-LEVEL RISK CONTRIBUTION
# ============================================================
#
# Marginal Risk Contribution:
#
# MRC_i = (Σw)_i / σ_p
#
# Component Risk Contribution:
#
# CRC_i = w_i × (Σw)_i / σ_p
#
# Risk Contribution %:
#
# CRC_i / σ_p
#
# ============================================================

sigma_w = (
    covariance_matrix_values
    @ weight_vector
)

portfolio_volatility = (
    np.sqrt(
        weight_vector
        @ covariance_matrix_values
        @ weight_vector
    )
)


marginal_risk_contribution = (
    sigma_w /
    portfolio_volatility
)


component_risk_contribution = (
    weight_vector *
    marginal_risk_contribution
)


risk_contribution_percentage = (
    component_risk_contribution /
    portfolio_volatility
    * 100
)


risk_contribution_df = pd.DataFrame({

    "Asset": assets,

    "Weight": weight_vector,

    "Marginal_Risk_Contribution":
        marginal_risk_contribution,

    "Component_Risk_Contribution":
        component_risk_contribution,

    "Risk_Contribution_%":
        risk_contribution_percentage

})


print("\n" + "=" * 60)
print("PORTFOLIO RISK CONTRIBUTION")
print("=" * 60)

print(
    risk_contribution_df
)

print(
    "\nTotal Risk Contribution:",
    round(
        risk_contribution_percentage.sum(),
        4
    ),
    "%"
)


# ============================================================
# 26. BENCHMARK PERFORMANCE
# ============================================================

benchmark_total_return = (
    (1 + benchmark_returns).prod()
    - 1
)


benchmark_years = (
    len(benchmark_returns) /
    trading_days
)


if benchmark_years > 0:

    benchmark_annualized_return = (
        (1 + benchmark_total_return)
        ** (1 / benchmark_years)
        - 1
    )

else:

    benchmark_annualized_return = np.nan


benchmark_annualized_volatility = (
    benchmark_returns.std()
    * np.sqrt(trading_days)
)


if benchmark_annualized_volatility != 0:

    benchmark_sharpe = (
        benchmark_annualized_return /
        benchmark_annualized_volatility
    )

else:

    benchmark_sharpe = np.nan


print("\n" + "=" * 60)
print("BENCHMARK PERFORMANCE")
print("=" * 60)

print(
    "Benchmark Total Return:",
    round(benchmark_total_return, 6)
)

print(
    "Benchmark Annualized Return:",
    round(
        benchmark_annualized_return,
        6
    )
)

print(
    "Benchmark Annualized Volatility:",
    round(
        benchmark_annualized_volatility,
        6
    )
)

print(
    "Benchmark Sharpe Ratio:",
    round(
        benchmark_sharpe,
        6
    )
)


# ============================================================
# 27. PORTFOLIO BETA
# ============================================================
#
# Beta = Cov(Rp, Rm) / Var(Rm)
#
# ============================================================

portfolio_beta = (
    portfolio_returns
    .cov(benchmark_returns)
    /
    benchmark_returns.var()
)


print("\n--- PORTFOLIO BETA ---")

print(
    "Portfolio Beta:",
    round(
        portfolio_beta,
        6
    )
)


# ============================================================
# 28. ACTIVE RETURN
# ============================================================
#
# Active Return =
# Portfolio Return - Benchmark Return
#
# ============================================================

active_returns = (
    portfolio_returns -
    benchmark_returns
)


active_total_return = (
    (1 + active_returns).prod()
    - 1
)


print("\n" + "=" * 60)
print("ACTIVE RETURN ANALYSIS")
print("=" * 60)

print(
    "Portfolio Total Return:",
    round(
        portfolio_total_return,
        6
    )
)

print(
    "Benchmark Total Return:",
    round(
        benchmark_total_return,
        6
    )
)

print(
    "Active Total Return:",
    round(
        active_total_return,
        6
    )
)

print(
    "Average Daily Active Return:",
    round(
        active_returns.mean(),
        6
    )
)


# ============================================================
# 29. TRACKING ERROR
# ============================================================
#
# Tracking Error =
# Standard deviation of active returns
#
# Annualized Tracking Error =
# Daily Tracking Error × sqrt(252)
#
# ============================================================

daily_tracking_error = (
    active_returns.std()
)


annualized_tracking_error = (
    daily_tracking_error
    * np.sqrt(trading_days)
)


print("\n" + "=" * 60)
print("TRACKING ERROR")
print("=" * 60)

print(
    "Daily Tracking Error:",
    round(
        daily_tracking_error,
        6
    )
)

print(
    "Annualized Tracking Error:",
    round(
        annualized_tracking_error,
        6
    )
)


# ============================================================
# 30. INFORMATION RATIO
# ============================================================
#
# Information Ratio =
# Annualized Active Return /
# Annualized Tracking Error
#
# ============================================================

annualized_active_return = (
    active_returns.mean()
    * trading_days
)


if annualized_tracking_error != 0:

    information_ratio = (
        annualized_active_return /
        annualized_tracking_error
    )

else:

    information_ratio = np.nan


print("\n" + "=" * 60)
print("INFORMATION RATIO")
print("=" * 60)

print(
    "Annualized Active Return:",
    round(
        annualized_active_return,
        6
    )
)

print(
    "Annualized Tracking Error:",
    round(
        annualized_tracking_error,
        6
    )
)

print(
    "Information Ratio:",
    round(
        information_ratio,
        6
    )
)


# ============================================================
# 31. PERFORMANCE COMPARISON TABLE
# ============================================================

performance_comparison = pd.DataFrame({

    "Metric": [

        "Total Return",
        "Annualized Return",
        "Annualized Volatility",
        "Sharpe Ratio"

    ],

    "Portfolio": [

        portfolio_total_return,
        portfolio_annualized_return,
        portfolio_annualized_volatility,
        portfolio_sharpe

    ],

    "Benchmark": [

        benchmark_total_return,
        benchmark_annualized_return,
        benchmark_annualized_volatility,
        benchmark_sharpe

    ]

})


print("\n" + "=" * 60)
print("PORTFOLIO VS BENCHMARK")
print("=" * 60)

print(
    performance_comparison
)


# ============================================================
# 32. FINAL PROJECT SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("FINAL PROJECT SUMMARY")
print("=" * 60)

print(
    "\nPortfolio Assets:",
    assets
)

print(
    "Portfolio Type: Equal Weight"
)

print(
    "Benchmark:",
    benchmark
)

print(
    "\nPortfolio Total Return:",
    round(
        portfolio_total_return * 100,
        2
    ),
    "%"
)

print(
    "Portfolio Annualized Return:",
    round(
        portfolio_annualized_return * 100,
        2
    ),
    "%"
)

print(
    "Portfolio Annualized Volatility:",
    round(
        portfolio_annualized_volatility * 100,
        2
    ),
    "%"
)

print(
    "Portfolio Sharpe Ratio:",
    round(
        portfolio_sharpe,
        4
    )
)

print(
    "Portfolio Beta:",
    round(
        portfolio_beta,
        4
    )
)

print(
    "Maximum Drawdown:",
    round(
        maximum_drawdown * 100,
        2
    ),
    "%"
)

print(
    "95% Historical VaR:",
    round(
        historical_var * 100,
        2
    ),
    "%"
)

print(
    "95% Expected Shortfall:",
    round(
        expected_shortfall * 100,
        2
    ),
    "%"
)

print(
    "Active Return:",
    round(
        active_total_return * 100,
        2
    ),
    "%"
)

print(
    "Annualized Tracking Error:",
    round(
        annualized_tracking_error * 100,
        2
    ),
    "%"
)

print(
    "Information Ratio:",
    round(
        information_ratio,
        4
    )
)


print("\n" + "=" * 60)
print("PROJECT 02 COMPLETE")
print("=" * 60)
