from flask import Blueprint, jsonify, request
from .services import get_macd_trend

macd_trend_blueprint = Blueprint('macd_trend', __name__)

@macd_trend_blueprint.route('/macd_trend', methods=['GET'])
def macd_trend():
    """
    Get MACD trend analysis for a stock.
    ---
    parameters:
      - name: ticker
        in: query
        type: string
        required: true
        description: The stock ticker symbol (e.g., AAPL).
      - name: period
        in: query
        type: string
        required: true
        enum: ['daily', 'weekly']
        description: The time period for MACD calculation.
      - name: start_date
        in: query
        type: string
        required: true
        description: The start date for the analysis (YYYY-MM-DD).
      - name: end_date
        in: query
        type: string
        required: true
        description: The end date for the analysis (YYYY-MM-DD).
    responses:
      200:
        description: A table of MACD trend analysis results.
      400:
        description: Invalid parameters.
    """
    ticker = request.args.get('ticker')
    period = request.args.get('period')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not all([ticker, period, start_date, end_date]):
        return jsonify({"error": "Missing required parameters"}), 400

    if period not in ['daily', 'weekly']:
        return jsonify({"error": "Invalid period value"}), 400

    analysis = get_macd_trend(ticker, period, start_date, end_date)
    return jsonify(analysis)