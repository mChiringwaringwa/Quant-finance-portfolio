# ============================================================
# PROJECT 02
# PORTFOLIO RISK & PERFORMANCE ANALYTICS
# ============================================================

# ------------------------------------------------------------
# 1. IMPORT LIBRARIES
# ------------------------------------------------------------

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf


# ------------------------------------------------------------
# 2. PROJECT SETTINGS
# ------------------------------------------------------------

assets = ["AAPL", "MSFT", "NVDA", "GOOG", "META"]

start_date = "2025-07-16"
end_date = "2026-07-15"


# ------------------------------------------------------------
# 3. DOWNLOAD PRICE DATA
# ------------------------------------------------------------

prices = yf.download(
    assets,
    start=start_date,
    end=end_date,
    auto_adjust=True
)["Close"]


# ------------------------------------------------------------
# 4. CALCULATE DAILY RETURNS
# ------------------------------------------------------------

returns = prices.pct_change().dropna()


# ------------------------------------------------------------
# 5. INSPECT DATA
# ------------------------------------------------------------

print("Price Data:")
print(prices.head())

print("\nDaily Returns:")
print(returns.head())

print("\nNumber of observations:", len(returns))
