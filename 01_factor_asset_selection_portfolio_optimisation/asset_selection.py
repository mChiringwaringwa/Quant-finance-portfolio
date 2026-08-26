# ============================================================
# PROJECT 01
# FACTOR-BASED ASSET SELECTION & ROBUST PORTFOLIO OPTIMIZATION
# ============================================================
#
# OBJECTIVE
# ------------------------------------------------------------
# Build a systematic quantitative asset-selection and portfolio
# construction framework.
#
# The project:
#   1. Cleans and aligns market data
#   2. Constructs quantitative factors
#   3. Ranks and selects assets
#   4. Optimizes factor lookback parameters
#   5. Tests parameter robustness
#   6. Selects a final three-asset universe
#   7. Performs constrained portfolio optimization
#   8. Uses equal weight as a benchmark
#   9. Uses the Max-40 constrained portfolio as the alternative
#  10. Freezes the portfolio specifications
#  11. Tests them on a genuinely unseen period
#  12. Performs transaction-cost sensitivity
#  13. Saves reusable outputs for Project 02

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

RISK_FREE_RATE = 0.0

FINAL_TEST_FRACTION = 0.20

INNER_VALIDATION_FRACTION = 0.20

TOP_N_ASSETS = 3

TRANSACTION_COSTS = [
    0.0000,     # 0 bps
    0.0010,     # 10 bps
    0.0025,     # 25 bps
    0.0050      # 50 bps
]


# ============================================================
# 3. DATA AND OUTPUT PATHS
# ============================================================

DATA_PATH = "../data"

OUTPUT_PATH = "../outputs"

os.makedirs(
    OUTPUT_PATH,
    exist_ok=True
)


# ============================================================
# 4. LOAD PRICE CSV
# ============================================================

def load_price_csv(
    ticker,
    path
):
    """
    Load a single ticker CSV and return a clean price Series.

    The function automatically identifies:
        - Date column
        - Close column
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
    # Identify Date column
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

    df = (
        df
        .set_index(date_column)
        .sort_index()
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
# 5. LOAD ALL MARKET DATA
# ============================================================

print(
    "\n" + "=" * 70
)

print(
    "LOADING RAW MARKET DATA"
)

print(
    "=" * 70
)


all_tickers = (
    ASSETS
    + [BENCHMARK]
)


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
# 6. ALIGN ASSET UNIVERSE
# ============================================================

asset_universe = (
    pd.concat(
        price_series,
        axis=1,
        join="inner"
    )
    .sort_index()
    .dropna()
)


print(
    "\n--- CLEANED ASSET UNIVERSE ---"
)

print(
    "Start:",
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
# 7. SAVE CLEANED PRICE DATA
# ============================================================
#
# This is the first reusable output from Project 01.
#
# Project 02 will read this file instead of loading and
# cleaning the original raw CSV files.
# ============================================================

processed_prices_path = os.path.join(
    OUTPUT_PATH,
    "processed_prices.csv"
)

asset_universe.to_csv(
    processed_prices_path
)

print(
    "\nProcessed prices saved to:",
    processed_prices_path
)


# ============================================================
# 8. CALCULATE RETURNS
# ============================================================

returns = (
    asset_universe
    .pct_change()
    .dropna()
)


# ============================================================
# 9. OUTER DEVELOPMENT / FINAL TEST SPLIT
# ============================================================
#
# 80% Development
# 20% Final Unseen Test
#
# The final test period is not used during model development.
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
    "\n" + "=" * 70
)

print(
    "OUTER DEVELOPMENT / FINAL TEST SPLIT"
)

print(
    "=" * 70
)

print(
    "\nDevelopment:"
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
    "\nFinal unseen test:"
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
# 10. CHRONOLOGY CHECK
# ============================================================

development_end = (
    development_df.index.max()
)

final_test_start = (
    final_test_df.index.min()
)


if not (
    development_end
    < final_test_start
):

    raise ValueError(
        "Development and final test periods overlap."
    )


print(
    "\nChronology check: PASSED"
)


# ============================================================
# 11. FACTOR SNAPSHOT FUNCTION
# ============================================================

def calculate_factor_snapshot(
    price_df,
    beta_window=60,
    momentum_window=60,
    volatility_window=20,
    sharpe_window=60
):
    """
    Calculate the latest factor values for every candidate asset.

    Factors:
        Beta
        Momentum
        Volatility
        Sharpe Ratio
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


    snapshot["Beta"] = (
        pd.Series(beta_values)
    )


    # --------------------------------------------------------
    # Momentum
    # --------------------------------------------------------

    snapshot["Momentum"] = (
        asset_prices
        .pct_change(momentum_window)
        .iloc[-1]
    )


    # --------------------------------------------------------
    # Annualized Volatility
    # --------------------------------------------------------

    snapshot["Volatility"] = (
        asset_returns
        .rolling(volatility_window)
        .std()
        .iloc[-1]
        * np.sqrt(TRADING_DAYS)
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

    snapshot["Sharpe"] = (
        rolling_mean
        / rolling_std
        * np.sqrt(TRADING_DAYS)
    )


    return snapshot


# ============================================================
# 12. FACTOR RANKING FUNCTION
# ============================================================

def rank_and_select_assets(
    snapshot
):
    """
    Rank candidate assets using four equally weighted factors.

    Higher score is better.

        Lower Beta       -> better
        Higher Momentum  -> better
        Lower Volatility -> better
        Higher Sharpe    -> better
    """

    ranking = (
        snapshot
        .copy()
    )


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
            pct=True,
            ascending=True
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
            pct=True,
            ascending=True
        )
    )


    ranking["Asset_Score"] = (
        0.25 * ranking["Beta_Score"]
        + 0.25 * ranking["Momentum_Score"]
        + 0.25 * ranking["Volatility_Score"]
        + 0.25 * ranking["Sharpe_Score"]
    )


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
# 13. DEVELOPMENT FACTOR SNAPSHOT
# ============================================================

development_snapshot = (
    calculate_factor_snapshot(
        development_df
    )
)


development_ranking, development_selected_assets = (
    rank_and_select_assets(
        development_snapshot
    )
)


print(
    "\n" + "=" * 70
)

print(
    "DEVELOPMENT FACTOR SNAPSHOT"
)

print(
    "=" * 70
)

print(
    development_snapshot
)


print(
    "\n--- DEVELOPMENT ASSET RANKING ---"
)

print(
    development_ranking
)


print(
    "\nSelected assets:",
    development_selected_assets
)


# ============================================================
# 14. DEVELOPMENT COVARIANCE MATRIX
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


development_correlation = (
    development_asset_returns
    .corr()
)


# ============================================================
# 15. INNER DEVELOPMENT SPLIT
# ============================================================
#
# Development:
#
#     80% Optimization Train
#     20% Validation
#
# The final test remains completely untouched.
# ============================================================

inner_split = int(
    len(development_df)
    * (1 - INNER_VALIDATION_FRACTION)
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
    "\n" + "=" * 70
)

print(
    "INNER DEVELOPMENT SPLIT"
)

print(
    "=" * 70
)

print(
    "\nOptimization train:"
)

print(
    optimization_train_df.index.min(),
    "to",
    optimization_train_df.index.max()
)


print(
    "\nValidation:"
)

print(
    optimization_validation_df.index.min(),
    "to",
    optimization_validation_df.index.max()
)


# ============================================================
# 16. HYPERPARAMETER GRID
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
    "\nParameter combinations:",
    len(parameter_grid)
)


# ============================================================
# 17. HYPERPARAMETER OPTIMIZATION
# ============================================================

optimization_results = []


for (
    beta_window,
    momentum_window,
    volatility_window,
    sharpe_window
) in parameter_grid:


    snapshot = calculate_factor_snapshot(
        optimization_train_df,

        beta_window=beta_window,

        momentum_window=momentum_window,

        volatility_window=volatility_window,

        sharpe_window=sharpe_window
    )


    ranking, selected_assets = (
        rank_and_select_assets(
            snapshot
        )
    )


    validation_returns = (
        optimization_validation_df[
            selected_assets
        ]
        .pct_change()
        .dropna()
    )


    weights = np.repeat(
        1 / len(selected_assets),
        len(selected_assets)
    )


    portfolio_returns = (
        validation_returns
        .dot(weights)
    )


    total_return = (
        (1 + portfolio_returns)
        .prod()
        - 1
    )


    annualized_volatility = (
        portfolio_returns.std()
        * np.sqrt(TRADING_DAYS)
    )


    annualized_return = (
        portfolio_returns.mean()
        * TRADING_DAYS
    )


    if annualized_volatility != 0:

        sharpe_ratio = (
            annualized_return
            - RISK_FREE_RATE
        ) / annualized_volatility

    else:

        sharpe_ratio = np.nan


    optimization_results.append({

        "Beta_Window":
            beta_window,

        "Momentum_Window":
            momentum_window,

        "Volatility_Window":
            volatility_window,

        "Sharpe_Window":
            sharpe_window,

        "Selected_Assets":
            selected_assets,

        "Validation_Return":
            total_return,

        "Validation_Volatility":
            annualized_volatility,

        "Validation_Sharpe":
            sharpe_ratio

    })


optimization_results_df = (
    pd.DataFrame(
        optimization_results
    )
)


optimization_results_df = (
    optimization_results_df
    .sort_values(
        "Validation_Sharpe",
        ascending=False
    )
    .reset_index(drop=True)
)


# ============================================================
# 18. PARAMETER ROBUSTNESS
# ============================================================

optimization_results_df[
    "Selected_Assets_Tuple"
] = (
    optimization_results_df[
        "Selected_Assets"
    ]
    .apply(
        lambda x: tuple(sorted(x))
    )
)


top_sharpe = (
    optimization_results_df[
        "Validation_Sharpe"
    ].max()
)


top_results = (
    optimization_results_df[
        np.isclose(
            optimization_results_df[
                "Validation_Sharpe"
            ],
            top_sharpe
        )
    ]
    .copy()
)


BASELINE_PARAMETERS = {

    "Beta_Window": 60,

    "Momentum_Window": 60,

    "Volatility_Window": 20,

    "Sharpe_Window": 60

}


parameter_columns = [
    "Beta_Window",
    "Momentum_Window",
    "Volatility_Window",
    "Sharpe_Window"
]


def parameter_distance(row):

    return sum(
        abs(
            row[parameter]
            - BASELINE_PARAMETERS[parameter]
        )
        for parameter in parameter_columns
    )


top_results["Parameter_Distance"] = (
    top_results
    .apply(
        parameter_distance,
        axis=1
    )
)


representative_parameters = (
    top_results
    .sort_values(
        [
            "Parameter_Distance",
            "Validation_Sharpe"
        ],
        ascending=[
            True,
            False
        ]
    )
    .iloc[0]
)


optimized_assets = (
    representative_parameters[
        "Selected_Assets"
    ]
)


# ============================================================
# 19. FINAL DEVELOPMENT ASSET SELECTION
# ============================================================
#
# Recalculate the representative robust parameter set using
# ALL development data.
#
# The final test data is still untouched.
# ============================================================

final_development_snapshot = (
    calculate_factor_snapshot(

        development_df,

        beta_window=int(
            representative_parameters[
                "Beta_Window"
            ]
        ),

        momentum_window=int(
            representative_parameters[
                "Momentum_Window"
            ]
        ),

        volatility_window=int(
            representative_parameters[
                "Volatility_Window"
            ]
        ),

        sharpe_window=int(
            representative_parameters[
                "Sharpe_Window"
            ]
        )

    )
)


final_development_ranking, selected_assets = (
    rank_and_select_assets(
        final_development_snapshot
    )
)


print(
    "\n" + "=" * 70
)

print(
    "FINAL DEVELOPMENT ASSET SELECTION"
)

print(
    "=" * 70
)

print(
    "\nRepresentative parameters:"
)

print(
    representative_parameters[
        parameter_columns
    ]
)


print(
    "\nSelected assets:"
)

print(
    selected_assets
)


# ============================================================
# 20. SAVE SELECTED ASSETS
# ============================================================

selected_assets_df = pd.DataFrame({

    "Asset":
        selected_assets

})


selected_assets_path = os.path.join(
    OUTPUT_PATH,
    "selected_assets.csv"
)


selected_assets_df.to_csv(
    selected_assets_path,
    index=False
)


# ============================================================
# 21. PORTFOLIO OPTIMIZATION DATA
# ============================================================

optimization_returns = (
    development_df[
        selected_assets
    ]
    .pct_change()
    .dropna()
)


expected_annualized_returns = (
    optimization_returns
    .mean()
    * TRADING_DAYS
)


annualized_covariance = (
    optimization_returns
    .cov()
    * TRADING_DAYS
)


# ============================================================
# 22. CONSTRAINED MAXIMUM-SHARPE FUNCTION
# ============================================================

def optimize_portfolio(
    expected_returns,
    covariance_matrix,
    max_weight
):
    """
    Maximize the Sharpe ratio subject to:

        Sum(weights) = 1

        0 <= weight <= max_weight
    """

    n_assets = (
        len(expected_returns)
    )


    initial_weights = np.repeat(
        1 / n_assets,
        n_assets
    )


    def portfolio_return(weights):

        return np.dot(
            weights,
            expected_returns
        )


    def portfolio_volatility(weights):

        variance = (
            weights
            @ covariance_matrix.values
            @ weights
        )

        return np.sqrt(
            variance
        )


    def negative_sharpe(weights):

        expected_return = (
            portfolio_return(weights)
        )

        volatility = (
            portfolio_volatility(weights)
        )


        if volatility == 0:

            return 1e6


        return -(
            (
                expected_return
                - RISK_FREE_RATE
            )
            / volatility
        )


    constraints = [

        {
            "type": "eq",

            "fun": lambda weights:
                np.sum(weights) - 1
        }

    ]


    bounds = [
        (
            0,
            max_weight
        )
        for _ in range(n_assets)
    ]


    result = minimize(

        negative_sharpe,

        initial_weights,

        method="SLSQP",

        bounds=bounds,

        constraints=constraints

    )


    if not result.success:

        raise RuntimeError(
            result.message
        )


    weights = result.x


    return_return = (
        portfolio_return(weights)
    )


    return_volatility = (
        portfolio_volatility(weights)
    )


    return_sharpe = (
        (
            return_return
            - RISK_FREE_RATE
        )
        / return_volatility
    )


    return {

        "weights":
            weights,

        "return":
            return_return,

        "volatility":
            return_volatility,

        "sharpe":
            return_sharpe

    }


# ============================================================
# 23. CONSTRAINED PORTFOLIO EXPERIMENTS
# ============================================================

maximum_weight_values = [
    1 / 3,
    0.40,
    0.50,
    0.75,
    1.00
]


constrained_results = []


for maximum_weight in maximum_weight_values:

    result = optimize_portfolio(

        expected_annualized_returns,

        annualized_covariance,

        maximum_weight

    )


    row = {

        "Maximum_Asset_Weight":
            maximum_weight,

        "Portfolio_Return":
            result["return"],

        "Portfolio_Volatility":
            result["volatility"],

        "Sharpe_Ratio":
            result["sharpe"]

    }


    for asset, weight in zip(
        selected_assets,
        result["weights"]
    ):

        row[asset] = weight


    constrained_results.append(
        row
    )


constrained_results_df = (
    pd.DataFrame(
        constrained_results
    )
)


constrained_results_df = (
    constrained_results_df[
        [
            "Maximum_Asset_Weight"
        ]
        + selected_assets
        + [
            "Portfolio_Return",
            "Portfolio_Volatility",
            "Sharpe_Ratio"
        ]
    ]
)


print(
    "\n" + "=" * 70
)

print(
    "CONSTRAINED PORTFOLIO OPTIMIZATION"
)

print(
    "=" * 70
)

print(
    constrained_results_df
)


# ============================================================
# 24. DEFINE BENCHMARK AND ALTERNATIVE MODEL
# ============================================================
#
# Benchmark:
#
# Equal Weight
#     33.33 / 33.33 / 33.33
#
# Alternative:
#
# Max-40 constrained maximum-Sharpe portfolio
#
# The Max-40 portfolio is the alternative model used in
# Project 02.
# ============================================================

equal_weight = np.repeat(
    1 / len(selected_assets),
    len(selected_assets)
)


max40_result = optimize_portfolio(

    expected_annualized_returns,

    annualized_covariance,

    0.40

)


max40_weights = (
    max40_result["weights"]
)


print(
    "\n" + "=" * 70
)

print(
    "BENCHMARK VS ALTERNATIVE MODEL"
)

print(
    "=" * 70
)


print(
    "\nEqual-weight benchmark:"
)

for asset, weight in zip(
    selected_assets,
    equal_weight
):

    print(
        f"{asset}: {weight:.2%}"
    )


print(
    "\nMax-40 alternative:"
)

for asset, weight in zip(
    selected_assets,
    max40_weights
):

    print(
        f"{asset}: {weight:.2%}"
    )


# ============================================================
# 25. FROZEN PORTFOLIOS
# ============================================================
#
# These weights are frozen before final OOS evaluation.
# ============================================================

frozen_portfolios_df = pd.DataFrame(

    [

        equal_weight,

        max40_weights

    ],

    index=[
        "Equal_Weight",
        "Max_40"
    ],

    columns=selected_assets

)


frozen_portfolios_path = os.path.join(
    OUTPUT_PATH,
    "frozen_portfolios.csv"
)


frozen_portfolios_df.to_csv(
    frozen_portfolios_path
)


print(
    "\nFrozen portfolios saved to:",
    frozen_portfolios_path
)


# ============================================================
# 26. PORTFOLIO EVALUATION FUNCTION
# ============================================================

def evaluate_portfolio(
    portfolio_returns
):
    """
    Calculate basic absolute portfolio metrics.
    """

    portfolio_returns = (
        portfolio_returns
        .dropna()
    )


    total_return = (
        (1 + portfolio_returns)
        .prod()
        - 1
    )


    annualized_return = (
        (1 + total_return)
        ** (
            TRADING_DAYS
            / len(portfolio_returns)
        )
        - 1
    )


    annualized_volatility = (
        portfolio_returns.std()
        * np.sqrt(TRADING_DAYS)
    )


    if annualized_volatility != 0:

        sharpe = (
            annualized_return
            - RISK_FREE_RATE
        ) / annualized_volatility

    else:

        sharpe = np.nan


    wealth = (
        1 + portfolio_returns
    ).cumprod()


    drawdown = (
        wealth
        /
        wealth.cummax()
        - 1
    )


    maximum_drawdown = (
        drawdown.min()
    )


    return {

        "Total_Return":
            total_return,

        "Annualized_Return":
            annualized_return,

        "Annualized_Volatility":
            annualized_volatility,

        "Sharpe_Ratio":
            sharpe,

        "Maximum_Drawdown":
            maximum_drawdown,

        "Final_Wealth":
            wealth.iloc[-1]

    }


# ============================================================
# 27. FINAL UNSEEN TEST RETURNS
# ============================================================

final_test_returns = (
    final_test_df[
        selected_assets
    ]
    .pct_change()
    .dropna()
)


final_test_returns_path = os.path.join(
    OUTPUT_PATH,
    "final_test_returns.csv"
)


final_test_returns.to_csv(
    final_test_returns_path
)


print(
    "\nFinal OOS returns saved to:",
    final_test_returns_path
)


# ============================================================
# 28. FINAL OOS PORTFOLIO EVALUATION
# ============================================================

final_results = []


for portfolio_name, weights in [

    (
        "Equal_Weight",
        equal_weight
    ),

    (
        "Max_40",
        max40_weights
    )

]:

    portfolio_returns = (
        final_test_returns
        .dot(weights)
    )


    metrics = evaluate_portfolio(
        portfolio_returns
    )


    row = {

        "Portfolio":
            portfolio_name

    }


    for asset, weight in zip(
        selected_assets,
        weights
    ):

        row[asset] = weight


    row.update(
        metrics
    )


    final_results.append(
        row
    )


final_results_df = (
    pd.DataFrame(
        final_results
    )
)


# ============================================================
# 29. FINAL OOS RESULTS
# ============================================================

print(
    "\n" + "=" * 70
)

print(
    "FINAL UNSEEN OUT-OF-SAMPLE RESULTS"
)

print(
    "=" * 70
)

print(
    final_results_df
)


# ============================================================
# 30. TRANSACTION-COST SENSITIVITY
# ============================================================
#
# The portfolios are frozen.
#
# We therefore model transaction cost as an initial
# implementation cost.
#
# Starting from cash:
#
# Initial turnover = sum(abs(target weights))
#
# Since the portfolio starts from zero exposure, this equals
# 100% of capital for a fully invested portfolio.
#
# Net initial implementation cost:
#
#     turnover × transaction_cost
#
# The portfolio is then held without daily rebalancing.
#
# This avoids the old problem where constant target weights
# generated artificially zero daily turnover.
# ============================================================

transaction_cost_results = []


for portfolio_name, weights in [

    (
        "Equal_Weight",
        equal_weight
    ),

    (
        "Max_40",
        max40_weights
    )

]:

    gross_returns = (
        final_test_returns
        .dot(weights)
    )


    initial_turnover = (
        np.abs(weights)
        .sum()
    )


    for cost in TRANSACTION_COSTS:

        implementation_cost = (
            initial_turnover
            * cost
        )


        net_returns = (
            gross_returns
            .copy()
        )


        # Apply implementation cost to initial capital.
        #
        # If initial wealth = 1:
        #
        # net wealth =
        # (1 - implementation cost)
        # × cumulative gross wealth

        gross_wealth = (
            1 + net_returns
        ).cumprod()


        net_wealth = (
            (
                1
                - implementation_cost
            )
            * gross_wealth
        )


        net_total_return = (
            net_wealth.iloc[-1]
            - 1
        )


        number_of_days = (
            len(net_returns)
        )


        net_annualized_return = (
            (
                1
                + net_total_return
            )
            ** (
                TRADING_DAYS
                / number_of_days
            )
            - 1
        )


        net_volatility = (
            net_returns.std()
            * np.sqrt(TRADING_DAYS)
        )


        if net_volatility != 0:

            net_sharpe = (
                net_annualized_return
                - RISK_FREE_RATE
            ) / net_volatility

        else:

            net_sharpe = np.nan


        drawdown = (
            net_wealth
            /
            net_wealth.cummax()
            - 1
        )


        net_max_drawdown = (
            drawdown.min()
        )


        transaction_cost_results.append({

            "Portfolio":
                portfolio_name,

            "Transaction_Cost":
                f"{cost * 10000:.0f}_bps",

            "Initial_Turnover":
                initial_turnover,

            "Implementation_Cost":
                implementation_cost,

            "Total_Return":
                net_total_return,

            "Annualized_Return":
                net_annualized_return,

            "Annualized_Volatility":
                net_volatility,

            "Sharpe_Ratio":
                net_sharpe,

            "Maximum_Drawdown":
                net_max_drawdown

        })


transaction_cost_df = (
    pd.DataFrame(
        transaction_cost_results
    )
)


print(
    "\n" + "=" * 70
)

print(
    "TRANSACTION-COST SENSITIVITY"
)

print(
    "=" * 70
)

print(
    transaction_cost_df
)


# ============================================================
# 31. SAVE PROJECT 01 OUTPUTS
# ============================================================

development_snapshot.to_csv(
    os.path.join(
        OUTPUT_PATH,
        "development_factor_snapshot.csv"
    )
)


final_development_snapshot.to_csv(
    os.path.join(
        OUTPUT_PATH,
        "final_development_factor_snapshot.csv"
    )
)


final_development_ranking.to_csv(
    os.path.join(
        OUTPUT_PATH,
        "final_development_asset_ranking.csv"
    )
)


development_covariance.to_csv(
    os.path.join(
        OUTPUT_PATH,
        "development_covariance_matrix.csv"
    )
)


development_correlation.to_csv(
    os.path.join(
        OUTPUT_PATH,
        "development_correlation_matrix.csv"
    )
)


optimization_results_df.to_csv(
    os.path.join(
        OUTPUT_PATH,
        "hyperparameter_results.csv"
    ),
    index=False
)


constrained_results_df.to_csv(
    os.path.join(
        OUTPUT_PATH,
        "constrained_portfolio_results.csv"
    ),
    index=False
)


final_results_df.to_csv(
    os.path.join(
        OUTPUT_PATH,
        "final_oos_results.csv"
    ),
    index=False
)


transaction_cost_df.to_csv(
    os.path.join(
        OUTPUT_PATH,
        "transaction_cost_sensitivity.csv"
    ),
    index=False
)


# ============================================================
# 32. SAVE MODEL SUMMARY
# ============================================================

model_summary = pd.DataFrame({

    "Selected_Assets":
        [
            ", ".join(selected_assets)
        ],

    "Beta_Window":
        [
            representative_parameters[
                "Beta_Window"
            ]
        ],

    "Momentum_Window":
        [
            representative_parameters[
                "Momentum_Window"
            ]
        ],

    "Volatility_Window":
        [
            representative_parameters[
                "Volatility_Window"
            ]
        ],

    "Sharpe_Window":
        [
            representative_parameters[
                "Sharpe_Window"
            ]
        ],

    "Benchmark":
        [
            "Equal_Weight"
        ],

    "Alternative_Model":
        [
            "Max_40"
        ]

})


model_summary.to_csv(
    os.path.join(
        OUTPUT_PATH,
        "model_summary.csv"
    ),
    index=False
)


# ============================================================
# 33. FINAL PROJECT SUMMARY
# ============================================================

print(
    "\n" + "=" * 70
)

print(
    "PROJECT 01 COMPLETED"
)

print(
    "=" * 70
)

print(
    "\nSelected assets:",
    selected_assets
)

print(
    "\nBenchmark: Equal Weight"
)

print(
    "Alternative model: Max-40 constrained portfolio"
)

print(
    "\nProject 01 outputs saved to:"
)

print(
    OUTPUT_PATH
)

print(
    "\nProject 01 ends at:"
)

print(
    "Asset selection, portfolio construction, OOS testing,"
)

print(
    "and transaction-cost sensitivity."
)

print(
    "\nRisk and performance attribution is performed in Project 02."
)
