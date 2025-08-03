from flask import Blueprint, jsonify, request
from .services import get_macd_analysis

macd_analysis_blueprint = Blueprint('macd_analysis', __name__)

@macd_analysis_blueprint.route('/macd_analysis', methods=['GET'])
def macd_analysis():
    """
    Get MACD analysis for a stock.
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
      - name: direction
        in: query
        type: string
        required: true
        enum: ['positive', 'negative']
        description: Whether the MACD histogram has turned positive or negative.
      - name: ma_filter
        in: query
        type: string
        required: false
        description: A comma-separated list of MAs to check against (e.g., 5,10,20).
    responses:
      200:
        description: A table of MACD analysis results.
      400:
        description: Invalid parameters.
    """
    ticker = request.args.get('ticker')
    period = request.args.get('period')
    direction = request.args.get('direction')
    ma_filter_str = request.args.get('ma_filter')

    if not all([ticker, period, direction]):
        return jsonify({"error": "Missing required parameters"}), 400

    if period not in ['daily', 'weekly'] or direction not in ['positive', 'negative']:
        return jsonify({"error": "Invalid parameter value"}), 400

    ma_filter = []
    if ma_filter_str:
        try:
            ma_filter = [int(ma) for ma in ma_filter_str.split(',')]
        except ValueError:
            return jsonify({"error": "Invalid ma_filter format"}), 400

    analysis = get_macd_analysis(ticker, period, direction, ma_filter)
    return jsonify(analysis)