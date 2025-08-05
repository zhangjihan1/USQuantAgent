import yfinance as yf
import numpy as np
import datetime

def get_expected_move(ticker):
    """
    Calculates the expected price move for a given stock ticker for the next 4 weekly expirations.
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
        try:
            opts = stock.option_chain(expiration_str)
        except Exception:
            # If option chain for a specific date fails, skip it.
            continue

        if opts.calls.empty or opts.puts.empty:
            continue

        # Find the at-the-money (ATM) strike
        atm_strike = min(opts.calls['strike'], key=lambda x:abs(x-last_price))
        
        # Get the IV for the ATM call and put
        try:
            atm_call = opts.calls[opts.calls['strike'] == atm_strike]
            atm_put = opts.puts[opts.puts['strike'] == atm_strike]

            if atm_call.empty or atm_put.empty:
                continue

            atm_call_iv = atm_call['impliedVolatility'].iloc[0]
            atm_put_iv = atm_put['impliedVolatility'].iloc[0]
        except (IndexError, KeyError):
            # Skip if IV is not available for this strike
            continue

        # Average the IV
        avg_iv = (atm_call_iv + atm_put_iv) / 2
        
        # Calculate days to expiration
        days_to_expiration = (expiration_date - today).days
        
        # If DTE is 0, it can cause a division by zero or meaningless result, so skip.
        if days_to_expiration <= 0:
            continue

        # Calculate expected move
        expected_move = last_price * avg_iv * np.sqrt(days_to_expiration / 365)
        
        results.append({
            "ticker": ticker,
            "last_price": round(last_price, 2),
            "expiration_date_used_for_iv": expiration_str,
            "atm_strike": atm_strike,
            "implied_volatility_percent": round(avg_iv * 100, 2),
            "days_to_expiration_used_in_calc": days_to_expiration,
            "expected_move": round(expected_move, 2),
            "expected_upper_move": round(last_price + expected_move, 2),
            "expected_lower_move": round(last_price - expected_move, 2)
        })

    if not results:
        return {"error": "Could not calculate expected move for any upcoming weekly expiration."}

    return results