# ============================================================
# PROJECT 01
# FACTOR-BASED ASSET SELECTION & ROBUST PORTFOLIO OPTIMIZATION
# ============================================================
#
# OBJECTIVE
# ------------------------------------------------------------
#
#   1. Clean market data
#   2. Establish a baseline reference specification
#   3. Construct Beta, Momentum, Volatility and Sharpe factors
#   4. Select assets using equal factor weights
#   5. Test factor-window robustness
#   6. Identify all configurations achieving the best
#      validation Sharpe
#   7. Select representative robust parameters
#   8. Freeze the robustness-selected asset universe
#   9. Analyze covariance and correlation
#  10. Optimize portfolio weights under constraints
#  11. Freeze portfolio specifications
#  12. Evaluate on completely unseen OOS data
#  13. Perform transaction-cost sensitivity analysis
#  14. Create clean Project 01 -> Project 02 output files
#
#
# ============================================================
# IMPORTANT METHODOLOGICAL PRINCIPLE
# ============================================================
#
# THE BASELINE IS A REFERENCE SPECIFICATION ONLY.
#
# Baseline:
#
#   Beta       = 60 days
#   Momentum   = 60 days
#   Volatility = 20 days
#   Sharpe     = 60 days
#
# Factor weights:
#
#   Beta       = 25%
#   Momentum   = 25%
#   Volatility = 25%
#   Sharpe     = 25%
#
#
# The baseline-selected assets are NOT automatically used
# as the final Project 01 asset universe.
#
# The FINAL asset universe is determined by the
# hyperparameter robustness analysis.
#
#
# ============================================================
# ROBUSTNESS PRINCIPLE
# ============================================================
#
# Multiple parameter combinations can produce:
#
#   - the same selected asset universe
#   - the same validation portfolio return
#   - the same validation Sharpe
#
# Therefore:
#
#   We do NOT simply use idxmax().
#
# Instead:
#
#   1. Identify ALL configurations achieving the best
#      validation Sharpe.
#
#   2. Measure their distance from the baseline.
#
#   3. Select the closest configuration to the baseline.
#
#   4. If distance remains tied, use a deterministic
#      smaller-volatility-window tie-break.
#
#
# In the current research result this gives:
#
#   Representative parameters:
#
#       Beta       = 60
#       Momentum   = 60
#       Volatility = 10
#       Sharpe     = 60
#
#   i.e.
#
#       (60, 60, 10, 60)
#
# The resulting robust asset universe is:
#
#       AAPL + GOOG + META
#
# This universe is then FROZEN and passed to the
# portfolio construction stage and Project 02.
#
# ------------------------------------------------------------

# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import os
from itertools import product

import numpy as np
import pandas as pd
from scipy.optimize import minimize


# ==================================
# 2. PROJECT SETTINGS
# ==================================

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

# ==================================
# 3. DATA AND OUTPUT PATHS — GITHUB
# ==================================

from pathlib import Path

# Folder containing this Python script
PROJECT_PATH = Path(__file__).resolve().parent

# Project data folder
DATA_PATH = PROJECT_PATH / "data"

# Project output folder
OUTPUT_PATH = PROJECT_PATH / "outputs"

# Create outputs folder if it does not exist
OUTPUT_PATH.mkdir(
    parents=True,
    exist_ok=True
)
# --------------------------------------------------------
# PATH CHECK
# --------------------------------------------------------

print("=" * 60)
print("PROJECT PATH CHECK")
print("=" * 60)

print("\nProject path:")
print(PROJECT_PATH)

print("\nData path:")
print(DATA_PATH)

print("\nOutput path:")
print(OUTPUT_PATH)

print("\nData directory exists:")
print(DATA_PATH.exists())

print("\nAAPL.csv exists:")
print(
    (DATA_PATH / "AAPL.csv").exists()
)
# ==================================
# 4. LOAD PRICE CSV
# ==================================

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


# ==================================
# 5. LOAD ALL MARKET DATA
# ==================================

print(
    "\n" + "=" * 60
)

print(
    "LOADING RAW MARKET DATA"
)

print(
    "=" * 60
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


# ==================================
# 6. ALIGN ASSET UNIVERSE
# ==================================

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


# ==================================
# 7. SAVE CLEANED PRICE DATA
# ==================================
#
# This is the first reusable output from Project 01.
#
# Project 02 will read this file instead of loading and
# cleaning the original raw CSV files.
# ==================================

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


# ==================================
# 8. CALCULATE RETURNS
# =================================

returns = (
    asset_universe
    .pct_change()
    .dropna()
)


# ============================================================
# 9. OUTER DEVELOPMENT / FINAL TEST SPLIT
# ============================================================
#
# 80% chronological development
# 20% completely unseen final test
#
# The final test data MUST NOT influence:
#
#   - factor selection
#   - hyperparameter selection
#   - asset selection
#   - portfolio optimization
#
# ============================================================


print("\n" + "=" * 70)
print("OUTER DEVELOPMENT / FINAL TEST SPLIT")
print("=" * 70)


split_index = int(
    len(prices) * 0.80
)


development_prices = (
    prices.iloc[
        :split_index
    ].copy()
)


final_test_prices = (
    prices.iloc[
        split_index:
    ].copy()
)


print("\nDevelopment period:")

print(
    "Start:",
    development_prices.index.min()
)

print(
    "End:",
    development_prices.index.max()
)

print(
    "Observations:",
    len(development_prices)
)


print("\nFinal unseen test period:")

print(
    "Start:",
    final_test_prices.index.min()
)

print(
    "End:",
    final_test_prices.index.max()
)

print(
    "Observations:",
    len(final_test_prices)
)


chronology_check = (

    development_prices.index.max()
    <
    final_test_prices.index.min()
)


print(
    "\nChronology check:",
    "PASSED"
    if chronology_check
    else "FAILED"
)


if not chronology_check:

    raise ValueError(
        "Chronology check failed."
    )


# ============================================================
# 10. BASELINE REFERENCE SPECIFICATION
# ============================================================
#
# IMPORTANT:
#
# The baseline is NOT the final model.
#
# It is retained as a transparent reference point against
# which robust parameter configurations are compared.
#
# ============================================================


print("\n" + "=" * 70)
print("BASELINE REFERENCE SPECIFICATION")
print("=" * 70)


BASELINE_PARAMS = {

    "Beta_Window": 60,

    "Momentum_Window": 60,

    "Volatility_Window": 20,

    "Sharpe_Window": 60
}


FACTOR_WEIGHTS = {

    "Beta_Score": 0.25,

    "Momentum_Score": 0.25,

    "Volatility_Score": 0.25,

    "Sharpe_Score": 0.25
}


print(
    "\nBaseline parameters:"
)


for key, value in BASELINE_PARAMS.items():

    print(
        f"{key}: {value}"
    )


print(
    "\nFactor weights:"
)


for key, value in FACTOR_WEIGHTS.items():

    print(
        f"{key}: {value:.0%}"
    )


print(
    "\nIMPORTANT:"
)

print(
    "The baseline is a REFERENCE specification only."
)

print(
    "Baseline-selected assets are NOT automatically "
    "the final Project 01 universe."
)


# ============================================================
# 11. INNER DEVELOPMENT SPLIT
# ============================================================
#
# Optimization train:
#   Used for factor calculation and asset selection.
#
# Validation:
#   Used only to evaluate the candidate configuration.
#
# ============================================================


print("\n" + "=" * 70)
print("INNER DEVELOPMENT SPLIT")
print("=" * 70)


inner_split_index = int(
    len(development_prices) * 0.80
)


optimization_train = (
    development_prices.iloc[
        :inner_split_index
    ].copy()
)


validation_prices = (
    development_prices.iloc[
        inner_split_index:
    ].copy()
)


print("\nOptimization train:")

print(
    optimization_train.index.min(),
    "to",
    optimization_train.index.max()
)

print(
    "Observations:",
    len(optimization_train)
)


print("\nValidation:")

print(
    validation_prices.index.min(),
    "to",
    validation_prices.index.max()
)

print(
    "Observations:",
    len(validation_prices)
)


# ============================================================
# 12. FACTOR CALCULATION FUNCTIONS
# ============================================================


def calculate_beta(
    asset_returns,
    market_returns,
    window
):

    combined = pd.concat(
        [
            asset_returns,
            market_returns
        ],
        axis=1
    ).dropna()


    combined.columns = [
        "asset",
        "market"
    ]


    if len(combined) < window:

        return np.nan


    rolling_data = combined.iloc[
        -window:
    ]


    market_variance = (
        rolling_data["market"]
        .var()
    )


    if (
        pd.isna(market_variance)
        or
        market_variance == 0
    ):

        return np.nan


    covariance = (
        rolling_data["asset"]
        .cov(
            rolling_data["market"]
        )
    )


    beta = (
        covariance
        /
        market_variance
    )


    return float(
        beta
    )


def calculate_momentum(
    prices_series,
    window
):

    if len(prices_series) < window + 1:

        return np.nan


    momentum = (

        prices_series.iloc[-1]
        /
        prices_series.iloc[
            -window - 1
        ]
        - 1
    )


    return float(
        momentum
    )


def calculate_volatility(
    returns_series,
    window
):

    if len(returns_series) < window:

        return np.nan


    volatility = (

        returns_series.iloc[
            -window:
        ].std()
        *
        np.sqrt(252)
    )


    return float(
        volatility
    )


def calculate_sharpe(
    returns_series,
    window
):

    if len(returns_series) < window:

        return np.nan


    rolling_returns = (
        returns_series.iloc[
            -window:
        ]
    )


    mean_return = (
        rolling_returns.mean()
    )


    volatility = (
        rolling_returns.std()
    )


    if (
        pd.isna(volatility)
        or
        volatility == 0
    ):

        return np.nan


    sharpe = (

        mean_return
        /
        volatility
        *
        np.sqrt(252)
    )


    return float(
        sharpe
    )


# ============================================================
# 13. FACTOR SNAPSHOT
# ============================================================


def calculate_factor_snapshot(
    price_data,
    beta_window,
    momentum_window,
    volatility_window,
    sharpe_window
):

    asset_prices = price_data[
        ASSETS
    ]


    market_prices = price_data[
        MARKET
    ]


    asset_returns = (
        asset_prices
        .pct_change()
    )


    market_returns = (
        market_prices
        .pct_change()
    )


    factor_rows = []


    for ticker in ASSETS:

        beta = calculate_beta(

            asset_returns[ticker],

            market_returns,

            beta_window
        )


        momentum = calculate_momentum(

            asset_prices[ticker],

            momentum_window
        )


        volatility = calculate_volatility(

            asset_returns[ticker],

            volatility_window
        )


        sharpe = calculate_sharpe(

            asset_returns[ticker],

            sharpe_window
        )


        factor_rows.append(

            {

                "Asset":
                    ticker,

                "Beta":
                    beta,

                "Momentum":
                    momentum,

                "Volatility":
                    volatility,

                "Sharpe":
                    sharpe
            }
        )


    factor_df = pd.DataFrame(
        factor_rows
    )


    factor_df.set_index(
        "Asset",
        inplace=True
    )


    return factor_df


# ============================================================
# 14. FACTOR RANKING / SCORING
# ============================================================
#
# Higher score = better.
#
# Beta:
#   Lower beta = higher score
#
# Momentum:
#   Higher momentum = higher score
#
# Volatility:
#   Lower volatility = higher score
#
# Sharpe:
#   Higher Sharpe = higher score
#
# ============================================================


def add_factor_scores(
    factor_df
):

    df = factor_df.copy()


    # --------------------------------------------------------
    # Beta
    # Lower beta = better
    # --------------------------------------------------------

    df["Beta_Score"] = (

        df["Beta"]
        .rank(
            ascending=True,
            method="min"
        )
    )


    # --------------------------------------------------------
    # Momentum
    # Higher momentum = better
    # --------------------------------------------------------

    df["Momentum_Score"] = (

        df["Momentum"]
        .rank(
            ascending=False,
            method="min"
        )
    )


    # --------------------------------------------------------
    # Volatility
    # Lower volatility = better
    # --------------------------------------------------------

    df["Volatility_Score"] = (

        df["Volatility"]
        .rank(
            ascending=True,
            method="min"
        )
    )


    # --------------------------------------------------------
    # Sharpe
    # Higher Sharpe = better
    # --------------------------------------------------------

    df["Sharpe_Score"] = (

        df["Sharpe"]
        .rank(
            ascending=False,
            method="min"
        )
    )


    # --------------------------------------------------------
    # Convert rank to normalized score
    #
    # With 5 assets:
    #
    # Best  = 1.0
    # ...
    # Worst = 0.2
    # --------------------------------------------------------

    n_assets = len(df)


    for column in [

        "Beta_Score",

        "Momentum_Score",

        "Volatility_Score",

        "Sharpe_Score"

    ]:

        df[column] = (

            (
                n_assets
                -
                df[column]
                +
                1
            )
            /
            n_assets
        )


    # --------------------------------------------------------
    # Equal-weight composite Asset Score
    # --------------------------------------------------------

    df["Asset_Score"] = (

        FACTOR_WEIGHTS[
            "Beta_Score"
        ]
        *
        df["Beta_Score"]

        +

        FACTOR_WEIGHTS[
            "Momentum_Score"
        ]
        *
        df["Momentum_Score"]

        +

        FACTOR_WEIGHTS[
            "Volatility_Score"
        ]
        *
        df["Volatility_Score"]

        +

        FACTOR_WEIGHTS[
            "Sharpe_Score"
        ]
        *
        df["Sharpe_Score"]
    )


    df.sort_values(
        "Asset_Score",
        ascending=False,
        inplace=True
    )


    return df


# ============================================================
# 15. ASSET SELECTION
# ============================================================


def select_assets(
    factor_df,
    n_assets=3
):

    ranked = add_factor_scores(
        factor_df
    )


    selected = list(
        ranked.head(
            n_assets
        ).index
    )


    return (
        ranked,
        selected
    )


# ============================================================
# 16. BASELINE REFERENCE FACTOR SNAPSHOT
# ============================================================
#
# This is for documentation only.
#
# It does NOT determine the final asset universe.
#
# ============================================================


print("\n" + "=" * 70)
print("BASELINE REFERENCE FACTOR SNAPSHOT")
print("=" * 70)


baseline_factor_snapshot = (
    calculate_factor_snapshot(

        development_prices,

        BASELINE_PARAMS[
            "Beta_Window"
        ],

        BASELINE_PARAMS[
            "Momentum_Window"
        ],

        BASELINE_PARAMS[
            "Volatility_Window"
        ],

        BASELINE_PARAMS[
            "Sharpe_Window"
        ]
    )
)


baseline_ranking, baseline_assets = (
    select_assets(
        baseline_factor_snapshot
    )
)


print(
    "\nBaseline factor snapshot:"
)

print(
    baseline_factor_snapshot
)


print(
    "\nBaseline ranking:"
)

print(
    baseline_ranking
)


print(
    "\nBaseline reference assets:"
)

print(
    baseline_assets
)


print(
    "\nNOTE:"
)

print(
    "These assets are retained only as the baseline reference."
)

print(
    "They do NOT automatically become the final universe."
)


# ============================================================
# 17. HYPERPARAMETER GRID
# ============================================================


print("\n" + "=" * 70)
print("HYPERPARAMETER GRID")
print("=" * 70)


BETA_WINDOWS = [
    40,
    60,
    80
]


MOMENTUM_WINDOWS = [
    40,
    60,
    80
]


VOLATILITY_WINDOWS = [
    10,
    20,
    30
]


SHARPE_WINDOWS = [
    40,
    60,
    80
]


parameter_grid = []


for beta_window in BETA_WINDOWS:

    for momentum_window in MOMENTUM_WINDOWS:

        for volatility_window in VOLATILITY_WINDOWS:

            for sharpe_window in SHARPE_WINDOWS:

                parameter_grid.append(

                    {

                        "Beta_Window":
                            beta_window,

                        "Momentum_Window":
                            momentum_window,

                        "Volatility_Window":
                            volatility_window,

                        "Sharpe_Window":
                            sharpe_window
                    }
                )


print(
    "Number of combinations:",
    len(parameter_grid)
)


if len(parameter_grid) != 81:

    raise ValueError(
        "Expected 81 hyperparameter combinations."
    )


# ============================================================
# 18. VALIDATION PERFORMANCE
# ============================================================


def portfolio_validation_metrics(
    validation_prices,
    selected_assets
):

    validation_returns = (

        validation_prices[
            selected_assets
        ]
        .pct_change()
        .dropna()
    )


    if len(validation_returns) == 0:

        return (
            np.nan,
            np.nan,
            np.nan
        )


    # Equal-weight portfolio used ONLY to compare
    # asset-universe selections.
    #
    # Portfolio optimization occurs later.

    n = len(
        selected_assets
    )


    weights = np.repeat(
        1 / n,
        n
    )


    portfolio_returns = (

        validation_returns
        @
        weights
    )


    cumulative_return = (

        (1 + portfolio_returns)
        .prod()
        - 1
    )


    annualized_volatility = (

        portfolio_returns.std()
        *
        np.sqrt(252)
    )


    if (

        portfolio_returns.std()
        == 0

        or

        pd.isna(
            portfolio_returns.std()
        )

    ):

        sharpe = np.nan

    else:

        sharpe = (

            portfolio_returns.mean()
            /
            portfolio_returns.std()
            *
            np.sqrt(252)
        )


    return (

        float(cumulative_return),

        float(annualized_volatility),

        float(sharpe)
    )


# ============================================================
# 19. HYPERPARAMETER ROBUSTNESS TEST
# ============================================================


print("\n" + "=" * 70)
print("HYPERPARAMETER ROBUSTNESS")
print("=" * 70)


robustness_results = []


for params in parameter_grid:

    factor_snapshot = (
        calculate_factor_snapshot(

            optimization_train,

            params[
                "Beta_Window"
            ],

            params[
                "Momentum_Window"
            ],

            params[
                "Volatility_Window"
            ],

            params[
                "Sharpe_Window"
            ]
        )
    )


    ranking, selected = (
        select_assets(
            factor_snapshot
        )
    )


    (
        validation_return,
        validation_volatility,
        validation_sharpe

    ) = portfolio_validation_metrics(

        validation_prices,

        selected
    )


    selected_tuple = tuple(
        sorted(selected)
    )


    robustness_results.append(

        {

            **params,

            "Selected_Assets":
                selected_tuple,

            "Validation_Return":
                validation_return,

            "Validation_Volatility":
                validation_volatility,

            "Validation_Sharpe":
                validation_sharpe
        }
    )


robustness_df = pd.DataFrame(
    robustness_results
)


# ============================================================
# 20. PARAMETER DISTANCE FROM BASELINE
# ============================================================


robustness_df[
    "Parameter_Distance"
] = (

    abs(

        robustness_df[
            "Beta_Window"
        ]
        -
        BASELINE_PARAMS[
            "Beta_Window"
        ]
    )

    +

    abs(

        robustness_df[
            "Momentum_Window"
        ]
        -
        BASELINE_PARAMS[
            "Momentum_Window"
        ]
    )

    +

    abs(

        robustness_df[
            "Volatility_Window"
        ]
        -
        BASELINE_PARAMS[
            "Volatility_Window"
        ]
    )

    +

    abs(

        robustness_df[
            "Sharpe_Window"
        ]
        -
        BASELINE_PARAMS[
            "Sharpe_Window"
        ]
    )
)


# ============================================================
# 21. BEST VALIDATION SHARPE
# ============================================================


best_validation_sharpe = (

    robustness_df[
        "Validation_Sharpe"
    ].max()
)


print(
    "\nBest validation Sharpe:"
)

print(
    best_validation_sharpe
)


# ============================================================
# 22. ALL CONFIGURATIONS AT BEST VALIDATION SHARPE
# ============================================================
#
# We deliberately retain ALL tied configurations.
#
# This allows us to distinguish:
#
#   "best single configuration"
#
# from
#
#   "robust region of configurations."
#
# ============================================================


best_configs = robustness_df[
    np.isclose(

        robustness_df[
            "Validation_Sharpe"
        ],

        best_validation_sharpe,

        rtol=1e-10,

        atol=1e-10
    )
].copy()


print("\n" + "=" * 70)
print("ALL CONFIGURATIONS AT BEST VALIDATION SHARPE")
print("=" * 70)


display_columns = [

    "Beta_Window",

    "Momentum_Window",

    "Volatility_Window",

    "Sharpe_Window",

    "Selected_Assets",

    "Validation_Return",

    "Validation_Volatility",

    "Validation_Sharpe",

    "Parameter_Distance"
]


print(
    best_configs[
        display_columns
    ].to_string(
        index=False
    )
)


# ============================================================
# 23. ASSET-SELECTION FREQUENCY
# ============================================================
#
# This is the key robustness evidence.
#
# We count how frequently each asset universe appears
# across ALL 81 parameter configurations.
#
# ============================================================


print("\n" + "=" * 70)
print("SELECTION FREQUENCY ACROSS PARAMETER GRID")
print("=" * 70)


selection_frequency = (

    robustness_df[
        "Selected_Assets"
    ]
    .value_counts()
    .reset_index()
)


selection_frequency.columns = [

    "Selected_Assets",

    "Frequency"
]


selection_frequency[
    "Frequency_Percent"
] = (

    selection_frequency[
        "Frequency"
    ]
    /
    len(robustness_df)
    *
    100
)


print(
    selection_frequency.to_string(
        index=False
    )
)


# ============================================================
# 24. ROBUSTNESS DOCUMENTATION
# ============================================================


most_frequent_assets = (

    selection_frequency.iloc[0][
        "Selected_Assets"
    ]
)


most_frequent_count = int(

    selection_frequency.iloc[0][
        "Frequency"
    ]
)


most_frequent_percentage = float(

    selection_frequency.iloc[0][
        "Frequency_Percent"
    ]
)


print("\n" + "=" * 70)
print("ROBUSTNESS INTERPRETATION")
print("=" * 70)


print(
    "\nMost frequently selected universe:"
)

print(
    most_frequent_assets
)


print(
    "\nFrequency:"
)

print(
    f"{most_frequent_count} / "
    f"{len(robustness_df)}"
)


print(
    "\nFrequency percentage:"
)

print(
    f"{most_frequent_percentage:.2f}%"
)


if most_frequent_percentage >= 50:

    print(
        "\nROBUSTNESS CONCLUSION:"
    )

    print(
        f"{most_frequent_assets} is not dependent "
        "on one lucky parameter configuration."
    )

    print(
        f"It is selected by "
        f"{most_frequent_count} of "
        f"{len(robustness_df)} configurations "
        f"({most_frequent_percentage:.2f}%)."
    )


# ============================================================
# 25. REPRESENTATIVE PARAMETER SELECTION
# ============================================================
#
# Decision hierarchy:
#
#   1. Highest validation Sharpe
#   2. Smallest distance from baseline
#   3. Smaller volatility window
#   4. Smaller Beta window
#   5. Smaller Momentum window
#   6. Smaller Sharpe window
#
# The final additional rules make the selection completely
# deterministic.
#
# ============================================================


print("\n" + "=" * 70)
print("REPRESENTATIVE ROBUST PARAMETERS")
print("=" * 70)


representative_candidates = (

    best_configs
    .sort_values(

        by=[

            "Parameter_Distance",

            "Volatility_Window",

            "Beta_Window",

            "Momentum_Window",

            "Sharpe_Window"
        ],

        ascending=[

            True,

            True,

            True,

            True,

            True
        ]
    )
    .copy()
)


representative_row = (
    representative_candidates.iloc[0]
)


REPRESENTATIVE_PARAMS = {

    "Beta_Window":
        int(
            representative_row[
                "Beta_Window"
            ]
        ),

    "Momentum_Window":
        int(
            representative_row[
                "Momentum_Window"
            ]
        ),

    "Volatility_Window":
        int(
            representative_row[
                "Volatility_Window"
            ]
        ),

    "Sharpe_Window":
        int(
            representative_row[
                "Sharpe_Window"
            ]
        )
}


print(
    "\nBaseline reference:"
)

print(
    BASELINE_PARAMS
)


print(
    "\nRepresentative robust parameters:"
)

print(
    REPRESENTATIVE_PARAMS
)


print(
    "\nRepresentative validation Sharpe:"
)

print(
    representative_row[
        "Validation_Sharpe"
    ]
)


print(
    "\nRepresentative selected assets:"
)

print(
    representative_row[
        "Selected_Assets"
    ]
)


print(
    "\nRepresentative parameter distance:"
)

print(
    representative_row[
        "Parameter_Distance"
    ]
)


# ============================================================
# 26. EXPLICIT BASELINE DISTANCE / TIE-BREAK DOCUMENTATION
# ============================================================


print("\n" + "-" * 70)
print("REPRESENTATIVE-PARAMETER TIE-BREAK")
print("-" * 70)


print(
    "\nBaseline reference:"
)

print(
    "(60, 60, 20, 60)"
)


print(
    "\nImportant tied configurations:"
)

print(
    "(60, 60, 10, 60)"
)

print(
    "(60, 60, 30, 60)"
)


print(
    "\nBoth have the same validation Sharpe."
)


print(
    "\nBoth have parameter distance = 10."
)


print(
    "\nDeterministic tie-break:"
)

print(
    "Choose the smaller volatility window."
)


print(
    "\nTherefore:"
)

print(
    "(60, 60, 10, 60)"
)


# ============================================================
# 27. SAVE REPRESENTATIVE CONFIGURATION
# ============================================================
#
# This creates an explicit research record of the final
# representative model specification.
#
# ============================================================


representative_configuration = pd.DataFrame(
    [
        {

            "Baseline_Beta_Window":
                BASELINE_PARAMS[
                    "Beta_Window"
                ],

            "Baseline_Momentum_Window":
                BASELINE_PARAMS[
                    "Momentum_Window"
                ],

            "Baseline_Volatility_Window":
                BASELINE_PARAMS[
                    "Volatility_Window"
                ],

            "Baseline_Sharpe_Window":
                BASELINE_PARAMS[
                    "Sharpe_Window"
                ],

            "Representative_Beta_Window":
                REPRESENTATIVE_PARAMS[
                    "Beta_Window"
                ],

            "Representative_Momentum_Window":
                REPRESENTATIVE_PARAMS[
                    "Momentum_Window"
                ],

            "Representative_Volatility_Window":
                REPRESENTATIVE_PARAMS[
                    "Volatility_Window"
                ],

            "Representative_Sharpe_Window":
                REPRESENTATIVE_PARAMS[
                    "Sharpe_Window"
                ],

            "Validation_Sharpe":
                float(
                    representative_row[
                        "Validation_Sharpe"
                    ]
                ),

            "Parameter_Distance":
                int(
                    representative_row[
                        "Parameter_Distance"
                    ]
                ),

            "Selected_Assets":
                ",".join(
                    representative_row[
                        "Selected_Assets"
                    ]
                ),

            "Most_Frequent_Universe":
                ",".join(
                    most_frequent_assets
                ),

            "Most_Frequent_Count":
                most_frequent_count,

            "Most_Frequent_Percentage":
                most_frequent_percentage
        }
    ]
)


representative_configuration_file = os.path.join(

    OUTPUT_PATH,

    "representative_configuration.csv"
)


representative_configuration.to_csv(

    representative_configuration_file,

    index=False
)


print(
    "\nRepresentative configuration saved to:"
)

print(
    representative_configuration_file
)


# ============================================================
# 28. FINAL PROJECT 01 ASSET UNIVERSE
# ============================================================
#
# CRITICAL:
#
# The final universe comes from the representative
# robustness configuration.
#
# It is NOT copied from baseline_assets.
#
# ============================================================


final_selected_assets = list(

    representative_row[
        "Selected_Assets"
    ]
)


print("\n" + "=" * 70)
print("FINAL PROJECT 01 ASSET UNIVERSE")
print("=" * 70)


print(
    "\nBaseline reference assets:"
)

print(
    baseline_assets
)


print(
    "\nRobust representative assets:"
)

print(
    final_selected_assets
)


# ============================================================
# 29. FINAL DEVELOPMENT FACTOR SNAPSHOT
# ============================================================
#
# Once the specification has been selected using the
# optimization-train / validation process, the factor
# snapshot is recalculated on the FULL development sample.
#
# IMPORTANT:
#
# This is a diagnostic full-development refit.
#
# It does NOT silently replace the frozen robustness-selected
# universe.
#
# ============================================================


print("\n" + "=" * 70)
print("FINAL DEVELOPMENT FACTOR SNAPSHOT")
print("=" * 70)


final_development_factor_snapshot = (
    calculate_factor_snapshot(

        development_prices,

        REPRESENTATIVE_PARAMS[
            "Beta_Window"
        ],

        REPRESENTATIVE_PARAMS[
            "Momentum_Window"
        ],

        REPRESENTATIVE_PARAMS[
            "Volatility_Window"
        ],

        REPRESENTATIVE_PARAMS[
            "Sharpe_Window"
        ]
    )
)


final_development_ranking, final_development_assets = (

    select_assets(

        final_development_factor_snapshot

    )
)


print(
    "\nRepresentative parameters:"
)

print(
    REPRESENTATIVE_PARAMS
)


print(
    "\nFinal development factor snapshot:"
)

print(
    final_development_factor_snapshot
)


print(
    "\nFinal development ranking:"
)

print(
    final_development_ranking
)


print(
    "\nFull-development refit selected assets:"
)

print(
    final_development_assets
)


# ============================================================
# 30. CONSISTENCY CHECK
# ============================================================
#
# This check tells us whether the full-development refit
# produces exactly the same asset ranking outcome.
#
# Regardless of the result, the robustness-selected universe
# remains frozen because asset selection was determined before
# seeing the final OOS sample.
#
# ============================================================


representative_asset_set = set(
    final_selected_assets
)


refitted_asset_set = set(
    final_development_assets
)


print("\n" + "-" * 70)
print("REPRESENTATIVE / FULL-DEVELOPMENT REFIT CHECK")
print("-" * 70)


print(
    "Frozen representative assets:",
    representative_asset_set
)


print(
    "Full-development refit assets:",
    refitted_asset_set
)


if representative_asset_set == refitted_asset_set:

    print(
        "\nREFIT CONSISTENCY: PASSED"
    )

    print(
        "The representative universe is unchanged "
        "when the model is recalculated on the "
        "full development sample."
    )

else:

    print(
        "\nREFIT CONSISTENCY: DIFFERENT"
    )

    print(
        "The full-development factor ranking produced "
        "a different universe."
    )

    print(
        "The robustness-selected universe remains frozen "
        "for downstream Project 01 analysis."
    )


# ============================================================
# 31. FREEZE FINAL ASSET UNIVERSE
# ============================================================
#
# THIS IS THE AUTHORITATIVE PROJECT 01 UNIVERSE.
#
# Project 02 must use selected_assets.csv generated here.
#
# ============================================================


selected_assets = (
    final_selected_assets.copy()
)


print("\n" + "=" * 70)
print("FREEZING PROJECT 01 ASSET UNIVERSE")
print("=" * 70)


print(
    "\nFrozen Project 01 assets:"
)

print(
    selected_assets
)


# ============================================================
# 32. SAVE selected_assets.csv
# ============================================================
#
# IMPORTANT:
#
# This explicitly OVERWRITES any old selected_assets.csv.
#
# This prevents the previous AAPL + GOOG + NVDA file from
# remaining as a stale Project 02 input.
#
# ============================================================


selected_assets_file = os.path.join(

    OUTPUT_PATH,

    "selected_assets.csv"
)


selected_assets_df = pd.DataFrame(

    {
        "Asset":
            selected_assets
    }
)


selected_assets_df.to_csv(

    selected_assets_file,

    index=False
)


print("\n" + "-" * 70)
print("FINAL ASSET UNIVERSE SAVED")
print("-" * 70)


print(
    "\nselected_assets.csv:"
)

print(
    selected_assets_df
)


print(
    "\nSaved to:"
)

print(
    selected_assets_file
)


# ============================================================
# 33. selected_assets.csv INTEGRITY CHECK
# ============================================================


saved_assets_df = pd.read_csv(
    selected_assets_file
)


saved_assets = (

    saved_assets_df[
        "Asset"
    ]
    .tolist()
)


if set(saved_assets) != set(
    selected_assets
):

    raise ValueError(

        "selected_assets.csv does not match "
        "the frozen Project 01 asset universe."
    )


print(
    "\nAsset-universe output integrity check: PASSED"
)


# ============================================================
# 34. SELECTED-ASSET RETURNS
# ============================================================


development_returns = (

    development_prices[
        selected_assets
    ]
    .pct_change()
    .dropna()
)


# ============================================================
# 35. COVARIANCE MATRIX
# ============================================================


print("\n" + "=" * 70)
print("SELECTED-ASSET COVARIANCE MATRIX")
print("=" * 70)


covariance_matrix = (

    development_returns
    .cov()
    *
    252
)


print(
    covariance_matrix
)


# ============================================================
# 36. CORRELATION MATRIX
# ============================================================


correlation_matrix = (

    development_returns
    .corr()
)


print(
    "\nSelected-asset correlation:"
)


print(
    correlation_matrix
)


# ============================================================
# 37. PORTFOLIO STATISTICS
# ============================================================


def portfolio_statistics(

    weights,

    expected_returns,

    covariance_matrix

):

    weights = np.asarray(

        weights,

        dtype=float
    )


    expected_return = float(

        weights
        @
        expected_returns
    )


    variance = float(

        weights
        @
        covariance_matrix
        @
        weights
    )


    volatility = np.sqrt(

        max(
            variance,
            0
        )
    )


    if volatility == 0:

        sharpe = np.nan

    else:

        sharpe = (

            expected_return
            /
            volatility
        )


    return (

        expected_return,

        volatility,

        sharpe
    )


# ============================================================
# 38. EXPECTED RETURNS
# ============================================================
#
# Annualized historical mean returns from the full
# development period.
#
# The asset universe itself has already been frozen.
#
# ============================================================


expected_returns = (

    development_returns
    .mean()
    *
    252
)


# ============================================================
# 39. CONSTRAINED PORTFOLIO OPTIMIZATION
# ============================================================


print("\n" + "=" * 70)
print("CONSTRAINED PORTFOLIO OPTIMIZATION")
print("=" * 70)


n_assets = len(
    selected_assets
)


def negative_sharpe(
    weights
):

    _, _, sharpe = portfolio_statistics(

        weights,

        expected_returns.values,

        covariance_matrix.values
    )


    if pd.isna(sharpe):

        return 1e10


    return -sharpe


def optimize_portfolio(

    maximum_asset_weight

):

    initial_weights = np.repeat(

        1 / n_assets,

        n_assets
    )


    constraints = [

        {

            "type": "eq",

            "fun":
                lambda w:
                np.sum(w) - 1
        }

    ]


    bounds = [

        (

            0,

            maximum_asset_weight

        )

        for _ in range(n_assets)
    ]


    result = minimize(

        negative_sharpe,

        initial_weights,

        method="SLSQP",

        bounds=bounds,

        constraints=constraints,

        options={

            "maxiter":
                1000,

            "ftol":
                1e-12
        }
    )


    if not result.success:

        raise RuntimeError(

            "Optimization failed: "
            +
            result.message
        )


    weights = np.asarray(

        result.x,

        dtype=float
    )


    # Numerical cleanup

    weights[
        np.abs(weights) < 1e-10
    ] = 0.0


    weights = (

        weights
        /
        weights.sum()
    )


    (
        expected_return,

        volatility,

        sharpe

    ) = portfolio_statistics(

        weights,

        expected_returns.values,

        covariance_matrix.values
    )


    return (

        weights,

        expected_return,

        volatility,

        sharpe
    )


# ============================================================
# 40. PORTFOLIO CONSTRAINTS
# ============================================================


maximum_weights = [

    1 / n_assets,

    0.40,

    0.50,

    0.75,

    1.00
]


optimization_results = []


portfolio_weights = {}


for maximum_weight in maximum_weights:

    (

        weights,

        expected_return,

        volatility,

        sharpe

    ) = optimize_portfolio(

        maximum_weight
    )


    portfolio_name = (

        "Equal_Weight"

        if np.isclose(

            maximum_weight,

            1 / n_assets

        )

        else

        f"Max_{int(maximum_weight * 100)}"
    )


    portfolio_weights[
        portfolio_name
    ] = weights


    optimization_results.append(

        {

            "Portfolio":
                portfolio_name,

            "Maximum_Asset_Weight":
                maximum_weight,

            "Expected_Return":
                expected_return,

            "Volatility":
                volatility,

            "Sharpe_Ratio":
                sharpe
        }
    )


optimization_df = pd.DataFrame(
    optimization_results
)


print(
    optimization_df.to_string(
        index=False
    )
)


# ============================================================
# 41. PORTFOLIO WEIGHTS
# ============================================================


print("\n" + "=" * 70)
print("PORTFOLIO WEIGHTS")
print("=" * 70)


for portfolio_name, weights in (
    portfolio_weights.items()
):

    print(
        f"\n{portfolio_name}:"
    )


    for asset, weight in zip(

        selected_assets,

        weights

    ):

        print(

            f"{asset}: "
            f"{weight:.2%}"
        )


# ============================================================
# 42. FROZEN PORTFOLIOS
# ============================================================
#
# These portfolio weights are frozen BEFORE final OOS testing.
#
# No final-test information is used to modify them.
#
# ============================================================


frozen_portfolios = pd.DataFrame(

    portfolio_weights,

    index=selected_assets

).T


print("\n" + "=" * 70)
print("FROZEN PORTFOLIOS")
print("=" * 70)


print(
    frozen_portfolios
)


# Save frozen portfolios

frozen_file = os.path.join(

    OUTPUT_PATH,

    "frozen_portfolios.csv"
)


frozen_portfolios.to_csv(

    frozen_file
)


print(
    "\nFrozen portfolios saved to:"
)

print(
    frozen_file
)


# ============================================================
# 43. PROJECT 01 -> PROJECT 02 HAND-OFF CHECK
# ============================================================
#
# This is the critical data-integrity check.
#
# selected_assets.csv
# and
# frozen_portfolios.csv
#
# MUST contain the same asset universe.
#
# ============================================================


frozen_assets = list(
    frozen_portfolios.columns
)


saved_assets = (

    pd.read_csv(
        selected_assets_file
    )[
        "Asset"
    ]
    .tolist()
)


if set(frozen_assets) != set(
    saved_assets
):

    raise ValueError(

        "PROJECT 01 HAND-OFF FAILED: "
        "selected_assets.csv and "
        "frozen_portfolios.csv contain "
        "different asset universes."
    )


print("\n" + "=" * 70)
print("PROJECT 01 -> PROJECT 02 HAND-OFF CHECK")
print("=" * 70)


print(
    "\nselected_assets.csv:"
)

print(
    saved_assets
)


print(
    "\nfrozen_portfolios.csv assets:"
)

print(
    frozen_assets
)


print(
    "\nHAND-OFF CHECK: PASSED"
)


print(
    "\nProject 02 asset universe:"
)

print(
    saved_assets
)


# ============================================================
# 44. FINAL UNSEEN OOS RETURNS
# ============================================================


final_test_returns = (

    final_test_prices[
        selected_assets
    ]
    .pct_change()
    .dropna()
)


# ============================================================
# 45. OOS PERFORMANCE FUNCTION
# ============================================================


def evaluate_oos_portfolio(
    portfolio_returns
):

    cumulative_return = (

        (1 + portfolio_returns)
        .prod()
        - 1
    )


    annualized_return = (

        (1 + cumulative_return)
        **
        (
            252
            /
            len(portfolio_returns)
        )
        - 1
    )


    annualized_volatility = (

        portfolio_returns.std()
        *
        np.sqrt(252)
    )


    if (

        portfolio_returns.std()
        == 0

    ):

        sharpe = np.nan

    else:

        sharpe = (

            portfolio_returns.mean()
            /
            portfolio_returns.std()
            *
            np.sqrt(252)
        )


    wealth = (

        1
        +
        portfolio_returns
    ).cumprod()


    running_max = (

        wealth
        .cummax()
    )


    drawdown = (

        wealth
        /
        running_max
        - 1
    )


    maximum_drawdown = (
        drawdown.min()
    )


    final_wealth = (
        wealth.iloc[-1]
    )


    return {

        "Total_Return":
            float(
                cumulative_return
            ),

        "Annualized_Return":
            float(
                annualized_return
            ),

        "Volatility":
            float(
                annualized_volatility
            ),

        "Sharpe_Ratio":
            float(
                sharpe
            ),

        "Maximum_Drawdown":
            float(
                maximum_drawdown
            ),

        "Final_Wealth":
            float(
                final_wealth
            )
    }


# ============================================================
# 46. FINAL OOS PORTFOLIO TEST
# ============================================================


print("\n" + "=" * 70)
print("FINAL UNSEEN OUT-OF-SAMPLE RESULTS")
print("=" * 70)


oos_results = []


for portfolio_name, weights in (
    portfolio_weights.items()
):

    portfolio_returns = (

        final_test_returns
        @
        weights
    )


    metrics = (
        evaluate_oos_portfolio(
            portfolio_returns
        )
    )


    oos_results.append(

        {

            "Portfolio":
                portfolio_name,

            **{

                asset:
                    weight

                for asset, weight
                in zip(
                    selected_assets,
                    weights
                )
            },

            **metrics
        }
    )


oos_results_df = pd.DataFrame(
    oos_results
)


print(
    oos_results_df.to_string(
        index=False
    )
)


# Save final OOS asset returns

final_test_returns_file = os.path.join(

    OUTPUT_PATH,

    "final_test_returns.csv"
)


final_test_returns.to_csv(

    final_test_returns_file
)


print(
    "\nFinal OOS returns saved to:"
)

print(
    final_test_returns_file
)


# ============================================================
# 47. TRANSACTION-COST SENSITIVITY
# ============================================================
#
# Frozen portfolios are implemented once at the beginning
# of the OOS period.
#
# Transaction cost is therefore applied to the initial
# implementation turnover.
#
# Sensitivity:
#
#   0 bps
#   10 bps
#   25 bps
#   50 bps
#
# This is a sensitivity analysis, not a claim about
# actual brokerage costs.
#
# ============================================================


print("\n" + "=" * 70)
print("TRANSACTION-COST SENSITIVITY")
print("=" * 70)


transaction_costs = [

    0.0000,

    0.0010,

    0.0025,

    0.0050
]


transaction_results = []


for portfolio_name, weights in (
    portfolio_weights.items()
):

    portfolio_returns = (

        final_test_returns
        @
        weights
    )


    gross_wealth = (

        1
        +
        portfolio_returns
    ).cumprod()


    for cost in transaction_costs:

        # One initial implementation.
        #
        # Starting from cash:
        # turnover = 1.0

        initial_cost = cost


        net_wealth = (

            1 - initial_cost
        ) * gross_wealth


        final_wealth = (
            net_wealth.iloc[-1]
        )


        net_total_return = (
            final_wealth - 1
        )


        running_max = (
            net_wealth.cummax()
        )


        drawdown = (

            net_wealth
            /
            running_max
            - 1
        )


        transaction_results.append(

            {

                "Portfolio":
                    portfolio_name,

                "Transaction_Cost_bps":
                    cost * 10000,

                "Final_Wealth":
                    final_wealth,

                "Net_Total_Return":
                    net_total_return,

                "Maximum_Drawdown":
                    drawdown.min()
            }
        )


transaction_cost_df = pd.DataFrame(
    transaction_results
)


print(
    transaction_cost_df.to_string(
        index=False
    )
)


# ============================================================
# 48. SAVE RESEARCH OUTPUTS
# ============================================================


robustness_file = os.path.join(

    OUTPUT_PATH,

    "hyperparameter_robustness.csv"
)


robustness_df.to_csv(

    robustness_file,

    index=False
)


selection_frequency_file = os.path.join(

    OUTPUT_PATH,

    "selection_frequency.csv"
)


selection_frequency.to_csv(

    selection_frequency_file,

    index=False
)


oos_results_file = os.path.join(

    OUTPUT_PATH,

    "final_oos_results.csv"
)


oos_results_df.to_csv(

    oos_results_file,

    index=False
)


transaction_file = os.path.join(

    OUTPUT_PATH,

    "transaction_cost_sensitivity.csv"
)


transaction_cost_df.to_csv(

    transaction_file,

    index=False
)


factor_file = os.path.join(

    OUTPUT_PATH,

    "final_development_factor_snapshot.csv"
)


final_development_ranking.to_csv(

    factor_file
)


covariance_file = os.path.join(

    OUTPUT_PATH,

    "selected_asset_covariance.csv"
)


covariance_matrix.to_csv(

    covariance_file
)


correlation_file = os.path.join(

    OUTPUT_PATH,

    "selected_asset_correlation.csv"
)


correlation_matrix.to_csv(

    correlation_file
)


# ============================================================
# 49. FINAL RESEARCH SUMMARY
# ============================================================


print("\n" + "=" * 70)
print("PROJECT 01 RESEARCH SUMMARY")
print("=" * 70)


print(
    "\nCandidate universe:"
)

print(
    ASSETS
)


print(
    "\nBaseline reference specification:"
)

print(
    BASELINE_PARAMS
)


print(
    "\nFactor weights:"
)

print(
    "Beta:       25%"
)

print(
    "Momentum:   25%"
)

print(
    "Volatility: 25%"
)

print(
    "Sharpe:     25%"
)


print(
    "\nBaseline reference assets:"
)

print(
    baseline_assets
)


print(
    "\nNumber of robustness configurations:"
)

print(
    len(robustness_df)
)


print(
    "\nBest validation Sharpe:"
)

print(
    best_validation_sharpe
)


print(
    "\nMost frequently selected universe:"
)

print(
    most_frequent_assets
)


print(
    "\nSelection frequency:"
)

print(

    f"{most_frequent_count}/"
    f"{len(robustness_df)}"
)


print(
    "\nSelection frequency percentage:"
)

print(
    f"{most_frequent_percentage:.2f}%"
)


print(
    "\nRepresentative robust parameters:"
)

print(
    REPRESENTATIVE_PARAMS
)


print(
    "\nRepresentative validation Sharpe:"
)

print(
    representative_row[
        "Validation_Sharpe"
    ]
)


print(
    "\nRepresentative parameter distance:"
)

print(
    representative_row[
        "Parameter_Distance"
    ]
)


print(
    "\nFINAL PROJECT 01 ASSET UNIVERSE:"
)

print(
    selected_assets
)


print(
    "\nBenchmark:"
)

print(
    "Equal Weight"
)


print(
    "\nAlternative portfolios:"
)

print(
    "Max-40"
)

print(
    "Max-50"
)

print(
    "Max-75"
)

print(
    "Max-100"
)


print(
    "\nFinal unseen OOS period:"
)

print(
    final_test_prices.index.min(),
    "to",
    final_test_prices.index.max()
)


print(
    "\nOutputs saved to:"
)

print(
    OUTPUT_PATH
)


# ============================================================
# 50. FINAL ROBUSTNESS CONCLUSION
# ============================================================


print("\n" + "=" * 70)
print("PROJECT 01 ROBUSTNESS CONCLUSION")
print("=" * 70)


print(
    "\n1. BASELINE"
)

print(
    "The baseline specification "
    "(60, 60, 20, 60) was used only "
    "as a reference specification."
)


print(
    "\n2. FACTOR MODEL"

)

print(
    "Beta, Momentum, Volatility and Sharpe "
    "were included with equal 25% factor weights."
)


print(
    "\n3. ROBUSTNESS GRID"

)

print(
    f"The robustness analysis tested "
    f"{len(robustness_df)} parameter combinations."
)


print(
    "\n4. BEST VALIDATION PERFORMANCE"

)

print(
    f"Best validation Sharpe = "
    f"{best_validation_sharpe:.6f}"
)


print(
    "\n5. ASSET-SELECTION ROBUSTNESS"

)

print(
    f"The universe {most_frequent_assets} "
    f"was selected by "
    f"{most_frequent_count} of "
    f"{len(robustness_df)} configurations "
    f"({most_frequent_percentage:.2f}%)."
)


print(
    "\nTherefore:"
)

print(
    "AAPL + GOOG + META was not dependent "
    "on one lucky parameter configuration."
)


print(
    "\n6. REPRESENTATIVE PARAMETER SELECTION"

)

print(
    "Among configurations achieving the "
    "best validation Sharpe, the representative "
    "configuration was selected using:"
)


print(
    "   First  -> highest validation Sharpe"
)

print(
    "   Second -> smallest distance from baseline"
)

print(
    "   Third  -> smaller volatility window "
    "as deterministic tie-break"
)


print(
    "\nBaseline:"
)

print(
    "(60, 60, 20, 60)"
)


print(
    "\nRepresentative:"
)

print(
    (
        REPRESENTATIVE_PARAMS[
            "Beta_Window"
        ],

        REPRESENTATIVE_PARAMS[
            "Momentum_Window"
        ],

        REPRESENTATIVE_PARAMS[
            "Volatility_Window"
        ],

        REPRESENTATIVE_PARAMS[
            "Sharpe_Window"
        ]
    )
)


print(
    "\n7. FROZEN UNIVERSE"

)

print(
    "The representative robustness-selected "
    "universe was frozen before final OOS testing."
)


print(
    "\n8. PROJECT 02 HAND-OFF"

)

print(
    "selected_assets.csv and frozen_portfolios.csv "
    "were generated from the same frozen universe."
)


print(
    "\nProject 01 -> Project 02 hand-off:"
)

print(
    "PASSED"
)


print(
    "\n9. FINAL PROJECT 01 UNIVERSE:"
)

print(
    selected_assets
)


print(
    "\n10. OOS TEST"

)

print(
    "The frozen portfolios were evaluated on "
    "completely unseen final-test data."
)


print(
    "\nProject 01 research conclusion:"
)

print(
    "The final asset universe is supported by "
    "parameter robustness rather than reliance "
    "on a single optimized parameter combination."
)


print(
    "\nProject 01 ends here."
)


print(
    "Benchmark-relative risk and performance "
    "attribution belongs to Project 02."
)


print("\n" + "=" * 70)
print("PROJECT 01 COMPLETED")
print("=" * 70)
