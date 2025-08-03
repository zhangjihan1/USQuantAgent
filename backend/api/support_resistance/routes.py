from flask import Blueprint, jsonify, request
from .services import get_support_resistance

support_resistance_blueprint = Blueprint('support_resistance', __name__)

@support_resistance_blueprint.route('/support_resistance', methods=['GET'])
def support_resistance():
    """
    Get support and resistance levels for a stock.
    ---
    parameters:
      - name: ticker
        in: query
        type: string
        required: true
        description: The stock ticker symbol (e.g., AAPL).
    responses:
      200:
        description: A list of support and resistance levels.
        schema:
          type: object
          properties:
            support:
              type: array
              items:
                type: number
            resistance:
              type: array
              items:
                type: number
      400:
        description: Invalid ticker symbol.
    """
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({"error": "Ticker symbol is required"}), 400

    levels = get_support_resistance(ticker)
    return jsonify(levels)