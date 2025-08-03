from flask import Blueprint, jsonify, request
import yfinance as yf

stock_history_blueprint = Blueprint('stock_history', __name__)

@stock_history_blueprint.route('/stock_history', methods=['GET'])
def stock_history():
    """
    Get historical stock data.
    ---
    parameters:
      - name: ticker
        in: query
        type: string
        required: true
        description: The stock ticker symbol (e.g., AAPL).
    responses:
      200:
        description: A list of historical stock data.
      400:
        description: Invalid ticker symbol.
    """
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({"error": "Ticker symbol is required"}), 400

    stock = yf.Ticker(ticker)
    hist = stock.history(period="3y")
    hist.reset_index(inplace=True)
    hist['Date'] = hist['Date'].dt.strftime('%Y-%m-%d')
    return jsonify(hist.to_dict(orient='records'))