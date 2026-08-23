# ============================================================
# PROJECT 01
# FACTOR-BASED ASSET SELECTION & ROBUST PORTFOLIO OPTIMIZATION
# ============================================================
#
# Objective:
# Build a systematic factor-based asset-selection framework,
# evaluate parameter robustness, construct constrained portfolios,
# and test the frozen portfolios on a genuinely unseen period.
#
# Assets:
# AAPL, MSFT, NVDA, GOOG, META
#
# Benchmark:
# S&P 500 (^GSPC)
#
# Factors:
#   1. Rolling Beta
#   2. Momentum
#   3. Rolling Volatility
#   4. Rolling Sharpe Ratio
#
# Validation:
#   Outer split: 80% Development / 20% Final Unseen Test
#   Inner split: 80% Optimization Train / 20% Validation
#
# Hyperparameter grid:
#   Beta windows       = [40, 60, 80]
#   Momentum windows   = [40, 60, 80]
#   Volatility windows = [10, 20, 30]
#   Sharpe windows     = [40, 60, 80]
#
# Total combinations = 81
#
# IMPORTANT:
# Final-test data is never used for parameter selection.
# ============================================================


# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import os
from itertools import product

import numpy as np
import pandas as pd
from scipy.optimize import minimize


# ============================================================
# 2. PROJECT SETTINGS
# ============================================================

ASSETS = [
    "AAPL",
    "MSFT",
    "NVDA",
    "GOOG",
    "META"
]

BENCHMARK = "^GSPC"

TRADING_DAYS = 252

INITIAL_WEALTH = 1.0

RISK_FREE_RATE = 0.0

FINAL_TEST_FRACTION = 0.20

TOP_N_ASSETS = 3


# ============================================================
# 3. DATA PATHS
# ============================================================

DATA_PATH = "../data"

OUTPUT_PATH = "../outputs"

os.makedirs(
    DATA_PATH,
    exist_ok=True
)

os.makedirs(
    OUTPUT_PATH,
    exist_ok=True
)


# ============================================================
# 4. LOAD RAW CSV DATA
# ============================================================
#
# Project 01 uses the CSV files downloaded during data
# preparation.
#
# Expected structure:
#
# ../data/AAPL.csv
# ../data/MSFT.csv
# ../data/NVDA.csv
# ../data/GOOG.csv
# ../data/META.csv
# ../data/^GSPC.csv
#
# If your filenames differ, change only the filenames below.
# ============================================================


def load_price_csv(
    ticker,
    path
):
    """
    Load a single asset CSV and return a price Series.

    The function attempts to identify the Date and Close
    columns automatically.
    """

    file_path = os.path.join(
        path,
        f"{ticker}.csv"
    )

    if not os.path.exists(file_path):

        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    df = pd.read_csv(
        file_path
    )

    # --------------------------------------------------------
    # Identify date column
    # --------------------------------------------------------

    date_column = None

    for column in df.columns:

        if str(column).lower() == "date":

            date_column = column
            break

    if date_column is None:

        date_column = df.columns[0]

    df[date_column] = pd.to_datetime(
        df[date_column]
    )

    df = df.set_index(
        date_column
    )

    # --------------------------------------------------------
    # Identify Close column
    # --------------------------------------------------------

    close_column = None

    for column in df.columns:

        if str(column).lower() == "close":

            close_column = column
            break

    if close_column is None:

        raise ValueError(
            f"Close column not found in {file_path}"
        )

    prices = (
        pd.to_numeric(
            df[close_column],
            errors="coerce"
        )
        .rename(ticker)
    )

    return prices


# ============================================================
# 5. LOAD ALL ASSETS
# ============================================================

all_tickers = ASSETS + [BENCHMARK]

price_series = []

for ticker in all_tickers:

    series = load_price_csv(
        ticker,
        DATA_PATH
    )

    price_series.append(
        series
    )


# ============================================================
# 6. BUILD ALIGNED ASSET UNIVERSE
# ============================================================

asset_universe = pd.concat(
    price_series,
    axis=1,
    join="inner"
).sort_index()


# Remove rows with missing values

asset_universe = (
    asset_universe
    .dropna()
)


# ============================================================
# 7. INSPECT ASSET UNIVERSE
# ============================================================

print("\n" + "=" * 65)
print("ASSET UNIVERSE")
print("=" * 65)

print(
    asset_universe.head()
)

print(
    "\nStart:",
    asset_universe.index.min()
)

print(
    "End:",
    asset_universe.index.max()
)

print(
    "Observations:",
    len(asset_universe)
)

print(
    "Assets:",
    list(asset_universe.columns)
)


# ============================================================
# 8. SAVE REUSABLE PROCESSED PRICE DATA
# ============================================================
#
# Project 02 will read this file.
#
# This prevents Project 02 from repeating the raw-data
# preparation performed here.
# ============================================================

processed_prices_path = (
    "../data/processed_prices.csv"
)

asset_universe.to_csv(
    processed_prices_path
)

print(
    "\n--- REUSABLE DATA SAVED ---"
)

print(
    "Prices:",
    processed_prices_path
)


# ============================================================
# 9. CALCULATE RETURNS
# ============================================================

returns = (
    asset_universe
    .pct_change()
    .dropna()
)


development_returns = (
    returns
    .drop(columns=BENCHMARK)
)


benchmark_returns = (
    returns[BENCHMARK]
)


# ============================================================
# 10. OUTER DEVELOPMENT / FINAL TEST SPLIT
# ============================================================
#
# Chronological split:
#
# 80% Development
# 20% Final Unseen Test
#
# No random shuffling is used.
# ============================================================

split_index = int(
    len(asset_universe)
    * (1 - FINAL_TEST_FRACTION)
)


development_df = (
    asset_universe
    .iloc[:split_index]
    .copy()
)

final_test_df = (
    asset_universe
    .iloc[split_index:]
    .copy()
)


print(
    "\n--- ASSET SELECTION DATA SPLIT ---"
)

print(
    "\nDevelopment Data:"
)

print(
    "Start:",
    development_df.index.min()
)

print(
    "End:",
    development_df.index.max()
)

print(
    "Observations:",
    len(development_df)
)


print(
    "\nFinal Unseen Test Data:"
)

print(
    "Start:",
    final_test_df.index.min()
)

print(
    "End:",
    final_test_df.index.max()
)

print(
    "Observations:",
    len(final_test_df)
)


# ============================================================
# 11. CHRONOLOGY CHECK
# ============================================================

development_end = (
    development_df.index.max()
)

final_test_start = (
    final_test_df.index.min()
)


print(
    "\n--- CHRONOLOGY CHECK ---"
)

print(
    "Development ends:",
    development_end
)

print(
    "Final test begins:",
    final_test_start
)

print(
    "No overlap:",
    development_end < final_test_start
)


# ============================================================
# 12. DEVELOPMENT RETURNS
# ============================================================

development_returns = (
    development_df[ASSETS]
    .pct_change()
)


print(
    "\n--- DEVELOPMENT RETURNS ---"
)

print(
    development_returns.head()
)


# ============================================================
# 13. FACTOR SNAPSHOT FUNCTION
# ============================================================


def calculate_factor_snapshot(
    price_df,
    beta_window=60,
    momentum_window=60,
    volatility_window=20,
    sharpe_window=60
):
    """
    Calculate the latest available factor values for all
    candidate assets using only the supplied historical data.

    Factors:
        Beta
        Momentum
        Volatility
        Sharpe
    """

    asset_prices = (
        price_df[ASSETS]
        .copy()
    )

    market_prices = (
        price_df[BENCHMARK]
        .copy()
    )

    asset_returns = (
        asset_prices
        .pct_change()
    )

    market_returns = (
        market_prices
        .pct_change()
    )

    snapshot = pd.DataFrame(
        index=ASSETS
    )

    # --------------------------------------------------------
    # Rolling Beta
    # --------------------------------------------------------

    beta_values = {}

    for asset in ASSETS:

        covariance = (
            asset_returns[asset]
            .rolling(beta_window)
            .cov(market_returns)
        )

        market_variance = (
            market_returns
            .rolling(beta_window)
            .var()
        )

        beta_series = (
            covariance
            / market_variance
        )

        beta_values[asset] = (
            beta_series.iloc[-1]
        )

    snapshot["Beta"] = pd.Series(
        beta_values
    )


    # --------------------------------------------------------
    # Momentum
    # --------------------------------------------------------

    momentum = (
        asset_prices
        .pct_change(momentum_window)
        .iloc[-1]
    )

    snapshot["Momentum"] = (
        momentum
    )


    # --------------------------------------------------------
    # Annualized Volatility
    # --------------------------------------------------------

    volatility = (
        asset_returns
        .rolling(volatility_window)
        .std()
        .iloc[-1]
        * np.sqrt(TRADING_DAYS)
    )

    snapshot["Volatility"] = (
        volatility
    )


    # --------------------------------------------------------
    # Rolling Sharpe
    # --------------------------------------------------------

    rolling_mean = (
        asset_returns
        .rolling(sharpe_window)
        .mean()
        .iloc[-1]
    )

    rolling_std = (
        asset_returns
        .rolling(sharpe_window)
        .std()
        .iloc[-1]
    )

    sharpe = (
        rolling_mean
        / rolling_std
        * np.sqrt(TRADING_DAYS)
    )

    snapshot["Sharpe"] = (
        sharpe
    )


    return snapshot


# ============================================================
# 14. ASSET RANKING FUNCTION
# ============================================================


def rank_and_select_assets(
    snapshot
):
    """
    Rank assets using four equally weighted factors.

    Preferred characteristics:

        Lower Beta       -> better
        Higher Momentum  -> better
        Lower Volatility -> better
        Higher Sharpe    -> better

    Each factor receives 25%.
    """

    ranking = snapshot.copy()


    # --------------------------------------------------------
    # Factor scores
    # --------------------------------------------------------

    ranking["Beta_Score"] = (
        ranking["Beta"]
        .rank(
            pct=True,
            ascending=False
        )
    )

    ranking["Momentum_Score"] = (
        ranking["Momentum"]
        .rank(
            pct=True
        )
    )

    ranking["Volatility_Score"] = (
        ranking["Volatility"]
        .rank(
            pct=True,
            ascending=False
        )
    )

    ranking["Sharpe_Score"] = (
        ranking["Sharpe"]
        .rank(
            pct=True
        )
    )


    # --------------------------------------------------------
    # Composite Asset Score
    # --------------------------------------------------------

    ranking["Asset_Score"] = (
        0.25 * ranking["Beta_Score"]
        + 0.25 * ranking["Momentum_Score"]
        + 0.25 * ranking["Volatility_Score"]
        + 0.25 * ranking["Sharpe_Score"]
    )


    # --------------------------------------------------------
    # Sort
    # --------------------------------------------------------

    ranking = (
        ranking
        .sort_values(
            "Asset_Score",
            ascending=False
        )
    )


    selected_assets = (
        ranking
        .head(TOP_N_ASSETS)
        .index
        .tolist()
    )


    return ranking, selected_assets


# ============================================================
# 15. FINAL DEVELOPMENT FACTOR SNAPSHOT
# ============================================================

development_snapshot = (
    calculate_factor_snapshot(
        development_df
    )
)


print(
    "\n--- 60-DAY ROLLING BETA ---"
)

development_returns_all = (
    development_df
    .pct_change()
)

beta_table = pd.DataFrame(
    index=development_returns_all.index
)

for asset in ASSETS:

    covariance = (
        development_returns_all[asset]
        .rolling(60)
        .cov(
            development_returns_all[BENCHMARK]
        )
    )

    market_variance = (
        development_returns_all[BENCHMARK]
        .rolling(60)
        .var()
    )

    beta_table[asset] = (
        covariance
        / market_variance
    )


print(
    beta_table.tail()
)


print(
    "\n--- FINAL DEVELOPMENT BETA ---"
)

print(
    beta_table.iloc[-1]
)


# ============================================================
# 16. FINAL DEVELOPMENT FACTORS
# ============================================================

print(
    "\n--- FINAL DEVELOPMENT FACTOR SNAPSHOT ---"
)

print(
    development_snapshot
)


# ============================================================
# 17. DEVELOPMENT COVARIANCE MATRIX
# ============================================================

development_asset_returns = (
    development_df[ASSETS]
    .pct_change()
    .dropna()
)


development_covariance = (
    development_asset_returns
    .cov()
    * TRADING_DAYS
)


print(
    "\n--- DEVELOPMENT ANNUALIZED COVARIANCE MATRIX ---"
)

print(
    development_covariance
)


# ============================================================
# 18. DEVELOPMENT CORRELATION MATRIX
# ============================================================

development_correlation = (
    development_asset_returns
    .corr()
)


print(
    "\n--- DEVELOPMENT CORRELATION MATRIX ---"
)

print(
    development_correlation
)


# ============================================================
# 19. INNER DEVELOPMENT SPLIT
# ============================================================
#
# Development data is split again:
#
# 80% Optimization Train
# 20% Validation
#
# This validation period is used for hyperparameter selection.
#
# The final unseen test remains untouched.
# ============================================================

inner_split = int(
    len(development_df) * 0.80
)


optimization_train_df = (
    development_df
    .iloc[:inner_split]
    .copy()
)

optimization_validation_df = (
    development_df
    .iloc[inner_split:]
    .copy()
)


print(
    "\n--- INNER DEVELOPMENT SPLIT ---"
)

print(
    "\nOptimization Train:"
)

print(
    "Start:",
    optimization_train_df.index.min()
)

print(
    "End:",
    optimization_train_df.index.max()
)

print(
    "Observations:",
    len(optimization_train_df)
)


print(
    "\nOptimization Validation:"
)

print(
    "Start:",
    optimization_validation_df.index.min()
)

print(
    "End:",
    optimization_validation_df.index.max()
)

print(
    "Observations:",
    len(optimization_validation_df)
)

print(
    "\nNo overlap:",
    optimization_train_df.index.max()
    < optimization_validation_df.index.min()
)


# ============================================================
# 20. HYPERPARAMETER GRID
# ============================================================

beta_windows = [
    40,
    60,
    80
]

momentum_windows = [
    40,
    60,
    80
]

volatility_windows = [
    10,
    20,
    30
]

sharpe_windows = [
    40,
    60,
    80
]


parameter_grid = list(
    product(
        beta_windows,
        momentum_windows,
        volatility_windows,
        sharpe_windows
    )
)


print(
    "\nNumber of parameter combinations:",
    len(parameter_grid)
)


# ============================================================
# 21. HYPERPARAMETER OPTIMIZATION
# ============================================================

optimization_results = []


for (
    beta_window,
    momentum_window,
    volatility_window,
    sharpe_window
) in parameter_grid:

    # --------------------------------------------------------
    # Calculate factors using optimization train only
    # --------------------------------------------------------

    snapshot = calculate_factor_snapshot(
        optimization_train_df,
        beta_window=beta_window,
        momentum_window=momentum_window,
        volatility_window=volatility_window,
        sharpe_window=sharpe_window
    )


    # --------------------------------------------------------
    # Rank and select assets
    # --------------------------------------------------------

    ranking, selected_assets = (
        rank_and_select_assets(
            snapshot
        )
    )


    # --------------------------------------------------------
    # Validation returns
    # --------------------------------------------------------

    validation_returns = (
        optimization_validation_df[
            selected_assets
        ]
        .pct_change()
        .dropna()
    )


    # --------------------------------------------------------
    # Equal-weight portfolio
    # --------------------------------------------------------

    weights = np.repeat(
        1 / len(selected_assets),
        len(selected_assets)
    )


    portfolio_returns = (
        validation_returns
        .dot(weights)
    )


    # --------------------------------------------------------
    # Portfolio total return
    # --------------------------------------------------------

    total_return = (
        (1 + portfolio_returns)
        .prod()
        - 1
    )


    #
