# Decision Log

This file records architectural and implementation decisions using a list format.
2025-08-03 18:22:03 - Log of updates made.

*

## Decision

*   Use `yf.Ticker(ticker).history()` instead of `yf.download()` for fetching stock data.

## Rationale

*   The `yf.download()` function was returning a DataFrame with a MultiIndex, which caused compatibility issues with the `pandas_ta` library. The `yf.Ticker(ticker).history()` method provides a more consistent and predictable DataFrame structure.

## Implementation Details

*   The `get_support_resistance`, `get_rsi_analysis`, `get_macd_analysis`, and `get_macd_trend` functions in the backend were updated to use the new data fetching method.
* * *

[2025-08-04 22:00:00] - Corrected Support/Resistance Calculation Logic

## Decision

*   Refactored the support and resistance calculation to correctly classify levels relative to the current price.

## Rationale

*   The previous implementation incorrectly pooled support and resistance levels, causing them to be inverted. The new logic ensures that support levels are always below the current price and resistance levels are always above it.

## Implementation Details

*   The `get_support_resistance` function in `backend/api/support_resistance/services.py` was updated to:
    1.  Combine all potential levels into a single list.
    2.  Filter out invalid and duplicate values.
    3.  Separate the levels into `supports` (below current price) and `resistances` (above current price).
    4.  Return the three closest support and resistance levels.
* * *

[2025-08-04 22:10:00] - Changed RSI Calculation Period

## Decision

*   Changed the RSI calculation period from 14 to 6 in the RSI analysis feature.

## Rationale

*   The user requested a shorter RSI period for the analysis, likely to make it more sensitive to recent price changes.

## Implementation Details

*   The `get_rsi_analysis` function in `backend/api/rsi_analysis/services.py` was updated to use `length=6` in the `data.ta.rsi()` call.
*   The column name used for filtering was updated from `RSI_14` to `RSI_6`.
* * *

[2025-08-04 22:38:00] - Added Candlestick Chart to RSI Analysis Page

## Decision

*   Implemented a feature to display a candlestick chart in a dialog when a user clicks on a row in the RSI analysis results table.

## Rationale

*   The user requested this feature to provide more detailed, visual analysis of the stock data related to the RSI signals.

## Implementation Details

*   Created a new backend endpoint (`/api/stock_history`) to fetch historical stock data with technical indicators (RSI, MACD, and multiple moving averages).
*   Created a new React component (`StockChartDialog.js`) to display the candlestick chart using the `react-stockcharts` library.
*   Modified the `RsiAnalysis.js` page to open the dialog and pass the relevant data when a table row is clicked.