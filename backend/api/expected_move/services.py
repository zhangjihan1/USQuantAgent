import yfinance as yf
import numpy as np
import datetime

def get_expected_move(ticker):
    """
    Calculates the weekly expected price move for a given stock ticker based on the nearest option expiration.
    """
    stock = yf.Ticker(ticker)
    
    # Get the stock's current price
    try:
        last_price = stock.history(period="1d")['Close'].iloc[-1]
    except IndexError:
        return {"error": "Could not fetch the last price for the ticker."}

    # Get the option chain expirations
    expirations = stock.options
    if not expirations:
        return {"error": "No options data available for this ticker."}

    # Find the nearest upcoming expiration date
    today = datetime.date.today()
    expiration_dates = [datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in expirations]
    upcoming_expirations = sorted([d for d in expiration_dates if d >= today])

    if not upcoming_expirations:
        return {"error": "Could not find any suitable upcoming expirations."}

    # Use the nearest expiration to get the IV
    next_expiration_date = upcoming_expirations[0]
    expiration_str = next_expiration_date.strftime('%Y-%m-%d')
    
    # Get the options for that expiration
    opts = stock.option_chain(expiration_str)
    
    if opts.calls.empty or opts.puts.empty:
        return {"error": f"No calls or puts data for expiration {expiration_str}."}

    # Find the at-the-money (ATM) strike
    # Find the strike price closest to the last stock price
    atm_strike = min(opts.calls['strike'], key=lambda x: abs(x - last_price))
    
    # Get the IV for the ATM call and put
    try:
        atm_call = opts.calls[opts.calls['strike'] == atm_strike]
        atm_put = opts.puts[opts.puts['strike'] == atm_strike]
        
        if atm_call.empty or atm_put.empty:
            return {"error": f"No ATM options found for strike {atm_strike} on {expiration_str}."}

        atm_call_iv = atm_call['impliedVolatility'].iloc[0]
        atm_put_iv = atm_put['impliedVolatility'].iloc[0]
    except (IndexError, KeyError):
        return {"error": f"Could not find implied volatility for the ATM strike ({atm_strike}) on {expiration_str}."}

    # Average the IV
    avg_iv = (atm_call_iv + atm_put_iv) / 2
    
    # Per user instruction, use 7 days for a weekly calculation.
    days_to_expiration = 7
    
    # Calculate expected move using the user-provided formula
    # Expected Move = Stock Price × Implied Volatility × √(Days to Expiration / 365)
    expected_move = last_price * avg_iv * np.sqrt(days_to_expiration / 365)
    
    # The function will now return a single object with more details for clarity
    return {
        "ticker": ticker,
        "last_price": round(last_price, 2),
        "expiration_date_used_for_iv": expiration_str,
        "atm_strike": atm_strike,
        "implied_volatility_percent": round(avg_iv * 100, 2),
        "days_to_expiration_used_in_calc": days_to_expiration,
        "expected_move": round(expected_move, 2),
        "expected_upper_move": round(last_price + expected_move, 2),
        "expected_lower_move": round(last_price - expected_move, 2)
    }