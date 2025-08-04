import yfinance as yf
import pandas_ta as ta
import numpy as np
def get_stock_history(ticker, start_date, end_date):
    data = yf.Ticker(ticker).history(start=start_date, end=end_date)
    if data.empty:
        return []

    # Calculate indicators
    data.ta.rsi(length=6, append=True)
    data.ta.macd(append=True)
    for length in [5, 10, 20, 30, 50]:
        data.ta.sma(length=length, append=True)

    data.reset_index(inplace=True)
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')

    # Replace NaN with None for valid JSON
    data = data.replace({np.nan: None})
    return data.to_dict(orient='records')
