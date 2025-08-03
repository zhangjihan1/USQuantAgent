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