import yfinance as yf
from database import SessionLocal
from models import StockData
from datetime import datetime
import pandas as pd

def fetch_and_save(ticker: str):
    df = yf.download(ticker, period='1mo')

    # RSI 計算
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    db = SessionLocal()

    for index, row in df.iterrows():
        db_stock = StockData(
            ticker=ticker,
            date=index.date(),
            open=row['Open'],
            high=row['High'],
            low=row['Low'],
            close=row['Close'],
            volume=row['Volume'],
            rsi=row['RSI'] if not pd.isna(row['RSI']) else None
        )
        db.add(db_stock)

    db.commit()
    db.close()