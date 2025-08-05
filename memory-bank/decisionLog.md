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
* * *

[2025-08-05 12:37:49] - Replaced `react-stockcharts` with `@react-financial-charts`

## Decision

*   Switched from the unmaintained `react-stockcharts` library to the actively maintained `@react-financial-charts` fork.

## Rationale

*   The `react-stockcharts` library was causing a "subscribe is not a function" TypeError due to incompatibility with modern React versions (16.3+).
*   The `@react-financial-charts` library is a drop-in replacement that resolves this issue and ensures ongoing compatibility and support.

## Implementation Details

*   Uninstalled `react-stockcharts`.
*   Installed the following packages: `@react-financial-charts/core`, `@react-financial-charts/series`, `@react-financial-charts/axes`, `@react-financial-charts/tooltip`, `d3-format`, `d3-time-format`, and `prop-types`.
*   Updated the import statements in `frontend/src/components/StockChartDialog.js` to reflect the new package structure.
* * *

[2025-08-05 12:40:11] - Corrected Charting Library Implementation

## Decision

*   Installed missing `@react-financial-charts/indicators` and `@react-financial-charts/coordinates` packages.
*   Corrected the import path for `CrossHairCursor` in `frontend/src/components/StockChartDialog.js`.

## Rationale

*   The previous implementation was missing necessary packages and had an incorrect import path, which caused the application to fail.

## Implementation Details

*   Installed the missing packages using `npm install`.
*   Updated the import statement for `CrossHairCursor` to import from `@react-financial-charts/coordinates`.
* * *

[2025-08-05 12:46:41] - Fixed MACD Tooltip Rendering Issue

## Decision

*   Explicitly defined and passed `appearance` properties to the `MACDSeries` and `MACDTooltip` components in `frontend/src/components/StockChartDialog.js`.

## Rationale

*   The application was crashing with a `TypeError: Cannot read properties of undefined (reading 'strokeStyle')` because the `MACDTooltip` was not receiving the necessary styling information from the `MACDSeries`.

## Implementation Details

*   Created a `macdAppearance` object to define the `strokeStyle` and `fillStyle` for the MACD indicator.
*   Passed the `macdAppearance` object to the `MACDSeries` component.
*   Passed both the `options` from the `macdIndicator` and the `macdAppearance` object to the `MACDTooltip` component.
* * *

[2025-08-05 13:07:42] - Fixed Empty Candlestick Chart Issue

## Decision

*   Moved all technical indicator calculations from the frontend to the backend.
*   Standardized the data format sent from the backend to match what the frontend charting library expects.

## Rationale

*   The candlestick chart was not rendering because of a mismatch between the data provided by the backend and the data expected by the frontend. The frontend was performing its own calculations, which were incompatible with the data structure it received.

## Implementation Details

*   **Backend (`backend/api/stock_history/services.py`):**
    *   Changed the moving average calculation from SMA to EMA to match the frontend's requirements.
    *   Renamed the technical indicator columns (e.g., `RSI_6` to `rsi`) to provide a consistent and predictable data structure.
*   **Frontend (`frontend/src/components/StockChartDialog.js`):**
    *   Removed all frontend-based technical indicator calculations (`ema`, `rsi`, `macd`).
    *   Modified the chart components to use the pre-calculated indicator data directly from the API response.
* * *

[2025-08-05 13:13:36] - Fixed Data Structure and Case-Sensitivity Issues

## Decision

*   Modified the backend to convert all data keys to lowercase.
*   Restructured the MACD data into a nested object.
*   Updated the frontend to correctly parse the new data structure.

## Rationale

*   The chart was not rendering due to a case-sensitivity mismatch between the backend data keys (e.g., `Close`) and the frontend's expected keys (e.g., `close`).
*   The MACD chart's vertical axis was not being calculated correctly because the data was not in the expected nested format.

## Implementation Details

*   **Backend (`backend/api/stock_history/services.py`):**
    *   Converted all DataFrame column names to lowercase before returning the JSON response.
    *   Created a nested `macd` object containing the `macd`, `signal`, and `divergence` values.
*   **Frontend (`frontend/src/components/StockChartDialog.js`):**
    *   Updated the `parsedData` mapping to use the lowercase `date` key.
    *   Modified the `yExtents` for the MACD chart to correctly calculate the min/max values from the nested `macd` object.
* * *

[2025-08-05 13:18:11] - Fixed `KeyError` in Backend Service

## Decision

*   Added a check in the backend service to ensure that MACD columns exist before attempting to process them.

## Rationale

*   The application was crashing with a `KeyError: 'macd_value'` when the historical data was too short to calculate the MACD indicator.

## Implementation Details

*   **Backend (`backend/api/stock_history/services.py`):**
    *   Added a conditional check to see if the `macd_value`, `macd_signal`, and `macd_histogram` columns exist in the DataFrame.
    *   If the columns exist, they are nested into a `macd` object as before.
    *   If the columns do not exist, the `macd` column is set to `None` to prevent the application from crashing.
* * *

[2025-08-05 13:22:18] - Fixed Frontend Crash with Null MACD Data

## Decision

*   Added a conditional check in the frontend component to ensure that the MACD chart is only rendered when the `macd` data is not `null`.

## Rationale

*   The application was crashing with a `TypeError: Cannot read properties of null (reading 'macd')` when the backend returned `null` for the `macd` field.

## Implementation Details

*   **Frontend (`frontend/src/components/StockChartDialog.js`):**
    *   Wrapped the MACD `Chart` component in a conditional check (`data.some(d => d.macd) && ...`) to ensure it only renders when at least one data point has a non-null `macd` value.
    *   Added a ternary operator to the `yExtents` of the MACD chart to prevent errors when the `macd` data is `null`.
* * *

[2025-08-05 13:32:09] - Acknowledged `UNSAFE_componentWillMount` Warning

## Decision

*   Acknowledged the `UNSAFE_componentWillMount` warning originating from the `@react-financial-charts` library. No code changes will be made to address this.

## Rationale

*   The warning is an internal issue within the third-party library and does not cause any functional problems or crashes in the application.
*   The project is already using the latest version of the library, so an update is not possible.
*   Suppressing the warning is the most practical approach, as directly modifying the library's code is not feasible.

## Implementation Details

*   No code changes were implemented. The decision was made to accept the warning as a known issue with the third-party dependency.
* * *

[2025-08-05 13:38:45] - Fixed State Management Issue in Stock Chart Dialog

## Decision

*   Added a `useEffect` hook to the `StockChartDialog` component to reset its internal `data` state to `null` whenever the dialog is closed.

## Rationale

*   The application was crashing with a `TypeError: Cannot read properties of null (reading 'date')` when reopening the chart for the same stock. This was caused by the component retaining stale data from the previous render.

## Implementation Details

*   **Frontend (`frontend/src/components/StockChartDialog.js`):**
    *   A new `useEffect` hook was added that triggers when the `open` prop changes.
    *   If the `open` prop is `false`, the `setData` state updater is called with `null` to clear the old chart data.
* * *

[2025-08-05 13:43:21] - Removed Technical Indicators from Stock Chart

## Decision

*   Removed all technical indicators (MACD, RSI, and Moving Averages) from the stock chart feature.

## Rationale

*   The user requested a cleaner chart that only displays the candlestick series.

## Implementation Details

*   **Backend (`backend/api/stock_history/services.py`):**
    *   Removed all code related to calculating and returning technical indicators.
*   **Frontend (`frontend/src/components/StockChartDialog.js`):**
    *   Removed all imports, components, and logic related to displaying the indicator charts and tooltips.