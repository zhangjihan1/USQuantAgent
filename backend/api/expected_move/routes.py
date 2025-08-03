from flask import Blueprint, jsonify, request
from .services import get_expected_move

expected_move_blueprint = Blueprint('expected_move', __name__)

@expected_move_blueprint.route('/expected_move', methods=['GET'])
def expected_move():
    """
    Get the expected price move for a stock.
    ---
    parameters:
      - name: ticker
        in: query
        type: string
        required: true
        description: The stock ticker symbol (e.g., AAPL).
    responses:
      200:
        description: The expected upper and lower price moves.
        schema:
          type: object
          properties:
            expected_upper_move:
              type: number
            expected_lower_move:
              type: number
      400:
        description: Invalid ticker symbol.
    """
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({"error": "Ticker symbol is required"}), 400

    move = get_expected_move(ticker)
    return jsonify(move)