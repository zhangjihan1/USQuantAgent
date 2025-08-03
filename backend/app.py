from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

from api.support_resistance.routes import support_resistance_blueprint
from api.expected_move.routes import expected_move_blueprint
from api.rsi_analysis.routes import rsi_analysis_blueprint
from api.macd_analysis.routes import macd_analysis_blueprint
from api.macd_trend.routes import macd_trend_blueprint
from api.stock_history.routes import stock_history_blueprint

app = Flask(__name__)
app.register_blueprint(support_resistance_blueprint, url_prefix='/api')
app.register_blueprint(expected_move_blueprint, url_prefix='/api')
app.register_blueprint(rsi_analysis_blueprint, url_prefix='/api')
app.register_blueprint(macd_analysis_blueprint, url_prefix='/api')
app.register_blueprint(macd_trend_blueprint, url_prefix='/api')
app.register_blueprint(stock_history_blueprint, url_prefix='/api')
CORS(app)
swagger = Swagger(app)

@app.route('/')
def index():
    """
    A simple endpoint to test if the server is running.
    ---
    responses:
      200:
        description: A simple hello world message
        examples:
          text/plain: Hello, World!
    """
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)