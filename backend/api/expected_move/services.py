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
        
        # Calculate the expected move from the at-the-money (ATM) straddle price.
        # This is a more reliable method than using the 'impliedVolatility' field directly,
        # especially around events like earnings.
        try:
            atm_call = opts.calls[opts.calls['strike'] == atm_strike]
            atm_put = opts.puts[opts.puts['strike'] == atm_strike]

            if atm_call.empty or atm_put.empty:
                continue

            # Use the mid-price (average of bid and ask) for better accuracy.
            # Fallback to lastPrice if bid/ask is not available.
            atm_call_bid = atm_call['bid'].iloc[0]
            atm_call_ask = atm_call['ask'].iloc[0]
            if atm_call_bid == 0 or atm_call_ask == 0:
                atm_call_price = atm_call['lastPrice'].iloc[0]
            else:
                atm_call_price = (atm_call_bid + atm_call_ask) / 2

            atm_put_bid = atm_put['bid'].iloc[0]
            atm_put_ask = atm_put['ask'].iloc[0]
            if atm_put_bid == 0 or atm_put_ask == 0:
                atm_put_price = atm_put['lastPrice'].iloc[0]
            else:
                atm_put_price = (atm_put_bid + atm_put_ask) / 2
            
            expected_move = atm_call_price + atm_put_price

            # Calculate days to expiration
            days_to_expiration = (expiration_date - today).days
            if days_to_expiration <= 0:
                continue

            # Back-calculate the implied volatility from the expected move for display purposes.
            # Formula: IV = (Expected Move / Stock Price) / sqrt(DTE / 365)
            if last_price > 0 and days_to_expiration > 0:
                avg_iv = (expected_move / last_price) / np.sqrt(days_to_expiration / 365)
            else:
                avg_iv = 0

        except (IndexError, KeyError):
            # Skip if essential option data is not available for this strike
            continue
        
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