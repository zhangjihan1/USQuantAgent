from flask import Blueprint, request
from .services import get_stock_history

stock_history_blueprint = Blueprint('stock_history_bp', __name__)

@stock_history_blueprint.route('/stock_history', methods=['GET'])
def stock_history_route():
    ticker = request.args.get('ticker')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    return get_stock_history(ticker, start_date, end_date)
