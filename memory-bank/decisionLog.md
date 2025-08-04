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