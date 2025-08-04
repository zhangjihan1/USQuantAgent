import yfinance as yf
import pandas as pd
import numpy as np

def get_support_resistance(ticker):
    """
    Calculates support and resistance levels for a given stock ticker.
    """
    stock = yf.Ticker(ticker)
    data = stock.history(period="3y", interval="1d")
    if data.empty:
        return {"error": "Could not download data for the ticker."}

    data = data.copy()
    data['High'] = data['High'].astype(float)
    data['Low'] = data['Low'].astype(float)
    data['Close'] = data['Close'].astype(float)

    # 1. Swing Highs and Lows
    support_levels = data['Low'].rolling(window=14, min_periods=1).min()
    resistance_levels = data['High'].rolling(window=14, min_periods=1).max()

    # 2. Moving Averages
    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['MA200'] = data['Close'].rolling(window=200).mean()

    # 3. Pivot Points
    last_day = data.iloc[-1]
    pivot = (last_day['High'] + last_day['Low'] + last_day['Close']) / 3
    s1 = (2 * pivot) - last_day['High']
    r1 = (2 * pivot) - last_day['Low']
    s2 = pivot - (last_day['High'] - last_day['Low'])
    r2 = pivot + (last_day['High'] - last_day['Low'])

    # 4. Psychological Levels
    last_price = data.tail(1)['Close'].iloc[0]
    if np.isnan(last_price):
        round_numbers = []
    else:
        round_numbers = [round(last_price, -1) + i * 10 for i in range(-5, 6)]

    # Combine all potential levels, clean them, and classify them
    last_price = data['Close'].iloc[-1]
    all_levels = (
        list(support_levels.tail(5).values) +
        list(resistance_levels.tail(5).values) +
        [s1, s2, r1, r2] +
        list(data['MA50'].tail(1).values) +
        list(data['MA200'].tail(1).values) +
        round_numbers
    )

    # Remove NaN and duplicates
    all_levels = sorted(list(set([l for l in all_levels if not np.isnan(l)])))

    # Separate into support and resistance based on the last price
    supports = [level for level in all_levels if level < last_price]
    resistances = [level for level in all_levels if level > last_price]

    # Get the 3 closest support levels (highest values below current price)
    final_supports = sorted(supports, reverse=True)[:3]

    # Get the 3 closest resistance levels (lowest values above current price)
    final_resistances = sorted(resistances)[:3]

    return {
        "support": [round(s, 2) for s in final_supports],
        "resistance": [round(r, 2) for r in final_resistances],
        "current_price": round(last_price, 2)
    }