import yfinance as yf
import numpy as np
import datetime

def get_expected_move(ticker):
    """
    Calculates the expected price move for a given stock ticker for the next 4 weekly expirations.
    """
    stock = yf.Ticker(ticker)
    
    # Get the stock's current price
    last_price = stock.history(period="1d")['Close'].iloc[-1]
    
    # Get the option chain expirations
    expirations = stock.options
    if not expirations:
        return {"error": "No options data available for this ticker."}

    # Find upcoming Friday expirations
    today = datetime.date.today()
    expiration_dates = [datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in expirations]
    friday_expirations = sorted([d for d in expiration_dates if d.weekday() == 4 and d >= today])

    if not friday_expirations:
        return {"error": "Could not find any suitable weekly expirations."}

    results = []
    
    # Calculate expected move for the next up to 4 weekly expirations
    for expiration_date in friday_expirations[:4]:
        expiration_str = expiration_date.strftime('%Y-%m-%d')
        
        # Get the options for that expiration
        opts = stock.option_chain(expiration_str)
        
        # Find the at-the-money (ATM) strike
        atm_strike = min(opts.calls['strike'], key=lambda x:abs(x-last_price))
        
        # Get the IV for the ATM call and put
        try:
            atm_call_iv = opts.calls[opts.calls['strike'] == atm_strike]['impliedVolatility'].iloc[0]
            atm_put_iv = opts.puts[opts.puts['strike'] == atm_strike]['impliedVolatility'].iloc[0]
        except IndexError:
            # Skip if IV is not available for this strike
            continue

        # Average the IV
        avg_iv = (atm_call_iv + atm_put_iv) / 2
        
        # Calculate days to expiration
        days_to_expiration = (expiration_date - today).days
        
        # Calculate expected move
        expected_move = last_price * avg_iv * np.sqrt(days_to_expiration / 365)
        
        results.append({
            "expiration_date": expiration_str,
            "expected_upper_move": round(last_price + expected_move, 2),
            "expected_lower_move": round(last_price - expected_move, 2)
        })

    return results