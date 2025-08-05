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
        data.ta.ema(length=length, append=True)

    # Rename columns to be more generic
    data.rename(columns={
        "RSI_6": "rsi",
        "MACD_12_26_9": "macd_value",
        "MACDh_12_26_9": "macd_histogram",
        "MACDs_12_26_9": "macd_signal",
        "EMA_5": "ema5",
        "EMA_10": "ema10",
        "EMA_20": "ema20",
        "EMA_30": "ema30",
        "EMA_50": "ema50",
    }, inplace=True)

    # Nest MACD fields if they exist
    if 'macd_value' in data.columns and 'macd_signal' in data.columns and 'macd_histogram' in data.columns:
        data['macd'] = data.apply(lambda row: {
            'macd': row['macd_value'],
            'signal': row['macd_signal'],
            'divergence': row['macd_histogram']
        }, axis=1)
        data.drop(columns=['macd_value', 'macd_signal', 'macd_histogram'], inplace=True)
    else:
        data['macd'] = None

    data.reset_index(inplace=True)
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
    data.columns = [col.lower() for col in data.columns]


    # Replace NaN with None for valid JSON
    data = data.replace({np.nan: None})
    return data.to_dict(orient='records')
