import yfinance as yf
import pandas_ta as ta
from flask import jsonify

def get_stock_history(ticker, start_date, end_date):
    try:
        data = yf.Ticker(ticker).history(start=start_date, end=end_date)
        if data.empty:
            return jsonify({"error": "No data found for the given ticker and date range."}), 404

        # Calculate indicators
        data.ta.rsi(length=6, append=True)
        data.ta.macd(append=True)
        for length in [5, 10, 20, 30, 50]:
            data.ta.sma(length=length, append=True)

        data.reset_index(inplace=True)
        data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')

        return jsonify(data.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
