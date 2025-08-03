from flask import Blueprint, jsonify, request
from .services import get_rsi_analysis

rsi_analysis_blueprint = Blueprint('rsi_analysis', __name__)

@rsi_analysis_blueprint.route('/rsi_analysis', methods=['GET'])
def rsi_analysis():
    """
    Get RSI analysis for a stock.
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
        description: The time period for RSI calculation.
      - name: condition
        in: query
        type: string
        required: true
        enum: ['large', 'small']
        description: Whether the RSI should be larger or smaller than the threshold.
      - name: threshold
        in: query
        type: number
        required: true
        description: The RSI threshold value.
    responses:
      200:
        description: A table of RSI analysis results.
      400:
        description: Invalid parameters.
    """
    ticker = request.args.get('ticker')
    period = request.args.get('period')
    condition = request.args.get('condition')
    threshold = request.args.get('threshold', type=float)

    if not all([ticker, period, condition, threshold is not None]):
        return jsonify({"error": "Missing required parameters"}), 400

    if period not in ['daily', 'weekly'] or condition not in ['large', 'small']:
        return jsonify({"error": "Invalid parameter value"}), 400

    analysis = get_rsi_analysis(ticker, period, condition, threshold)
    return jsonify(analysis)