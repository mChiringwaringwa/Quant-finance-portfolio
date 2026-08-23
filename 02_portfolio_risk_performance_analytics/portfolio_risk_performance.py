# ============================================================
# PROJECT 02
# PORTFOLIO RISK & PERFORMANCE ANALYTICS
# ============================================================

# ------------------------------------------------------------
# 1. IMPORT LIBRARIES
# ------------------------------------------------------------

import numpy as np
import pandas as pd


# ------------------------------------------------------------
# 2. PROJECT SETTINGS
# ------------------------------------------------------------

assets = ["AAPL", "MSFT", "NVDA", "GOOG", "META"]

initial_capital = 1.0
risk_free_rate = 0.0
trading_days = 252


# ------------------------------------------------------------
# 3. LOAD SAVED PRICE DATA
# ------------------------------------------------------------

# Update these filenames if your CSV files use different names.

files = {
    "AAPL": "AAPL.csv",
    "MSFT": "MSFT.csv",
    "NVDA": "NVDA.csv",
    "GOOG": "GOOG.csv",
    "META": "META.csv"
}


price_data = {}

for asset in assets:

    df = pd.read_csv(
        files[asset],
        parse_dates=["Date"]
    )

    df = df.set_index("Date")

    price_data[asset] = df["Close"]


prices = pd.concat(
    price_data,
    axis=1
)

prices.columns = assets

prices = prices.sort_index()


# ------------------------------------------------------------
# 4. ALIGN DATA
# ------------------------------------------------------------

prices = prices.dropna()


# ------------------------------------------------------------
# 5. CALCULATE DAILY RETURNS
# ------------------------------------------------------------

returns = prices.pct_change().dropna()


# ------------------------------------------------------------
# 6. INSPECT DATA
# ------------------------------------------------------------

print("=" * 60)
print("PORTFOLIO RISK & PERFORMANCE ANALYTICS")
print("=" * 60)

print("\n--- PRICE DATA ---")
print(prices.head())

print("\n--- DAILY RETURNS ---")
print(returns.head())

print("\nNumber of observations:", len(returns))

print("\nStart date:", prices.index.min())
print("End date:", prices.index.max())


# ============================================================
# 7. PORTFOLIO DEFINITIONS
# ============================================================

portfolios = {

    "Equal_Weight": {
        "AAPL": 1 / 5,
        "MSFT": 1 / 5,
        "NVDA": 1 / 5,
        "GOOG": 1 / 5,
        "META": 1 / 5
    },

    "AAPL_GOOG_META": {
        "AAPL": 1 / 3,
        "GOOG": 1 / 3,
        "META": 1 / 3
    },

    "AAPL_GOOG": {
        "AAPL": 0.50,
        "GOOG": 0.50
    }
}


# ============================================================
# 8. PORTFOLIO RETURN FUNCTION
# ============================================================

def calculate_portfolio_returns(
    returns,
    weights
):

    weights = pd.Series(weights)

    weights = weights.reindex(
        returns.columns,
        fill_value=0.0
    )

    portfolio_returns = returns.dot(weights)

    return portfolio_returns


# ============================================================
# 9. PERFORMANCE METRICS
# ============================================================

def calculate_performance(
    portfolio_returns,
    risk_free_rate=0.0
):

    total_return = (
        (1 + portfolio_returns).prod() - 1
    )

    annualized_return = (
        portfolio_returns.mean()
        * trading_days
    )

    annualized_volatility = (
        portfolio_returns.std()
        * np.sqrt(trading_days)
    )

    if annualized_volatility != 0:

        sharpe_ratio = (
            annualized_return - risk_free_rate
        ) / annualized_volatility

    else:

        sharpe_ratio = np.nan

    wealth_index = (
        1 + portfolio_returns
    ).cumprod()

    running_max = wealth_index.cummax()

    drawdown = (
        wealth_index / running_max
    ) - 1

    maximum_drawdown = drawdown.min()

    return {
        "Total_Return": total_return,
        "Annualized_Return": annualized_return,
        "Annualized_Volatility": annualized_volatility,
        "Sharpe_Ratio": sharpe_ratio,
        "Maximum_Drawdown": maximum_drawdown
    }


# ============================================================
# 10. CALCULATE PORTFOLIO PERFORMANCE
# ============================================================

performance_results = []

portfolio_return_series = {}

for name, weights in portfolios.items():

    portfolio_returns = calculate_portfolio_returns(
        returns,
        weights
    )

    portfolio_return_series[name] = portfolio_returns

    metrics = calculate_performance(
        portfolio_returns,
        risk_free_rate
    )

    metrics["Portfolio"] = name

    performance_results.append(metrics)


performance_df = pd.DataFrame(
    performance_results
)

performance_df = performance_df[
    [
        "Portfolio",
        "Total_Return",
        "Annualized_Return",
        "Annualized_Volatility",
        "Sharpe_Ratio",
        "Maximum_Drawdown"
    ]
]


# ============================================================
# 11. DISPLAY PERFORMANCE
# ============================================================

print("\n" + "=" * 60)
print("PORTFOLIO PERFORMANCE")
print("=" * 60)

print(
    performance_df.to_string(
        index=False
    )
)


# ============================================================
# 12. COVARIANCE MATRIX
# ============================================================

annualized_covariance = (
    returns.cov()
    * trading_days
)

print("\n" + "=" * 60)
print("ANNUALIZED COVARIANCE MATRIX")
print("=" * 60)

print(
    annualized_covariance
)


# ============================================================
# 13. CORRELATION MATRIX
# ============================================================

correlation_matrix = returns.corr()

print("\n" + "=" * 60)
print("CORRELATION MATRIX")
print("=" * 60)

print(
    correlation_matrix
)


# ============================================================
# 14. PORTFOLIO RISK CONTRIBUTION
# ============================================================

def calculate_risk_contribution(
    returns,
    weights
):

    weights = pd.Series(weights)

    weights = weights.reindex(
        returns.columns,
        fill_value=0.0
    )

    covariance_matrix = (
        returns.cov()
    )

    weights_array = weights.values

    portfolio_variance = (
        weights_array
        @ covariance_matrix.values
        @ weights_array
    )

    portfolio_volatility = np.sqrt(
        portfolio_variance
    )

    sigma_w = (
        covariance_matrix
        @ weights_array
    )

    marginal_risk = (
        sigma_w
        / portfolio_volatility
    )

    component_risk = (
        weights_array
        * marginal_risk
    )

    risk_contribution = (
        component_risk
        / portfolio_volatility
    )

    result = pd.DataFrame({

        "Weight": weights_array,

        "Marginal_Risk_Contribution":
            marginal_risk,

        "Component_Risk_Contribution":
            component_risk,

        "Risk_Contribution_%":
            risk_contribution * 100
    })

    result.index = weights.index

    return (
        portfolio_variance,
        portfolio_volatility,
        result
    )


# ============================================================
# 15. RISK CONTRIBUTION FOR SELECTED PORTFOLIO
# ============================================================

selected_portfolio = portfolios[
    "AAPL_GOOG_META"
]

(
    portfolio_variance,
    portfolio_volatility,
    risk_contribution_df
) = calculate_risk_contribution(
    returns[
        ["AAPL", "GOOG", "META"]
    ],
    selected_portfolio
)


print("\n" + "=" * 60)
print("PORTFOLIO RISK CONTRIBUTION")
print("=" * 60)

print(
    risk_contribution_df
)


print(
    "\nPortfolio Variance:",
    portfolio_variance
)

print(
    "Portfolio Volatility:",
    portfolio_volatility
)

print(
    "\nTotal Risk Contribution:",
    risk_contribution_df[
        "Risk_Contribution_%"
    ].sum()
)


# ============================================================
# 16. ACTIVE PERFORMANCE ANALYSIS
# ============================================================

benchmark = portfolio_return_series[
    "Equal_Weight"
]

portfolio = portfolio_return_series[
    "AAPL_GOOG_META"
]

active_returns = (
    portfolio - benchmark
)

active_total_return = (
    (1 + portfolio).prod()
    / (1 + benchmark).prod()
) - 1

tracking_error = (
    active_returns.std()
    * np.sqrt(trading_days)
)

annualized_active_return = (
    active_returns.mean()
    * trading_days
)

if tracking_error != 0:

    information_ratio = (
        annualized_active_return
        / tracking_error
    )

else:

    information_ratio = np.nan


# ============================================================
# 17. ACTIVE PERFORMANCE OUTPUT
# ============================================================

print("\n" + "=" * 60)
print("ACTIVE PERFORMANCE ANALYSIS")
print("=" * 60)

print(
    "Active Total Return:",
    active_total_return
)

print(
    "Annualized Active Return:",
    annualized_active_return
)

print(
    "Annualized Tracking Error:",
    tracking_error
)

print(
    "Information Ratio:",
    information_ratio
)


# ============================================================
# 18. TRANSACTION COST SENSITIVITY
# ============================================================

transaction_costs = [
    0.0000,
    0.0010,
    0.0025,
    0.0050
]

transaction_results = []

portfolio_returns = portfolio_return_series[
    "AAPL_GOOG_META"
]

# Equal fixed weights imply zero turnover after
# initial allocation, so transaction costs are applied
# to the initial portfolio formation.

initial_turnover = 1.0

for cost in transaction_costs:

    transaction_cost = (
        initial_turnover
        * cost
    )

    adjusted_returns = (
        portfolio_returns.copy()
    )

    adjusted_returns.iloc[0] -= (
        transaction_cost
    )

    metrics = calculate_performance(
        adjusted_returns,
        risk_free_rate
    )

    metrics["Transaction_Cost"] = cost

    transaction_results.append(
        metrics
    )


transaction_df = pd.DataFrame(
    transaction_results
)


print("\n" + "=" * 60)
print("TRANSACTION COST SENSITIVITY")
print("=" * 60)

print(
    transaction_df[
        [
            "Transaction_Cost",
            "Total_Return",
            "Annualized_Return",
            "Annualized_Volatility",
            "Sharpe_Ratio",
            "Maximum_Drawdown"
        ]
    ].to_string(index=False)
)


# ============================================================
# 19. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("PROJECT SUMMARY")
print("=" * 60)

best_portfolio = (
    performance_df
    .sort_values(
        "Sharpe_Ratio",
        ascending=False
    )
    .iloc[0]
)

print(
    "Best Portfolio by Sharpe:",
    best_portfolio["Portfolio"]
)

print(
    "Sharpe Ratio:",
    best_portfolio["Sharpe_Ratio"]
)

print(
    "Total Return:",
    best_portfolio["Total_Return"]
)

print(
    "Maximum Drawdown:",
    best_portfolio["Maximum_Drawdown"]
)

print("\nAnalysis complete.")
