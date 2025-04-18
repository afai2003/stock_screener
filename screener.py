import yfinance as yf
import pandas as pd

def calculate_rsi(df, window=14):
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def screen_stocks(rsi_threshold=30):
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    matched = []

    for ticker in tickers:
        df = yf.download(ticker, period='1mo')
        df['RSI'] = calculate_rsi(df)
        latest_rsi = df['RSI'].iloc[-1]

        if latest_rsi < rsi_threshold:
            matched.append({
                "ticker": ticker,
                "RSI": round(latest_rsi, 2)
            })

    return matched