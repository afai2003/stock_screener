from fastapi import FastAPI
from screener import screen_stocks
from data_collector import fetch_and_save

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Stock Screener API is running"}

@app.get("/screen")
def screen(rsi_lt: float = 30):
    results = screen_stocks(rsi_lt)
    return {"matched_stocks": results,
            "message": "hihi"}

@app.post("/fetch")
def fetch(ticker: str = "AAPL"):
    fetch_and_save(ticker)
    return {"status": "ok"}