import yfinance as yf
import pandas as pd
import pandas_ta as ta
import numpy as np

def get_rsi_analysis(ticker, period, condition, threshold):
    """
    Performs RSI analysis on a stock.
    """
    interval = '1d' if period == 'daily' else '1wk'
    stock = yf.Ticker(ticker)
    data = stock.history(period="10y", interval=interval)
    if data.empty:
        return {"error": "Could not download data for the ticker."}

    data.ta.rsi(length=14, append=True)
    
    if condition == 'large':
        triggered_dates = data[data['RSI_14'] > threshold].index
    else: # small
        triggered_dates = data[data['RSI_14'] < threshold].index

    results = []
    for date in triggered_dates:
        start_index = data.index.get_loc(date)
        
        # Ensure we have enough data for the following 5 weeks
        if start_index + 5 < len(data):
            price_changes = {}
            for week in range(1, 6):
                future_date = data.index[start_index + week]
                price_change = ((data.loc[future_date, 'Close'] - data.loc[date, 'Close']) / data.loc[date, 'Close']) * 100
                price_changes[f'week_{week}'] = round(price_change, 2)
            
            results.append({
                "date": date.strftime('%Y-%m-%d'),
                **price_changes
            })

    if not results:
        return {"message": "No data met the specified criteria."}

    # Calculate statistics
    df_results = pd.DataFrame(results)
    avg_changes = df_results.mean(numeric_only=True).to_dict()
    percentiles = {
        '25th': df_results.quantile(0.25, numeric_only=True).to_dict(),
        '50th': df_results.quantile(0.50, numeric_only=True).to_dict(),
        '75th': df_results.quantile(0.75, numeric_only=True).to_dict(),
        '90th': df_results.quantile(0.90, numeric_only=True).to_dict(),
    }

    return {
        "table_data": results,
        "summary": {
            "average_changes": avg_changes,
            "percentiles": percentiles
        }
    }