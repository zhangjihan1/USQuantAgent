import yfinance as yf
import pandas as pd
import pandas_ta as ta
import numpy as np

def get_macd_trend(ticker, period, start_date, end_date):
    """
    Performs MACD trend analysis on a stock.
    """
    interval = '1d' if period == 'daily' else '1wk'
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date, interval=interval)
    if data.empty:
        return {"error": "Could not download data for the ticker in the specified date range."}

    data.ta.macd(append=True)

    trends = []
    in_trend = False
    trend_start_date = None
    trend_type = None

    for i in range(1, len(data)):
        # Start of a new trend
        if not in_trend:
            if data['MACDh_12_26_9'][i] > 0 and data['MACDh_12_26_9'][i-1] < 0:
                in_trend = True
                trend_start_date = data.index[i]
                trend_type = 'uptrend'
            elif data['MACDh_12_26_9'][i] < 0 and data['MACDh_12_26_9'][i-1] > 0:
                in_trend = True
                trend_start_date = data.index[i]
                trend_type = 'downtrend'
        # End of a trend
        elif (trend_type == 'uptrend' and data['MACDh_12_26_9'][i] < 0) or \
             (trend_type == 'downtrend' and data['MACDh_12_26_9'][i] > 0):
            
            trend_end_date = data.index[i]
            start_price = data.loc[trend_start_date, 'Close']
            end_price = data.loc[trend_end_date, 'Close']
            price_change = ((end_price - start_price) / start_price) * 100
            
            trends.append({
                "start_date": trend_start_date.strftime('%Y-%m-%d'),
                "end_date": trend_end_date.strftime('%Y-%m-%d'),
                "trend": trend_type,
                "price_change": round(price_change, 2)
            })
            in_trend = False

    return {"trends": trends}