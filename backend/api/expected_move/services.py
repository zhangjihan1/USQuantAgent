import yfinance as yf
import numpy as np
import datetime

def get_expected_move(ticker):
    """
    Calculates the expected price move for a given stock ticker based on option IV.
    """
    stock = yf.Ticker(ticker)
    
    # Get the stock's current price
    last_price = stock.history(period="1d")['Close'].iloc[-1]
    
    # Get the option chain
    expirations = stock.options
    if not expirations:
        return {"error": "No options data available for this ticker."}

    # Find the next weekly expiration (a Friday)
    today = datetime.date.today()
    next_friday = today + datetime.timedelta((4 - today.weekday()) % 7)
    
    # Find the closest expiration date in the options chain
    expiration_dates = [datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in expirations]
    
    # Find the expiration that is a Friday and is closest to our target Friday
    friday_expirations = [d for d in expiration_dates if d.weekday() == 4 and d >= today]
    if not friday_expirations:
        return {"error": "Could not find a suitable weekly expiration."}
        
    closest_expiration_date = min(friday_expirations, key=lambda d: abs(d - next_friday))
    closest_expiration_str = closest_expiration_date.strftime('%Y-%m-%d')

    # Get the options for that expiration
    opts = stock.option_chain(closest_expiration_str)
    
    # Find the at-the-money (ATM) strike
    atm_strike = min(opts.calls['strike'], key=lambda x:abs(x-last_price))
    
    # Get the IV for the ATM call and put
    atm_call_iv = opts.calls[opts.calls['strike'] == atm_strike]['impliedVolatility'].iloc[0]
    atm_put_iv = opts.puts[opts.puts['strike'] == atm_strike]['impliedVolatility'].iloc[0]
    
    # Average the IV
    avg_iv = (atm_call_iv + atm_put_iv) / 2
    
    # Calculate days to expiration
    days_to_expiration = (closest_expiration_date - today).days
    
    # Calculate expected move
    expected_move = last_price * avg_iv * np.sqrt(days_to_expiration / 365)
    
    return {
        "expected_upper_move": round(last_price + expected_move, 2),
        "expected_lower_move": round(last_price - expected_move, 2)
    }