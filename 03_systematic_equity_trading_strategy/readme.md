### Project 03 — Systematic Short-Term Trading Engine

## 1. Project Overview

Project 03 develops and validates a systematic short-term trading overlay applied to the portfolio selected and frozen in Project 01.

The objective is not to redefine the investment universe or optimise portfolio weights. Instead, Project 03 asks:

> Can a systematic technical trading strategy improve the risk-adjusted behaviour of the frozen portfolio by dynamically controlling short-term market exposure?

The trading engine uses:

- Simple Moving Average (SMA) trend signals
- Relative Strength Index (RSI)
- Parameter optimisation
- Chronological development/final-test separation
- Expanding walk-forward validation
- Rolling walk-forward validation
- Parameter sensitivity analysis
- Regime robustness analysis
- Active exposure diagnostics
- Final unseen out-of-sample testing

The strategy is applied to the same assets selected by Project 01.

---

## 2. Relationship with the Other Projects

The three projects form a single quantitative investment research pipeline:

```text
PROJECT 01
Asset Selection & Portfolio Construction
                |
                | Frozen portfolio specification
                v
PROJECT 02
Portfolio Risk & Performance Analytics
                |
                | Same frozen portfolio
                v
PROJECT 03
Systematic Short-Term Trading Engine

```
Each project answers a different question.

> Project 01
Which assets should be selected and how should the portfolio be constructed?

> Project 02
How did the selected portfolio perform and what risks did it carry?

> Project 03
Can systematic short-term trading control exposure to the same selected portfolio?

This separation prevents Project 03 from redefining the investment universe or changing the strategic portfolio weights.

## 3. Frozen Portfolio
Project 03 inherits the portfolio specification from Project 01.
The selected portfolio used in the trading engine is:

|Asset | Frozen Weight|
|------|---------------|
|AAPL | 40%|
|GOOG | 40%|
|META | 20%|

The weights are treated as fixed inputs.

Project 03:
- does not select assets;
- does not optimise portfolio weights;
- does not replace the Project 01 portfolio;
- does not perform asset selection.
- Trading parameters are optimised independently of portfolio construction.

## 4. Investment Universe
The trading universe is therefore:
  AAPL
  GOOG
  META
These assets are inherited from the frozen Project 01 portfolio.

The trading signal is calculated separately for each asset, while the resulting asset-level returns are aggregated using the frozen portfolio weights.

## 5. Trading Strategy
The strategy combines trend and momentum information.

> 5.1 Moving Average Signal
Two simple moving averages are calculated:

```text
SMA_short,t 
And:
SMA_long,t

A bullish trend condition occurs when:
SMA_short,t > SMA_long,t 

The signal is therefore:
Signal = 1  → Invested
Signal = 0  → No exposure / Cash

```
> 5.2 RSI Filter
A 14-period Relative Strength Index is calculated.

The strategy requires:
RSI > RSI_threshold
Therefore, the long signal is:

```text
           |--1, SMA_short,t > SMA_long,t & RSI > RSI_threshold
Signal_t = |
           |--0, otherwise

where:
1 = invested
0 = no exposure / cash
```
## 6. Avoiding Look-Ahead Bias
The trading signal is lagged by one trading day before being applied to returns.

```text
The strategy return is:
R_strategy,t = Signal_t-1 * R_t

Rather than:
Signal_t * R_t 

```
This ensures that information from day (t) is not used to generate a return on the same day.

This provides an important safeguard against look-ahead bias.


## 7. Portfolio-Level Trading Return
Signals are generated at the individual asset level.

The resulting strategy returns are then combined using the frozen Project 01 weights.

```text
For the frozen portfolio:
R_portfolio,t = 0.40R_AAPL,t + 0.40R_GOOG,t + 0.20R_META,t

where each asset return has already been adjusted by its trading signal.

Importantly, active assets are not renormalised.

For example, if:
AAPL = invested
GOOG = not invested
META = invested

the exposure remains:
AAPL = 40%
GOOG = 0%
META = 20%

rather than being rescaled to:
AAPL = 66.67%
META = 33.33%

```
The difference is important because renormalisation would change the frozen Project 01 portfolio specification.

## 8. Development / Final Test Framework
The historical sample is divided chronologically into:

```text
80% Development
20% Final Unseen Test

No future observations from the final test period are used during parameter selection.

Development Period
28 July 2025
        to
1 May 2026
Observations:
193

Final Unseen Test Period
4 May 2026
        to
14 July 2026
Observations:
49
```
The final test therefore represents observations that were not used in the initial parameter-selection process.

## 9. Parameter Optimisation
The initial parameter grid tested:
```text
Short SMA
10
15
20
25

Long SMA
40
50
60

RSI Threshold
60
70
80

Total combinations:
4 * 3 * 3 = 36
```
Therefore:
36 parameter combinations were evaluated on the development period.

Invalid combinations where the short window was greater than or equal to the long window were excluded.

## 10. Development-Period Result
The best development specification was:
```text
Short SMA = 25
Long SMA  = 40
RSI       = 60
Development return:
7.388%
```
This specification was then carried forward for the fixed-strategy comparison.

Importantly, the development result is not treated as evidence of future profitability.

It was used only to establish the trading specification before the final unseen test.

## 11. Expanding Walk-Forward Validation
To test whether parameter optimisation remains useful through time, an expanding walk-forward procedure was implemented.

Configuration:
```text
Training window = 100 observations
Test window     = 30 observations
```
At each step:
- Train using historical observations only.
- Test the available trading parameter combinations.
- Select the best parameters.
- Apply those parameters to the next unseen test window.
- Expand the training sample.
- Repeat.

This simulates a researcher periodically recalibrating the trading strategy as additional historical information becomes available.

> Expanding Parameter Selections
The optimisation selected:
```text
Short = 25
Long  = 60
RSI   = 60
```
for all three reported test windows.
This indicates strong parameter stability across the expanding training windows.

## 12. Expanding Walk-Forward Results

|Method  | Average Return  | Total Compounded Return| 
|-------- |------------------ |------------------ |
|Optimized  | -0.355%  | -1.074% |
|Fixed  | 0.986%  | 2.973% |
|Buy & Hold  | 2.067%  | 5.529% |

The optimised strategy did not outperform the fixed strategy or Buy & Hold during the expanding walk-forward test.

Robustness statistics were:
```text
Average Optimized − Fixed = -0.013408
Std. Dev. Difference      = 0.007588
T-statistic               = -3.060644
Optimized Wins             = 0
```
This is an important research result.

It indicates that frequent re-optimisation did not improve performance during the observed expanding walk-forward periods.

## 13. Rolling Walk-Forward Validation
A rolling walk-forward procedure was also implemented.

Unlike the expanding approach, the rolling approach keeps the training window at a fixed length.

Configuration:
```text
Training window = 100 observations
Test window     = 30 observations
```
At each step, the model is trained on the most recent 100 observations and tested on the following 30 observations.

This provides a second way of assessing whether parameter adaptation improves out-of-sample performance.

## 14. Rolling Walk-Forward Results

|Method | Average Return | Total Compounded Return|
|-------- |------------------ |------------------ |
|Optimized | -0.026% | -0.958%|
|Fixed | 0.986% | 2.973%|
|Buy & Hold | 2.067% | 5.529%|

Rolling robustness statistics:
```text
Average Optimized − Fixed = -0.010116
Std. Dev. Difference      = 0.003696
T-statistic               = -4.740825
Optimized Wins             = 0
```
Again, rolling optimisation did not improve performance relative to the fixed specification.

## 15. Parameter Stability
The walk-forward parameter history showed:
```text
Expanding

25 / 60 / 60
25 / 60 / 60
25 / 60 / 60

Rolling
25 / 60 / 60
25 / 50 / 60
20 / 40 / 60
```
The expanding procedure therefore showed stronger parameter stability, while the rolling procedure adapted more substantially to recent observations.

However, the additional adaptation did not translate into better walk-forward performance.

## 16. Parameter Sensitivity Analysis
A separate sensitivity analysis was performed over:
```text
Short SMA = 8 to 17
Long SMA  = 38 to 52
RSI       = 70
```
The resulting heatmap examines development-period return across combinations of short and long moving-average windows.

The heatmap shows a relatively broad region of stronger development-period performance rather than a single isolated optimum.

The stronger region is approximately concentrated around:
```text
Short SMA ≈ 14–17
Long SMA  ≈ 43–52
```
This provides evidence that development performance is not exclusively dependent on one precise SMA combination within this sensitivity region.

However, the sensitivity analysis fixes RSI at 70 and therefore does not directly test the selected 25/40/60 specification.

Consequently, the heatmap should be interpreted as a parameter sensitivity analysis, not as confirmation that 25/40/60 is the universal optimum.

## 17. Regime Robustness
The strategy was also evaluated across different market regimes.

The regime framework combines trend and volatility information to distinguish environments such as:
```text
Bull_LowVol
Bull_HighVol
Bear_LowVol
Bear_HighVol
```
The purpose is to investigate whether strategy behaviour changes depending on market conditions.

Development-period results showed meaningful differences between regimes.
