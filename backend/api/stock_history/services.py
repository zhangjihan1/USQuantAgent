import yfinance as yf
import pandas_ta as ta
import numpy as np
def get_stock_history(ticker, start_date, end_date):
    data = yf.Ticker(ticker).history(start=start_date, end=end_date)
    if data.empty:
        return []

    data.reset_index(inplace=True)
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
    data.columns = [col.lower() for col in data.columns]


    # Replace NaN with None for valid JSON
    data = data.replace({np.nan: None})
    return data.to_dict(orient='records')
