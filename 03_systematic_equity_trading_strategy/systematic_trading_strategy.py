
# ============================================================
# PROJECT 03
# SYSTEMATIC TRADING STRATEGY & OUT-OF-SAMPLE VALIDATION
#
# ARCHITECTURE
# ============================================================
#
# PROJECT 01
#     Asset Selection + Portfolio Construction
#                    |
#                    v
#     frozen_portfolios.csv
#     processed_prices.csv
#                    |
#                    v
# PROJECT 03
#     Trading Strategy + Parameter Optimisation
#     + Expanding Walk-Forward Validation
#     + Rolling Walk-Forward Validation
#     + Parameter Sensitivity
#     + Regime Robustness
#     + Final Out-of-Sample Test
#
# IMPORTANT:
#
# Project 03 DOES NOT:
#     - select assets
#     - select a portfolio
#     - optimise portfolio weights
#     - change Project 01 weights
#
# Project 03 DOES:
#     - inherit the frozen Project 01 portfolio
#     - generate trading signals for inherited assets
#     - optimise trading-rule parameters
#     - validate the trading strategy
#     - evaluate final unseen performance
# ============================================================


import os
import warnings
from itertools import product

import numpy as np
import pandas as pd


warnings.filterwarnings("ignore")


# ============================================================
# 1. CONFIGURATION
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_NAME = (
    "Project_03_Systematic_Trading"
)


# ------------------------------------------------------------
# Project 01 portfolio to inherit
#
# IMPORTANT:
# This is NOT a portfolio decision made by Project 03.
#
# Project 03 reads this portfolio from Project 01.
# ------------------------------------------------------------

TARGET_PORTFOLIO = "Max_40"


# ------------------------------------------------------------
# Trading parameter grid
#
# 4 × 3 × 3 = 36 combinations
# ------------------------------------------------------------

SHORT_WINDOWS = [
    10,
    15,
    20,
    25
]

LONG_WINDOWS = [
    40,
    50,
    60
]

RSI_THRESHOLDS = [
    60,
    70,
    80
]


# ------------------------------------------------------------
# Walk-forward parameters
# ------------------------------------------------------------

TRAIN_SIZE = 100
TEST_SIZE = 30


# ------------------------------------------------------------
# Final chronological split
#
# First 80% = development
# Last 20%  = final unseen test
# ------------------------------------------------------------

FINAL_TEST_FRACTION = 0.20


# ------------------------------------------------------------
# Parameter sensitivity
# ------------------------------------------------------------

SENSITIVITY_SHORT_VALUES = list(
    range(8, 18)
)

SENSITIVITY_LONG_VALUES = list(
    range(38, 53)
)

SENSITIVITY_RSI = 70


# ------------------------------------------------------------
# Risk-free rate
# ------------------------------------------------------------

RISK_FREE_RATE_ANNUAL = 0.0


# ============================================================
# 2. DATA PATHS
# ============================================================

DATA_DIR = os.path.join(
    PROJECT_ROOT,
    "data"
)

FROZEN_PORTFOLIOS_FILE = os.path.join(
    DATA_DIR,
    "frozen_portfolios.csv"
)

PROCESSED_PRICES_FILE = os.path.join(
    DATA_DIR,
    "processed_prices.csv"
)


# ------------------------------------------------------------
# If Project 01 files are not copied into Project 03/data,
# also check common Project 01 locations.
# ------------------------------------------------------------

def find_project01_file(filename):

    candidate_paths = [

        os.path.join(
            PROJECT_ROOT,
            "data",
            filename
        ),

        os.path.join(
            PROJECT_ROOT,
            "..",
            "Project_01",
            "data",
            filename
        ),

        os.path.join(
            PROJECT_ROOT,
            "..",
            "Project 1",
            "data",
            filename
        ),

        os.path.join(
            PROJECT_ROOT,
            "..",
            "Project1",
            "data",
            filename
        ),

        os.path.join(
            PROJECT_ROOT,
            "..",
            "data",
            filename
        )
    ]

    for path in candidate_paths:

        path = os.path.abspath(path)

        if os.path.isfile(path):
            return path

    raise FileNotFoundError(
        f"\nCould not find {filename}.\n\n"
        "Project 03 expects Project 01 output in:\n"
        f"{os.path.abspath(DATA_DIR)}\n\n"
        "Expected file:\n"
        f"{filename}"
    )


# ============================================================
# 3. LOAD PROJECT 01 FROZEN PORTFOLIO
# ============================================================

frozen_path = find_project01_file(
    "frozen_portfolios.csv"
)


print("\n" + "=" * 70)
print("PROJECT 01 FROZEN PORTFOLIO")
print("=" * 70)


print(
    "\nFrozen portfolio file:"
)

print(
    frozen_path
)


# ------------------------------------------------------------
# IMPORTANT:
#
# Our actual Project 01 file has this structure:
#
#             AAPL     GOOG     META
# Equal_Weight ...
# Max_40       ...
# Max_50       ...
#
# Therefore:
#
#   index  = portfolio names
#   columns = asset names
#
# There is NO separate Portfolio column,
# Asset column or Weight column.
# ------------------------------------------------------------

frozen_portfolios = pd.read_csv(
    frozen_path,
    index_col=0
)


print(
    "\nFrozen portfolios loaded:"
)

print(
    frozen_portfolios
)


print(
    "\nPortfolio names:"
)

print(
    frozen_portfolios.index.tolist()
)


print(
    "\nAsset columns:"
)

print(
    frozen_portfolios.columns.tolist()
)


# ============================================================
# 4. VERIFY TARGET PORTFOLIO
# ============================================================

if TARGET_PORTFOLIO not in frozen_portfolios.index:

    raise ValueError(
        f"\nPortfolio '{TARGET_PORTFOLIO}' "
        "was not found in Project 01 frozen portfolios.\n\n"
        f"Available portfolios:\n"
        f"{frozen_portfolios.index.tolist()}"
    )


# ============================================================
# 5. INHERIT FROZEN PROJECT 01 WEIGHTS
# ============================================================

frozen_weights = (
    frozen_portfolios
    .loc[TARGET_PORTFOLIO]
    .copy()
)


# ------------------------------------------------------------
# Convert weights to numeric
# ------------------------------------------------------------

frozen_weights = pd.to_numeric(
    frozen_weights,
    errors="coerce"
)


if frozen_weights.isna().any():

    raise ValueError(
        "\nNon-numeric values were found in "
        "the frozen portfolio weights."
    )


# ------------------------------------------------------------
# Remove zero-weight assets
#
# Example:
#
# Max_40:
# AAPL = 0.40
# GOOG = 0.40
# META = 0.20
#
# All three remain.
#
# An asset with 0.00 weight is not part of the
# active inherited portfolio.
# ------------------------------------------------------------

frozen_weights = (
    frozen_weights[
        frozen_weights > 0
    ]
)


# ============================================================
# 6. VALIDATE FROZEN WEIGHTS
# ============================================================

weight_sum = (
    frozen_weights.sum()
)


print(
    "\n" + "=" * 70
)

print(
    "INHERITED PROJECT 01 PORTFOLIO"
)

print(
    "=" * 70
)


print(
    "\nTarget portfolio:"
)

print(
    TARGET_PORTFOLIO
)


print(
    "\nInherited weights:"
)

print(
    frozen_weights
)


print(
    f"\nWeight sum: {weight_sum:.6f}"
)


if not np.isclose(
    weight_sum,
    1.0,
    atol=1e-6
):

    raise ValueError(
        "\nProject 01 frozen portfolio weights "
        "do not sum to 1.0.\n"
        f"Observed sum: {weight_sum:.6f}\n\n"
        "Project 03 will NOT modify these weights."
    )


# ------------------------------------------------------------
# Assets and weights used throughout Project 03
# ------------------------------------------------------------

ASSETS = (
    frozen_weights
    .index
    .tolist()
)


WEIGHTS = frozen_weights.astype(
    float
)


print(
    "\nAssets inherited from Project 01:"
)

print(
    ASSETS
)


print(
    "\nWeights inherited from Project 01:"
)

print(
    WEIGHTS
)


# ============================================================
# 7. LOAD PROJECT 01 PROCESSED PRICES
# ============================================================

prices_path = find_project01_file(
    "processed_prices.csv"
)


print(
    "\n" + "=" * 70
)

print(
    "PROJECT 01 PROCESSED PRICES"
)

print(
    "=" * 70
)


print(
    "\nProcessed price file:"
)

print(
    prices_path
)


# ------------------------------------------------------------
# Actual Project 01 processed_prices.csv structure:
#
# Date | AAPL | MSFT | NVDA | GOOG | META | ^GSPC
#
# The first column is the Date index.
# ------------------------------------------------------------

prices = pd.read_csv(
    prices_path,
    index_col=0,
    parse_dates=True
)


print(
    "\nProcessed prices loaded:"
)

print(
    prices.shape
)


print(
    "\nAvailable price columns:"
)

print(
    prices.columns.tolist()
)


print(
    "\nFirst five observations:"
)

print(
    prices.head()
)


# ============================================================
# 8. CHECK FROZEN ASSETS AGAINST PRICE DATA
# ============================================================

missing_assets = [
    asset
    for asset in ASSETS
    if asset not in prices.columns
]


if missing_assets:

    raise ValueError(
        "\nProject 01 frozen assets are missing "
        "from processed_prices.csv.\n\n"
        f"Missing assets:\n{missing_assets}\n\n"
        f"Available price columns:\n"
        f"{prices.columns.tolist()}"
    )


# ============================================================
# 9. KEEP ONLY INHERITED PORTFOLIO ASSETS
# ============================================================

prices = (
    prices[
        ASSETS
    ]
    .copy()
)


# ------------------------------------------------------------
# Ensure numerical prices
# ------------------------------------------------------------

for asset in ASSETS:

    prices[asset] = pd.to_numeric(
        prices[asset],
        errors="coerce"
    )


# ------------------------------------------------------------
# Sort chronologically
# ------------------------------------------------------------

prices = prices.sort_index()


# ------------------------------------------------------------
# Remove observations where one of the inherited assets
# is unavailable.
# ------------------------------------------------------------

prices = prices.dropna(
    subset=ASSETS,
    how="any"
)


# ============================================================
# 10. CREATE DAILY RETURNS
# ============================================================

returns = (
    prices
    .pct_change()
    .dropna()
)


print(
    "\n" + "=" * 70
)

print(
    "PROJECT 03 DATASET"
)

print(
    "=" * 70
)


print(
    "\nAssets used:"
)

print(
    ASSETS
)


print(
    "\nNumber of price observations:"
)

print(
    len(prices)
)


print(
    "\nNumber of return observations:"
)

print(
    len(returns)
)


print(
    "\nDate range:"
)

print(
    prices.index.min(),
    "to",
    prices.index.max()
)


# ============================================================
# 11. FROZEN PORTFOLIO BUY & HOLD
# ============================================================
#
# This is the benchmark for Project 03.
#
# It represents what would happen if we simply held
# the Project 01 portfolio without applying a trading overlay.
#
# IMPORTANT:
#
# AAPL = 40%
# GOOG = 40%
# META = 20%
#
# These weights remain unchanged.
# ============================================================

portfolio_bh_returns = (
    returns[
        ASSETS
    ]
    .mul(
        WEIGHTS,
        axis=1
    )
    .sum(axis=1)
)


portfolio_bh_returns.name = (
    "Frozen_Portfolio_Buy_Hold"
)


# ============================================================
# 12. RSI FUNCTION
# ============================================================

def calculate_rsi(
    series,
    period=14
):

    delta = series.diff()

    gain = delta.clip(
        lower=0
    )

    loss = -delta.clip(
        upper=0
    )

    average_gain = (
        gain
        .rolling(
            period
        )
        .mean()
    )

    average_loss = (
        loss
        .rolling(
            period
        )
        .mean()
    )

    rs = (
        average_gain /
        average_loss.replace(
            0,
            np.nan
        )
    )

    rsi = (
        100 -
        (
            100 /
            (1 + rs)
        )
    )

    return rsi


# ============================================================
# 13. ASSET TRADING STRATEGY
# ============================================================
#
# Trading rule:
#
#     SMA_short > SMA_long
#              AND
#     RSI > RSI threshold
#
# Signal:
#
#     1 = invested
#     0 = cash
#
# Strategy return:
#
#     Signal_(t-1) × Asset_Return_t
#
# The one-day lag is essential.
# ============================================================

def generate_asset_strategy(
    price_series,
    short_window,
    long_window,
    rsi_threshold
):

    result = pd.DataFrame(
        index=price_series.index
    )

    result["Price"] = (
        price_series
    )

    result["Daily_Return"] = (
        price_series
        .pct_change()
    )

    result["SMA_Short"] = (
        price_series
        .rolling(
            short_window
        )
        .mean()
    )

    result["SMA_Long"] = (
        price_series
        .rolling(
            long_window
        )
        .mean()
    )

    result["RSI"] = calculate_rsi(
        price_series,
        period=14
    )


    # --------------------------------------------------------
    # Trading signal
    # --------------------------------------------------------

    result["Signal"] = (
        (
            result["SMA_Short"]
            >
            result["SMA_Long"]
        )
        &
        (
            result["RSI"]
            >
            rsi_threshold
        )
    ).astype(float)


    # --------------------------------------------------------
    # Lag signal by one trading day.
    #
    # Today's signal cannot earn today's return.
    # --------------------------------------------------------

    result["Strategy_Return"] = (
        result["Signal"]
        .shift(1)
        *
        result["Daily_Return"]
    )


    return result


# ============================================================
# 14. PORTFOLIO TRADING STRATEGY
# ============================================================
#
# The same trading rule is applied to every asset inherited
# from Project 01.
#
# The resulting asset strategy returns are then multiplied
# by the FROZEN Project 01 weights.
#
# NO WEIGHT RENORMALISATION.
# ============================================================

def generate_portfolio_strategy(
    price_df,
    short_window,
    long_window,
    rsi_threshold
):

    asset_strategy_returns = (
        pd.DataFrame(
            index=price_df.index
        )
    )

    asset_signals = (
        pd.DataFrame(
            index=price_df.index
        )
    )


    for asset in ASSETS:

        asset_result = (
            generate_asset_strategy(
                price_df[asset],
                short_window,
                long_window,
                rsi_threshold
            )
        )


        asset_strategy_returns[
            asset
        ] = (
            asset_result[
                "Strategy_Return"
            ]
        )


        asset_signals[
            asset
        ] = (
            asset_result[
                "Signal"
            ]
        )


    # --------------------------------------------------------
    # Apply frozen Project 01 weights.
    #
    # Example:
    #
    # AAPL signal = 1
    # GOOG signal = 0
    # META signal = 1
    #
    # Contributions:
    #
    # AAPL = 0.40 × AAPL return
    # GOOG = 0.40 × 0
    # META = 0.20 × META return
    #
    # We DO NOT turn this into:
    #
    # AAPL = 66.67%
    # META = 33.33%
    #
    # because that would change the Project 01 portfolio.
    # --------------------------------------------------------

    weighted_returns = (
        asset_strategy_returns
        .mul(
            WEIGHTS,
            axis=1
        )
    )


    portfolio_strategy_returns = (
        weighted_returns
        .sum(axis=1)
    )


    portfolio_strategy_returns.name = (
        "Strategy_Return"
    )


    return (
        portfolio_strategy_returns,
        asset_strategy_returns,
        asset_signals
    )


# ============================================================
# 15. PERFORMANCE FUNCTIONS
# ============================================================

def total_return(
    returns_series
):

    clean = (
        returns_series
        .dropna()
    )

    if len(clean) == 0:
        return np.nan

    return (
        (1 + clean).prod()
        - 1
    )


def annualised_return(
    returns_series
):

    clean = (
        returns_series
        .dropna()
    )

    if len(clean) == 0:
        return np.nan

    total = total_return(
        clean
    )

    return (
        (1 + total)
        **
        (252 / len(clean))
        - 1
    )


def annualised_volatility(
    returns_series
):

    clean = (
        returns_series
        .dropna()
    )

    if len(clean) < 2:
        return np.nan

    return (
        clean.std()
        *
        np.sqrt(252)
    )


def sharpe_ratio(
    returns_series
):

    clean = (
        returns_series
        .dropna()
    )

    if len(clean) < 2:
        return np.nan

    excess_daily = (
        clean.mean()
        -
        RISK_FREE_RATE_ANNUAL / 252
    )

    volatility = (
        clean.std()
    )

    if volatility == 0:
        return np.nan

    return (
        excess_daily /
        volatility
        *
        np.sqrt(252)
    )


def maximum_drawdown(
    returns_series
):

    clean = (
        returns_series
        .dropna()
    )

    if len(clean) == 0:
        return np.nan

    wealth = (
        1 + clean
    ).cumprod()

    running_peak = (
        wealth.cummax()
    )

    drawdown = (
        wealth /
        running_peak
        - 1
    )

    return drawdown.min()


def evaluate_returns(
    returns_series
):

    clean = (
        returns_series
        .dropna()
    )

    return {

        "Total Return":
            total_return(
                clean
            ),

        "Annualized Return":
            annualised_return(
                clean
            ),

        "Annualized Volatility":
            annualised_volatility(
                clean
            ),

        "Sharpe":
            sharpe_ratio(
                clean
            ),

        "Maximum Drawdown":
            maximum_drawdown(
                clean
            ),

        "Final Wealth":
            (
                1 + clean
            ).prod()
    }


# ============================================================
# 16. PARAMETER OPTIMISATION
# ============================================================
#
# Parameters are optimised using ONLY the supplied training
# dataset.
#
# Portfolio weights are NEVER optimised here.
# ============================================================

def optimise_parameters(
    price_df
):

    results = []


    for (
        short_window,
        long_window,
        rsi_threshold
    ) in product(
        SHORT_WINDOWS,
        LONG_WINDOWS,
        RSI_THRESHOLDS
    ):


        # ----------------------------------------------------
        # Short moving average must be shorter than long.
        # ----------------------------------------------------

        if short_window >= long_window:
            continue


        strategy_returns, _, _ = (
            generate_portfolio_strategy(
                price_df,
                short_window,
                long_window,
                rsi_threshold
            )
        )


        score = total_return(
            strategy_returns
        )


        results.append(
            {

                "Short_Window":
                    short_window,

                "Long_Window":
                    long_window,

                "RSI_Threshold":
                    rsi_threshold,

                "Training_Return":
                    score
            }
        )


    results_df = pd.DataFrame(
        results
    )


    results_df = (
        results_df
        .sort_values(
            "Training_Return",
            ascending=False
        )
        .reset_index(drop=True)
    )


    if results_df.empty:

        raise ValueError(
            "\nNo valid parameter combinations "
            "were available."
        )


    best = (
        results_df.iloc[0]
    )


    return (

        int(
            best["Short_Window"]
        ),

        int(
            best["Long_Window"]
        ),

        int(
            best["RSI_Threshold"]
        ),

        results_df
    )


# ============================================================
# 17. 80/20 CHRONOLOGICAL SPLIT
# ============================================================
#
# IMPORTANT:
#
# Split the PRICE dataset first.
#
# The returns are then selected by DATE.
#
# This avoids the one-observation shift created by pct_change().
# ============================================================

split_index = int(
    len(prices)
    *
    (1 - FINAL_TEST_FRACTION)
)


development_prices = (
    prices.iloc[
        :split_index
    ]
    .copy()
)


final_test_prices = (
    prices.iloc[
        split_index:
    ]
    .copy()
)


development_returns = (
    returns.loc[
        returns.index
        <= development_prices.index[-1]
    ]
    .copy()
)


final_test_returns = (
    returns.loc[
        returns.index
        >= final_test_prices.index[0]
    ]
    .copy()
)


print(
    "\n" + "=" * 70
)

print(
    "80/20 CHRONOLOGICAL DEVELOPMENT / FINAL TEST SPLIT"
)

print(
    "=" * 70
)


print(
    "\nDevelopment price observations:"
)

print(
    len(development_prices)
)


print(
    "Final test price observations:"
)

print(
    len(final_test_prices)
)


print(
    "\nDevelopment period:"
)

print(
    development_prices.index.min(),
    "to",
    development_prices.index.max()
)


print(
    "\nFinal unseen test period:"
)

print(
    final_test_prices.index.min(),
    "to",
    final_test_prices.index.max()
)


# ============================================================
# 18. DEVELOPMENT PARAMETER OPTIMISATION
# ============================================================

(
    best_short,
    best_long,
    best_rsi,
    parameter_search
) = optimise_parameters(
    development_prices
)


print(
    "\n" + "=" * 70
)

print(
    "DEVELOPMENT PARAMETER OPTIMISATION"
)

print(
    "=" * 70
)


print(
    "\nNumber of parameter combinations tested:"
)

print(
    len(parameter_search)
)


print(
    "\nBest parameters:"
)

print(
    "Short window:",
    best_short
)

print(
    "Long window:",
    best_long
)

print(
    "RSI threshold:",
    best_rsi
)


print(
    "\nBest development return:"
)

print(
    f"{parameter_search.iloc[0]['Training_Return']:.4%}"
)


# ============================================================
# 19. GENERAL FIXED STRATEGY
# ============================================================
#
# These parameters are selected once from the development
# period and then treated as FIXED.
# ============================================================

fixed_portfolio_returns, \
fixed_asset_strategy_returns, \
fixed_asset_signals = (
    generate_portfolio_strategy(
        prices,
        best_short,
        best_long,
        best_rsi
    )
)


# ============================================================
# 20. FINAL TEST WITH WARM-UP
# ============================================================
#
# The final test remains unseen.
#
# We only carry historical observations forward to allow
# SMA and RSI calculations to initialise.
# ============================================================

final_test_lookback = max(
    best_long,
    best_short,
    14
)


warmup_start = max(
    0,
    split_index -
    final_test_lookback
)


final_test_input = (
    prices.iloc[
        warmup_start:
    ]
    .copy()
)


final_test_strategy_all, \
_, _ = (
    generate_portfolio_strategy(
        final_test_input,
        best_short,
        best_long,
        best_rsi
    )
)


final_test_strategy = (
    final_test_strategy_all
    .loc[
        final_test_prices.index
    ]
)


# ============================================================
# 21. FINAL TEST FROZEN PORTFOLIO BUY & HOLD
# ============================================================

final_test_bh = (
    final_test_returns[
        ASSETS
    ]
    .mul(
        WEIGHTS,
        axis=1
    )
    .sum(axis=1)
)


final_test_bh.name = (
    "Frozen_Portfolio_Buy_Hold"
)


# ============================================================
# 22. FINAL TEST RESULTS
# ============================================================

final_fixed_metrics = (
    evaluate_returns(
        final_test_strategy
    )
)


final_bh_metrics = (
    evaluate_returns(
        final_test_bh
    )
)


final_test_comparison = (
    pd.DataFrame(
        [
            final_fixed_metrics,
            final_bh_metrics
        ],
        index=[
            "General Fixed Trading Strategy",
            "Frozen Portfolio Buy & Hold"
        ]
    )
)


print(
    "\n" + "=" * 70
)

print(
    "FINAL UNSEEN TEST — GENERAL FIXED STRATEGY"
)

print(
    "=" * 70
)


print(
    final_test_comparison.to_string()
)


# ============================================================
# 23. EXPANDING WALK-FORWARD VALIDATION
# ============================================================
#
# Training window:
#
#     grows over time
#
# Test window:
#
#     30 observations
#
# Parameters are selected using training data ONLY.
# ============================================================

print(
    "\n" + "=" * 70
)

print(
    "EXPANDING WALK-FORWARD VALIDATION"
)

print(
    "=" * 70
)


expanding_results = []

parameter_history_expanding = []


start = TRAIN_SIZE


while (
    start + TEST_SIZE
    <= len(development_prices)
):


    train_end = start

    test_end = (
        start +
        TEST_SIZE
    )


    train_prices = (
        development_prices.iloc[
            :train_end
        ]
        .copy()
    )


    test_prices = (
        development_prices.iloc[
            train_end:test_end
        ]
        .copy()
    )


    # --------------------------------------------------------
    # Optimise ONLY on historical training observations
    # --------------------------------------------------------

    (
        opt_short,
        opt_long,
        opt_rsi,
        search_results
    ) = optimise_parameters(
        train_prices
    )


    # --------------------------------------------------------
    # Optimised strategy
    # --------------------------------------------------------

    optimized_lookback = max(
        opt_long,
        opt_short,
        14
    )


    optimized_input = pd.concat(
        [
            train_prices.tail(
                optimized_lookback
            ),
            test_prices
        ]
    )


    optimized_all, _, _ = (
        generate_portfolio_strategy(
            optimized_input,
            opt_short,
            opt_long,
            opt_rsi
        )
    )


    optimized_test = (
        optimized_all
        .loc[
            test_prices.index
        ]
    )


    # --------------------------------------------------------
    # Fixed strategy
    # --------------------------------------------------------

    fixed_lookback = max(
        best_long,
        best_short,
        14
    )


    fixed_input = pd.concat(
        [
            train_prices.tail(
                fixed_lookback
            ),
            test_prices
        ]
    )


    fixed_all, _, _ = (
        generate_portfolio_strategy(
            fixed_input,
            best_short,
            best_long,
            best_rsi
        )
    )


    fixed_test = (
        fixed_all
        .loc[
            test_prices.index
        ]
    )


    # --------------------------------------------------------
    # Buy & Hold benchmark
    # --------------------------------------------------------

    bh_test = (
        returns.loc[
            test_prices.index,
            ASSETS
        ]
        .mul(
            WEIGHTS,
            axis=1
        )
        .sum(axis=1)
    )


    # --------------------------------------------------------
    # Store results
    # --------------------------------------------------------

    expanding_results.append(
        {

            "Test_Start":
                test_prices.index.min(),

            "Test_End":
                test_prices.index.max(),

            "Optimized_Return":
                total_return(
                    optimized_test
                ),

            "Fixed_Return":
                total_return(
                    fixed_test
                ),

            "Buy_Hold_Return":
                total_return(
                    bh_test
                ),

            "Optimized_Short":
                opt_short,

            "Optimized_Long":
                opt_long,

            "Optimized_RSI":
                opt_rsi
        }
    )


    parameter_history_expanding.append(
        {

            "Test_Start":
                test_prices.index.min(),

            "Test_End":
                test_prices.index.max(),

            "Short_Window":
                opt_short,

            "Long_Window":
                opt_long,

            "RSI_Threshold":
                opt_rsi
        }
    )


    start += TEST_SIZE


expanding_results_df = (
    pd.DataFrame(
        expanding_results
    )
)


parameter_history_expanding_df = (
    pd.DataFrame(
        parameter_history_expanding
    )
)


# ============================================================
# 24. EXPANDING WALK-FORWARD SUMMARY
# ============================================================

if not expanding_results_df.empty:

    expanding_summary = pd.DataFrame(

        {

            "Average Return":
            [

                expanding_results_df[
                    "Optimized_Return"
                ].mean(),

                expanding_results_df[
                    "Fixed_Return"
                ].mean(),

                expanding_results_df[
                    "Buy_Hold_Return"
                ].mean()
            ],

            "Total Compounded Return":
            [

                (
                    1 +
                    expanding_results_df[
                        "Optimized_Return"
                    ]
                ).prod()
                - 1,

                (
                    1 +
                    expanding_results_df[
                        "Fixed_Return"
                    ]
                ).prod()
                - 1,

                (
                    1 +
                    expanding_results_df[
                        "Buy_Hold_Return"
                    ]
                ).prod()
                - 1
            ]
        },

        index=[
            "Optimized",
            "Fixed",
            "Buy & Hold"
        ]
    )

else:

    expanding_summary = (
        pd.DataFrame()
    )


print(
    "\nExpanding walk-forward results:"
)

print(
    expanding_results_df.to_string(
        index=False
    )
)


print(
    "\nExpanding walk-forward summary:"
)

print(
    expanding_summary.to_string()
)


# ============================================================
# 25. EXPANDING PARAMETER STABILITY
# ============================================================

if not parameter_history_expanding_df.empty:

    print(
        "\nExpanding parameter history:"
    )

    print(
        parameter_history_expanding_df
        .to_string(
            index=False
        )
    )


    print(
        "\nExpanding parameter selection frequency:"
    )

    print(
        parameter_history_expanding_df[
            [
                "Short_Window",
                "Long_Window",
                "RSI_Threshold"
            ]
        ]
        .value_counts()
        .to_string()
    )


# ============================================================
# 26. EXPANDING ROBUSTNESS
# ============================================================

if not expanding_results_df.empty:

    expanding_difference = (
        expanding_results_df[
            "Optimized_Return"
        ]
        -
        expanding_results_df[
            "Fixed_Return"
        ]
    )


    expanding_mean_difference = (
        expanding_difference.mean()
    )


    expanding_std_difference = (
        expanding_difference.std(
            ddof=1
        )
    )


    expanding_n = (
        expanding_difference.count()
    )


    if (
        expanding_std_difference != 0
        and expanding_n > 1
    ):

        expanding_t_stat = (
            expanding_mean_difference
            /
            (
                expanding_std_difference
                /
                np.sqrt(expanding_n)
            )
        )

    else:

        expanding_t_stat = np.nan


    expanding_robustness = (
        pd.DataFrame(
            {
                "Metric":
                [

                    "Average Optimized - Fixed",

                    "Std Dev Difference",

                    "T-statistic",

                    "Optimized Wins"
                ],

                "Value":
                [

                    expanding_mean_difference,

                    expanding_std_difference,

                    expanding_t_stat,

                    (
                        expanding_difference
                        > 0
                    ).sum()
                ]
            }
        )
    )

else:

    expanding_robustness = (
        pd.DataFrame()
    )


print(
    "\nExpanding robustness:"
)

print(
    expanding_robustness.to_string(
        index=False
    )
)


# ============================================================
# 27. REGIME CLASSIFICATION
# ============================================================
#
# Regime classification is performed on the DEVELOPMENT
# period only.
#
# This keeps the final 20% genuinely unseen.
#
# Regimes:
#
#     Bull_LowVol
#     Bull_HighVol
#     Bear_LowVol
#     Bear_HighVol
#
# Trend:
#
#     SMA20 > SMA50 = Bull
#     SMA20 < SMA50 = Bear
#
# Volatility:
#
#     rolling 20-day volatility compared with its
#     historical expanding median.
# ============================================================

def classify_regime(
    price_series,
    short_window=20,
    long_window=50
):

    sma_short = (
        price_series
        .rolling(
            short_window
        )
        .mean()
    )


    sma_long = (
        price_series
        .rolling(
            long_window
        )
        .mean()
    )


    volatility = (
        price_series
        .pct_change()
        .rolling(20)
        .std()
    )


    volatility_median = (
        volatility
        .expanding()
        .median()
    )


    regime = pd.Series(
        index=price_series.index,
        dtype="object"
    )


    bull = (
        sma_short >
        sma_long
    )


    bear = (
        sma_short <
        sma_long
    )


    high_volatility = (
        volatility >
        volatility_median
    )


    regime.loc[
        bull &
        high_volatility
    ] = "Bull_HighVol"


    regime.loc[
        bull &
        ~high_volatility
    ] = "Bull_LowVol"


    regime.loc[
        bear &
        high_volatility
    ] = "Bear_HighVol"


    regime.loc[
        bear &
        ~high_volatility
    ] = "Bear_LowVol"


    return regime


# ============================================================
# 28. DEVELOPMENT WEIGHTED PRICE PROXY
# ============================================================
#
# This is NOT a new portfolio.
#
# It is simply a weighted price proxy used for regime
# classification.
# ============================================================

weighted_price = (
    prices[
        ASSETS
    ]
    .mul(
        WEIGHTS,
        axis=1
    )
    .sum(axis=1)
)


development_weighted_price = (
    weighted_price
    .loc[
        development_prices.index
    ]
)


regime_series = (
    classify_regime(
        development_weighted_price,
        short_window=20,
        long_window=50
    )
)


# ============================================================
# 29. REGIME ROBUSTNESS
# ============================================================

development_fixed_returns = (
    fixed_portfolio_returns
    .reindex(
        development_prices.index
    )
)


development_bh_returns = (
    portfolio_bh_returns
    .reindex(
        development_prices.index
    )
)

regime_records = []


for regime_name in [

    "Bull_LowVol",

    "Bull_HighVol",

    "Bear_LowVol",

    "Bear_HighVol"
]:

    mask = (
        regime_series ==
        regime_name
    )


    strategy_regime = (
        development_fixed_returns[
            mask
        ]
        .dropna()
    )


    bh_regime = (
        development_bh_returns[
            mask
        ]
        .dropna()
    )


    if len(strategy_regime) == 0:
        continue


    regime_records.append(
        {

            "Regime":
                regime_name,

            "Observations":
                len(strategy_regime),

            "Strategy_Return":
                total_return(
                    strategy_regime
                ),

            "Strategy_Volatility":
                annualised_volatility(
                    strategy_regime
                ),

            "Strategy_Sharpe":
                sharpe_ratio(
                    strategy_regime
                ),

            "Strategy_Max_Drawdown":
                maximum_drawdown(
                    strategy_regime
                ),

            "Buy_Hold_Return":
                total_return(
                    bh_regime
                )
        }
    )


regime_results_df = (
    pd.DataFrame(
        regime_records
    )
)


print(
    "\n" + "=" * 70
)

print(
    "REGIME ROBUSTNESS — DEVELOPMENT PERIOD"
)

print(
    "=" * 70
)


if not regime_results_df.empty:

    print(
        regime_results_df.to_string(
            index=False
        )
    )

else:

    print(
        "\nNo valid regime observations."
    )


# ============================================================
# 30. PARAMETER SENSITIVITY
# ============================================================
#
# Sensitivity is performed on DEVELOPMENT data only.
#
# RSI is held at 70 while SMA parameters vary.
# ============================================================

sensitivity_records = []


for (
    short_window,
    long_window
) in product(
    SENSITIVITY_SHORT_VALUES,
    SENSITIVITY_LONG_VALUES
):


    if short_window >= long_window:
        continue


    strategy_returns, _, _ = (
        generate_portfolio_strategy(
            development_prices,
            short_window,
            long_window,
            SENSITIVITY_RSI
        )
    )


    sensitivity_records.append(
        {

            "Short_Window":
                short_window,

            "Long_Window":
                long_window,

            "RSI_Threshold":
                SENSITIVITY_RSI,

            "Return":
                total_return(
                    strategy_returns
                ),

            "Volatility":
                annualised_volatility(
                    strategy_returns
                ),

            "Sharpe":
                sharpe_ratio(
                    strategy_returns
                ),

            "Max_Drawdown":
                maximum_drawdown(
                    strategy_returns
                )
        }
    )


sensitivity_df = (
    pd.DataFrame(
        sensitivity_records
    )
)


print(
    "\n" + "=" * 70
)

print(
    "PARAMETER SENSITIVITY — DEVELOPMENT PERIOD"
)

print(
    "=" * 70
)


print(
    sensitivity_df
    .sort_values(
        "Return",
        ascending=False
    )
    .head(20)
    .to_string(
        index=False
    )
)


# ============================================================
# 31. ROLLING WALK-FORWARD VALIDATION
# ============================================================
#
# Unlike expanding validation:
#
# The training window stays fixed at 100 observations.
#
# Example:
#
# Window 1:
#     Train = observations 1–100
#     Test  = 101–130
#
# Window 2:
#     Train = observations 31–130
#     Test  = 131–160
#
# etc.
# ============================================================

print(
    "\n" + "=" * 70
)

print(
    "ROLLING WALK-FORWARD VALIDATION"
)

print(
    "=" * 70
)


rolling_results = []

parameter_history_rolling = []


for start in range(

    0,

    len(development_prices)
    -
    TRAIN_SIZE
    -
    TEST_SIZE
    + 1,

    TEST_SIZE
):


    train_start = start


    train_end = (
        start +
        TRAIN_SIZE
    )


    test_end = (
        train_end +
        TEST_SIZE
    )


    train_prices = (
        development_prices.iloc[
            train_start:train_end
        ]
        .copy()
    )


    test_prices = (
        development_prices.iloc[
            train_end:test_end
        ]
        .copy()
    )


    # --------------------------------------------------------
    # Optimise ONLY on rolling training window
    # --------------------------------------------------------

    (
        opt_short,
        opt_long,
        opt_rsi,
        search_results
    ) = optimise_parameters(
        train_prices
    )


    # --------------------------------------------------------
    # Optimized strategy
    # --------------------------------------------------------

    optimized_lookback = max(
        opt_long,
        opt_short,
        14
    )


    optimized_input = pd.concat(
        [
            train_prices.tail(
                optimized_lookback
            ),
            test_prices
        ]
    )


    optimized_all, _, _ = (
        generate_portfolio_strategy(
            optimized_input,
            opt_short,
            opt_long,
            opt_rsi
        )
    )


    optimized_test = (
        optimized_all
        .loc[
            test_prices.index
        ]
    )


    # --------------------------------------------------------
    # Fixed strategy
    # --------------------------------------------------------

    fixed_lookback = max(
        best_long,
        best_short,
        14
    )


    fixed_input = pd.concat(
        [
            train_prices.tail(
                fixed_lookback
            ),
            test_prices
        ]
    )


    fixed_all, _, _ = (
        generate_portfolio_strategy(
            fixed_input,
            best_short,
            best_long,
            best_rsi
        )
    )


    fixed_test = (
        fixed_all
        .loc[
            test_prices.index
        ]
    )


    # --------------------------------------------------------
    # Buy & Hold
    # --------------------------------------------------------

    bh_test = (
        returns.loc[
            test_prices.index,
            ASSETS
        ]
        .mul(
            WEIGHTS,
            axis=1
        )
        .sum(axis=1)
    )


    # --------------------------------------------------------
    # Store
    # --------------------------------------------------------

    rolling_results.append(
        {

            "Test_Start":
                test_prices.index.min(),

            "Test_End":
                test_prices.index.max(),

            "Optimized_Return":
                total_return(
                    optimized_test
                ),

            "Fixed_Return":
                total_return(
                    fixed_test
                ),

            "Buy_Hold_Return":
                total_return(
                    bh_test
                ),

            "Optimized_Short":
                opt_short,

            "Optimized_Long":
                opt_long,

            "Optimized_RSI":
                opt_rsi
        }
    )


    parameter_history_rolling.append(
        {

            "Test_Start":
                test_prices.index.min(),

            "Test_End":
                test_prices.index.max(),

            "Short_Window":
                opt_short,

            "Long_Window":
                opt_long,

            "RSI_Threshold":
                opt_rsi
        }
    )


rolling_results_df = (
    pd.DataFrame(
        rolling_results
    )
)


parameter_history_rolling_df = (
    pd.DataFrame(
        parameter_history_rolling
    )
)


# ============================================================
# 32. ROLLING WALK-FORWARD SUMMARY
# ============================================================

if not rolling_results_df.empty:

    rolling_summary = pd.DataFrame(

        {

            "Average Return":
            [

                rolling_results_df[
                    "Optimized_Return"
                ].mean(),

                rolling_results_df[
                    "Fixed_Return"
                ].mean(),

                rolling_results_df[
                    "Buy_Hold_Return"
                ].mean()
            ],

            "Total Compounded Return":
            [

                (
                    1 +
                    rolling_results_df[
                        "Optimized_Return"
                    ]
                ).prod()
                - 1,

                (
                    1 +
                    rolling_results_df[
                        "Fixed_Return"
                    ]
                ).prod()
                - 1,

                (
                    1 +
                    rolling_results_df[
                        "Buy_Hold_Return"
                    ]
                ).prod()
                - 1
            ]
        },

        index=[
            "Optimized",
            "Fixed",
            "Buy & Hold"
        ]
    )

else:

    rolling_summary = (
        pd.DataFrame()
    )


print(
    "\nRolling walk-forward results:"
)

print(
    rolling_results_df.to_string(
        index=False
    )
)


print(
    "\nRolling walk-forward summary:"
)

print(
    rolling_summary.to_string()
)


# ============================================================
# 33. ROLLING PARAMETER STABILITY
# ============================================================

if not parameter_history_rolling_df.empty:

    print(
        "\nRolling parameter history:"
    )

    print(
        parameter_history_rolling_df
        .to_string(
            index=False
        )
    )


    print(
        "\nRolling parameter selection frequency:"
    )

    print(
        parameter_history_rolling_df[
            [
                "Short_Window",
                "Long_Window",
                "RSI_Threshold"
            ]
        ]
        .value_counts()
        .to_string()
    )


# ============================================================
# 34. ROLLING ROBUSTNESS
# ============================================================

if not rolling_results_df.empty:

    rolling_difference = (
        rolling_results_df[
            "Optimized_Return"
        ]
        -
        rolling_results_df[
            "Fixed_Return"
        ]
    )


    rolling_mean_difference = (
        rolling_difference.mean()
    )


    rolling_std_difference = (
        rolling_difference.std(
            ddof=1
        )
    )


    rolling_n = (
        rolling_difference.count()
    )


    if (
        rolling_std_difference != 0
        and rolling_n > 1
    ):

        rolling_t_stat = (
            rolling_mean_difference
            /
            (
                rolling_std_difference
                /
                np.sqrt(rolling_n)
            )
        )

    else:

        rolling_t_stat = np.nan


    rolling_robustness = (
        pd.DataFrame(
            {

                "Metric":
                [

                    "Average Optimized - Fixed",

                    "Std Dev Difference",

                    "T-statistic",

                    "Optimized Wins"
                ],

                "Value":
                [

                    rolling_mean_difference,

                    rolling_std_difference,

                    rolling_t_stat,

                    (
                        rolling_difference
                        > 0
                    ).sum()
                ]
            }
        )
    )

else:

    rolling_robustness = (
        pd.DataFrame()
    )


print(
    "\nRolling robustness:"
)

print(
    rolling_robustness.to_string(
        index=False
    )
)


# ============================================================
# 35. ASSET-LEVEL SIGNAL DIAGNOSTICS
# ============================================================
#
# These diagnostics use the general fixed parameters selected
# from the development period.
# ============================================================

(
    fixed_portfolio_returns,
    fixed_asset_strategy_returns,
    fixed_asset_signals
) = generate_portfolio_strategy(

    prices,

    best_short,

    best_long,

    best_rsi
)


signal_statistics = []


for asset in ASSETS:

    signal = (
        fixed_asset_signals[
            asset
        ]
        .dropna()
    )


    signal_statistics.append(
        {

            "Asset":
                asset,

            "Frozen_Weight":
                WEIGHTS[
                    asset
                ],

            "Average_Signal":
                signal.mean(),

            "Signal_1_Days":
                int(
                    signal.sum()
                ),

            "Signal_0_Days":
                int(
                    (signal == 0)
                    .sum()
                ),

            "Invested_Percentage":
                signal.mean()
        }
    )


signal_statistics_df = (
    pd.DataFrame(
        signal_statistics
    )
)


print(
    "\n" + "=" * 70
)

print(
    "ASSET-LEVEL SIGNAL DIAGNOSTICS"
)

print(
    "=" * 70
)


print(
    signal_statistics_df.to_string(
        index=False
    )
)


# ============================================================
# 36. ACTIVE EXPOSURE DIAGNOSTICS
# ============================================================
#
# This shows how much of the frozen portfolio is actually
# invested at each point in time.
#
# It does NOT change the frozen portfolio weights.
#
# Example:
#
# AAPL = active
# GOOG = inactive
# META = active
#
# Active exposure =
#
# 0.40 + 0 + 0.20
# =
# 0.60
#
# The remaining 40% is effectively cash.
# ============================================================

active_weight_df = (
    fixed_asset_signals
    .mul(
        WEIGHTS,
        axis=1
    )
)


active_weight_df[
    "Total_Active_Exposure"
] = (
    active_weight_df
    .sum(axis=1)
)


print(
    "\n" + "=" * 70
)

print(
    "ACTIVE PORTFOLIO EXPOSURE"
)

print(
    "=" * 70
)


print(
    "\nAverage active exposure:"
)

print(
    active_weight_df[
        "Total_Active_Exposure"
    ].mean()
)


print(
    "\nMinimum active exposure:"
)

print(
    active_weight_df[
        "Total_Active_Exposure"
    ].min()
)


print(
    "\nMaximum active exposure:"
)

print(
    active_weight_df[
        "Total_Active_Exposure"
    ].max()
)


# ============================================================
# 37. FINAL DEVELOPMENT EXPANDING OPTIMISATION
# ============================================================
#
# The complete 80% development sample is now used.
#
# The final 20% remains untouched.
# ============================================================

(
    final_expanding_short,
    final_expanding_long,
    final_expanding_rsi,
    final_expanding_search
) = optimise_parameters(
    development_prices
)


# ============================================================
# 38. FINAL DEVELOPMENT ROLLING OPTIMISATION
# ============================================================
#
# Only the most recent TRAIN_SIZE observations of the
# development period are used.
# ============================================================

rolling_train_prices = (
    development_prices
    .iloc[
        -TRAIN_SIZE:
    ]
    .copy()
)


(
    final_rolling_short,
    final_rolling_long,
    final_rolling_rsi,
    final_rolling_search
) = optimise_parameters(
    rolling_train_prices
)


# ============================================================
# 39. FINAL EXPANDING OOS STRATEGY
# ============================================================

expanding_final_lookback = max(
    final_expanding_long,
    final_expanding_short,
    14
)


expanding_final_input = pd.concat(
    [

        development_prices.tail(
            expanding_final_lookback
        ),

        final_test_prices
    ]
)


expanding_final_all, _, _ = (
    generate_portfolio_strategy(
        expanding_final_input,

        final_expanding_short,

        final_expanding_long,

        final_expanding_rsi
    )
)


final_expanding_strategy = (
    expanding_final_all
    .loc[
        final_test_prices.index
    ]
)


# ============================================================
# 40. FINAL ROLLING OOS STRATEGY
# ============================================================

rolling_final_lookback = max(
    final_rolling_long,
    final_rolling_short,
    14
)


rolling_final_input = pd.concat(
    [

        rolling_train_prices.tail(
            rolling_final_lookback
        ),

        final_test_prices
    ]
)


rolling_final_all, _, _ = (
    generate_portfolio_strategy(

        rolling_final_input,

        final_rolling_short,

        final_rolling_long,

        final_rolling_rsi
    )
)


final_rolling_strategy = (
    rolling_final_all
    .loc[
        final_test_prices.index
    ]
)


# ============================================================
# 41. FINAL GENERAL FIXED OOS STRATEGY
# ============================================================

general_final_lookback = max(
    best_long,
    best_short,
    14
)


general_final_input = pd.concat(
    [

        development_prices.tail(
            general_final_lookback
        ),

        final_test_prices
    ]
)


general_final_all, _, _ = (
    generate_portfolio_strategy(

        general_final_input,

        best_short,

        best_long,

        best_rsi
    )
)


general_final_strategy = (
    general_final_all
    .loc[
        final_test_prices.index
    ]
)


# ============================================================
# 42. FINAL OOS COMPARISON
# ============================================================

final_oos_results = (
    pd.DataFrame(

        [

            evaluate_returns(
                final_expanding_strategy
            ),

            evaluate_returns(
                final_rolling_strategy
            ),

            evaluate_returns(
                general_final_strategy
            ),

            evaluate_returns(
                final_test_bh
            )
        ],

        index=[

            "Expanding Optimized",

            "Rolling Optimized",

            "General Fixed",

            "Frozen Portfolio Buy & Hold"
        ]
    )
)


print(
    "\n" + "=" * 70
)

print(
    "FINAL UNSEEN OUT-OF-SAMPLE COMPARISON"
)

print(
    "=" * 70
)


print(
    final_oos_results.to_string()
)


print(
    "\nFinal expanding parameters:"
)

print(
    "Short:",
    final_expanding_short,

    "Long:",
    final_expanding_long,

    "RSI:",
    final_expanding_rsi
)


print(
    "\nFinal rolling parameters:"
)

print(
    "Short:",
    final_rolling_short,

    "Long:",
    final_rolling_long,

    "RSI:",
    final_rolling_rsi
)


print(
    "\nGeneral fixed parameters:"
)

print(
    "Short:",
    best_short,

    "Long:",
    best_long,

    "RSI:",
    best_rsi
)


# ============================================================
# 43. FINAL OOS DAILY RETURNS
# ============================================================

final_oos_daily = (
    pd.DataFrame(
        {

            "Expanding_Optimized":
                final_expanding_strategy,

            "Rolling_Optimized":
                final_rolling_strategy,

            "General_Fixed":
                general_final_strategy,

            "Frozen_Portfolio_Buy_Hold":
                final_test_bh
        }
    )
)


# ============================================================
# 44. FINAL OOS RETURN DIFFERENCES
# ============================================================

final_difference = (
    pd.DataFrame(
        {

            "Expanding_vs_BH":
                (
                    final_expanding_strategy
                    -
                    final_test_bh
                ),

            "Rolling_vs_BH":
                (
                    final_rolling_strategy
                    -
                    final_test_bh
                ),

            "General_vs_BH":
                (
                    general_final_strategy
                    -
                    final_test_bh
                ),

            "Expanding_vs_Rolling":
                (
                    final_expanding_strategy
                    -
                    final_rolling_strategy
                )
        }
    )
)


# ============================================================
# 45. FINAL PARAMETER SUMMARY
# ============================================================

final_parameter_summary = (
    pd.DataFrame(
        [

            {

                "Strategy":
                    "Expanding Optimized",

                "Short_Window":
                    final_expanding_short,

                "Long_Window":
                    final_expanding_long,

                "RSI_Threshold":
                    final_expanding_rsi
            },


            {

                "Strategy":
                    "Rolling Optimized",

                "Short_Window":
                    final_rolling_short,

                "Long_Window":
                    final_rolling_long,

                "RSI_Threshold":
                    final_rolling_rsi
            },


            {

                "Strategy":
                    "General Fixed",

                "Short_Window":
                    best_short,

                "Long_Window":
                    best_long,

                "RSI_Threshold":
                    best_rsi
            }
        ]
    )
)


# ============================================================
# 46. OUTPUT DIRECTORY
# ============================================================

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "outputs"
)


os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ============================================================
# 47. SAVE INHERITED PORTFOLIO
# ============================================================

inherited_portfolio_output = (
    frozen_weights
    .rename("Weight")
    .rename_axis("Asset")
    .reset_index()
)


inherited_portfolio_output[
    "Portfolio"
] = TARGET_PORTFOLIO


inherited_portfolio_output = (
    inherited_portfolio_output[
        [
            "Portfolio",
            "Asset",
            "Weight"
        ]
    ]
)


inherited_portfolio_output.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "inherited_frozen_portfolio.csv"
    ),
    index=False
)


# ============================================================
# 48. SAVE ASSET SIGNALS
# ============================================================

fixed_asset_signals.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "asset_trading_signals.csv"
    )
)


# ============================================================
# 49. SAVE ASSET STRATEGY RETURNS
# ============================================================

fixed_asset_strategy_returns.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "asset_strategy_returns.csv"
    )
)


# ============================================================
# 50. SAVE PORTFOLIO DAILY RETURNS
# ============================================================

portfolio_daily_output = (
    pd.DataFrame(
        {

            "Frozen_Portfolio_Buy_Hold":
                portfolio_bh_returns,

            "General_Fixed_Strategy":
                fixed_portfolio_returns
        }
    )
)


portfolio_daily_output.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "portfolio_daily_returns.csv"
    )
)


# ============================================================
# 51. SAVE EXPANDING WALK-FORWARD
# ============================================================

expanding_results_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "expanding_walk_forward_results.csv"
    ),
    index=False
)


parameter_history_expanding_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "expanding_parameter_history.csv"
    ),
    index=False
)


expanding_robustness.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "expanding_robustness.csv"
    ),
    index=False
)


# ============================================================
# 52. SAVE ROLLING WALK-FORWARD
# ============================================================

rolling_results_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "rolling_walk_forward_results.csv"
    ),
    index=False
)


parameter_history_rolling_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "rolling_parameter_history.csv"
    ),
    index=False
)


rolling_robustness.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "rolling_robustness.csv"
    ),
    index=False
)


# ============================================================
# 53. SAVE PARAMETER SENSITIVITY
# ============================================================

sensitivity_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "parameter_sensitivity.csv"
    ),
    index=False
)


# ============================================================
# 54. SAVE REGIME ROBUSTNESS
# ============================================================

regime_results_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "regime_robustness.csv"
    ),
    index=False
)


# ============================================================
# 55. SAVE SIGNAL DIAGNOSTICS
# ============================================================

signal_statistics_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "signal_statistics.csv"
    ),
    index=False
)


active_weight_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "active_weight_diagnostics.csv"
    )
)


# ============================================================
# 56. SAVE FINAL OOS RESULTS
# ============================================================

final_oos_results.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "final_oos_results.csv"
    )
)


final_oos_daily.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "final_oos_daily_returns.csv"
    )
)


final_difference.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "final_oos_return_differences.csv"
    )
)


final_parameter_summary.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "final_parameter_summary.csv"
    ),
    index=False
)


# ============================================================
# 57. SAVE PARAMETER SEARCH
# ============================================================

parameter_search.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "development_parameter_search.csv"
    ),
    index=False
)


final_expanding_search.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "final_expanding_parameter_search.csv"
    ),
    index=False
)


final_rolling_search.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "final_rolling_parameter_search.csv"
    ),
    index=False
)


# ============================================================
# 58. FINAL RISK / PERFORMANCE SUMMARY
# ============================================================

summary_rows = []


for name, series in [

    (
        "Final Expanding Optimized",
        final_expanding_strategy
    ),

    (
        "Final Rolling Optimized",
        final_rolling_strategy
    ),

    (
        "Final General Fixed",
        general_final_strategy
    ),

    (
        "Final Frozen Portfolio Buy & Hold",
        final_test_bh
    )
]:


    metrics = evaluate_returns(
        series
    )


    metrics[
        "Strategy"
    ] = name


    summary_rows.append(
        metrics
    )


risk_summary_df = (
    pd.DataFrame(
        summary_rows
    )
)


risk_summary_df = (
    risk_summary_df
    .set_index(
        "Strategy"
    )
)


risk_summary_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "risk_performance_summary.csv"
    )
)



# ============================================================
# 61. FINAL VALIDATION MESSAGE
# ============================================================

print(
    "\n" + "=" * 70
)

print(
    "PROJECT 03 COMPLETE"
)

print(
    "=" * 70
)


print(
    "\nProject 01 portfolio inherited:"
)


for asset in ASSETS:

    print(
        f"  {asset}: "
        f"{WEIGHTS[asset]:.2%}"
    )


print(
    "\nPortfolio weights were NOT redefined."
)


print(
    "Portfolio weights were NOT optimised."
)


print(
    "Asset selection was NOT performed by Project 03."
)


print(
    "\nTrading parameters were optimised "
    "independently of portfolio construction."
)


print(
    "\nFinal test observations were kept "
    "outside parameter selection."
)


print(
    "\nFinal output directory:"
)


print(
    OUTPUT_DIR
)


print(
    "\nKey files created:"
)


for filename in [

    "inherited_frozen_portfolio.csv",

    "asset_trading_signals.csv",

    "asset_strategy_returns.csv",

    "portfolio_daily_returns.csv",

    "expanding_walk_forward_results.csv",

    "expanding_parameter_history.csv",

    "expanding_robustness.csv",

    "rolling_walk_forward_results.csv",

    "rolling_parameter_history.csv",

    "rolling_robustness.csv",

    "parameter_sensitivity.csv",

    "regime_robustness.csv",

    "signal_statistics.csv",

    "active_weight_diagnostics.csv",

    "final_oos_results.csv",

    "final_oos_daily_returns.csv",

    "final_oos_return_differences.csv",

    "final_parameter_summary.csv",

    "development_parameter_search.csv",

    "final_expanding_parameter_search.csv",

    "final_rolling_parameter_search.csv",

    "risk_performance_summary.csv"

]:

    print(
        "  " + filename
    )


print(
    "\nNo final-test observations were used "
    "for parameter selection."
)


print(
    "\nProject 03 systematic trading research "
    "pipeline finished successfully."
)


# ============================================================
# 59. FINAL OOS EQUITY CURVES
# ============================================================
import matplotlib.pyplot as plt

final_equity = (
    1 +
    final_oos_daily
).cumprod()


plt.figure(
    figsize=(12, 6)
)


for column in final_equity.columns:

    plt.plot(
        final_equity.index,
        final_equity[column],
        label=column
    )


plt.title(
    "Project 03 — Final Unseen OOS Equity Curves"
)


plt.xlabel(
    "Date"
)


plt.ylabel(
    "Growth of $1"
)


plt.legend()


plt.grid(
    alpha=0.3
)


plt.tight_layout()


plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "final_oos_equity_curves.png"
    ),
    dpi=150
)


plt.show()


# ============================================================
# 60. PARAMETER SENSITIVITY HEATMAP
# ============================================================

if not sensitivity_df.empty:

    heatmap_data = (
        sensitivity_df
        .pivot_table(
            index="Short_Window",
            columns="Long_Window",
            values="Return"
        )
    )


    plt.figure(
        figsize=(10, 7)
    )


    plt.imshow(
        heatmap_data,
        aspect="auto"
    )


    plt.xticks(
        range(
            len(
                heatmap_data.columns
            )
        ),
        heatmap_data.columns
    )


    plt.yticks(
        range(
            len(
                heatmap_data.index
            )
        ),
        heatmap_data.index
    )


    plt.colorbar(
        label="Development Return"
    )


    plt.title(
        "Project 03 — SMA Parameter Sensitivity"
    )


    plt.xlabel(
        "Long Window"
    )


    plt.ylabel(
        "Short Window"
    )


    plt.tight_layout()


    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "parameter_sensitivity_heatmap.png"
        ),
        dpi=150
    )


    plt.show()